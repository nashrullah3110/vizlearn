# -*- coding: utf-8 -*-
"""Content for the Pydantic track.

Tier one: the seven modules that get a reader from "what is this for" to
"I can define a model and read its errors".

Two things shape every page here.

**Many small programs, not one big one.** The Python track puts two
substantial programs on a page. That works when the subject is a language
feature, but Pydantic is a stack of small rules that interact, and one long
script hides which rule produced which line. So a module here is a sequence
of steps, each a heading, a sentence, and a program short enough to hold in
your head - and each one runnable on its own.

**Every program prints something that answers the question.** Several are
written so the output contradicts the guess a reader would make: that
`Optional` means optional, that `"36"` stays a string, that a validation
error stops at the first problem. Being wrong on the page and seeing it
immediately is the point.

Examples use VizLearn's own domain - courses, tracks, modules, readers -
rather than the foo/bar of the docs, so the data has a shape worth arguing
about.
"""

TOPICS = []
CHECKS = {}


def topic(slug, title, cat, lead, svg, steps, notes, article, check,
          wheels=None, prelude=None):
    """One module. `steps` is a list of (heading, blurb, code) triples.

    `wheels` names extra .whl files this module's editors need on top of the
    Pyodide-shipped pydantic - tier five needs pydantic-settings and the
    FastAPI stack. `prelude` is setup code run before the reader's, in the
    same namespace and not shown in the editor.
    """
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "steps": steps, "notes": notes, "article": article, "check": check,
        "wheels": wheels or [], "prelude": prelude or "",
    })
    # build_labs.py expects {"check": [...]}, not the bare list - the same
    # shape python_topics.CHECKS uses.
    CHECKS["pydantic/%s.html" % slug] = {"check": check}


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
# 1. What Pydantic is for
# ---------------------------------------------------------------------------
topic(
    "what_is_pydantic",
    "What Pydantic Is For",
    "Foundations",
    "A type annotation does nothing at runtime. Pydantic is the library that "
    "makes it mean something.",
    _svg(_box(14, 30, 40, 30, S) + _txt(34, 49, '"12"', M) +
         _arrow(58, 45, 76, 45) +
         _box(80, 26, 34, 38, S, A) + _txt(97, 42, "check", A, 8) + _txt(97, 54, "coerce", A, 8) +
         _arrow(118, 45, 136, 45) +
         _txt(148, 49, "12", A)),
    [
        ("A type hint is only a note to the reader",
         "Python does not check annotations at runtime. This function promises an "
         "<code>int</code> and is handed a string, and Python raises nothing at all "
         "&mdash; the failure arrives later, somewhere else, as something confusing.",
         '''# The annotation says int. Python does not care.
def modules_left(count: int) -> str:
    return "You have " + str(count) + " modules to go"

print(modules_left(12))
print(modules_left("twelve"))     # no error - the annotation is decoration
print(modules_left(None))         # still no error

# The damage shows up later, in arithmetic that should have worked:
def halfway(count: int) -> float:
    return count / 2

print(halfway(12))
try:
    print(halfway("twelve"))
except TypeError as e:
    print("TypeError:", e)        # <- the real failure, far from the cause'''),

        ("The same promise, enforced",
         "A Pydantic model reads the same annotations and actually applies them. "
         "Nothing about the type declarations changed &mdash; only who is reading them.",
         '''from pydantic import BaseModel, ValidationError

class Reader(BaseModel):
    name: str
    modules_done: int

ok = Reader(name="Ada", modules_done=12)
print("valid  :", ok)

try:
    Reader(name="Ada", modules_done="twelve")
except ValidationError as e:
    print("caught :", e.errors()[0]["msg"])

# The point: the failure happens here, at the moment the bad value arrives,
# not three functions later when someone tries to divide by it.'''),

        ("It converts, not just complains",
         "Data arriving from JSON, a form or a query string is text. Pydantic "
         "converts what can be converted and rejects what cannot, so the rest of "
         "your program works with real types.",
         '''from pydantic import BaseModel

class Module(BaseModel):
    title: str
    minutes: int
    published: bool

# Everything here arrives as a string, the way a web form would send it.
m = Module(title="Vectors", minutes="9", published="true")

print(m)
print("minutes is  :", type(m.minutes).__name__, "->", m.minutes + 1)
print("published is:", type(m.published).__name__, "->", not m.published)

# Try changing "9" to "nine" and running this again.'''),

        ("Errors that name the problem",
         "When it does refuse, it refuses with detail: which field, what was wrong, "
         "and what it actually received. Every field is checked, so you get the whole "
         "list rather than the first failure.",
         '''from pydantic import BaseModel, ValidationError

class Module(BaseModel):
    title: str
    minutes: int
    published: bool

try:
    Module(title=None, minutes="nine", published="maybe")
except ValidationError as e:
    print("problems found:", e.error_count())
    print()
    for err in e.errors():
        print("field :", err["loc"][0])
        print("  said:", err["msg"])
        print("  got :", repr(err["input"]))
        print()'''),

        ("Where a model belongs",
         "Pydantic earns its place at the <strong>boundary</strong> &mdash; the line "
         "where data you did not write enters code you did. Validate once on the way "
         "in, and everything downstream can stop guessing.",
         '''import json
from pydantic import BaseModel, ValidationError

# Pretend this arrived from an API, a file, or a form post.
payload = '{"title": "Dot Product", "minutes": "11", "published": "yes"}'

class Module(BaseModel):
    title: str
    minutes: int
    published: bool

module = Module.model_validate_json(payload)   # one line: parse AND check
print("parsed  :", module)

# From here on, minutes really is an int. No isinstance checks needed.
def reading_time(m: Module) -> str:
    return "about %d minutes" % round(m.minutes * 1.2)

print("derived :", reading_time(module))

bad = '{"title": "Norms", "minutes": "a while", "published": "yes"}'
try:
    Module.model_validate_json(bad)
except ValidationError as e:
    print("rejected:", e.errors()[0]["msg"])'''),

        ("What you get for free",
         "Because the model already describes the data precisely, it can also hand "
         "that description to other tools &mdash; as a dict, as JSON, or as a schema "
         "that documentation and API tooling can read.",
         '''from pydantic import BaseModel

class Module(BaseModel):
    title: str
    minutes: int
    published: bool

m = Module(title="Eigenvalues", minutes=14, published=True)

print("as a dict :", m.model_dump())
print("as JSON   :", m.model_dump_json())
print()
print("the schema it generated:")
schema = m.model_json_schema()
for name, spec in schema["properties"].items():
    print("  %-10s %s" % (name, spec.get("type")))
print("  required:", schema["required"])'''),
    ],
    [
        "Pydantic does not replace type hints &mdash; it reads the ones you already write. The annotation is the schema.",
        "Validation happens when a model is <em>created</em>. Assigning to an attribute afterwards is not checked unless you ask for it with <code>model_config = ConfigDict(validate_assignment=True)</code>.",
        "<code>model_validate_json</code> parses and validates in one step. It is faster than <code>json.loads</code> followed by <code>model_validate</code>, because the parsing happens in Rust.",
        "Pydantic v2's core is written in Rust. That is why validating at the boundary is cheap enough to do on every request.",
        "The library is used by FastAPI, LangChain, HuggingFace and most of the modern Python API stack. Learning it once pays off across all of them.",
        "If a value is <em>already</em> the right type, validation is nearly free &mdash; there is nothing to convert.",
    ],
    '''
title: What Pydantic Is For, and the Problem It Solves
intro: Python's type annotations do nothing on their own. This is the library that makes them real.

## The gap between what you wrote and what runs

Pydantic takes a Python class with type annotations and turns it into a data validator. You define a model, pass in a dictionary or JSON, and get back a typed object if the data fits. If it does not, you get an error that names every field that failed and why.

That description sounds simple, but the range of what it covers is wide. Pydantic handles type coercion, so a string "42" arriving from JSON becomes the integer 42 without any code from you. It produces JSON Schema from your models, which feeds OpenAPI docs when used with a framework like FastAPI. It validates nested structures, enforces constraints on individual fields, and gives you hooks for custom logic that runs during validation.

This article explains what problem Pydantic solves, how it differs from plain dataclasses, and what coercion means in practice. It then covers the error format, the extra things a model gives you beyond validation, and the common expectations people bring that do not match how the library actually works. The final section maps out where the rest of the track goes.

Write a function like this and you've made a promise:

```python
def modules_left(count: int) -> str:
    return "You have " + str(count) + " modules to go"
```

The promise is that `count` is a whole number. Python doesn't keep it. Annotations are stored on the function object and else skipped at runtime. They exist for human readers, editors and type checkers like mypy, none of which are present when your program is really running. Call `modules_left("twelve")` and Python does just what you asked. It concatenates strings and returns a sentence that reads fine.

That is a small problem when the wrong value is only printed. It turns a real one the moment a thing math happens. A string that has been travelling through three function calls disguised as an int fails at the point it's finally cut. The traceback points at the division, not at the front door where the bad value walked in.

This is the gap Pydantic fills. It reads the annotations you already write and enforces them, at a moment you choose.

## Validation is a boundary problem

Almost no bad data originates inside your program. It arrives. From a JSON request body, a form post, a config file, a CSV, a DB column that has been nullable since 2019, an setting var, another team's API. all that crosses into your code from outside is, until proven else, a guess.

The handy discipline is to check that data once, at the edge. Convert it into a thing trustworthy. After that line, each function downstream can assume the shape is right and stop defending itself. The option. An `isinstance` check at the top of each function, or worse, no check and a hope. Spreads the same anxiety through the whole code.

A Pydantic model is that boundary written down. It's a class whose annotations show what you need. Making one is the act of checking.

```python
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    minutes: int
    published: bool
```

Three lines, and you now have a thing that will refuse to exist unless the data fits.

## Coercion: the part people do not expect

The first surprise for most people is that Pydantic doesn't merely check. It converts. Hand the model above `minutes="9"` and you get back an int `9`, not an error.

That is deliberate, and it follows from where models are used. Data crossing a boundary is often text. A query string has no ints in it. An HTML form sends strings. A CSV is strings all the way down. If a model rejected all that arrived as text, you'd spend your life writing `int(request.args["minutes"])` and catching `ValueError` by hand. Which is just the code Pydantic exists to delete.

So the default action, called **lax mode**, is to accept anything that has an unambiguous reading. `"9"` turns `9`. `9.0` turns `9`. `"true"`, `"yes"` and `1` all become `True`. But `"nine"` doesn't become anything. There's no unambiguous reading. Neither does `9.5`, because turning it into `9` would silently lose data you might have needed.

Where that trade is wrong. And at times it's, above all deep inside a system where types should already be correct &mdash; strict mode is on hand. Gets a module of its own later in this track.

## Errors that are worth reading

The second thing that sets apart Pydantic from a hand-written check is the quality of its refusals.

A hand-written checker often raises on the first problem it meets. The caller fixes that one, resubmits. Discovers the next. Pydantic checks each field and raises once, carrying the full list. For a form, that is the gap between one error message at a time and a form that highlights all four broken inputs at once.

Each entry in that list has three parts worth reading apart.

The **location** is a path, not a name. For a flat model it's just the field. For anything nested it shows the route: `address.pin` is one level down, `modules.2.minutes` is the `minutes` field of the third item in a list. When a payload is deep, this is the fastest way to find the offending value.

The **type** is a stable machine-readable code. `int_parsing`, `string_too_short`, `greater_than`. Not a sentence. It's what you match on if you're converting errors into an API response or a translated message. It won't change underneath you when the wording is better.

The **input** is the value that was really received. Nine times in ten, seeing it's the whole diagnosis. You expected a number and the caller sent `"null"` as a string.

## What else the model buys you

Once the shape of your data is written down just enough to validate against, it's written down just enough for other things too.

`model_dump()` gives you a plain dict. `model_dump_json()` gives you a JSON string, handling the types. Dates, UUIDs, decimals. That `json.dumps` refuses. And `model_json_schema()` makes a JSON Schema doc showing the model.

That last one is quietly the reason Pydantic is all over. FastAPI doesn't have its own check layer. It uses Pydantic. It turns those made schemas into the interactive docs you get for free at `/docs`. The same method drives structured output in LLM libraries. Here The schema tells the model what shape to answer in. You show your data once. A few tools read that description.

## What it is not

Pydantic isn't an ORM, though it's often paired with one. It doesn't talk to your DB. A model isn't a table.

It isn't a static type checker either. Mypy analyses code without running it. Pydantic checks values while the program runs. They complement each other rather than compete, and using both is normal.

And it isn't free. check costs a thing. This Is just why the boundary discipline matters. Validate on the way in, once. Then trust the result rather than re-checking the same object at each layer.

## What the hand-written version looks like

It's worth seeing the code Pydantic replaces. The compare shows a few of its design choices at once.

```python
def parse_module(raw):
    if not isinstance(raw, dict):
        raise ValueError("expected an object")
    title = raw.get("title")
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    minutes = raw.get("minutes")
    if isinstance(minutes, str):
        try:
            minutes = int(minutes)
        except ValueError:
            raise ValueError("minutes must be a number")
    elif not isinstance(minutes, int):
        raise ValueError("minutes must be a number")
    return {"title": title, "minutes": minutes}
```

Fifteen lines for two fields, and it's already worse than it looks. It stops at the first error. A caller with two mistakes discovers them one at a time. Its messages don't say which field failed in a machine-readable way. It has no idea what to do about a third field when somebody adds one, and nothing forces that person to note this function exists. And it shows the same shape a second time, in prose, in what docs exists.

The Pydantic version is the class meaning and nothing else. each one of those problems is solved as a side effect rather than as an extra feature.

## The cost, and when it matters

check isn't free, and it's worth being concrete rather than reassuring.

Building a model does real work: reading a compiled schema, checking each field, converting where needed. Making the object. A plain class set does none of that. If you make millions of objects in a tight loop, you'll measure the gap.

Two things make it matter less than people fear. The first is that Pydantic v2 does the work in Rust rather than Python. This Moved it from "noticeable" to "often irrelevant". The second is scale. A model that validates in single-digit microseconds sits next to a DB query taking milliseconds and a network call taking hundreds of milliseconds. In a common request handler, check is a rounding error on the request.

Where it truly matters is bulk. checking a hundred thousand rows from a file, or each element of a large array in a numeric pipeline, is a case where you should measure. The answer there's often not to abandon models but to validate the holder once rather than each item through a Python loop. This Is a topic the `TypeAdapter` module returns to.

The rule that follows is the one this article opened with. Validate at the boundary, once. Re-checking an object that has already passed is pure cost with no data gained.

## Where it came from, and why v2 matters

Pydantic v1 was pure Python. It was common enough to become a dependency of a large part of the ecosystem. Slow enough that its speed was a recurring complaint.

Version 2, released in 2023, kept the API broadly recognisable and rewrote the engine in Rust as a split package called `pydantic-core`. When you install `pydantic` you get both. A Python layer that reads your annotations and builds a schema. A compiled core that runs that schema against data.

This split shows a few things you'll notice. It's why check is fast. It's why the error `type` codes look like machine identifiers rather than sentences. They come from the core. It's why `model_validate_json` beats `json.loads` plus check. The core parses and validates in one pass without building mid Python objects. And it's why a wheel exists for each platform: there's compiled code in there.

The hands-on result for you is about docs. A great deal of Pydantic material online predates v2 and shows an API that has moved. The solid signals. V1 uses `@checker`, `.dict()`, `.json()` and `class Config`. V2 uses `@field_validator`, `.model_dump()`, `.model_dump_json()` and `model_config`. If an article uses the first set, treat all in it as historical.

## Four things people expect it to be

**An ORM.** It isn't, and it doesn't talk to a DB. It pairs well with one. SQLModel exists just to join them. But a model isn't a table and checking one doesn't persist anything.

**A static type checker.** Also no. Mypy and Pyright analyse code without running it and catch mistakes in your own source. Pydantic checks values at runtime and catches mistakes in data. They share in vocab and not in job. A serious code uses both.

**A output format.** `model_dump_json` makes JSON. Pydantic isn't competing with `json` or `msgpack`. It shows and checks the shape. The encoding is a service it offers on top.

**auto.** Nothing validates until you ask. A function annotated with a model type doesn't check its arg. Only making or checking a model does. There's a `@validate_call` decorator that brings the same checking to function args. It's opt-in for the same reason.

## The habit worth forming

When you find yourself writing `if not isinstance(...)`, or reaching into a dict with `.get()` and a default, or writing a comment that shows what shape a param is meant to have. That is a model waiting to be written.

The comment in given is the strongest signal. A sentence showing the shape of data is a schema that can't be ran, checked or kept honest. Turning it into a model costs about the same number of lines and can't go stale.

## Where this track goes

The next module builds a first model properly. Fields, needed versus optional. What you get back. After that comes the part all trips over. just which values Pydantic will convert and which it will refuse. How to read the error when it refuses.

The fastest way through all of it's to keep changing the values in the editors above and pressing Run. A rule you've watched break is a rule you note.
''',
    [
        {"q": "What does a plain Python type annotation do at runtime?",
         "options": ["Rejects wrong types", "Converts the value", "Nothing", "Logs a warning"],
         "answer": 2,
         "why": "Annotations are stored and ignored while the program runs. They serve readers, editors and static checkers. Pydantic is one of the tools that chooses to act on them."},
        {"q": "A model field is annotated `minutes: int` and receives the string `\"9\"`. What happens by default?",
         "options": ["ValidationError", "It becomes the integer 9", "It stays the string \"9\"", "It becomes None"],
         "answer": 1,
         "why": "Default lax mode converts anything with an unambiguous reading, because data crossing a boundary usually arrives as text. `\"nine\"` would raise, because there is no unambiguous reading."},
        {"q": "Why does Pydantic report every invalid field rather than stopping at the first?",
         "options": ["It is faster", "So a caller can fix everything in one pass", "To make errors longer", "It stops at the first by default"],
         "answer": 1,
         "why": "One raise carrying the full list means a form can highlight all its broken inputs at once, instead of revealing them one resubmission at a time."},
        {"q": "Where does a Pydantic model earn its place?",
         "options": ["At the boundary where outside data enters", "In every function", "Only in tests", "In the database layer"],
         "answer": 0,
         "why": "Validate once where untrusted data arrives, and everything downstream can assume the shape is correct. Re-checking at every layer costs time and adds no safety."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Your first BaseModel
# ---------------------------------------------------------------------------
topic(
    "your_first_basemodel",
    "Your First BaseModel",
    "Foundations",
    "Defining a model, creating one, reading it back, and turning it into a dict "
    "or JSON when you are done.",
    _svg(_box(20, 18, 120, 56, S) +
         _txt(80, 32, "class Module(BaseModel):", A, 8) +
         _txt(80, 46, "title: str", M, 8) +
         _txt(80, 60, "minutes: int", M, 8)),
    [
        ("Subclass, annotate, done",
         "A model is a class inheriting from <code>BaseModel</code> whose annotations "
         "list the fields. There is no <code>__init__</code> to write &mdash; Pydantic "
         "builds one from the annotations.",
         '''from pydantic import BaseModel

class Module(BaseModel):
    title: str
    track: str
    minutes: int

m = Module(title="Dot Product", track="maths", minutes=11)

print(m)
print()
print("one field  :", m.title)
print("another    :", m.minutes)
print("its type   :", type(m.minutes).__name__)'''),

        ("Keyword arguments, and why",
         "Fields are passed by name. Positional arguments are refused on purpose: a "
         "model can grow fields over time, and position would silently change meaning "
         "when it did.",
         '''from pydantic import BaseModel

class Module(BaseModel):
    title: str
    track: str
    minutes: int

# This is the way.
print(Module(title="Norms", track="maths", minutes=8))

# This is not:
try:
    Module("Norms", "maths", 8)
except TypeError as e:
    print("TypeError:", e)

# A dict works too, which is what you usually have from JSON.
data = {"title": "Norms", "track": "maths", "minutes": 8}
print(Module(**data))
print(Module.model_validate(data))     # the explicit version'''),

        ("Fields are ordinary attributes",
         "Once built, a model behaves like a normal object: attribute access, "
         "methods, everything. It is a class, not a dictionary wearing a hat.",
         '''from pydantic import BaseModel

class Module(BaseModel):
    title: str
    track: str
    minutes: int

    # Methods work exactly as they do on any class.
    def slug(self) -> str:
        return self.title.lower().replace(" ", "_")

    def is_long(self) -> bool:
        return self.minutes > 10

m = Module(title="Matrix Multiplication", track="maths", minutes=15)

print("title :", m.title)
print("slug  :", m.slug())
print("long? :", m.is_long())

# Reading a field that does not exist fails like any attribute would.
try:
    print(m.author)
except AttributeError as e:
    print("AttributeError:", e)'''),

        ("Getting the data back out",
         "<code>model_dump()</code> returns a plain dict and "
         "<code>model_dump_json()</code> a JSON string. These are how a model leaves "
         "your program again.",
         '''from pydantic import BaseModel

class Module(BaseModel):
    title: str
    track: str
    minutes: int

m = Module(title="Eigenvalues", track="maths", minutes=14)

d = m.model_dump()
print("dict   :", d)
print("a key  :", d["track"])
print()
print("json   :", m.model_dump_json())
print("pretty :")
print(m.model_dump_json(indent=2))'''),

        ("Round trip",
         "Out to JSON and back in again. This is the everyday shape of an API: "
         "receive, validate, work, serialise, send.",
         '''from pydantic import BaseModel

class Module(BaseModel):
    title: str
    track: str
    minutes: int

original = Module(title="Projections", track="maths", minutes=9)

wire = original.model_dump_json()
print("sent     :", wire)

received = Module.model_validate_json(wire)
print("received :", received)
print()
print("equal?   :", original == received)

# Models compare by value, not identity - handy in tests.
print("same obj?:", original is received)'''),

        ("Two models, one shape",
         "Because a model is just a class, the ordinary tools apply. Here two models "
         "describe the same subject at different depths &mdash; the pattern behind "
         "\"summary\" and \"detail\" API responses.",
         '''from pydantic import BaseModel

class ModuleSummary(BaseModel):
    title: str
    minutes: int

class ModuleDetail(BaseModel):
    title: str
    minutes: int
    track: str
    description: str

full = ModuleDetail(
    title="The Chain Rule",
    minutes=13,
    track="maths",
    description="How derivatives compose, and why backpropagation is this rule.",
)

# Build the smaller one from the bigger one's data.
summary = ModuleSummary.model_validate(full.model_dump())

print("detail  :", full.model_dump())
print()
print("summary :", summary.model_dump())'''),
    ],
    [
        "There is no <code>__init__</code> to write. Pydantic generates one from the annotations, which is why adding a field is a one-line change.",
        "Positional arguments are deliberately not allowed. Fields are keyword-only so that adding one can never silently change what an existing call means.",
        "<code>Module(**data)</code> and <code>Module.model_validate(data)</code> do the same job. The second reads better when the data is already a dict, and is the one to reach for in a pipeline.",
        "Models compare by value: two models of the same class with the same field values are <code>==</code>. That makes assertions in tests short.",
        "<code>model_dump()</code> gives Python objects (a <code>datetime</code> stays a <code>datetime</code>); <code>model_dump_json()</code> gives JSON-safe text. Reach for the second when something is leaving the process.",
        "In Pydantic v1 these were <code>.dict()</code> and <code>.json()</code>. Both still exist in v2 but are deprecated &mdash; most tutorials you find will use the old names.",
    ],
    '''
title: Your First BaseModel, End to End
intro: Defining a model, creating one, reading it back, and getting the data out again.

## The whole idea in three lines

A BaseModel is the class you inherit from to get everything Pydantic offers. You list the fields you expect, give each one a type, and the class does the rest. It checks the data when you create an object, converts what it can, and refuses what it cannot.

This is the first model you will write, so the article stays small on purpose. You will see how little code it takes to define one, what happens when you create an instance from clean data, and what the object lets you do afterwards. Fields become attributes. The object knows how to describe itself, compare itself to another, and copy itself.

The article walks through creating a model, reading what comes back, and the methods every model carries. It then shows how to get the data out again as a dictionary or as JSON, and how that round trip behaves. It ends with two models describing the same thing, which shows why you sometimes want one shape for input and another for output. Read it before anything else in the track, because every later article builds on this class.

If you have never used the library, treat this as the map for everything else. The ideas here come back in every later article, so a few minutes now saves confusion later. No prior knowledge of validation is needed.

A Pydantic model is a class that takes from from `BaseModel` and lists its fields as annotations.

```python
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    track: str
    minutes: int
```

That is the entire meaning. There's no `__init__`, no set of `self.title = title`, no check code. Pydantic reads the annotations when the class is created and builds the machinery from them. A constructor, a checker, a serialiser, an equality method and a readable `repr`.

The economy matters more than it first appears. Adding a field is one line. In the hand-written equal it's four. The param, the set, the check. The line in `to_dict`. Those four drift apart over time. The drift is where bugs live.

## Creating one

Models take keyword args:

```python
m = Module(title="Dot Product", track="maths", minutes=11)
```

Spot-based args are refused, and the refusal is deliberate rather than an oversight. Models grow. A field added in the middle of a class body would silently change what each spot-based call meant, and nothing would raise. The values would simply land in the wrong slots. needing names makes that class of bug hopeless.

When the data is already a dict. This It often is if it came from JSON, there are two ways in:

```python
Module(**data)
Module.model_validate(data)
```

They do the same work. `model_validate` reads better in a pipeline, makes it obvious that check is happening. Doesn't break if the dict happens to hold a key that isn't a valid Python identifier.

## What you get back

An plain object. Field access works, methods you define work. The values have the types the annotations promised:

```python
m.title          # "Dot Product"
m.minutes + 1    # 12  - a real int, not a string
```

That last line is the payoff. Downstream code doesn't need to check or convert anything. The conversion already happened at the door.

Models aren't dicts. `m["title"]` raises, and asking for a field that doesn't exist raises `AttributeError` like any other object. This is a feature. A typo in a dict key returns `None` or a `KeyError` deep inside a function, whereas a typo in an field name is caught at once and is visible to your editor's autocomplete.

## Methods and behaviour

Because a model is a class, you can give it methods:

```python
class Module(BaseModel):
    title: str
    minutes: int

    def slug(self) -> str:
        return self.title.lower().replace(" ", "_")
```

This is worth doing. Logic that depends only on a model's own fields belongs on the model. Here It's discoverable and testable, rather than in a loose function three modules away.

Later in this track you'll meet `@computed_field`. This Is the version of this that also appears in the serialised output.

## Getting the data out

Two methods, and the gap between them is worth getting right early.

`model_dump()` returns a dict of Python objects. A `datetime` field comes back as a `datetime`, a `Decimal` as a `Decimal`. Use it when the data is staying inside your program. Passing to another function, feeding a template, checking in a test.

`model_dump_json()` returns a JSON string, converting all into a thing JSON can represent. Use it when the data is leaving. An HTTP response, a message queue, a file on disk. It handles the types that plain `json.dumps` refuses outright. This Is a small mercy you'll appreciate the first time a `datetime` appears in a payload.

Both take args that shape the output. `include`, `exclude`, `exclude_none`, `by_alias`. And those get a module of their own in the output tier.

If you've read older tutorials you'll have seen `.dict()` and `.json()`. Those are the Pydantic v1 names. They still work in v2 but emit deprecation warnings. A great deal of writing on the internet hasn't caught up.

## The round trip

Put the two directions together and you've the shape of most web services:

```python
wire = original.model_dump_json()          # going out
received = Module.model_validate_json(wire) # coming back in
original == received                        # True
```

That equality is worth noticing. Models compare by value, not identity. Two apart made models with the same contents are equal. In tests this turns a page of field-by-field assertions into one line.

`model_validate_json` is also the right way to accept JSON. It's tempting to write `json.loads` followed by `model_validate`. It works. Parsing inside Pydantic's Rust core is faster and the errors it makes know where in the doc the problem was.

## Two models of the same thing

A pattern that arrives quickly in real work. The same subject needs other shapes in other places. A list endpoint returns a title and a duration. A detail endpoint returns all. A create endpoint accepts all except the id. This The server assigns.

The instinct is to build one model with a lot of optional fields. Resist it. Optional-all means the model no longer docs anything. each field might be missing. No reader can tell what is really sure.

split models say what they mean. `ModuleSummary` has two needed fields and is honest about it. Converting between them is one line. A dump from one is valid input to the other when the fields line up.

## Field order, and why it exists

Fields have an order &mdash; the order you wrote them &mdash; and although you can't pass them positionally, the order isn't cosmetic.

It finds the order of keys in `model_dump()` and in the made JSON. This Matters when a human reads the output or when a thing downstream diffs two payloads. It finds the order fields appear in the made schema. So in API docs. And it finds check order. This Turns large once you write checkers that look at before-checked fields.

The hands-on advice is to order fields the way you'd explain them. Identity first, then the key fields, then the optional extras. It costs nothing and each reader of the output gains.

## Looking at the model itself

A model knows about its own fields, and that introspection is on hand to you:

```python
Module.model_fields          # {'title': FieldInfo(...), 'minutes': FieldInfo(...)}
list(Module.model_fields)    # ['title', 'minutes']
```

Each `FieldInfo` carries the annotation, whether the field is needed, the default if there's one. Any metadata such as a description. This is what the schema gen reads. It's on hand to you for the same kind of work. Building a form, making a table header, checking that each field has a description before you ship.

`model_fields` is defined on the class, not the instance. You can inspect a model without having any data for it.

## Copying and changing

Models are plain objects and you can assign to their fields. That is often not what you want. Above all if a thing else is holding a link to the same object.

`model_copy` makes a new one:

```python
original = Module(title="Vectors", track="maths", minutes=8)
longer = original.model_copy(update={"minutes": 12})
```

Two things to know about it. The copy is shallow by default. A nested model or a list is shared between the two objects. Pass `deep=True` when that matters. And `update` does **not** validate the new values. It writes them in right. If the values came from anywhere untrusted, build a new model instead of copying with an update.

## Making a model immutable

By default a model's fields can be reassigned, and by default that reassignment isn't checked:

```python
m.minutes = "not a number"    # allowed, and now the field is a string
```

Two settings fix two other halves of that. `validate_assignment=True` runs check on set. The line above raises. `frozen=True` forbids set fully and makes the model hashable. So It can be a dict key or a set member.

```python
class Module(BaseModel):
    model_config = ConfigDict(frozen=True)
    title: str
```

Frozen models are worth reaching for more often than people do. A value that arrives from outside, is checked once and then read many times has no business being mutable. Freezing it drops a whole class of "who changed this?" question.

## Inheritance

Models inherit, and it works the way you'd hope. Subclass fields are added to the parent's, and the parent's checkers still run.

```python
class ModuleBase(BaseModel):
    title: str
    minutes: int

class ModuleInDB(ModuleBase):
    id: int
    created_by: str
```

This is the standard way to express the family of shapes one concept needs. A base with the common fields, then `Create`, `Update` and `InDB` variants that add or relax what they must. It keeps the shared fields in one place. A change to the base reaches all of them.

Be careful with one thing: a subclass can't make an from parent needed field optional in a way that reads clearly. Redeclaring `title: str = "untitled"` works. A reader now has to check two classes to know what `title` does. If the variants differ a lot, split models are kinder than deep class chain.

## What `repr` gives you

Printing a model prints its fields. This Is more handy than the default `<Module object at 0x...>` and is one of the small things that makes models pleasant in a REPL or a log line.

You can keep a field out of that output with `Field(repr=False)`. The obvious use being anything secret. A password hash or an API token in a model that gets logged is a genuine incident waiting to happen. `repr=False` is the one-word fix.

Note that it only affects the form. The value is still in `model_dump()`. A field that must never leave the process needs `exclude=True` as well, or a split output model that simply doesn't have it.

## Two mistakes worth avoiding early

**Treating a model like a dict.** Models don't support `m["title"]`. The instinct to reach for it often signals code that is passing models where it should be passing dicts, or the reverse. Decide which side of the boundary a function is on. If it takes untrusted data, it takes a dict and validates it. If it takes checked data, it takes a model and uses fields.

**Putting costly work in a model.** A model is made each time data arrives. Anything in a checker runs on that path. A network call, a DB lookup or a file read inside a model turns check into I/O, makes the model hopeless to test without mocking. Turns a `ValidationError` into a timeout. Keep models pure. They check the shape of data using only the data. Rules that need to consult the world belong in the layer that owns the world.

## A working shape to copy

Putting the module together, these is close to what a real model looks like once it has been through a couple of rounds of use:

```python
class Module(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    track: str
    minutes: int = 10
    published: bool = False

    def slug(self) -> str:
        return self.title.lower().replace(" ", "_")
```

Frozen, because it arrives from outside and is then only read. Two needed fields, because a module without a title or a track isn't a module. Two defaults with obvious values. One method, because the slug is derived from the title and belongs next to it.

Nothing exotic, and it already gives you check, coercion, equality, a readable `repr`, JSON in both directions and a schema. That ratio. How much you get for how little you wrote. Is the reason the library is worth learning properly rather than copying from examples.

## What to try next

Change a thing in the editors above and watch what happens. Add a field to a model and leave it out of the constructor call. Pass `minutes` as `"11"` and print its type. Drop a field from the JSON before checking it back.

The next module is just about those conversions. Which values Pydantic will quietly accept and turn into the type you asked for, and which it will refuse.
''',
    [
        {"q": "Why does a model refuse positional arguments?",
         "options": ["To save memory", "Because adding a field would silently change what positional calls mean", "Because dicts are unordered", "It does not - they work"],
         "answer": 1,
         "why": "Models gain fields over time. If position mattered, inserting a field would reassign every existing positional call's values without raising anything."},
        {"q": "What is the difference between `model_dump()` and `model_dump_json()`?",
         "options": ["None", "dump gives Python objects, dump_json gives a JSON-safe string", "dump_json is deprecated", "dump only works on nested models"],
         "answer": 1,
         "why": "`model_dump()` keeps Python types like `datetime` intact for use inside your program. `model_dump_json()` converts everything to something JSON can carry, for data that is leaving the process."},
        {"q": "Two separately created `Module` objects have identical field values. What does `==` return?",
         "options": ["False - different objects", "True - models compare by value", "It raises", "Only if you define __eq__"],
         "answer": 1,
         "why": "Pydantic generates an `__eq__` that compares field values, which is what makes assertions in tests short."},
        {"q": "You have a dict from `json.loads`. Which is the better way to build a model from it?",
         "options": ["Module(**data)", "Module.model_validate(data)", "Module.parse(data)", "Module.from_dict(data)"],
         "answer": 1,
         "why": "Both `Module(**data)` and `model_validate(data)` work, but `model_validate` states that validation is happening and survives keys that are not valid Python identifiers."},
    ],
)


# ---------------------------------------------------------------------------
# 3. Types and coercion
# ---------------------------------------------------------------------------
topic(
    "types_and_coercion",
    "Types and Coercion",
    "Foundations",
    "Exactly which values Pydantic will convert for you, and which it refuses. "
    "The single biggest source of surprise in the library.",
    _svg(_txt(28, 32, '"9"', M) + _arrow(42, 28, 66, 28) + _txt(84, 32, "9", A) +
         _txt(28, 52, "9.5", M) + _arrow(42, 48, 66, 48) + _txt(88, 52, "error", A) +
         _txt(28, 72, '"nine"', M) + _arrow(48, 68, 66, 68) + _txt(88, 72, "error", A)),
    [
        ("What becomes an int",
         "Strings that read as whole numbers convert. Floats convert only when nothing "
         "is lost. Everything else raises &mdash; guessing would be worse than failing.",
         '''from pydantic import BaseModel, ValidationError

class M(BaseModel):
    n: int

for value in ["9", 9.0, True, "  9  ", 9, "9.0", 9.5, "nine", None, [9]]:
    try:
        print("%-8r -> %r" % (value, M(n=value).n))
    except ValidationError as e:
        print("%-8r -> refused (%s)" % (value, e.errors()[0]["type"]))

# Note 9.0 converts but 9.5 does not: dropping .5 would lose information
# you might have needed, so Pydantic refuses rather than rounding.'''),

        ("What becomes a float, and what becomes a str",
         "Ints widen to floats without complaint. Strings, however, are strict in one "
         "surprising direction: a number is <em>not</em> silently turned into text.",
         '''from pydantic import BaseModel, ValidationError

class F(BaseModel):
    x: float

class S(BaseModel):
    s: str

print("-- into float --")
for value in [9, "9.5", "1e3", True, "abc"]:
    try:
        print("%-8r -> %r" % (value, F(x=value).x))
    except ValidationError:
        print("%-8r -> refused" % (value,))

print()
print("-- into str --")
for value in ["hello", 9, 9.5, True, None]:
    try:
        print("%-8r -> %r" % (value, S(s=value).s))
    except ValidationError:
        print("%-8r -> refused" % (value,))

# str is the asymmetry worth remembering: int -> str does NOT happen.'''),

        ("Booleans are the trap",
         "<code>bool</code> accepts a specific list of words and numbers. It is more "
         "generous than <code>bool()</code> and stricter at the same time &mdash; and "
         "the difference bites when parsing query strings.",
         '''from pydantic import BaseModel, ValidationError

class B(BaseModel):
    flag: bool

for value in ["true", "True", "yes", "on", "1", 1,
              "false", "no", "off", "0", 0,
              "maybe", 2, "", None]:
    try:
        print("%-8r -> %r" % (value, B(flag=value).flag))
    except ValidationError:
        print("%-8r -> refused" % (value,))

# Compare with plain Python, where every non-empty string is truthy:
print()
print('bool("false") in plain Python is', bool("false"))
print("Pydantic reads the *meaning* of the word, not its emptiness.")'''),

        ("Order matters inside a Union",
         "A union tries its members left to right in smart mode. That is usually what "
         "you want, but it means the order you write can change the type you get.",
         '''from typing import Union
from pydantic import BaseModel

class Loose(BaseModel):
    v: Union[int, str]

class Reversed(BaseModel):
    v: Union[str, int]

for value in ["9", 9, "nine"]:
    a = Loose(v=value).v
    b = Reversed(v=value).v
    print("%-6r -> int|str gives %-6r (%s)   str|int gives %-6r (%s)"
          % (value, a, type(a).__name__, b, type(b).__name__))

# If the distinction matters, do not rely on order - say what you mean
# with a discriminated union, or turn on strict mode.'''),

        ("Turning coercion off",
         "When data should already be the right type &mdash; deep inside a system "
         "rather than at its edge &mdash; strict mode makes conversion an error "
         "instead of a convenience.",
         '''from pydantic import BaseModel, ConfigDict, ValidationError

class Lax(BaseModel):
    minutes: int

class Strict(BaseModel):
    model_config = ConfigDict(strict=True)
    minutes: int

print("lax    :", Lax(minutes="9").minutes)

try:
    Strict(minutes="9")
except ValidationError as e:
    print("strict :", e.errors()[0]["msg"])

print("strict :", Strict(minutes=9).minutes, "(a real int is fine)")

# Strict can also be set per field - see the constraints module.'''),

        ("A realistic mixed payload",
         "Everything so far, applied to the kind of dictionary a form or query string "
         "actually produces: all strings, several types wanted.",
         '''from pydantic import BaseModel

class ModuleForm(BaseModel):
    title: str
    minutes: int
    rating: float
    published: bool

# Exactly what a browser form submission looks like: strings throughout.
raw = {"title": "Bayes' Theorem", "minutes": "12",
       "rating": "4.5", "published": "on"}

m = ModuleForm.model_validate(raw)

print("model :", m)
print()
for name, value in m.model_dump().items():
    print("  %-10s %-8r %s" % (name, value, type(value).__name__))

print()
print("arithmetic works now:", m.minutes * 2, "|", round(m.rating + 0.5, 1))'''),
    ],
    [
        "The default is called <strong>lax mode</strong>. It converts anything with a single unambiguous reading and refuses everything else.",
        "<code>9.0 -> 9</code> works but <code>9.5 -> 9</code> does not. Pydantic converts only when nothing is lost; it will not round for you.",
        "<code>int -> str</code> does <em>not</em> happen. String is the one common field type that will not accept a number, because doing so hides real mistakes.",
        "<code>bool</code> reads words: <code>true/yes/on/1</code> and <code>false/no/off/0</code>. Anything else raises &mdash; unlike Python's <code>bool()</code>, where <code>\"false\"</code> is truthy.",
        "In a <code>Union</code>, smart mode prefers an exact type match before it tries converting. Where the outcome matters, use a discriminated union rather than relying on order.",
        "Strict mode is available per model (<code>ConfigDict(strict=True)</code>) or per field, so you can be lax at the boundary and strict inside.",
    ],
    '''
title: Types and Coercion: What Pydantic Will and Will Not Convert
intro: The rules behind the library's most surprising action, one value at a time.

## Why it converts at all

Pydantic does not demand that incoming data already has the right Python type. It will try to convert it first. A string "36" becomes the integer 36. The number 1 can become True. This behaviour is called coercion, and it exists because most data arrives as text.

Coercion is useful, and it is also the source of many surprises. Some conversions feel obvious and others feel strange. A float with a fractional part will not become an integer, but a float like 3.0 will. A string will not be built out of an integer unless you ask for it. Knowing where the lines sit saves you from bugs that only show up with real traffic.

This article goes through the common targets one at a time. You will see what Pydantic accepts for integers, floats, strings and booleans, and why strings behave differently from the others. It then covers unions, where the order of the types can change the result, and finishes with the switch that turns coercion off. By the end you should be able to predict what a given input becomes before you run it.

Keep the examples in mind as you read. Each one is short enough to try yourself.

The first time someone sees `minutes="9"` become `9` they often ask whether that is safe. It's a fair question. The answer is in where models get used.

Data arriving from outside a program is nearly always text. A query string is text. An HTML form submission is text. A CSV is text. An setting var is text. If a model refused all that wasn't already the right Python type, the code in front of each model would be a pile of `int(...)` calls wrapped in `try`. This Is just the code the library exists to drop.

So the default &mdash; **lax mode** &mdash; is to accept any value with one unambiguous reading. Refuse the rest. The rules are worth knowing just. "unambiguous" turns out to be a stricter test than most people expect.

## Into int

A string converts if it reads as a whole number, nearby whitespace included: `"9"` and `"  9  "` both give `9`.

A float converts only if nothing is lost. `9.0` turns `9`. **`9.5` raises.** This is the rule people are most often surprised by. It's the right one. Rounding silently is how a total ends up being a penny out and no one can find why. If you want rounding, ask for it by name.

`True` turns `1`, because `bool` is a subclass of `int` in Python and always has been.

all else refuses: `"nine"`, `None`, a list, a dict. There's no reading of `"nine"` that is unambiguous without inventing a natural-language parser.

## Into float

More permissive, because floats can represent more. ints widen (`9` gives `9.0`). Strings that read as numbers convert. Scientific form like `"1e3"` works. `True` gives `1.0`.

Note that this is one place where data truly can be lost. A very large int won't live a trip through a float just. But that is a property of floating point rather than of Pydantic.

## Into str, and the asymmetry

Here is the rule that catches people: **a number doesn't become a string.** A field annotated `str` given `9` raises.

That seems inconsistent until you think about which direction the mistake often runs. Text arriving where a number was wanted is normal. It's what the wire looks like. A number arriving where text was wanted is often a genuine mistake in the calling code. Converting it would bury that mistake. The skew is doing handy work.

If you really want numbers accepted as text, say so with a checker that runs before conversion. There's a module on those later.

## Into bool

Booleans have their own table, and it isn't Python's.

`True` comes from `True`, `1`, `1.0`. The strings `"1"`, `"true"`, `"True"`, `"yes"`, `"on"`, `"t"`, `"y"`. `False` comes from `False`, `0`, `0.0`, and the strings `"0"`, `"false"`, `"no"`, `"off"`, `"f"`, `"n"`. Anything else. `"maybe"`, `2`, `""`, `None` &mdash; raises.

Compare that with plain Python. Here `bool("false")` is `True` because the string is non-empty. Pydantic reads the *meaning* of the word rather than the emptiness of the holder. This Is almost always what you wanted when the value came from a checkbox or a query param. It's also why `?published=false` does the right thing without you writing a special case.

## Unions and order

A `Union[int, str]` has to decide which member to try. Pydantic v2 uses **smart mode**. It first looks for a member the value already matches just. Only then tries conversion, left to right.

That resolves the common cases sensibly. An actual `int` stays an `int`, an unconvertible string stays a string. But it doesn't drop ambiguity fully. A string like `"9"` can meet both members. Which one wins depends on the order you wrote.

Where the gap matters, don't lean on order. Say what you mean. A discriminated union picks a member by an clear tag field. Strict mode drops conversion from the question. Both have modules later in this track.

## Turning it off

Coercion is right at the boundary and often wrong inside. Once data has been checked at the door, a value arriving as the wrong type deeper in the system is a bug in your own code. Quietly fixing it hides the bug.

Strict mode makes conversion an error:

```python
class Strict(BaseModel):
    model_config = ConfigDict(strict=True)
    minutes: int
```

`Strict(minutes="9")` now raises. `Strict(minutes=9)` is fine. Strictness can also be set on a single field. This Is the more common need. Lax about most things, exact about the one that matters.

There's a module on strict mode in the next tier that covers when the trade is worth making.

## Reading the type codes

each refusal carries a stable `type` code. They're worth recognising because they say just which rule fired:

`int_parsing` means a string didn't read as an int. `int_from_float` means a float had a fractional part. `string_type` means a non-string reached a `str` field. `bool_parsing` means a string wasn't in the boolean table. Matching on these is more solid than matching on the message. This Is prose and may be reworded.

## Dates, times and the other standard types

Pydantic knows the common standard-library types, and the conversions are the ones you'd want.

A `datetime` field accepts a `datetime`, an ISO 8601 string such as `"2026-08-26T14:30:00"`. A Unix timestamp as an int or float. A `date` accepts `"2026-08-26"`. A `time` accepts `"14:30:00"`. A `timedelta` accepts some seconds or an ISO 8601 duration.

`UUID` accepts a `UUID` or its string form. `Decimal` accepts a string, an int or a float. And for money you want the string. `Decimal(0.1)` takes from the float's inaccuracy while `Decimal("0.1")` doesn't. `Path` accepts a string. `Enum` accepts the member or its value.

The pattern is steady: the type itself always works. The obvious textual form works. That is what makes models handy right against JSON. Here None of these types exist natively.

Timezones deserve a warning. A naive `datetime` string makes a naive `datetime`. Checking one of those to an aware one raises. If your use is timezone-aware, say so in the type with `AwareDatetime`. The model will reject naive input rather than letting it through to fail later.

## What a collection will accept

holder types coerce their contents, item by item.

`List[int]` given `["1", "2", "3"]` gives `[1, 2, 3]`. Each element goes through the same rules given above. If one element fails, only that element fails. The error's `loc` names its index.

There's a shape rule and a content rule. A `List[int]` accepts a list. In lax mode also a tuple, a set or a gen. All of those are sequences of items. It does **not** accept a bare string, though a string is strictly iterable. That exception is deliberate and it's a mercy: `List[str]` given `"abc"` making `["a", "b", "c"]` would be a memorably bad afternoon.

`Dict[str, int]` coerces keys and values on its own. `Set[int]` deduplicates. This Means a set field can quietly return fewer items than were sent. Often what you want, at times a surprise.

`Tuple[int, str]` is checked positionally and by length. Just two items, first an int, second a string. `Tuple[int, ...]` means any number of ints.

## None is not a wildcard

A common early mistake is expecting `None` to be accepted wherever a value is missing. It isn't. `None` is a value like any other. It's accepted only where the type allows it. Which means `Optional[X]`, or `X | None`.

A field annotated `int` given `None` raises, with the type `int_type`. This is right: "no value" and "the number zero" are other facts. A library that quietly turned one into the other would be hiding data.

If you want missing to mean a thing exact, say it with a default: `minutes: int = 0` accepts an absent field and gives you a zero, while still refusing an clear `None`.

## JSON mode is stricter than Python mode

There are two check modes, and they differ in ways that at times matter.

`model_validate` takes Python objects. `model_validate_json` takes a JSON string and parses it in the Rust core.

The gap shows up because JSON has fewer types than Python. A JSON doc has no `datetime`. A `datetime` field checked from JSON must accept a string. And it does. But in Python mode, some conversions that would be ambiguous in JSON are allowed because the input type already disambiguates them.

For everyday models the two behave the same and you can skip the gap. It turns relevant with custom serialisers and with `Decimal`. Here The JSON parser can preserve a number's exact textual form in a way that a Python float has already lost. When precision matters, checking from JSON right isn't just faster &mdash; it's more faithful.

## The rules on one page

Worth committing to memory, because most surprises are one of these:

**To `int`:** whole-number strings yes, whitespace skipped. Floats only when exact. `True` gives `1`. Anything else raises.

**To `float`:** ints yes, numeric strings yes, scientific form yes.

**To `str`:** other strings only. Numbers, booleans and `None` all raise.

**To `bool`:** a fixed vocab of words and `0`/`1`. All else raises, including `2`.

**To a holder:** the items are coerced on their own. A string is never treated as a sequence of characters.

**`None`:** allowed only where the annotation says so.

**all over:** conversion never loses data silently. Where it would, it raises instead.

That last line is the principle the whole table is made from. If you note one thing, note that. You can often predict the rest.

## Debugging a conversion you did not expect

When a field comes out as a thing surprising, there's a quick sequence that finds the cause almost each time.

**Print the type, not the value.** `print(type(m.minutes).__name__, m.minutes)` sets apart `9` the int from `9` the string, which `print(m.minutes)` doesn't.

**Look at the error's `input`.** If it raised, the report shows what really arrived. It's often not what the caller believed they sent. `"null"` as a four-character string, a number wrapped in a list, an empty string where a missing field was intended.

**Check for a `Union`.** surprise types nearly always come from a union member being chosen that you didn't have in mind. `Union[int, str]` will hand you a string at times and an int other times. Both are correct action for the annotation you wrote.

**Try it in strict mode.** Temporarily setting `strict=True` turns each silent conversion into an error that names the field. It's the fastest way to find out which conversions a model is really performing. You can turn it off again later.

## What to take away

Coercion is the feature people distrust first and lean on most. It exists because the boundary is made of text. It's bounded by a single principle. Convert when the reading is unambiguous and nothing is lost, refuse else.

Once that principle is in your head, the single rules stop needing to be stored. `9.5` to an int loses data. It raises. `"9"` to an int loses nothing. So It converts. `9` to a string loses nothing either. But That direction hides caller mistakes, so it's the one deliberate exception. And knowing it's an exception is easier than remembering it as an any rule.

## The practical shape

Run the last editor above and look at what happened. A dict of four strings. Just what a browser sends. Became a model with a string, an int, a float and a bool, each usable in math without a single conversion call in sight.

That is the whole value proposition. You wrote the types once, in the annotations. The messy part happened at the boundary where it belongs.

The next module deals with the fields that aren't always there. Optional values, defaults. The gap between "missing" and "null" that trips up nearly all.
''',
    [
        {"q": "A field is `n: int`. What does Pydantic do with the float `9.5`?",
         "options": ["Gives 9", "Gives 10", "Raises a ValidationError", "Gives 9.5"],
         "answer": 2,
         "why": "Conversion happens only when nothing is lost. `9.0` becomes `9`, but rounding `9.5` would discard information, so it refuses rather than guessing."},
        {"q": "A field is `s: str`. What happens with the integer `9`?",
         "options": ["Gives \"9\"", "Raises a ValidationError", "Gives 9", "Gives None"],
         "answer": 1,
         "why": "This is the asymmetry to remember. Text arriving where a number is wanted is normal; a number arriving where text is wanted is usually a real bug in the caller, so it is not hidden."},
        {"q": "What does a `bool` field do with the string `\"false\"`?",
         "options": ["True, because the string is non-empty", "False", "Raises", "None"],
         "answer": 1,
         "why": "Pydantic reads the meaning of the word, not the emptiness of the container. Plain Python's `bool(\"false\")` is `True`, which is why query-string parsing needs this behaviour."},
        {"q": "When is strict mode the right choice?",
         "options": ["Always", "At the boundary where text arrives", "Deep inside a system where types should already be correct", "Never"],
         "answer": 2,
         "why": "At the boundary, coercion removes conversion code you would otherwise write. Inside, a wrong type is a bug of your own, and silently fixing it hides the bug."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Required, optional and defaults
# ---------------------------------------------------------------------------
topic(
    "required_optional_and_defaults",
    "Required, Optional and Defaults",
    "Foundations",
    "Optional does not mean optional. The three-way difference between missing, "
    "null and defaulted, and the mutable-default trap.",
    _svg(_box(10, 26, 44, 38, S) + _txt(32, 42, "missing", M, 8) + _txt(32, 55, "raises", A, 8) +
         _box(58, 26, 44, 38, S) + _txt(80, 42, "None", M, 8) + _txt(80, 55, "allowed", A, 8) +
         _box(106, 26, 44, 38, S) + _txt(128, 42, "default", M, 8) + _txt(128, 55, "filled", A, 8)),
    [
        ("A field with no default is required",
         "That is the whole rule. Leave it out and the model refuses to exist, with "
         "the error type <code>missing</code>.",
         '''from pydantic import BaseModel, ValidationError

class Module(BaseModel):
    title: str
    minutes: int

print(Module(title="Norms", minutes=8))

try:
    Module(title="Norms")
except ValidationError as e:
    err = e.errors()[0]
    print("refused :", err["loc"], "->", err["msg"], "|", err["type"])'''),

        ("Optional[int] is not an optional field",
         "This is the single most common misreading in the library. "
         "<code>Optional[int]</code> means “int or None”. It says nothing about "
         "whether the field must be supplied.",
         '''from typing import Optional
from pydantic import BaseModel, ValidationError

class Strict(BaseModel):
    note: Optional[str]           # nullable, but STILL REQUIRED

class Truly(BaseModel):
    note: Optional[str] = None    # nullable AND optional

print("explicit None :", Strict(note=None))

try:
    Strict()
except ValidationError as e:
    print("omitted       : refused ->", e.errors()[0]["type"])

print("with a default:", Truly())
print("still nullable:", Truly(note=None))

# The default is what makes a field optional. Not the type.'''),

        ("Three states, not two",
         "“Not sent” and “sent as null” are different facts, and an API often "
         "needs to tell them apart. <code>model_fields_set</code> is how you ask.",
         '''from typing import Optional
from pydantic import BaseModel

class Update(BaseModel):
    title: Optional[str] = None
    minutes: Optional[int] = None

absent = Update()
nulled = Update(title=None)
given  = Update(title="Projections")

for name, m in [("omitted", absent), ("sent as null", nulled), ("sent", given)]:
    print("%-13s fields_set=%-12s dump=%s"
          % (name, m.model_fields_set, m.model_dump()))

print()
print("only what was actually sent:", given.model_dump(exclude_unset=True))
print("this is how a PATCH endpoint avoids overwriting untouched fields")'''),

        ("The mutable default trap",
         "In ordinary Python a mutable default is shared by every call. Pydantic does "
         "not have that bug &mdash; but the habit it teaches, "
         "<code>default_factory</code>, is still what you want for anything computed.",
         '''from typing import List
from pydantic import BaseModel, Field

# First, the classic Python bug, so the contrast is clear:
def add_tag(tag, tags=[]):        # <- shared list, created once
    tags.append(tag)
    return tags

print("plain python:", add_tag("maths"))
print("plain python:", add_tag("python"), "<- the first call leaked in")

# Pydantic copies the default per instance, so this is safe:
class Module(BaseModel):
    title: str
    tags: List[str] = []

a = Module(title="A")
b = Module(title="B")
a.tags.append("maths")
print()
print("a.tags:", a.tags)
print("b.tags:", b.tags, "<- unaffected")

# Use default_factory when the default must be COMPUTED per instance:
import itertools
counter = itertools.count(1)

class Draft(BaseModel):
    order: int = Field(default_factory=lambda: next(counter))

print()
print("factory:", Draft().order, Draft().order, Draft().order)'''),

        ("Defaults are not validated by default",
         "Pydantic trusts what you wrote in the class body and skips checking it. That "
         "is a speed decision, and it means a wrong default sits there quietly until "
         "you ask for it to be checked.",
         '''from pydantic import BaseModel, ConfigDict, ValidationError

class Sloppy(BaseModel):
    minutes: int = "not a number"     # nonsense, and never noticed

class Careful(BaseModel):
    model_config = ConfigDict(validate_default=True)
    minutes: int = "not a number"

s = Sloppy()
print("sloppy  :", repr(s.minutes), "<- a str in an int field")
print("and so  :", type(s.minutes).__name__)

try:
    Careful()
except ValidationError as e:
    print("careful : caught it ->", e.errors()[0]["msg"])'''),

        ("Putting it together",
         "A realistic model: some fields the caller must supply, some with sensible "
         "defaults, one genuinely nullable, and a list that starts empty.",
         '''from typing import List, Optional
from pydantic import BaseModel, Field

class Module(BaseModel):
    title: str                                   # required
    track: str                                   # required
    minutes: int = 10                            # defaulted
    published: bool = False                      # defaulted
    summary: Optional[str] = None                # nullable and optional
    tags: List[str] = Field(default_factory=list)

minimal = Module(title="Determinant", track="maths")
print("minimal :", minimal.model_dump())
print()

full = Module(title="Determinant", track="maths", minutes=13,
              published=True, summary="Area, and what a matrix does to it.",
              tags=["linear-algebra", "geometry"])
print("full    :", full.model_dump())
print()
print("what the caller actually set:", full.model_fields_set)
print("only their input           :", minimal.model_dump(exclude_unset=True))'''),
    ],
    [
        "A field is required when it has <strong>no default</strong>. The type is irrelevant to that decision.",
        "<code>Optional[str]</code> means <code>str | None</code>. To make a field genuinely optional you must also write <code>= None</code>.",
        "<code>model_fields_set</code> tells you which fields the caller actually supplied &mdash; the only way to distinguish “omitted” from “sent as null”.",
        "<code>model_dump(exclude_unset=True)</code> returns only what was supplied. This is the correct shape for a PATCH request, where absent means “leave alone”.",
        "Unlike plain Python, a mutable default such as <code>[]</code> is safe here &mdash; Pydantic deep-copies it per instance. Use <code>default_factory</code> when the value must be <em>computed</em> each time.",
        "Defaults are not validated unless you set <code>validate_default=True</code>. It is a deliberate speed trade, and it will hide a typo in a default.",
    ],
    '''
title: Required, Optional and Defaults: The Three-Way Distinction
intro: Why Optional doesn't mean optional. How to tell "not sent" from "sent as null".

## The rule, first

Every field on a model is in one of three states. It is required, so the caller must provide it. It has a default, so the model fills it in when the caller does not. Or it can be None, which is a separate idea that people often mix up with the other two.

The confusion comes from the word Optional. In Python's typing module it means "this value may be None". It does not mean "you may leave this out". A field typed as Optional with no default is still required. That one fact causes more wrong assumptions than almost anything else in the library.

This article separates the three ideas and shows how Pydantic treats each. You will see the simple rule for what makes a field required, and why Optional does not change it. It then looks at the difference between a field that is missing and a field that is present but null, since an API often needs to tell those apart. The last part covers mutable defaults, such as lists, which are a famous trap in plain Python and behave differently here. Read it before you design any model that accepts input from outside.

Nothing here is hard, but it is easy to get wrong by assumption. Most of the surprises come from a single word. Once you have seen how each state behaves on real input, you will stop second-guessing your own models. You will also read other people's models faster, because you will know what to look for first.

A field is needed when it has no default value. That is the entire rule. The type annotation plays no part in it.

```python
class Module(BaseModel):
    title: str        # required
    minutes: int = 10 # optional, defaults to 10
```

Leave out `title` and the model refuses to be built, with an error whose `type` is `missing`. Leave out `minutes` and you get `10`.

all confusing about this topic comes from one word being borrowed for two jobs.

## Optional does not mean optional

`Optional[str]` comes from the `typing` module. Here It means just one thing: `str or None`. It's a statement about which *values* are allowed. It says nothing whatsoever about whether the field has to be supplied.

```python
class Strict(BaseModel):
    note: Optional[str]        # nullable, and STILL REQUIRED
```

`Strict(note=None)` works. `Strict()` raises `missing`. This surprises nearly all once. The surprise is fully the fault of English rather than of Pydantic. `Optional` was named for type theory, not for form fields.

To get the action people often mean, add the default:

```python
class Truly(BaseModel):
    note: Optional[str] = None   # nullable AND optional
```

It's worth internalising as two split questions. *Can this value be null?* is answered by the type. *Must the caller provide it?* is answered by whether there's a default. They're split. All four mixes are legitimate and at times handy.

Pydantic v1 blurred this: it made `Optional` fields default to `None` on its own. Pydantic v2 stopped, just because the silent default hid the gap. If you find old code that leans on it, this is one of the changes that will bite during a migration.

## Missing and null are different facts

For most models the gap doesn't matter. For anything that updates existing data, it matters enormously.

Consider a PATCH endpoint. A client sends `{"title": "New Name"}`. What should happen to `summary`? Obviously nothing. They didn't mention it. Now a client sends `{"summary": null}`. What should happen? Just as obviously, `summary` should be cleared. Those are opposite intentions. After check both fields are `None` in the model.

`model_fields_set` recovers the gap. It's a set of the field names the caller really supplied:

```python
Update(title="x").model_fields_set   # {"title"}
Update().model_fields_set            # set()
```

And `model_dump(exclude_unset=True)` uses it, returning only the fields that were given. That output is the correct thing to apply to an existing record. Absent keys are absent. An clear `None` is present and clears the value.

Getting this wrong is a real and common bug. An update endpoint that dumps the whole model and writes each field will happily overwrite six columns with `None` because the client only mentioned one.

## The mutable default trap, and why it is not one here

each Python programmer eventually learns this the hard way:

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```

The list is created once, when the function is defined. Shared by each call that doesn't pass one. The second call sees the first call's data.

Pydantic doesn't have this bug. A default like `tags: List[str] = []` is deep-copied for each new instance. Two models never share a list. You can write the natural thing and it's safe.

`default_factory` still matters, though, for defaults that must be *found* rather than copied. A timestamp, a made id, a counter. Anything whose value should reflect the moment of creation:

```python
created: datetime = Field(default_factory=datetime.now)
```

Written as `= datetime.now()` that would freeze the time the class was defined. Each model would claim to have been created at import.

## Defaults are not checked

This one is quiet and at times costly. By default, Pydantic doesn't validate default values:

```python
class Sloppy(BaseModel):
    minutes: int = "not a number"
```

That class meaning raises nothing, and `Sloppy().minutes` is the string. The thinking is speed. You wrote the default yourself. Checking it on each instantiation is work with no expected payoff.

The cost is that a mistyped default is invisible until a thing downstream does math. If you'd rather be told, `model_config = ConfigDict(validate_default=True)` turns the checking on, at a small cost per instance.

For a model with hand-written defaults that never change, the default action is fine. For a model whose defaults come from config or a constant defined elsewhere, turning check on is cheap insurance.

## Choosing well

A few habits that keep models honest.

Prefer needed fields. each default is a choice made on behalf of a caller who didn't make it. A model where all is optional docs nothing. A reader can't tell what is really sure.

Don't use `None` as a stand-in for a real default. If a missing duration means ten minutes, write `minutes. Int = 10`, not `Optional[int] = None` with a `or 10` scattered through the code that follows.

Reserve `None` for values that are truly absent in the domain. A summary no one has written yet, an end date for a thing still running. Then `None` carries meaning rather than marking a gap in the model.

And when you're modelling an update rather than a creation, reach for `exclude_unset` early. It's easier to build the endpoint right than to work out later why six columns went blank.

## The ellipsis, and other spellings of "required"

You'll meet `Field(...)` in older code and in a lot of docs:

```python
title: str = Field(..., min_length=3)
```

The literal `Ellipsis` was Pydantic v1's way of saying "there's no default, this is needed". `Field` needed a thing in the default spot. It still works in v2. It's redundant: omitting the default says the same thing.

```python
title: str = Field(min_length=3)     # identical, and clearer
```

Prefer the second. The first makes readers who haven't met the rule stop and look it up, and it buys nothing.

## Defaults that depend on the environment

A default doesn't have to be a literal. `default_factory` takes any callable. This Means a default can come from config, the clock, or a gen:

```python
created: datetime = Field(default_factory=datetime.now)
request_id: str = Field(default_factory=lambda: uuid4().hex)
retries: int = Field(default_factory=lambda: int(os.getenv("RETRIES", "3")))
```

The third one is worth a caution. Reading config inside a default factory works. It happens at model-build time rather than at import. This Makes it harder to reason about and hard to replace in tests. For anything that is really config, a settings model is the better home. That is a module in the last tier.

There's also a form of `default_factory` that receives the already-checked data, letting a default depend on other fields. It's powerful and easy to overuse. A value found from other fields is often better expressed as a `computed_field`. This Doesn't pretend to be an input.

## How this appears in the schema

The gap between needed, optional and nullable isn't just a Python concern. It shows up in the made JSON Schema. So in your API docs and any client made from it.

A field with no default appears in the schema's `needed` array. A field with a default doesn't. Its default is recorded. A nullable field's type turns an `anyOf` including `null`.

So the four mixes give four truly other contracts for a consumer:

`str` &mdash; must be sent, can't be null.
`str = "x"` &mdash; may be omitted, can't be null.
`Optional[str]` &mdash; must be sent, may be null.
`Optional[str] = None` &mdash; may be omitted, may be null.

Reading them as sentences like that is the fastest way to check you've written what you meant. If the sentence sounds wrong for your API, the annotation is wrong.

## Designing create and update models

The place all of this comes together is a resource with more than one shape.

**Create** takes what a caller may supply. The server-assigned id is absent fully. Not optional, absent. Because including it invites a caller to try setting it.

**Update**, for a PATCH, has each field optional with a `None` default. Is dumped with `exclude_unset=True` so that untouched fields stay untouched.

**Output** has all the caller is allowed to see, with server-assigned fields needed. By the time you're returning one they exist.

```python
class ModuleCreate(BaseModel):
    title: str
    minutes: int = 10

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    minutes: Optional[int] = None

class ModuleOut(BaseModel):
    id: int
    title: str
    minutes: int
```

Three small classes rather than one clever one. Each says just what it means. None of them needs a comment showing which fields apply when.

The temptation is always to collapse them into a single model with all optional. It looks like less code and it's. It's also a model that docs nothing, makes useless API docs. Can't tell a client what is sure in a response.

## A note on validation order

Fields are checked in declaration order. Defaults are filled as part of that pass. This matters once you write a checker that reads another field. It can only see fields declared *above* it. The ones below haven't been processed yet.

If a rule needs the whole object, that is what `model_validator(mode="after")` is for. It runs once, after each field is in place. Trying to express a cross-field rule as a field checker on whichever field happens to come last works until somebody reorders the class.

## A checklist for a field you are about to write

Four questions, in order, and the annotation falls out of the answers.

**Can this be absent?** If yes, it needs a default. If no, leave the default off and let the model refuse.

**Can this be null, usefully?** Only if "no value" is a real state in your domain. An unwritten summary, an unfinished end date. If `None` would just mean "no one bothered", it isn't nullable. It's defaulted.

**Is the default a constant or does it depend on when we are?** A constant goes in right. Anything found. A time, an id, a fresh holder &mdash; goes in `default_factory`.

**Am I creating or updating?** Creating means needed fields are needed. Updating means all is optional and you dump with `exclude_unset=True`.

Most confusing models are the result of answering the second question with "I suppose so" instead of thinking about it. `Optional[X] = None` is the annotation people reach for when they haven't decided. A model full of them has quietly recorded that nothing was ever decided.

## What this buys downstream

The payoff for being precise here shows up one spot else fully: in the code that reads the model.

If `summary: Optional[str] = None` truly means "may not have been written yet", then `if module.summary:` is a real branch about the domain. If it means "we weren't sure", each reader has to defend against `None` on each field. The type system has stopped helping.

needed fields are a promise to the rest of your program. Each one you make lets code downstream stop checking. That is the actual product of this module. Not the syntax. The discipline of deciding what is sure and then writing it down where the compiler, the schema and the next reader can all see it.

## One last distinction

There's a fourth state people at times need, beyond needed, defaulted and nullable. A field that may be absent but has no sensible default. Here You truly want to know whether it was supplied.

That is what `model_fields_set` and `exclude_unset` exist for. It's worth naming by name because the instinct is to invent a sentinel. A magic string, a `-1`, a custom `UNSET` object. And thread it through the code. Pydantic already tracks the answer. Reach for the sentinel only when the value has to live output. This Is rare. Think hard before you do. Each consumer of that data now has to know about your magic value.

## Next

The next module is about the moment a model says no. How to read a `ValidationError` in full, what each part of an entry means. How to turn one into a message a user can act on.
''',
    [
        {"q": "A field is declared `note: Optional[str]` with no default. Is it required?",
         "options": ["No - Optional makes it optional", "Yes - it is nullable but still required", "Only in strict mode", "It defaults to None"],
         "answer": 1,
         "why": "`Optional[str]` means `str or None`, which is about allowed values. Requiredness is decided by whether a default exists. Pydantic v1 added the default implicitly; v2 deliberately does not."},
        {"q": "Which tells you whether a caller actually supplied a field?",
         "options": ["model_dump()", "model_fields_set", "model_json_schema()", "The field being None"],
         "answer": 1,
         "why": "After validation an omitted field and an explicitly null one both read as `None`. `model_fields_set` is the only record of what was actually sent."},
        {"q": "What does `model_dump(exclude_unset=True)` produce, and why does it matter?",
         "options": ["Everything except None", "Only fields the caller supplied - the right shape for PATCH", "Only required fields", "An empty dict"],
         "answer": 1,
         "why": "An update that dumps every field will overwrite untouched columns with defaults or None. Excluding unset fields keeps 'not mentioned' meaning 'leave alone'."},
        {"q": "Why use `default_factory=datetime.now` instead of `= datetime.now()`?",
         "options": ["It is faster", "The second freezes the time the class was defined", "Both are identical", "The second is a syntax error"],
         "answer": 1,
         "why": "`datetime.now()` is evaluated once, when the class body runs, so every instance would claim the same creation time. A factory is called per instance."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Reading a ValidationError
# ---------------------------------------------------------------------------
topic(
    "reading_a_validation_error",
    "Reading a ValidationError",
    "Foundations",
    "Every field checked, every failure reported at once - and how to turn that "
    "into a message somebody can act on.",
    _svg(_box(16, 20, 128, 20, S, A) + _txt(80, 33, "3 validation errors", A, 8) +
         _box(16, 46, 128, 14, S) + _txt(80, 56, "loc  -  where", M, 7) +
         _box(16, 62, 128, 14, S) + _txt(80, 72, "type  -  which rule", M, 7)),
    [
        ("It does not stop at the first problem",
         "Every field is checked and one exception is raised carrying all of them. "
         "That is what lets a form highlight four broken inputs at once instead of "
         "revealing them one submission at a time.",
         '''from pydantic import BaseModel, ValidationError

class Module(BaseModel):
    title: str
    track: str
    minutes: int
    published: bool

try:
    Module(title=None, track=42, minutes="soon", published="perhaps")
except ValidationError as e:
    print("count:", e.error_count())
    print()
    print(e)'''),

        ("errors() is the version for code",
         "Printing the exception gives prose for a human. "
         "<code>errors()</code> gives a list of dicts &mdash; the version you build "
         "an API response or a translated message from.",
         '''from pydantic import BaseModel, ValidationError

class Module(BaseModel):
    title: str
    minutes: int

try:
    Module(title=None, minutes="soon")
except ValidationError as e:
    for err in e.errors():
        print("loc   :", err["loc"])
        print("type  :", err["type"])
        print("msg   :", err["msg"])
        print("input :", repr(err["input"]))
        print("-" * 40)'''),

        ("loc is a path, not a name",
         "For a flat model it is just the field. For anything nested it is the route "
         "to the value: a list index is an integer, a nested field is a string.",
         '''from typing import List
from pydantic import BaseModel, ValidationError

class Lesson(BaseModel):
    name: str
    minutes: int

class Track(BaseModel):
    title: str
    lessons: List[Lesson]

bad = {
    "title": "Maths",
    "lessons": [
        {"name": "Vectors", "minutes": 8},
        {"name": "Norms", "minutes": "later"},     # index 1
        {"name": None, "minutes": 5},              # index 2
    ],
}

try:
    Track.model_validate(bad)
except ValidationError as e:
    for err in e.errors():
        path = ".".join(str(p) for p in err["loc"])
        print("%-22s %s" % (path, err["msg"]))'''),

        ("type is the stable handle",
         "The message is prose and may be reworded between releases. The type is a "
         "machine code that will not move &mdash; match on it, not on the sentence.",
         '''from pydantic import BaseModel, Field, ValidationError

class Module(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

FRIENDLY = {
    "string_too_short": "That needs to be a bit longer.",
    "greater_than": "That has to be more than zero.",
    "int_parsing": "Please enter a whole number.",
    "missing": "This one is required.",
}

for payload in [{"title": "Hi", "minutes": 5},
                {"title": "Vectors", "minutes": -3},
                {"title": "Vectors", "minutes": "ten"},
                {"title": "Vectors"}]:
    try:
        Module.model_validate(payload)
        print("%-38s ok" % str(payload))
    except ValidationError as e:
        err = e.errors()[0]
        nice = FRIENDLY.get(err["type"], err["msg"])
        print("%-38s %s -> %s" % (str(payload), err["loc"][0], nice))'''),

        ("Turning errors into a response",
         "The shape most APIs want: a mapping of field name to a list of messages, "
         "ready to render beside the inputs that produced them.",
         '''import json
from pydantic import BaseModel, Field, ValidationError

class Signup(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@]+@[^@]+\\.[^@]+$")
    modules_done: int = Field(ge=0)

def validate(payload):
    try:
        return Signup.model_validate(payload), None
    except ValidationError as e:
        problems = {}
        for err in e.errors():
            field = ".".join(str(p) for p in err["loc"]) or "_"
            problems.setdefault(field, []).append(err["msg"])
        return None, problems

model, problems = validate({"name": "A", "email": "nope", "modules_done": -1})
print("problems:")
print(json.dumps(problems, indent=2))

model, problems = validate({"name": "Ada", "email": "ada@vizlearn.in",
                            "modules_done": 12})
print()
print("accepted:", model)'''),

        ("Errors you raise yourself",
         "A validator that raises <code>ValueError</code> is folded into the same "
         "report, with the type <code>value_error</code>. Your rules and the built-in "
         "ones come back together.",
         '''from pydantic import BaseModel, field_validator, ValidationError

class Module(BaseModel):
    title: str
    track: str

    @field_validator("track")
    @classmethod
    def known_track(cls, v: str) -> str:
        allowed = {"maths", "python", "dsa", "ml"}
        if v not in allowed:
            raise ValueError("unknown track %r (try one of %s)"
                             % (v, ", ".join(sorted(allowed))))
        return v

print(Module(title="Vectors", track="maths"))

try:
    Module(title=None, track="astrology")
except ValidationError as e:
    print()
    print("both problems, one report:")
    for err in e.errors():
        print("  %-8s %-12s %s" % (err["loc"][0], err["type"], err["msg"]))'''),
    ],
    [
        "One exception carries every failure. <code>e.error_count()</code> is how many, <code>e.errors()</code> is the list.",
        "Each entry has <code>loc</code> (where), <code>type</code> (which rule), <code>msg</code> (prose) and <code>input</code> (what arrived).",
        "<code>loc</code> is a tuple describing a path. Integers are list indices, so <code>('lessons', 1, 'minutes')</code> means the second lesson's duration.",
        "Match on <code>type</code>, never on <code>msg</code>. Types are stable identifiers; messages are prose and get reworded.",
        "<code>input</code> is usually the fastest diagnosis available &mdash; it shows what the caller actually sent, which is often not what they believed they sent.",
        "A <code>ValueError</code> raised inside your own validator arrives in the same list with type <code>value_error</code>, so custom rules and built-in ones are handled by one piece of code.",
    ],
    '''
title: Reading a ValidationError, and Turning It Into a Message
intro: each field checked, each failure in one report - and what each part of an entry is for.

## One raise, every problem

When data fails validation, Pydantic raises a ValidationError. It does not stop at the first problem. It checks every field and collects all the failures into one error, so you can see everything that is wrong in a single pass.

That error is more useful than it first looks. Each problem has a location, a type, a message, and the input that caused it. The printed version is made for a person reading a terminal. The structured version is made for code, and that is the one you want when you turn an error into a response for an API client.

This article shows how to read the error, and then how to use it. You will learn what the errors method returns and what each key means. You will see how the location path points to a nested field, and why you should match on the error type rather than the message text. The last part shapes the errors into a clean format that a client can act on. If you ever write code that handles bad input, this is the article to read.

Good error handling is what separates a model that merely works from one people can use. A clear error saves a support request. A vague one costs an afternoon, so it pays to learn the format well and early.

Most hand-written check gives up at the first thing it doesn't like. The caller fixes it, resubmits. Meets the next one. Four mistakes take four round trips.

Pydantic checks each field and raises once, carrying the full list. For a signup form that is the gap between a form which highlights all four broken inputs at once and one which reveals them slowly, like a bad quiz.

`e.error_count()` tells you how many. `str(e)` gives a readable summary. This Is what you saw printed in the first editor above. Both are for humans.

## errors() is the version for code

`e.errors()` returns a list of dicts. This is what you build anything real on top of. Each entry has four parts, and they do other jobs.

**`loc`** is where the problem is. It's a tuple, not a string. It shows a path rather than naming a field. For a flat model it has one element. For nested data it has as many as it needs to reach the value.

**`type`** is which rule failed, as a short stable identifier: `missing`, `int_parsing`, `string_too_short`, `greater_than`, `value_error`.

**`msg`** is the human sentence, in English, written by Pydantic.

**`input`** is the value that really arrived.

## loc, in detail

Reading `loc` well is most of debugging a large payload.

ints in the tuple are sequence indices. Strings are field or key names. So `("lessons", 1, "minutes")` reads as. Inside `lessons`, the item at index 1, its `minutes` field. Joining it with dots. `lessons.1.minutes`. Gives you a thing you can paste into a search or show to a colleague.

For a union you'll at times see the union member's name in the path too. Pydantic reports which branch it was attempting when it failed. That looks noisy at first and is truly handy when a discriminated union picks the wrong branch.

The key habit is to render the path rather than the field name. Code that does `err["loc"][0]` works fine until the first nested model arrives, at which point each error appears to be about the top-level holder.

## Match on type, not on message

This is the rule that saves the most future pain.

Messages are prose. They get reworded, clarified and at times translated between releases. Any code that does `if "should be a valid int" in err["msg"]` is one minor upgrade away from silently failing.

Types are identifiers. `int_parsing` will still be `int_parsing`. Mapping them to your own copy is a dict lookup:

```python
FRIENDLY = {
    "string_too_short": "That needs to be a bit longer.",
    "missing": "This one is required.",
}
```

This is also how you localise. The type is the key. Your translation table holds the sentences.

A handy default is to fall back to `err["msg"]` when a type isn't in your table. You get good copy for the cases you've thought about. A thing serviceable for the ones you haven't.

## The shape an API wants

Most front ends want errors grouped by field. Each message can render beside the input that caused it:

```python
problems = {}
for err in e.errors():
    field = ".".join(str(p) for p in err["loc"]) or "_"
    problems.setdefault(field, []).append(err["msg"])
```

A list per field, because one field can fail a few rules at once. The `or "_"` catches model-level errors, whose `loc` is empty because they belong to the whole object rather than any single field. A cross-field rule like "end date must be after start date" has nowhere else to go.

If you're using FastAPI, this change already happens for you. A `ValidationError` on a request body turns a 422 whose body is `e.errors()`. Knowing the shape means knowing what your own clients receive.

## Your own errors, in the same report

Custom rules don't need a split channel. A checker that raises `ValueError` is caught and folded into the same list, with the type `value_error` and your message:

```python
@field_validator("track")
@classmethod
def known_track(cls, v: str) -> str:
    if v not in {"maths", "python", "dsa", "ml"}:
        raise ValueError("unknown track %r" % v)
    return v
```

This is a good thing to notice early. It means one piece of error-handling code covers built-in and custom check alike. A caller can't tell. Or need to care. Which kind of rule they broke.

Raise `ValueError`, not `ValidationError`. Making a `ValidationError` by hand is awkward and not needed. Pydantic wraps yours right and adds the location for you. An `AssertionError` also works. Is a poor choice because assertions vanish when Python is run with `-O`.

## What input tells you

Don't skip `input`. It's often the entire diagnosis.

A caller insists they're sending a number. `input` shows `"12"` with quotes. They're sending a string. Their JSON serialiser is the culprit. Or it shows `None` for a field they believe they set, and their own code has a missing key. Or it shows `"null"`, the four-character string, and a thing in the chain stringified a null.

None of that is visible in the message. All of it's visible in one line of the report.

## The parts of an entry you have not used yet

Beyond `loc`, `type`, `msg` and `input`, an error entry carries two more things.

`url` is a link to the docs page for that error type. It's the `https://errors.pydantic.dev/...` line you see at the end of a printed error. It's truly handy while learning and noise in a log. It can be turned off: `e.errors(include_url=False)`.

`ctx` holds the params of the rule that failed, when there are any. A `greater_than` error carries `{"gt": 0}`. A `string_too_short` carries `{"min_length": 3}`. This is what lets you write one message template per type and fill in the actual limit:

```python
TEMPLATES = {
    "greater_than": "Must be more than {gt}.",
    "string_too_short": "Needs at least {min_length} characters.",
}
msg = TEMPLATES[err["type"]].format(**err.get("ctx", {}))
```

That is the gap between "that is too short" and "needs at least 3 characters", without hard-coding the 3 in two places.

## Errors from a JSON string

`model_validate_json` makes the same error entries with one addition. When the JSON itself is malformed, you get a `json_invalid` error whose context includes the spot in the doc.

That matters for large payloads. A missing comma four hundred lines into a config file makes an error that names the line. This Is a lot more use than "invalid JSON".

It's also why checking JSON right is better than `json.loads` followed by `model_validate`. Go through `json.loads` and a syntax error is a `JSONDecodeError` from a other library. This You've to catch apart and which knows nothing about your model. Validate the JSON right and malformed docs and invalid data arrive through one exception type, handled in one place.

## Model-level errors have no field

A rule that spans fields belongs to the object, not to any one field. Its `loc` is empty:

```python
@model_validator(mode="after")
def check_window(self):
    if self.ends_at <= self.starts_at:
        raise ValueError("ends_at must be after starts_at")
    return self
```

The resulting entry has `loc: ()`. Any code that assumes `loc[0]` exists will raise an `IndexError` on it. Which is a bug that appears the first time somebody adds a cross-field rule, long after the error handling was written.

Handle it by name. Grouping code should fall back to a key like `"_"` or `"__root__"` for empty locations. The front end should have one spot to display an error that isn't attached to an input.

## Testing that validation fails

check logic deserves tests, and the handy ones assert on `type` and `loc` rather than on prose.

```python
import pytest
from pydantic import ValidationError

def test_minutes_must_be_positive():
    with pytest.raises(ValidationError) as exc:
        Module(title="Vectors", minutes=-1)
    errors = exc.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("minutes",)
    assert errors[0]["type"] == "greater_than"
```

Asserting on the message makes the test fail when Pydantic rewords a thing. This Teaches your team to distrust the suite. Asserting on `loc` and `type` tests the thing you really care about. That the right rule fired on the right field.

It's also worth testing the plus case by name. That a valid payload makes the values you expect, coercions included. A test that `minutes="9"` turns the int `9` docs an intention that is else invisible.

## Making errors useful to a human

A last thought, because this is where check meets the person using your software.

The default messages are written for developers. "Input should be a valid int, unable to parse string as an int" is precise and it isn't what you want beside a form field. A user doesn't care about parsing. They care that they typed "ten" in a box that wanted a number.

The translation layer is small. A dict from `type` to a sentence &mdash; and it's worth building once, early, for the twenty or so error types your use can really give. Fall back to `msg` for anything unmapped so nothing ever renders blank.

And keep the developer version too. Logging the full `errors()` while showing the friendly version means that when a user says "it told me my email was wrong and it wasn't", you've the `input` value that settles it.

## A complete handler you can lift

Putting the pieces together, this is a small function that covers all above. Grouping by field, using `ctx` for the limits, falling back gracefully, and handling model-level errors:

```python
TEMPLATES = {
    "missing": "This field is required.",
    "int_parsing": "Please enter a whole number.",
    "greater_than": "Must be more than {gt}.",
    "string_too_short": "Needs at least {min_length} characters.",
}

def friendly(exc: ValidationError) -> dict:
    out = {}
    for err in exc.errors(include_url=False):
        field = ".".join(str(p) for p in err["loc"]) or "_form"
        template = TEMPLATES.get(err["type"])
        if template:
            message = template.format(**err.get("ctx", {}))
        else:
            message = err["msg"]
        out.setdefault(field, []).append(message)
    return out
```

Twelve lines, and it covers each error the use can give. New error types degrade to Pydantic's own wording rather than to a blank space. Nothing is ever invisible, and adding a nicer message later is one dict entry.

## Why the design is the way it is

It's worth noticing what this error model is optimised for. It shows a few choices that look odd in alone.

It reports all at once because the costly part of check is the round trip to the user, not the checking.

It uses stable codes rather than messages because the consumer is often another program. Programs need identifiers that don't move.

It carries `input` because the most common question after a rejection is "what did they really send". The option is asking them.

And it makes `loc` a path rather than a name because real payloads nest. An error that can't say *where* in a hundred-line doc the problem is has told you almost nothing.

each one of those is a choice made for the person on the other end of the failure. Reading errors well is mostly a matter of noticing that the data you want is already in there.

## One more habit

Log the full error, show the friendly one.

These are other audiences with other needs. Merging them serves neither. The user needs a sentence they can act on, in their language, next to the input that caused it. You need `loc`, `type`, `input` and enough context to copy the failure without asking anyone anything.

Doing both costs one extra line at the point where you catch the exception. It's the gap between a support conversation that starts with "can you tell me just what you typed" and one that starts with "I can see what happened". The data was in the exception the whole time. The only question is whether you kept it.

## Next

The next module goes the other way: not reading the errors Pydantic makes. Writing the rules that give them. `Field` constraints let you say more about a value than its type. A min, a length, a pattern. And each one of them comes back through just the machinery given here.
''',
    [
        {"q": "A payload has four invalid fields. How many exceptions does Pydantic raise?",
         "options": ["Four", "One, carrying all four", "One per model", "It stops at the first"],
         "answer": 1,
         "why": "Every field is checked and a single `ValidationError` carries the complete list, so a caller can fix everything in one pass."},
        {"q": "What does `loc` of `('lessons', 1, 'minutes')` mean?",
         "options": ["Three separate errors", "The minutes field of the item at index 1 in lessons", "A field literally named lessons.1.minutes", "Line 1 of the file"],
         "answer": 1,
         "why": "`loc` is a path. Integers are sequence indices and strings are field names, so this locates one value inside a nested structure."},
        {"q": "Why match on `type` rather than `msg`?",
         "options": ["type is shorter", "msg is prose and gets reworded between releases", "msg is always empty", "There is no difference"],
         "answer": 1,
         "why": "Types are stable identifiers; messages are human sentences that may be clarified or translated. Matching on prose breaks quietly on upgrade."},
        {"q": "What should a custom validator raise to join the same error report?",
         "options": ["ValidationError", "ValueError", "TypeError", "Exception"],
         "answer": 1,
         "why": "Pydantic catches `ValueError`, wraps it with the field's location and gives it the type `value_error`. Building a `ValidationError` by hand is unnecessary."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Field constraints
# ---------------------------------------------------------------------------
topic(
    "field_constraints",
    "Field Constraints",
    "Foundations",
    "Saying more about a value than its type: bounds, lengths, patterns - and the "
    "metadata that becomes your documentation.",
    _svg(_txt(80, 24, "minutes: int", M, 9) +
         _box(28, 34, 104, 22, S, A) + _txt(80, 48, "Field(gt=0, le=180)", A, 8) +
         _txt(52, 72, "-5  refused", M, 8) + _txt(120, 72, "12  ok", A, 8)),
    [
        ("A type is a weak promise",
         "<code>int</code> allows every integer, including the ones your domain has no "
         "meaning for. <code>Field</code> is where you narrow it.",
         '''from pydantic import BaseModel, Field, ValidationError

class Loose(BaseModel):
    minutes: int

class Tight(BaseModel):
    minutes: int = Field(gt=0, le=180)

print("loose accepts nonsense :", Loose(minutes=-5000).minutes)

for value in [12, 0, -5, 181]:
    try:
        print("tight %-5s -> ok" % value, Tight(minutes=value).minutes)
    except ValidationError as e:
        print("tight %-5s -> %s" % (value, e.errors()[0]["msg"]))'''),

        ("Number bounds",
         "Four comparisons, named after the operators they stand for: "
         "<code>gt</code>, <code>ge</code>, <code>lt</code>, <code>le</code>. Plus "
         "<code>multiple_of</code> for step sizes.",
         '''from pydantic import BaseModel, Field, ValidationError

class Rating(BaseModel):
    score: float = Field(ge=0, le=5)          # 0 to 5 inclusive
    votes: int = Field(gt=0)                  # strictly positive
    step: int = Field(multiple_of=5)          # 0, 5, 10, ...

for payload in [{"score": 4.5, "votes": 12, "step": 10},
                {"score": 5.0, "votes": 1, "step": 0},
                {"score": 5.1, "votes": 12, "step": 10},
                {"score": 4.0, "votes": 0, "step": 10},
                {"score": 4.0, "votes": 3, "step": 7}]:
    try:
        Rating.model_validate(payload)
        print("%-42s ok" % str(payload))
    except ValidationError as e:
        err = e.errors()[0]
        print("%-42s %s: %s" % (str(payload), err["loc"][0], err["msg"]))'''),

        ("String length and shape",
         "<code>min_length</code> and <code>max_length</code> bound the size; "
         "<code>pattern</code> is a regular expression the whole value must match.",
         '''from pydantic import BaseModel, Field, ValidationError

class Module(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    slug: str = Field(pattern=r"^[a-z0-9_]+$")

for payload in [{"title": "Dot Product", "slug": "dot_product"},
                {"title": "Hi", "slug": "hi"},
                {"title": "Dot Product", "slug": "Dot Product"},
                {"title": "Dot Product", "slug": "dot-product"}]:
    try:
        Module.model_validate(payload)
        print("%-46s ok" % str(payload))
    except ValidationError as e:
        err = e.errors()[0]
        print("%-46s %s: %s" % (str(payload), err["loc"][0], err["msg"]))

# Note the last one: a hyphen is not in [a-z0-9_], so it fails.'''),

        ("Collection sizes",
         "The same length arguments work on lists, sets and dicts &mdash; useful for "
         "“at least one” rules that would otherwise be a validator.",
         '''from typing import List
from pydantic import BaseModel, Field, ValidationError

class Track(BaseModel):
    title: str
    modules: List[str] = Field(min_length=1, max_length=5)

print(Track(title="Maths", modules=["Vectors", "Norms"]))

for bad in [[], ["a", "b", "c", "d", "e", "f"]]:
    try:
        Track(title="Maths", modules=bad)
    except ValidationError as e:
        print("%-32s %s" % (str(bad)[:30], e.errors()[0]["msg"]))'''),

        ("Constraints and defaults together",
         "<code>Field</code> carries the default as well as the rules. The first "
         "positional argument is the default; <code>default_factory</code> covers "
         "anything that must be computed.",
         '''from typing import List
from pydantic import BaseModel, Field

class Module(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(default=10, gt=0, le=180)
    tags: List[str] = Field(default_factory=list, max_length=8)

print("defaults used :", Module(title="Norms").model_dump())
print("overridden    :", Module(title="Norms", minutes=25,
                                tags=["maths"]).model_dump())

# A required field with constraints simply has no default:
class Required(BaseModel):
    minutes: int = Field(gt=0)      # constrained AND required

try:
    Required()
except Exception as e:
    print()
    print("still required:", type(e).__name__)'''),

        ("Metadata is not decoration",
         "<code>description</code>, <code>title</code> and <code>examples</code> go "
         "into the generated JSON Schema &mdash; which is what FastAPI turns into your "
         "API documentation. Writing them is writing your docs.",
         '''import json
from pydantic import BaseModel, Field

class Module(BaseModel):
    title: str = Field(
        min_length=3,
        description="Shown as the page heading.",
        examples=["Dot Product"],
    )
    minutes: int = Field(
        default=10, gt=0, le=180,
        description="Estimated reading time.",
    )

schema = Module.model_json_schema()

for name, spec in schema["properties"].items():
    print(name)
    for key in ("type", "description", "default", "minLength",
                "exclusiveMinimum", "maximum", "examples"):
        if key in spec:
            print("   %-17s %s" % (key, spec[key]))
    print()

print("required:", schema.get("required", []))'''),
    ],
    [
        "<code>Field</code> narrows a type. The annotation says what kind of value; <code>Field</code> says which values of that kind are acceptable.",
        "Numbers: <code>gt</code>, <code>ge</code>, <code>lt</code>, <code>le</code>, <code>multiple_of</code>. Strings and collections: <code>min_length</code>, <code>max_length</code>. Strings also take <code>pattern</code>.",
        "<code>pattern</code> must match from the start of the string. Anchor it with <code>^...$</code> when you mean the whole value, or a prefix match will let more through than you intended.",
        "The first argument of <code>Field</code> is the default. <code>Field(gt=0)</code> with no default is still a required field.",
        "<code>description</code> and <code>examples</code> land in <code>model_json_schema()</code>, which FastAPI renders as documentation. This is the cheapest documentation you will ever write.",
        "Constraints run <em>after</em> coercion. <code>Field(gt=0)</code> on an <code>int</code> sees <code>\"5\"</code> as <code>5</code> and compares the number, not the text.",
    ],
    '''
title: Field Constraints: Saying What You Actually Mean
intro: A type allows far more values than your domain does. Field is where you close the gap.

## The gap between a type and a meaning

A type tells Pydantic what kind of value to expect. It says nothing about what the value should mean. An integer can be negative. A string can be empty. A list can hold a thousand items. For most real data, the type is only the first half of the rule.

Field constraints are the second half. You attach limits to a field with Field, and Pydantic enforces them during validation. A price must be above zero. A username must be between three and twenty characters. A tag list must hold at least one item. The rules sit next to the field, so anyone reading the model can see them.

This article covers the constraints by kind. The number constraints handle ranges and multiples. The string constraints handle length and patterns. Collections have their own limits on size. The last section looks at how constraints combine with default values, and where a default can quietly break a rule you thought you had set. Each constraint also ends up in the JSON Schema, so your documentation stays in step with your checks.

Read it with a real model in mind, such as a form you already have. You will find that most of the rules you currently check by hand can move into the field itself, where they are shorter and easier to see.

`minutes: int` is a weak statement. It permits `0`, `-5000`. A number larger than the age of the universe in seconds. None of those are durations. The annotation captures the shape of the value and nothing about its meaning.

`Field` closes that gap:

```python
minutes: int = Field(gt=0, le=180)
```

Now the model refuses what the domain refuses. Two things follow from that. The second matters more than people expect.

The first is that bad data stops at the door. The second is that the rule is now written down in the one place a reader will look. A check buried in a service function is invisible to all who doesn't open that function. A constraint on the field is part of the model's meaning. It appears in the made schema, the API docs and your editor's tooltips.

## The number constraints

Four checks, named for the ops: `gt`, `ge`, `lt`, `le`. There's no `eq`. That is what a `Literal` is for.

`multiple_of` constrains the step. This Is more handy than it first appears. Prices in whole pence, durations in five-minute blocks, page sizes in powers of ten.

Choosing between `gt=0` and `ge=1` on an int field is worth a moment. They accept just the same values. They say other things. `gt=0` says *plus*. `ge=1` says *at least one*. Pick the one that matches the sentence you'd say out loud. The error message the caller sees is made from it.

## The string constraints

`min_length` and `max_length` bound the number of characters.

`pattern` takes a regular formula, and there's one detail that catches people. It's a *match from the start*, not a full-string search. `pattern=r"[a-z]+"` will happily accept `"abc123!!!"`. The pattern matched at the beginning and nothing said it had to reach the end. If you mean the whole value, anchor it: `r"^[a-z]+$"`.

That single omission is the most common bug in this area. It fails in the permissive direction. Letting bad values through rather than rejecting good ones. Which is just the way a check bug lives longest.

Keep patterns simple. A regular formula that needs a comment is often better as a `field_validator`. Here You can name the rule and write a clear message. There's a module on those in the next tier.

## Collections

`min_length` and `max_length` work on lists, sets and dicts too, counting items rather than characters.

`min_length=1` is the handy one. "This list must not be empty" is a real rule that would else cost you a checker. It makes a better error than a downstream `IndexError`.

## Constraints and defaults

`Field` carries the default and the rules:

```python
minutes: int = Field(default=10, gt=0, le=180)
```

A field with constraints and no default is still needed. `Field(gt=0)` doesn't make anything optional. This trips people who read `Field(...)` as being like a default.

For mutable or found defaults, `default_factory` belongs here too: `Field(default_factory=list, max_length=8)` gives you an empty list per instance and a cap on how many items it may grow to.

You may also see `Field(...)` with a literal ellipsis in older code. That was the v1 way of writing "needed". It still works. Simply omitting the default is clearer.

## Order of operations

Constraints run **after** coercion, and knowing that drops a class of confusion.

A field declared `int = Field(gt=0)` given the string `"5"` first turns the int `5`, then is checked against zero. The compare never sees the text. Likewise a `str` field with `min_length=3` counts characters after any string coercion has happened.

So a value can fail in two distinct ways, with two distinct error types: `int_parsing` if it couldn't become an int at all, `greater_than` if it became one and was too small. Your error handling gets both for free. They mean truly other things to a caller.

## Metadata is documentation

`Field` also carries `title`, `description` and `examples`. They change no action whatsoever. They're the highest-value thing in this module.

They land in `model_json_schema()`. If you're using FastAPI, that schema *is* your API docs. The descriptions appear next to the fields, the examples pre-fill the interactive request form, the constraints show as the documented limits. You write a sentence in the model and it appears in the docs your consumers read.

For anything with an audience beyond yourself, show the fields whose meaning isn't obvious from the name. `minutes` needs no description. `weight` badly does. Of what, in what unit?

## What constraints are not for

A constraint is a statement about a single value in alone. Anything that depends on another field. An end date after a start date, a discount not exceeding a price. Can't be expressed here. A field constraint can't see its siblings. That is what `model_validator` is for.

Anything needing a lookup &mdash; does this track exist, is this name taken &mdash; also doesn't belong here. A model should be able to validate without touching a DB. Keep I/O-dependent rules in the layer that owns the I/O.

And a constraint isn't a substitute for thinking about the type. If a field can only be one of four strings, `Literal["maths", "python", "dsa", "ml"]` is better than a pattern. It's clearer, it makes a better error. It appears in the schema as an enumeration a client can render as a dropdown.

## Annotated: the other spelling

all in this module can also be written with `Annotated`. In modern Pydantic that spelling is often the better one:

```python
from typing import Annotated
from pydantic import Field

minutes: Annotated[int, Field(gt=0, le=180)]
```

The two forms behave the same way for a simple field. The gap appears when a default is involved, and it's a real gain:

```python
minutes: Annotated[int, Field(gt=0, le=180)] = 10
```

Here the constraint lives with the type and the default sits where defaults most times sit. In the `= Field(default=10, gt=0)` form the two are tangled together in one call. It's easy to misread which part is the default.

The bigger win is reuse. This The next section is about.

## Constrained types you can name

Because `Annotated` makes a type, you can give it a name and use it all over:

```python
Minutes = Annotated[int, Field(gt=0, le=180)]
Slug = Annotated[str, Field(pattern=r"^[a-z0-9_]+$")]

class Module(BaseModel):
    slug: Slug
    minutes: Minutes = 10

class Lesson(BaseModel):
    slug: Slug
    minutes: Minutes
```

This is the single highest-value habit in this module. The rule for what a slug is now exists once. Change it and each model that uses it changes. Without this, the same regular formula gets copied into six models and four of them are updated when it changes.

It also raises the reading. `slug: Slug` says what the field is. `slug: str = Field(pattern=r"^[a-z0-9_]+$")` makes the reader parse a regular formula to find out.

Pydantic ships some of these ready-made. `PositiveInt`, `NonNegativeInt`, `PositiveFloat`, `StrictStr` and others. And they're worth using where they fit, for the same reason.

## Strictness on a single field

Whole-model strictness is a blunt instrument. often the need is narrower. Lax about most of a payload, exact about one field where a silent conversion would be dangerous.

```python
user_id: int = Field(strict=True)
```

Now `user_id="123"` raises while the rest of the model still accepts strings for its numbers. Identifiers are the classic case. An id that arrives as text is often a sign that a thing upstream is confused. Quietly converting it hides that.

The `Annotated` form works too: `Annotated[int, Field(strict=True)]`. This Can then be named and reused like any other constrained type.

## More than one constraint, and how failures report

A field can carry a few constraints. They're all checked. If more than one fails, you get more than one error entry for that field:

```python
title: str = Field(min_length=3, max_length=10, pattern=r"^[A-Z]")
```

Given `"ab"`, both `min_length` and `pattern` fail. Both appear. That is worth knowing when you build the field-to-messages mapping given in the errors module. A field maps to a *list* of messages, not one.

Constraints are checked after coercion, and a coercion failure short-circuits the rest. There's no point checking a value against zero when it never became a number. So a field makes either one `*_parsing` error or one or more constraint errors, never both.

## What the schema does with them

each constraint has a JSON Schema equal, and Pydantic emits it:

`gt` turns `exclusiveMinimum`, `ge` turns `min`, `lt` turns `exclusiveMaximum`, `le` turns `max`. `min_length` and `max_length` become `minLength`/`maxLength` for strings and `minItems`/`maxItems` for arrays. `pattern` turns `pattern`. `multiple_of` turns `multipleOf`.

This is why constraints are better than checkers when either would do. A `field_validator` that checks `v > 0` is invisible to the schema. The docs says "int", the client-side form has no idea. The made client will happily send `-1`. `Field(gt=0)` appears in the docs as a documented min. Tooling that reads the schema can enforce it before a request is ever made.

The general rule: express a rule as a constraint if a constraint can express it. Reach for a checker only when it can't.

## Constraints that are really types

Finally, a check worth running on yourself. If a constraint is trying to enumerate a small set of allowed values, it's the wrong tool.

```python
track: str = Field(pattern=r"^(maths|python|dsa|ml)$")     # works
track: Literal["maths", "python", "dsa", "ml"]             # better
```

The second version makes a clearer error, appears in the schema as an enumeration a client can render as a dropdown. Is checked by mypy in your own code. The regular formula does none of that. It will be the thing somebody forgets to update when a fifth track is added.

## A short catalogue to work from

all on hand, in one place. So You can stop looking it up.

**Numbers:** `gt`, `ge`, `lt`, `le`, `multiple_of`. Also `allow_inf_nan=False` for floats. This Is worth setting on anything that will be serialised to JSON. `Infinity` and `NaN` aren't valid JSON. A value that checked happily will fail on the way out.

**Strings:** `min_length`, `max_length`, `pattern`. Plus the config-level `str_strip_whitespace`, `str_to_lower` and `str_to_upper`. This Apply to each string field on a model. Stripping whitespace on input is almost always the right default for form data.

**sets:** `min_length`, `max_length`.

**Decimals:** `max_digits` and `decimal_places`. This Are what you want for money and which no amount of `float` will give you.

**all:** `strict`, `frozen` on a single field, `description`, `title`, `examples`, `deprecated`, `repr=False`, `exclude=True`.

## The habit this module is really teaching

Look at the constraints you've written and ask what a reader learns from them. A well-constrained model is a specification. Someone can read the class and know what the system considers a valid module, without opening a single function.

An unconstrained model is a list of types. The actual rules are scattered through the code that consumes it. A check here, an assertion there, an assumption one spot else that no one wrote down. Those rules still exist. They're just not anywhere you can read them. They disagree with each other more often than anyone expects.

Moving a rule into the model isn't primarily about catching bad data, though it does that. It's about having one place where the shape of your domain is stated. This Is the same reason the annotations were worth enforcing in the first place.

## Next

That ends the foundations. You can define a model, know just what it will and won't convert, control what is needed, narrow values to your domain. Read the errors when a thing doesn't fit.

The last module in this tier steps back to a question worth answering before you reach for a model at all. When a plain dataclass is the better tool.
''',
    [
        {"q": "What does `pattern=r\"[a-z]+\"` accept?",
         "options": ["Only all-lowercase strings", "Also 'abc123!!!' - it matches from the start but need not reach the end", "Nothing", "Any string"],
         "answer": 1,
         "why": "`pattern` matches from the start rather than requiring the whole string. Without `^...$` anchors it fails permissively, which is how this bug survives longest."},
        {"q": "A field is `int = Field(gt=0)` and receives `\"5\"`. What happens?",
         "options": ["Rejected - it is a string", "Coerced to 5, then compared against 0, and accepted", "Compared as text", "Rejected - gt needs a float"],
         "answer": 1,
         "why": "Constraints run after coercion. That is also why the two failure modes have different error types: `int_parsing` versus `greater_than`."},
        {"q": "Does `Field(gt=0)` with no default make a field optional?",
         "options": ["Yes", "No - it is still required", "Only for ints", "It defaults to 0"],
         "answer": 1,
         "why": "Requiredness is decided by the presence of a default. `Field` with only constraints supplies no default, so the field stays required."},
        {"q": "Why write `description=` on a field?",
         "options": ["It makes validation stricter", "It appears in the generated JSON Schema and therefore in API docs", "It is required", "It speeds up validation"],
         "answer": 1,
         "why": "Metadata changes no behaviour but flows into `model_json_schema()`, which FastAPI renders as documentation. It is the cheapest documentation available."},
    ],
)


# ---------------------------------------------------------------------------
# 7. Pydantic vs dataclasses
# ---------------------------------------------------------------------------
topic(
    "pydantic_vs_dataclasses",
    "Pydantic vs Dataclasses",
    "Foundations",
    "Both give you a class from annotations. Only one checks anything - and the "
    "cost of checking is the whole decision.",
    _svg(_box(12, 24, 60, 42, S) + _txt(42, 40, "dataclass", M, 8) + _txt(42, 54, "no checks", M, 8) +
         _box(88, 24, 60, 42, S, A) + _txt(118, 40, "BaseModel", A, 8) + _txt(118, 54, "validates", A, 8)),
    [
        ("Side by side",
         "The class bodies are nearly identical. What they do with a wrong value is "
         "not.",
         '''from dataclasses import dataclass, asdict
from pydantic import BaseModel, ValidationError

@dataclass
class ModuleDC:
    title: str
    minutes: int

class ModuleBM(BaseModel):
    title: str
    minutes: int

d = ModuleDC(title="Norms", minutes="eight")
print("dataclass accepted :", d)
print("   minutes is a    :", type(d.minutes).__name__)

try:
    ModuleBM(title="Norms", minutes="eight")
except ValidationError as e:
    print("pydantic refused   :", e.errors()[0]["msg"])

print()
print("both convert to dicts:")
print("  ", asdict(d))
print("  ", ModuleBM(title="Norms", minutes=8).model_dump())'''),

        ("A dataclass will take anything",
         "It generates an <code>__init__</code> that assigns. It does not look at the "
         "annotations at all beyond deciding which fields exist.",
         '''from dataclasses import dataclass

@dataclass
class Module:
    title: str
    minutes: int
    published: bool

m = Module(title=None, minutes=[1, 2, 3], published="perhaps")
print("constructed happily:", m)
print()
print("title     :", type(m.title).__name__)
print("minutes   :", type(m.minutes).__name__)
print("published :", type(m.published).__name__)

# Nothing is wrong until something downstream assumes otherwise:
try:
    print(m.minutes / 2)
except TypeError as e:
    print()
    print("and here it finally breaks:", e)'''),

        ("Speed is the real trade",
         "A dataclass is faster to build because it does nothing. Where the data is "
         "already trustworthy, that difference is free.",
         '''import time
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class PointDC:
    x: float
    y: float

class PointBM(BaseModel):
    x: float
    y: float

N = 20000

t = time.perf_counter()
for i in range(N):
    PointDC(x=1.0, y=2.0)
dc = time.perf_counter() - t

t = time.perf_counter()
for i in range(N):
    PointBM(x=1.0, y=2.0)
bm = time.perf_counter() - t

print("dataclass : %.3f s" % dc)
print("pydantic  : %.3f s" % bm)
print("ratio     : %.1fx" % (bm / dc))
print()
print("Everything here runs slower than a real interpreter, so the")
print("ratio is the number that transfers, not the seconds.")'''),

        ("Use both, at different depths",
         "The usual answer is not one or the other. Validate at the boundary, then "
         "work with something cheap inside.",
         '''from dataclasses import dataclass
from pydantic import BaseModel

# The boundary: whatever arrived, checked once.
class ModuleIn(BaseModel):
    title: str
    minutes: int

# The interior: trusted, cheap, used in hot loops.
@dataclass
class Module:
    title: str
    minutes: int

    def reading_time(self) -> str:
        return "about %d min" % round(self.minutes * 1.2)

raw = {"title": "Eigenvalues", "minutes": "14"}   # note the string

checked = ModuleIn.model_validate(raw)            # validate ONCE
module = Module(**checked.model_dump())           # then go cheap

print("validated :", checked)
print("internal  :", module)
print("derived   :", module.reading_time())'''),

        ("Pydantic can validate a dataclass too",
         "If you like the dataclass API but want the checking, "
         "<code>pydantic.dataclasses.dataclass</code> is a drop-in that validates.",
         '''from pydantic.dataclasses import dataclass
from pydantic import ValidationError

@dataclass
class Module:
    title: str
    minutes: int

print("coerces  :", Module(title="Norms", minutes="8"))

try:
    Module(title="Norms", minutes="eight")
except ValidationError as e:
    print("refuses  :", e.errors()[0]["msg"])

# It is still a real dataclass:
import dataclasses
print()
print("is a dataclass:", dataclasses.is_dataclass(Module))
print("fields        :", [f.name for f in dataclasses.fields(Module)])'''),

        ("Validating anything with TypeAdapter",
         "You do not need a model at all to get validation. "
         "<code>TypeAdapter</code> applies the same machinery to any annotation.",
         '''from typing import Dict, List
from pydantic import TypeAdapter, ValidationError

minutes = TypeAdapter(List[int])
print("list :", minutes.validate_python(["8", "12", 14.0]))

lookup = TypeAdapter(Dict[str, float])
print("dict :", lookup.validate_python({"maths": "4.5", "python": 4}))

try:
    minutes.validate_python(["8", "soon"])
except ValidationError as e:
    err = e.errors()[0]
    print("bad  :", err["loc"], err["msg"])

# Useful for a function argument, a config blob, or a JSON array
# that has no natural model around it.'''),
    ],
    [
        "A <code>@dataclass</code> reads annotations only to decide which fields exist. It never checks a value, ever.",
        "A <code>BaseModel</code> validates and coerces on construction. That costs time, and buys a guarantee.",
        "The honest comparison is not “which is better” but “where am I”. At a boundary, validate. Inside trusted code, do not pay for it twice.",
        "<code>pydantic.dataclasses.dataclass</code> gives the dataclass API with validation &mdash; handy when a dataclass already exists and you want checking without a rewrite.",
        "<code>TypeAdapter</code> validates any annotation &mdash; <code>List[int]</code>, <code>Dict[str, float]</code> &mdash; with no model required.",
        "A <code>NamedTuple</code> or <code>TypedDict</code> also checks nothing at runtime. Only Pydantic and libraries like it act on annotations while the program runs.",
    ],
    '''
title: Pydantic or a Dataclass? A Question Worth Answering Properly
intro: Both build a class from annotations. Only one checks anything. That is the whole choice.

## They look almost identical

Python already has dataclasses, and they look a lot like Pydantic models. You list fields with types, and you get an object with an init method written for you. So a fair question is why you would add a library for the same thing.

The answer is that the two do different jobs. A dataclass stores data in a tidy shape. It does not check it. If you pass a string where an integer belongs, the dataclass accepts it without complaint. Pydantic treats the annotations as rules and enforces them. That single difference decides which one belongs where.

This article compares them honestly. You will see how similar they look at first glance, and what a dataclass really does for you. Then it covers what the extra guarantee costs, in speed and in strictness. Many projects end up using both, and the article explains how to decide which goes where. It closes with a middle option, which is Pydantic's own dataclass decorator, and says when that choice makes sense.

If you already use dataclasses, nothing here asks you to throw them away. The goal is to give you a clear rule for choosing. That rule will save you from two common mistakes. One is adding validation to code that does not need it. The other is trusting data that was never checked. Both are easy to make, and both look reasonable at the time. Seeing the same class written both ways makes the trade-off concrete, and that is how the article is laid out. You can then apply the same test to any new class you write.

Both tools have a fair place in a project.

```python
@dataclass
class Module:
    title: str
    minutes: int

class Module(BaseModel):
    title: str
    minutes: int
```

Two lines of gap, and both give you a constructor, a readable `repr`, equality by value and a way to get a dict out. It's fully fair to wonder whether the choice matters.

It matters in just one place: what happens when the data is wrong.

## What a dataclass actually does

`@dataclass` reads the annotations to find out which fields exist and in what order. Then makes an `__init__` that assigns them. That is the extent of its interest in the types. The annotation `minutes. Int` is used to decide that a field called `minutes` exists. Its being an `int` is never checked, tested or acted on.

So `Module(title=None, minutes=[1, 2, 3], published="perhaps")` makes just right happily. Nothing is wrong until a thing downstream assumes the annotation was true. And then it fails one spot else, with a traceback pointing at the innocent party.

This isn't a flaw. A dataclass is a code-making convenience. It does what it advertises. It just doesn't do the thing people at times assume it does.

`NamedTuple` and `TypedDict` are in the same spot. It's worth saying because `TypedDict` in given looks like it should be checking a thing. It isn't. It's a description for static type checkers, invisible at runtime.

## What that guarantee costs

check is real work: reading a schema, checking each field, at times converting. It isn't free. Any honest compare has to say so.

The timing in the third editor above is worth running. Pydantic 2's core is Rust. The gap is far smaller than it was in v1. But A dataclass is still faster, for the simple reason that doing nothing is quicker than doing a thing.

Read the *ratio* rather than the seconds. all on this page runs on CPython compiled to WebAssembly. This Is a few times slower than a native interpreter. The scaled compare holds. The abs numbers don't transfer to your laptop.

And put the ratio in context. A model that validates in a few microseconds is irrelevant next to a DB query taking milliseconds, or a network call taking hundreds. check cost matters in tight loops over large sets. Almost nowhere else. Choosing a dataclass "for speed" in a request handler that then makes three SQL queries is optimising the wrong end.

## The answer is usually both

The instinct to pick one and use it all over is what makes this question feel harder than it's. The better framing is *where in the system am I*.

At the **boundary** &mdash; a request body, a config file, a CSV, another service's response &mdash; the data is a guess until proven else. Validate. This is the whole point of the library. The cost is paid once per item arriving.

**Inside**, past that line, the data has already been checked. Re-checking it at each layer buys nothing. The same values, checked again, will pass again. If you've a hot loop over ten thousand records, a dataclass is a fair interior form, and converting is one line:

```python
checked = ModuleIn.model_validate(raw)   # validate once
module = Module(**checked.model_dump())  # then go cheap
```

Be honest about whether you need that, though. For most uses, using models throughout is simpler. Simpler is worth more than a microsecond. The two-form pattern earns its keep when profiling has really pointed at check.

## The middle option

If you like the dataclass API. Or you've a code full of them. `pydantic.dataclasses.dataclass` is a drop-in swap that validates:

```python
from pydantic.dataclasses import dataclass

@dataclass
class Module:
    title: str
    minutes: int
```

Same decorator shape, same `dataclasses.fields()` introspection. Now `minutes="eight"` raises. It's a good way to add checking to existing code without rewriting it into models.

The trade is that you get less of Pydantic. `model_dump`, aliases, custom serialisers and the richer config surface belong to `BaseModel`. For anything that is going to be serialised, aliased or documented, a real model is the better home.

## Validating without a class at all

`TypeAdapter` is the piece most people meet late and wish they had met early. It applies the whole check machinery to any annotation, with no model in sight:

```python
TypeAdapter(List[int]).validate_python(["8", "12", 14.0])   # [8, 12, 14]
```

That is truly handy. A JSON array of numbers has no natural model wrapped around it. Neither does a `Dict[str, float]` of settings, or the arg to a function you want to check at its edge. Building a one-field model to hold a list is a common workaround. `TypeAdapter` is the thing it was working around.

It gets a full module in the output tier. It also handles dumping and schema making for bare types.

## A short decision list

Reach for **`BaseModel`** when data crosses a boundary, when you need output or aliases, or when the thing should appear in an API schema. This is most of the time.

Reach for **`@dataclass`** for inner values that never leave the process and never arrive from outside it. And where you've a reason beyond habit.

Reach for **`pydantic.dataclasses.dataclass`** when you want check on a dataclass that already exists.

Reach for **`TypeAdapter`** when the thing you need to validate isn't a class.

## The rest of the field

Dataclasses aren't the only option, and the others sit in predictable places.

**`attrs`** is the library dataclasses were inspired by. It's still ahead in features. Converters, richer checkers, better control over made methods. It does validate, if you ask it to. It's a fair choice for inner classes with complex build. It isn't aimed at the boundary and doesn't make JSON Schema.

**`NamedTuple`** gives you an immutable, tuple-shaped record with named access. It checks nothing at runtime. Its tuple-ness is either the point or a trap based on whether you wanted a thing you can unpack and compare positionally.

**`TypedDict`** shows the shape of a dict for a static type checker. It's worth being clear about this one. At runtime, a `TypedDict` **is a plain dict**. There's no class, no checking. No error if a key is missing or the wrong type. It's a comment mypy can read. Where people often want a `TypedDict` and check, what they want is a model.

**`SQLModel`** joins Pydantic and SQLAlchemy so one class can be both a table and a checked model. It's convenient and it's a coupling. Your API shape and your DB schema become the same object. This Is fine until they need to differ. This They eventually do.

## Memory, and the shape of an instance

A `BaseModel` instance stores its data in `__dict__` plus some bookkeeping. `__pydantic_fields_set__` for what was supplied. A link to the compiled checker on the class.

A dataclass also uses `__dict__` unless you declare `slots=True`. This Trades the ability to add fields for a smaller, faster object. A `NamedTuple` is the smallest of the lot, being a tuple.

For thousands of objects this is invisible. For millions it isn't. It's a real reason to use a thing leaner for the interior of a numeric or batch-handling system. It's also a reason not to worry about it before you've measured. "millions of objects" is a exact situation rather than a general one.

## Moving between them

Conversion is rote in each direction. This Is what makes the boundary-then-interior pattern hands-on.

From model to dataclass: `Module(**checked.model_dump())`.

From dataclass to model: `ModuleIn.model_validate(dataclasses.asdict(d))`, or `model_validate(d)` right. Pydantic can read fields off any objects when the model sets `from_attributes=True`.

That last setting deserves a mention of its own. `from_attributes=True` lets a model validate from any object with matching fields rather than needing a dict:

```python
class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    minutes: int

ModuleOut.model_validate(orm_row)
```

This is how a model reads an ORM row. It's the single most common reason to reach for it. In Pydantic v1 it was called `orm_mode`. This Is the name most tutorials still use.

## When a model is genuinely too much

A short list of cases where reaching for `BaseModel` is over-engineering.

A function returning two values doesn't need a model. A tuple, or a `NamedTuple` if the names help, is fine.

A short-lived inner structure that never leaves the function that built it doesn't need check. Nothing untrusted can reach it.

A constant lookup table is a dict. Wrapping it in a model to get field access is a lot of ceremony for a dot.

And a value with one field is often just that value. `class Slug(BaseModel). Value: str` is a wrapper that each caller has to unwrap. If you want a checked string type, `Annotated[str, Field(pattern=...)]` gives you that without the box.

## The question to actually ask

Not "which is faster" or "which is more modern", but: **does anything untrusted reach this object. Does it ever leave the process?**

If untrusted data reaches it, you need check. `BaseModel` is the tool built for that.

If it leaves the process. As JSON, in a response, in a schema &mdash; you want output and docs, and again that is `BaseModel`.

If neither is true, you've an inner value. The lightest thing that expresses it well is the right answer. That will often be a dataclass, and at times a tuple.

Most objects in most uses are at a boundary. This Is why the honest general recommendation is to use models and stop worrying about it. The notable cases are the exceptions. Now you can recognise them.

## A note on migrating an existing codebase

If you arrive at this with a project full of dataclasses, you don't have to choose in one go.

The cheapest first move is to convert only the classes that sit at a boundary. What parses your config, what accepts a request body, what reads a file. Those are where bad data enters. They're often a small fraction of the classes in a project. all else can stay just as it's.

The second move, if you want checking without restructuring, is `pydantic.dataclasses.dataclass` on the classes that stay. It's a one-line change per class, keeps `dataclasses.fields()` working for anything that introspects them. Starts raising on wrong types at once.

What you shouldn't do is convert all to `BaseModel` mechanically. You'll end up checking objects that were made by your own code from already-checked data, paying for checks that can't fail. The diff will be too large for anyone to review properly.

## Summary

A dataclass makes a class from annotations and never looks at the types again. A model makes a class from annotations and enforces them, converts what can be converted, makes structured errors, serialises in both directions and emits a schema.

The cost of all that is real and small. It's paid where you decide to pay it. The discipline is the same one this whole tier has been building towards. Know where your boundaries are, check there, and trust what you've checked.

Choose a dataclass for inner values that never meet the outside world. Choose a model for all else. And when you're truly unsure, choose the model. A slightly over-checked program is a much smaller problem than one where no one can say which values are sure.

## Where this leaves you

That is tier one. You can define a model, predict just what it will convert, control what is needed and what is merely nullable, narrow values to your domain with constraints, read the errors when data doesn't fit. Choose between a model and a plain class on grounds better than taste.

The next tier is about data with shape. Models inside models, lists of them, unions that pick between options. The standard-library types. Dates, UUIDs, decimals. That Pydantic already knows how to handle.
''',
    [
        {"q": "What does `@dataclass` do with the annotation `minutes: int`?",
         "options": ["Checks the value is an int", "Converts the value", "Uses it only to decide the field exists", "Raises if it is wrong"],
         "answer": 2,
         "why": "A dataclass reads annotations to discover the fields and generate an `__init__` that assigns them. The types are never checked at runtime."},
        {"q": "Where does validation genuinely earn its cost?",
         "options": ["Everywhere, always", "At the boundary where untrusted data arrives", "Only in tests", "Nowhere - it is too slow"],
         "answer": 1,
         "why": "Data crossing into your code is a guess until checked. Past that line it has already been proven, and re-checking the same values buys nothing."},
        {"q": "You need to validate a bare `List[int]` with no model around it. What do you use?",
         "options": ["A one-field wrapper model", "TypeAdapter", "A dataclass", "It cannot be done"],
         "answer": 1,
         "why": "`TypeAdapter(List[int])` applies the full machinery to any annotation. The wrapper model is the workaround people use before they discover it."},
        {"q": "What does `pydantic.dataclasses.dataclass` give you?",
         "options": ["Nothing different", "The dataclass API with validation added", "A faster dataclass", "A BaseModel"],
         "answer": 1,
         "why": "It is a drop-in that keeps dataclass introspection while validating on construction - useful for adding checks to existing dataclasses without rewriting them as models."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Nested models
# ---------------------------------------------------------------------------
topic(
    "nested_models",
    "Nested Models",
    "Real Data Shapes",
    "Models inside models: composition, dicts that become objects, and error "
    "paths that reach all the way down.",
    _svg(_box(14, 16, 132, 60, S) + _txt(80, 30, "Track", A, 9) +
         _box(26, 38, 50, 30, S) + _txt(51, 56, "Module", M, 8) +
         _box(84, 38, 50, 30, S) + _txt(109, 56, "Author", M, 8)),
    [
        ("A model can be a field type",
         "Annotate a field with another model and Pydantic validates the inner one "
         "too. A plain dict on the way in becomes a real object on the way out.",
         '''from pydantic import BaseModel

class Author(BaseModel):
    name: str
    email: str

class Module(BaseModel):
    title: str
    author: Author          # <- another model

m = Module(title="Vectors",
           author={"name": "Ada", "email": "ada@vizlearn.in"})

print(m)
print()
print("author is a :", type(m.author).__name__)
print("dotted acces:", m.author.name)
print("not a dict  :", isinstance(m.author, dict))'''),

        ("Errors carry the whole path",
         "This is where <code>loc</code> earns its design. The path names the route "
         "to the bad value, not just the top-level field that contained it.",
         '''from pydantic import BaseModel, ValidationError

class Author(BaseModel):
    name: str
    email: str

class Module(BaseModel):
    title: str
    author: Author

try:
    Module(title="Vectors", author={"name": None, "email": 42})
except ValidationError as e:
    for err in e.errors():
        path = ".".join(str(p) for p in err["loc"])
        print("%-16s %s" % (path, err["msg"]))

print()
# Compare with a failure at the top level:
try:
    Module(title="Vectors", author="Ada")
except ValidationError as e:
    err = e.errors()[0]
    print("%-16s %s" % (".".join(str(p) for p in err["loc"]), err["msg"]))'''),

        ("Nesting goes as deep as you like",
         "Three levels behaves exactly like two. The path simply gets longer, which "
         "is the point &mdash; it stays readable however deep the payload is.",
         '''from typing import List
from pydantic import BaseModel, ValidationError

class Lesson(BaseModel):
    name: str
    minutes: int

class Module(BaseModel):
    title: str
    lessons: List[Lesson]

class Track(BaseModel):
    title: str
    modules: List[Module]

data = {"title": "Maths", "modules": [
    {"title": "Vectors", "lessons": [
        {"name": "Direction", "minutes": 4},
        {"name": "Magnitude", "minutes": "soon"},   # <- three levels down
    ]},
]}

try:
    Track.model_validate(data)
except ValidationError as e:
    err = e.errors()[0]
    print("path :", err["loc"])
    print("read :", ".".join(str(p) for p in err["loc"]))
    print("said :", err["msg"])'''),

        ("Optional and defaulted nested models",
         "The rules from the defaults module apply unchanged. A nested model can be "
         "absent, null, or given a default like anything else.",
         '''from typing import Optional
from pydantic import BaseModel, Field

class Author(BaseModel):
    name: str = "unknown"
    email: Optional[str] = None

class Module(BaseModel):
    title: str
    author: Optional[Author] = None            # may be absent entirely
    reviewer: Author = Field(default_factory=Author)   # always present

bare = Module(title="Norms")
print("no author    :", bare.author)
print("but reviewer :", bare.reviewer)
print()

full = Module(title="Norms", author={"name": "Ada"})
print("given        :", full.author)
print("inner default:", full.author.email)'''),

        ("Dumping and reloading a nested tree",
         "<code>model_dump()</code> recurses, so the whole tree comes back as nested "
         "dicts &mdash; and that output is valid input again.",
         '''from typing import List
from pydantic import BaseModel

class Lesson(BaseModel):
    name: str
    minutes: int

class Module(BaseModel):
    title: str
    lessons: List[Lesson]

m = Module(title="Vectors", lessons=[
    {"name": "Direction", "minutes": 4},
    {"name": "Magnitude", "minutes": 6},
])

d = m.model_dump()
print("dict  :", d)
print("inner :", type(d["lessons"][0]).__name__, "- plain dicts, all the way down")
print()
print("json  :", m.model_dump_json())
print()
again = Module.model_validate(d)
print("round trip equal:", again == m)'''),

        ("Trimming what comes out",
         "<code>exclude</code> reaches into nested models with a dict, which is how "
         "you keep an internal field out of a public response.",
         '''from typing import List
from pydantic import BaseModel

class Author(BaseModel):
    name: str
    email: str

class Module(BaseModel):
    title: str
    author: Author
    internal_notes: str

m = Module(title="Vectors",
           author={"name": "Ada", "email": "ada@vizlearn.in"},
           internal_notes="needs a diagram")

print("everything :", m.model_dump())
print()
print("public     :", m.model_dump(exclude={"internal_notes": True,
                                            "author": {"email"}}))
print()
print("just a bit :", m.model_dump(include={"title": True,
                                            "author": {"name"}}))'''),
    ],
    [
        "A field annotated with a model validates that model too. Dicts on the way in become real objects, recursively.",
        "<code>loc</code> is the route to the failure: <code>('author', 'email')</code> is one level down, and it keeps working however deep the tree goes.",
        "A nested model is validated with its own rules, including its own validators, defaults and constraints. Nothing is skipped because it is inside something else.",
        "Use <code>default_factory</code> for a nested model that should always exist. A plain <code>= Author()</code> would share one instance across every parent.",
        "<code>model_dump()</code> recurses into nested models, and its output is valid input to the same model again.",
        "<code>include</code> and <code>exclude</code> take nested dicts &mdash; <code>exclude={\"author\": {\"email\"}}</code> drops one inner field and keeps the rest.",
    ],
    '''
title: Nested Models: Structure That Validates Itself
intro: Models inside models, and the error paths that make deep payloads debuggable.

## Composition is the whole mechanism

Real data has structure. A course has modules. A module has an author. An order has a customer and a list of items. Flat models cannot describe that, so Pydantic lets one model appear as the type of a field in another.

That is all nesting is. You do not write any special code to make it work. When the outer model validates, it hands each inner piece to the inner model, and the inner model checks it by its own rules. A plain dictionary goes in. A tree of typed objects comes out.

This article explains how composition works and why it needs so little from you. You will see how a dictionary becomes an object at every level of the tree. You will also see how errors report the exact path to the bad value, which matters when the data is three levels deep. The last part makes the point that every rule you set on a model still applies when that model is used inside another one. Constraints, defaults and validators all come along without extra effort.

This is the point where models start to look like the data you actually handle, so it is worth getting comfortable with it. Nothing new is needed beyond what you have already seen.

There's no special syntax for nesting. A model is a type. A field can be annotated with any type. A field can be a model:

```python
class Author(BaseModel):
    name: str
    email: str

class Module(BaseModel):
    title: str
    author: Author
```

That is it. all else follows from that one fact. This Is worth stating plainly because people often expect a nested schema to need declaring somehow. It doesn't. If you can write the inner model on its own, you can use it as a field type.

When `Module` is checked, the value for `author` is handed to `Author` for check. If it's already an `Author`, it passes through. If it's a dict, it turns one. If it's neither, the error says so.

## Dicts in, objects out

The conversion from dict to object is the part that makes nesting handy rather than merely possible.

JSON has objects, and Python decodes them as dicts. Without nested models you'd receive `{"author": {"name": "Ada"}}` and reach into it with `data["author"]["name"]`. Two dict lookups, each of which can raise `KeyError`, neither of which your editor can help with.

With nesting you get `m.author.name`. It's checked, it's autocompleted. A typo is an `AttributeError` at the point of the typo rather than a `KeyError` one spot downstream.

The reverse works too: `model_dump()` recurses. The result is nested plain dicts. So a model tree converts to and from JSON structure without you writing any of the walking.

## Errors that name the exact value

Nesting is where the `loc` design pays off. It's worth dwelling on because it's the gap between a debuggable API and an infuriating one.

A failure two levels down makes `loc: ("author", "email")`. Joined with dots, `author.email`. Three levels down with a list in the middle makes `("modules", 0, "lessons", 1, "minutes")`. The second lesson of the first module.

Compare that with what a hand-rolled checker often manages: "invalid module". For a payload of any size, the gap is between a caller who can fix the problem in ten seconds and one who has to bisect their own request.

There's a related failure worth recognising. If the value for a nested field isn't a mapping at all. A string, say. The error is on the field itself, with `loc: ("author",)` and the type `model_attributes_type`. That means "I couldn't even begin to read this as an Author". This Is a other problem from a field inside it being wrong. The shape of the error tells you which you've.

## Every rule still applies, at every level

A nested model isn't a lesser thing. Its constraints run, its checkers run, its defaults are filled, its config applies.

```python
class Author(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@]+@[^@]+\\.[^@]+$")
```

Use that as a field type and each parent gets those rules for free. This is the compounding gain of composition. A well-given small model is reusable. Each place it's reused takes from the entire specification rather than a copy of it that can drift.

It's also the arg for making small models. `Address`, `Money`, `DateRange`, `Contact`. Anything that appears in more than one place and has rules of its own is a model waiting to be extracted. The option is the same four fields and the same three constraints written out in five parent models, four of which get updated when the rule changes.

## Optional and defaulted nested models

The rules from the defaults module apply without change. One of them has a exact trap here.

For a nested model that should always exist, use `default_factory`:

```python
reviewer: Author = Field(default_factory=Author)
```

Not `= Author()`. That formula is checked once, when the class body runs. Each parent would share one `Author` instance. And since models are mutable by default, a change through one parent would be visible through all of them. Pydantic deep-copies simple defaults. But Making the instance at class-meaning time is still the wrong shape. A factory says what you mean.

For a nested model that may truly be absent, `Optional[Author] = None` behaves just as it does for any other type, with the same gap between omitted and by name null.

Note that a nested model whose own fields all have defaults can be built from an empty dict. This At times surprises people: `Module(title="x", author={})` succeeds if each `Author` field has a default. That is correct. It's a good reason to think about whether those inner defaults should exist.

## Shaping the output

`model_dump` takes `include` and `exclude`, and both understand structure. A set names top-level fields. A dict reaches inside. The two spellings don't mix in one literal. Once any entry needs to reach inside, each entry turns a key:

```python
m.model_dump(exclude={"internal_notes": True, "author": {"email"}})
```

That drops one top-level field and one field of the nested model, keeping all else. For lists of models there's a special key, `"__all__"`. This Applies the same pick to each item.

This is truly handy for the common case of one inner form and a few external views. It's also easy to overuse. Once the exclusion dict is more than a couple of entries, a split output model is clearer. It's checked, it appears right in the schema. No one has to trace an exclusion formula to work out what an endpoint really returns.

The rule of thumb: `exclude` for dropping one obviously-inner field, a split model for anything structural.

## Recursive models

A model can refer to itself. This Is how you show trees. Comment threads, group trees, nested menus:

```python
class Node(BaseModel):
    name: str
    children: List["Node"] = []
```

The quotes are needed because the class doesn't exist yet at the point the annotation is written. In modern Python with `from __future__ import annotations`, or in files where all annotations are strings, you can drop them.

Recursive models validate to any depth and dump to nested dicts as you'd expect. Two cautions. Depth is bounded by the recursion limit. Truly deep or maliciously nested input can raise. This Is worth thinking about if the data is untrusted. And a cycle. A node that holds itself. Won't terminate on dump. Pydantic detects some cases and raises. But The honest fix isn't to build cyclic data in a model designed as a tree.

## What good nesting looks like

Extract a model when a group of fields travels together and has rules of its own. `Address` is a model. `city. Str` sitting beside `postcode: str` in four other parents is four copies of a choice.

Keep the tree shallow where you can. Three levels is normal. Six often means the shape is showing your storage rather than your domain. A flatter form with links would read better.

Name inner models for what they're, not for where they sit. `Author` is reusable. `ModuleAuthor` is a name that stops the model being used anywhere else even when it would fit just right.

## Reusing a nested model across parents

The strongest arg for extracting a model is that the rules travel with it.

```python
class Address(BaseModel):
    line1: str = Field(min_length=1)
    city: str
    postcode: str = Field(pattern=r"^[A-Z0-9 ]{4,8}$")
```

Use `Address` in `Customer`, `Invoice` and `Warehouse` and all three enforce the postcode rule. Change the rule and all three change. The option. Three copies of three fields and one regular formula. Is three chances for the copies to diverge, and they'll.

The signal that a model wants extracting is fields that travel together. If `city` and `postcode` never appear apart, they're one concept with two fields. Naming that concept makes the parent shorter and the rule reusable.

## Validating against objects, not just dicts

Nested models most times arrive as dicts. That is what JSON decodes to. at times the source is objects instead. ORM rows, another library's classes. And by default a model won't read fields off an any object.

`from_attributes` changes that:

```python
class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    author: AuthorOut
```

Now `ModuleOut.model_validate(orm_row)` reads `row.title` and `row.author`. Validates the nested object the same way. This is how a model turns a DB row into a response, and it recurses. A row with a related object turns a nested model without any manual walking.

In Pydantic v1 this setting was called `orm_mode`. This Is the name most existing tutorials use.

## Performance, and what nesting costs

A nested model is a check of its own. A parent with three nested models does four validations. A list of fifty nested models does fifty-one.

That is the honest cost, and for a request handler it's irrelevant. The whole tree still validates in microseconds. It turns worth thinking about for bulk work, and the advice is the same as all over else in this library. Validate the tree once at the boundary, then pass the resulting objects around without re-checking.

The exact mistake to avoid is re-checking on the way out. Building a response by making an output model from an already-checked input model re-runs each rule in the tree for no gain. If the shapes are the same, `model_dump()` and a direct build is cheaper. If they differ, the second check is doing real work and is fine.

## A worked shape

Most real payloads are two or three levels, and the pattern is steady:

```python
class Author(BaseModel):
    name: str
    email: str

class Lesson(BaseModel):
    name: str
    minutes: int = Field(gt=0)

class Module(BaseModel):
    title: str
    author: Author
    lessons: List[Lesson] = Field(min_length=1)
```

Read it top to bottom and you've the entire contract. A module has a title, just one author with a name and an email. At least one lesson, each with a plus duration. No function needs to be opened to learn any of that. None of it can drift. It's the code that runs.

That is what nesting buys. Not the convenience of dotted access, though that is pleasant. A specification that is executable.

## The habit to take away

each time you find a group of fields repeated across two models, or a comment showing what shape a dict is meant to have, you've found a nested model waiting to be named.

The cost is three lines. The return is a rule that lives in one place, an error path that says just where a failure was, dotted access instead of chained lookups. A schema that shows the real structure rather than a flat guess of it.

Composition is the least clever feature in this library and one of the most valuable, just because it needs no special syntax. A model is a type. Types go in annotations. all else follows.

## A note on how deep to go

Depth in a model tends to mirror depth in what made the data. That isn't always the shape you want to work with.

A payload that nests six levels because a DB has six joined tables is showing storage, not domain. Flattening it. Or replacing an inner object with a link and fetching apart. Often makes a model that reads better and an API that is easier to consume.

Three levels is comfortable. Four is worth a second look. Beyond that, the question is often not "how do I model this" but "should the caller be receiving all of this at once".

## Next

Nesting one model inside another is half the picture. The other half is sets. Lists of models, dicts keyed by a thing real. What happens to the error path when the failure is in the seventeenth item.

## Summary

A model used as a field type is checked with its full rules, dicts become objects recursively. Errors carry the whole path to the failing value.

Extract a model when fields travel together or a group of them is repeated. Use `default_factory` for a nested default. Reach for `include`/`exclude` to drop a field or two. For a split output model when the gap is structural.
''',
    [
        {"q": "What is the `loc` for a bad `email` inside a nested `author` field?",
         "options": ["('email',)", "('author',)", "('author', 'email')", "It has no loc"],
         "answer": 2,
         "why": "`loc` is the full path to the failing value. That is what makes a deeply nested payload debuggable rather than merely rejected."},
        {"q": "You pass `author=\"Ada\"` where a nested `Author` model is expected. Where does the error point?",
         "options": ["At author.name", "At the author field itself", "At the whole model", "Nowhere - it is accepted"],
         "answer": 1,
         "why": "A string cannot be read as an Author at all, so the failure is on the field rather than inside it - a different problem from one of Author's own fields being wrong."},
        {"q": "Why use `Field(default_factory=Author)` rather than `= Author()` for a nested default?",
         "options": ["It is faster", "`= Author()` is evaluated once at class definition, so every parent would share one instance", "They are identical", "`= Author()` is a syntax error"],
         "answer": 1,
         "why": "The expression runs when the class body runs. A factory is called per instance, which is what a per-parent default needs."},
        {"q": "How do you exclude one field of a nested model from `model_dump`?",
         "options": ["Not possible", "exclude={\"author\": {\"email\"}}", "exclude=\"author.email\"", "Only with a separate model"],
         "answer": 1,
         "why": "`include` and `exclude` accept nested dicts to reach inside. For anything more structural than a field or two, a separate output model reads better and appears correctly in the schema."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Collections of models
# ---------------------------------------------------------------------------
topic(
    "collections_of_models",
    "Collections of Models",
    "Real Data Shapes",
    "Lists, dicts, sets and tuples of models - and what the error path looks like "
    "when it is the seventeenth item that is wrong.",
    _svg(_box(16, 24, 128, 42, S) +
         _box(24, 34, 32, 22, S, A) + _txt(40, 48, "0", A, 8) +
         _box(64, 34, 32, 22, S) + _txt(80, 48, "1", M, 8) +
         _box(104, 34, 32, 22, S) + _txt(120, 48, "2", M, 8)),
    [
        ("A list of models",
         "Each item is validated separately with the inner model's own rules. Dicts "
         "become objects, item by item.",
         '''from typing import List
from pydantic import BaseModel

class Lesson(BaseModel):
    name: str
    minutes: int

class Module(BaseModel):
    title: str
    lessons: List[Lesson]

m = Module(title="Vectors", lessons=[
    {"name": "Direction", "minutes": "4"},     # note the string
    {"name": "Magnitude", "minutes": 6},
])

for lesson in m.lessons:
    print("%-12s %2d min  (%s)" % (lesson.name, lesson.minutes,
                                   type(lesson).__name__))

print()
print("total:", sum(l.minutes for l in m.lessons), "minutes")'''),

        ("The index is in the error path",
         "When one item fails, only that item fails, and the path names its position. "
         "The other items still validate.",
         '''from typing import List
from pydantic import BaseModel, ValidationError

class Lesson(BaseModel):
    name: str
    minutes: int

class Module(BaseModel):
    title: str
    lessons: List[Lesson]

bad = {"title": "Vectors", "lessons": [
    {"name": "Direction", "minutes": 4},
    {"name": "Magnitude", "minutes": "soon"},   # index 1
    {"name": None, "minutes": 5},               # index 2
    {"name": "Basis"},                          # index 3, missing minutes
]}

try:
    Module.model_validate(bad)
except ValidationError as e:
    print("problems:", e.error_count())
    for err in e.errors():
        print("  %-22s %s" % (".".join(str(p) for p in err["loc"]), err["msg"]))'''),

        ("Dicts keyed by something meaningful",
         "<code>Dict[str, Model]</code> validates keys and values independently. The "
         "key appears in the error path just as an index would.",
         '''from typing import Dict
from pydantic import BaseModel, ValidationError

class Stats(BaseModel):
    modules: int
    minutes: int

class Site(BaseModel):
    tracks: Dict[str, Stats]

s = Site(tracks={
    "maths": {"modules": 47, "minutes": "520"},
    "python": {"modules": 46, "minutes": 410},
})

for name, stats in s.tracks.items():
    print("%-8s %2d modules, %d minutes" % (name, stats.modules, stats.minutes))

try:
    Site(tracks={"maths": {"modules": 47, "minutes": "ages"}})
except ValidationError as e:
    print()
    print("path:", e.errors()[0]["loc"])'''),

        ("Sets deduplicate, tuples are positional",
         "A set silently drops repeats, which is usually what you want and "
         "occasionally a surprise. A fixed tuple checks length and position.",
         '''from typing import Set, Tuple
from pydantic import BaseModel, ValidationError

class Module(BaseModel):
    tags: Set[str]
    grid: Tuple[int, int]              # exactly two ints
    scores: Tuple[float, ...]          # any number of floats

m = Module(tags=["maths", "vectors", "maths", "maths"],
           grid=("3", "4"),
           scores=[1, "2.5", 3])

print("tags   :", sorted(m.tags), "<- four in, three out")
print("grid   :", m.grid)
print("scores :", m.scores)

try:
    Module(tags=["a"], grid=(1, 2, 3), scores=[])
except ValidationError as e:
    print()
    print("wrong length:", e.errors()[0]["msg"])'''),

        ("Constraining the collection itself",
         "<code>min_length</code> and <code>max_length</code> apply to the container, "
         "so “at least one” is a constraint rather than a validator.",
         '''from typing import List
from pydantic import BaseModel, Field, ValidationError

class Module(BaseModel):
    title: str
    lessons: List[str] = Field(min_length=1, max_length=4)

print(Module(title="Vectors", lessons=["Direction", "Magnitude"]))

for bad in [[], ["a", "b", "c", "d", "e"]]:
    try:
        Module(title="Vectors", lessons=bad)
    except ValidationError as e:
        err = e.errors()[0]
        print("%-24s %-18s %s" % (str(bad)[:22], err["type"], err["msg"]))'''),

        ("A list is not a model - use TypeAdapter",
         "When the payload is a bare array with no object around it, you do not need "
         "a wrapper model. <code>TypeAdapter</code> validates the annotation directly.",
         '''from typing import List
from pydantic import BaseModel, TypeAdapter, ValidationError

class Lesson(BaseModel):
    name: str
    minutes: int

payload = '[{"name": "Direction", "minutes": "4"}, {"name": "Magnitude", "minutes": 6}]'

lessons = TypeAdapter(List[Lesson])

parsed = lessons.validate_json(payload)
print("parsed :", parsed)
print("typed  :", type(parsed[0]).__name__, "| minutes is", type(parsed[0].minutes).__name__)
print()
print("back out:", lessons.dump_json(parsed).decode())

try:
    lessons.validate_python([{"name": "X", "minutes": "soon"}])
except ValidationError as e:
    print()
    print("errors work the same:", e.errors()[0]["loc"])'''),
    ],
    [
        "Items are validated one at a time with the inner model's full rules &mdash; constraints, validators, defaults and all.",
        "An integer in <code>loc</code> is a sequence index; a string is a field or dict key. <code>('lessons', 1, 'minutes')</code> is the second lesson's duration.",
        "One bad item does not stop the rest being checked. You get every failure in the collection in a single report.",
        "<code>Set[...]</code> deduplicates. A field can come back with fewer items than were sent, which is usually the intent and occasionally a bug.",
        "<code>Tuple[int, int]</code> is checked by position <em>and</em> length; <code>Tuple[int, ...]</code> means any number of that type.",
        "For a bare JSON array with no enclosing object, use <code>TypeAdapter(List[Model])</code> rather than inventing a wrapper model with one field.",
    ],
    '''
title: Collections of Models, and Errors That Know Their Index
intro: Lists, dicts, sets and tuples - what gets checked, what gets converted, and where failures point.

## Item by item

Once you can nest one model inside another, the next step is a field that holds many of them. A course has a list of modules. A report has a dictionary of scores. A shape has a pair of coordinates. These are collections of models, and Pydantic validates them item by item.

Each item gets the full treatment. If one module in a list of fifty is wrong, Pydantic tells you which one. The error includes the position of the bad item, so you do not have to hunt through the input to find it. That small detail makes a large difference once the data comes from a user or another system.

This article covers the collection types one at a time. Lists validate each item and put the index in the error path. Dictionaries check both the keys and the values. Sets remove duplicates, which can be a feature or a surprise. Tuples check the length and the type at each position. Along the way you will see what the error paths look like, so you can read them without guessing. It is a short step from nested models, and it covers most of the shapes real payloads take.

The aim is to make a long payload feel as easy to check as a short one. You will not write any loops. You declare the shape, and the library walks it for you, reporting the position of every failure it finds along the way.

Each type behaves a little differently, so the details are worth a look.

A holder annotation shows two things: the shape of the holder and the type of what is in it. Both are enforced.

```python
lessons: List[Lesson]
```

Given a list, Pydantic walks it and validates each element as a `Lesson`. A dict turns a `Lesson` object. An element that is already a `Lesson` passes through. An element that is neither makes an error. For that element only.

That last part matters more than it sounds. check doesn't abandon the set at the first bad item. It checks all of them and reports all the failures. This For a bulk import is the gap between fixing one row per attempt and seeing the whole problem at once.

## The index is part of the path

An int in `loc` is a spot. So `("lessons", 1, "minutes")` reads as. The `lessons` field, the item at index 1, its `minutes` field.

For a payload with a hundred items this is the entire diagnosis. Without it, "one of your lessons has an invalid duration" sends the caller looking through a hundred objects by hand.

Note that the index is the spot in the *input*. This Is what you want. It lets the caller map the error back to the data they sent. If you're surfacing these to a user editing a form with repeated rows, the index is just the row number to highlight.

## Dicts, and what the key does

`Dict[str, Stats]` validates keys against `str` and values against `Stats`, on its own.

The key type is a real constraint. A handy one. `Dict[int, Stats]` will coerce the string keys that JSON forces on you back into ints. This Is a small annoyance handled once instead of at each read site. JSON object keys are always strings. This comes up more often than you'd expect.

In the error path, the key appears where an index would: `("tracks", "maths", "minutes")`. Same method, same readability.

A caution about key coercion with untrusted data: `Dict[int, X]` given `{"1": ...}` gives you `{1: ...}`. Two keys that differ only as strings can collide as ints. It's a narrow case. It's the kind of thing worth knowing before it happens.

## Sets deduplicate

`Set[str]` given `["maths", "vectors", "maths"]` gives a set of two items. No error, no warning. Deduplication is what a set is for.

That is often the intent. Where it bites is when the copies were real and no one thought about it. A list of tags is fine to deduplicate. A list of readings from a sensor isn't. A `Set[float]` will silently discard each repeated reading.

Sets are also unordered, so the order you sent isn't the order you get back. `model_dump_json` has to give an array from a thing with no defined order. If order matters, use a list. And if uniqueness matters too, check it in a checker. This Gives you an error instead of silent removal.

## Tuples check length and position

There are two spellings and they mean other things.

`Tuple[int, str]` is a fixed shape: just two items, the first an int, the second a string. Length is part of the contract. A three-item input fails with `too_long`.

`Tuple[int, ...]` is a homogeneous sequence of any length. The same as `List[int]` except immutable on the way out.

Fixed tuples are good for truly spot-based data. Coords, RGB values, a dim pair. They're a poor choice for anything where the spots have names. `point[0]` is worse than `point.x` and no one can tell what `config[3]` is. If you find yourself writing a comment to explain the spots, you want a model.

## Constraining the container

`min_length` and `max_length` count items:

```python
lessons: List[str] = Field(min_length=1, max_length=4)
```

`min_length=1` is the handy one. "This must not be empty" is a real rule. Expressing it as a constraint rather than a checker means it appears in the schema as `minItems`. A made client and the API docs both know about it.

Empty sets are worth a moment's thought often. An empty list is a valid list. Code that assumes at least one element will fail on it. Often with an `IndexError` far from the model. Deciding by name whether empty is allowed. Writing that choice down, drops a whole group of downstream surprise.

## Bare arrays and TypeAdapter

Not each payload has an object around it. An endpoint that returns a JSON array of lessons has no natural wrapper model. The classic workaround is to invent one:

```python
class LessonList(BaseModel):      # a box built only to hold a list
    items: List[Lesson]
```

`TypeAdapter` is what that workaround was working around:

```python
lessons = TypeAdapter(List[Lesson])
parsed = lessons.validate_json(payload)
```

You get the same check, the same error paths. `dump_json` in the other direction. It also works for anything else you can annotate. `Dict[str, float]`, `Optional[int]`, a bare `Lesson`, a union.

Build the adapter once and reuse it. Making a `TypeAdapter` compiles a schema. This Isn't free. Doing it inside a loop is a genuine and easily-missed speed mistake. Module level is the right home.

## Performance with large collections

This is the place in Pydantic where check cost turns visible. It's worth being concrete.

checking ten thousand items means ten thousand validations. The work happens in Rust. This Makes it far faster than a Python loop doing the same checks. It isn't free.

The key thing is to let the core do the looping. `TypeAdapter(List[Lesson]).validate_python(rows)` validates the whole list in one call into the compiled core. Writing `[Lesson.model_validate(r) for r in rows]` does the same work with ten thousand round trips between Python and Rust. It's measurably slower for no gain.

If you're streaming a very large file, validate in batches rather than building one huge list, for memory reasons rather than check ones.

And apply the rule from the first tier. Validate once, at the boundary. Re-checking a list of models that has already been checked is the most costly no-op on hand.

## Choosing the container

`List` when order matters or copies are real. Which is most of the time.

`Set` when the values are truly a set and you want deduplication as a feature, not as an accident.

`Dict` when items are looked up by a key that means a thing. If you find yourself scanning a list to find the item with a matching id on each read, a dict keyed by that id is the shape you wanted.

`Tuple` for fixed spot-based data, and only when the spots don't deserve names.

## Mutable defaults, one more time

The rule from the defaults module has a exact shape here that is worth repeating. Sets are where it bites.

```python
lessons: List[Lesson] = []
```

This is safe in Pydantic. The default is deep-copied per instance. Two models never share a list. In plain Python the equal would be the classic shared-mutable-default bug. The habit people bring from there's to reach for `default_factory` reflexively.

That habit isn't wrong, and `Field(default_factory=list)` is arguably clearer about intent. But it's worth knowing which of the two rules you're following. The reason matters. Use a factory because the default must be *found*, not because a literal would be shared.

## Uniqueness without a set

If you want a list. Order preserved, JSON array on the way out &mdash; but copies rejected rather than silently dropped, a set is the wrong tool. Deduplication and rejection are other actions.

The check belongs in a checker. This Is the next tier's subject. The shape is worth seeing now:

```python
@field_validator("tags")
@classmethod
def unique(cls, v: List[str]) -> List[str]:
    if len(set(v)) != len(v):
        raise ValueError("tags must be unique")
    return v
```

The gap from `Set[str]` is what the caller learns. A set tells them nothing and quietly returns fewer items. The checker tells them their input was wrong. For a form where somebody typed the same tag twice, the second is much more handy.

## Nested collections

sets nest as freely as models do, and the error paths keep working:

```python
schedule: Dict[str, List[Lesson]]
```

A failure inside makes `("schedule", "monday", 2, "minutes")`. The key, the index, the field. Four elements. It names just one value in a structure that would else take a while to search by hand.

The hands-on limit is comprehension rather than capability. `Dict[str, List[Dict[str, List[int]]]]` is valid and no one can read it. Once an annotation needs more than about three levels, extracting a model for the inner shape makes the outer one legible again. And gives the inner shape a name. This Is often the thing that was missing.

## Ordering and duplicates in the output

Two small actions that surprise people at output time.

A `Set` has no order. So `model_dump_json` makes an array in what order the set iterates. That order is stable within a run but isn't the input order. It isn't sure across runs. If a client diffs your responses, or a test checks JSON strings, a set field will give spurious differences. Use a list and sort it if you need determinism.

A `Dict` preserves insertion order in modern Python. Dict fields do round-trip in a stable order. That is a language promise rather than a Pydantic one, but it's dependable.

## Choosing well, in practice

Most set bugs come from picking the holder for the wrong reason.

Choosing `Set` because "items should be unique" gives you silent deduplication when what you wanted was an error.

Choosing `Tuple` because "it shouldn't change" gives you spot-based access when what you wanted was a frozen model.

Choosing `List` when each read starts with a scan for a matching id means you wanted a `Dict` and are paying a linear search for it.

The question that resolves all three: what does the *consumer* of this field do with it? Iterate in order, look one up by key, or check membership? Each of those has an obvious holder. The answer is rarely about what the producer finds convenient to send.

## What the container says to a reader

A last thought that applies to each set you annotate.

The holder type is docs. `List[Lesson]` says these are sorted and repeats are real. `Set[str]` says order is irrelevant and copies aren't a thing. `Dict[str, Stats]` says you look these up by name. `Tuple[int, int]` says just two. The spots mean a thing fixed.

Someone reading the model learns all of that without opening a single function. Choosing the holder carelessly. Defaulting to `List` because it's the one that always works. Throws that away and leaves the reader to infer the rules from the code that consumes it. This Is just the situation models exist to prevent.

## Two failure modes to watch for

**given non-empty.** Code that reads `items[0]` will raise on a valid empty list. Either constrain the field with `min_length=1` so an empty set never reaches you, or handle the empty case by name. Silently given is how a rare payload turns an incident.

**given small.** A list annotation places no upper bound. A caller can send a million items and your process will try to validate all of them. For any public endpoint, `max_length` is a cheap denial-of-service guard and a documented limit, and it costs one arg.

Both are the same oversight: a holder's *size* is part of its contract. Leaving it unstated means the contract is what the caller decides.

## Next

sets handle many things of the same type. The next module is about the opposite problem. A field that could be one of a few *other* types. How to make that choice clear rather than letting Pydantic guess.

## Summary

holders validate their contents item by item. Each failure carries a path that names the exact spot. Index for a sequence, key for a mapping. Nothing is skipped because a thing earlier failed. One report covers the whole set.

Choose the holder for what the consumer does with it, not for what is convenient to build. Constrain the size. An unbounded set is an unstated contract. And when the payload is a bare array with no object around it, use `TypeAdapter` rather than inventing a wrapper model to hold it.
''',
    [
        {"q": "Item 1 of a 4-item list is invalid. What happens to items 2 and 3?",
         "options": ["They are skipped", "They are still validated and their failures reported too", "The whole list is rejected untested", "Only item 1 is reported"],
         "answer": 1,
         "why": "Validation covers the whole collection and reports every failure in one exception, which is what makes bulk imports fixable in a single pass."},
        {"q": "What does `Set[float]` do with `[1.0, 2.0, 1.0]`?",
         "options": ["Raises on the duplicate", "Gives a set of two items", "Gives three items", "Gives a list"],
         "answer": 1,
         "why": "Sets deduplicate silently. That is right for tags and wrong for measurements - if repeats are meaningful, use a list."},
        {"q": "You need to validate a bare JSON array of models. What is the right tool?",
         "options": ["A wrapper model with one list field", "TypeAdapter(List[Model])", "A loop calling model_validate", "It cannot be validated"],
         "answer": 1,
         "why": "`TypeAdapter` validates any annotation directly. The wrapper model is the workaround people reach for before discovering it."},
        {"q": "Why is `TypeAdapter(List[X]).validate_python(rows)` better than a list comprehension of `X.model_validate`?",
         "options": ["No difference", "It loops inside the compiled core rather than crossing into Python per item", "It skips validation", "It is only for JSON"],
         "answer": 1,
         "why": "One call into Rust validates the whole list. The comprehension does the same checks with one Python-to-Rust round trip per item."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Unions and discriminated unions
# ---------------------------------------------------------------------------
topic(
    "unions_and_discriminated_unions",
    "Unions and Discriminated Unions",
    "Real Data Shapes",
    "A field that could be one of several shapes - and how to stop Pydantic "
    "guessing which one you meant.",
    _svg(_box(12, 20, 44, 22, S) + _txt(34, 35, "Video", M, 8) +
         _box(12, 48, 44, 22, S) + _txt(34, 63, "Quiz", M, 8) +
         _arrow(60, 31, 84, 45) + _arrow(60, 59, 84, 45) +
         _box(88, 34, 56, 22, S, A) + _txt(116, 48, "kind: ?", A, 8)),
    [
        ("Smart mode: exact match first",
         "A union tries an exact type match before it tries converting. That resolves "
         "the obvious cases and leaves the ambiguous ones to order.",
         '''from typing import Union
from pydantic import BaseModel

class M(BaseModel):
    v: Union[int, str]

for value in [9, "nine", "9", 9.0, True]:
    got = M(v=value).v
    print("%-8r -> %-8r (%s)" % (value, got, type(got).__name__))

# 9 stays an int and "nine" stays a str because both match exactly.
# "9" is where it gets interesting: it matches str exactly, so str wins,
# even though int is written first.'''),

        ("Where order does change the answer",
         "When no member matches exactly, the union converts left to right. The same "
         "input can then produce different types depending on how you wrote it.",
         '''from typing import Union
from pydantic import BaseModel

class A(BaseModel):
    v: Union[int, float]

class B(BaseModel):
    v: Union[float, int]

for value in ["7"]:
    a, b = A(v=value).v, B(v=value).v
    print("int|float gives %-6r (%s)" % (a, type(a).__name__))
    print("float|int gives %-6r (%s)" % (b, type(b).__name__))

print()
print("Same input, two annotations, two types. If that distinction")
print("matters to your program, do not express it as a plain Union.")'''),

        ("Unions of models get ambiguous fast",
         "Two models with overlapping fields are a coin toss. Pydantic will pick the "
         "first that validates, which may not be the one the data meant.",
         '''from typing import Union
from pydantic import BaseModel

class Video(BaseModel):
    title: str
    seconds: int = 0

class Quiz(BaseModel):
    title: str
    questions: int = 0

class Item(BaseModel):
    content: Union[Video, Quiz]

# Unambiguous - only Quiz has 'questions':
print(Item(content={"title": "Vectors", "questions": 5}).content)

# Ambiguous - both models accept a bare title, and Video is written first:
guess = Item(content={"title": "Vectors"}).content
print(guess, "<- got", type(guess).__name__, "by position, not by meaning")'''),

        ("A discriminator makes it explicit",
         "Give each model a literal tag field and point <code>Field(discriminator=)</code> "
         "at it. Pydantic then reads the tag and goes straight to the right model.",
         '''from typing import Literal, Union
from pydantic import BaseModel, Field

class Video(BaseModel):
    kind: Literal["video"]
    title: str
    seconds: int

class Quiz(BaseModel):
    kind: Literal["quiz"]
    title: str
    questions: int

class Item(BaseModel):
    content: Union[Video, Quiz] = Field(discriminator="kind")

print(Item(content={"kind": "video", "title": "Vectors", "seconds": 240}).content)
print(Item(content={"kind": "quiz", "title": "Check", "questions": 4}).content)

# No guessing left: the tag decides.'''),

        ("Better errors, too",
         "Without a discriminator a failure reports every branch it tried. With one, "
         "it reports the single branch that was actually meant.",
         '''from typing import Literal, Union
from pydantic import BaseModel, Field, ValidationError

class Video(BaseModel):
    kind: Literal["video"]
    seconds: int

class Quiz(BaseModel):
    kind: Literal["quiz"]
    questions: int

class Plain(BaseModel):
    content: Union[Video, Quiz]

class Tagged(BaseModel):
    content: Union[Video, Quiz] = Field(discriminator="kind")

bad = {"content": {"kind": "video", "seconds": "lots"}}

try:
    Plain.model_validate(bad)
except ValidationError as e:
    print("without discriminator:", e.error_count(), "errors")
    for err in e.errors():
        print("   ", err["loc"], err["type"])

try:
    Tagged.model_validate(bad)
except ValidationError as e:
    print()
    print("with discriminator   :", e.error_count(), "error")
    for err in e.errors():
        print("   ", err["loc"], err["type"])'''),

        ("An unknown tag fails cleanly",
         "The discriminator itself is validated. A tag nobody declared produces one "
         "clear error naming the values that are allowed.",
         '''from typing import Literal, Union, List
from pydantic import BaseModel, Field, ValidationError

class Video(BaseModel):
    kind: Literal["video"]
    seconds: int

class Quiz(BaseModel):
    kind: Literal["quiz"]
    questions: int

class Track(BaseModel):
    items: List[Union[Video, Quiz]] = Field(discriminator="kind")

t = Track(items=[{"kind": "video", "seconds": 240},
                 {"kind": "quiz", "questions": 4}])
for item in t.items:
    print(type(item).__name__, "->", item.model_dump())

try:
    Track(items=[{"kind": "podcast", "seconds": 10}])
except ValidationError as e:
    err = e.errors()[0]
    print()
    print("type :", err["type"])
    print("said :", err["msg"])'''),
    ],
    [
        "Smart mode tries an exact type match across all members first, and only then attempts conversion left to right.",
        "Where no member matches exactly, the order you wrote members in decides the result. That is a fragile thing to depend on.",
        "A union of models is ambiguous whenever more than one of them can accept the same payload &mdash; which is common once fields have defaults.",
        "<code>Field(discriminator=\"kind\")</code> with a <code>Literal</code> tag on each model removes the guessing entirely.",
        "Discriminated unions produce one error from the right branch instead of a pile of errors from every branch that was tried.",
        "Discriminated unions are also faster: one lookup on the tag instead of attempting each member in turn.",
    ],
    '''
title: Unions and Discriminated Unions: Stop Pydantic Guessing
intro: A field that could be a few shapes. How to make the choice clear.

## The problem a union creates

Sometimes a field can hold more than one kind of value. A payment could be a card or a bank transfer. A message could be text or an image. In Python typing you write that as a union, and Pydantic has to decide which member of the union the data belongs to.

That decision is harder than it sounds. Pydantic tries the members and picks the best match, but when two members look alike, it can choose the wrong one without telling you. With unions of plain types the result is usually fine. With unions of models it can go badly, and the error messages get long and confusing.

This article starts with the problem a union creates. It explains how smart mode picks a member, and the places where order still decides the outcome. It then shows why unions of models are worse, and what the error looks like when every member fails. The fix is a tag. A discriminated union uses one field, such as a type name, to say which model applies, so Pydantic no longer guesses. The result is faster, clearer, and far easier to debug.

You will meet unions sooner than you expect. Any API that accepts more than one kind of thing needs one. Events, payments, notifications and search results all fall into that group. The trouble is that a union that works in a quick test can misbehave on real traffic. The wrong member wins, or the error report becomes a wall of text that hides the real problem. This article shows you both of those failures before it shows the cure, so you can recognise them in your own code. The cure is small, and once you have used it you will reach for it by default. It also makes the generated documentation much clearer for anyone who calls your API.

Once you see the failure, the fix will feel obvious and easy to remember.

`Union[A, B]` says a value may be either. What it doesn't say is how to decide which, and a thing has to decide.

For simple types the choice is often obvious and often right. For models it's often neither. The failure mode is the worst kind. It doesn't raise, it just gives you the wrong object.

## Smart mode, and what it actually does

Pydantic v2 doesn't simply try members left to right. It uses **smart mode**. This Is a two-pass plan.

First it looks for a member the value already matches just, without any conversion. An `int` input against `Union[int, str]` matches `int`. A `str` input matches `str`. No ambiguity, no order dependence.

Only if nothing matches just does it try conversion, left to right, taking the first that succeeds.

This resolves most everyday unions sensibly. It's a genuine gain over v1. This Was strictly left-to-right and would happily turn an int into a string because `str` was written first.

But it doesn't drop ambiguity. It relocates it to the cases where nothing matches just. Which, for data arriving from JSON as strings, is a lot of cases.

## Where order still decides

`Union[int, float]` given the string `"7"` makes an `int`. `Union[float, int]` given the same string makes a `float`. Neither member matched just. Conversion ran left to right and the first success won.

If the gap matters to your program. And the gap between `7` and `7.0` matters in more places than people expect, from JSON output to dict keys to equality checks. Then you've a action that depends on the order somebody wrote two words in. That will live just until somebody reorders them for tidiness.

The lesson isn't to store the rules. It's that a plain union of convertible types is an unstable way to express a real gap.

## Unions of models are worse

With models the ambiguity is structural.

```python
class Video(BaseModel):
    title: str
    seconds: int = 0

class Quiz(BaseModel):
    title: str
    questions: int = 0
```

Both accept `{"title": "Vectors"}`, because the other field has a default in each. Neither matches "just" in any real sense. The first that validates wins. And that is `Video`, purely because of where it appears in the annotation.

The result is a `Video` that was meant to be a `Quiz`, made without any error. Found one spot much later when `questions` is missing.

Defaults make this sharply more likely. This Is worth noticing. Adding a default to a field of one union member can change how *other* payloads are classified.

## The fix is a tag

A discriminated union asks the data to say which shape it's. Each member gets a `Literal` field with a distinct value, and the union names it:

```python
class Video(BaseModel):
    kind: Literal["video"]
    title: str
    seconds: int

class Quiz(BaseModel):
    kind: Literal["quiz"]
    title: str
    questions: int

content: Union[Video, Quiz] = Field(discriminator="kind")
```

Now there's no guessing. Pydantic reads `kind`, looks up the matching model. Validates against that one only.

This is the same pattern as a tagged union in other languages. The same one you see in real API payloads all over. Stripe events, webhook bodies, message envelopes. If your data already has a `type` or `kind` field, it's already discriminated and you're just telling Pydantic about it.

## Three things you get

**Correctness.** The tag decides, so the answer doesn't depend on annotation order, on which fields happen to have defaults, or on which member was added first.

**Better errors.** Without a critic, a failure means Pydantic tried each member and none worked. You get the errors from all of them. A pile of messages about branches you were never in. With a critic, it tried just one. Reports just that one's problem.

That gap is stark on a union with five members. It turns "here are fifteen errors, work out which three are yours" into "seconds should be a valid int".

**Speed.** One dict lookup on the tag, rather than attempting check against each member until a thing sticks.

## When the tag is wrong

The critic field is checked too. A value that matches no member makes a single `union_tag_invalid` error listing the permitted tags. This Is an great error. It tells the caller both what was wrong and what the options are.

A payload missing the tag fully gives `union_tag_not_found`. Again, one clear error rather than a scatter.

## Practical shapes

Discriminated unions compose. A `List[Union[Video, Quiz]]` with a critic validates each item by its own tag. This Is just what a feed of mixed content needs. Errors still carry the index.

The tag field is a real field. It appears in `model_dump()`, it's needed. It must be a `Literal`. A plain `str` won't do. The whole method depends on the value being known at class-meaning time.

For a union that grows over time, `Union` of many members is unwieldy to write. `Annotated` helps:

```python
Content = Annotated[Union[Video, Quiz, Article], Field(discriminator="kind")]
```

Now `Content` is a named type you can use anywhere. Adding a fourth member is one edit in one place.

## Optional is a union too

Worth noticing, because it clarifies a thing people treat as special: `Optional[X]` is just `Union[X, None]`. All above applies to it.

It happens to be the least ambiguous union possible. `None` is only ever itself and nothing converts to it. That is why `Optional` never causes the problems this module shows. Why it's safe to reach for without thinking.

## What to reach for

Use a plain union for truly simple cases where each member is a distinct, non-convertible type. `Union[int, None]`, or a union of models with obviously disjoint needed fields.

Use a discriminated union for anything polymorphic: content types, event types, message kinds, shape variants. If you're modelling "one of these things", this is the tool.

Consider whether you want a union at all. at times the honest model is one type with optional fields. At times two split endpoints. A union in an API is a thing each client has to branch on. The tag makes that branching possible. But fewer branches is still better than more.

## Left-to-right, when you actually want it

Smart mode is the default, and there's a second mode for the cases where you want the older action:

```python
value: Union[int, str] = Field(union_mode="left_to_right")
```

Now members are tried strictly in order and the first success wins, with no exact-match pass first. That is at times what you want. A deliberate preference order. Here You'd rather have an `int` if the value can possibly be one.

It's worth knowing this exists mainly so that you recognise the action when reading v1 code. This Worked this way always. A union in an old code may be leaning on order in a way that quietly changed meaning during the v2 migration.

## The performance argument

There's a cost to a plain union that is easy to overlook.

checking against `Union[A, B, C, D]` may mean attempting up to four validations, each of which builds errors before failing. For a list of a thousand items, a union whose correct member is often last is doing four times the needed work and discarding three quarters of it.

A discriminated union does one dict lookup and one check. For large sets of polymorphic data. An event log, a feed, a batch of webhook payloads. That gap is measurable rather than theoretical.

So the tag isn't only about correctness and error quality. It's also the fast path.

## Nullable unions and the shape of Optional

`Optional[X]` is `Union[X, None]`, and it's the one union that never causes ambiguity. Nothing converts to `None` and `None` converts to nothing.

That is worth stating because it shows why `Optional` feels other from other unions though it isn't special. It isn't that Pydantic treats it differently. It's that its members can't share.

A related shape that does need care: `Optional[Union[A, B]]`, or equivalently `Union[A, B, None]`. The `None` part is unambiguous. The `A` versus `B` part has all the problems given above. Adding a critic still works. `None` is handled apart from the tagged members. So a nullable discriminated union is a just right good thing to write.

## Migrating a plain union to a tagged one

If you've an existing union that is misbehaving, the change is often additive rather than breaking.

Add a `kind` field with a `Literal` to each member and give it a default matching that member's tag:

```python
class Video(BaseModel):
    kind: Literal["video"] = "video"
```

Existing code that makes `Video(...)` without a tag keeps working. The default fills it in. Existing *data* without the tag will now fail check. This Is the part to plan for. Either a migration that adds the field, or a `model_validator(mode="before")` that infers the tag from the shape for a transition period.

The inference checker is a handy trick and a temporary one. It looks at which fields are present, decides what the payload must be. Writes the tag in. Keep it until the old data is gone, then delete it. It's just the guessing that the critic was added to drop.

## Unions in the schema

A plain union turns `anyOf` in JSON Schema. A list of options with nothing to say how a consumer should choose between them. A made client will often give a type that could be any of them and leave the disambiguation to whoever calls it.

A discriminated union turns `oneOf` with a `critic` object naming the property and mapping its values to schemas. Tooling understands this. Made clients give a proper tagged type, docs groups the variants and shows which tag selects which. Checkers on the other side can check the same rule you check.

If your API is consumed by made clients, this alone is a strong reason to tag each polymorphic field. The gap between the two client types. One you've to narrow by inspection, one that narrows itself. Is felt by each consumer on each call.

## A checklist

If the members are a fixed set of *kinds* of thing, tag them.

If the data already has a `type`, `kind` or `event` field, you've a tag. Tell Pydantic about it.

If the members are simple, disjoint scalar types, a plain union is fine.

If you're leaning on the order you wrote the members in, stop and add a tag. That dependency is invisible to the next reader.

And if you can't find a natural tag, consider whether the union is really modelling one thing with optional parts. This Is often what a hard-to-tag union turns out to be.

## What the tag is really doing

A discriminated union works because it moves a choice from inference to declaration.

Without a tag, a thing has to work out what a payload is by looking at what it holds. That is guessing. Carefully built. Guessing has a failure mode where it's confidently wrong. With a tag, the payload states what it's and check checks that claim against one schema.

That is a pattern well beyond Pydantic. Any time a system decides what a thing is by checking its shape, adding an clear marker makes the system simpler, faster and more honest about its failures. The critic is the version of that idea you get for one line of annotation.

## Before you reach for a union

One question worth asking first: is this really a few shapes, or one shape whose fields vary?

A union of two models that share nine of their ten fields is often the second thing wearing the costume of the first. One model with an optional field is simpler to write, simpler to consume and simpler to doc.

Reach for a union when the options are truly other. Other needed fields, other meaning, other handling downstream. When they're the same thing with a variation, model the variation.

## Next

Unions choose between shapes. The next module is about choosing between *values*. Enums and literals. This Are how you say a field may only ever hold one of a small fixed set.
''',
    [
        {"q": "In smart mode, what does Pydantic try first for a union?",
         "options": ["Left to right conversion", "An exact type match across all members", "The narrowest type", "Random order"],
         "answer": 1,
         "why": "An exact match wins without any conversion. Only when nothing matches exactly does it fall back to converting left to right, which is where order starts to matter."},
        {"q": "Two models in a union can both accept `{\"title\": \"x\"}`. What happens?",
         "options": ["A ValidationError", "The first one that validates wins, by position", "Both are returned", "The one with more fields wins"],
         "answer": 1,
         "why": "This is the dangerous case: no error, just the wrong object. Defaults make it much more likely, since they let a member accept payloads it was never meant for."},
        {"q": "What does `Field(discriminator=\"kind\")` require of each member?",
         "options": ["A str field named kind", "A Literal field named kind with a distinct value", "Nothing", "An Enum"],
         "answer": 1,
         "why": "The value must be known at class-definition time so Pydantic can build the tag-to-model lookup, which is what `Literal` provides and a plain `str` does not."},
        {"q": "Why do discriminated unions produce better errors?",
         "options": ["They have shorter messages", "Only one branch is attempted, so only its errors are reported", "They suppress errors", "They validate less"],
         "answer": 1,
         "why": "Without a tag, every member is tried and every member's failures are reported. With one, exactly one branch runs, so the report is about the shape the data actually claimed to be."},
    ],
)


# ---------------------------------------------------------------------------
# 11. Enums and literals
# ---------------------------------------------------------------------------
topic(
    "enums_and_literals",
    "Enums and Literals",
    "Real Data Shapes",
    "Closed sets of values, the two ways to spell them, and why a Literal usually "
    "beats a regular expression.",
    _svg(_box(20, 26, 120, 38, S) +
         _txt(50, 42, "maths", A, 8) + _txt(110, 42, "python", A, 8) +
         _txt(50, 56, "dsa", A, 8) + _txt(110, 56, "ml", A, 8)),
    [
        ("Literal is the smallest way to say it",
         "A <code>Literal</code> lists the permitted values inline. Anything else is "
         "refused, and the error names the options.",
         '''from typing import Literal
from pydantic import BaseModel, ValidationError

class Module(BaseModel):
    title: str
    track: Literal["maths", "python", "dsa", "ml"]

print(Module(title="Vectors", track="maths"))

try:
    Module(title="Vectors", track="astrology")
except ValidationError as e:
    err = e.errors()[0]
    print()
    print("type :", err["type"])
    print("said :", err["msg"])
    print("got  :", repr(err["input"]))'''),

        ("Why not a regular expression",
         "A pattern can express the same rule and tells you far less. Compare the two "
         "errors, and remember which one a client can render as a dropdown.",
         '''from typing import Literal
from pydantic import BaseModel, Field, ValidationError

class WithPattern(BaseModel):
    track: str = Field(pattern=r"^(maths|python|dsa|ml)$")

class WithLiteral(BaseModel):
    track: Literal["maths", "python", "dsa", "ml"]

for cls in (WithPattern, WithLiteral):
    try:
        cls(track="astrology")
    except ValidationError as e:
        print("%-12s %s" % (cls.__name__, e.errors()[0]["msg"]))

print()
print("in the schema:")
print("  pattern:", WithPattern.model_json_schema()["properties"]["track"])
print("  literal:", WithLiteral.model_json_schema()["properties"]["track"])'''),

        ("Enum when the values need behaviour",
         "An <code>Enum</code> gives the set a name, a home for methods, and members "
         "you can refer to in code rather than retyping the strings.",
         '''from enum import Enum
from pydantic import BaseModel

class Track(str, Enum):
    MATHS = "maths"
    PYTHON = "python"
    DSA = "dsa"

    @property
    def label(self) -> str:
        return {"maths": "Maths for ML",
                "python": "Python",
                "dsa": "Algorithms"}[self.value]

class Module(BaseModel):
    title: str
    track: Track

m = Module(title="Vectors", track="maths")     # the string is accepted
print("field   :", m.track)
print("is enum :", isinstance(m.track, Track))
print("value   :", m.track.value)
print("label   :", m.track.label)
print()
print("by member:", Module(title="Norms", track=Track.DSA).track.label)'''),

        ("str, Enum - and why the mixin matters",
         "Inheriting from <code>str</code> makes members behave like strings "
         "everywhere else in your program, and keeps the JSON output plain.",
         '''from enum import Enum
from pydantic import BaseModel

class Plain(Enum):
    MATHS = "maths"

class Strish(str, Enum):
    MATHS = "maths"

class A(BaseModel):
    t: Plain

class B(BaseModel):
    t: Strish

a, b = A(t="maths"), B(t="maths")

print("plain  ==   'maths' :", a.t == "maths")
print("str,Enum == 'maths' :", b.t == "maths")
print()
print("plain  json :", a.model_dump_json())
print("str    json :", b.model_dump_json())
print()
print("dump mode=python:", b.model_dump()["t"], type(b.model_dump()["t"]).__name__)
print("dump mode=json  :", b.model_dump(mode="json")["t"])'''),

        ("Literals in a discriminated union",
         "This is where <code>Literal</code> stops being a convenience and becomes "
         "load-bearing: it is the tag a discriminated union reads.",
         '''from typing import Literal, Union, List
from pydantic import BaseModel, Field

class Video(BaseModel):
    kind: Literal["video"]
    seconds: int

class Quiz(BaseModel):
    kind: Literal["quiz"]
    questions: int

class Track(BaseModel):
    items: List[Union[Video, Quiz]] = Field(discriminator="kind")

t = Track(items=[{"kind": "video", "seconds": 240},
                 {"kind": "quiz", "questions": 4}])

for item in t.items:
    print("%-6s %s" % (type(item).__name__, item.model_dump()))

print()
print("the tag is a real field:", t.items[0].kind)'''),

        ("Literals are not only strings",
         "Any hashable literal works &mdash; numbers, booleans, <code>None</code> "
         "&mdash; and they combine, which is useful for versioned payloads.",
         '''from typing import Literal, Optional
from pydantic import BaseModel, ValidationError

class Payload(BaseModel):
    version: Literal[1, 2]
    mode: Literal["fast", "exact"] = "fast"
    debug: Literal[True, False, None] = None

print(Payload(version=2))                   # the literal value itself
print(Payload(version=1, mode="exact", debug=True))

for bad in [3, "2"]:                        # note: "2" is NOT coerced
    try:
        Payload(version=bad)
    except ValidationError as e:
        print("version=%-4r %s" % (bad, e.errors()[0]["msg"]))

# A Literal matches the value as given. Unlike an int field, it does not
# parse "2" into 2 first - the literal members are compared directly.'''),
    ],
    [
        "<code>Literal[\"a\", \"b\"]</code> is the shortest way to declare a closed set, and the error it produces names every allowed value.",
        "A <code>Literal</code> becomes an <code>enum</code> in JSON Schema, so API docs and generated clients can render it as a choice. A <code>pattern</code> cannot.",
        "Use an <code>Enum</code> when the set deserves a name, needs methods, or is referenced from code in several places.",
        "Inherit from <code>str</code> as well as <code>Enum</code> so members compare equal to their strings and serialise as plain text.",
        "<code>model_dump()</code> keeps enum members; <code>model_dump(mode=\"json\")</code> and <code>model_dump_json()</code> convert them to their values.",
        "<code>Literal</code> is what a discriminated union reads as its tag, which is the one place it cannot be replaced by anything else.",
    ],
    '''
title: Enums and Literals: Closed Sets Done Properly
intro: Two ways to say a field may only hold one of a fixed list, and when each is right.

## The rule a type cannot express

Many fields should accept only a small, fixed set of values. A status can be draft, published or archived. A level can be beginner, intermediate or advanced. A plain string type cannot express that, because any string would pass. You need a type that names the allowed values.

Python gives you two ways to do it. A Literal lists the exact values inline, right in the annotation. An Enum defines a named class with members, which suits values you use in many places. Pydantic validates both, rejects anything outside the set, and puts the allowed values into the error message and the JSON Schema.

This article explains the rule a plain type cannot express and why a regular expression is the wrong tool for it. It covers Literal first, since it is the lighter option. Then it moves to Enum, including how Pydantic converts between a raw value and a member. You will see why the str mixin matters for JSON, and why leaving it out causes trouble. The final section helps you choose between the two, and covers what happens when new values appear in the data later.

Most applications are full of closed sets. Roles, states, categories and plan names all qualify. Getting them wrong does not usually crash anything. It lets a typo travel deep into your system, where it turns up as a strange bug days later. A closed type stops that at the door. The article shows both options side by side, so you can see what each one costs and what each one gives back. It also covers how the choice affects the JSON your API sends, which is where many people first notice a problem. Take a few minutes to learn which one fits which job, and you will make the choice quickly every time after.

Both choices are quick to learn and easy to apply.

`track: str` allows each string ever written. Your use allows four. That gap is where invalid data lives. Closing it's one of the highest-value constraints on hand. A misspelt group is a bug that lives for months because nothing rejects it.

There are two good ways to close it, and one common bad one.

## Literal

```python
track: Literal["maths", "python", "dsa", "ml"]
```

The permitted values are written where the type goes. Anything else raises, with an error that lists the options.

It's the smallest thing that works, it needs no imports beyond `typing`. Mypy understands it. So your own code gets checked against the same set. A compare against `"mathematics"` is flagged by your editor before it ever runs.

## Why not a regular expression

`Field(pattern=r"^(maths|python|dsa|ml)$")` enforces the same rule. It's worse in four distinct ways. They're worth listing because the pattern approach is common.

**The error.** A `Literal` says the input should be one of a list. Gives the list. A pattern says the string should match a regular formula. Prints the formula. One of those is usable by a person who didn't write your code.

**The schema.** A `Literal` turns `enum` in JSON Schema. docs renders it as a set of choices, a made client offers a type with four options, a form builder makes a dropdown. A `pattern` turns a `pattern`, and each tool downstream shrugs.

**Static checking.** Mypy knows the four values of a `Literal` and will tell you when a compare can never be true. It has no idea what a regular formula permits.

**Maintenance.** Adding a fifth track means editing a regular formula. This Is a place people make mistakes, versus adding a word to a list.

The only case for a pattern is a set that is truly open. A format rather than a list. Slugs, postcodes, identifiers. If you can enumerate the values, enumerate them.

## Enum

An `Enum` gives the set an identity:

```python
class Track(str, Enum):
    MATHS = "maths"
    PYTHON = "python"
    DSA = "dsa"
```

Three things follow that a `Literal` doesn't give you.

**A name to refer to.** `Track.MATHS` instead of `"maths"` in the code that consumes the model. That means a typo is an `AttributeError` at import rather than a compare that quietly returns `False`.

**One meaning.** The set exists once and is used by each model that needs it. A `Literal` written out in four models is four copies. Though `Annotated` fixes that. A named `Track = Literal[...]` alias is a just right good middle ground.

**one spot to put action.** A display label, a colour, an sorting, a `from_legacy_name` classmethod. Enums can have methods and properties. That is often just where that logic belongs.

## The str mixin is not optional

Write `class Track(str, Enum)`, not `class Track(Enum)`, unless you've a exact reason.

Without the mixin, members aren't strings. `Track.MATHS == "maths"` is `False`. This Breaks each compare in code that doesn't know about the enum. `json.dumps` refuses them. String formatting makes `Track.MATHS` rather than `maths`.

With the mixin, members *are* strings with extra structure. each compare works, output is plain text. Code that was written before the enum existed keeps working.

Python 3.11 added `StrEnum`. This Is the same idea with a cleaner spelling. Either is fine. The plain `Enum` is the one to avoid.

## What comes out when you dump

This trips people up, so it's worth being clear.

`model_dump()` returns Python objects, so an enum field comes back as the enum member. That is often what you want inside your program.

`model_dump(mode="json")` and `model_dump_json()` convert members to their values. JSON has no enums. So the wire format is the plain string either way.

With the `str` mixin the gap rarely bites. The member behaves like its value anyway. Without it, a member reaching `json.dumps` raises. That is the shape of the bug.

## Literals do more than strings

Any hashable literal works: `Literal[1, 2]`, `Literal[True]`, `Literal[None]`, and mixtures.

`Literal[1, 2]` for a version field is a truly good pattern. It makes a payload's supported versions clear and rejects an unsupported one at the boundary with a clear message, rather than one spot deep in code written for version 1.

One thing to know, because it differs from a plain `int` field. A `Literal` checks the value as given rather than parsing it first. `Literal[1, 2]` given the string `"2"` raises `literal_error`. Here `minutes: int` would happily have converted it. If a version number arrives from a query string as text, annotate it `int` and constrain it, or convert before checking.

## The one place Literal is required

A discriminated union reads its tag from a `Literal` field. Nothing else will do. Not a `str` with a default, not an `Enum` member as a default. Because the method needs the value known at class-meaning time to build the lookup table.

So if you're writing polymorphic models, `Literal` isn't a stylistic choice. It's the method.

## Choosing

Reach for **`Literal`** when the set is small, local. Doesn't need action. A status field used by one model, a critic tag, a version number.

Reach for **`Enum`** when the set is part of your domain vocab, is used in a few places, or wants methods. Anything you'd find yourself writing a constants module for.

Reach for a **named `Literal` alias**. `Track = Literal["maths", "python"]`. When you want reuse without the ceremony of a class. It's underused and it's often just right.

And avoid a bare `str` with a comment listing the allowed values. That comment is a schema that nothing enforces. It will be wrong within a year.

## Migration, briefly

One hands-on warning. Adding a value to a `Literal` or `Enum` is safe. Dropping one is a breaking change for anyone who has stored the old value. Check will start rejecting data that was before fine. Including rows already in your DB.

The usual fix is to keep the old value accepted, mapped to a thing sensible in a checker, for if old data exists. It's worth thinking about before you tighten a set that has been open for a while.

## Named literal aliases

There's a middle option between an inline `Literal` and a full `Enum` that deserves more use than it gets:

```python
Track = Literal["maths", "python", "dsa", "ml"]

class Module(BaseModel):
    track: Track

class Lesson(BaseModel):
    track: Track
```

One meaning, reused, with no class to write and no `.value` to note. Mypy narrows it in your own code. The schema still gets a proper enumeration.

It's the right answer oddly often. The reason to reach past it for a real `Enum` is action. A label, an sorting, a lookup. Or the ergonomics of `Track.MATHS` over the bare string. If you need neither, the alias is less machinery for the same result.

## Enums in the schema

Both spellings give an `enum` in JSON Schema. But They differ in one handy way.

A `Literal` inlines the values into the field. An `Enum` makes a named meaning in `$defs` that the field links. A set used by six fields appears once and is referenced six times.

That matters for made clients. A referenced meaning often turns a named type in the target language. A TypeScript union alias, a Java enum. Which is reusable on the consumer's side too. Inlined values become six anonymous unions that happen to have the same members.

So for a set that appears in more than a couple of places in a public API, an `Enum` gives your consumers a better artefact, not just you.

## Defaults and the two spellings

A small ergonomic gap worth knowing.

With a `Literal`, the default is the value: `track: Track = "maths"`.

With an `Enum`, the default is most times the member: `track: Track = Track.MATHS`. The string also works. Check coerces it. The member reads better and is checked by your editor.

One caution with enum defaults: `= Track.MATHS` is checked once at class-meaning time. This Is fine because enum members are singletons and immutable. This is one of the few mutable-looking defaults that is truly safe.

## Extending a set safely

Adding a value is backwards matching for the producer and not always for the consumer.

Your model will accept the new value at once. each client that has made a type from your schema won't, until they regenerate. And a strict client may reject a response holding a tag it has never heard of.

This is a real API design consideration rather than a Pydantic one. The usual mitigations are. Version the endpoint, doc that the set is open to extension so clients build tolerant parsers, or add the new value behind a flag until consumers have caught up.

Dropping a value is worse and worth stating plainly. It will start rejecting data you've already stored. If a `track` column holds `"legacy"` and you drop it from the enum, each read of those rows now raises. The safe path is to keep accepting the old value, map it in a checker. Only drop it once the data is gone.

## Where an enum is the wrong shape

Two cases where reaching for an enum causes more trouble than it blocks.

**A set that truly changes at runtime.** groups a user can create, tags from a DB, anything editable through an admin interface. An enum is fixed at import. A set that changes needs a checker that checks against the current list. That check belongs in the layer that can see the list.

**A set with hundreds of members.** Country codes, currency codes, timezone names. Strictly an enum works. In practice the schema turns huge, the made client turns huge. The error message lists three hundred options. A pattern plus a lookup is kinder to everybody.

The rule of thumb: enumerate when the set is small, stable and part of your domain's vocab. else validate membership another way.

## Summary

`Literal` for small, local sets and for critic tags. A named `Literal` alias when the same small set is used in a few places. `Enum` when the set is domain vocab, needs action, or appears across a public API where consumers gain from a named type. `str, Enum` always, never a bare `Enum`. And never a bare `str` with a comment.

## The underlying point

A closed set is one of the few pieces of domain knowledge that a type system can hold fully.

Most rules are guesses &mdash; a length bound, a range, a pattern that permits things you'd reject. "This field is one of these four values" is exact. There's nothing left over, no edge case, no judgement call. Writing it down as a `Literal` or an `Enum` captures the entire truth about that field.

That is why it's worth the small effort of not writing `str`. You get an exact error, a schema a client can render, a static check on your own checks. A meaning that can't drift from the code that uses it. All from choosing a more exact annotation than the one that would have worked.

## A last practical note

When you add an enum to an existing field, run your data through it before you deploy.

A `str` field that has been accepting anything for a year almost certainly holds values no one expected. A trailing space, a other case, an old name from before a rename, a placeholder somebody typed once. each one of those will start raising the moment the annotation tightens.

Finding them beforehand is a short script and an afternoon. Finding them later is an incident. The failures arrive on reads of existing data rather than on new input. This Is the direction no one tests.

## Next

The next module covers the types Pydantic already knows how to parse for you. Dates, times, UUIDs and decimals. And the traps in each, above all the two that cost money: floats and timezones.
''',
    [
        {"q": "Why prefer `Literal[\"a\", \"b\"]` over `Field(pattern=r\"^(a|b)$\")`?",
         "options": ["It is faster", "Better error, appears as an enum in the schema, and mypy understands it", "Patterns do not work", "No real difference"],
         "answer": 1,
         "why": "The Literal error lists the allowed values, the schema becomes a renderable choice for clients and docs, and static checkers can verify your own comparisons against it."},
        {"q": "Why write `class Track(str, Enum)` rather than `class Track(Enum)`?",
         "options": ["It is required by Pydantic", "So members compare equal to their strings and serialise as plain text", "It is faster", "To allow methods"],
         "answer": 1,
         "why": "Without the mixin, `Track.MATHS == \"maths\"` is False and json.dumps refuses the member, which breaks any code that does not know the enum exists."},
        {"q": "What does `model_dump()` return for an enum field, versus `model_dump_json()`?",
         "options": ["Both give the value", "The member, and the value respectively", "Both give the member", "It raises"],
         "answer": 1,
         "why": "`model_dump()` keeps Python objects, so you get the member. JSON has no enums, so the JSON forms convert to the underlying value."},
        {"q": "Where is `Literal` not just a preference but the required mechanism?",
         "options": ["Any string field", "As the tag of a discriminated union", "Optional fields", "Nested models"],
         "answer": 1,
         "why": "The discriminator lookup is built at class-definition time, so the tag value must be known then - which is what Literal provides and a plain str does not."},
    ],
)


# ---------------------------------------------------------------------------
# 12. Dates, UUIDs and decimals
# ---------------------------------------------------------------------------
topic(
    "dates_uuids_and_decimals",
    "Dates, UUIDs and Decimals",
    "Real Data Shapes",
    "The standard-library types Pydantic already parses - and the two traps that "
    "cost real money: floats and naive datetimes.",
    _svg(_txt(34, 30, '"2026-08-26"', M, 8) + _arrow(72, 26, 92, 26) + _txt(120, 30, "date", A, 8) +
         _txt(34, 52, '"12.10"', M, 8) + _arrow(72, 48, 92, 48) + _txt(120, 52, "Decimal", A, 8) +
         _txt(34, 74, "1774526400", M, 8) + _arrow(72, 70, 92, 70) + _txt(120, 74, "datetime", A, 8)),
    [
        ("Dates and times from strings",
         "ISO 8601 text and Unix timestamps both work. This is what makes a model "
         "usable directly against JSON, which has no date type at all.",
         '''from datetime import date, datetime, time, timedelta
from pydantic import BaseModel

class Module(BaseModel):
    published_on: date
    updated_at: datetime
    slot: time
    length: timedelta

m = Module(published_on="2026-08-26",
           updated_at="2026-08-26T14:30:00",
           slot="14:30",
           length=900)                    # seconds

print("date     :", m.published_on, type(m.published_on).__name__)
print("datetime :", m.updated_at)
print("time     :", m.slot)
print("duration :", m.length, "->", m.length.total_seconds(), "seconds")
print()
print("a unix timestamp works too:")
print("  ", Module(published_on=1787702400,     # exactly midnight UTC
                   updated_at=1787836800,
                   slot="09:00", length="PT1H30M").updated_at)'''),

        ("The timezone trap",
         "A naive datetime and an aware one cannot be compared. If your system is "
         "timezone-aware, say so in the type and let bad input be rejected.",
         '''from datetime import datetime, timezone
from pydantic import BaseModel, AwareDatetime, NaiveDatetime, ValidationError

class Loose(BaseModel):
    at: datetime

class Aware(BaseModel):
    at: AwareDatetime

naive = Loose(at="2026-08-26T14:30:00").at
aware = Loose(at="2026-08-26T14:30:00+00:00").at

print("naive :", naive, "| tzinfo:", naive.tzinfo)
print("aware :", aware, "| tzinfo:", aware.tzinfo)

try:
    print(naive < aware)
except TypeError as e:
    print()
    print("comparing them:", e)

try:
    Aware(at="2026-08-26T14:30:00")
except ValidationError as e:
    print()
    print("AwareDatetime rejects naive input:", e.errors()[0]["msg"])'''),

        ("Money is not a float",
         "Binary floating point cannot represent most decimal fractions. "
         "<code>Decimal</code> can &mdash; but only if you keep the value as text on "
         "the way in.",
         '''from decimal import Decimal
from pydantic import BaseModel

print("plain python:")
print("  0.1 + 0.2      =", 0.1 + 0.2)
print("  == 0.3         ?", 0.1 + 0.2 == 0.3)
print()

class FromFloat(BaseModel):
    price: Decimal

class Money(BaseModel):
    price: Decimal

a = FromFloat(price=0.1)          # the float was already inexact
b = Money(price="0.1")            # the text is exact

print("Decimal from float :", a.price)
print("Decimal from str   :", b.price)
print()
print("three of each      :", a.price * 3, "|", b.price * 3)
print()
print("This is why prices travel as strings in JSON.")'''),

        ("Constraining a decimal properly",
         "<code>max_digits</code> and <code>decimal_places</code> say what a currency "
         "amount actually is, and no amount of <code>float</code> will give you them.",
         '''from decimal import Decimal
from pydantic import BaseModel, Field, ValidationError

class Price(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=8, decimal_places=2)

print(Price(amount="12.50"))
print(Price(amount="99999.99"))

for bad in ["12.505", "0", "123456789.00"]:
    try:
        Price(amount=bad)
    except ValidationError as e:
        print("%-14s %-20s %s" % (bad, e.errors()[0]["type"], e.errors()[0]["msg"]))'''),

        ("UUIDs and paths",
         "Both accept their string form, which is the only form JSON has. A UUID "
         "field also rejects a string that is not one.",
         '''from uuid import UUID, uuid4
from pathlib import Path
from pydantic import BaseModel, ValidationError

class Asset(BaseModel):
    id: UUID
    location: Path

a = Asset(id="123e4567-e89b-12d3-a456-426614174000",
          location="assets/og/maths.png")

print("id       :", a.id, "->", type(a.id).__name__)
print("version  :", a.id.version)
print("path     :", a.location, "->", type(a.location).__name__)
print("suffix   :", a.location.suffix)
print("parent   :", a.location.parent)

try:
    Asset(id="not-a-uuid", location="x")
except ValidationError as e:
    print()
    print("bad uuid :", e.errors()[0]["msg"])'''),

        ("What comes out the other side",
         "None of these types exist in JSON, so serialising converts them. "
         "<code>model_dump()</code> keeps the objects; the JSON forms make text.",
         '''from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel

class Module(BaseModel):
    id: UUID
    published_on: date
    updated_at: datetime
    price: Decimal

m = Module(id="123e4567-e89b-12d3-a456-426614174000",
           published_on="2026-08-26",
           updated_at="2026-08-26T14:30:00+00:00",
           price="12.50")

py = m.model_dump()
print("mode=python:")
for k, v in py.items():
    print("   %-13s %-42s %s" % (k, str(v), type(v).__name__))

print()
print("mode=json  :", m.model_dump(mode="json"))
print()
print("json string:", m.model_dump_json())'''),
    ],
    [
        "<code>date</code>, <code>datetime</code>, <code>time</code> and <code>timedelta</code> all accept their ISO 8601 text, and datetimes also accept a Unix timestamp.",
        "A naive datetime cannot be compared with an aware one &mdash; Python raises. Use <code>AwareDatetime</code> to reject naive input at the boundary instead of failing later.",
        "<code>Decimal(0.1)</code> inherits the float's error; <code>Decimal(\"0.1\")</code> does not. Send money as a string in JSON, and validate it as <code>Decimal</code>.",
        "<code>max_digits</code> and <code>decimal_places</code> express what a currency amount is. There is no float equivalent.",
        "<code>UUID</code> and <code>Path</code> accept their string forms and give you the real objects, with <code>.version</code>, <code>.suffix</code> and the rest.",
        "<code>model_dump()</code> keeps these as Python objects; <code>model_dump(mode=\"json\")</code> and <code>model_dump_json()</code> convert them to strings, because JSON has none of these types.",
    ],
    '''
title: Dates, UUIDs and Decimals: The Types JSON Does Not Have
intro: What Pydantic parses for you, and the two traps that cost real money.

## Why this module exists

JSON has strings, numbers, booleans, lists and objects. That is the whole list. It has no date, no UUID and no decimal. Yet your code needs all three, so something has to turn text into the right Python objects.

Pydantic does that work. It reads an ISO date string and gives you a date object. It reads a UUID string and gives you a UUID. It reads a number and, if you ask, gives you an exact Decimal. Each type has its own parsing rules and its own failure modes, and some of them catch people out.

This article explains why these types exist as a group and how Pydantic handles them. It covers dates and times, including the timezone trap, where a naive time and an aware time look the same but behave very differently. It then covers money, and why a float is the wrong type for it. You will see how to constrain a decimal to a set number of places. The last part covers UUIDs and file paths, which are small topics that save a lot of manual parsing.

Each of these types hides a small trap, and each trap is cheap to avoid once you know it.

Each one is covered with a short example so the behaviour is clear.

JSON has six types: string, number, boolean, null, array and object. Your domain has more. Dates, timestamps, durations, identifiers, money. None of them exist on the wire. All of them arrive as strings or numbers that have to be turned back into a thing handy.

That conversion is tedious, easy to get subtly wrong. Pydantic already does it. Knowing just what it accepts saves writing the parsing. Knowing where the traps are saves the bugs.

## Dates and times

`date` accepts a `date`, an ISO string like `"2026-08-26"`. A Unix timestamp. But only one that lands just on midnight. A timestamp with a time part raises `date_from_datetime_inexact`, on the thinking that silently discarding the time would lose data you might have needed.

`datetime` accepts a `datetime`, an ISO 8601 string with or without an offset. A Unix timestamp as an int or float. Both `"2026-08-26T14:30:00"` and the space-split variant work. So does a trailing `Z`.

`time` accepts `"14:30"` and `"14:30:00.123"`.

`timedelta` accepts some seconds or an ISO 8601 duration such as `"PT1H30M"`.

The pattern is the one from the coercion module. The type itself always works. The obvious textual form works. What you get back is a real object. `.year`, `.weekday()` and math all work without you having called `strptime` anywhere.

## The timezone trap

This is the first of the two costly ones.

A `datetime` string without an offset makes a **naive** datetime. One with no `tzinfo`. A string with an offset makes an **aware** one. Both are valid `datetime` objects and both pass a `datetime` annotation.

They can't be checked. `naive < aware` raises `TypeError`. Subtracting one from the other raises. So a model that accepts both will work just right until the day a client sends the other kind. Then fail one spot fully unrelated to the model.

The fix is to be clear in the type:

```python
from pydantic import AwareDatetime

updated_at: AwareDatetime
```

Now a naive string is rejected at the boundary, with a clear message, at the point the bad data arrived. `NaiveDatetime` exists for the opposite need.

The general advice for anything with users in more than one place. Store and transmit UTC with an clear offset, use `AwareDatetime` in your models. Convert to local time only at the moment of display. A system that is always aware has no timezone bugs. A system that is inconsistently aware has nothing but.

## Money is not a float

This is the second costly trap. It isn't a Pydantic quirk. It's how binary floating point works.

`0.1 + 0.2` isn't `0.3` in any language using IEEE 754. `0.1` can't be shown just in binary any more than one-third can be in decimal. The error is tiny and it builds up. Money code that builds up errors eventually makes a total that is a penny out and an afternoon no one enjoys.

`Decimal` shows decimal fractions just. But the conversion matters enormously:

```python
Decimal(0.1)     # 0.1000000000000000055511151231257827
Decimal("0.1")   # 0.1
```

By the time a float exists, the data is already lost. Passing it to `Decimal` faithfully preserves the wrong number.

So money should travel as a **string** in JSON. Be checked as `Decimal`. That is why so many payment APIs quote amounts as `"12.50"` rather than `12.50`. It's a rule worth adopting rather than fighting.

If a float is unavoidable on the way in, be aware that you've already lost exactness and any quantisation is damage control, not a fix.

## Constraining a decimal

Two constraints exist for decimals namely:

```python
amount: Decimal = Field(gt=0, max_digits=8, decimal_places=2)
```

`decimal_places=2` rejects `"12.505"`. `max_digits=8` bounds the total number of large digits. Together they express "a currency amount" far better than any `float` annotation can. They appear in the schema.

This is also a good example of a constraint carrying domain meaning. `decimal_places=2` is a statement that this system deals in whole pence. This Is a real choice that would else live only in whoever's head made it.

## UUIDs and paths

`UUID` accepts a `UUID` or its string form. Rejects anything that isn't a valid UUID. Which is a truly handy check. An id from an untrusted source is a common injection vector when it's treated as an opaque string.

What you get back is a real `UUID`. `.version` and `.hex` work. Note that `model_dump()` gives you the `UUID` object and the JSON forms give the string. This Matters if you pass the dump to a thing expecting text.

`Path` accepts a string and gives you a `pathlib.Path`, with `.suffix`, `.parent` and the rest. A caution. Checking a thing as a `Path` doesn't make it safe. It doesn't check the path exists. It certainly doesn't prevent `../../etc/passwd`. Path traversal is a security check you still have to write.

`EmailStr` deserves a mention because people look for it. It exists. It lives in a split package (`email-checker`) that must be installed. Without it, a plain `str` with a pattern is the pragmatic option. And worth remembering that no regular formula truly validates an email address. The only real check is sending a message to it.

## What comes out

Because none of these types exist in JSON, output has to convert them. The mode decides whether it does.

`model_dump()` returns Python objects: a `date` stays a `date`, a `Decimal` stays a `Decimal`. Right for passing data within your program.

`model_dump(mode="json")` returns JSON-matching values: dates become ISO strings, decimals become strings, UUIDs become strings.

`model_dump_json()` returns the JSON text right.

The mistake worth avoiding is `json.dumps(model.model_dump())`. That passes `date` and `Decimal` objects to a serialiser that can't handle them. Raises `TypeError: Object of type date isn't JSON serializable`. A confusing error. The model clearly supports JSON. Use `model_dump_json()`, or `model_dump(mode="json")` if you need the dict first.

## A checklist for these types

Use `AwareDatetime` rather than `datetime` for anything that crosses a timezone boundary. This means anything with users.

Use `Decimal` with a string input for money, always, and add `decimal_places`.

Use `UUID` rather than `str` for identifiers that are UUIDs. The check is free and catches malformed input at the door.

Use `date` rather than `datetime` when there's no time. A date that is secretly midnight in some timezone is a bug waiting for a daylight-saving transition.

And use `model_dump_json()` rather than assembling JSON yourself. The conversions happen where they're already correct.

## Formatting on the way out

Pydantic serialises dates and datetimes as ISO 8601. This Is the right default and isn't always the format a consumer wants.

Changing it's a field serialiser. This Is the next tier's material. The shape is short:

```python
@field_serializer("published_on")
def show_date(self, value: date) -> str:
    return value.strftime("%d %B %Y")
```

Worth a word of caution though. A model that serialises dates in a human format is making display output. Display formatting often belongs in the layer that knows the reader's locale rather than in the data model. For an API, ISO 8601 is almost always the correct answer and the consumer formats it.

The one common exception is a date-only field where the ISO string is already right and the concern is the *type*. Making sure a `date` doesn't accidentally serialise as a full datetime with a spurious midnight. Using `date` rather than `datetime` handles that at the source.

## Timestamps, seconds and milliseconds

A hands-on trap when accepting Unix timestamps: JavaScript's `Date.now()` returns **milliseconds**. Most of the rest of the world uses **seconds**.

Pydantic assumes seconds. Hand it a millisecond timestamp and you get a date tens of thousands of years in the future, checked happily. It's a just right valid datetime.

There's no way for the library to know which you meant. The check is yours. A constraint on the datetime range is the cheapest guard:

```python
updated_at: AwareDatetime = Field(le=datetime(2100, 1, 1, tzinfo=timezone.utc))
```

Anything from a millisecond timestamp fails that at once and obviously, at the boundary, rather than appearing in a report as the year 57,000.

## Decimals and JSON output

`Decimal` serialises to a JSON **string** by default, not a number. That is deliberate and it's correct. A JSON number is a float to most parsers. Writing `12.50` as a number would hand the receiving end the same inexactness you used `Decimal` to avoid.

It does mean a consumer expecting a number gets a string. This At times surprises people integrating with an existing client. The answer is nearly always to fix the client rather than the output. But if you must emit a number, a field serialiser can do it. You should be aware you're choosing convenience over exactness.

The same thinking shows why money should arrive as a string. A payload that sends `"12.50"` and validates it as `Decimal` is exact from end to end. One that sends `12.50` as a JSON number has already lost the promise before your model saw it.

## Comparing and storing

Two habits that prevent most date bugs downstream.

**Store UTC, display local.** Convert at the edges only. A system where all inner is UTC with an clear offset has no ambiguity anywhere. One that stores local times has an unanswerable question each time the clocks change.

**Use the narrowest type.** If a field is truly a date, annotate it `date`, not `datetime`. A `datetime` standing in for a date carries a time that means nothing. That meaningless midnight will eventually be shifted by a timezone conversion into the previous day. Choosing `date` makes that hopeless rather than unlikely.

## A quick reference

`date` &mdash; ISO string, or a timestamp landing just on midnight.

`datetime` &mdash; ISO string with or without offset, or a Unix timestamp in seconds. Prefer `AwareDatetime`.

`time` &mdash; `"14:30"` or `"14:30:00.123"`.

`timedelta` &mdash; seconds as a number, or an ISO duration like `"PT1H30M"`.

`Decimal` &mdash; a string, always, for anything money. Constrain with `decimal_places`.

`UUID` &mdash; the UUID or its string form. Invalid strings are rejected.

`Path` &mdash; a string. Note that check says nothing about safety or existence.

None of these exist in JSON. All of them are strings on the wire. `model_dump_json()` is the thing that knows how to make them.

## Why these traps are expensive

The two traps in this module. Naive datetimes and floats for money. Share a shape worth recognising. It's the shape of most costly bugs.

Neither fails at the point of the mistake. A naive datetime validates just right and sits in the model until a thing checks it to an aware one, possibly weeks later, in a other module, written by somebody else. A float price validates just right and is just right for each value anyone tests with. Wrong by fractions of a penny in aggregate.

That delay is what makes them costly. A bug that raises at once costs minutes. A bug that makes plausible wrong answers costs but long it takes for somebody to notice the totals don't merge, plus the work of finding out why.

Annotating `AwareDatetime` and `Decimal` moves both failures to the boundary. Here They're named, located and cheap. That is the same arg as the whole library, applied to the two types where getting it wrong costs the most.

## The general lesson

each type in this module exists because JSON is poorer than your domain. The gap has to be closed one spot.

Closing it in the model means the conversion happens once, in a place that is declared, tested and visible in the schema. Closing it in the consuming code means it happens all over, differently. One of those places will forget the timezone or the decimal places.

Choosing the precise type isn't pedantry. It's deciding that the gap gets closed at the boundary rather than scattered through all downstream.

## Next

That ends the shapes. The last module in this tier returns to coercion with a sharper question. Now that you know what Pydantic will convert, when should you stop it?
''',
    [
        {"q": "Why does `Decimal(\"0.1\")` differ from `Decimal(0.1)`?",
         "options": ["They are the same", "The float is already inexact before Decimal sees it", "Decimal cannot take strings", "The string is rounded"],
         "answer": 1,
         "why": "0.1 has no exact binary representation, so the float is already wrong when it is handed over. Decimal faithfully preserves the wrong value - which is why money travels as a string."},
        {"q": "What happens when you compare a naive datetime with an aware one?",
         "options": ["It works", "Python raises TypeError", "The naive one is assumed UTC", "Pydantic converts it"],
         "answer": 1,
         "why": "They are not comparable. A model accepting plain `datetime` takes both kinds happily, so the failure appears far from the model - which is what `AwareDatetime` prevents."},
        {"q": "Why does `json.dumps(m.model_dump())` fail on a model with a date field?",
         "options": ["model_dump is broken", "model_dump returns Python objects, and json.dumps cannot serialise a date", "Dates are unsupported", "It needs mode='python'"],
         "answer": 1,
         "why": "`model_dump()` deliberately keeps Python types. Use `model_dump_json()`, or `model_dump(mode=\"json\")` when you need the dict first."},
        {"q": "Which constraint expresses 'a currency amount in whole pence'?",
         "options": ["gt=0", "decimal_places=2", "max_length=2", "multiple_of=0.01"],
         "answer": 1,
         "why": "`decimal_places=2` rejects values with more precision than the system handles, and records that decision in the schema where it can be read."},
    ],
)


# ---------------------------------------------------------------------------
# 13. Strict vs lax mode
# ---------------------------------------------------------------------------
topic(
    "strict_vs_lax_mode",
    "Strict vs Lax Mode",
    "Real Data Shapes",
    "Coercion is right at the edge and wrong in the middle. How to be lax where "
    "text arrives and exact everywhere else.",
    _svg(_box(10, 22, 62, 44, S) + _txt(41, 40, "lax", M, 9) + _txt(41, 54, "converts", M, 8) +
         _box(88, 22, 62, 44, S, A) + _txt(119, 40, "strict", A, 9) + _txt(119, 54, "refuses", A, 8)),
    [
        ("The same model, two answers",
         "Lax converts anything unambiguous. Strict requires the value to already be "
         "the annotated type.",
         '''from pydantic import BaseModel, ConfigDict, ValidationError

class Lax(BaseModel):
    minutes: int
    rating: float
    published: bool

class Strict(BaseModel):
    model_config = ConfigDict(strict=True)
    minutes: int
    rating: float
    published: bool

payload = {"minutes": "12", "rating": "4.5", "published": "true"}

print("lax    :", Lax.model_validate(payload))

try:
    Strict.model_validate(payload)
except ValidationError as e:
    print("strict :", e.error_count(), "errors")
    for err in e.errors():
        print("   %-10s %s" % (err["loc"][0], err["type"]))

print()
print("strict, correct types:",
      Strict(minutes=12, rating=4.5, published=True))'''),

        ("Strict on one field only",
         "The usual need is narrower than a whole model: lax about most of a payload, "
         "exact about the one field where a quiet conversion would be dangerous.",
         '''from pydantic import BaseModel, Field, ValidationError

class Event(BaseModel):
    user_id: int = Field(strict=True)      # must really be an int
    minutes: int                            # happily takes "12"
    note: str

e = Event(user_id=42, minutes="12", note="watched")
print("ok :", e)

try:
    Event(user_id="42", minutes="12", note="watched")
except ValidationError as exc:
    err = exc.errors()[0]
    print()
    print("field:", err["loc"][0])
    print("type :", err["type"])
    print("said :", err["msg"])'''),

        ("Strict as a reusable type",
         "<code>Annotated</code> turns strictness into a named type, so the rule lives "
         "in one place and reads well at every use.",
         '''from typing import Annotated
from pydantic import BaseModel, Field, StrictInt, ValidationError

UserId = Annotated[int, Field(strict=True)]

class Enrolment(BaseModel):
    user_id: UserId
    module_id: UserId
    progress: int          # ordinary, lax

print(Enrolment(user_id=1, module_id=2, progress="40"))

for bad in [{"user_id": "1", "module_id": 2, "progress": 0},
            {"user_id": 1, "module_id": "2", "progress": 0}]:
    try:
        Enrolment.model_validate(bad)
    except ValidationError as e:
        print("refused:", e.errors()[0]["loc"][0])

# Pydantic ships some of these ready made:
class Ready(BaseModel):
    n: StrictInt
print()
print("StrictInt is the same idea:", Ready(n=5))'''),

        ("What strict still allows",
         "Strict is not “no conversion at all”. Widening that cannot lose information "
         "still happens, and a bool is still an int in Python.",
         '''from pydantic import BaseModel, ConfigDict, ValidationError

class S(BaseModel):
    model_config = ConfigDict(strict=True)
    x: float

for value in [1.5, 2, True, "3.0"]:
    try:
        print("%-6r -> %r" % (value, S(x=value).x))
    except ValidationError:
        print("%-6r -> refused" % (value,))

print()
print("int -> float is a widening with no loss, so strict permits it.")
print("The string is refused: that would be parsing, not widening.")'''),

        ("JSON is strict-aware",
         "Validating from JSON in strict mode still accepts the forms JSON has no "
         "choice about &mdash; a date has to arrive as text because JSON has no dates.",
         '''from datetime import date
from pydantic import BaseModel, ConfigDict, ValidationError

class Strict(BaseModel):
    model_config = ConfigDict(strict=True)
    published_on: date
    minutes: int

# From JSON: the date must be a string, and strict accepts that.
print("from json  :", Strict.model_validate_json(
    '{"published_on": "2026-08-26", "minutes": 12}'))

# From Python: a string date is refused, because a real date was available.
try:
    Strict(published_on="2026-08-26", minutes=12)
except ValidationError as e:
    print("from python:", e.errors()[0]["msg"])

print("from python:", Strict(published_on=date(2026, 8, 26), minutes=12))'''),

        ("The pattern worth copying",
         "Two models: a lax one at the boundary that accepts the wire format, and a "
         "strict one inside where a wrong type means a bug of your own.",
         '''from pydantic import BaseModel, ConfigDict, ValidationError

class ModuleIn(BaseModel):
    "The boundary. Text arrives; convert it."
    title: str
    minutes: int
    published: bool

class Module(BaseModel):
    "The interior. Types are already right; a mismatch is our bug."
    model_config = ConfigDict(strict=True, frozen=True)
    title: str
    minutes: int
    published: bool

raw = {"title": "Vectors", "minutes": "12", "published": "yes"}

checked = ModuleIn.model_validate(raw)
module = Module.model_validate(checked.model_dump())

print("boundary :", checked)
print("interior :", module)
print()

# Later, somewhere in our own code, a mistake:
try:
    Module(title="Norms", minutes="8", published=False)
except ValidationError as e:
    print("caught our own bug:", e.errors()[0]["msg"])'''),
    ],
    [
        "Lax is the default and it exists because the boundary is made of text. Query strings, form posts and CSVs have no integers in them.",
        "Strict requires the value to already be the annotated type. It is set per model with <code>ConfigDict(strict=True)</code> or per field with <code>Field(strict=True)</code>.",
        "Per-field is usually what you want. Identifiers and money are the classic cases: a silent conversion there hides a real upstream mistake.",
        "Strict still permits lossless widening &mdash; <code>int</code> to <code>float</code> &mdash; and <code>bool</code> remains a subclass of <code>int</code>.",
        "In strict mode, JSON input still accepts the string forms JSON forces, such as dates. Strictness is about avoiding <em>unnecessary</em> conversion, not about refusing the format.",
        "<code>StrictInt</code>, <code>StrictStr</code>, <code>StrictBool</code> and <code>StrictFloat</code> are ready-made types for the same thing.",
    ],
    '''
title: Strict vs Lax Mode: Where Coercion Helps and Where It Hides Bugs
intro: The default is right at the edge of your system and wrong in the middle. Choosing per field is the answer.

## Two different jobs

By default Pydantic runs in lax mode. It converts values when it can, so "5" becomes 5 and 1 becomes True. That is friendly, and for data that arrives as text it is usually what you want. It can also hide bugs, because a wrong type gets quietly fixed instead of reported.

Strict mode does the opposite. It accepts only values that already have the right type. A string where an integer belongs is an error, even if the string looks like a number. The two modes do different jobs, and choosing between them is a design decision about how much you trust your input.

This article explains the two jobs and how to switch strict mode on. It shows that you can set it for a whole model, but that a per-field setting is usually the better answer. It also covers what strict mode still allows, since it is less rigid than people expect. The last section looks at strict mode and JSON, where the rules differ from Python input. After reading it you will know when a strict field is worth the friction.

all in this tier has assumed lax mode. This Is the default: convert anything with an unambiguous reading, refuse the rest.

That is just right at a boundary. A query string is text. A form post is text. A CSV is text. If check refused all that wasn't already the right Python type, the code in front of each model would be a pile of `int()` calls in `try` blocks. This Is the code the library exists to delete.

It's just wrong three layers in. If a function inside your own system passes a string where an int was expected, that is a bug you wrote. Converting it silently means the bug lives. The symptom appears one spot else. Often as a number that is subtly wrong rather than an error that names the cause.

Same action, opposite value, based on which side of the boundary you're standing on. Which is why the setting exists.

## Turning it on

Per model:

```python
class Config(BaseModel):
    model_config = ConfigDict(strict=True)
```

Per field:

```python
user_id: int = Field(strict=True)
```

Or as a reusable type. This Is often the nicest:

```python
UserId = Annotated[int, Field(strict=True)]
```

Pydantic also ships `StrictInt`, `StrictStr`, `StrictBool` and `StrictFloat`. This Are the same thing pre-named.

## Per field is the usual answer

Whole-model strictness sounds tidy and is often impractical. A real payload mixes fields that arrive as text with fields that don't.

The narrower need is much more common: be lax about most of a model and exact about the one or two fields where a quiet conversion would be dangerous.

**Identifiers** are the classic case. A `user_id` arriving as `"42"` rather than `42` often means a thing upstream lost a type. A JSON serialiser configured oddly, a value that went through a URL and was never converted back. Accepting it papers over that. Refusing it tells you where the problem is while it's still cheap to find.

**Money** is the other. A `Decimal` field that accepts a float will accept an already-inexact value and validate it happily. This Is the worst possible outcome for a currency amount.

**Booleans** are worth considering too. `bool` is generous in lax mode. `"yes"`, `"on"`, `"t"` all work. And that is truly handy for a checkbox and truly alarming for a flag that controls whether money moves.

## What strict still allows

Strict doesn't mean "no conversion whatsoever", and the exceptions are principled.

An `int` is still accepted for a `float` field. Widening an int to a float loses nothing and Python treats the two as by number matching throughout.

A `bool` is still accepted for an `int` field. `bool` truly is a subclass of `int` in Python. That one at times surprises people. If it matters, a checker is the way to exclude it.

What strict drops is **parsing**. Turning text into a thing else. `"3.0"` to a float is parsing, and strict refuses it.

## Strict and JSON

There's a subtlety worth understanding, because it looks like an inconsistency and isn't.

In strict mode, checking from a JSON string still accepts the textual forms JSON has no option to. A `date` field checked from JSON accepts `"2026-08-26"`. JSON has no date type and there's no stricter form on hand.

checked from Python, the same strict model refuses that string. In Python a real `date` object *was* on hand and a string means somebody skipped a step.

The principle is steady once stated: strict mode refuses *not needed* conversion. When the format offers no option, accepting the only on hand form isn't laxity.

This is one more reason `model_validate_json` is worth preferring over `json.loads` plus `model_validate`. It knows the input was JSON and applies the right rules. Going via Python objects loses that context.

## The two-model pattern

The clean way to express all of this is a lax model at the boundary and a strict one inside:

```python
class ModuleIn(BaseModel):          # boundary: text arrives, convert it
    title: str
    minutes: int

class Module(BaseModel):            # interior: types are already right
    model_config = ConfigDict(strict=True, frozen=True)
    title: str
    minutes: int
```

The boundary model absorbs the messiness of the wire. The interior model is a statement that all past this point has been checked. A mistake in your own code will be caught rather than converted.

Adding `frozen=True` to the interior model is a natural companion. Checked data that only gets read has no reason to be mutable. Freezing it drops another class of question.

Whether this is worth two classes depends on the system. For a small use it's over-engineering. One lax model is fine. For a large one with a few layers and a few teams, the strict interior model is a contract that catches real mistakes.

## A middle path

If two models feels like too much, there's a lighter version that gets most of the gain. Turn on `validate_assignment` and make the key fields strict.

```python
class Module(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    user_id: Annotated[int, Field(strict=True)]
    minutes: int
```

Now the payload can arrive as text and be converted. The identifier must be right. Later sets are checked rather than trusted. One class, and the two most common bug sources are closed.

## When to reach for strict

**Do** use it on identifiers, money, and any flag with results.

**Do** use it for interior models in a layered system. Here Wrong types show your own bugs.

**Do** use it in tests. Here You want to assert on just what a function made without coercion smoothing it over.

**Don't** use it on a public API's request model. Your clients send JSON, JSON sends text. Refusing `"12"` for a duration will make support tickets rather than better data.

**Don't** reach for it as a general "safer" setting. Lax mode isn't sloppy. It's the correct action for the job it was designed for. Strictness applied indiscriminately just moves work back into your callers.

## Strictness in tests

There's a use for strict mode that has nothing to do with production. It's one of the most valuable.

In a test, coercion can hide the thing you're asserting. A test that checks a function returned `minutes=12` will pass if the function returned `"12"` and the model converted it. So the test doesn't really verify the action it claims to.

checking the result with a strict model closes that gap. The assertion turns about the real type. A function that starts returning strings fails the test rather than quietly leaning on coercion downstream.

The same applies to fixtures. A fixture built with `minutes="12"` isn't exercising the same code path as production data that arrives as an int, and strictness makes that visible.

## What strict does not protect you from

Worth being clear about the limits. "strict" sounds like a general safety setting and isn't.

It doesn't check ranges. `StrictInt` accepts `-999999` happily. That is what `Field(gt=0)` is for.

It doesn't check meaning. A strict `str` accepts an empty string, a string of spaces. A string holding a script tag.

It doesn't make a model safe to expose. Strictness is about types, not about authorisation, sanitisation or business rules.

And it doesn't drop the need to think about the boundary. A strict model at the edge of a public API doesn't make the API safer. It makes it harder to call right. This Pushes the conversion into your consumers' code where you can't see it.

## Reading the errors

Strict failures have their own error types, and recognising them saves a moment's confusion.

Where a lax model would report `int_parsing` for `"twelve"`, a strict model reports `int_type` for `"12"`. The message is about the *type* being wrong rather than the value being unparseable.

That gap is truly handy in a log. `int_parsing` means somebody sent nonsense. `int_type` on a strict field means somebody sent a well-formed value in the wrong form. This Is often a wiring problem in a caller rather than bad input from a user. The two deserve other responses.

## A decision you can apply mechanically

For each field, ask where its value comes from.

**From a human, a form, a URL or a CSV**. Lax. It's text, it will always be text. Refusing it moves work to the caller with no gain.

**From another service's JSON** &mdash; lax for anything JSON has no type for, strict for identifiers. A partner sending `"user_id": "42"` is worth knowing about.

**From your own code, past the boundary**. Strict. A wrong type here is your bug and you want it loud.

**From a test** &mdash; strict. So The assertion means what it says.

Applied field by field, that makes models that are permissive just where permissiveness helps and exact all over else. Which is the whole point. Isn't a thing a single global setting can express.

## The principle underneath

Both modes exist because check answers a other question in other places.

At the boundary the question is "can I make sense of this?". Being generous is correct. The sender had no better option than text.

Inside the question is "is this what I think it's?". Being generous is wrong. The sender is you and a mismatch means a thing is broken.

Getting this right is mostly a matter of noticing which question you're asking. The setting is small. The habit of asking is the thing worth taking away.

## One more reason it matters

Coercion is the feature people are most suspicious of when they meet Pydantic and most dependent on within a week. That reversal is worth understanding. It's the same reversal that makes the strict/lax choice feel hard.

The suspicion is fair: a library that silently changes your data sounds like a library that will eventually change it wrongly. The dependence is also fair: the boundary really is made of text. A thing has to do the converting.

What resolves it's that Pydantic's conversion is bounded by a rule you can state in one sentence. Convert when the reading is unambiguous and nothing is lost. And that you can switch it off, per field, wherever that rule isn't the one you want.

Very few libraries give you both the sensible default and the precise replace. Knowing that the replace exists. Where to apply it, is what turns coercion from a thing you handle into a thing you've decided about.

## Where to start if you are unsure

If this is a new code, the pragmatic default is: lax all over, plus `strict=True` on identifiers and money.

That mix takes ten seconds to apply, keeps each request model easy to call. Closes the two cases where a silent conversion most often shows a real problem upstream. It's a better starting point than either extreme. You can tighten exact fields later as you learn where your data really goes wrong.

The one thing worth doing on purpose rather than by default is choosing, once, for each new field. Strictness applied by habit is no better than laxity applied by habit.

## Where tier two leaves you

You can now show data with real shape. Models inside models, sets with real error paths, unions that say which branch they're, closed sets of values. The standard-library types that JSON can't carry. And you can decide, per field, how much conversion you're willing to accept.

What you can't yet do is express a rule that no annotation can hold. A value that must be checked against another value, a field found from the rest, a scaling applied before checking. That is the next tier, and it starts with checkers.

## Summary

Lax mode converts anything unambiguous and is correct at the boundary. The boundary is text. Strict mode needs the annotated type and is correct inside, because a mismatch there's your own bug.

Set it per field rather than per model often. Strict still permits lossless widening. Still accepts the string forms JSON has no option to. Identifiers, money and consequential flags are the fields where it earns its place first.
''',
    [
        {"q": "Why is lax mode the default?",
         "options": ["It is faster", "Because data at a boundary arrives as text and would otherwise need manual conversion everywhere", "For backwards compatibility", "It is not - strict is"],
         "answer": 1,
         "why": "Query strings, form posts and CSVs contain no integers. Refusing text would put an `int()` call in a try block in front of every model, which is the code the library removes."},
        {"q": "Does strict mode refuse an `int` for a `float` field?",
         "options": ["Yes", "No - widening loses nothing, so it is allowed", "Only in JSON mode", "Only for negatives"],
         "answer": 1,
         "why": "Strict removes parsing, not lossless widening. `bool` for an `int` is also still accepted, because bool genuinely is a subclass of int in Python."},
        {"q": "A strict model validates a `date` field from a JSON string. What happens?",
         "options": ["Refused - it is a string", "Accepted, because JSON has no date type", "Converted silently in all modes", "It raises a config error"],
         "answer": 1,
         "why": "Strict refuses *unnecessary* conversion. From Python a real date object was available so a string is refused; from JSON the string is the only representation there is."},
        {"q": "Which field is the classic candidate for `strict=True` in an otherwise lax model?",
         "options": ["A description", "An identifier or a money amount", "An optional note", "A title"],
         "answer": 1,
         "why": "An id arriving as text usually means something upstream lost a type, and a Decimal accepting a float accepts an already-inexact value. Both are cases where silence hides a real problem."},
    ],
)


# ---------------------------------------------------------------------------
# 14. field_validator
# ---------------------------------------------------------------------------
topic(
    "field_validator",
    "field_validator",
    "Control",
    "Rules a type cannot express, and normalisation applied before the value is "
    "ever stored.",
    _svg(_txt(30, 30, '" Ada "', M, 8) + _arrow(56, 26, 76, 26) +
         _box(80, 16, 66, 20, S, A) + _txt(113, 30, "validator", A, 8) +
         _arrow(113, 42, 113, 56) + _txt(113, 70, '"Ada"', A, 9)),
    [
        ("A rule the annotation cannot hold",
         "Anything that is not a type, a bound or a pattern needs code. A validator "
         "receives the value after coercion and either returns it or raises.",
         '''from pydantic import BaseModel, field_validator, ValidationError

TRACKS = {"maths", "python", "dsa", "ml"}

class Module(BaseModel):
    title: str
    track: str

    @field_validator("track")
    @classmethod
    def known_track(cls, v: str) -> str:
        if v not in TRACKS:
            raise ValueError("unknown track %r; try one of %s"
                             % (v, ", ".join(sorted(TRACKS))))
        return v

print(Module(title="Vectors", track="maths"))

try:
    Module(title="Vectors", track="astrology")
except ValidationError as e:
    err = e.errors()[0]
    print()
    print("type :", err["type"])
    print("said :", err["msg"])'''),

        ("Returning a changed value",
         "A validator is not only a check. Whatever it returns becomes the field, "
         "which makes it the right place for normalisation.",
         '''from pydantic import BaseModel, field_validator

class Module(BaseModel):
    title: str
    tags: list

    @field_validator("title")
    @classmethod
    def tidy(cls, v: str) -> str:
        return " ".join(v.split()).title()

    @field_validator("tags")
    @classmethod
    def lower_unique(cls, v: list) -> list:
        seen, out = set(), []
        for tag in v:
            t = tag.strip().lower()
            if t and t not in seen:
                seen.add(t)
                out.append(t)
        return out

m = Module(title="  the   chain    RULE ", tags=[" Maths ", "maths", "CALCULUS", ""])
print("title:", repr(m.title))
print("tags :", m.tags)'''),

        ("One validator, several fields",
         "Pass more than one name, or <code>\"*\"</code> for all of them. The field "
         "being validated is available through the info argument.",
         '''from pydantic import BaseModel, field_validator, ValidationInfo, ValidationError

class Module(BaseModel):
    title: str
    summary: str
    track: str

    @field_validator("title", "summary")
    @classmethod
    def not_blank(cls, v: str, info: ValidationInfo) -> str:
        if not v.strip():
            raise ValueError("%s cannot be blank" % info.field_name)
        return v.strip()

    @field_validator("*")
    @classmethod
    def no_control_chars(cls, v):
        if isinstance(v, str) and any(ord(c) < 32 for c in v):
            raise ValueError("contains a control character")
        return v

print(Module(title=" Vectors ", summary=" What they are ", track="maths"))

try:
    Module(title="   ", summary="x", track="maths")
except ValidationError as e:
    print()
    print("blank:", e.errors()[0]["msg"])'''),

        ("Seeing fields already validated",
         "<code>info.data</code> holds the fields validated <em>before</em> this one. "
         "Declaration order therefore decides what is visible.",
         '''from pydantic import BaseModel, field_validator, ValidationInfo, ValidationError

class Module(BaseModel):
    minutes: int
    lessons: int

    @field_validator("lessons")
    @classmethod
    def enough_time(cls, v: int, info: ValidationInfo) -> int:
        minutes = info.data.get("minutes")       # declared above, so present
        if minutes is not None and v > minutes:
            raise ValueError("%d lessons cannot fit in %d minutes" % (v, minutes))
        return v

print(Module(minutes=30, lessons=5))

try:
    Module(minutes=3, lessons=5)
except ValidationError as e:
    print("refused:", e.errors()[0]["msg"])

# If an earlier field failed, it is simply absent from info.data:
try:
    Module(minutes="ages", lessons=5)
except ValidationError as e:
    print()
    print("earlier failure:", [x["loc"][0] for x in e.errors()])'''),

        ("Before and after coercion",
         "<code>mode=\"after\"</code> is the default and sees the converted value. "
         "<code>mode=\"before\"</code> sees the raw input, which is where you fix a "
         "shape rather than a value.",
         '''from pydantic import BaseModel, field_validator

class Module(BaseModel):
    tags: list

    # The wire sometimes sends "a,b,c" instead of a list. Fix the shape
    # BEFORE Pydantic tries to validate it as a list.
    @field_validator("tags", mode="before")
    @classmethod
    def split_csv(cls, v):
        if isinstance(v, str):
            return [part.strip() for part in v.split(",") if part.strip()]
        return v

    @field_validator("tags")            # mode="after" is the default
    @classmethod
    def lowercase(cls, v: list) -> list:
        return [t.lower() for t in v]

print("from a list  :", Module(tags=["Maths", "Vectors"]).tags)
print("from a string:", Module(tags="Maths, Vectors, Norms").tags)'''),

        ("Where a validator is the wrong tool",
         "If a constraint can express the rule, use the constraint &mdash; it appears "
         "in the schema and a validator does not.",
         '''from pydantic import BaseModel, Field, field_validator

class ByValidator(BaseModel):
    minutes: int

    @field_validator("minutes")
    @classmethod
    def positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("must be positive")
        return v

class ByConstraint(BaseModel):
    minutes: int = Field(gt=0)

for cls in (ByValidator, ByConstraint):
    spec = cls.model_json_schema()["properties"]["minutes"]
    print("%-13s schema: %s" % (cls.__name__, spec))

print()
print("Both reject -1. Only one told the documentation, the generated")
print("client and the form builder that zero is the floor.")'''),
    ],
    [
        "A validator runs after coercion by default, so the value it receives is already the annotated type.",
        "Whatever it <strong>returns</strong> becomes the field. Forgetting the <code>return</code> silently sets the field to <code>None</code>.",
        "Raise <code>ValueError</code>. Pydantic wraps it with the field's location and gives it the type <code>value_error</code>.",
        "<code>@classmethod</code> is required and goes <em>below</em> <code>@field_validator</code>. The wrong order is a common and confusing error.",
        "<code>info.data</code> exposes fields validated earlier, so declaration order decides what a validator can see. For a rule that needs everything, use <code>model_validator</code>.",
        "Prefer a <code>Field</code> constraint when one can express the rule: constraints reach the JSON Schema, validators do not.",
    ],
    '''
title: field_validator: Rules an Annotation Cannot Express
intro: Custom checks and scaling, and just where in the pipeline they run.

## What is left after types and constraints

Types and constraints cover a great deal, but not everything. Some rules need real logic. A slug must be lowercase with no spaces. A date must fall on a weekday. An email domain must be on an approved list. No annotation can say that, so Pydantic lets you write a function.

A field validator is a method attached to one field. Pydantic calls it after the type check, hands it the value, and takes back either the value or an error. It can also change the value on the way through, which makes it a good place to clean up input as well as reject it.

This article shows the shape of a field validator and the decorator that marks it. It covers the quiet second job, which is normalisation, such as trimming spaces or fixing case. You will see how to apply one validator to several fields at once, and how a validator can look at other fields that were already checked. Along the way it points out the common mistakes, like raising the wrong kind of error. It is the first place you write your own logic into a model.

You do not need to write a validator for every field. Most fields need none. The skill is knowing the moment when a type and a constraint have run out, and the article gives you a simple way to tell. When that moment arrives, a few lines of plain Python usually settle it.

Annotations show the kind of value. Constraints narrow it to a range, a length or a pattern. Between them they cover a great deal, and then they stop.

They can't check membership of a set that lives in a DB. They can't norm whitespace before checking a length. They can't say "if this looks like a legacy identifier, convert it". They can't express any rule whose logic is longer than a compare.

`field_validator` is where those live. It's a classmethod that receives one field's value. Either returns a value or raises.

## The shape

```python
@field_validator("track")
@classmethod
def known_track(cls, v: str) -> str:
    if v not in TRACKS:
        raise ValueError("unknown track %r" % v)
    return v
```

Four things about that are load-bearing.

**`@classmethod` is needed**, and it must sit *below* `@field_validator`. Decorators apply bottom-up. This order gives `field_validator` a classmethod to register. Reversed, you get an error that doesn't obviously say what is wrong, and it's one of the most common mistakes people make with this API.

**Raise `ValueError`**, not `ValidationError`. Pydantic catches it, attaches the field's location, gives it the type `value_error`. Folds it into the same report as each built-in failure. Making a `ValidationError` yourself is awkward and not needed. `AssertionError` also works but is a poor choice. `python -O` drops assertions and your check would silently stop running.

**Return the value.** This is the mistake that bites hardest. It fails quietly. A checker that checks and forgets to return sets the field to `None`. If a field mysteriously turns `None` after you add a checker, this is why.

**Name the failure usefully.** The message goes to whoever sent the data. `"unknown track 'astrology'. Try one of dsa, maths, ml, python"` is worth the extra few characters over `"invalid"`.

## Validation is also normalisation

Because the returned value turns the field, a checker is the natural place to clean data.

Stripping whitespace, merging runs of spaces, lowercasing an identifier, deduplicating a list, norming a phone number. All of these belong here. Doing them here means each consumer downstream gets the clean version. The option is norming at each use site. Here One place will forget.

There's a small config-level shortcut for the most common case: `str_strip_whitespace=True` in `model_config` strips each string field. This Drops a lot of trivial checkers in one line.

Be careful about how much you transform. A checker that much rewrites its input is doing work a reader won't expect from the annotation. A caller may be surprised that what they sent isn't what came back. Norming whitespace is uncontroversial. Silently correcting a misspelt group isn't. Probably deserves to be an error instead.

## Several fields at once

The decorator takes multiple names:

```python
@field_validator("title", "summary")
```

And `"*"` applies to each field. This Is at times handy for a cross-cutting concern. Rejecting control characters, say. Though a checker that runs on each field has to be careful. It will receive values of each type.

`ValidationInfo`, the optional second arg, carries `field_name`. This Is what lets one checker give a message naming the exact field it was applied to.

## Seeing other fields, and the limit of that

`info.data` is a dict of the fields checked *before* this one:

```python
@field_validator("lessons")
@classmethod
def enough_time(cls, v, info):
    minutes = info.data.get("minutes")
```

Fields are checked in declaration order. `minutes` is visible to `lessons` only because it's declared above it. Reorder the class and the checker silently stops seeing it.

That fragility is the reason to treat `info.data` as a convenience rather than the tool for cross-field rules. Use `.get()` rather than indexing. A field that failed its own check is simply absent. A `KeyError` inside a checker is a much worse error than the one it was trying to report.

For any rule that truly depends on more than one field, `model_validator(mode="after")` is the correct tool. It runs once, after all is populated. It doesn't care what order the class was written in. That is the next module.

## Before and after

By default a checker runs in `mode="after"`. After coercion. The value is already the annotated type. That is what you want for almost each rule. You're checking a real `int` rather than a thing that might be a string.

`mode="before"` runs on the raw input, before Pydantic has tried anything. Its use is fixing the *shape* of data rather than the value:

```python
@field_validator("tags", mode="before")
@classmethod
def split_csv(cls, v):
    if isinstance(v, str):
        return [p.strip() for p in v.split(",")]
    return v
```

A caller sends `"maths,vectors"` where a list was wanted. In `after` mode you'd never see it. Check would already have failed. A string isn't a list. In `before` mode you can convert it and let normal check proceed.

Two rules for `before` checkers. Accept what might arrive. The value hasn't been checked and could be anything. Guard with `isinstance` rather than given. And pass through anything you don't handle, unchanged. So The normal path still runs.

## Validators and inheritance

checkers are from parent like any other classmethod. A base model's rules apply to each subclass. That makes a base a good home for cross-cutting scaling.

A subclass can replace a checker by defining one with the same name. This Replaces it fully rather than adding to it. If you want both, give them other names. A few checkers can target the same field and they run in meaning order.

## When not to reach for one

Three cases where a checker is the wrong answer.

**When a constraint would do.** `Field(gt=0)` and a checker that checks `v > 0` both reject the same values. Only the constraint appears in the JSON Schema. That means the docs says the min, the made client knows it. A form can enforce it before a request is sent. A checker is invisible to all of that.

**When it needs I/O.** A checker that queries a DB to check a foreign key turns check into a network call, makes the model untestable without a DB. Turns a check error into a timeout. Keep models pure. They check data using only data. Existence checks belong in the layer that owns the storage.

**When it's really a type.** A checker enforcing membership of four strings should be a `Literal`. A checker checking a value is one of a set with action should be an `Enum`. Both give better errors and both appear in the schema.

## Several validators on one field

More than one checker can target the same field, and they run in meaning order:

```python
@field_validator("slug")
@classmethod
def strip(cls, v): return v.strip()

@field_validator("slug")
@classmethod
def lower(cls, v): return v.lower()
```

Splitting rules like this is often clearer than one function doing four things. Each has a name that says what it enforces. The name matters more than it looks. It appears in tracebacks and it's what a reader scans for when asking "where is the rule about slugs?".

The counter-arg is that a chain of tiny checkers can obscure the order dependency between them. If step two only makes sense after step one, saying so in one function with two comments is honest. Splitting them and hoping no one reorders isn't.

## What info carries

The optional second param is a `ValidationInfo`. Beyond `field_name` and `data` it has two more things.

`config` exposes the model's config. This Lets a checker behave differently based on, say, whether the model is strict.

`context` is any data you pass in at check time:

```python
Module.model_validate(payload, context={"tenant": "acme"})
```

Inside a checker, `info.context` holds that dict. This is the supported way to give check access to a thing external without reaching for a global. A tenant, a feature flag, a set of permitted values loaded once per request.

It's truly handy and easy to overuse. A model whose rules depend heavily on context is a model that can't be understood on its own. The checks may belong in a service instead.

## Reusing a rule across models

If two models need the same checker, don't copy it. There are two clean options.

Put it on a shared base model. Each subclass takes from it. Good when the models are truly related.

Or make it part of a type with `AfterValidator`. The rule travels with the annotation rather than with the class. That is the `Annotated` module's subject. It's often the better answer when the models are unrelated but the field means the same thing in both.

Copying the same `@field_validator` into four classes is the thing both of those exist to prevent.

## Errors worth writing well

The message you raise is seen by whoever sent the data. It's worth a moment's thought.

Include what was wrong and what would be right. `"unknown track 'astrology'. Try one of dsa, maths, ml, python"` costs a few characters and saves a support message.

Don't include the value if it might be sensitive. The error report already carries `input`. A message that also embeds a token puts it in a second place.

And keep the message about the data, not the code. `"check failed in known_track"` tells the caller nothing they can act on.

## Summary

`field_validator` handles what annotations and constraints can't: logic. It runs after coercion by default, receives one field. What it returns turns that field. Which makes it as much a scaling hook as a check.

note the four mechanics: `@classmethod` underneath, raise `ValueError`, always return. Use `mode="before"` only when you're fixing shape rather than value.

And reach for it second. Types first, constraints next, checkers for what is left.

## A worked example

A tag list arriving from a form, needing three things done to it.

```python
@field_validator("tags", mode="before")
@classmethod
def accept_csv(cls, v):
    return [p for p in v.split(",")] if isinstance(v, str) else v

@field_validator("tags")
@classmethod
def clean(cls, v: List[str]) -> List[str]:
    seen, out = set(), []
    for tag in v:
        t = tag.strip().lower()
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out
```

Two checkers, two jobs, two modes. The first repairs the shape when a caller sends a string. The second norms and deduplicates once the value really is a list.

Splitting them this way is deliberate. Doing both in a single `before` checker would mean the cleaning logic runs on unvalidated input and has to defend itself. Doing both in `after` would mean the string never arrives. Each piece runs where its assumptions hold.

The result is a field that accepts `"Maths, maths, VECTORS "` or `["Maths", "maths", "VECTORS "]` and makes `["maths", "vectors"]` either way. And each consumer downstream gets the clean version without knowing any of this happened.

## The order to reach for things

Types, then constraints, then checkers. Working down that list rather than up makes models where most rules are visible in the annotations and only the truly complex ones are in code. Which is also the order of how much each rule tells your schema, your docs and your consumers.

## Validators and the schema

Worth restating once more, because it's the trade this whole module sits inside.

A checker enforces a rule just right and tells no one. The value is rejected, the caller gets an error. Each tool that reads your schema. docs, made clients, form builders, contract tests. Remains unaware that the rule exists.

That isn't an arg against checkers. It's an arg for using them for what truly needs them. For reaching first for the annotations and constraints that can say the same thing in a form other tools can read.

When a rule can only be a checker, consider showing it in the model's docstring. This Turns the schema's description. The rule still won't be machine-readable. A human reading your docs will at least know it's there rather than discovering it through a rejection.
''',
    [
        {"q": "What happens if a validator checks a value but forgets to return it?",
         "options": ["The original value is kept", "The field becomes None", "It raises", "Validation is skipped"],
         "answer": 1,
         "why": "Whatever the validator returns becomes the field, and a function with no return returns None. This fails silently, which is what makes it the most costly mistake with this API."},
        {"q": "Why must `@classmethod` sit below `@field_validator`?",
         "options": ["Style only", "Decorators apply bottom-up, so field_validator needs a classmethod to register", "It does not matter", "classmethod is optional"],
         "answer": 1,
         "why": "The inner decorator runs first. Reversed, field_validator receives a plain function and the resulting error does not obviously explain the cause."},
        {"q": "When is `mode=\"before\"` the right choice?",
         "options": ["Always", "When fixing the shape of raw input, such as a CSV string that should be a list", "For performance", "When raising errors"],
         "answer": 1,
         "why": "In after mode the value has already been coerced, so a string where a list was expected has already failed. Before mode is the only place to repair the shape."},
        {"q": "Why prefer `Field(gt=0)` over a validator that checks `v > 0`?",
         "options": ["It is faster", "The constraint appears in the JSON Schema; the validator is invisible to docs and clients", "Validators cannot raise", "No difference"],
         "answer": 1,
         "why": "Both reject the same values, but only the constraint reaches documentation, generated clients and form builders that read the schema."},
    ],
)


# ---------------------------------------------------------------------------
# 15. model_validator
# ---------------------------------------------------------------------------
topic(
    "model_validator",
    "model_validator",
    "Control",
    "Rules that span fields - the ones a per-field validator structurally cannot "
    "see.",
    _svg(_box(16, 20, 52, 22, S) + _txt(42, 34, "starts", M, 8) +
         _box(92, 20, 52, 22, S) + _txt(118, 34, "ends", M, 8) +
         _box(16, 52, 128, 22, S, A) + _txt(80, 66, "ends > starts", A, 8)),
    [
        ("A rule about two fields",
         "<code>mode=\"after\"</code> runs once, on the finished model, with every "
         "field populated and converted. Return <code>self</code>.",
         '''from datetime import date
from pydantic import BaseModel, model_validator, ValidationError

class Cohort(BaseModel):
    starts_on: date
    ends_on: date

    @model_validator(mode="after")
    def ends_after_start(self):
        if self.ends_on <= self.starts_on:
            raise ValueError("ends_on must be after starts_on")
        return self

print(Cohort(starts_on="2026-09-01", ends_on="2026-12-01"))

try:
    Cohort(starts_on="2026-12-01", ends_on="2026-09-01")
except ValidationError as e:
    err = e.errors()[0]
    print()
    print("loc  :", err["loc"], "<- empty: it belongs to the model, not a field")
    print("said :", err["msg"])'''),

        ("Order does not matter here",
         "A field validator can only see fields declared above it. A model validator "
         "sees all of them, however the class is written.",
         '''from pydantic import BaseModel, model_validator, ValidationError

class Budget(BaseModel):
    spent: int
    total: int          # declared AFTER spent

    @model_validator(mode="after")
    def within_budget(self):
        if self.spent > self.total:
            raise ValueError("spent %d exceeds total %d" % (self.spent, self.total))
        return self

print(Budget(spent=40, total=100))

try:
    Budget(spent=140, total=100)
except ValidationError as e:
    print("refused:", e.errors()[0]["msg"])

print()
print("A field_validator on 'spent' could not have done this:")
print("'total' is declared later, so it is not in info.data yet.")'''),

        ("At least one of these",
         "The classic cross-field rule. Neither field is individually wrong; the "
         "combination is.",
         '''from typing import Optional
from pydantic import BaseModel, model_validator, ValidationError

class Contact(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None

    @model_validator(mode="after")
    def one_way_to_reach(self):
        if not self.email and not self.phone:
            raise ValueError("provide at least an email or a phone number")
        return self

print(Contact(email="ada@vizlearn.in"))
print(Contact(phone="+44 20 7946 0958"))

try:
    Contact()
except ValidationError as e:
    print()
    print("refused:", e.errors()[0]["msg"])'''),

        ("mode=before: reshaping the whole payload",
         "A before validator receives the raw input for the entire model. It is where "
         "you accept a legacy shape and translate it.",
         '''from pydantic import BaseModel, model_validator

class Module(BaseModel):
    title: str
    minutes: int

    @model_validator(mode="before")
    @classmethod
    def accept_old_shape(cls, data):
        if isinstance(data, dict):
            data = dict(data)
            # v1 of our API called these something else.
            if "name" in data and "title" not in data:
                data["title"] = data.pop("name")
            if "duration_seconds" in data and "minutes" not in data:
                data["minutes"] = round(data.pop("duration_seconds") / 60)
        return data

print("new shape:", Module(title="Vectors", minutes=8))
print("old shape:", Module.model_validate({"name": "Vectors",
                                           "duration_seconds": 480}))'''),

        ("Deriving a field from others",
         "An after validator can set fields as well as check them &mdash; useful when "
         "one value should be filled in from the rest.",
         '''from typing import Optional
from pydantic import BaseModel, model_validator

class Module(BaseModel):
    title: str
    slug: Optional[str] = None

    @model_validator(mode="after")
    def fill_slug(self):
        if self.slug is None:
            object.__setattr__(self, "slug",
                               self.title.lower().replace(" ", "-"))
        return self

print(Module(title="The Chain Rule"))
print(Module(title="The Chain Rule", slug="chain-rule"))

print()
print("For values that are ALWAYS derived and never supplied,")
print("a computed_field is the better tool - that is the next module.")'''),

        ("Several rules, and where they report",
         "Model validators run in definition order, after every field. The first to "
         "raise stops the rest, so put the cheapest check first.",
         '''from pydantic import BaseModel, model_validator, ValidationError

class Enrolment(BaseModel):
    seats: int
    taken: int
    waitlist: int

    @model_validator(mode="after")
    def taken_fits(self):
        if self.taken > self.seats:
            raise ValueError("taken cannot exceed seats")
        return self

    @model_validator(mode="after")
    def waitlist_only_when_full(self):
        if self.waitlist and self.taken < self.seats:
            raise ValueError("no waitlist while seats remain")
        return self

print(Enrolment(seats=30, taken=30, waitlist=4))

for bad in [{"seats": 10, "taken": 12, "waitlist": 0},
            {"seats": 10, "taken": 5, "waitlist": 3}]:
    try:
        Enrolment.model_validate(bad)
    except ValidationError as e:
        print("%-40s %s" % (str(bad), e.errors()[0]["msg"]))'''),
    ],
    [
        "<code>mode=\"after\"</code> receives the finished model as <code>self</code> and must <strong>return self</strong>.",
        "<code>mode=\"before\"</code> receives the raw input for the whole model, is a <code>@classmethod</code>, and must return the data to validate.",
        "A model-level error has an empty <code>loc</code>, because it belongs to the object rather than any one field. Code that assumes <code>loc[0]</code> exists will break on it.",
        "Unlike <code>field_validator</code> with <code>info.data</code>, a model validator does not depend on declaration order &mdash; every field is already present.",
        "Validators run in definition order and the first raise stops the rest, so put cheap checks before expensive ones.",
        "Keep them pure. A model validator that queries a database makes validation an I/O operation and the model untestable on its own.",
    ],
    '''
title: model_validator: Rules That Span Fields
intro: The checks a per-field checker structurally can't make. The two modes that make them.

## Why a field validator is not enough

A field validator sees one field. Some rules cannot be checked that way, because they depend on two or more fields together. A start date must come before an end date. A password must match its confirmation. If a discount is present, a reason must be present too.

A model validator runs against the whole object, so it can compare fields with each other. It is the right tool for any rule that spans fields. It comes in two main flavours. One runs after the fields are validated, and sees clean, typed values. The other runs before, and sees the raw input.

This article starts with why a field validator is not enough. It covers the after mode first, since that is the one you will use most. It explains the empty location in the error, which is how a model-level failure shows up. Then it covers the before mode, where you can reshape the raw input. The last section shows how to set values from a model validator rather than only checking them. Together these cover the cross-field rules that real forms and APIs always seem to need.

These rules are common in forms, bookings and anything with a range. The article keeps each case small.

A `field_validator` receives one value. That is the right shape for most rules. It's structurally incapable of expressing a large and key class of them.

An end date must be after a start date. A discount must not exceed the price. Either an email or a phone number must be present. A waitlist only makes sense when each seat is taken. None of these is a statement about a single field. Each field is on their own fine. It's the mix that is wrong.

`info.data` looks like a way round this. It half is. It exposes fields checked *earlier*. This Means the rule only works if the fields happen to be declared in the right order and silently stops working when somebody reorders the class for tidiness. That isn't a foundation to build on.

`model_validator` is the tool built for the job.

## mode="after"

The common case. It runs once, after each field has been checked and converted, and receives the finished model:

```python
@model_validator(mode="after")
def ends_after_start(self):
    if self.ends_on <= self.starts_on:
        raise ValueError("ends_on must be after starts_on")
    return self
```

Three mechanics. It takes `self`, not `cls`. Isn't a classmethod. Which is the opposite of `field_validator` and catches people out. It must **return `self`**, and losing is the same silent failure as losing to return from a field checker. And by the time it runs, the fields are real Python objects. `self.ends_on` is a `date` and checking it works.

That last point is worth dwelling on. Because coercion has already happened, an after checker can compare, subtract and sort without any defensive conversion. The rule reads just like the sentence you'd say out loud.

## The empty location

An error raised here has `loc: ()` &mdash; an empty tuple.

That is correct: the failure belongs to the object, not to any single field. There's no one input to highlight. The problem is the link between two of them.

It's also the thing most likely to break error-handling code written before the first cross-field rule was added. Anything doing `err["loc"][0]` will raise `IndexError`. It will do so the first time somebody adds a checker like this. Long after the handler was written and tested.

Handle it by name. Group under a key like `"_form"`. Give the interface one spot to display an error that isn't attached to an input. each form library has a concept for this. The model just needs to feed it.

## mode="before"

A before checker receives the raw input for the entire model, before any field has been looked at. It's a classmethod. It returns the data that will then be checked most times.

Its main use is accepting a shape you didn't design:

```python
@model_validator(mode="before")
@classmethod
def accept_old_shape(cls, data):
    if isinstance(data, dict) and "name" in data:
        data = dict(data)
        data["title"] = data.pop("name")
    return data
```

This is the translation layer for a legacy payload, a third-party API with other names, or a version of your own format you no longer want in the model. The model stays clean and shows the shape you want. The adapter sits in one visible place.

Two rules, both the same as for field-level before checkers. Guard with `isinstance`. The input hasn't been checked and may not be a dict at all. And copy before mutating. `dict(data)`. Because modifying the caller's dict in place is a surprise no one enjoys debugging.

Use `before` sparingly. It runs before all. Any error it raises is reported without the field context that makes Pydantic errors handy. Complex logic there's hard to follow. For anything that is truly per-field, a field checker says more.

## Setting values, not just checking

An after checker can modify the model. This Makes it a way to derive one field from others:

```python
@model_validator(mode="after")
def fill_slug(self):
    if self.slug is None:
        object.__setattr__(self, "slug", self.title.lower().replace(" ", "-"))
    return self
```

The `object.__setattr__` is needed on a frozen model and is harmless else. On a mutable model a plain set works, though it will re-trigger check if `validate_assignment` is on.

Before reaching for this, ask whether the value is ever legitimately supplied by the caller. If it's. A slug that defaults from the title but can be overridden. This is right. If it never is. Is always derived, then it isn't really an input at all and `computed_field` is the better tool. That is the next module.

## Order, and short-circuiting

a few model checkers can coexist. They run in meaning order. The first to raise stops the rest.

That has a hands-on result: put the cheap, foundational checks first. If `taken > seats` is nonsense, there's no value in also checking a rule about the waitlist that assumes those numbers make sense. And the second error would only confuse the caller.

It also means model checkers don't build up errors the way field check does. Field errors all appear together. Model-level errors appear one at a time. If you want a caller to see each cross-field problem at once, you've to collect them yourself in a single checker and raise one error showing all of them.

## Keeping it pure

The strongest advice in this module: a model checker should decide using only the data in front of it.

The temptation is real. "Does this track exist?" is a check question. The answer is in a DB. Putting the query in a checker makes it run on each build, makes the model hopeless to test without a DB, turns a `ValidationError` into a possible timeout. Hides an I/O call one spot no one expects one.

The rule that keeps this clean: models check *shape and inner agreement*. The service layer checks *facts about the world*. A date range being backwards is shape. A track existing is a fact. They're other concerns and they fail differently. One is a 422, the other is arguably a 404.

## Choosing between the three tools

**A constraint** when the rule is a bound, a length or a pattern on one field. It reaches the schema.

**A field checker** when one field needs logic, or norming.

**A model checker** when the rule involves more than one field, or the shape of the whole payload.

Working down that list rather than up makes models where most rules are visible in the annotations and only the truly complex ones are in code.

## Collecting several problems at once

Model checkers stop at the first failure. This Means a caller fixing cross-field errors discovers them one at a time. Just the experience field check avoids.

If a few rules should report together, collect them in one checker:

```python
@model_validator(mode="after")
def check_all(self):
    problems = []
    if self.ends_on <= self.starts_on:
        problems.append("ends_on must be after starts_on")
    if self.seats < self.taken:
        problems.append("seats cannot be fewer than taken")
    if problems:
        raise ValueError("; ".join(problems))
    return self
```

It's less tidy than split checkers and it gives the caller all in one response. Which matters depends on whether a human is fixing a form or a service is failing a request.

## Validators and assignment

With `validate_assignment=True`, after checkers run again on each set.

That is often what you want. A cross-field rule should hold after a change, not only at build. It has two results worth knowing.

An costly checker now runs on each set, not once.

And an mid state may be invalid. Setting `starts_on` to a date after the current `ends_on` raises, though you were about to fix `ends_on` on the next line. There's no transaction. Each set is checked alone.

Where that bites, the functional approach is cleaner. Build a new model with `model_copy(update={...})` giving both fields at once, or make a fresh one. It's also a good arg for `frozen=True` on models with cross-field rules. If it can't be mutated, it can't pass through an invalid mid state.

## Inheritance

Model checkers are from parent. So A base can carry an rule that each subclass enforces.

A subclass redefining a checker with the same name replaces it. Give it a other name to have both. Note that the parent's runs first.

This makes a base model a fair home for a rule shared across a family. "no model in this system may have an end before its start". While each subclass adds its own.

## What belongs where, once more

The line worth holding, because it's the one people cross first.

A model checker answers: **is this object inside steady?** Dates in order, totals adding up, at least one contact method present. All answerable from the data in front of it.

A service answers: **is this true of the world?** Does the track exist, is the name taken, does this user have permission. All needing a thing the model can't see.

Keeping that line means models are testable with plain data, check can't make a network call. A `ValidationError` always means the payload was malformed rather than that a thing external was down. Those are three properties worth protecting.

## Summary

`model_validator(mode="after")` takes `self`, returns `self`, and sees each field already converted. The right place for any rule about links between fields. `mode="before"` is a classmethod taking raw input, for translating a payload shape.

Model-level errors carry an empty `loc`. This Your error handling needs to expect. checkers run in meaning order and stop at the first failure. And keep them pure. That checking a model never touches the world.

## A short checklist

Before writing one, three questions.

**Does the rule involve more than one field?** If not, a field checker or a constraint is more exact and gives a better error location.

**Can it be decided from the data alone?** If it needs a lookup, it belongs in the service layer, not here.

**Should the caller see each failure at once?** If so, collect them in a single checker rather than writing a few that stop at the first.

## What this buys

A model with cross-field rules is a model that can't exist in a nonsensical state. A cohort whose end precedes its start isn't merely flagged one spot. It can't be made.

That is a strong promise, and it's what makes the rest of the code simpler. each function receiving that model can stop checking. The object couldn't have been built if the check would have failed. The rule exists once, at the boundary, instead of being re-asserted defensively wherever the data travels.


## Mistakes people make

**Using `info.data` in a field checker for a cross-field rule.** It only exposes fields declared earlier. The rule works until somebody reorders the class for readability and then silently stops.

**Losing to return `self`.** The same silent failure as all over else in this library.

**Doing I/O.** A checker that queries a DB makes the model untestable without one, turns a `ValidationError` into a possible timeout. Hides a network call one spot no one expects one.

**Writing a few checkers when the caller needs each failure at once.** Model checkers stop at the first raise. A form with three cross-field problems reveals them one at a time. Collect them into one checker when they should be reported together.

**given `loc[0]` exists.** Model-level errors carry an empty `loc`. Error-handling code written before the first cross-field rule will raise `IndexError` the day one is added.

**Mutating in an after checker on a model with `validate_assignment`.** The set re-triggers check. This Re-runs the checker. Use `object.__setattr__`, or set the value in a `before` checker instead.

## Where the errors go

One hands-on result of the empty `loc` deserves a final mention. It shapes how the front end has to work.

A field error can be rendered beside its input. A model error can't. There's no single input it belongs to. each form needs one spot to display it. A banner above the fields, a summary at the top, a message near the submit button.

If that place doesn't exist, cross-field errors are either invisible or attached arbitrarily to whichever field the code happened to pick. Both are worse than a plain sentence in an obvious place.

It's a small piece of interface design that follows right from a modelling choice. It's easiest to get right by knowing it's coming.
''',
    [
        {"q": "What must an `after` model validator return?",
         "options": ["Nothing", "self", "A dict", "True"],
         "answer": 1,
         "why": "It receives the finished model and must return it. Forgetting is the same silent failure as forgetting to return from a field validator."},
        {"q": "What is the `loc` of an error raised by a model validator?",
         "options": ["The first field", "An empty tuple", "The model name", "It has none"],
         "answer": 1,
         "why": "The failure belongs to the object rather than any one field. Handling code that does `loc[0]` will raise IndexError the first time such a rule is added."},
        {"q": "Why not use `info.data` in a field validator for a cross-field rule?",
         "options": ["It is slower", "It only exposes fields declared earlier, so reordering the class breaks the rule", "It is deprecated", "It cannot raise"],
         "answer": 1,
         "why": "Fields validate in declaration order. A rule depending on that order is invisible to whoever later reorders the class for readability."},
        {"q": "Where does 'does this track exist in the database?' belong?",
         "options": ["A model validator", "A field validator", "The service layer, not the model", "A constraint"],
         "answer": 2,
         "why": "Models check shape and internal consistency using only the data. A validator doing I/O makes the model untestable, turns validation into a network call, and hides a query where nobody expects one."},
    ],
)


# ---------------------------------------------------------------------------
# 16. Computed fields
# ---------------------------------------------------------------------------
topic(
    "computed_fields",
    "Computed Fields",
    "Control",
    "Values derived from other fields that belong in the output but were never an "
    "input.",
    _svg(_box(14, 24, 46, 20, S) + _txt(37, 38, "minutes", M, 8) +
         _box(14, 50, 46, 20, S) + _txt(37, 64, "lessons", M, 8) +
         _arrow(64, 34, 84, 47) + _arrow(64, 60, 84, 47) +
         _box(88, 36, 58, 22, S, A) + _txt(117, 50, "pace", A, 8)),
    [
        ("A property is invisible to serialisation",
         "An ordinary <code>@property</code> works on the object and does not appear "
         "in <code>model_dump()</code>. Often that is right &mdash; sometimes it is "
         "not.",
         '''from pydantic import BaseModel

class Module(BaseModel):
    title: str
    minutes: int
    lessons: int

    @property
    def pace(self) -> float:
        return round(self.minutes / self.lessons, 1)

m = Module(title="Vectors", minutes=30, lessons=5)

print("on the object :", m.pace)
print("in the dump   :", m.model_dump())
print("in the json   :", m.model_dump_json())'''),

        ("computed_field puts it in the output",
         "Add the decorator and the value appears in every serialisation, while still "
         "being a normal property on the object.",
         '''from pydantic import BaseModel, computed_field

class Module(BaseModel):
    title: str
    minutes: int
    lessons: int

    @computed_field
    @property
    def pace(self) -> float:
        return round(self.minutes / self.lessons, 1)

m = Module(title="Vectors", minutes=30, lessons=5)

print("on the object :", m.pace)
print("in the dump   :", m.model_dump())
print("in the json   :", m.model_dump_json())'''),

        ("It is output only",
         "A computed field cannot be supplied. It is not an input, does not appear in "
         "the constructor, and is recomputed from the fields every time.",
         '''from pydantic import BaseModel, computed_field, ValidationError

class Module(BaseModel):
    minutes: int
    lessons: int

    @computed_field
    @property
    def pace(self) -> float:
        return round(self.minutes / self.lessons, 1)

m = Module(minutes=30, lessons=5)
print("computed:", m.pace)

# Supplying it is ignored (or rejected, with extra="forbid"):
m2 = Module(minutes=30, lessons=5, pace=999)
print("supplied:", m2.pace, "<- ignored; it is derived, not stored")

# It follows the fields:
m3 = Module(minutes=60, lessons=5)
print("recomputed:", m3.pace)'''),

        ("Describing it properly",
         "The return annotation becomes its type in the schema. Add a description and "
         "it documents itself like any other field.",
         '''import json
from pydantic import BaseModel, computed_field

class Module(BaseModel):
    title: str
    minutes: int

    @computed_field(description="Reading time with a 20% margin, in minutes.")
    @property
    def estimated_minutes(self) -> int:
        return round(self.minutes * 1.2)

m = Module(title="Vectors", minutes=10)
print("value :", m.estimated_minutes)
print("dump  :", m.model_dump())
print()

schema = m.model_json_schema(mode="serialization")
print("in the serialization schema:")
for name, spec in schema["properties"].items():
    print("  %-20s %-8s %s" % (name, spec.get("type"), spec.get("description", "")))'''),

        ("Excluding it when you do not want it",
         "It behaves like a field for <code>include</code> and <code>exclude</code>, "
         "so an internal calculation can be kept out of a public response.",
         '''from pydantic import BaseModel, computed_field

class Module(BaseModel):
    title: str
    minutes: int
    cost_pence: int

    @computed_field
    @property
    def hours(self) -> float:
        return round(self.minutes / 60, 2)

    @computed_field
    @property
    def margin(self) -> int:
        return self.cost_pence * 3

m = Module(title="Vectors", minutes=90, cost_pence=200)

print("everything :", m.model_dump())
print("public     :", m.model_dump(exclude={"cost_pence", "margin"}))
print("just hours :", m.model_dump(include={"title": True, "hours": True}))'''),

        ("Cost, and when not to use it",
         "It runs on every serialisation. That is fine for arithmetic and wrong for "
         "anything expensive &mdash; and it must never fail.",
         '''from pydantic import BaseModel, computed_field

calls = {"n": 0}

class Module(BaseModel):
    minutes: int
    lessons: int

    @computed_field
    @property
    def pace(self) -> float:
        calls["n"] += 1
        return round(self.minutes / self.lessons, 1)

m = Module(minutes=30, lessons=5)
m.model_dump(); m.model_dump(); m.model_dump_json()
print("serialisations: 3, property calls:", calls["n"])

# And the trap: a computed field that can raise breaks serialisation.
class Risky(BaseModel):
    minutes: int
    lessons: int

    @computed_field
    @property
    def pace(self) -> float:
        return self.minutes / self.lessons      # lessons could be 0

r = Risky(minutes=30, lessons=0)
try:
    r.model_dump()
except ZeroDivisionError as e:
    print()
    print("dump failed:", type(e).__name__, "-", e)
    print("A model that validated fine can no longer be serialised.")'''),
    ],
    [
        "A plain <code>@property</code> works on the object but never appears in <code>model_dump()</code>. <code>@computed_field</code> is what adds it to the output.",
        "The decorator goes <em>above</em> <code>@property</code>. The other order does not work.",
        "It is output-only: it cannot be passed to the constructor, is not validated, and is recalculated from the current field values each time.",
        "The return annotation is required &mdash; it becomes the field's type in the serialisation schema.",
        "It runs on <strong>every</strong> serialisation, so keep it cheap. There is no caching.",
        "A computed field that can raise turns a valid model into one that cannot be serialised. Guard the edge cases or use a plain property instead.",
    ],
    '''
title: Computed Fields: Derived Values in the Output
intro: Values found from other fields that belong in the response but were never an input.

## The gap it fills

Sometimes a value is not stored at all. It is worked out from other fields. A full name comes from first and last. A total comes from price and quantity. A model can compute these with a normal Python property, but a property does not appear when you dump the model to a dictionary or JSON.

A computed field fixes that. You mark a property with a decorator, and Pydantic includes it in the output and in the schema. The value is still calculated on demand. It is never accepted as input, which keeps the model honest about what the caller can set and what the model derives.

This article explains the gap that computed fields fill and the shape of the decorator. It makes the point that they are output only, and why that is the right design. You will see how they show up in the JSON Schema, and why there are two schemas for a model that has them, one for input and one for output. The last section covers how to leave them out of a dump when you do not want them. They are a small feature that removes a lot of repeated code.

Some values aren't data you receive. They're results of data you receive. A full name from a first and last. A total from a quantity and a price. A reading time from a word count. An `is_expired` flag from an expiry date and the clock.

Storing them as fields is wrong. They can then disagree with the values they came from. Accepting them from a caller is worse, because the caller can lie.

The obvious answer is a `@property`. It's half right. A property finds from the current values and can't drift. But it's invisible to output. `model_dump()` doesn't include it, `model_dump_json()` doesn't include it, and the schema doesn't know it exists. For a value that exists purely for inner use, that is fine. For one your API consumers need, it isn't.

`@computed_field` closes the gap: the value is derived, and it appears in the output.

## The shape

```python
@computed_field
@property
def pace(self) -> float:
    return round(self.minutes / self.lessons, 1)
```

Three mechanics.

**Decorator order.** `@computed_field` goes above `@property`. The reverse doesn't work, and the failure isn't self-explanatory.

**The return annotation is needed.** It turns the field's type in the output schema. Pydantic will complain if it's missing. It isn't merely docs.

**It reads the model.** Because it takes `self`, all on the model is on hand. And check has already happened. Those values are real converted types.

## Output only, and why that matters

A found field isn't an input. It doesn't appear in the constructor signature, it isn't checked. Passing it's skipped. Or rejected, if you've set `extra="forbid"`.

That skew is the whole point. The value is a function of the model. Allowing it to be supplied would allow it to be supplied *wrongly*. You'd have two sources of truth for one fact.

It also means the value is always current. Change `minutes` and `pace` changes with it. It's recomputed on access rather than stored. There's no stale-derived-value bug on hand. This Is the class of bug this feature drops.

## The schema, and the two modes

A found field appears in the **output** schema and not the check one. This Is just right. It's a thing you emit, never a thing you accept.

That gap surfaces in `model_json_schema(mode=...)`. The default, `mode="check"`, shows what the model accepts. Found fields are absent. `mode="output"` shows what it makes, and they're present.

For a FastAPI response model this is handled for you. The response schema is the output one. Found fields appear in the docs as fields consumers can expect. That is often the reason to reach for the feature in the first place.

You can pass `description`, `title` and `examples` to the decorator. They land in the schema like any other field's metadata. A derived value often needs a description more than a stored one does. The name alone rarely shows the formula.

## Excluding them

Found fields behave like fields for `include` and `exclude`:

```python
m.model_dump(exclude={"cost_pence", "margin"})
```

This is worth knowing because derived values are often the ones you don't want in a public response. A margin found from a cost is a just right fair inner field and an unfortunate thing to leak. It's easy to forget that adding a found field changes what each existing output emits.

That is truly a footgun: unlike a normal field. This You had to add to the model on purpose, a found field can be added for one inner purpose and silently appear in each API response the model feeds.

## The cost

A found field runs on **each** output. There's no caching.

For math on a couple of fields that is irrelevant. For anything heavier it isn't. The cost times. Serialising a list of a thousand models runs each found field a thousand times.

If a value is costly and truly needs to be in the output, find it once and store it in a real field. Accepting that you now own keeping it steady. `functools.cached_property` isn't a substitute here. It doesn't participate in output.

The rule: found fields are for cheap derivations. Math, string formatting, a compare, a lookup in a small dict. Anything that touches I/O or loops over data doesn't belong.

## The failure mode to guard against

This is the sharpest edge in the module, and it's easy to walk into.

A found field that can raise turns a valid model into one that can't be serialised.

```python
@computed_field
@property
def pace(self) -> float:
    return self.minutes / self.lessons     # lessons could be 0
```

`Module(minutes=30, lessons=0)` validates just right. each field is the right type and within its constraints. And then `model_dump()` raises `ZeroDivisionError`. Not a `ValidationError`, not at the boundary. At the moment you try to send a response.

The failure is far from the cause and it isn't a check error. None of the error handling you built for check catches it.

Two defences. Make the hopeless state hopeless: `lessons: int = Field(gt=0)` means the divisor can't be zero and the found field can't fail. Or handle the edge inside the property and return a thing sensible. The first is better. It fixes the model rather than the symptom.

The general principle: a found field should be **total**. Defined for each mix of values the model permits. If it isn't, either the model is too permissive or the value isn't really a found field.

## Computed field, property, or stored?

**Plain `@property`** when the value is for inner use and shouldn't be serialised. Most helper methods on a model are this.

**`@computed_field`** when the value is derived, cheap, total, and consumers need it in the output.

**A stored field** when the value is costly, when it must be preserved as it was at a point in time (a price at the moment of sale, not the current price), or when it truly is an input.

That middle case &mdash; historical values &mdash; is worth flagging. A found field always reflects the *current* inputs. If you need what the total was when the order was placed, that is data, not a derivation. It belongs in a column.

## Naming and the schema

A found field's name is the method name. It appears in the output just as written. That is worth a moment's care. Renaming it later is a breaking change for each consumer.

The return annotation isn't optional, and it does real work. It turns the field's type in the output schema. Consumers and made clients know what to expect.

A `description` in the decorator is more valuable here than on plain fields. `total` doesn't explain whether tax is included. `minutes` doesn't explain the margin applied. The name is a label. Derived values often need a sentence.

## Serialisation aliases work too

Found fields accept `alias`. This Matters if the rest of your API is camelCase:

```python
@computed_field(alias="estimatedMinutes")
@property
def estimated_minutes(self) -> int:
    ...
```

Without it, a model whose plain fields are aliased will emit one stubbornly snake_case key among them. An `alias_generator` on the model doesn't apply to found fields. This is one place the whole-model rule needs a per-field top-up.

## Ordering in the output

Found fields appear after regular fields in the serialised output, in the order they're defined.

That is stable and predictable, and worth knowing if anything downstream cares about key order. A snapshot test, a diff, a human reading a log. You can't interleave them with declared fields.

## A pattern: flags derived from state

One of the most handy uses is turning inner state into a flag a consumer can act on:

```python
@computed_field
@property
def is_expired(self) -> bool:
    return self.expires_at < datetime.now(timezone.utc)
```

The consumer doesn't have to know your expiry rules, parse a date, or get the timezone right. They get a boolean.

Two cautions with this exact shape. It depends on the clock. Serialising the same model twice can give other output. Which breaks snapshot tests and can surprise a cache. And it makes the model's output non-fixed. This Is a property worth being deliberate about rather than discovering.

If determinism matters, pass the link time in rather than reading the clock, or find the flag in the layer that is making the response.

## Summary of the trade

A found field buys you a derived value in the output that can never disagree with its inputs, given in the schema, with no storage and no sync.

It costs a function call on each output. It demands that the function be total. Defined for each state the model permits. Because a failure there breaks output of an object that checked just right.

Cheap, total, and truly derived. Those three rules are the whole rule.

## Summary

`@computed_field` above `@property`, with a return annotation. The value is derived, output-only, recomputed each time. Appears in the output schema.

Keep them cheap, because they run on each dump. Keep them total, because a found field that raises breaks output of a model that checked just right. And note that adding one changes the output of each output the model already feeds. Including the public ones.

## One more use worth knowing

A found field is a good place to expose a value the model stores in a form consumers shouldn't have to understand.

Storage often wants one shape and a consumer wants another. A duration in seconds inside, minutes in the response. A status code inside, a readable label outside. Split first and last names, a display name in the output.

The found field bridges that without duplicating state. The stored field remains the single source of truth. The derived view is sure to agree with it because it's found from it.

This is a better pattern than storing both. This Is where the two eventually disagree and no one can say which is right.


## Mistakes people make

**Writing one that can raise.** A division by a field that might be zero turns a just right valid model into one that can't be serialised. And the failure isn't a `ValidationError`. None of your check error handling catches it. Constrain the inputs so the hopeless state can't occur.

**Putting costly work in one.** It runs on each output with no caching. Serialising a thousand models runs it a thousand times. Anything touching I/O or looping over data doesn't belong.

**Losing the return annotation.** It isn't docs. It's the field's type in the output schema, and Pydantic needs it.

**Reading the clock.** A field derived from `datetime.now()` makes output non-fixed. This Breaks snapshot tests and surprises caches. Pass the link time in, or find the flag where the response is made.

**Not aliasing it.** An `alias_generator` on the model doesn't reach found fields. A camelCase API ends up with one stubbornly snake_case key. The decorator takes `alias` for just this.

**Adding one without checking what already consumes the model.** Unlike a regular field. This You on purpose added to a schema, a found field written for one inner purpose at once appears in each existing output. Including the public ones.

## Deciding, in one line

Cheap, total, and truly derived.

Cheap, because it runs on each output and there's no caching. Total, because a failure breaks the output of a model that checked just right. truly derived, because if a caller could fairly supply it, it's an input with a default rather than a found value.

Fail any of those three and the answer is a thing else. A stored field, a plain property, or a value found in the layer making the response.
''',
    [
        {"q": "Why does a plain `@property` not appear in `model_dump()`?",
         "options": ["It is a bug", "Properties are not fields; only `@computed_field` adds one to the output", "It needs an annotation", "It does appear"],
         "answer": 1,
         "why": "A property is ordinary Python and Pydantic does not serialise it. `@computed_field` is the opt-in that makes a derived value part of the model's output."},
        {"q": "What happens if you pass a computed field to the constructor?",
         "options": ["It overrides the calculation", "It is ignored, or rejected with extra=forbid", "It raises always", "It is stored"],
         "answer": 1,
         "why": "Computed fields are output-only. Allowing them as input would create a second source of truth for a value that is a function of the model."},
        {"q": "A computed field divides by another field that can be zero. When does this fail?",
         "options": ["At validation, as a ValidationError", "At serialisation, as a ZeroDivisionError", "Never", "At class definition"],
         "answer": 1,
         "why": "The model validates fine - every field is the right type. The failure arrives at `model_dump()` and is not a ValidationError, so validation error handling does not catch it."},
        {"q": "Which schema mode shows computed fields?",
         "options": ["validation", "serialization", "Both", "Neither"],
         "answer": 1,
         "why": "They describe what the model emits, never what it accepts, so they appear in `model_json_schema(mode=\"serialization\")` - which is what a FastAPI response model uses."},
    ],
)


# ---------------------------------------------------------------------------
# 17. model_config
# ---------------------------------------------------------------------------
topic(
    "model_config",
    "model_config",
    "Control",
    "The settings that change how a whole model behaves - extra keys, mutability, "
    "assignment checking and string handling.",
    _svg(_box(18, 18, 124, 56, S) + _txt(80, 32, "model_config", A, 9) +
         _txt(80, 46, "extra  frozen", M, 8) +
         _txt(80, 60, "validate_assignment", M, 8)),
    [
        ("Unknown keys are ignored by default",
         "Extra keys in the input are silently dropped. That is forgiving and it hides "
         "typos, which is why <code>extra=\"forbid\"</code> exists.",
         '''from pydantic import BaseModel, ConfigDict, ValidationError

class Lenient(BaseModel):
    title: str
    minutes: int

class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    minutes: int

payload = {"title": "Vectors", "minutes": 8, "minuets": 99}   # typo

m = Lenient.model_validate(payload)
print("ignored :", m.model_dump(), "<- the typo vanished silently")

try:
    Strict.model_validate(payload)
except ValidationError as e:
    err = e.errors()[0]
    print("forbid  :", err["type"], "->", err["loc"], err["msg"])'''),

        ("Or keep them",
         "<code>extra=\"allow\"</code> stores unknown keys on the model. Useful for a "
         "passthrough payload; a liability everywhere else.",
         '''from pydantic import BaseModel, ConfigDict

class Passthrough(BaseModel):
    model_config = ConfigDict(extra="allow")
    title: str

m = Passthrough(title="Vectors", source="partner-api", trace_id="abc123")

print("declared :", m.title)
print("extra    :", m.model_extra)
print("dumped   :", m.model_dump())
print()
print("attribute access works:", m.source)'''),

        ("Assignment is not checked unless you ask",
         "Validation happens at construction. Assigning afterwards writes whatever you "
         "give it &mdash; until <code>validate_assignment</code> is on.",
         '''from pydantic import BaseModel, ConfigDict, ValidationError

class Loose(BaseModel):
    minutes: int

class Checked(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    minutes: int

a = Loose(minutes=8)
a.minutes = "not a number"
print("loose   :", repr(a.minutes), "<- an int field holding a str")

b = Checked(minutes=8)
b.minutes = "12"
print("checked :", repr(b.minutes), "<- coerced on assignment")

try:
    b.minutes = "ages"
except ValidationError as e:
    print("checked :", e.errors()[0]["msg"])'''),

        ("Frozen models are hashable",
         "<code>frozen=True</code> forbids assignment entirely and lets the model be a "
         "dict key or set member.",
         '''from pydantic import BaseModel, ConfigDict, ValidationError

class Point(BaseModel):
    model_config = ConfigDict(frozen=True)
    x: int
    y: int

p = Point(x=1, y=2)
print("value:", p)

try:
    p.x = 5
except ValidationError as e:
    print("frozen:", e.errors()[0]["type"])

seen = {Point(x=1, y=2), Point(x=1, y=2), Point(x=3, y=4)}
print()
print("in a set  :", len(seen), "unique points")
print("as a key  :", {Point(x=1, y=2): "origin-ish"})'''),

        ("String handling for form data",
         "Three settings remove a pile of trivial validators when the input comes from "
         "humans.",
         '''from pydantic import BaseModel, ConfigDict

class Raw(BaseModel):
    email: str
    code: str

class Tidy(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True,
                              str_to_lower=True)
    email: str
    code: str

messy = {"email": "  ADA@VizLearn.IN  ", "code": "  ABC123 "}

print("raw  :", Raw.model_validate(messy).model_dump())
print("tidy :", Tidy.model_validate(messy).model_dump())
print()
print("str_min_length works too, as a model-wide floor:")

class NoBlanks(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=1)
    title: str

try:
    NoBlanks(title="   ")
except Exception as e:
    print("  blank title:", type(e).__name__)'''),

        ("Reading from objects, not just dicts",
         "<code>from_attributes</code> lets a model validate anything with matching "
         "attributes &mdash; which is how a model reads an ORM row.",
         '''from pydantic import BaseModel, ConfigDict, ValidationError

class Row:                       # pretend this came from a database
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes

class Plain(BaseModel):
    title: str
    minutes: int

class FromObj(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    minutes: int

row = Row("Vectors", 8)

try:
    Plain.model_validate(row)
except ValidationError as e:
    print("without :", e.errors()[0]["type"])

print("with    :", FromObj.model_validate(row))
print()
print("In Pydantic v1 this setting was called orm_mode.")'''),
    ],
    [
        "<code>extra</code> takes <code>\"ignore\"</code> (the default), <code>\"forbid\"</code> or <code>\"allow\"</code>. Forbid catches typos in keys; the default silently drops them.",
        "Validation runs at construction only. <code>validate_assignment=True</code> extends it to later assignments.",
        "<code>frozen=True</code> blocks assignment and makes the model hashable, so it can be a dict key or live in a set.",
        "<code>str_strip_whitespace</code>, <code>str_to_lower</code> and <code>str_min_length</code> apply to every string field and remove a lot of trivial validators.",
        "<code>from_attributes=True</code> lets <code>model_validate</code> read attributes off any object &mdash; the setting called <code>orm_mode</code> in v1.",
        "Config is inherited, so a base model with your house settings gives every subclass the same behaviour.",
    ],
    '''
title: model_config: Settings That Change the Whole Model
intro: Extra keys, mutability, set checking and string handling - the switches worth knowing.

## Where behaviour lives

Each model has settings that change how it behaves as a whole. Should it reject keys it does not know? Should it trim whitespace from every string? Should it allow its fields to be changed after creation? Those are questions about the model, not about a single field.

The answers live in model_config, a small dictionary on the class. You set it once, and it applies to every field. It is where Pydantic keeps its switches, and a handful of them come up in nearly every project.

This article explains where behaviour lives and how to read the options. It spends the most time on the extra setting, which decides what happens to keys you did not declare. It covers the fact that validation happens once, when the object is created, and what that means for later changes. It then looks at the frozen setting, which is the other answer to the problem of mutation. Along the way you will see which settings are worth knowing by heart and which you can look up when you need them. After this, the model stops being a fixed thing and becomes something you can tune.

Think of the config as the control panel for a model. You rarely need all of it, but a few switches matter a great deal. Some protect you from typos in incoming data. Some save you from cleaning strings by hand. Some make an object safe to share, because it can no longer change. The article names the ones worth remembering and shows what each does to real input. You will also see how config is inherited, so one base class can set the rules for a whole family of models. Learning the handful that matter will save you from writing the same defensive code again and again. Reach for this article whenever a model behaves in a way you did not expect.

all so far has been per field. `model_config` is per model. A `ConfigDict` assigned in the class body that changes how the whole thing behaves.

```python
class Module(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    title: str
```

In Pydantic v1 this was an inner `class Config`. That still works and is deprecated. It's the clearest signal that a tutorial predates v2.

There are a lot of settings. These are the ones that come up constantly.

## extra: what to do with keys you did not declare

The default is `"skip"` &mdash; unknown keys are silently dropped.

That is forgiving, and it hides mistakes. A caller sending `minuets` instead of `minutes` gets no error and no field. The model is built with what default `minutes` has, and the bug surfaces later as a value that is inexplicably wrong.

`extra="forbid"` rejects them:

```python
model_config = ConfigDict(extra="forbid")
```

Now the typo is an error naming the offending key. For an inner API, a config file, or anything where you control both ends, this is almost always the better default. It converts a silent misunderstanding into an direct one.

The arg for `"skip"` is forward match on a public API. A client sending fields from a newer version shouldn't break against an older server. That is a real consideration. It applies to *your* API's request models rather than to each model in your code.

`extra="allow"` keeps unknown keys, storing them on the model and exposing them through `model_extra`. It's right for a genuine passthrough. A webhook body you forward, an envelope whose payload you don't own. all over else it turns your model into a dict with extra steps. Loses the promise that the fields on the object are the fields you declared.

## Validation happens once

This surprises people, and it's worth being clear about.

A model is checked when it's made. Assigning to an field later is a plain Python set: no checking, no coercion.

```python
m = Module(minutes=8)
m.minutes = "not a number"      # allowed, and now the field is a string
```

The thinking is speed &mdash; most models are built, read and discarded. Checking each set would be work for a case that rarely arises.

`validate_assignment=True` turns it on. sets are then checked and coerced like constructor args. `m.minutes = "12"` gives you `12` and `m.minutes = "ages"` raises.

Turn it on for any model that is truly mutated after build, above all one holding config or building up state. It costs a little per set and drops a class of bug where a model's declared types quietly stop being true.

Note that it also makes any `model_validator(mode="after")` run again on each set. This Is often what you want and is worth knowing if those checkers are costly.

## frozen: the other answer to mutation

`frozen=True` forbids set altogether. An attempt raises a `ValidationError` with type `frozen_instance`.

It also makes the model **hashable**. It can be a dict key or a set member. Which unlocks a lot of plain Python that mutable models can't do.

For checked data that arrives from outside and is then only read, frozen is the right default and is under-used. It drops the question "did anything change this?" fully, it makes the object safe to share across threads or pass anywhere without defensive copying. It makes the intent clear.

`model_copy(update={...})` still works on a frozen model. Making a modified version is one line. That is the functional-update pattern. It's often clearer than mutation anyway.

Single fields can be frozen with `Field(frozen=True)` when only part of the model should be fixed. An id that must never change while the rest of the record can.

## String settings for human input

Three settings that apply to each string field:

`str_strip_whitespace=True` strips leading and trailing whitespace. For form data this is nearly always correct. It drops a pile of one-line checkers.

`str_to_lower=True` and `str_to_upper=True` norm case. handy for emails, codes and identifiers. Wrong for anything with display text. Apply it to models that are all identifiers rather than reaching for it globally.

`str_min_length=1` sets a floor for each string. Mixed with stripping, this is the compact way to say "no blank strings anywhere in this model". This Is a rule most form models want and few state.

## from_attributes: reading objects

By default `model_validate` expects a mapping. `from_attributes=True` lets it read fields off any object:

```python
class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    minutes: int

ModuleOut.model_validate(orm_row)
```

This is how a model turns a DB row into a response. It recurses. A row with related objects turns nested models without any manual conversion.

It was `orm_mode` in v1. This Is the name most existing material uses.

Two cautions. It reads fields. So A lazy-loading ORM link will be *loaded* when the model touches it. Which is how a single output quietly turns fifty queries. And it will read any field matching a field name, so a model with a field called `password_hash` pointed at a user row will faithfully put the hash in your response. Output models should list only what may be seen.

## A few more worth knowing

`populate_by_name=True` lets a field be filled by either its alias or its Python name. It pairs with aliases and gets a module of its own next tier.

`use_enum_values=True` stores the value rather than the enum member. It makes dumps simpler and loses the member's action. Often the `str, Enum` mixin is the better answer.

`validate_default=True` checks default values, which are else trusted.

`arbitrary_types_allowed=True` permits fields of types Pydantic knows nothing about, checked only by `isinstance`. It's an escape hatch for wrapping a third-party object. A sign you might want a custom type instead.

## Config is inherited

A base model's config applies to each subclass, and a subclass can replace single settings.

That makes a house base model a truly good pattern:

```python
class Base(BaseModel):
    model_config = ConfigDict(extra="forbid",
                              str_strip_whitespace=True,
                              validate_assignment=True)
```

each model in the code takes from from it and gets the same defaults, decided once. It's much better than the same `ConfigDict` copied into forty classes, four of which will end up other for no reason anybody remembers.

## Suggested defaults

For **request models** on a public API: `extra="skip"` for forward match, `str_strip_whitespace=True`.

For **inner and config models**: `extra="forbid"`. A typo is an error rather than a mystery.

For **checked data that is then only read**: `frozen=True`.

For **anything mutated after build**: `validate_assignment=True`.

## Settings that catch mistakes

Three more worth knowing because each closes a exact hole.

`validate_default=True` checks default values. This Are else trusted. A mistyped default sits silently until a thing downstream does math on a string. Worth turning on for models whose defaults come from constants defined elsewhere.

`revalidate_instances="always"` re-validates a model instance passed into another model. By default an object that is already the right class is accepted as-is, on the fair assumption it was checked when built. If it was mutated later without `validate_assignment`, that assumption is wrong. This setting closes the gap at the cost of re-running check.

`ser_json_timedelta` and `ser_json_bytes` control how those two types serialise. This Matters when a consumer expects seconds rather than an ISO duration.

## Protected namespaces

By default Pydantic reserves the `model_` prefix and warns if you declare a field starting with it. That is where its own methods live &mdash; `model_dump`, `model_validate`, `model_fields`.

That is a genuine problem if your domain has fields like `model_name` or `model_version`. This Is common in anything ML-adjacent.

`protected_namespaces=()` turns the warning off, and `protected_namespaces=("model_config",)` narrows it. Be aware that a field truly named `model_dump` would shadow the method. The warning is doing real work. Disable it on purpose rather than to silence noise.

## Where to set config

Three places, in growing order of scope.

On the class, as `model_config = ConfigDict(...)`. clear and local.

On a shared base model, from parent by all. Best for house rules.

As a keyword in the class meaning. `class Module(BaseModel, frozen=True)`. Which is compact and less discoverable.

For a code of any size, the base model is the answer. One file states the rules, each model follows them. Changing a rule is one edit rather than forty.

## Config and inheritance

Config merges rather than replaces. A subclass setting one key keeps its parent's other settings. This Is what makes the base-model pattern hands-on.

That also means an from parent setting can be surprising in a subclass that didn't ask for it. If a base sets `extra="forbid"` and a subclass truly needs passthrough, it must say so by name. Which is the right default. Silently permissive is worse than by name permissive.

## A worked house base

```python
class Base(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
```

Five choices, made once. Typos in keys are errors. Whitespace never reaches a field. sets are checked. Fields accept either spelling. The whole API speaks camelCase.

each model taking from from that is steady with every other. A new developer takes from the rules without being told them.

The one thing to avoid is a base so opinionated that half the models replace half of it. If a setting is wrong for a third of your models, it doesn't belong in the shared base.

## Summary

`model_config` is where model-wide action is decided. The four that matter most: `extra` for unknown keys, `validate_assignment` for mutation, `frozen` for immutability and hashability. The `str_*` family for human input.

Set them on purpose rather than by default, put your house settings on a shared base. Note that the two most common silent bugs in this area. An skipped typo in a key and an unvalidated set. Are both one config entry away from being loud.

## The short version

Four settings account for most of the value.

`extra="forbid"` turns a typo in a key from a silent nothing into a named error. Set it anywhere you control both ends.

`validate_assignment=True` extends check past build. So A model's declared types stay true for its whole life.

`frozen=True` makes checked data immutable and hashable. This Is the right shape for anything that arrives from outside and is then only read.

`str_strip_whitespace=True` drops a group of trivial checker and a group of trivial bug.

Put them on a shared base, decide them once. Let each model in the code inherit the same rules.


## Mistakes people make

**Leaving `extra` at its default where you control both ends.** A typo in a key makes no error, no field and a value that silently falls back to a default. `extra="forbid"` turns a mystery into a message.

**given set is checked.** It isn't. A model built right can hold anything at all a moment later. The declared types quietly stop being true.

**Copying the same `ConfigDict` into forty classes.** They drift. Four of them end up other for no reason anybody remembers. A shared base makes the rule one edit.

**Using `from_attributes` on an output model without listing fields carefully.** It reads what field matches a field name. A model pointed at a user row will faithfully serialise a password hash. It also triggers lazy ORM links. This Is how one output turns fifty queries.

**Silencing the protected-namespace warning reflexively.** A field truly named `model_dump` would shadow the method. Disable the warning on purpose for a domain that needs `model_` names, not to quieten noise.

**Building a base so opinionated that half the models replace it.** If a setting is wrong for a third of your models, it isn't a house rule and doesn't belong in the shared base.

## What it is really for

Config is where a code records the choices it has made about its own data.

Whether an surprise key is a mistake or a courtesy. Whether checked objects may change. Whether the wire speaks camelCase. Whether a blank string is a value.

Those are real choices, and each code makes them. Often silently, differently in other files, and rediscovered by each new person. Writing them once, on a shared base, turns a set of accidents into a rule.
''',
    [
        {"q": "What does a model do by default with a key it did not declare?",
         "options": ["Raises", "Silently ignores it", "Stores it", "Warns"],
         "answer": 1,
         "why": "The default is `extra=\"ignore\"`. A typo in a key produces no error and no field, so the bug appears later as a value that is inexplicably a default."},
        {"q": "Is `m.minutes = \"not a number\"` validated by default?",
         "options": ["Yes", "No - validation happens at construction only", "Only for ints", "It raises AttributeError"],
         "answer": 1,
         "why": "Assignment is plain Python unless `validate_assignment=True` is set. Without it, a model's declared types can quietly stop being true."},
        {"q": "What does `frozen=True` give you besides blocking assignment?",
         "options": ["Faster validation", "Hashability, so the model can be a dict key or set member", "Automatic caching", "Stricter types"],
         "answer": 1,
         "why": "Immutability makes the model hashable, which unlocks ordinary Python that mutable models cannot do - and `model_copy(update=...)` still produces modified versions."},
        {"q": "What is the risk of `from_attributes=True` on an output model?",
         "options": ["None", "It reads any matching attribute, so undeclared-but-named fields like password_hash can reach the response, and lazy relations get loaded", "It is slow", "It breaks nesting"],
         "answer": 1,
         "why": "It faithfully reads whatever attribute matches a field name, and touching a lazy ORM relationship triggers queries. Output models should list only what may be seen."},
    ],
)


# ---------------------------------------------------------------------------
# 18. Annotated and custom types
# ---------------------------------------------------------------------------
topic(
    "annotated_and_custom_types",
    "Annotated and Custom Types",
    "Control",
    "Naming a constrained type once and reusing it - the habit that stops the same "
    "rule being copied into six models.",
    _svg(_box(20, 20, 120, 22, S, A) + _txt(80, 34, "Minutes = int + gt=0", A, 8) +
         _arrow(50, 46, 50, 58) + _arrow(110, 46, 110, 58) +
         _box(20, 60, 52, 18, S) + _txt(46, 73, "Module", M, 8) +
         _box(88, 60, 52, 18, S) + _txt(114, 73, "Lesson", M, 8)),
    [
        ("The same rule, written twice",
         "Two models needing the same constrained field is where duplication starts. "
         "It is fine at two and a problem at six.",
         '''from pydantic import BaseModel, Field

class Module(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9_]+$")
    minutes: int = Field(gt=0, le=180)

class Lesson(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9_]+$")     # copied
    minutes: int = Field(gt=0, le=180)             # copied

print(Module(slug="dot_product", minutes=11))
print(Lesson(slug="direction", minutes=4))
print()
print("Two definitions of one rule. Change it and you must remember both.")'''),

        ("Annotated names the type",
         "<code>Annotated[T, Field(...)]</code> is a real type. Give it a name and the "
         "rule exists once.",
         '''from typing import Annotated
from pydantic import BaseModel, Field, ValidationError

Slug = Annotated[str, Field(pattern=r"^[a-z0-9_]+$")]
Minutes = Annotated[int, Field(gt=0, le=180)]

class Module(BaseModel):
    slug: Slug
    minutes: Minutes = 10

class Lesson(BaseModel):
    slug: Slug
    minutes: Minutes

print(Module(slug="dot_product"))
print(Lesson(slug="direction", minutes=4))

for cls, bad in [(Module, {"slug": "Dot Product"}), (Lesson, {"slug": "x", "minutes": 0})]:
    try:
        cls.model_validate(bad)
    except ValidationError as e:
        print("%-7s %s" % (cls.__name__, e.errors()[0]["msg"]))'''),

        ("Defaults read better this way",
         "With <code>Annotated</code> the constraint lives with the type and the "
         "default sits where defaults normally sit.",
         '''from typing import Annotated
from pydantic import BaseModel, Field

class Tangled(BaseModel):
    # constraint and default in one call - which part is which?
    minutes: int = Field(default=10, gt=0, le=180)

class Clear(BaseModel):
    # the type carries the rule; the default is just a default
    minutes: Annotated[int, Field(gt=0, le=180)] = 10

print(Tangled())
print(Clear())
print()
print("Same behaviour. The second reads as 'a Minutes, defaulting to 10'.")'''),

        ("AfterValidator: logic inside a type",
         "A validator can be part of the type itself, so the rule travels with it "
         "instead of being a method on one model.",
         '''from typing import Annotated
from pydantic import BaseModel, AfterValidator, ValidationError

def must_be_known(v: str) -> str:
    known = {"maths", "python", "dsa", "ml"}
    if v not in known:
        raise ValueError("unknown track %r; try %s" % (v, ", ".join(sorted(known))))
    return v

Track = Annotated[str, AfterValidator(must_be_known)]

class Module(BaseModel):
    track: Track

class Enrolment(BaseModel):
    track: Track          # same rule, no duplicated method

print(Module(track="maths"))
print(Enrolment(track="dsa"))

try:
    Enrolment(track="astrology")
except ValidationError as e:
    print("refused:", e.errors()[0]["msg"])'''),

        ("BeforeValidator normalises inside the type",
         "Pair a before-validator with a constraint and the type both cleans and "
         "checks &mdash; every model that uses it gets both.",
         '''from typing import Annotated
from pydantic import BaseModel, BeforeValidator, Field, ValidationError

def to_slug(v):
    if isinstance(v, str):
        return "_".join(v.strip().lower().split())
    return v

Slug = Annotated[str, BeforeValidator(to_slug), Field(pattern=r"^[a-z0-9_]+$")]

class Module(BaseModel):
    slug: Slug

print(Module(slug="  The Chain   RULE "))
print(Module(slug="dot_product"))

try:
    Module(slug="chain-rule!")          # normalised, then still invalid
except ValidationError as e:
    print("refused:", e.errors()[0]["msg"])'''),

        ("What ships already",
         "Pydantic includes a set of these. Use them where they fit rather than "
         "rebuilding the same thing.",
         '''from pydantic import (BaseModel, PositiveInt, NonNegativeInt, StrictInt,
                      AwareDatetime, ValidationError)

class Stats(BaseModel):
    views: NonNegativeInt          # >= 0
    minutes: PositiveInt           # > 0
    user_id: StrictInt             # no "42"

print(Stats(views=0, minutes=8, user_id=42))

for bad in [{"views": -1, "minutes": 8, "user_id": 1},
            {"views": 0, "minutes": 0, "user_id": 1},
            {"views": 0, "minutes": 8, "user_id": "1"}]:
    try:
        Stats.model_validate(bad)
    except ValidationError as e:
        print("%-42s %s" % (str(bad), e.errors()[0]["type"]))'''),
    ],
    [
        "<code>Annotated[T, Field(...)]</code> is a type. Bind it to a name and the rule is defined once and reused everywhere.",
        "With <code>Annotated</code> the default sits outside the type &mdash; <code>Annotated[int, Field(gt=0)] = 10</code> &mdash; which reads better than tangling both into one <code>Field</code> call.",
        "<code>AfterValidator</code> and <code>BeforeValidator</code> put logic inside the type, so the rule travels with it rather than being a method on one model.",
        "Metadata composes left to right: a before-validator runs, then coercion, then constraints, then an after-validator.",
        "Pydantic ships <code>PositiveInt</code>, <code>NonNegativeInt</code>, <code>StrictInt</code>, <code>AwareDatetime</code> and others &mdash; use them rather than rebuilding them.",
        "A named type is also better documentation: <code>slug: Slug</code> says what the field is; a raw regular expression makes the reader work it out.",
    ],
    '''
title: Annotated and Custom Types: Define the Rule Once
intro: The habit that stops the same constraint being copied into six models.

## The duplication problem

Suppose three models all have a field that holds a positive amount of money. You could repeat the same constraints in each one. That works until the rule changes, and then you have to find and fix every copy. The duplication is the problem, not the rule.

Annotated lets you attach Pydantic rules to a type once and give the result a name. You write the name wherever you need it. The rule lives in one place, the models read better, and the type tells the reader what the field is for.

This article starts with the duplication problem and shows how Annotated solves it. It explains why the result reads better too, since a name like PositiveAmount says more than a bare number. Then it goes further and puts logic into the type, with validators that travel with it. You will see the order in which the pieces run when you stack several of them. The aim is to leave you with a small library of your own types, so the rules of your domain are written down once and used everywhere.

This is the article to read when your models start to feel repetitive. A project with twenty models often has the same five rules written out a hundred times. That is a maintenance problem waiting to happen. One rule changes, three copies get updated, and the fourth is forgotten. A named type fixes that for good. It also gives your team a shared vocabulary, so a field called Slug or Percentage means the same thing everywhere it appears. The article builds up from a bare constraint to a type with its own logic, one small step at a time. By the end you will have a pattern you can copy into any codebase you work on, whatever its size, with very little ceremony.

Every step is small, and each one builds directly on the last.

You write a slug field with a pattern. Then another model needs a slug. The pattern is copied. Then a third. Six months later the rule changes to permit hyphens. Four of the six get updated.

This is the most plain form of drift there's. It doesn't need a clever answer. It needs the rule to exist once.

## Annotated is the mechanism

`Annotated[T, ...]` is standard `typing`. It means "this is a `T`, with extra metadata attached". Static type checkers see straight through to the `T` while libraries can read the metadata.

Pydantic reads it:

```python
Slug = Annotated[str, Field(pattern=r"^[a-z0-9_]+$")]
Minutes = Annotated[int, Field(gt=0, le=180)]
```

`Slug` is now a type. Use it in any model:

```python
class Module(BaseModel):
    slug: Slug
    minutes: Minutes = 10
```

One meaning, each use site steady, and one place to change it.

## It reads better, too

Beyond reuse, there's a readability arg that applies even to a type used once.

`slug: str = Field(pattern=r"^[a-z0-9_]+$")` tells the reader this is a string and then makes them parse a regular formula to learn anything more. `slug: Slug` tells them what the field *is*. If they need the details, the meaning is one jump away and has a name attached.

The default placement is better as well. Compare:

```python
minutes: int = Field(default=10, gt=0, le=180)
minutes: Annotated[int, Field(gt=0, le=180)] = 10
```

Both behave the same way. The second splits the two concerns. What kind of value this is. What it defaults to. And reads as a sentence: a `Minutes`, defaulting to 10.

## Putting logic in the type

Constraints aren't the only thing that can live in an `Annotated`. checkers can too. This Means a rule needing actual code can still be part of a reusable type rather than a method bolted to one model.

```python
def must_be_known(v: str) -> str:
    if v not in KNOWN_TRACKS:
        raise ValueError("unknown track %r" % v)
    return v

Track = Annotated[str, AfterValidator(must_be_known)]
```

each model with a `Track` field now enforces it. Without this, the same `@field_validator` gets copied into each model. This Is the first problem with extra steps.

`BeforeValidator` does the same at the other end of the pipeline. This Makes it the tool for scaling:

```python
Slug = Annotated[str, BeforeValidator(to_slug), Field(pattern=r"^[a-z0-9_]+$")]
```

That type cleans its input and then checks it. Any model using it gets both actions, and neither is written twice.

There's also `WrapValidator`, which wraps the whole check step and can catch and replace failures. It's the most powerful and least often needed. Reach for it when you want to supply a fallback rather than pass an error.

## The order things run in

With a few pieces of metadata, the pipeline is worth knowing:

A `BeforeValidator` runs first, on the raw input. Then coercion to the base type. Then constraints from `Field`. Then an `AfterValidator`, on the final value.

So `Annotated[str, BeforeValidator(to_slug), Field(pattern=...)]` norms `"  The Chain RULE "` into `the_chain_rule` and *then* checks it against the pattern. Written the other way round, the pattern would reject the first before anything cleaned it.

Multiple checkers of the same kind run in the order they appear.

## What ships already

Before building your own, check what exists. Pydantic includes a good set:

`PositiveInt`, `NegativeInt`, `NonNegativeInt`, `NonPositiveInt`, and the `Float` equivalents.

`StrictInt`, `StrictStr`, `StrictBool`, `StrictFloat` for per-field strictness.

`AwareDatetime`, `NaiveDatetime`, `PastDate`, `FutureDate` for time.

`Json` for a field that holds a JSON string and should be parsed and checked as structured data.

`SecretStr` and `SecretBytes`, which are worth knowing: they hide their value in `repr` and logs. A password or token can't leak into a traceback by accident. The real value comes from `.get_secret_value()`, which makes each access deliberate and greppable.

## Composing types

Named types compose, which is where this starts paying compound interest:

```python
Minutes = Annotated[int, Field(gt=0, le=180)]
Schedule = Dict[str, List[Minutes]]
```

each int in that nested structure is checked as a `Minutes`. The constraint applies at each depth, and the annotation stays readable.

This is also how to keep deep annotations comprehensible. `Dict[str, List[Annotated[int, Field(gt=0, le=180)]]]` is strictly the same thing and no one can read it.

## Where to put them

A `types.py` module beside your models is the usual answer. It turns out to be a truly handy file. Read it and you learn the vocab of the domain. What a slug is, what a duration may be, what an identifier looks like. Without reading a single model.

That is worth more than the deduplication. A named set of domain types is docs that can't go stale. It's the code that runs.

## When not to bother

Don't name a type used once with no rule attached. `Title = Annotated[str, Field()]` is ceremony.

Don't build a custom type where a `Literal` or `Enum` is the honest answer. A pattern matching four values is a worse enumeration than an enumeration.

And don't go so far that a reader can't tell what a field really is. `slug: Slug` is clear. `slug: NormalisedConstrainedIdentifier` is a name that has stopped helping.

## Types that carry documentation

Metadata inside `Annotated` reaches the schema just as it would from a `Field`. This Means a named type can carry its own description:

```python
Minutes = Annotated[
    int,
    Field(gt=0, le=180, description="Reading time in minutes."),
]
```

Now each field of that type is documented the same way, all over, with no repetition. For an API with a dozen models sharing a vocab, that agreement is visible in the made docs and would be hopeless to maintain by hand.

## Composing with unions and containers

Named types combine with all else:

```python
Slug = Annotated[str, Field(pattern=r"^[a-z0-9_]+$")]
OptionalSlug = Optional[Slug]
SlugList = Annotated[List[Slug], Field(min_length=1)]
```

The last one is worth reading twice: the outer `Field` constrains the *list*. Each item is still checked as a `Slug`. Constraints at two levels, one line, still legible.

That legibility is the point. The equal written inline is a nested `Annotated` that no one will want to modify.

## Custom types with `__get_pydantic_core_schema__`

For a type Pydantic knows nothing about. A third-party class, a domain object with its own parsing. There's a protocol to teach it:

```python
class Money:
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        ...
```

This is the full escape hatch. It's truly the right answer for a library wrapping its own types.

For use code it's almost never needed. `Annotated` with a `BeforeValidator` that makes the object, plus `arbitrary_types_allowed` if needed, covers nearly each case with a fraction of the machinery. Reach for the protocol when you're writing a library others will use with Pydantic, not when you've one awkward field.

## Where a named type goes wrong

**Naming the type after the field.** `ModuleTitle` can't be reused by `Lesson`. This Defeats the purpose. Name it after what it's: `Title`, `Slug`, `Minutes`.

**Too many layers.** A type built from three other named types is impressive and unreadable. If a reader has to follow three meanings to learn what a field accepts, the abstraction has stopped paying.

**Hiding a `Literal`.** A custom type checking membership of four strings is worse than the enumeration it's imitating.

**Naming a thing with no rule.** `Name = Annotated[str, Field()]` is ceremony with no content.

## The file this produces

A `types.py` in a mature project is one of its most handy docs. Ten or twenty lines defining what a slug is, what a duration may be, what an identifier looks like, what money means here.

Read it and you've the domain's vocab before opening a single model. That is the real return. Not saved keystrokes. A single place where the shape of the domain is stated and can't drift from the code that enforces it.

## Summary

`Annotated[T, Field(...)]` makes a constraint into a named, reusable type. `AfterValidator` and `BeforeValidator` put logic inside that type so rules needing code are reusable too. Metadata runs left to right: before-checkers, coercion, constraints, after-checkers.

Use the types Pydantic already ships. Collect your own in one module. And reach for this the second time you write the same rule, not the sixth.

## When to start

The rule of thumb is the second case. The first time you write a constraint, write it inline. The second time you need the same one, name it.

That threshold is low on purpose. The cost of naming a type is one line and the cost of not naming it compounds quietly. Six copies of a rule, four of which are updated when it changes. No one notices the other two until a thing invalid gets through.

Naming early also raises the models at once, before any reuse happens. `slug: Slug` reads better than a regular formula embedded in a field declaration. The reuse is the payoff. The readability is the down payment.


## Mistakes people make

**Naming the type after the field it first appeared on.** `ModuleTitle` is a type no other model can fairly use. This Drops the only reason to have named it. `Title` can be used by `Lesson`, `Track` and all else.

**Building a type where a `Literal` is the honest answer.** A constrained string checking membership of four values makes a worse error, a worse schema and worse static checking than the enumeration it's imitating.

**Stacking layers until no one can read it.** A type composed from three other named types is impressive and opaque. If understanding a field means following three meanings, the abstraction has stopped paying for itself.

**Reaching for `__get_pydantic_core_schema__` too early.** The full protocol exists for library authors teaching Pydantic about their own types. use code almost always wants an `Annotated` with a `BeforeValidator` instead, at a fraction of the cost.

**Putting the metadata in the wrong order.** `Annotated[str, Field(pattern=p), BeforeValidator(f)]` still runs the normaliser first. Before-checkers always precede coercion. But reading it in that order misleads whoever keeps it next. Write the pipeline in the order it runs.

**Naming a type with no rule in it.** `Annotated[str, Field()]` is ceremony. If there's nothing to say about the type beyond `str`, write `str`.

## The return

A named type isn't primarily about saving keystrokes.

It's about there being one place where the shape of a domain idea is stated. About each model that uses it taking from that statement rather than a copy of it.

The reuse blocks drift. The name raises each model it appears in. And the file they live in turns the closest thing a code has to a written description of its own vocab. One that can't go stale. It's the code doing the work.

## How this changes a codebase

The visible effect is smaller models. The real effect is that choices stop being scattered.

Before: six models each declare a slug, each with its own copy of a pattern. The meaning of a slug exists only as an emergent property of six places agreeing.

After: one line says what a slug is. Six models refer to it. The meaning exists, in one place, with a name.

That shift matters most at the moments codebases often go wrong. When a rule changes, when somebody new adds a seventh model, when a bug turns out to be one of the six copies having been updated and the others not.

It also changes how the code reads to somebody arriving. Models built from named domain types show the domain. Models built from `str` and `int` with regular expressions attached show a output format. The domain has to be inferred.

The method is a single line of `typing`. The return is a code where the vocab is written down.

## A last practical note

add named types bit by bit rather than in one refactor.

The natural moment is when you next write a rule for the second time. Extract it then, use it in both places. Move on. Repeat that for a few weeks and a `types.py` builds up on its own, holding just the rules that really repeat. Which is a better pick than any up-front attempt to guess them.

The reverse approach, sitting down to define a full vocab before it's needed, tends to give types nothing uses and abstractions that don't match how the domain turned out.
''',
    [
        {"q": "What is `Annotated[str, Field(pattern=...)]`?",
         "options": ["A Pydantic-only construct", "A real type you can name and reuse anywhere", "A validator", "A default value"],
         "answer": 1,
         "why": "`Annotated` is standard typing. Bound to a name it becomes a reusable type, so a rule is defined once and every use site stays consistent."},
        {"q": "In `Annotated[str, BeforeValidator(f), Field(pattern=p)]`, what runs first?",
         "options": ["The pattern", "The before-validator, then coercion, then the pattern", "They run in parallel", "Undefined order"],
         "answer": 1,
         "why": "Before-validators see raw input, then coercion happens, then constraints, then after-validators. Written the other way the pattern would reject values the normaliser was meant to fix."},
        {"q": "Why is `Annotated[int, Field(gt=0)] = 10` preferable to `Field(default=10, gt=0)`?",
         "options": ["It is faster", "It separates what the type is from what it defaults to, and the type can be named and reused", "The second is invalid", "No difference at all"],
         "answer": 1,
         "why": "Behaviour is identical; the Annotated form keeps the constraint with the type and the default where defaults normally sit, and lets the constrained type be reused."},
        {"q": "What does `SecretStr` protect against?",
         "options": ["Weak passwords", "The value appearing in repr, logs and tracebacks", "SQL injection", "Short strings"],
         "answer": 1,
         "why": "It hides the value in representations so a token cannot leak into a log by accident, and requires `.get_secret_value()` to read it - making every access deliberate."},
    ],
)


# ---------------------------------------------------------------------------
# 19. Validator modes
# ---------------------------------------------------------------------------
topic(
    "validator_modes",
    "Validator Modes",
    "Control",
    "before, after, plain and wrap - what runs when, relative to coercion, and why "
    "the choice changes what you can do.",
    _svg(_box(8, 34, 30, 22, S) + _txt(23, 48, "before", M, 7) +
         _arrow(40, 45, 52, 45) +
         _box(54, 34, 34, 22, S, A) + _txt(71, 48, "coerce", A, 7) +
         _arrow(90, 45, 102, 45) +
         _box(104, 34, 30, 22, S) + _txt(119, 48, "after", M, 7)),
    [
        ("Seeing the pipeline",
         "One field, one validator of each kind, printing what it received. The order "
         "and the types tell you everything.",
         '''from typing import Annotated
from pydantic import BaseModel, BeforeValidator, AfterValidator

def before(v):
    print("  before : %-8r (%s)" % (v, type(v).__name__))
    return v

def after(v):
    print("  after  : %-8r (%s)" % (v, type(v).__name__))
    return v

class M(BaseModel):
    n: Annotated[int, BeforeValidator(before), AfterValidator(after)]

print('validating "12":')
m = M(n="12")
print("  result :", repr(m.n))
print()
print("before saw the string; coercion ran; after saw the int.")'''),

        ("before is for shape, after is for value",
         "Choosing the wrong mode is the usual reason a validator never runs: in after "
         "mode a bad shape has already failed.",
         '''from typing import Annotated, List
from pydantic import BaseModel, BeforeValidator, AfterValidator, ValidationError

def split_csv(v):
    return [p.strip() for p in v.split(",")] if isinstance(v, str) else v

def lowercase(v: List[str]) -> List[str]:
    return [t.lower() for t in v]

class Right(BaseModel):
    tags: Annotated[List[str], BeforeValidator(split_csv), AfterValidator(lowercase)]

class Wrong(BaseModel):
    # split_csv in AFTER mode never sees the string - validation failed first
    tags: Annotated[List[str], AfterValidator(split_csv)]

print("right:", Right(tags="Maths, Vectors").tags)

try:
    Wrong(tags="Maths, Vectors")
except ValidationError as e:
    print("wrong:", e.errors()[0]["type"], "- the string never reached the validator")'''),

        ("plain replaces validation entirely",
         "A plain validator takes over: no coercion happens at all, and whatever it "
         "returns is the field.",
         '''from typing import Annotated, Any
from pydantic import BaseModel, PlainValidator

def parse_duration(v: Any) -> int:
    "Accept 90, '90', '1h30m' - and decide the result ourselves."
    if isinstance(v, int):
        return v
    s = str(v).strip()
    if s.isdigit():
        return int(s)
    total, num = 0, ""
    for ch in s:
        if ch.isdigit():
            num += ch
        elif ch == "h":
            total += int(num or 0) * 60; num = ""
        elif ch == "m":
            total += int(num or 0); num = ""
    return total + int(num or 0)

class Module(BaseModel):
    minutes: Annotated[int, PlainValidator(parse_duration)]

for value in [90, "90", "1h30m", "2h", "45m"]:
    print("%-8r -> %d" % (value, Module(minutes=value).minutes))'''),

        ("wrap sees both sides",
         "A wrap validator receives the value <em>and</em> the handler that would "
         "normally validate it, so it can catch a failure and substitute something.",
         '''from typing import Annotated, Any
from pydantic import BaseModel, WrapValidator, ValidationError, ValidatorFunctionWrapHandler

def default_on_failure(v: Any, handler: ValidatorFunctionWrapHandler) -> int:
    try:
        return handler(v)          # run normal validation
    except ValidationError:
        return 0                   # ...and rescue it

class Lenient(BaseModel):
    views: Annotated[int, WrapValidator(default_on_failure)]

for value in [12, "12", "lots", None]:
    print("%-8r -> %r" % (value, Lenient(views=value).views))

print()
print("Use sparingly: swallowing an error is a decision to lose information.")'''),

        ("Order among several",
         "Validators of the same kind run in the order written. Before-validators run "
         "outside-in, after-validators inside-out.",
         '''from typing import Annotated
from pydantic import BaseModel, BeforeValidator, AfterValidator

def b1(v):
    print("  before 1"); return v
def b2(v):
    print("  before 2"); return v
def a1(v):
    print("  after 1"); return v
def a2(v):
    print("  after 2"); return v

class M(BaseModel):
    n: Annotated[int, BeforeValidator(b1), BeforeValidator(b2),
                 AfterValidator(a1), AfterValidator(a2)]

print("validating:")
M(n="1")
print()
print("Written left to right, before-validators run in that order and")
print("after-validators run in it too - read top to bottom as the pipeline.")'''),

        ("The same modes on a decorator",
         "<code>field_validator</code> takes the same <code>mode</code> argument. "
         "<code>Annotated</code> makes it reusable; the decorator keeps it local.",
         '''from pydantic import BaseModel, field_validator

class Module(BaseModel):
    tags: list
    title: str

    @field_validator("tags", mode="before")
    @classmethod
    def split_csv(cls, v):
        return [p.strip() for p in v.split(",")] if isinstance(v, str) else v

    @field_validator("title", mode="after")
    @classmethod
    def titlecase(cls, v: str) -> str:
        return v.strip().title()

m = Module(tags="maths, vectors", title="  the chain rule ")
print("tags :", m.tags)
print("title:", repr(m.title))'''),
    ],
    [
        "<strong>before</strong> sees the raw input, unconverted. Use it to fix the <em>shape</em> of a value.",
        "<strong>after</strong> is the default and sees the coerced value, already the annotated type. Use it to check or normalise the <em>value</em>.",
        "<strong>plain</strong> replaces validation entirely &mdash; no coercion runs, and whatever it returns is the field.",
        "<strong>wrap</strong> receives the value and a handler, so it can run normal validation and catch the failure.",
        "The commonest mistake is putting shape-fixing logic in after mode, where the bad shape has already failed validation and the code never runs.",
        "Both spellings exist: <code>Annotated[T, BeforeValidator(f)]</code> for a reusable type, <code>@field_validator(\"x\", mode=\"before\")</code> for one model.",
    ],
    '''
title: Validator Modes: before, after, plain and wrap
intro: What runs when, scaled to coercion. Why the choice decides what a checker can do.

## The pipeline

Every validator in Pydantic runs at a particular point in the pipeline. Some run after the built-in type check. Some run before it. Some replace it entirely. A few wrap around it and decide what to do with the result. The point where a validator runs is called its mode.

Choosing the right mode matters. A validator that runs too late sees a value that has already been converted, so it cannot fix the raw input. A validator that runs too early sees data that has not been checked, so it must defend itself against anything. Most of the confusing validator bugs come from the wrong mode.

This article lays out the pipeline first, so you can see where each mode sits. It covers after, which is the default and the safest. It covers before, which is for fixing the shape of the input. It covers plain, which takes over the check completely, and wrap, which surrounds it. For each one you will see what the validator receives and what it is responsible for. Once you know the four, you can pick the right one for a rule by thinking about when it should run.

The names are easy to remember once the pipeline is clear. Think of the check as a line of stations. Each mode is a different position on that line. You will leave the article knowing which station to stand at for each kind of rule, which is the whole skill.

Pick the mode by asking one question, which is when the rule should run.

checking one field is a sequence, and each mode is a slot in it:

1. **before** checkers run on the raw input, just as it arrived.
2. **Coercion** converts the value to the annotated type.
3. **Constraints** from `Field` are checked.
4. **after** checkers run on the final, converted value.

`plain` and `wrap` are other: they replace or surround the whole thing rather than sitting inside it.

Almost each confusion about checkers dissolves once this sequence is clear. The question "why did my checker not run?" nearly always has the answer "it was in after mode and the value failed at step 2".

## after: the default

An after checker receives the value already converted. `n: int` given `"12"` reaches an after checker as the int `12`.

That is what you want for nearly all. Checking membership of a set, checking against a bound that a constraint can't express, norming a string, deduplicating a list. All of these are simpler when the value is known to be the right type. You can operate on it right with no defensive `isinstance`.

It's also safer. An after checker can't receive an any object. It can't fail in surprising ways on input it never anticipated.

## before: fixing the shape

A before checker sees the raw input. Nothing has been checked. The value could be anything.

Its purpose is repairing the *shape* of data before normal check gets to it. The canonical case is a field that should be a list, from a caller that sends a comma-split string:

```python
def split_csv(v):
    return [p.strip() for p in v.split(",")] if isinstance(v, str) else v
```

In after mode this code would never run. A string isn't a list. Check fails at step 2 and step 4 is never reached. This is the single most common checker mistake. The symptom. "my checker isn't being called". Sounds like a bug in Pydantic rather than a mode choice.

Two rules for before checkers, both results of receiving unchecked input. Guard with `isinstance` rather than given a type. And return anything you don't handle unchanged. Normal check still runs on it.

Keep them small. Complex logic operating on unvalidated input is hard to reason about. Errors raised there lack the context that makes Pydantic's messages handy.

## plain: taking over

A plain checker replaces check for that field. No coercion runs, no constraints are checked. What it returns turns the value &mdash; unvalidated.

```python
minutes: Annotated[int, PlainValidator(parse_duration)]
```

The annotation still says `int`, and that now serves as docs and as the schema type rather than as a thing enforced. Your function is fully in charge for making an int.

This is the right tool for a truly custom input format. Durations like `"1h30m"`, a coord string, a domain-exact identifier. Trying to express those with before checkers plus normal coercion is more convoluted than simply owning the parse.

The cost is that you've taken job, including making sensible errors. Raise `ValueError` for bad input rather than returning a thing wrong, or you've built a field that silently accepts nonsense.

## wrap: around the outside

A wrap checker receives the value *and* a handler that performs the normal check. That lets it act before, after, and instead of:

```python
def default_on_failure(v, handler):
    try:
        return handler(v)
    except ValidationError:
        return 0
```

The main uses are supplying a fallback instead of failing, adding context to an error before re-raising. Short-circuiting costly check for a known-good sentinel.

Use it sparingly, and be honest about the fallback case. Swallowing a `ValidationError` and substituting a default is a choice to lose data. The caller sent a thing wrong and will never know. That is at times right. A metrics field where a bad value shouldn't fail the whole request. And often a way to hide a bug for months.

## Order

a few checkers of the same kind run in the order written. Read the annotation left to right and you're reading the pipeline top to bottom.

Mixed kinds follow the sequence: all before checkers, then coercion and constraints, then all after checkers.

That makes a norm-then-check type read on its own:

```python
Slug = Annotated[str, BeforeValidator(to_slug), Field(pattern=r"^[a-z0-9_]+$")]
```

Norm, then coerce, then check. Swap the order of the metadata and the intent changes.

## Two spellings

all here exists in both forms.

`Annotated[T, BeforeValidator(f)]` makes the rule part of a type. It's reusable across models. This is the better default for anything a second model will ever need.

`@field_validator("x", mode="before")` attaches the rule to one model. Better when the logic is truly exact to that model, or when it needs `info.data` to see other fields. Which the `Annotated` form doesn't provide.

`model_validator` also takes `mode`, with `before` receiving the whole raw payload and `after` receiving the finished model. Same vocab, model-wide scope.

## Choosing

Ask what the value looks like when your logic needs to see it.

**Already the right type** &mdash; after. This covers most cases.

**Still in its raw form, wrong shape** &mdash; before.

**A format Pydantic has no idea about** &mdash; plain.

**Need to catch or replace a failure** &mdash; wrap.

And when a checker doesn't seem to run, check the mode first. It's the answer far more often than anything else.

## A worked example

A duration field accepting `90`, `"90"` and `"1h30m"`, rejecting nonsense. Constrained to a sensible range.

`plain` is the honest choice: the input format isn't a thing coercion can be expected to handle. Taking over the parse is clearer than a chain of before-checkers trying to massage `"1h30m"` into a thing `int()` will accept.

Since a plain checker skips constraints, the range check moves into the function or into a split after checker. That is the trade. Full control over parsing, full job for all downstream of it.

## Modes on model validators

The same vocab applies at model level, with other scope.

`model_validator(mode="before")` receives the raw input for the whole payload. Often a dict. It can be anything. It's a classmethod. It returns the data to be checked. Use it to translate a legacy shape or fill in a derived key before field check runs.

`model_validator(mode="after")` receives the finished model as `self` and returns it. This is where cross-field rules belong.

There's a `mode="wrap"` at model level too, receiving the payload and a handler. This Can catch a whole-model failure and substitute a thing. It's rare and powerful. The same caution about swallowing errors applies.

## What each mode can and cannot do

Worth a table in your head.

A **before** checker can change the shape, can't lean on the type. Its errors carry less context because nothing has been located yet.

An **after** checker can lean on the type, can't repair a shape that already failed. Gets good error locations for free.

A **plain** checker controls all and takes from nothing. No coercion, no constraints. Anything you want enforced you must enforce yourself.

A **wrap** checker can do all of the above and is the only one that can see a failure and decide what to do about it.

## Debugging when a validator misbehaves

Three questions, in order, that resolve nearly each case.

**Is it running at all?** Put a `print` at the top. If nothing appears, the mode is wrong. Almost always an after checker whose input failed coercion first.

**What type is it receiving?** Print `type(v)`. A before checker gets raw input and an after checker gets the coerced value. given the wrong one is the second most common mistake.

**Is it returning?** A checker with no `return` sets the field to `None`, silently. If a field turns `None` after you added a checker, that is the cause.

## Constraints still run in the middle

A detail that is easy to forget: `Field` constraints sit between the two checker slots.

So `Annotated[int, BeforeValidator(f), Field(gt=0), AfterValidator(g)]` runs `f` on raw input, coerces, checks `> 0`, then runs `g`. An after checker never sees a value that failed a constraint. The constraint raised first.

That is often convenient &mdash; the after checker can assume the bounds hold &mdash; and at times the reason a checker meant to *fix* an out-of-range value never runs. Clamping belongs in `before`, or in the constraint's lack.

## Performance

checkers are Python, and Python is the slow part of an else Rust pipeline.

For a model built a few times per request this is irrelevant. For checking a large set it's the dominant cost. Each item's checkers are a round trip out of the core and back.

If profiling points at check on a hot path, the questions are. Can this rule be a constraint instead. Constraints run in Rust. And is the checker doing work that could be done once outside rather than per item. A checker that rebuilds a set of permitted values on each call is a common and easily fixed version of the second.

## Summary

Four slots around one pipeline: before, coerce, constrain, after. `plain` replaces the pipeline. `wrap` surrounds it.

Choose by asking what the value looks like when your logic needs to see it. When a checker doesn't run, check the mode before anything else. And note that constraints sit between the two plain slots. An after checker only ever sees values that already passed them.

## The mental model

One sentence holds most of it: **before sees what arrived, after sees what it became.**

all else follows. A checker repairing a shape must run before. After the shape has already failed. A checker checking meaning should run after, because it can then lean on the type. Constraints sit between them. An after checker never sees a value that broke one.

`plain` and `wrap` step outside that sequence. One replacing it, the other nearby it. And both are for cases where the standard pipeline isn't what you want at all.

Keep the sentence and the rest is derivable.


## Mistakes people make

**Shape-fixing logic in after mode.** The single most common. It presents as "my checker never runs". The value failed coercion at step two and step four was never reached.

**given the type in a before checker.** It receives raw input. This Can be anything at all. Guard with `isinstance` and pass through unchanged what you don't handle. The normal path still runs.

**Losing to return.** Silent, and it sets the field to `None`. If a field mysteriously turns `None` after a checker is added, this is why.

**Expecting constraints to run after a plain checker.** `plain` replaces the pipeline fully. No coercion and no constraints. Anything you want enforced is now yours to enforce.

**Swallowing errors in a wrap checker.** Catching a `ValidationError` and substituting a default is a choice to lose data. The caller sent a thing wrong and will never be told. at times correct, often a bug hidden for months.

**Rebuilding data inside a checker on each call.** A checker that makes a set of permitted values each time it runs does that work once per item checked. Hoist it out. On a large set it's the dominant cost.

## A closing note

Nearly each question about checkers reduces to a question about spot.

Not "how do I write this rule" but "where in the sequence does it need to sit". Once that is settled the code is often short and obvious. When a checker behaves strangely the spot is almost always what is wrong.

Before, coerce, constrain, after. Four slots, one order. All else follows from knowing which one you're in.
''',
    [
        {"q": "Your validator turns a CSV string into a list, but it never runs. Why?",
         "options": ["A Pydantic bug", "It is in after mode, and a string already failed list coercion before it", "It needs @classmethod", "The field is optional"],
         "answer": 1,
         "why": "After validators run at step 4, and coercion failed at step 2. Shape-fixing logic must be in before mode, where the raw value is still available."},
        {"q": "What does a `plain` validator skip?",
         "options": ["Nothing", "Coercion and constraints - it replaces validation entirely", "Only constraints", "Only coercion"],
         "answer": 1,
         "why": "It takes over completely. Whatever it returns becomes the field unvalidated, so producing the right type and raising on bad input are both your responsibility."},
        {"q": "What does a `wrap` validator receive besides the value?",
         "options": ["The model", "A handler that performs the normal validation", "The field name", "Nothing"],
         "answer": 1,
         "why": "Calling the handler runs standard validation, so a wrap validator can catch its failure and substitute a value, or add context and re-raise."},
        {"q": "In `Annotated[str, BeforeValidator(to_slug), Field(pattern=p)]`, what is the order?",
         "options": ["Pattern, then normaliser", "Normaliser, then coercion, then pattern", "Both at once", "Pattern only"],
         "answer": 1,
         "why": "The pipeline is before, coerce, constrain, after. Written the other way the pattern would reject the messy input the normaliser existed to clean."},
    ],
)


# ---------------------------------------------------------------------------
# 20. model_dump and model_dump_json
# ---------------------------------------------------------------------------
topic(
    "model_dump_and_model_dump_json",
    "model_dump and model_dump_json",
    "In and Out",
    "Getting data back out: the two modes, the arguments that shape the output, "
    "and the mistake that raises TypeError.",
    _svg(_box(20, 16, 120, 20, S, A) + _txt(80, 30, "Module", A, 9) +
         _arrow(50, 40, 50, 52) + _arrow(110, 40, 110, 52) +
         _box(16, 54, 54, 20, S) + _txt(43, 68, "dict", M, 8) +
         _box(90, 54, 54, 20, S) + _txt(117, 68, "json", M, 8)),
    [
        ("Two methods, two purposes",
         "<code>model_dump()</code> gives Python objects for use inside your program. "
         "<code>model_dump_json()</code> gives text for leaving it.",
         '''from datetime import date
from decimal import Decimal
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    published_on: date
    price: Decimal

m = Module(title="Vectors", published_on="2026-08-26", price="12.50")

d = m.model_dump()
print("dump    :", d)
for k, v in d.items():
    print("   %-14s %s" % (k, type(v).__name__))

print()
print("dump_json:", m.model_dump_json())'''),

        ("The TypeError everybody meets once",
         "Passing <code>model_dump()</code> to <code>json.dumps</code> fails, because "
         "the dict still holds real Python objects.",
         '''import json
from datetime import date
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    published_on: date

m = Module(title="Vectors", published_on="2026-08-26")

try:
    json.dumps(m.model_dump())
except TypeError as e:
    print("json.dumps(model_dump()) ->", e)

print()
print("correct  :", m.model_dump_json())
print("or first :", json.dumps(m.model_dump(mode="json")))'''),

        ("Choosing what comes out",
         "<code>include</code> and <code>exclude</code> pick fields, and reach into "
         "nested models with a dict.",
         '''from pydantic import BaseModel

class Author(BaseModel):
    name: str
    email: str

class Module(BaseModel):
    title: str
    author: Author
    internal_notes: str

m = Module(title="Vectors",
           author={"name": "Ada", "email": "ada@vizlearn.in"},
           internal_notes="needs a diagram")

print("all      :", m.model_dump())
print("public   :", m.model_dump(exclude={"internal_notes": True,
                                          "author": {"email"}}))
print("minimal  :", m.model_dump(include={"title": True,
                                          "author": {"name"}}))'''),

        ("Dropping what was never set",
         "Three filters that matter for updates: <code>exclude_unset</code>, "
         "<code>exclude_defaults</code> and <code>exclude_none</code>.",
         '''from typing import Optional
from pydantic import BaseModel

class Update(BaseModel):
    title: Optional[str] = None
    minutes: int = 10
    summary: Optional[str] = None

m = Update(title="Vectors", summary=None)

print("everything      :", m.model_dump())
print("exclude_unset   :", m.model_dump(exclude_unset=True))
print("exclude_defaults:", m.model_dump(exclude_defaults=True))
print("exclude_none    :", m.model_dump(exclude_none=True))
print()
print("exclude_unset keeps summary=None because it WAS sent.")
print("exclude_none drops it, losing the instruction to clear the field.")'''),

        ("Excluding a field permanently",
         "<code>Field(exclude=True)</code> keeps a value out of every serialisation, "
         "which is what you want for anything secret.",
         '''from pydantic import BaseModel, Field, SecretStr

class User(BaseModel):
    name: str
    password_hash: str = Field(exclude=True)
    api_token: SecretStr

u = User(name="Ada", password_hash="$2b$12$abcdef", api_token="tok_live_123")

print("repr    :", u)
print("dump    :", u.model_dump())
print("json    :", u.model_dump_json())
print()
print("the value is still there when you ask for it:")
print("   hash :", u.password_hash)
print("   token:", u.api_token.get_secret_value())'''),

        ("Round tripping",
         "A dump is valid input again &mdash; but only if you did not filter it. That "
         "is worth checking rather than assuming.",
         '''from pydantic import BaseModel, ValidationError

class Module(BaseModel):
    title: str
    minutes: int

m = Module(title="Vectors", minutes=8)

full = Module.model_validate(m.model_dump())
print("round trip :", full == m)

try:
    Module.model_validate(m.model_dump(exclude={"minutes"}))
except ValidationError as e:
    print("filtered   :", e.errors()[0]["type"], "- a filtered dump is not valid input")

print()
print("json round trip:", Module.model_validate_json(m.model_dump_json()) == m)'''),
    ],
    [
        "<code>model_dump()</code> keeps Python objects; <code>model_dump_json()</code> produces JSON text. Use the second for anything leaving the process.",
        "<code>json.dumps(m.model_dump())</code> raises <code>TypeError</code> on dates and decimals. Use <code>model_dump_json()</code>, or <code>model_dump(mode=\"json\")</code> if you need the dict.",
        "<code>include</code> and <code>exclude</code> take sets or nested dicts. Once one entry needs to reach inside, every entry becomes a key.",
        "<code>exclude_unset</code> is the one for PATCH: it emits only what the caller supplied, so an explicit <code>null</code> survives and an omission stays omitted.",
        "<code>exclude_none</code> is <em>not</em> the same thing &mdash; it drops explicit nulls too, which throws away the instruction to clear a field.",
        "<code>Field(exclude=True)</code> keeps a value out of every dump permanently. <code>SecretStr</code> additionally hides it from <code>repr</code> and logs.",
    ],
    '''
title: model_dump and model_dump_json: Getting Data Back Out
intro: Two methods, a few filters, and the one mistake that raises TypeError.

## Two methods, and the difference that matters

Validation brings data in. Sooner or later you have to send it back out, as a dictionary for Python code or as JSON for a client. Pydantic has two methods for this, and they look similar enough that people use the wrong one.

The first, model_dump, gives you a dictionary of Python values. The second, model_dump_json, gives you a JSON string. The difference matters because some Python values, such as dates and decimals, are not JSON. Pass a dumped dictionary straight to the standard json module and you can hit a TypeError.

This article explains the difference between the two methods and when each one is right. It covers that TypeError and how to avoid it. It then shows how to shape the output, choosing which fields to include and which to leave out. There are three exclusion options that look alike, such as leaving out unset fields, default fields and None values, and the article separates them clearly. By the end you will know how to produce exactly the output a caller expects, and how to do it with the least code.

You will use these two methods in almost every project, so small details add up quickly.

Each option is shown with the exact output it produces.

`model_dump()` returns a dict of Python objects. A `date` field is a `date`. A `Decimal` is a `Decimal`. An enum member is the member.

`model_dump_json()` returns a JSON string, converting all to a thing JSON can carry.

The rule of thumb: **dump for inside, dump_json for outside**. If the data is going to another function, a template, a test assertion, use `model_dump()`. If it's going into an HTTP response, a queue, or a file, use `model_dump_json()`.

There's a third form worth knowing: `model_dump(mode="json")` gives you a dict whose values are already JSON-matching. That is what you want when a thing else will do the encoding. A framework, a JSON logger, an SDK that takes a dict.

In Pydantic v1 these were `.dict()` and `.json()`. They still exist in v2 and warn. They're all over the internet.

## The TypeError

Everybody meets this once:

```python
json.dumps(m.model_dump())
# TypeError: Object of type date is not JSON serializable
```

It's confusing because the model obviously supports JSON, and the error blames a `date`.

`model_dump()` on purpose didn't convert anything. It handed you real Python objects. `json.dumps` doesn't know what to do with a `date`.

Three correct forms: `model_dump_json()` if you want the string, `json.dumps(model_dump(mode="json"))` if a thing else must do the encoding, or `model_dump(mode="json")` alone if you need the dict.

## Shaping the output

`include` and `exclude` select fields. A set names top-level fields. A dict reaches into nested models. The two spellings don't mix in one literal. Once anything needs to reach inside, each entry turns a key with `True`.

For lists of models there's a special key, `"__all__"`, applying a pick to each item.

Both are handy for dropping one obviously-inner field. Beyond that, a split output model reads better, appears right in the schema. Doesn't need anyone to trace an exclusion formula to work out what an endpoint returns.

## The three exclusions that look similar

These get confused constantly, and the gap is the whole point of the update module.

`exclude_unset=True` omits fields the caller never supplied. Fields by name sent, *including clear nulls*, are kept.

`exclude_defaults=True` omits fields whose value equals their default, whether supplied or not.

`exclude_none=True` omits each field that is `None`. But It got that way.

For a PATCH endpoint, `exclude_unset` is the correct one and the other two are wrong.

Consider a client sending `{"summary": null}` meaning "clear the summary". With `exclude_unset` the output is `{"summary": None}`. The instruction lives. With `exclude_none` the output is `{}`. The instruction is gone. The summary stays as it was. That is a bug users report as "the clear button doesn't work", and it's one arg away.

`exclude_defaults` has a narrower use: making a minimal config file, or a payload where anything unspecified should fall back to the receiver's defaults.

## Keeping secrets out

Two methods, for two other exposures.

`Field(exclude=True)` keeps a field out of each output. It's still on the object and still accessible. It simply never appears in a dump. This is right for a password hash, an inner id, or anything the model needs and consumers must not see.

`SecretStr` handles a other risk: the value appearing in a `repr`, a log line or a traceback. It displays as `**********` and needs `.get_secret_value()` to read. This Makes each access deliberate and easy to grep for.

They're complementary. A token that must neither be logged nor serialised wants both.

The safest structure of all is a split output model that simply doesn't have the field. You can't leak what isn't there. No future refactor can accidentally drop a flag.

## Round tripping

A dump is valid input to the same model:

```python
Module.model_validate(m.model_dump()) == m
```

That is truly handy for copying, for caching, and for tests.

It stops being true the moment you filter. `model_dump(exclude={"minutes"})` makes a dict missing a needed field. Checking it raises. Worth remembering when a filtered dump is being stored and later read back. The filter that made the output tidy also made it un-reloadable.

Round tripping through JSON works too, and is exact for the types Pydantic knows.

## Nested behaviour

all recurses. `model_dump()` on a model holding models returns nested plain dicts, and `model_dump_json()` makes nested JSON.

One thing to check when a nested model is a *other* class than you expect. Output follows the field's declared type. If you assign a subclass instance to a field annotated with the parent, by default the extra fields aren't serialised. The model serialises per to what it promised rather than what it happens to hold.

That action is deliberate &mdash; it stops a subclass leaking fields through an API that documented the parent &mdash; and it surprises people who expected the subclass's data. `SerializeAsAny` opts out where you truly want the richer output.

## Warnings

Pydantic will warn when output meets a thing it didn't expect. Often a field holding a value that doesn't match its annotation. This Happens when `validate_assignment` is off and a thing assigned freely.

Those warnings are worth listening to rather than silencing. They mean the object's real contents have diverged from what the model claims. The serialised output may not be what the schema promises.

## Rounding trips and warnings

Pydantic emits a warning when output meets a value that doesn't match its field's annotation. That happens when `validate_assignment` is off and a thing assigned freely, leaving the object's contents at odds with what the model claims.

Those warnings are worth reading rather than filtering. They mean the serialised output may not match the schema you publish. This Is a defect a consumer will find before you do.

If you see them regularly, the fix is upstream: turn on `validate_assignment`, or freeze the model so the divergence can't happen.

## Subclasses and what gets emitted

If a field is annotated with a parent model and holds a subclass instance, the extra fields are **not** serialised by default. The model emits what it promised, not what it happens to hold.

That is deliberate, and it's a safety property. A subclass carrying inner fields can't leak them through an endpoint documented as returning the parent.

It also surprises people who expected the richer output. `SerializeAsAny[Parent]` opts out where you truly want what the object really is. And where you've met yourself that all a subclass might carry is safe to expose.

## Context

Both dump methods accept a `context` dict. Serialisers can read it through their `info` arg.

That is the supported way to make output depend on a thing external without a global. A locale, a viewer's permissions, a feature flag:

```python
m.model_dump(context={"role": "admin"})
```

Used sparingly it's the clean answer to "this field is only visible to some callers". Used heavily it makes output no one can predict from the model alone. Split output models are clearer.

## Choosing between filtering and separate models

The recurring question in this module: `exclude` or a second model?

Use `exclude` for one or two obviously-inner fields. Here The shapes are else same and the intent is plain at the call site.

Use a split model when the gap is structural, when the same gap is needed in more than one place, or when the output is part of a public contract. A model is checked, appears right in the schema, can't be forgotten at a new call site. Is hopeless to get wrong by mistyping a field name in a set.

The exclusion set is the thing that quietly stops matching the model. A field renamed in the model and not in the exclusion set silently starts appearing in your public output, and nothing raises.

## Performance

output happens in Rust and is fast. It isn't free. Two habits cost more than people expect.

Serialising more than you send. Building a full dump and then picking three keys out of it does the work for each field including nested trees. `include` does the same job without the waste.

Serialising the same object again and again. Inside a loop that renders one object per row, hoisting the dump out is the obvious fix and easy to miss.

Neither matters at small scale. Both are visible when a response holds thousands of models.

## Summary

`model_dump()` for Python objects, `model_dump_json()` for text, `model_dump(mode="json")` for a JSON-safe dict.

`json.dumps(model_dump())` is the classic mistake. The dict is full of real objects.

`exclude_unset` for PATCH, and not `exclude_none`. This Discards the gap between "not mentioned" and "please clear this".

`Field(exclude=True)` and `SecretStr` for secrets, and a split output model when you want the promise rather than the setting.

## A last habit

Look at what your model really emits, once, before it goes anywhere public.

One `print(m.model_dump_json(indent=2))` shows you the keys, the casing, the formats. Anything present that shouldn't be. It's the same five-minute review as printing the schema. It catches a other set of problems. A secret that was never excluded, a nested field no one meant to expose, snake_case where the rest of the API is camelCase.

The output of a model is a contract with all who consumes it. It's worth having read it.


## Mistakes people make

**`json.dumps(model_dump())`.** The classic. The dict holds real `date` and `Decimal` objects. The standard encoder refuses them. The error blames a date and the cause is the wrong method.

**`exclude_none` where `exclude_unset` was meant.** On an update endpoint this discards a caller's clear instruction to clear a field. It presents as "the clear button doesn't work" and is one arg away from correct.

**Filtering a dump that is later reloaded.** An unfiltered dump round-trips. A filtered one is missing needed fields and won't validate. This bites when the tidy output is stored and read back later.

**Trusting an exclusion set to stay correct.** Rename a field in the model, forget the exclusion set. A thing inner silently begins appearing in your public output. Nothing raises. A split output model can't fail this way.

**Serialising more than you need.** Building a full dump of a nested tree to pick three keys out of it does all the work for each field. `include` does the same job without it.

**Skipping output warnings.** They mean an object's contents no longer match what the model claims, often because a thing was assigned without `validate_assignment`. The published schema and the actual output have diverged. A consumer will find it first.

## The two mistakes

If only two things live from this module, make them these.

`json.dumps(model_dump())` raises, because the dict is full of real Python objects. Use `model_dump_json()`, or `mode="json"` when a thing else does the encoding.

`exclude_none` isn't `exclude_unset`. The first throws away a caller's clear instruction to clear a field. The second preserves it. On a PATCH endpoint that gap is a bug users report and no one can copy.

## Output as a contract

The output of a model is a contract, whether or not anybody wrote it down.

Somebody is parsing those keys. A thing depends on that date format. A client one spot assumes a field is present because it always has been. None of that is in a doc. It's in the action. It turns binding the moment anyone builds against it.

That is why the choices in this module deserve more care than they often get. Adding a found field changes each response the model feeds. Renaming a field breaks parsers. Changing an exclusion set alters what leaves your system, silently and without any test failing.

The hands-on habit is to treat a model that reaches the outside world as a published interface. Know what it emits, be deliberate about changing it. Prefer a split output model when the shape you send differs from the shape you hold. A dedicated class makes the contract clear, checkable and hard to alter by accident. Which is just what a contract should be.
''',
    [
        {"q": "Why does `json.dumps(m.model_dump())` raise TypeError on a date field?",
         "options": ["model_dump is broken", "model_dump returns real Python objects, which json.dumps cannot encode", "Dates are unsupported", "It needs an argument"],
         "answer": 1,
         "why": "`model_dump()` deliberately preserves Python types. Use `model_dump_json()`, or `model_dump(mode=\"json\")` when something else does the encoding."},
        {"q": "A PATCH client sends `{\"summary\": null}` to clear a field. Which filter preserves that?",
         "options": ["exclude_none", "exclude_unset", "exclude_defaults", "Any of them"],
         "answer": 1,
         "why": "`exclude_unset` keeps fields that were supplied, including explicit nulls. `exclude_none` would drop it, silently discarding the instruction to clear the value."},
        {"q": "What does `Field(exclude=True)` do?",
         "options": ["Rejects the field on input", "Keeps it out of every serialisation while remaining on the object", "Hides it from repr only", "Makes it optional"],
         "answer": 1,
         "why": "The value is still there and still accessible; it just never appears in a dump. `SecretStr` covers the different risk of the value appearing in logs and tracebacks."},
        {"q": "Is `model_dump(exclude={\"minutes\"})` valid input to the same model?",
         "options": ["Always", "Not if minutes is required - the field is now missing", "Only in JSON mode", "Yes, defaults fill it"],
         "answer": 1,
         "why": "An unfiltered dump round-trips, but filtering removes fields the model requires. This matters when a filtered dump is stored and later read back."},
    ],
)


# ---------------------------------------------------------------------------
# 21. Aliases
# ---------------------------------------------------------------------------
topic(
    "aliases",
    "Aliases",
    "In and Out",
    "When the wire format and your Python names disagree - camelCase, reserved "
    "words, and fields that arrive under more than one name.",
    _svg(_box(12, 30, 54, 26, S) + _txt(39, 47, "publishedAt", M, 7) +
         _arrow(70, 43, 90, 43) +
         _box(94, 30, 54, 26, S, A) + _txt(121, 47, "published_at", A, 7)),
    [
        ("The wire says camelCase",
         "An alias lets a field be populated from a different key without renaming "
         "your Python attribute.",
         '''from pydantic import BaseModel, Field

class Module(BaseModel):
    title: str
    published_at: str = Field(alias="publishedAt")
    reading_minutes: int = Field(alias="readingMinutes")

payload = {"title": "Vectors", "publishedAt": "2026-08-26", "readingMinutes": 8}

m = Module.model_validate(payload)
print("python side :", m.published_at, "|", m.reading_minutes)
print("dump        :", m.model_dump())
print("dump by alias:", m.model_dump(by_alias=True))'''),

        ("By default the alias replaces the name",
         "Once a field has an alias, the Python name no longer works as input &mdash; "
         "unless you turn <code>populate_by_name</code> on.",
         '''from pydantic import BaseModel, ConfigDict, Field, ValidationError

class Strict(BaseModel):
    published_at: str = Field(alias="publishedAt")

class Either(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    published_at: str = Field(alias="publishedAt")

print("alias works  :", Strict(publishedAt="2026-08-26"))

try:
    Strict(published_at="2026-08-26")
except ValidationError as e:
    print("name refused :", e.errors()[0]["type"], e.errors()[0]["loc"])

print()
print("with populate_by_name, both work:")
print("  ", Either(publishedAt="2026-08-26"))
print("  ", Either(published_at="2026-08-26"))'''),

        ("Different names in and out",
         "<code>validation_alias</code> and <code>serialization_alias</code> separate "
         "the two directions, which a single <code>alias</code> cannot.",
         '''from pydantic import BaseModel, Field

class Module(BaseModel):
    minutes: int = Field(validation_alias="durationMinutes",
                         serialization_alias="reading_minutes")

m = Module.model_validate({"durationMinutes": 8})

print("python    :", m.minutes)
print("plain dump:", m.model_dump())
print("by alias  :", m.model_dump(by_alias=True))
print()
print("It reads one name and writes another - useful when translating")
print("between two systems that disagree about both.")'''),

        ("Accepting several spellings",
         "<code>AliasChoices</code> takes the first key that is present, which is how "
         "you support an old and a new name at once.",
         '''from pydantic import AliasChoices, BaseModel, Field

class Module(BaseModel):
    minutes: int = Field(
        validation_alias=AliasChoices("minutes", "readingMinutes", "duration"))

for payload in [{"minutes": 8},
                {"readingMinutes": 9},
                {"duration": 10}]:
    print("%-26s -> %d" % (str(payload), Module.model_validate(payload).minutes))

print()
print("One field, three accepted spellings, no branching in your code.")'''),

        ("Reaching into a nested payload",
         "<code>AliasPath</code> pulls a value out of a nested structure, flattening "
         "someone else's shape into yours.",
         '''from pydantic import AliasPath, BaseModel, Field

class Module(BaseModel):
    title: str
    author_name: str = Field(validation_alias=AliasPath("author", "name"))
    first_tag: str = Field(validation_alias=AliasPath("tags", 0))

payload = {
    "title": "Vectors",
    "author": {"name": "Ada", "email": "ada@vizlearn.in"},
    "tags": ["maths", "linear-algebra"],
}

m = Module.model_validate(payload)
print(m)
print()
print("A nested API response became a flat model, with no manual digging.")'''),

        ("Generating aliases for the whole model",
         "<code>alias_generator</code> applies a rule to every field, which beats "
         "writing <code>alias=</code> forty times.",
         '''from pydantic import BaseModel, ConfigDict

def to_camel(name: str) -> str:
    head, *rest = name.split("_")
    return head + "".join(word.capitalize() for word in rest)

class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel,
                              populate_by_name=True)

class Module(ApiModel):
    title: str
    published_at: str
    reading_minutes: int

m = Module.model_validate({"title": "Vectors",
                           "publishedAt": "2026-08-26",
                           "readingMinutes": 8})

print("python :", m.reading_minutes)
print("out    :", m.model_dump(by_alias=True))
print("by name:", Module(title="X", published_at="Y", reading_minutes=1).reading_minutes)'''),
    ],
    [
        "<code>Field(alias=...)</code> sets one name used for both input and output. By default it <em>replaces</em> the Python name as input.",
        "<code>populate_by_name=True</code> lets a field be filled by either its alias or its Python name &mdash; almost always what you want.",
        "<code>validation_alias</code> and <code>serialization_alias</code> control the two directions independently.",
        "<code>model_dump(by_alias=True)</code> is required to emit aliases. Without it you get Python names, which is a common cause of “my API returns snake_case”.",
        "<code>AliasChoices</code> accepts several input spellings; <code>AliasPath</code> pulls a value out of a nested payload.",
        "<code>alias_generator</code> on a shared base applies a naming rule to every field, so a whole API can be camelCase in one line.",
    ],
    '''
title: Aliases: When the Wire and Your Code Disagree
intro: camelCase payloads, reserved words, legacy names, and nested shapes flattened into yours.

## Four reasons a field needs another name

The name a field has in your code is not always the name it has in the data. An external API may send camelCase keys, while your Python code uses snake_case. A legacy system may use cryptic names you would rather not spread through your code. An alias connects the two.

An alias tells Pydantic that the input key differs from the attribute name. You work with a clean name in Python and accept the awkward name on the wire. That keeps outside conventions at the edge, where they belong, instead of leaking into your own code.

This article begins with the four reasons a field needs another name. It then shows the simple form of an alias and how to use by_alias on the way out. It covers how to separate the direction, so the name you accept can differ from the name you send. You will also see how a field can accept several spellings, which helps when you migrate from an old format. Aliases are a small feature, but a lot of real integration work depends on them.

Anyone who has connected to a third-party service has met this problem. The data never quite matches the naming you would choose. You can rename things by hand in a conversion step, but that step is one more place for a typo to hide. An alias moves the mapping into the model, where it is declared once and checked every time. The same declaration can serve both directions, or each direction can have its own rule, depending on what the other side expects. The article also touches on the settings that decide whether the alias or the real name is accepted on input, which is a frequent source of confusion. Learn it once, and mismatched names stop being a source of friction in your integrations.

**The wire is camelCase.** JavaScript clients and a great many APIs use `publishedAt`. Python uses `published_at`. Renaming your fields to match makes each Python file read badly. Renaming their payload isn't an option.

**The key is a reserved word.** A payload with `from`, `class`, `import` or `id` can't map onto an field with the same name.

**The name is bad.** A third-party API calls a thing `dt2`. You don't have to.

**The name changed.** You're renaming a field and both spellings must work through a deprecation window.

## The simple form

```python
published_at: str = Field(alias="publishedAt")
```

One alias, used for input and output. There's one action here that catches all: **by default the alias replaces the Python name as input**. `Module(published_at="...")` now raises. This Is surprising when you've been making the model in your own tests.

`populate_by_name=True` fixes it:

```python
model_config = ConfigDict(populate_by_name=True)
```

Now either spelling works on the way in. This is almost always what you want. It's worth setting on a base model so no one has to rediscover it.

## by_alias on the way out

Aliases aren't used for output unless you ask:

```python
m.model_dump()                 # {"published_at": ...}
m.model_dump(by_alias=True)    # {"publishedAt": ...}
```

Losing this is the most common alias bug. The symptom is "my API accepts camelCase but returns snake_case". The aliases were configured right. The output call didn't ask for them.

In FastAPI, `response_model_by_alias` defaults to `True`. Responses use aliases on its own. Which means a manual `model_dump()` elsewhere in the same code behaves differently from the endpoint. Worth knowing before you spend an afternoon on it.

## Separating the directions

A single `alias` uses the same name both ways. When the directions differ, use the two exact settings:

```python
minutes: int = Field(validation_alias="durationMinutes",
                     serialization_alias="reading_minutes")
```

Read one name, write another. That sounds exotic and comes up when you sit between two systems that disagree. Consuming a partner API and exposing your own shape, or migrating a field where you must accept the old name and emit the new one.

Where both are set, they win over a plain `alias` in their own directions.

## Several accepted spellings

`AliasChoices` takes the first key present:

```python
minutes: int = Field(validation_alias=AliasChoices("minutes", "readingMinutes", "duration"))
```

This is the clean way to run a rename. Add the new name to the front, keep the old one, ship. Clients migrate at their own pace. Neither your model nor your handlers need a branch for it. Drop the old entry when the traffic stops.

It also handles the plain mess of a payload assembled by a few teams over a few years. Here The same value appears under three names based on which service made it.

## Reaching into nested data

`AliasPath` pulls a value out of a nested structure:

```python
author_name: str = Field(validation_alias=AliasPath("author", "name"))
first_tag: str = Field(validation_alias=AliasPath("tags", 0))
```

Strings are keys, ints are indices. A deeply nested third-party response turns a flat model with no manual digging and no mid models you didn't want.

Use it with judgement. Flattening two or three values from a response is just right. Flattening twenty makes a model whose link to the payload is hopeless to see. Modelling the real structure with nested models is clearer.

Note that `AliasPath` is check-only. There's no output equal. Rebuilding a nested shape from flat fields isn't a rename. If you need that, a custom serialiser or a split output model is the answer.

## Doing it for the whole model

Writing `alias="..."` on forty fields is tedious and drifts. `alias_generator` applies a rule to each field:

```python
class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
```

Inherit from that and each model in your API speaks camelCase, with no per-field config at all. Pydantic ships `to_camel` and `to_pascal` in `pydantic.alias_generators`. You often don't even write the function.

An clear `alias` on a field replaces the gen. This Is what you want for the handful of exceptions each real API has.

This is the right shape for a code-wide rule. One base model, one setting, each model steady. One place to change it.

## Aliases in the schema

The made JSON Schema uses aliases. This Is correct. The schema shows the wire format. The wire format is what the alias names.

So consumers of your OpenAPI doc see `publishedAt`, made clients give `publishedAt`. The docs matches what the endpoint really accepts. This is one of the places where getting aliases right pays off beyond your own code.

## Things that go wrong

**Losing `by_alias=True`** on a manual dump. The most common one.

**Losing `populate_by_name`** and then being unable to make the model in tests using Python names.

**Aliasing to a name that collides** with another field's name. This Makes confusing action rather than a clear error.

**Using aliases to paper over a bad model.** If half your fields need aliases to make sense, the model may be showing someone else's payload rather than your domain. A translation layer. An input model matching their shape, converted to yours. Is at times clearer than twenty aliases.

## Aliases and nested models

An alias applies to the field it's declared on. Nesting is unaffected. A nested model's own aliases apply when it's checked. `by_alias=True` passes through the whole tree on the way out.

So a camelCase rule applied through a shared base model reaches each level without extra work. This Is the main reason to prefer `alias_generator` on a base over per-field aliases.

The one thing to check is agreement. A tree where the parent is aliased and one nested model isn't makes output that is camelCase at the top and snake_case two levels down. Valid, confusing. Just the kind of thing that lives review.

## What the schema says

made schemas use aliases. This Is correct: the schema shows the wire. The alias is the wire name.

That has a hands-on result worth knowing. If you make a schema for inner purposes and expect Python names, you won't get them. `model_json_schema(by_alias=False)` makes the Python-named version when that is truly what you need.

For anything published, the aliased schema is the right one. It matches what the endpoint accepts and returns.

## Aliases in error messages

An error's `loc` uses the **alias**, not the Python name, when check failed on an aliased field.

That is the right action. The caller sent `publishedAt` and should be told about `publishedAt`, not about an field name they've never seen. But it means error-handling code can't assume `loc` matches your field names. This At times matters when mapping errors back to inner state.

## A migration recipe

Renaming a field in a live API, without breaking anyone:

**Step one.** Add the new name as the main, keep the old one accepted:

```python
minutes: int = Field(validation_alias=AliasChoices("minutes", "readingMinutes"))
```

Both work on the way in. Output uses whichever you set as the output alias. Keep emitting the old name for now.

**Step two.** Switch the output alias to the new name. Clients reading the response see the new one. Clients sending either still work.

**Step three.** Once traffic on the old name stops, drop it from `AliasChoices`.

Three small deploys, no coordinated cutover, no broken clients. This is the pattern aliases make possible and it's worth knowing before you need it.

## Deciding whether you need them at all

A model full of aliases is at times a sign that the model is showing someone else's payload rather than your domain.

If you consume a third-party API with thirty oddly-named fields, two models can be cleaner than thirty aliases. One matching their shape just, with their names. A conversion into yours. The first model docs their API honestly. The second is your domain, unpolluted.

Aliases are best when the gap is a *rule*. CamelCase versus snake_case, a reserved word, a rename in progress. When the gap is a whole foreign vocab, a translation layer says more.

## Summary

`alias` for one name both ways. `validation_alias` and `serialization_alias` when the directions differ. `populate_by_name=True` so Python names still work as input. `by_alias=True` to emit them.

`AliasChoices` for a few accepted spellings. This Makes renames painless. `AliasPath` for flattening nested payloads. `alias_generator` on a shared base for a whole-API rule.

And the one to note: aliases aren't used on output unless you ask for them.

## The one-line summary

Aliases exist so your Python can read like Python while your API reads like what your consumers expect.

Set the rule once on a shared base with `alias_generator` and `populate_by_name`, note `by_alias=True` when dumping by hand. Reach for `AliasChoices` the moment you need to rename a thing without breaking anyone.

all else in this module is a variation on those three.


## Mistakes people make

**Losing `by_alias=True`.** Comfortably the most common. Aliases aren't used on output unless requested. The symptom. An API accepting camelCase and returning snake_case. Looks like a config problem rather than a missing arg on one call.

**Losing `populate_by_name`.** An alias replaces the Python name as input. Your own tests can no longer make the model with the names you wrote. The fix is one config entry and it belongs on a shared base.

**Inconsistent nesting.** A parent with an alias gen and a nested model without one makes output that is camelCase at the top and snake_case two levels down. Valid, confusing. Just the sort of thing that lives review.

**given `loc` matches your field names.** Errors report the alias. That is the name the caller used. Code mapping errors back to inner state has to account for it.

**Expecting `AliasPath` to work on the way out.** It's check-only. Rebuilding a nested shape from flat fields isn't a rename. Needs a serialiser or a split output model.

**Aliasing an entire foreign vocab.** Thirty aliases often means the model is showing someone else's payload rather than your domain. Two models. One matching their shape, one matching yours, with a conversion between. Says more and stays readable.

## The failure mode to expect

If a thing about aliases isn't working, check `by_alias=True` first.

It accounts for most alias problems, it makes no error. The symptom. An API that accepts one rule and returns another. Looks like a config problem rather than a missing arg on a single call.

The second thing to check is `populate_by_name`. This Is what stops your own tests being able to make the model using the names you wrote.

## The convention decision

Behind the mechanics is one choice worth making on purpose rather than per model.

Does your API speak the wire's rule, or your language's? Both are defensible. Agreement is what matters. A mixed API is worse than either choice made badly.

If your consumers are browsers and JavaScript clients, camelCase on the wire is what they expect. An `alias_generator` on a shared base gives it to each model at once with no per-field work.

If your consumers are Python services, snake_case throughout is simpler and needs no aliases at all.

What makes trouble is deciding case by case. Some endpoints camelCase, some not, some models aliased and their nested models not. each consumer then needs to know which is which. No amount of docs makes that pleasant.

Make the choice once, express it in a base model. Let the exceptions be genuine exceptions rather than accidents.

## One thing to remember

If just one fact lives this module, make it `by_alias=True`.

Aliases configured just right still do nothing on output until that arg is passed, the failure is silent. The symptom looks like a config problem rather than a missing keyword on a single call. It's the first thing to check when aliases appear not to work.
''',
    [
        {"q": "You set `alias=\"publishedAt\"`. Why does `Module(published_at=...)` now fail?",
         "options": ["A bug", "By default the alias replaces the Python name as input", "Aliases are output-only", "It needs by_alias"],
         "answer": 1,
         "why": "The alias becomes the input name. `populate_by_name=True` restores the Python name as an accepted alternative, which is almost always what you want."},
        {"q": "Your API accepts camelCase but returns snake_case. What is missing?",
         "options": ["populate_by_name", "by_alias=True on the dump", "validation_alias", "An alias_generator"],
         "answer": 1,
         "why": "Aliases are not used for output unless requested. FastAPI does this for you on response models, which is why a manual dump elsewhere can behave differently."},
        {"q": "What is `AliasChoices` for?",
         "options": ["Choosing between models", "Accepting several input spellings, first one present wins", "Output formatting", "Nested paths"],
         "answer": 1,
         "why": "It is the clean way to run a rename: add the new name, keep the old, and clients migrate at their own pace with no branching in your code."},
        {"q": "What does `AliasPath(\"author\", \"name\")` do?",
         "options": ["Renames the field", "Pulls a value from a nested payload into a flat field", "Creates a nested model", "Sets a serialisation alias"],
         "answer": 1,
         "why": "Strings are keys and integers are indices, so a nested response flattens into your model. It is validation-only - there is no serialisation equivalent."},
    ],
)


# ---------------------------------------------------------------------------
# 22. Parsing JSON
# ---------------------------------------------------------------------------
topic(
    "parsing_json",
    "Parsing JSON",
    "In and Out",
    "Why model_validate_json beats json.loads plus model_validate - speed, error "
    "quality and fidelity.",
    _svg(_txt(38, 28, "json.loads", M, 8) + _arrow(66, 24, 82, 24) + _txt(112, 28, "dict", M, 8) +
         _arrow(112, 34, 112, 46) + _txt(112, 60, "model", M, 8) +
         _box(14, 66, 132, 18, S, A) + _txt(80, 79, "model_validate_json: one step", A, 8)),
    [
        ("One call instead of two",
         "<code>model_validate_json</code> parses and validates together, inside the "
         "Rust core, without building an intermediate dict.",
         '''import json
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    minutes: int

payload = '{"title": "Vectors", "minutes": 8}'

two_steps = Module.model_validate(json.loads(payload))
one_step = Module.model_validate_json(payload)

print("two steps:", two_steps)
print("one step :", one_step)
print("equal    :", two_steps == one_step)
print()
print("Same result. The second never materialises the dict.")'''),

        ("Malformed JSON is one exception, not two",
         "Going via <code>json.loads</code> means catching a "
         "<code>JSONDecodeError</code> separately. The direct call folds it into "
         "<code>ValidationError</code>.",
         '''import json
from pydantic import BaseModel, ValidationError

class Module(BaseModel):
    title: str
    minutes: int

broken = '{"title": "Vectors", "minutes": 8'      # missing brace

try:
    Module.model_validate(json.loads(broken))
except json.JSONDecodeError as e:
    print("via loads :", type(e).__name__, "- a different exception type")

try:
    Module.model_validate_json(broken)
except ValidationError as e:
    err = e.errors()[0]
    print("direct    :", err["type"])
    print("            ", err["msg"])
    print("position  :", err.get("ctx"))'''),

        ("One handler for both failure kinds",
         "Because syntax errors and validation errors arrive the same way, the code "
         "that deals with a bad request has one shape.",
         '''from pydantic import BaseModel, Field, ValidationError

class Module(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

def accept(raw: str):
    try:
        return Module.model_validate_json(raw), None
    except ValidationError as e:
        return None, [(".".join(str(p) for p in err["loc"]) or "_body", err["msg"])
                      for err in e.errors()]

for raw in ['{"title": "Vectors", "minutes": 8}',
            '{"title": "Vectors", "minutes": 8',
            '{"title": "no", "minutes": -1}']:
    model, problems = accept(raw)
    print(raw[:38])
    print("   ->", model if model else problems)'''),

        ("Decimals keep their exact text",
         "The JSON parser sees the digits as written. Going through Python floats "
         "loses that before validation ever runs.",
         '''import json
from decimal import Decimal
from pydantic import BaseModel

class Price(BaseModel):
    amount: Decimal

payload = '{"amount": 0.1}'

via_python = Price.model_validate(json.loads(payload))
direct = Price.model_validate_json(payload)

print("via json.loads    :", via_python.amount)
print("model_validate_json:", direct.amount)
print()
print("json.loads made a float first, and the float was already inexact.")
print("The direct parser read the characters 0.1 and kept them.")'''),

        ("Dumping and reloading",
         "The other direction is symmetric, and a JSON round trip is exact for every "
         "type Pydantic knows.",
         '''from datetime import date
from decimal import Decimal
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    published_on: date
    price: Decimal

m = Module(title="Vectors", published_on="2026-08-26", price="12.50")

wire = m.model_dump_json()
print("out :", wire)

back = Module.model_validate_json(wire)
print("in  :", back)
print("equal:", back == m)
print()
print("date and Decimal both survived the trip intact.")'''),

        ("Bare arrays and other shapes",
         "<code>TypeAdapter</code> gives the same one-step parsing for anything that "
         "is not a model.",
         '''from typing import List, Dict
from pydantic import BaseModel, TypeAdapter, ValidationError

class Lesson(BaseModel):
    name: str
    minutes: int

lessons = TypeAdapter(List[Lesson])

payload = '[{"name": "Direction", "minutes": "4"}, {"name": "Magnitude", "minutes": 6}]'
parsed = lessons.validate_json(payload)
print("parsed:", parsed)
print("out   :", lessons.dump_json(parsed).decode())

scores = TypeAdapter(Dict[str, float])
print("dict  :", scores.validate_json('{"maths": "4.5", "python": 4}'))

try:
    lessons.validate_json('[{"name": "X", "minutes": "soon"}]')
except ValidationError as e:
    print("error :", e.errors()[0]["loc"], e.errors()[0]["type"])'''),
    ],
    [
        "<code>model_validate_json</code> parses and validates in one pass inside the Rust core, without building an intermediate Python dict.",
        "Malformed JSON becomes a <code>ValidationError</code> with type <code>json_invalid</code>, so syntax and validation failures share one handler.",
        "The error context includes the position in the document, which matters for a large payload where “invalid JSON” alone is useless.",
        "<code>Decimal</code> is more faithful this way: the parser reads the digits as written, where <code>json.loads</code> has already produced an inexact float.",
        "<code>model_dump_json</code> is the matching direction, and a JSON round trip is exact for every type Pydantic knows.",
        "<code>TypeAdapter(...).validate_json()</code> gives the same benefits for bare arrays, dicts and other non-model shapes.",
    ],
    '''
title: Parsing JSON: One Step Instead of Two
intro: Why model_validate_json beats json.loads plus model_validate on speed, errors and fidelity.

## The habit worth changing

Most people parse JSON with the standard library and then pass the result to a model. That is two steps, and it works. It is also a habit worth changing, because Pydantic can do both steps in one call.

The method is model_validate_json. It reads the JSON string or bytes directly and validates as it goes. That brings three gains. It is faster, because the parsing happens in Rust. The error messages are better, because they refer to the original text. And it keeps number fidelity, so large integers and precise decimals do not get mangled on the way through Python.

This article explains the habit and why you might want to drop it. It covers speed, error quality and fidelity with numbers, one after another. It then looks at the other direction, turning a model back into JSON text. It also notes that bytes work as input, which matters when you read from a network socket or a file. The aim is to make the single-step version your default for JSON input, with a clear idea of why.

Almost every service parses JSON, so even a small gain here applies to nearly all your traffic. The change is tiny. It takes one method call in place of two. Yet it affects speed, error clarity and the accuracy of your numbers all at once. The article makes the case with concrete examples rather than claims, so you can see each benefit for yourself. For example, you will see the same bad input fail in both styles, and compare the messages. One points at the exact spot in the text. The other can only tell you that something is wrong. You will also learn the one situation where the two-step habit is still the better choice. After reading, you will know when to use each approach and why, instead of copying whichever one you saw last.

Real payloads rarely look like textbook examples. They arrive from browsers, mobile apps and other servers, each with its own habits. Some contain huge integers. Some contain numbers with many digits after the point. A parser that quietly rounds them can cause trouble that is very hard to trace. Seeing how each approach treats such values helps you choose with confidence, and the examples here use exactly those cases.

Most people write this:

```python
data = json.loads(raw)
model = Module.model_validate(data)
```

It works. The better form is:

```python
model = Module.model_validate_json(raw)
```

It isn't merely shorter. It's faster, makes better errors. Is more faithful with numbers. Three split reasons, and they compound.

## Speed

The two-step version parses JSON into Python objects. Dicts, lists, strings, floats. And then validates those objects, converting again into what the model wants.

each mid object is allocated and thrown away. For a large payload that is a lot of garbage created for no purpose.

`model_validate_json` parses and validates in a single pass inside `pydantic-core`, the Rust engine. It reads the JSON text and makes the final values right, skipping the mid form fully.

The saving grows with payload size. For a small request body it's unimportant. For a large doc, or a high-throughput endpoint, it's a real gap for a change that makes the code shorter.

## Error quality

This is the arg that matters most day to day.

With `json.loads`, malformed JSON raises `json.JSONDecodeError`. A other exception, from a other library, that knows nothing about your model. Your handler needs two `except` clauses making two shapes of error response. The JSON one has no field data because there are no fields yet.

`model_validate_json` folds it in. Malformed JSON turns a `ValidationError` with the type `json_invalid`, arriving through just the same channel as a missing field or a failed constraint.

That means one handler. The function that turns a `ValidationError` into a 422 response now covers syntax errors too, without a special case.

The error also carries the **spot** in the doc. For a missing comma four hundred lines into a config file, being told the line and column is the gap between a fix and a search.

## Fidelity with numbers

The subtlest of the three, and the one that costs money.

`json.loads` turns `0.1` into a Python float. That is what JSON numbers are in Python. The float is already inexact at that moment. Handing it to a `Decimal` field faithfully preserves the wrong value.

`model_validate_json` reads the characters. When the target is a `Decimal`, it can make it from the exact text. `0.1` in the doc turns `Decimal("0.1")` rather than the float's guess.

For anything money, that isn't a micro-tuning. It's the gap between correct and quietly wrong. It also means the advice from the types module ("send money as a string") has a companion. Even when a partner sends money as a JSON number, parsing right recovers more of it than going via Python.

## The other direction

`model_dump_json()` is the matching call, and it's even for the same reasons. It serialises from the model's data straight to text, without building an mid dict.

A round trip is exact for each type Pydantic knows. A `date` turns an ISO string and parses back to the same `date`. A `Decimal` turns a string and returns as the same `Decimal`. A UUID lives. This makes JSON a fair format for caching checked objects. Makes equality assertions in tests trustworthy.

## Bytes work too

Both methods accept `bytes` and `str`. This Is what an HTTP body really is.

That saves a decode step, and avoids a class of bug where the wrong encoding is assumed. If you're reading a request body or a file, pass the bytes straight in.

## Non-model shapes

Not each payload is an object. `TypeAdapter` gives the same one-step parsing for anything you can annotate:

```python
TypeAdapter(List[Lesson]).validate_json(payload)
TypeAdapter(Dict[str, float]).validate_json(payload)
```

Same speed gain, same error handling, same fidelity. And `dump_json` in the other direction, which returns `bytes`.

Build the adapter once at module level. Making one compiles a schema. Doing that inside a loop is a real and easily-missed speed mistake.

## When to keep the two steps

There are legitimate reasons to parse apart.

**You need the raw structure first.** Inspecting a `type` field to choose a model, logging the payload, or routing on a thing before checking. Though a discriminated union often drops the first of those.

**The input isn't JSON.** YAML, TOML and msgpack all give Python objects. `model_validate` is the right entry point for them.

**You already have a dict** from a DB driver, another library, or your own code. There's nothing to parse.

The rule is simple: if you're holding JSON text or bytes, use `model_validate_json`. If you're holding Python objects, use `model_validate`. The mistake is converting text to objects yourself purely to hand them to a checker that would rather have had the text.

## In practice with a framework

FastAPI already does this for request bodies. An endpoint annotated with a model gets the fast path without you asking.

Where it matters in use code is all over else. Reading a config file, consuming a queue message, calling another service and checking the response, loading a fixture in a test. Those are all places where the two-step habit is common and the one-step version is strictly better.

## Strictness and JSON

The strict-mode module noted that a strict model checking from JSON still accepts the string forms JSON has no option to. A date as text, say.

That action depends on Pydantic knowing the input was JSON. This It only does when you use `model_validate_json`. Parse with `json.loads` first and that context is gone. The model sees a Python string where a `date` was wanted. In strict mode refuses it.

So the two-step form isn't merely slower, it can be *stricter in the wrong way*. Another reason to hand the text straight over.

## Large payloads

For very large docs, two things are worth knowing.

Parsing is a single pass and memory-bounded by the result rather than by mid objects. `model_validate_json` uses usefully less memory than the two-step form on a big doc.

There's no streaming. The whole doc is parsed before check ends. A hundred-megabyte file is a hundred megabytes in memory. If that matters, the answer is at a other level. A streaming JSON reader making records, each checked on their own or in batches with a `TypeAdapter`.

## Reading from a file

The natural spelling reads bytes and hands them straight over:

```python
config = Settings.model_validate_json(Path("config.json").read_bytes())
```

No decode step, no `json.load`, and a malformed file makes a `ValidationError` naming the spot rather than a `JSONDecodeError` from elsewhere.

For a config file that is a truly nice pattern. One call, one exception type. Errors that say which key was wrong and where in the file it was.

## Other formats

Only JSON gets the fast path. Only JSON has a parser inside the core.

YAML, TOML and msgpack all go through their own libraries. This Give Python objects. This Then go to `model_validate`. That is the correct shape for those formats and there's nothing to optimise. But it does mean a YAML config gets none of the fidelity gain for decimals. A syntax error arrives as that library's exception.

If exactness matters in a YAML config, quoting the number so it arrives as a string is the pragmatic fix.

## What to take away

The habit is small: when you're holding JSON text or bytes, hand it to Pydantic rather than to `json.loads`.

It's faster, because it skips an entire mid form. It makes better errors, because syntax and check failures arrive through one channel with spots attached. It's more faithful, because decimals keep the digits as written. And it's shorter to write.

Very few changes improve four things at once for one fewer line of code.

## Summary

`model_validate_json` for JSON text or bytes. `model_validate` for Python objects. One pass in Rust rather than two with garbage in between. Malformed JSON turns a `ValidationError` with a spot. One handler covers syntax and check alike. And decimals keep the precision that a trip through Python floats would have destroyed.

`model_dump_json` on the way out, `TypeAdapter` for shapes that aren't models. Build adapters once rather than per call.

## Where this fits

This is a small change with an unusually good ratio. It applies in more places than request handling.

Reading a config file. Consuming a queue message. checking another service's response. Loading a test fixture. Anywhere JSON text or bytes are in hand and a model is about to be built from them.

In each of those the two-step habit is common. In each of them the one-step form is faster, makes better errors and keeps more precision. It's worth grepping for `json.loads` once and seeing how many of them are at once followed by a check call.


## Mistakes people make

**Parsing first out of habit.** `json.loads` followed at once by `model_validate` is the shape to grep for. each instance of it's slower, makes worse errors and loses decimal precision checked with handing the text over right.

**Catching two exception types.** Code with an `except JSONDecodeError` beside an `except ValidationError` is code that parsed apart. checking the text right merges both into one channel and one handler.

**Decoding bytes needlessly.** An HTTP body is bytes and both methods accept bytes. Decoding to `str` first adds a step and a chance to assume the wrong encoding.

**Expecting streaming.** There's none. The whole doc is parsed before check ends. A very large file is fully in memory. Streaming needs a other tool making records, each checked on their own or in batches.

**given the fast path applies to YAML or TOML.** Only JSON has a parser inside the core. Other formats go through their own libraries and give Python objects. This Then take the plain route. Including losing decimal exactness on the way.

**Using it when you already have a dict.** There's nothing to parse. The rule is simply which you're holding. Text or bytes go to `model_validate_json`, Python objects go to `model_validate`.

## One line, four improvements

Speed, because an entire mid form is skipped. Errors, because syntax and check failures arrive through one channel with spots attached. Fidelity, because decimals keep the digits as written. Strictness, because the parser knows the input was JSON and applies the right rules.

All of it from handing Pydantic the text instead of parsing it first. Which is also less code than the option.

## Why the habit persists

The two-step form isn't the result of anyone deciding it was better. It's what you write when you learn `json` before you learn Pydantic. This Is the order nearly everybody learns them in.

`json.loads` is the obvious way to turn text into data. Once the data exists, checking it's the obvious next step. Both halves are fair and the mix is worse than either author intended.

That is worth naming because it shows why the pattern is all over, including in a lot of docs and answers online. Why changing it's a matter of noticing rather than of understanding.

The check takes a minute: search a code for `json.loads` and look at the line after each one. Wherever it's a check call, the two lines collapse into one that is faster, more precise about numbers. Makes errors that say where in the doc the problem was.

There's rarely a reason to keep the two-step version once seen. Unless a thing truly needs the raw structure in between. This Is a real case and a small one.
''',
    [
        {"q": "What does `model_validate_json` do with malformed JSON?",
         "options": ["Raises JSONDecodeError", "Raises ValidationError with type json_invalid, including a position", "Returns None", "Silently ignores it"],
         "answer": 1,
         "why": "Syntax failures arrive through the same channel as validation failures, so one handler covers both - and the context names where in the document the problem is."},
        {"q": "Why is `model_validate_json` more faithful for a `Decimal` field?",
         "options": ["It rounds better", "json.loads makes a float first, losing precision before validation runs", "Decimals are unsupported otherwise", "It is not"],
         "answer": 1,
         "why": "The direct parser reads the digits as written and can build the Decimal from exact text. Going via Python, the value is already an inexact float when Pydantic sees it."},
        {"q": "You already have a dict from a database driver. Which method?",
         "options": ["model_validate_json", "model_validate", "Either", "TypeAdapter"],
         "answer": 1,
         "why": "There is no JSON text to parse. The rule is: text or bytes go to `model_validate_json`, Python objects go to `model_validate`."},
        {"q": "Where should a `TypeAdapter` be constructed?",
         "options": ["Inside the function that uses it", "Once at module level", "Per request", "It does not matter"],
         "answer": 1,
         "why": "Constructing one compiles a schema. Doing that inside a loop or per call is a real performance mistake that is easy to miss."},
    ],
)


# ---------------------------------------------------------------------------
# 23. Custom serializers
# ---------------------------------------------------------------------------
topic(
    "custom_serializers",
    "Custom Serializers",
    "In and Out",
    "Changing what comes out without changing what goes in - per field, per model, "
    "and only when the default is genuinely wrong.",
    _svg(_box(18, 18, 124, 20, S, A) + _txt(80, 32, "Decimal('12.50')", A, 8) +
         _arrow(80, 42, 80, 54) +
         _box(18, 56, 124, 20, S) + _txt(80, 70, '"£12.50"', M, 8)),
    [
        ("A field serialiser",
         "<code>@field_serializer</code> replaces the output for one field. The input "
         "side is untouched.",
         '''from decimal import Decimal
from pydantic import BaseModel, field_serializer

class Price(BaseModel):
    amount: Decimal

    @field_serializer("amount")
    def show_money(self, value: Decimal) -> str:
        return "£%.2f" % value

p = Price(amount="12.5")

print("on the object:", p.amount, "(a", type(p.amount).__name__ + ")")
print("dumped       :", p.model_dump())
print("as json      :", p.model_dump_json())'''),

        ("Only the output changes",
         "Validation still produces the real type, so arithmetic and comparisons keep "
         "working. Serialisation is the last step, not a conversion.",
         '''from decimal import Decimal
from pydantic import BaseModel, field_serializer

class Basket(BaseModel):
    unit: Decimal
    quantity: int

    @field_serializer("unit")
    def money(self, v: Decimal) -> str:
        return "£%.2f" % v

b = Basket(unit="4.25", quantity=3)

print("still a Decimal:", b.unit * b.quantity)
print("comparison     :", b.unit > Decimal("4"))
print("but dumped     :", b.model_dump())'''),

        ("Different output for JSON and Python",
         "<code>when_used</code> restricts a serialiser to one mode, so internal dumps "
         "keep the real object.",
         '''from datetime import date
from pydantic import BaseModel, field_serializer

class Module(BaseModel):
    title: str
    published_on: date

    @field_serializer("published_on", when_used="json")
    def pretty(self, value: date) -> str:
        return value.strftime("%d %B %Y")

m = Module(title="Vectors", published_on="2026-08-26")

print("mode=python:", m.model_dump())
print("mode=json  :", m.model_dump(mode="json"))
print("json string:", m.model_dump_json())
print()
print("The Python dump keeps a real date for code that needs one.")'''),

        ("Serialising a whole model",
         "<code>@model_serializer</code> replaces the entire output, which is how you "
         "emit a shape that is not simply your fields.",
         '''from pydantic import BaseModel, model_serializer

class Module(BaseModel):
    title: str
    minutes: int
    track: str

    @model_serializer
    def as_envelope(self) -> dict:
        return {
            "type": "module",
            "id": self.title.lower().replace(" ", "-"),
            "attributes": {"title": self.title,
                           "minutes": self.minutes,
                           "track": self.track},
        }

m = Module(title="Dot Product", minutes=11, track="maths")
print(m.model_dump())
print()
print(m.model_dump_json(indent=2))'''),

        ("Hiding a value instead of formatting it",
         "A serialiser is one way to redact. <code>SecretStr</code> and "
         "<code>Field(exclude=True)</code> are usually better, and the comparison is "
         "worth seeing.",
         '''from pydantic import BaseModel, Field, SecretStr, field_serializer

class User(BaseModel):
    name: str
    email: str
    token_a: str                       # redacted by a serialiser
    token_b: SecretStr                 # hidden by its type
    token_c: str = Field(exclude=True)  # never serialised at all

    @field_serializer("token_a")
    def mask(self, v: str) -> str:
        return v[:4] + "…" + v[-2:]

u = User(name="Ada", email="ada@vizlearn.in",
         token_a="tok_live_abcdef", token_b="tok_live_ghijkl",
         token_c="tok_live_mnopqr")

print("repr :", u)
print()
print("dump :", u.model_dump())'''),

        ("When the default was already right",
         "Most custom serialisers are display formatting in the wrong layer. Compare "
         "what a consumer can do with each.",
         '''from datetime import date
from pydantic import BaseModel, field_serializer

class Pretty(BaseModel):
    on: date

    @field_serializer("on")
    def fmt(self, v: date) -> str:
        return v.strftime("%d %B %Y")

class Plain(BaseModel):
    on: date

d = date(2026, 8, 26)
print("pretty:", Pretty(on=d).model_dump_json())
print("plain :", Plain(on=d).model_dump_json())
print()
print("A client can sort, filter and localise the second.")
print("The first has to be parsed back, and only by an English reader.")'''),
    ],
    [
        "<code>@field_serializer(\"x\")</code> replaces the output for one field. Validation and the in-memory type are unaffected.",
        "The method takes <code>self</code> and the field's value, and returns whatever should appear in the output.",
        "<code>when_used=\"json\"</code> limits a serialiser to JSON output, so <code>model_dump()</code> keeps the real Python object.",
        "<code>@model_serializer</code> replaces the whole output, which is how you emit an envelope or a shape that is not just your fields.",
        "A serialiser changes the output but <em>not</em> the schema, so the documented type and the actual output can silently disagree unless you set <code>return_type</code>.",
        "For secrets prefer <code>SecretStr</code> or <code>Field(exclude=True)</code>; a masking serialiser still leaks the value into <code>repr</code> and logs.",
    ],
    '''
title: Custom Serializers: Changing What Comes Out
intro: Per-field and per-model output control, and the strong arg for not using it.

## What they do

Pydantic knows how to turn most values into JSON. Sometimes the default is not what you want. A datetime should go out in a particular format. A set should become a sorted list. A secret value should be masked. A serializer lets you control what comes out.

The important point is that a serializer changes only the output. The data inside the model stays exactly as it was validated. Nothing about how the object is stored or used in your code changes. You are choosing how it looks at the moment it leaves.

This article explains what serializers do and what they leave alone. It shows that you can get two different outputs from one serializer, depending on whether you dump to Python or to JSON. You will see how to serialise a whole model rather than a single field, which is useful for reshaping the output. The last section covers the schema problem, since a serializer can change the type a client sees, and your documentation needs to say so. It is the tool to reach for when the default output is almost right.

Use a serializer only when the default output is not what you want, because every one adds code you must maintain. The article shows the common cases, so you can tell quickly whether you need one at all. Often the answer is a small function of three lines. It also explains how serializers interact with the exclusion options you met earlier, so your output stays predictable when you combine them.

Think of a serializer as the last step before data leaves your program. It is the right place for presentation choices such as date formats, rounding and masking. It is the wrong place for business rules, which belong in validation. Keeping that split clear makes models much easier to reason about, and it keeps the output code short and predictable.

Pydantic's defaults are good: dates become ISO strings, decimals become strings, enums become values, nested models become nested objects. For most fields there's nothing to decide.

When the default is truly wrong, `@field_serializer` replaces the output for one field:

```python
@field_serializer("amount")
def show_money(self, value: Decimal) -> str:
    return "£%.2f" % value
```

The method takes `self` and the value, and returns what should appear.

## Only the output changes

This is the key property. A serialiser doesn't change check. Doesn't change what the field holds.

`p.amount` is still a `Decimal`. Math works, checks work. Each rule you attached still ran. The serialiser is the last step on the way out, not a conversion applied to the model.

That split is what makes the feature safe. You aren't weakening the model to meet a consumer's format preference.

## Two modes, two outputs

`when_used` restricts a serialiser to one direction:

`"always"` is the default. `"json"` applies only to `model_dump_json()` and `model_dump(mode="json")`. `"unless-none"` skips it for null values.

The `"json"` case is the handy one. It lets `model_dump()` keep a real `date` for code inside your program while JSON output gets what format a consumer needs. Without it, a formatting serialiser makes the Python dump useless for anything that wanted the object.

## Serialising the whole model

`@model_serializer` replaces the entire output:

```python
@model_serializer
def as_envelope(self) -> dict:
    return {"type": "module", "attributes": {...}}
```

This is for shapes that aren't simply your fields. A JSON:API envelope, a legacy format you must emit, a payload where the structure differs from your inner one.

It's powerful and it's a big hammer. each field is now your job. A field added to the model doesn't appear in the output until somebody remembers to add it to the serialiser. That divergence is just the drift models exist to prevent.

A `mode="wrap"` variant receives a handler that makes the default output, letting you take that and adjust it rather than rebuilding it. That is much safer. New fields still flow through:

```python
@model_serializer(mode="wrap")
def add_meta(self, handler):
    data = handler(self)
    data["_type"] = "module"
    return data
```

Prefer the wrap form when you're boosting rather than replacing.

## The schema problem

Here is the sharp edge, and it's easy to miss.

A serialiser changes the output. It doesn't change the schema. So a `Decimal` field serialised as `"£12.50"` still appears in the made schema as a decimal, your API docs says one thing, and the endpoint returns another.

For a public API that is a real defect. Made clients will give a type that doesn't match the data they receive.

`return_type` fixes it:

```python
@field_serializer("amount", return_type=str)
```

Now the output schema reports a string. The docs matches reality. Set it when the serialised type differs from the field type. This Is most of the time.

## Secrets: a serialiser is the weakest option

Masking a token with a serialiser is a common idea and the worst of the three on hand.

`@field_serializer` making `tok_…ef` keeps the value out of dumps and leaves it in `repr`, in logs, in tracebacks. In any code that reads the field.

`SecretStr` hides it from `repr` and needs `.get_secret_value()`. This Makes access deliberate and greppable.

`Field(exclude=True)` keeps it out of each output fully.

For anything truly secret, use the type and the exclusion. Reach for a serialiser only when you want a *partial* value in the output on purpose. Showing the last four digits of a card. This Is a product choice rather than a security one.

## The argument against most custom serialisers

Most custom serialisers are display formatting that has ended up in the wrong layer.

`"26 August 2026"` is a formatting choice. It assumes English, a date order. A reader rather than a program. A client receiving it can't sort by it, can't filter on it, can't show it in another language. Has to parse it back to do anything handy.

`"2026-08-26"` is data. each client can sort it, compare it and format it but that client's user needs.

The same arg applies to currency symbols, thousands separators, scaled times ("3 days ago") and rounded numbers. All of them are choices that belong where the audience is known. This Is the presentation layer, not the data model.

So the honest guidance: before writing a serialiser, ask whether the default was wrong or merely unseen. If it's being changed for a human reader, that logic probably belongs closer to the human.

## When they are genuinely right

**Emitting a legacy format** you don't control and can't change.

**Redacting on purpose**, where a partial value is the intended product action.

**Wrapping in an envelope** needed by a specification, best done with `mode="wrap"`.

**finding a form** that is costly to store but cheap to derive. Here A found field would be the option.

**Interoperating with a thing exact** &mdash; a system that wants timestamps in milliseconds, or booleans as `"Y"`/`"N"`.

Each of those is a real constraint from outside, rather than a preference from inside.

## The info argument

Both decorators accept an optional `info` param carrying `mode`, `context` and the exclusion settings in force.

`mode` lets one serialiser behave differently for Python and JSON output without needing `when_used`.

`context` is the notable one. It's a dict passed to the dump call. This Makes output dependent on a thing the model doesn't know:

```python
@field_serializer("salary")
def maybe_hide(self, v, info):
    if (info.context or {}).get("role") != "hr":
        return None
    return v
```

Used carefully that is a clean answer to field-level visibility rules. Used freely it makes an endpoint whose output can't be predicted from the model. Split output models per audience are easier to reason about and to doc.

## Serialising unusual types

The other legitimate reason to write a serialiser is a field whose type Pydantic has no view about. A third-party object accepted via `arbitrary_types_allowed`.

Such a field has no default output. A dump either fails or makes a thing unhelpful. A serialiser turning it into a dict or a string isn't a formatting preference. It's the only way the model can be serialised at all.

If you find yourself doing this for a type used in a few models, the better shape is a custom type that knows how to serialise itself. The knowledge lives with the type rather than being repeated in each model that holds one.

## Testing what you emit

Custom output is worth testing right. It's the part of a model that no other test exercises.

check tests make models. They don't check what comes out. A serialiser can be broken for months while each check test passes.

The test is short &mdash; build a model, dump it, assert on the result &mdash; and it's the only thing standing between a formatting change and a silently altered API response.

Assert on `model_dump()` and `model_dump_json()` apart when `when_used` is involved. That is just the case where they differ.

## The decision, restated

Before writing one, three questions.

**Is the default really wrong, or just unseen?** ISO dates and decimal strings look odd and are correct.

**Is this for a machine or a person?** Machines want data. People want formatting. That belongs where the person is.

**Will the schema still be true?** If not, set `return_type`, or you're publishing a doc that lies about your own output.

Most proposed serialisers fail one of those. This Is the reason this module argues against its own subject as much as for it.

## Summary

`@field_serializer` for one field, `@model_serializer` for the whole output, `mode="wrap"` when boosting rather than replacing so new fields still flow through.

`when_used="json"` keeps Python dumps handy. `return_type` keeps the schema honest. `info.context` makes output gated when that is truly needed.

For secrets prefer `SecretStr` and `Field(exclude=True)`. And reach for a serialiser when an external constraint demands a shape. Not when a default merely looks unseen.

## What to remember

output is the last thing that happens and the first thing a consumer sees.

Pydantic's defaults are chosen so that output is data. Sortable, close, parseable, unambiguous across locales. Most reasons to replace them turn out to be formatting for a human. Humans are downstream of the layer that knows who they're.

replace when a thing outside truly demands a shape. Set `return_type` so the schema keeps telling the truth. And test what you emit. No other test does.


## Mistakes people make

**Formatting for a person in a data layer.** Covered at length. Still the most common. A date rendered as "26 August 2026" can't be sorted, filtered or localised by anyone receiving it.

**Losing `return_type`.** The output changes, the schema doesn't. Your docs quietly starts showing a thing the endpoint no longer returns. made clients then give a type that doesn't match the data. The failure surfaces in someone else's code.

**Using a plain `@model_serializer` for a small addition.** Replacing the entire output to add one key means each field is now hand-kept. A field added to the model six months later never appears. `mode="wrap"` adds the key and lets all else flow through untouched.

**Masking a secret with a serialiser and stopping there.** The dump is clean and the value is still in `repr`, still in logs, still in tracebacks, still readable by any code holding the model. `SecretStr` and `Field(exclude=True)` address the parts a serialiser can't.

**Not testing the output.** check tests make models. They never look at what comes out. A serialiser can be broken for months while the suite stays green. The first person to notice is a consumer.

**based on context that isn't always passed.** A serialiser reading `info.context` needs a sensible default for each call that doesn't supply one, including the ones in tests and the ones a framework makes inside. `(info.context or {})` rather than `info.context[...]` is the gap between a graceful default and a `TypeError` during a response.

## The test

Is the default wrong for a machine, or merely unformatted for a person?

Only the first is a serialiser's job. all else. Currency symbols, readable dates, scaled times, rounded numbers. Is a choice about an audience. Belongs where the audience is known.

Applying that one question honestly drops most proposed serialisers. Makes the left ones easy to justify.

## A final framing

It helps to think of output as the boundary in the other direction.

check is where you stop trusting the outside world and convert its text into your types. output is where you stop given your types and give a thing the outside world can read.

Both are conversions at an edge. Both work best when they convert to a thing *neutral*. check doesn't try to guess what a caller meant. It accepts unambiguous readings and refuses the rest. output should be symmetrical. Emit data with a single unambiguous reading, and let the consumer decide how to present it.

A custom serialiser that formats for a human breaks that symmetry. It takes a value with one meaning and makes one with a presentation baked in. This The next layer has to undo before it can do anything else.

That is the underlying reason the advice in this module runs against its own subject. The feature is well designed and at times key. It's just that most of the reasons people reach for it are reasons to do the work one spot else.
''',
    [
        {"q": "Does a `@field_serializer` change what the field holds in memory?",
         "options": ["Yes", "No - only the output; validation and the stored type are unaffected", "Only in JSON mode", "It replaces the validator"],
         "answer": 1,
         "why": "It runs on the way out. The attribute is still the validated type, so arithmetic and comparisons keep working - which is what makes the feature safe."},
        {"q": "A Decimal field is serialised as \"£12.50\". What does the schema say?",
         "options": ["string", "Still a decimal, unless you set return_type", "It errors", "Nothing"],
         "answer": 1,
         "why": "Serialisers change output but not the schema, so docs and generated clients describe a type the endpoint no longer returns. `return_type` keeps them honest."},
        {"q": "Why prefer `@model_serializer(mode=\"wrap\")` over the plain form?",
         "options": ["It is faster", "The handler produces the default output, so newly added fields still flow through", "It is required", "It supports JSON only"],
         "answer": 1,
         "why": "The plain form makes every field your responsibility, so a field added later silently never appears. Wrapping augments the default rather than replacing it."},
        {"q": "What is the argument against serialising a date as \"26 August 2026\"?",
         "options": ["It is slower", "It is display formatting: a client cannot sort, filter or localise it", "Dates cannot be formatted", "It breaks validation"],
         "answer": 1,
         "why": "ISO output is data every client can work with. Formatting assumes a language and a reader, and belongs in the layer that knows who the audience is."},
    ],
)


# ---------------------------------------------------------------------------
# 24. JSON Schema
# ---------------------------------------------------------------------------
topic(
    "json_schema",
    "JSON Schema",
    "In and Out",
    "The document your model generates - and the reason FastAPI can document your "
    "API without you writing any docs.",
    _svg(_box(14, 20, 56, 24, S, A) + _txt(42, 36, "model", A, 8) +
         _arrow(74, 32, 92, 32) +
         _box(96, 20, 50, 24, S) + _txt(121, 36, "schema", M, 8) +
         _arrow(121, 48, 121, 60) + _txt(80, 74, "docs / clients / forms", M, 8)),
    [
        ("What a model already knows",
         "<code>model_json_schema()</code> turns the annotations into a JSON Schema "
         "document. Nothing extra was written to produce it.",
         '''import json
from pydantic import BaseModel, Field

class Module(BaseModel):
    title: str = Field(min_length=3, description="Shown as the page heading.")
    minutes: int = Field(default=10, gt=0, le=180)
    published: bool = False

print(json.dumps(Module.model_json_schema(), indent=2))'''),

        ("Constraints become schema keywords",
         "Every constraint has a standard equivalent, which is why a constraint is "
         "worth more than an equivalent validator.",
         '''import json
from pydantic import BaseModel, Field, field_validator

class ByConstraint(BaseModel):
    minutes: int = Field(gt=0, le=180)
    title: str = Field(min_length=3, max_length=60)

class ByValidator(BaseModel):
    minutes: int
    title: str

    @field_validator("minutes")
    @classmethod
    def positive(cls, v):
        if not 0 < v <= 180:
            raise ValueError("out of range")
        return v

for cls in (ByConstraint, ByValidator):
    props = cls.model_json_schema()["properties"]
    print(cls.__name__)
    print("   minutes:", json.dumps(props["minutes"]))
    print("   title  :", json.dumps(props["title"]))'''),

        ("Nested models become $defs",
         "A reused model appears once as a definition and is referenced, which is what "
         "lets a generated client produce a named type.",
         '''import json
from typing import List
from pydantic import BaseModel

class Author(BaseModel):
    name: str
    email: str

class Module(BaseModel):
    title: str
    author: Author
    reviewers: List[Author]

schema = Module.model_json_schema()
print("properties:")
for name, spec in schema["properties"].items():
    print("   %-11s %s" % (name, json.dumps(spec)))
print()
print("$defs:", list(schema["$defs"]))
print()
print("Author is defined once and referenced twice.")'''),

        ("Two modes: what it takes, what it gives",
         "Computed fields appear only in the serialisation schema, because they are "
         "output and never input.",
         '''import json
from pydantic import BaseModel, computed_field

class Module(BaseModel):
    title: str
    minutes: int

    @computed_field(description="Reading time with a margin.")
    @property
    def estimated(self) -> int:
        return round(self.minutes * 1.2)

for mode in ("validation", "serialization"):
    props = Module.model_json_schema(mode=mode)["properties"]
    print("%-14s %s" % (mode, list(props)))

print()
print("An input model must not advertise a field callers cannot send.")'''),

        ("Literals and enums become choices",
         "This is the concrete payoff from the enums module: a client can render a "
         "dropdown, and a pattern gives it nothing to work with.",
         '''import json
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field

class Track(str, Enum):
    MATHS = "maths"
    PYTHON = "python"

class M(BaseModel):
    a: Literal["draft", "published"]
    b: Track
    c: str = Field(pattern=r"^(draft|published)$")

schema = M.model_json_schema()
for name, spec in schema["properties"].items():
    print("%-3s %s" % (name, json.dumps(spec)))
print()
print("$defs:", json.dumps(schema.get("$defs", {})))'''),

        ("Adding what the annotations cannot say",
         "<code>json_schema_extra</code> attaches anything the schema supports but "
         "Pydantic has no annotation for.",
         '''import json
from pydantic import BaseModel, ConfigDict, Field

class Module(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"examples": [{"title": "Vectors", "minutes": 8}]})

    title: str = Field(
        min_length=3,
        description="Shown as the page heading.",
        examples=["Dot Product", "Eigenvalues"],
        json_schema_extra={"x-editable": True},
    )
    minutes: int = Field(default=10, gt=0)

print(json.dumps(Module.model_json_schema(), indent=2))'''),
    ],
    [
        "<code>model_json_schema()</code> generates a standard JSON Schema document from the annotations, constraints and metadata you already wrote.",
        "Constraints map to schema keywords: <code>gt</code> to <code>exclusiveMinimum</code>, <code>min_length</code> to <code>minLength</code>, <code>pattern</code> to <code>pattern</code>. A validator maps to nothing.",
        "Nested models become entries in <code>$defs</code> and are referenced, so a reused model becomes a named type in a generated client.",
        "<code>mode=\"validation\"</code> describes what the model accepts; <code>mode=\"serialization\"</code> describes what it emits, including computed fields.",
        "<code>Literal</code> and <code>Enum</code> become <code>enum</code>, which documentation and form builders can render as a set of choices.",
        "<code>description</code>, <code>examples</code> and <code>json_schema_extra</code> flow straight into the document &mdash; the cheapest API documentation available.",
    ],
    '''
title: JSON Schema: The Document Your Model Already Wrote
intro: What the made schema holds, and why it's the reason Pydantic is all over.

## The output you did not write

Every Pydantic model can describe itself as a JSON Schema. You did not write that document. It comes from the field names, the types, the constraints and the defaults you already declared. The model is the single source of truth, and the schema follows from it.

That matters because many tools read JSON Schema. API documentation uses it. Form builders use it. Code generators and validators in other languages use it. FastAPI builds its OpenAPI docs from it. When your model changes, the schema changes with it, so the documentation does not drift.

This article starts with the output you never wrote, and what it looks like. It covers what reads the schema, and why that makes it more than a curiosity. It then compares constraints with validators in concrete terms, since the schema can express the first but usually not the second. You will see how definitions and references keep nested models tidy. The last section covers the two modes, one for validation and one for serialisation, which can produce different schemas for the same model.

The schema is the bridge between your Python code and everything else that talks to your service. A front-end developer can read it. A tester can generate cases from it. A partner can validate their own payloads against it before they send anything. This article shows what that document contains and how closely it follows the model. It also shows where the two part ways, because some rules written in Python cannot be expressed in a schema at all. Knowing where the line falls tells you what your documentation really promises. You will finish with a clear view of what is described for free and what you must explain yourself, which helps you keep your documentation honest as the model grows.

`Module.model_json_schema()` returns a dict that is a valid JSON Schema doc. Types, needed fields, defaults, constraints, descriptions, and meanings for nested models.

You wrote none of it. It's derived fully from the annotations, `Field` args and docstrings already in the class.

This is quietly the reason Pydantic became a dependency of half the modern Python ecosystem. check is handy. A *machine-readable description of your data that can't drift from the code* is what other tools can build on.

## What reads it

**FastAPI** turns these schemas into your OpenAPI doc. This Turns the interactive docs at `/docs`. The descriptions you wrote on fields appear next to those fields. The examples pre-fill the request form. The constraints show as documented limits.

**Client gens** turn OpenAPI into typed clients in TypeScript, Go, Java and the rest. The quality of that made client is a direct function of the quality of your schema.

**LLM tooling** uses schemas to constrain structured output. The schema tells the model what shape to answer in. The same model then validates the answer.

**Form builders and checkers** on the other side of the wire read the same doc. A browser can enforce your `minLength` before a request is ever sent.

One class meaning feeds all of them.

## Constraints versus validators, concretely

This is the strongest hands-on arg in the whole track. The schema is where you can see it.

`Field(gt=0, le=180)` makes `"exclusiveMinimum": 0, "max": 180`. A made client knows the range. The docs states it. A form can enforce it.

A `field_validator` that checks the same thing makes **nothing**. The schema says `"type": "int"` and the rule is invisible to each consumer. It's still enforced. A bad value is still rejected. But the caller only finds out by being rejected.

Same enforcement, fully other experience for whoever is calling you. That is why the guidance has been. Express a rule as a constraint when a constraint can express it.

The same holds for `Literal` against a `pattern`. A `Literal` turns `"enum": ["draft", "published"]` and a client can render a dropdown. A pattern matching the same two values turns a regular formula the client can't do anything with.

## Definitions and references

A nested model appears once in `$defs` and is referenced with `$ref` wherever it's used.

That matters for made clients: a referenced meaning often turns a named type in the target language. `Author` used in two fields turns one `Author` type used twice, rather than two anonymous objects that happen to match.

It also keeps the doc small when a model is reused heavily. It's why recursive models give a schema at all. A self-link is just a `$ref` back to the same meaning.

## The two modes

`model_json_schema(mode="check")` is the default and shows what the model **accepts**.

`mode="output"` shows what it **emits**.

They differ in real ways. Found fields appear only in the output schema. They're output and can never be supplied. A field with `exclude=True` appears in check and not output. output aliases apply to one and check aliases to the other.

Frameworks pick the right one for you: FastAPI uses the check schema for request bodies and the output schema for response models. Knowing the gap matters when you make a schema yourself and wonder why a field is missing.

## Metadata is the cheap win

`description`, `title` and `examples` on a field change no action and flow straight into the doc.

For anything with consumers beyond yourself, this is the highest-value writing you can do per character. A field called `weight` needs a description. Of what, in what unit? A field called `title` doesn't.

`examples` deserve given focus because they populate the interactive docs's request form. A developer trying your API for the first time gets a working request they can send, rather than an empty box. That gap shows up in how many of them succeed.

`json_schema_extra` attaches anything else the schema format supports that Pydantic has no dedicated arg for. Vendor extensions like `x-` keys, or keywords from a newer draft. It takes a dict, or a callable that receives and modifies the made schema.

## What does not translate

Some things simply can't be expressed in JSON Schema, and knowing which keeps expectations right.

**checker logic.** Any Python has no schema equal.

**Cross-field rules.** A `model_validator` enforcing "end after start" has no form. doc it in the model's docstring. This Turns the schema's description. At least a human reading the docs learns about it.

**Custom output.** As the previous module covered, a serialiser changes output without changing the schema unless you set `return_type`.

Where a rule can't be expressed, the honest thing is to show it in prose so the docs isn't silently incomplete.

## A habit worth adopting

Print the schema for a model you've just written. It takes one line. It shows you what your consumers will really see.

Constraints you thought you had documented and didn't. Fields with no description whose names aren't self-explanatory. A `pattern` where a `Literal` would have made a set of choices. A needed field you meant to make optional.

It's the fastest review on hand for an API model. It uses data the model already holds.

## Customising the whole document

`model_config` accepts `json_schema_extra`, which can be a dict merged into the model's schema or a callable that receives and edits it:

```python
model_config = ConfigDict(
    json_schema_extra={"examples": [{"title": "Vectors", "minutes": 8}]})
```

Model-level examples appear in docs as full sample payloads. This Is more handy to a first-time caller than per-field examples: they can copy one and send it.

For deeper control there's `GenerateJsonSchema`, a class you can subclass to change how schemas are made across a whole use. Renaming meanings, altering how optionals are shown, adding vendor extensions all over. It's the right tool for a house style applied to an entire API and large overkill for one model.

## Docstrings become descriptions

A model's docstring turns the schema's `description`. That is worth knowing because it's free docs for the rules that can't be expressed structurally.

A cross-field rule &mdash; "ends_on must be after starts_on" &mdash; has no schema form. Writing it in the docstring means a consumer reading the docs learns about it, instead of discovering it through a 422.

`use_attribute_docstrings=True` extends this to fields, taking the string literal beneath an field as its description. It keeps the docs next to what it shows. This Is where it stays accurate.

## Reading the schema as a review

The most hands-on use of this module is as a review tool. One line. You see what your consumers see:

```python
print(json.dumps(Module.model_json_schema(), indent=2))
```

Things it well surfaces: fields whose name doesn't explain them and which have no description. A `pattern` where a `Literal` would have made a set of choices. A rule you thought was documented that turns out to live in a checker. A field in `needed` that you meant to default. A nested model inlined because it's used once. Here A named meaning would give clients a better type.

None of that needs running the API. It's the highest-value five minutes on hand on a model that other people will consume.

## Where schemas end up

Worth knowing the chain, because it shows why the small things matter.

Your model makes a schema. FastAPI collects those into an OpenAPI doc. That doc is read by the interactive docs, by client gens in a few languages, by API gateways, by contract-testing tools. Increasingly by LLM tooling deciding what shape to give.

A description you write once is read by everybody in that chain. So is a missing one.

## What to remember

The schema is made from what you already wrote. Its quality is a direct function of how exact your annotations are.

Constraints appear. Checkers don't. `Literal` and `Enum` become choices. Patterns become opaque. Nested models become named meanings and so named client types. Descriptions and examples cost nothing and are read by each tool downstream.

The habit worth forming is simply printing it. all above turns visible the moment you look at the doc your model already makes.

## Summary

`model_json_schema()` makes a standard doc from what you already wrote. Constraints become keywords. Checkers become nothing. Nested models become referenced meanings and so named types in made clients. `Literal` and `Enum` become renderable choices.

Two modes, for input and output. Metadata. Descriptions and examples above all. Is the cheapest docs you'll ever write. It's read by tools you may never see.

## The habit

Print the schema for the next model you write.

It takes one line and it's the only view of your model that matches what consumers get. all this module shows. A checker that documented nothing, a pattern that should have been a `Literal`, a field with no description, a needed field you meant to default. Turns visible at once.

The schema was made from work you had already done. Looking at it's the cheapest quality check on hand.


## Mistakes people make

**Expressing a rule as a checker when a constraint would do.** The rule is enforced and invisible. docs, made clients and browser-side forms all remain unaware of it. The caller only learns the limit by breaching it.

**Using a `pattern` where a `Literal` belongs.** A regular formula matching four values turns an opaque string in the schema. The enumeration turns a set of choices a form can render as a dropdown and a client can turn into a union type.

**Leaving fields undescribed.** `weight` needs a description. Of what, in what unit. Names that aren't self-explanatory and have no description give docs that strictly exists and helps no one.

**Never looking at it.** The schema is one line away and it's the only view of your model that matches what consumers really receive. all above turns obvious the moment you print it.

**Expecting cross-field rules to appear.** A `model_validator` has no schema form at all. Where a rule can't be expressed structurally, put it in the model's docstring so at least a human reading the docs learns about it.

**Losing the two modes.** making a check schema and wondering why a found field is missing, or a output schema and wondering why an excluded field is absent, are both the same misunderstanding. One shows what goes in, the other what comes out.

## Why this is the reason

check is handy and other libraries do it.

What made Pydantic a dependency of half the modern Python ecosystem is this. A machine-readable description of your data, made from the code that enforces it. So incapable of drifting from it.

docs that can't go stale. Clients made from the truth. Forms enforcing the same rules as the server. All from annotations you were going to write anyway.

## What good looks like

A well-given model makes a schema somebody could run a client against without asking you a question.

each field has a type narrow enough to be handy. `Literal` rather than `str` where the set is closed, `date` rather than `str` where it's a date. each constraint that exists in your head exists in the doc. each field whose name isn't self-explanatory has a description. There's at least one full example. Nested concepts are named models rather than inline objects. The made client has named types.

A poorly-given model makes a doc that is strictly valid and useless. All is a string, nothing has bounds, no field is given. The real rules live in checkers the consumer can't see.

Both are made on its own from code that validates the same way. The gap is fully in how exact the annotations were. Which is the arg this whole track has been making, arriving finally at the place where it turns visible to somebody other than you.
''',
    [
        {"q": "What does a `field_validator` contribute to the generated schema?",
         "options": ["The rule as a keyword", "Nothing - it is invisible to consumers", "A description", "An example"],
         "answer": 1,
         "why": "Arbitrary logic has no schema equivalent. The rule is still enforced, but documentation, generated clients and browser forms know nothing about it - which is why constraints are preferred where they can express the rule."},
        {"q": "Where do computed fields appear?",
         "options": ["The validation schema", "The serialization schema only", "Both", "Neither"],
         "answer": 1,
         "why": "They are output-only, so advertising them in an input schema would tell callers to send something that cannot be sent."},
        {"q": "Why does a nested model appear in `$defs` rather than inline?",
         "options": ["To save bytes only", "So it is referenced once and becomes a named type in generated clients", "It is a bug", "Because of recursion limits"],
         "answer": 1,
         "why": "A referenced definition becomes one named type used in several places, rather than several anonymous objects that happen to match. It is also what makes recursive models expressible."},
        {"q": "What do `examples` on a field do?",
         "options": ["Change validation", "Populate the interactive docs' request form with a working request", "Set the default", "Nothing"],
         "answer": 1,
         "why": "They change no behaviour and flow into the schema, where documentation tools use them to give a first-time caller something that works rather than an empty box."},
    ],
)


# ---------------------------------------------------------------------------
# 25. TypeAdapter
# ---------------------------------------------------------------------------
topic(
    "type_adapter",
    "TypeAdapter",
    "In and Out",
    "Validation, serialisation and schemas for things that are not models - the "
    "piece most people meet late and wish they had met early.",
    _svg(_box(14, 24, 52, 22, S) + _txt(40, 38, "List[int]", M, 8) +
         _arrow(70, 35, 88, 35) +
         _box(92, 24, 54, 22, S, A) + _txt(119, 38, "validated", A, 8) +
         _txt(80, 66, "no model required", M, 8)),
    [
        ("The wrapper model you do not need",
         "A bare list has no object around it. The usual workaround is a one-field "
         "model; <code>TypeAdapter</code> is what that was working around.",
         '''from typing import List
from pydantic import BaseModel, TypeAdapter

class Wrapper(BaseModel):        # a box built only to hold a list
    items: List[int]

print("workaround:", Wrapper(items=["1", "2", "3"]).items)

numbers = TypeAdapter(List[int])
print("direct    :", numbers.validate_python(["1", "2", "3"]))
print("from json :", numbers.validate_json("[1, 2, 3]"))'''),

        ("It works on anything you can annotate",
         "Scalars, containers, unions, models, and combinations of them all go through "
         "the same machinery.",
         '''from typing import Dict, List, Optional, Union
from pydantic import BaseModel, TypeAdapter

class Lesson(BaseModel):
    name: str
    minutes: int

cases = [
    (TypeAdapter(int), "42"),
    (TypeAdapter(Optional[int]), None),
    (TypeAdapter(List[str]), ("a", "b")),
    (TypeAdapter(Dict[str, float]), {"maths": "4.5"}),
    (TypeAdapter(Union[int, str]), "nine"),
    (TypeAdapter(List[Lesson]), [{"name": "Direction", "minutes": "4"}]),
]

for adapter, value in cases:
    print("%-24r -> %r" % (value, adapter.validate_python(value)))'''),

        ("The same errors you already know",
         "Paths, types and messages are identical to a model's, so one error handler "
         "covers both.",
         '''from typing import List
from pydantic import BaseModel, TypeAdapter, ValidationError

class Lesson(BaseModel):
    name: str
    minutes: int

lessons = TypeAdapter(List[Lesson])

try:
    lessons.validate_python([
        {"name": "Direction", "minutes": 4},
        {"name": "Magnitude", "minutes": "soon"},
        {"minutes": 5},
    ])
except ValidationError as e:
    print("problems:", e.error_count())
    for err in e.errors():
        print("  %-22s %-16s %s" % (".".join(str(p) for p in err["loc"]),
                                    err["type"], err["msg"]))'''),

        ("Serialising and schemas too",
         "It is not only validation. An adapter dumps and generates a schema for the "
         "same annotation.",
         '''import json
from typing import List
from pydantic import BaseModel, TypeAdapter

class Lesson(BaseModel):
    name: str
    minutes: int

lessons = TypeAdapter(List[Lesson])
data = lessons.validate_python([{"name": "Direction", "minutes": 4}])

print("dump      :", lessons.dump_python(data))
print("dump_json :", lessons.dump_json(data).decode())
print()
print("schema    :", json.dumps(lessons.json_schema(), indent=1)[:260], "...")'''),

        ("Build it once",
         "Constructing an adapter compiles a schema. Doing that inside a loop is a "
         "real and easily missed cost.",
         '''import time
from typing import List
from pydantic import TypeAdapter

rows = [[1, 2, 3] for _ in range(300)]

t = time.perf_counter()
for row in rows:
    TypeAdapter(List[int]).validate_python(row)     # rebuilt every time
inside = time.perf_counter() - t

adapter = TypeAdapter(List[int])                    # built once
t = time.perf_counter()
for row in rows:
    adapter.validate_python(row)
outside = time.perf_counter() - t

print("rebuilt each time : %.4f s" % inside)
print("built once        : %.4f s" % outside)
print("ratio             : %.1fx" % (inside / outside))
print()
print("Module level is where an adapter belongs.")'''),

        ("Validating a whole list in one call",
         "Letting the core do the looping beats a comprehension that crosses into "
         "Python for every item.",
         '''import time
from typing import List
from pydantic import BaseModel, TypeAdapter

class Lesson(BaseModel):
    name: str
    minutes: int

rows = [{"name": "L%d" % i, "minutes": i % 30 + 1} for i in range(2000)]
adapter = TypeAdapter(List[Lesson])

t = time.perf_counter()
one = [Lesson.model_validate(r) for r in rows]
per_item = time.perf_counter() - t

t = time.perf_counter()
many = adapter.validate_python(rows)
whole = time.perf_counter() - t

print("per item  : %.4f s" % per_item)
print("whole list: %.4f s" % whole)
print("ratio     : %.1fx" % (per_item / whole))
print("same result:", one == many)'''),
    ],
    [
        "<code>TypeAdapter(T)</code> applies the whole machinery to any annotation &mdash; no model needed.",
        "It has the same surface as a model: <code>validate_python</code>, <code>validate_json</code>, <code>dump_python</code>, <code>dump_json</code> and <code>json_schema</code>.",
        "Errors are identical in shape to a model's, so one error handler covers both.",
        "Build the adapter <strong>once</strong>, at module level. Constructing one compiles a schema, and doing it per call is a genuine cost.",
        "Validating a whole list in one call lets the Rust core do the looping, which beats a comprehension calling <code>model_validate</code> per item.",
        "It is the right tool for a bare JSON array, a config dict, a function argument, or anything else without a natural model around it.",
    ],
    '''
title: TypeAdapter: Validation Without a Model
intro: The same machinery applied to any annotation - and the fastest way to validate a large set.

## The thing people work around

Pydantic's validation works on models, but not all your data comes wrapped in one. Sometimes you have a plain list of integers. Sometimes a dictionary of names to scores. Sometimes a union of types. You still want the same checking and the same errors.

People often work around this. They build a throwaway model with one field, just to borrow validation. That is clumsy, and it is unnecessary. TypeAdapter takes any type and gives it the same validation and serialisation surface that a model has.

This article starts with the workaround people reach for and why it is a smell. It shows that a TypeAdapter offers the same methods as a model, and lists what you can pass it, from simple types to complex ones. It makes the point that you should build the adapter once and reuse it, because construction has a cost. You will see how to validate a whole collection in a single call, and how to get a schema from an adapter. It is the tool for data that does not need a class of its own.

Many projects reach this point sooner or later, usually with a list of records that has no model of its own. Maybe it is a config value, a webhook body or a column of data you want to check. The adapter handles all of these without any extra class. Because it follows the same rules as a model, you do not need to learn a second set of behaviours. The errors look the same. The modes work the same. Even the schema output matches. This article introduces the adapter through the workaround it replaces, then shows what it can do and how to use it without paying for it more than once. That last point matters in a busy service, because building an adapter on every call is a quiet and avoidable cost in code that runs often.

A model validates a model. But plenty of data isn't shaped like one.

An endpoint returns a bare JSON array. A config value is a `Dict[str, float]`. A function takes a `List[UUID]` and you'd like to check it. A queue message is a single int.

The common workaround is a wrapper model:

```python
class LessonList(BaseModel):
    items: List[Lesson]
```

A box built only so that a thing can be inside it. Each caller has to reach through `.items` to get at the actual data.

`TypeAdapter` is what that was working around:

```python
lessons = TypeAdapter(List[Lesson])
lessons.validate_python(rows)
```

## The same surface as a model

An adapter has the methods you already know, applied to the annotation instead of to a class:

`validate_python` and `validate_json` for input. `dump_python` and `dump_json` for output. `json_schema` for the schema.

So all from the previous modules applies. Coercion works the same way. Constraints inside `Annotated` are honoured. Errors have the same `loc`, `type`, `msg` and `input`. The error handler you already wrote covers adapters without change.

That last point is worth emphasising: this isn't a parallel API with its own rules. It's the same machinery, handled differently.

## What you can pass it

Anything you can write as an annotation.

Scalars: `TypeAdapter(int)`. holders: `List`, `Dict`, `Set`, `Tuple`. Optionals and unions, including discriminated ones. Models. Constrained types from `Annotated`. Any nesting of those.

`TypeAdapter(Annotated[int, Field(gt=0)])` validates a bare plus int. This Is at times just what a function arg needs.

## Build it once

This is the mistake worth naming loudly, because it's invisible and common.

Making a `TypeAdapter` **compiles a schema**. That is real work. The same work that happens once when a model class is defined.

```python
for row in rows:
    TypeAdapter(List[int]).validate_python(row)     # recompiles every iteration
```

The adapter belongs at module level, built once and reused:

```python
NUMBERS = TypeAdapter(List[int])

for row in rows:
    NUMBERS.validate_python(row)
```

The gap is large and it doesn't look like a speed bug in review. This Is just why it lives.

## Validating a collection in one call

The second speed point is the more valuable one, and it applies to models too.

Two ways to validate a thousand rows:

```python
[Lesson.model_validate(r) for r in rows]              # per item
TypeAdapter(List[Lesson]).validate_python(rows)       # whole list
```

Both give the same result. The first crosses from Python into Rust and back a thousand times. The second makes one call. The loop happens inside the compiled core.

For bulk work &mdash; importing a file, handling a batch, checking a large response &mdash; that is the single most good tuning on hand in this library, and it's one line.

This is also the answer to the concern raised back in the first tier about check cost on large sets. The cost is real. The way to reduce it's to let the core do the looping rather than to skip checking.

## Where it earns its place

**Bare arrays.** An endpoint that accepts or returns a JSON list.

**config.** A `Dict[str, str]` from setting or a file, checked without inventing a settings model for three values.

**Function args.** Checking an arg at a public function's edge without wrapping it.

**Bulk check.** The speed case above.

**Dynamic types.** Because it takes a type at runtime, you can build one from a type found at runtime. handy in plain code and in libraries.

## Schemas without models

`json_schema()` makes a schema doc for the annotation. This Is how a framework docs an endpoint whose body is a bare array.

That is the piece that makes the wrapper model truly not needed. before you needed the model to get a schema. Now the annotation is enough. Your API docs shows an array as an array rather than as an object with an `items` field no one sends.

## When a model is still better

`TypeAdapter` isn't a swap for models. Reaching for it all over would be a mistake.

A model gives you a **name**. `Lesson` means a thing. `Dict[str, Any]` doesn't. Named types are how a code stays comprehensible.

A model gives you a place for **checkers, config and methods**. An adapter has no class body.

A model gives you **field access**. `lesson.minutes` beats `data["minutes"]`. Your editor can help with the first.

So: models for the domain concepts, adapters for the shapes around them. A `List[Lesson]` is an adapter wrapping a model. That is the usual setup. The model names the thing, the adapter handles the set.

## A small caution

An adapter validates and hands back plain Python objects. `TypeAdapter(Dict[str, float])` gives you a dict, not a thing with promises attached.

Nothing stops later code putting a string in that dict. check happened at a moment. It isn't a permanent property of the object. This Is the same as all over else in Pydantic and worth remembering when the checked thing is a mutable builtin rather than a model with `frozen=True` on hand.

## Adapters and constrained types

Because an adapter takes any annotation, it takes constrained ones:

```python
Port = Annotated[int, Field(ge=1, le=65535)]
PORTS = TypeAdapter(List[Port])

PORTS.validate_python(["80", "443"])     # [80, 443]
PORTS.validate_python([0])               # ValidationError
```

That is a compact way to validate a list of values against a domain rule with no model anywhere. config lists, command-line args and query params are all natural fits.

## Validating function arguments

An adapter at a public function's edge gives you the same promises a model would, without wrapping the args in an object:

```python
IDS = TypeAdapter(List[UUID])

def fetch(ids):
    ids = IDS.validate_python(ids)
    ...
```

Pydantic also ships `@validate_call`. This Reads a function's own annotations and validates args on its own. That is often the nicer spelling when a whole function should be checked. An adapter is better when only one arg needs it, or when the check is gated.

## The schema for a bare shape

`json_schema()` is what makes the wrapper model truly not needed rather than merely inconvenient.

Before adapters, an endpoint accepting a bare JSON array needed a model to give a schema. The resulting docs given an object with an `items` field that no client ever sent. With an adapter the schema shows an array. An array is what it's.

FastAPI uses this inside. This Is why annotating a request body as `List[Item]` makes correct docs with no wrapper in sight.

## Adapters are cheap to hold, not to build

The gap that matters for speed: an adapter is costly to *make* and cheap to *use*.

Making compiles a schema. Using it runs compiled code. So the pattern is always the same. Build at module level, use anywhere:

```python
LESSONS = TypeAdapter(List[Lesson])
```

Uppercase by rule, because it's a module-level constant. Putting it at the top makes it obvious it's built once.

If a type is only known at runtime, cache the adapters in a dict keyed by type rather than rebuilding. `functools.lru_cache` on a small factory function is the usual shape.

## A short list of uses

A bare JSON array in or out. A config dict. A function arg at a public edge. Bulk check of a large set in one call. A shape whose type is found at runtime. A schema for a thing that isn't a model.

Each of those has a wrapper-model workaround, and each is cleaner without one.

## Summary

`TypeAdapter` applies the whole machinery. Check, coercion, constraints, output, schemas, errors &mdash; to any annotation, with the same action and the same error shapes as a model.

Build it once at module level. Prefer one call over a Python loop for sets. Use models where a thing deserves a name and a class body. Use adapters for the shapes around them.

It's the piece most people find late. The one that drops the most awkward code when they do.

## Why it is worth learning early

Most people discover `TypeAdapter` after writing a few wrapper models. Then go back and delete them.

The habit it replaces is small but pervasive. Reaching for a class because check seemed to need one. Once you know an annotation is enough, a whole group of awkward code stops being written. The box around the list, the `.items` each caller has to unwrap, the schema that shows an object where the data is an array.

Models for things that deserve names. Adapters for the shapes around them. That division is most of the judgement this module is trying to pass on.


## Mistakes people make

**Making inside a loop.** The single most costly mistake here. The one that looks fine in review. Building an adapter compiles a schema. Doing it per loop repeats that work each time. Module level, uppercase, once.

**Looping in Python over a set.** `[Model.model_validate(r) for r in rows]` crosses between Python and Rust once per row. `TypeAdapter(List[Model]).validate_python(rows)` makes one call and loops inside the compiled core. For bulk work it's the highest-value one-line change on hand.

**Using an adapter where a model belongs.** A `Dict[str, Any]` passed around a code is a shape with no name, no methods, no field access and no place to put a rule. If the thing is a domain concept, it deserves a class.

**given check persists.** An adapter hands back plain Python objects. A checked `Dict[str, float]` is an plain dict. Nothing stops later code putting a string in it. check happened at a moment. It isn't a property the object carries later.

**Losing it can serialise and make schemas.** People discover `validate_python` and stop. `dump_json` and `json_schema` are the other half. The schema in given is what makes the wrapper model truly not needed rather than merely inconvenient.

**Rebuilding adapters for runtime types without caching.** When the type is found, cache the adapters in a dict keyed by type, or wrap a small factory in `functools.lru_cache`.

## The short version

Any annotation, the whole machinery, no class needed.

Build it once at module level. Build compiles a schema. Validate sets in one call rather than looping in Python. And use it wherever the data has no natural model around it. Which is more often than the wrapper-model habit suggests.

## A note on naming and discovery

One reason `TypeAdapter` is found late is that it doesn't look like the thing people are searching for. Someone with a bare JSON array searches for how to validate a list, finds examples using models. Builds the wrapper. Nothing in that path mentions adapters.

So it's worth stating the shape plainly: **if you can write it as a type annotation, you can validate it, serialise it. Make a schema for it, without a class.**

That covers a great deal. A list of models. A dict of settings. A single constrained int. An optional union. Anything nested from those.

The corollary is equally handy: if you're writing a class purely so that a thing can be checked, stop and check whether an annotation would do. The wrapper model is a real and widespread pattern. Almost each instance of it predates its author discovering this.

Where a class still earns its place is where a class was always the right answer. A domain concept that deserves a name, one spot to hang methods, field access instead of subscripting, a place for checkers and config. Those are properties of a model, not of check. Adapters were never competing for them.

## Where it sits in the library

It's easy to read this module as being about an tuning or a convenience. It's really about a boundary in how Pydantic is organised.

`BaseModel` is a way of *declaring* a shape and getting action attached to it. `TypeAdapter` is a way of *using* the same machinery against a shape declared some other way.

all the library does &mdash; coercion rules, constraints, error paths, JSON parsing, output, schema making &mdash; lives underneath both. A model isn't a more capable checker. It's a class with that checker bound to it, plus a namespace for methods and config.

Seeing it that way makes the choice obvious rather than a matter of taste. Ask whether you need the class. If the answer is yes. Because the thing has a name, needs methods, wants field access. Write a model. If the answer is no, an annotation and an adapter give you same check with nothing extra to maintain.
''',
    [
        {"q": "Why is `TypeAdapter(List[Lesson])` better than a wrapper model with one list field?",
         "options": ["It is the only way", "Same validation with no artificial object, and the schema describes an array rather than an object", "It is stricter", "No real difference"],
         "answer": 1,
         "why": "The wrapper exists only to hold the list, forces callers through `.items`, and makes the API document an object where the data is an array."},
        {"q": "Where should a TypeAdapter be constructed?",
         "options": ["Inside the loop", "Once at module level", "Per request", "It makes no difference"],
         "answer": 1,
         "why": "Constructing one compiles a schema. Rebuilding it per call is real repeated work and does not look like a performance bug in review."},
        {"q": "Which validates a thousand rows faster?",
         "options": ["A comprehension of model_validate", "TypeAdapter(List[Model]).validate_python(rows)", "They are identical", "Neither validates"],
         "answer": 1,
         "why": "One call lets the Rust core do the looping; the comprehension crosses between Python and Rust once per item. It is the most effective single-line optimisation here."},
        {"q": "When is a model still the better choice than an adapter?",
         "options": ["Never", "When the thing deserves a name, needs validators or config, or benefits from attribute access", "Only for JSON", "Only for nested data"],
         "answer": 1,
         "why": "Adapters have no class body and hand back plain objects. Models name domain concepts and give validators, config and methods somewhere to live."},
    ],
)


# ---------------------------------------------------------------------------
# 26. Generic models
# ---------------------------------------------------------------------------
topic(
    "generic_models",
    "Generic Models",
    "In Practice",
    "One envelope, many payloads - the pattern behind every paginated response "
    "you have ever consumed.",
    _svg(_box(16, 20, 128, 54, S) + _txt(80, 34, "Page[T]", A, 9) +
         _box(30, 42, 44, 22, S) + _txt(52, 56, "Module", M, 8) +
         _box(86, 42, 44, 22, S) + _txt(108, 56, "Lesson", M, 8)),
    [
        ("The duplication a generic removes",
         "Two envelopes with identical structure and one differing field. A third "
         "resource means a third copy.",
         '''from typing import List
from pydantic import BaseModel

class Module(BaseModel):
    title: str

class Lesson(BaseModel):
    name: str

class ModulePage(BaseModel):
    items: List[Module]
    total: int
    page: int

class LessonPage(BaseModel):          # the same class again
    items: List[Lesson]
    total: int
    page: int

print(ModulePage(items=[{"title": "Vectors"}], total=1, page=1))
print(LessonPage(items=[{"name": "Direction"}], total=1, page=1))'''),

        ("One envelope, parameterised",
         "Inherit from <code>Generic[T]</code> and the payload type becomes an "
         "argument. Validation applies to whatever you fill it with.",
         '''from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int = 1

class Module(BaseModel):
    title: str
    minutes: int

class Lesson(BaseModel):
    name: str

mp = Page[Module](items=[{"title": "Vectors", "minutes": "8"}], total=1)
lp = Page[Lesson](items=[{"name": "Direction"}], total=1)

print("modules:", mp)
print("lessons:", lp)
print()
print("inner type:", type(mp.items[0]).__name__, "| coerced:", mp.items[0].minutes)'''),

        ("The parameter is validated",
         "A generic is not a free pass. The payload is checked against whatever type "
         "you supplied, with the usual errors and paths.",
         '''from typing import Generic, List, TypeVar
from pydantic import BaseModel, ValidationError

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int

class Module(BaseModel):
    title: str
    minutes: int

try:
    Page[Module](items=[{"title": "Vectors", "minutes": "soon"}], total=1)
except ValidationError as e:
    err = e.errors()[0]
    print("path:", err["loc"])
    print("said:", err["msg"])

# And a plain type works just as well as a model:
print()
print("ints:", Page[int](items=["1", "2", "3"], total=3))'''),

        ("Bounded and constrained parameters",
         "<code>TypeVar(bound=...)</code> restricts what the parameter may be, which "
         "keeps a generic honest about what it can hold.",
         '''from typing import Generic, List, TypeVar
from pydantic import BaseModel

class Resource(BaseModel):
    id: int

TResource = TypeVar("TResource", bound=Resource)

class Page(BaseModel, Generic[TResource]):
    items: List[TResource]

    def ids(self):
        return [item.id for item in self.items]     # safe: bound guarantees .id

class Module(Resource):
    title: str

p = Page[Module](items=[{"id": 1, "title": "Vectors"},
                        {"id": 2, "title": "Norms"}])
print(p)
print("ids:", p.ids())'''),

        ("Several parameters",
         "A generic can take more than one, which is how a result-or-error envelope "
         "gets written once.",
         '''from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

D = TypeVar("D")
E = TypeVar("E")

class Result(BaseModel, Generic[D, E]):
    ok: bool
    data: Optional[D] = None
    error: Optional[E] = None

class Module(BaseModel):
    title: str

class Problem(BaseModel):
    code: str
    detail: str

good = Result[Module, Problem](ok=True, data={"title": "Vectors"})
bad = Result[Module, Problem](ok=False,
                              error={"code": "not_found", "detail": "no such module"})

print("ok  :", good)
print("bad :", bad)'''),

        ("What the schema does with it",
         "Each parameterisation becomes its own definition, so a generated client "
         "gets a real named type rather than an untyped envelope.",
         '''import json
from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int

class Module(BaseModel):
    title: str

schema = Page[Module].model_json_schema()
print("title :", schema["title"])
print("props :", list(schema["properties"]))
print("$defs :", list(schema.get("$defs", {})))
print()
print("items :", json.dumps(schema["properties"]["items"]))'''),
    ],
    [
        "Inherit from both <code>BaseModel</code> and <code>Generic[T]</code>, then parameterise with <code>Page[Module]</code>.",
        "The parameter is fully validated &mdash; a generic gives you reuse, not an escape from checking.",
        "Each parameterisation is a distinct class, built and cached the first time you use it.",
        "<code>TypeVar(bound=X)</code> restricts the parameter, which lets methods on the generic safely use what <code>X</code> guarantees.",
        "The generated schema names each parameterisation (<code>Page[Module]</code>), so clients get real named types rather than an envelope of anything.",
        "Parameterise at module level rather than inside a hot function &mdash; building the class the first time costs something.",
    ],
    '''
title: Generic Models: One Envelope, Many Payloads
intro: The pattern behind each paginated response, written once instead of once per resource.

## The duplication

Imagine an API that wraps every response in an envelope. The envelope has a status, a message and a payload. The payload changes from endpoint to endpoint. You could write a separate envelope model for each one, but they would all repeat the same fields.

A generic model solves that. You define the envelope once, with a type parameter standing in for the payload. When you use it, you fill in the parameter, and you get a model specialised for that payload. The shared structure is written once, and the varying part is chosen at the point of use.

This article starts with the duplication and then shows the generic version. It makes clear that the result is still fully validated, so the payload is checked against the type you chose. Each filled-in version is a real class of its own, which you can inspect and reuse. The last section covers bounded parameters, which limit what types are allowed. Generic models fit best for the wrappers and containers that appear all over an API, such as pages of results.

If you have ever copied a model and changed one field, this article is for you. Wrappers for pages, results, responses and events all share this pattern. The typing is not complicated, and you need no advanced knowledge of Python generics to follow it. You will see how a single definition produces many classes. You will also see how Pydantic checks the filled-in type, so a mistake in the payload is caught exactly as it would be in a hand-written model. The article ends with bounds, which let you say that a parameter must be a model, or a number, instead of anything at all. That keeps the shared structure honest and gives your editor better hints. Small as the idea is, it removes a surprising amount of repeated code from a typical API project.

each API with more than one list endpoint grows the same class a few times:

```python
class ModulePage(BaseModel):
    items: List[Module]
    total: int
    page: int

class LessonPage(BaseModel):
    items: List[Lesson]
    total: int
    page: int
```

same apart from one type. A third resource means a third copy. A change to pagination means editing all of them. Or, more realistically, editing most of them.

## The generic version

```python
T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int = 1
```

Inherit from `BaseModel` and `plain[T]`, use `T` where the varying type goes. Parameterise at the point of use:

```python
Page[Module](items=[...], total=1)
```

One meaning. Adding a field to the envelope reaches each resource at once. There's no possibility of the copies disagreeing because there are no copies.

## It is still validated

A common assumption is that a plain loosens things. It doesn't.

`Page[Module]` validates `items` as a list of `Module`, with each rule `Module` carries. Coercion works, constraints run, errors have the usual paths. `("items", 0, "minutes")` names the first item's field just as it would in a non-plain model.

`Page[int]` validates a list of ints, with the same coercion rules as anywhere else. The param can be any type Pydantic understands, not only models.

## Each parameterisation is a real class

`Page[Module]` is a distinct class, created the first time you write it and cached later.

That has two results worth knowing.

It has a name, `Page[Module]`. This Appears in the schema and in error messages. A consumer sees a exact type rather than a vague envelope.

And building it costs a thing. The cost is small and paid once per parameterisation. It means `Page[Module]` inside a hot function is doing a lookup that a module-level alias would avoid:

```python
ModulePage = Page[Module]
```

That alias is also better style: it names the type once and each use site is shorter.

## Bounded parameters

An unbounded `TypeVar` can be anything. A plain can't assume anything about it. A bound fixes that:

```python
TResource = TypeVar("TResource", bound=Resource)

class Page(BaseModel, Generic[TResource]):
    items: List[TResource]

    def ids(self):
        return [item.id for item in self.items]
```

Because the param must be a `Resource`, each item is sure to have `id`. The method is safe. Without the bound, mypy would object and the method would be a runtime gamble.

Bounds are also docs. `plain[TResource]` with a bound says what kind of thing this envelope is for. A bare `T` says nothing.

## Several parameters

More than one is allowed, and the result-or-error envelope is the common case:

```python
class Result(BaseModel, Generic[D, E]):
    ok: bool
    data: Optional[D] = None
    error: Optional[E] = None
```

Written once, used as `Result[Module, Problem]` all over. This is a pattern many codebases reinvent per endpoint.

Keep the count low. Two params is comfortable, three is a stretch. Beyond that the type is often trying to be a few types at once.

## Schemas and clients

Each parameterisation makes its own schema, titled with the parameterised name.

That is the hands-on payoff for consumers. A made TypeScript client gets `PageModule` and `PageLesson` as distinct types, each with right typed `items`. Without type vars you'd have written those classes by hand and got the same result at more cost. With a hand-rolled `items: List[Any]` envelope you'd get a client that types `items` as `any` and helps no one.

FastAPI handles plain response models right. `response_model=Page[Module]` &mdash; and docs it right.

## Inheritance and generics together

A plain model can be subclassed, and a subclass can fix the param:

```python
class ModulePage(Page[Module]):
    facets: Dict[str, int] = {}
```

That gives you the shared envelope plus a thing exact to one resource. It's a good pattern when one endpoint truly needs an extra field. A bad one if each subclass adds a thing. At that point the envelope isn't really shared.

## When not to reach for one

**Two use sites.** Two near-same classes are easier to read than a plain. The pattern earns its keep at three or four. The cost of waiting is small.

**The classes differ in more than one type.** A plain with a param and three overridden fields isn't a shared shape.

**A union would say it better.** If the payload is one of a fixed small set rather than any, a discriminated union shows that just and a plain doesn't.

**The envelope has no structure.** `plain[T]` wrapping a single field of type `T` is a box. `TypeAdapter` validates the payload right without one.

## Generics and validation cost

Parameterising isn't free, and it's worth knowing where the cost falls.

`Page[Module]` builds a class the first time it's written. Resolving the type var, making a schema, caching the result. each later use of the same parameterisation reuses it.

So the cost is per distinct parameterisation, paid once. It's the same cost a hand-written `ModulePage` would have paid at import. check itself is same. The schema the plain makes is the schema the hand-written class would have made.

The mistake, as with `TypeAdapter`, is doing the parameterisation one spot repetitive. `Page[Module]` inside a function called per request performs a cached lookup each time. A module-level alias performs it once. The gap is small and free to avoid.

## Generics with FastAPI

`response_model=Page[Module]` works right, and the docs names the type right. `PageModule` in the made schema, with `items` typed as an array of `Module`.

That is worth doing rather than falling back to an untyped envelope. A response model of `Page[Module]` gives each consumer a real type. A model with `items: List[Any]` gives them nothing. They'll write the type by hand on their side and get it wrong when yours changes.

The same applies to a `Result[Data, Error]` envelope. If your API wraps each response, making that wrapper plain is the gap between a client library that knows what each endpoint returns and one that unwraps `any`.

## Summary

`class Page(BaseModel, plain[T])`, used as `Page[Module]`. The param is fully checked with its own rules. Each parameterisation is a real, named class that appears right in the schema and in made clients.

Bound the type var when the plain needs to lean on what the param gives. Alias parameterisations at module level. Keep the param count to one or two.

And reach for it at the third copy of an envelope, not the second. Two similar classes are easier to read than a plain. The pattern earns its keep as soon as there are more.


## Mistakes people make

**Reaching for one at the second copy.** Two similar classes read better than a plain. The pattern earns its keep around the third or fourth, and waiting costs almost nothing.

**Parameterising in a hot path.** `Page[Module]` performs a cached class lookup each time it's checked. A module-level alias does it once and reads better at each use site.

**Leaving the type var unbounded when methods need it.** A method calling `item.id` on a bare `T` is a runtime gamble that mypy will object to. `TypeVar(bound=Resource)` makes the promise real and docs what the envelope is for.

**Too many params.** Two is comfortable. Three is a stretch. Beyond that the type is trying to be a few types. Split classes will be clearer.

**Wrapping a single field.** `plain[T]` around a model with one field of type `T` is a box. `TypeAdapter` validates the payload right and makes a schema that shows what the data really is.

**given a plain is looser.** It isn't. `Page[Module]` validates its items with each rule `Module` carries. The error paths are same to a hand-written envelope's.

**Losing `response_model=Page[Module]`.** Falling back to an untyped envelope in FastAPI means each consumer gets `any` and writes the type by hand on their side. Where it will be wrong the first time yours changes.

## Reading a generic model

One hands-on note for anyone keeping these.

A plain reads worse than the classes it replaces. That is the trade. `class ModulePage(BaseModel)` with three concrete fields can be understood at a glance. `class Page(BaseModel, plain[T])` needs the reader to hold a type var in their head and then find the parameterisations to know what it's ever filled with.

Two things make that cost small. Name the type var usefully. `TResource` says more than `T` once there's more than one. And alias the parameterisations at module level. A reader searching for "what does the modules endpoint return" finds `ModulePage = Page[Module]` rather than an formula buried in a decorator.

Neither costs anything, and both turn a plain from a thing clever into a thing plain.

## A worked shape

Most APIs end up with two plain envelopes and nothing else.

```python
T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int = 1
    size: int = 20

class Result(BaseModel, Generic[T]):
    ok: bool
    data: Optional[T] = None
    error: Optional[Problem] = None

ModulePage = Page[Module]
LessonPage = Page[Lesson]
```

Two meanings and a handful of aliases replace one envelope class per resource. This In a system of fifteen resources is fifteen classes all saying the same thing.

The aliases matter as much as the type vars. They give each parameterisation a name a reader can search for, keep the parameterisation out of hot paths. Make endpoint signatures short: `response_model=ModulePage` rather than a bracketed formula in a decorator.

Adding a field to pagination. A cursor, a `has_more` flag &mdash; is then one edit that reaches each list endpoint at once, right, including in the docs and in each made client. That is the property worth having. The reason the pattern lives contact with a real code.

## Generics and static checking

One gain that doesn't show up at runtime at all.

Mypy and Pyright understand `plain[T]`. So `Page[Module]` is a type they can reason about. `page.items[0].title` is checked. `page.items[0].name` is flagged before the code runs.

A hand-written `ModulePage` gives the same static gain. This isn't an arg for type vars over concrete classes. It's an arg against the shortcut people reach for when they tire of writing envelopes:

```python
class Page(BaseModel):
    items: List[Any]
```

That validates nothing about the payload, tells mypy nothing. Makes a schema in which `items` is an array of anything. each consumer. Your own code, a static checker, a made client &mdash; is worse off.

The choice isn't really "plain or concrete". It's "typed or untyped". The plain is what makes the typed option cheap enough that no one reaches for the untyped one.

## Why envelopes end up generic

It's worth noticing why this pattern appears in nearly each API of any size. It isn't really about type vars.

An API with fifteen list endpoints has fifteen responses that differ in just one place. That is a shape. Shapes want names. Writing fifteen classes to express one shape is the kind of duplication that looks harmless in a small code and turns a maintenance surface in a large one. Not because typing it's hard. Because changing it later means finding all fifteen.

The plain is simply the language feature that lets the shape have a name. `Page` is the concept. `Page[Module]` is that concept applied. Once written, adding a field to pagination is a single edit that can't miss a case. Each consumer sees the change always.

That is the same arg as extracting a nested model, or naming a constrained type, or putting config on a shared base. Each is a other method for the same principle. State a choice once, in a place that has a name. Let all that needs it refer to that rather than to a copy.
''',
    [
        {"q": "Does `Page[Module]` validate its `items`?",
         "options": ["No - generics skip validation", "Yes, fully, with Module's own rules and normal error paths", "Only the length", "Only in strict mode"],
         "answer": 1,
         "why": "A generic gives reuse, not an escape from checking. Coercion, constraints and error paths all behave exactly as in a non-generic model."},
        {"q": "Why alias `ModulePage = Page[Module]` at module level?",
         "options": ["Required syntax", "Each parameterisation builds a real class; the alias names it once and avoids repeating the lookup", "It changes validation", "For mypy only"],
         "answer": 1,
         "why": "`Page[Module]` creates and caches a distinct class. Naming it once is both clearer at every use site and avoids doing the lookup in a hot path."},
        {"q": "What does `TypeVar(\"T\", bound=Resource)` let you do?",
         "options": ["Nothing extra", "Write methods on the generic that rely on what Resource guarantees", "Skip validation", "Allow any type"],
         "answer": 1,
         "why": "The bound means every parameterisation is a Resource, so a method can safely use `item.id`. It also documents what the envelope is for."},
        {"q": "When is a generic the wrong tool?",
         "options": ["Always", "At two use sites, or when the payload is one of a fixed small set", "For paginated responses", "With models"],
         "answer": 1,
         "why": "Two near-identical classes read better than a generic; the pattern earns its keep around the third. And a fixed small set of payloads is a discriminated union, which says more."},
    ],
)


# ---------------------------------------------------------------------------
# 27. Settings management
# ---------------------------------------------------------------------------
topic(
    "settings_management",
    "Settings Management",
    "In Practice",
    "Typed configuration from the environment, validated at start-up instead of "
    "failing at midnight.",
    _svg(_txt(34, 30, "DB_PORT=5432", M, 7) + _arrow(72, 26, 90, 26) + _txt(120, 30, "int", A, 8) +
         _txt(34, 52, 'DEBUG="yes"', M, 7) + _arrow(72, 48, 90, 48) + _txt(120, 52, "bool", A, 8) +
         _box(14, 62, 132, 18, S, A) + _txt(80, 75, "checked at start-up", A, 8)),
    [
        ("Configuration is a boundary too",
         "<code>os.environ</code> gives strings and no guarantees. A settings model "
         "reads, converts and checks in one place.",
         '''import os
from pydantic_settings import BaseSettings

# The environment as your process actually sees it: strings, or nothing.
os.environ["APP_PORT"] = "8642"
os.environ["APP_DEBUG"] = "yes"

print("raw    :", repr(os.environ.get("APP_PORT")),
      repr(os.environ.get("APP_DEBUG")))

class Settings(BaseSettings):
    app_port: int = 8000
    app_debug: bool = False
    app_name: str = "VizLearn"

s = Settings()
print("typed  :", s)
print("port+1 :", s.app_port + 1, "(a real int)")
print("not    :", not s.app_debug)'''),

        ("Missing configuration fails at start-up",
         "A required setting with no value raises immediately, naming the variable "
         "&mdash; rather than surfacing as an error hours later.",
         '''import os
from pydantic_settings import BaseSettings
from pydantic import ValidationError

for key in ("DATABASE_URL", "SECRET_KEY"):
    os.environ.pop(key, None)

class Settings(BaseSettings):
    database_url: str          # required
    secret_key: str            # required
    timeout: int = 30

try:
    Settings()
except ValidationError as e:
    print("missing at start-up:", e.error_count())
    for err in e.errors():
        print("   ", err["loc"][0], "->", err["type"])

os.environ["DATABASE_URL"] = "postgres://localhost/viz"
os.environ["SECRET_KEY"] = "s3cret"
print()
print("with values:", Settings())'''),

        ("Prefixes and explicit names",
         "<code>env_prefix</code> namespaces a whole model; "
         "<code>validation_alias</code> pins one field to a specific variable.",
         '''import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

os.environ["VIZ_HOST"] = "0.0.0.0"
os.environ["VIZ_PORT"] = "8642"
os.environ["DATABASE_URL"] = "postgres://localhost/viz"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VIZ_")

    host: str = "127.0.0.1"
    port: int = 8000
    # This one does not follow the prefix - name it explicitly.
    db: str = Field(validation_alias="DATABASE_URL")

print(Settings())'''),

        ("Constraints and validators still apply",
         "A settings model is a model. Everything from the earlier tiers works, which "
         "is what makes configuration checkable rather than merely typed.",
         '''import os
from typing import Literal
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings

os.environ.update({"PORT": "70000", "ENV": "staging", "WORKERS": "0"})

class Settings(BaseSettings):
    port: int = Field(ge=1, le=65535)
    env: Literal["dev", "test", "prod"]
    workers: int = Field(gt=0)

try:
    Settings()
except ValidationError as e:
    for err in e.errors():
        print("%-8s %-22s %s" % (err["loc"][0], err["type"], err["msg"]))

os.environ.update({"PORT": "8642", "ENV": "prod", "WORKERS": "4"})
print()
print("valid:", Settings())'''),

        ("Nested settings from one variable",
         "A nested model can be filled from JSON in a single variable, or from "
         "delimited names.",
         '''import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Redis(BaseModel):
    host: str = "localhost"
    port: int = 6379

os.environ["REDIS"] = '{"host": "cache.internal", "port": "6380"}'

class Settings(BaseSettings):
    redis: Redis = Redis()

print("from json  :", Settings().redis)

# Or with a delimiter, one variable per leaf:
os.environ.pop("REDIS")
os.environ["REDIS__HOST"] = "other.internal"
os.environ["REDIS__PORT"] = "6381"

class Nested(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")
    redis: Redis = Redis()

print("from parts :", Nested().redis)'''),

        ("Secrets, and not printing them",
         "<code>SecretStr</code> keeps a value out of logs and tracebacks, which "
         "matters most in the object every process prints at start-up.",
         '''import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings

os.environ.update({"SECRET_KEY": "sk_live_abcdef123456",
                   "DATABASE_URL": "postgres://user:hunter2@db/viz"})

class Unsafe(BaseSettings):
    secret_key: str
    database_url: str

class Safe(BaseSettings):
    secret_key: SecretStr
    database_url: SecretStr

print("unsafe:", Unsafe())
print()
print("safe  :", Safe())
print("dump  :", Safe().model_dump())
print()
print("reading it deliberately:", Safe().secret_key.get_secret_value()[:6] + "...")'''),
    ],
    [
        "<code>BaseSettings</code> is a <code>BaseModel</code> that reads its values from the environment. Everything you know about models applies.",
        "Field names map to environment variables case-insensitively; <code>env_prefix</code> namespaces the whole model and <code>validation_alias</code> pins one field.",
        "A missing required setting fails at start-up, naming the variable &mdash; not at 3am when the code path is first taken.",
        "Constraints and validators work, so configuration can be <em>checked</em>, not merely typed: a port in range, an environment from a fixed set.",
        "Nested models come from JSON in one variable, or from <code>env_nested_delimiter</code> names such as <code>REDIS__HOST</code>.",
        "Use <code>SecretStr</code> for credentials. A settings object is the thing most likely to be printed at start-up, and that is how secrets reach logs.",
    ],
    '''
title: Settings Management: Configuration That Fails Early
intro: Typed, checked config from the setting - and why start-up is the right place to fail.

## Configuration is untrusted input

Your application needs configuration. A database address, an API key, a debug flag, a port number. These usually come from environment variables or files, and that makes them untrusted input, just like a request from a user. They can be missing, misspelled or the wrong type.

Pydantic has a companion package for this, called pydantic-settings. You describe your settings as a model, and it reads the values from the environment and validates them. The same type checks and constraints apply. A bad configuration is caught as soon as the program starts, not hours later when some code path finally needs the value.

This article explains why configuration deserves validation and why failing at start-up is the right behaviour. It covers how names map between environment variables and fields. You will see how to check values, not only type them, so that a port number really is a sensible port. It then covers nested settings for grouped options, loading from files, and secrets, which should be handled so they do not leak into logs. The result is configuration you can trust before the first request arrives.

all in this track has argued that data crossing into your program should be checked at the boundary. config is such data. It's often treated as though it isn't.

The common code is `int(os.environ.get("PORT", "8000"))` scattered through a code, with no central statement of what config exists, no defaults in one place. No check that anything needed is really set. A missing var turns a `None` that travels until a thing fails on it.

`pydantic-settings` applies the model discipline to it. `BaseSettings` is a `BaseModel` that reads its values from the setting.

```python
class Settings(BaseSettings):
    app_port: int = 8000
    app_debug: bool = False
    database_url: str
```

Field names map to setting vars case-insensitively. `app_port` reads `APP_PORT`. Values arrive as strings and are coerced by the plain rules. Which is just the case lax coercion was designed for.

Note `app_debug: bool`. The boolean vocab from the coercion module means `APP_DEBUG=yes`, `=1`, `=true` and `=on` all work. `=maybe` raises. That is a much better outcome than `bool(os.environ.get("APP_DEBUG"))`. Here The string `"false"` is `True`.

## Failing at start-up

The single biggest gain is *when* the failure happens.

`database_url: str` has no default. So It's needed. If the var isn't set, making `Settings()` raises at once, naming the field. A deployment missing a var fails at boot, visibly, before serving anything.

The option is a `None` that sits quietly until the first request touching the DB. This May be minutes or hours later. Makes an error about `NoneType` far from the cause.

That is why settings should be instantiated once at start-up, not lazily on first use. The whole value is in failing before the process claims to be ready.

## Naming

Three methods, in growing specificity.

**silent.** `app_port` reads `APP_PORT`. Case-insensitive.

**Prefix.** `env_prefix="VIZ_"` in `SettingsConfigDict` makes each field read `VIZ_`-prefixed vars. This is how you keep an use's config from colliding with all else in a holder.

**clear.** `Field(validation_alias="DATABASE_URL")` pins one field to one var. This Is what you need for the shared names that don't follow your prefix &mdash; `DATABASE_URL`, `PORT`, `TZ`.

`AliasChoices` works here too. This Is the clean way to accept both an old and a new var name during a migration.

## Checking, not just typing

A settings model is a model. All from the earlier tiers applies. And config is a place where that matters more than people expect.

```python
port: int = Field(ge=1, le=65535)
env: Literal["dev", "test", "prod"]
workers: int = Field(gt=0)
```

`ENV=staging` now fails at boot with a message naming the three permitted values. Without it, `staging` passes through the use and makes action no one intended. Some `if env == "prod"` was false and nothing said so.

This is the strongest arg for settings models over a config dict. Config errors are among the most common causes of production incidents. Almost all of them are typos or values outside a permitted set. Both are just what check catches.

checkers work too, for cross-field rules. "if `TLS_ENABLED`, then `CERT_PATH` must be set" is a `model_validator` and a truly handy one.

## Nesting

Grouped config can be a nested model, filled two ways.

From JSON in one var: `REDIS='{"host": "cache", "port": 6380}'`.

Or from delimited names, with `env_nested_delimiter="__"`: `REDIS__HOST=cache` and `REDIS__PORT=6380`.

The delimited form is often nicer operationally. Each value is its own var. It can be set on its own and overridden per setting without rewriting a JSON blob.

## Files

`env_file=".env"` in `SettingsConfigDict` reads a dotenv file. This Is where local development config often lives. Real setting vars take precedence. A deployed process is never affected by a file that happened to ship.

There's also `secrets_dir`, which reads each field from a file of that name in a folder. The shape Docker and Kubernetes secrets use. Here A secret is mounted as a file rather than exposed in the setting.

The precedence order, highest first: values passed right to `Settings(...)`, then the setting, then the dotenv file, then the secrets folder, then defaults. That is worth knowing when a value isn't what you expected.

## Secrets

Use `SecretStr` for credentials, and the reason is exact.

A settings object is the single thing most likely to be printed. Log it at start-up to record the config. A plain `str` password is in your logs forever. Include it in an error report and it goes to your error tracker. `repr` it in a debugger session that gets pasted into a ticket, and it's in the ticket.

`SecretStr` displays as `**********` all over and needs `.get_secret_value()` to read. This Makes each real access deliberate and greppable.

Note that a `SecretStr` in `model_dump()` stays hidden. A settings dump is safe to log. Which is the property you want.

## One instance

Build it once and pass it around, or use a cached accessor:

```python
@lru_cache
def get_settings() -> Settings:
    return Settings()
```

Making settings reads the setting and validates. Doing that per request is wasted work. The cached function is also convenient in FastAPI. Here It can be a dependency and overridden in tests.

Avoid a module-level global made at import. It runs at import time. This Makes it awkward to test with other values and can fail before logging is configured. Making a start-up crash with no handy output.

## Testing

Two habits make settings testable.

Create with clear values: `Settings(app_port=1234)` bypasses the setting fully. This Is what a unit test wants.

And use `monkeypatch.setenv` for tests that truly exercise the setting reading. Don't mutate `os.environ` right. The change leaks into each test that follows.

## Layering environments

Most uses need the same settings with other values per setting. The clean shape uses plain class chain:

```python
class Settings(BaseSettings):
    env: Literal["dev", "test", "prod"] = "dev"
    debug: bool = False
    db_pool_size: int = 5

class ProdSettings(Settings):
    debug: bool = False
    db_pool_size: int = 20
```

That is better than branching on `env` inside the use. Each setting's config is stated in one place and can be read without tracing conditionals.

Where it goes wrong is depth. Three levels of settings class chain with replaces at each is harder to reason about than a flat model whose values come from the setting. Prefer supplying other values to the same model wherever you can. Reserve subclassing for genuine structural differences.

## What belongs in settings

Not all configurable belongs here.

**Yes:** anything that differs between settings (URLs, credentials, pool sizes, log levels), anything secret, anything an op may need to change without a deploy.

**No:** use constants that never vary, feature logic dressed up as config, or anything a caller supplies per request. That is a request model.

The test is whether a value could fairly differ between your laptop and production. If it couldn't, it's a constant. Making it configurable adds a failure mode with no gain. Another var that can be unset, misspelt or set to a thing nonsensical.

## Summary

`BaseSettings` treats config as untrusted input crossing a boundary. This Is what it's. Field names map to setting vars, `env_prefix` namespaces them, `validation_alias` pins the exceptions.

needed fields with no default make a misconfigured deployment fail at boot with the var named, rather than hours later. Constraints and `Literal` catch the typos and out-of-range values behind most config incidents. `SecretStr` keeps credentials out of the logs a settings object is uniquely likely to reach.

Build it once, cache it, and let it refuse to start when a thing is wrong.


## Mistakes people make

**Instantiating settings lazily.** The entire gain is failing at boot with the var named. Make them at start-up. A settings object built on first use turns a config error into a runtime one, hours later.

**Giving all a default.** A default on `DATABASE_URL` means a misconfigured deployment starts happily and points at the wrong DB. needed fields should be needed.

**A module-level global built at import.** It runs before logging is configured. A failure makes a crash with no handy output. It's awkward to test with other values. A cached accessor function is better.

**Plain `str` for credentials.** A settings object is the thing most likely to be logged at start-up or attached to an error report. `SecretStr` is the gap between that being routine and being an incident.

**`env: str` instead of a `Literal`.** `ENV=staging` then silently takes each else-branch in the use. Nothing anywhere says the value wasn't recognised.

**Mutating `os.environ` in tests.** It leaks into each test that follows and makes failures that depend on sorting. `monkeypatch.setenv`, or pass values right.

**Configuring things that never vary.** each setting is another var that can be unset, misspelt or set to a thing nonsensical. If it couldn't fairly differ between your laptop and production, it's a constant.

## Testing configuration

Two habits keep settings testable.

Create with clear values where the test isn't about the setting: `Settings(port=1234)` bypasses reading it fully. This Is what a unit test wants and is far clearer than arranging vars around the call.

Use `monkeypatch.setenv` when the test truly exercises the reading, never a direct mutation of `os.environ`. That leaks into each test after it and makes failures that depend on sorting.

And test the failure case. A test asserting that a missing `DATABASE_URL` raises is worth having. It's the action the whole module exists for. It's the one no one notices has broken until a deployment comes up healthy with no DB.

## A last note on start-up

There's a general principle behind this module worth stating on its own.

The best time to discover that a thing is misconfigured is before the process claims to be ready. Not on the first request, not when a code path is first taken. Not at three in the morning when the only person who knows what `WORKERS` should be is asleep.

A settings model turns config from a thing an use discovers bit by bit into a thing it asserts at boot. each needed var is checked, each value is converted to the type the code expects, each constrained field is inside its range. If any of that fails the process stops with a message naming just what is wrong.

That is the same arg as checking a request body, applied to the other kind of input a program takes. It's just that request bodies are obviously untrusted and config often isn't treated that way. Which is just why config errors cause so many incidents.

## One habit

Create settings on the first line of your use's start-up, before anything else runs.

That single placement choice is what converts a class of production incident into a failed deploy. all else in this module is detail around it.
''',
    [
        {"q": "Why does a required setting with no default matter?",
         "options": ["It is faster", "The process fails at boot naming the variable, instead of producing a None that fails hours later", "It saves memory", "It enables caching"],
         "answer": 1,
         "why": "Failing before the process claims to be ready is the whole point. A missing variable that becomes None surfaces far from its cause, whenever that code path is first taken."},
        {"q": "`APP_DEBUG=false` with a `bool` field gives what?",
         "options": ["True, because the string is non-empty", "False", "A ValidationError", "None"],
         "answer": 1,
         "why": "Pydantic reads the meaning of the word, unlike `bool(os.environ.get(...))` where any non-empty string is truthy. That difference is a classic configuration bug."},
        {"q": "Why is `env: Literal[\"dev\", \"test\", \"prod\"]` better than `env: str`?",
         "options": ["It is faster", "ENV=staging fails at boot with the permitted values named, instead of silently taking every else-branch", "It uses less memory", "No difference"],
         "answer": 1,
         "why": "Typos and out-of-range values cause most configuration incidents. A closed set catches them at start-up rather than letting them alter behaviour silently."},
        {"q": "Why use `SecretStr` in a settings model specifically?",
         "options": ["It encrypts the value", "A settings object is the thing most likely to be logged or printed at start-up", "It is required", "It speeds up reading"],
         "answer": 1,
         "why": "It is not encryption - it hides the value from repr, logs and tracebacks, and requires `.get_secret_value()` so every real access is deliberate."},
    ],
    wheels=["python_dotenv-1.2.3-py3-none-any.whl",
            "pydantic_settings-2.3.4-py3-none-any.whl"],
)


# ---------------------------------------------------------------------------
# 28. Pydantic with FastAPI
# ---------------------------------------------------------------------------
topic(
    "pydantic_with_fastapi",
    "Pydantic with FastAPI",
    "In Practice",
    "The reason most people arrive here: request bodies, response models and "
    "documentation generated from the annotations you already wrote.",
    _svg(_box(12, 22, 46, 22, S) + _txt(35, 36, "request", M, 8) +
         _arrow(60, 33, 74, 33) +
         _box(78, 22, 66, 22, S, A) + _txt(111, 36, "BaseModel", A, 8) +
         _arrow(111, 48, 111, 60) + _txt(80, 74, "422 / docs / client", M, 8)),
    [
        ("A model is the request body",
         "Annotate a parameter with a model and FastAPI parses, validates and hands "
         "you a real object. <code>client</code> calls the app through ASGI.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0, le=180)

@app.post("/modules/", status_code=201)
def create(module: ModuleIn):
    return {"created": module.title, "minutes": module.minutes}

client = TestClient(app)

r = client.post("/modules/", json={"title": "Vectors", "minutes": "8"})
print(r.status_code, r.json())
print()
print("the string 8 became an int before the handler ran")'''),

        ("Validation failures become 422",
         "A <code>ValidationError</code> on a request body is turned into a 422 whose "
         "body is really just <code>errors()</code>.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

@app.post("/modules/")
def create(module: ModuleIn):
    return {"ok": True}

client = TestClient(app)

r = client.post("/modules/", json={"title": "no", "minutes": -1})
print("status:", r.status_code)
for err in r.json()["detail"]:
    print("  %-22s %-18s %s" % (".".join(str(p) for p in err["loc"]),
                                err["type"], err["msg"]))'''),

        ("Path and query parameters too",
         "The same rules apply to values from the URL. The <code>loc</code> tells the "
         "caller which part of the request was wrong.",
         '''from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/modules/{module_id}")
def read(module_id: int, verbose: bool = False, q: Optional[str] = None):
    return {"id": module_id, "verbose": verbose, "q": q}

client = TestClient(app)

print(client.get("/modules/7").json())
print(client.get("/modules/7?verbose=yes&q=norms").json())

r = client.get("/modules/abc")
print()
print("bad path:", r.status_code, r.json()["detail"][0]["loc"],
      r.json()["detail"][0]["type"])'''),

        ("response_model shapes what comes back",
         "The output is validated and filtered against the model, so a field the "
         "response model does not declare cannot leak.",
         '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserOut(BaseModel):
    id: int
    name: str

@app.get("/users/{user_id}", response_model=UserOut)
def read(user_id: int):
    # The handler returns more than the response model declares.
    return {"id": user_id, "name": "Ada",
            "password_hash": "$2b$12$secret",
            "internal_note": "do not ship"}

client = TestClient(app)
print(client.get("/users/1").json())
print()
print("The extra keys were filtered out by the response model.")'''),

        ("Three models for one resource",
         "Create, update and output are different shapes. Separate models say what "
         "each endpoint actually accepts and returns.",
         '''from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
DB = {1: {"id": 1, "title": "Vectors", "minutes": 8}}

class ModuleCreate(BaseModel):
    title: str
    minutes: int = 10

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    minutes: Optional[int] = None

class ModuleOut(BaseModel):
    id: int
    title: str
    minutes: int

@app.patch("/modules/{module_id}", response_model=ModuleOut)
def update(module_id: int, patch: ModuleUpdate):
    stored = DB[module_id]
    stored.update(patch.model_dump(exclude_unset=True))   # only what was sent
    return stored

client = TestClient(app)
print("before:", DB[1])
print("patch :", client.patch("/modules/1", json={"minutes": 12}).json())
print("title untouched, because it was never sent")'''),

        ("The schema is the documentation",
         "Everything you wrote &mdash; constraints, descriptions, examples &mdash; is "
         "in the OpenAPI document FastAPI serves.",
         '''import json
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="VizLearn API")

class ModuleIn(BaseModel):
    title: str = Field(min_length=3, description="Shown as the page heading.",
                       examples=["Dot Product"])
    minutes: int = Field(default=10, gt=0, le=180,
                         description="Estimated reading time.")

@app.post("/modules/")
def create(module: ModuleIn):
    return module

spec = app.openapi()
print("paths  :", list(spec["paths"]))
print()
schema = spec["components"]["schemas"]["ModuleIn"]
for name, prop in schema["properties"].items():
    print("%-8s %s" % (name, json.dumps(prop)))'''),
    ],
    [
        "A parameter annotated with a model <em>is</em> the request body. FastAPI parses the JSON and validates it before your handler runs.",
        "A <code>ValidationError</code> becomes a 422 whose <code>detail</code> is really just <code>e.errors()</code> &mdash; the shape you already know how to read.",
        "Path and query parameters are validated by the same rules, and <code>loc</code> starts with <code>path</code>, <code>query</code> or <code>body</code>.",
        "<code>response_model</code> validates <em>and filters</em> the output, so a field it does not declare cannot leak from a handler that returned too much.",
        "Use separate <code>Create</code>, <code>Update</code> and <code>Out</code> models. One model with everything optional documents nothing.",
        "Your constraints, descriptions and examples are the OpenAPI document, which is the interactive docs and every generated client.",
    ],
    '''
title: Pydantic with FastAPI: Where It All Arrives
intro: Request bodies, response models and docs, all from annotations you already wrote.

## Why this is the common entry point

FastAPI is the most common way people first meet Pydantic. You write a model, use it as the type of a function argument, and FastAPI does the rest. It reads the request body, validates it with your model, and hands your function a typed object.

That is a lot of work done by one annotation. The same model also feeds the interactive documentation, because FastAPI turns it into an OpenAPI schema. And when validation fails, FastAPI sends back a 422 response that carries the Pydantic errors in a structured form. You did not write any of that code.

This article explains why this is the usual entry point, and how the pieces fit. It covers the request body and how the model becomes the contract. It then looks at the 422 response and what it contains, so you can read it and shape it. The last part is about response_model, which does two jobs at once: it filters what you return and it documents it. Once you see how the model sits in the middle of the framework, the rest of FastAPI makes more sense.

You do not need to know FastAPI well to follow this. The focus stays on the model and what the framework does with it. Every behaviour described here comes from a few lines you write, plus conventions the framework applies for you. Knowing which part comes from which side makes debugging much easier.

The examples stay small and focused.

Most people meet Pydantic through FastAPI. Often without realising they're two libraries. That is a compliment to the integration and it leaves a gap. All that looks like FastAPI magic is Pydantic doing what the previous tiers given.

FastAPI has no check layer of its own. It reads your annotations, hands the request body to a Pydantic model, converts the resulting `ValidationError` into a 422. Turns the made JSON Schema into your docs. That is the whole of it. Knowing where the line falls makes both easier to reason about.

## The request body

```python
@app.post("/modules/", status_code=201)
def create(module: ModuleIn):
    return {"created": module.title}
```

A param annotated with a model is the body. FastAPI reads the request, validates it with `model_validate_json`. Calls your handler with a real object.

By the time your code runs, `module.minutes` is an int. Even if the client sent `"8"`. And each constraint has passed. There's no checking to do at the top of the handler. This Is the point.

Scalars annotated with plain types become query or path params. The same coercion applies: `?verbose=yes` turns `True` because of the boolean vocab from the coercion module.

## 422, and what it contains

When check fails, the handler never runs. FastAPI returns 422 with a body whose `detail` is `e.errors()`.

So all from the errors module applies right to what your API returns. `loc` is a path. Its first element is `body`, `path`, `query` or `header`. Telling the caller which part of the request was wrong before naming the field within it.

That is worth showing your API's consumers. A 422 from a FastAPI service is more helpful than most people realise. Clients often discard it and report "bad request".

If you want a other shape, an exception handler for `RequestValidationError` lets you reformat it globally. And the grouping code from the errors module drops straight in.

## response_model does two things

```python
@app.get("/users/{user_id}", response_model=UserOut)
```

It **validates** the output. This Catches a handler returning the wrong shape before a client does.

And it **filters** the output to the model's fields. A handler returning a dict with `password_hash` in it makes a response without one. `UserOut` doesn't declare it.

That second action is a genuine security property and worth leaning on on purpose. The pattern to internalise. A response model should list just what a caller may see. Then over-returning from a handler can't leak. Leaning instead on the handler returning just the right keys means each future edit to that handler is a chance to leak a thing.

It also fixes the schema. Without `response_model` the docs can't say what an endpoint returns. With it, consumers get a typed response.

## Three models, not one

The instinct is one `Module` model all over. Resist it, for the reasons the defaults module gave.

**Create** takes what a caller may supply. No `id`. Not optional, absent. Because the server assigns it.

**Update** has all optional, and the handler applies `model_dump(exclude_unset=True)` so untouched fields stay untouched. This is the correct PATCH shape, and getting it wrong is how six columns become `None`.

**Out** declares just what may be seen, with server-assigned fields needed.

Three small classes, each honest. One model with all optional makes docs that promises nothing and a response type no client can lean on.

## Dependencies

`Depends` composes checked values the same way:

```python
def pagination(page: int = 1, size: int = Query(default=20, le=100)) -> Page:
    return Page(page=page, size=size)

@app.get("/modules/")
def list_modules(p: Page = Depends(pagination)):
    ...
```

The dependency's params are checked like any others. The constraint on `size` is enforced and documented. Each endpoint using it takes from both.

`get_settings` from the settings module is the same pattern. Being a dependency makes it overridable in tests.

## Where validation stops

The line from the checkers module matters here more than anywhere.

A model checks shape and inner agreement. "Does this track exist?" is a fact about the world. It belongs in the handler or the service layer. Not least because the right response is a 404 or a 409, not a 422.

Keeping that split means your models stay testable without a DB. Your status codes stay real.

## The documentation is your schema

`app.openapi()` is assembled from `model_json_schema()` for each model you used. Which means each recommendation from the schema module cashes out here:

A `Field(gt=0)` appears as a documented min. A checker checking the same thing appears as nothing.

A `Literal` turns a set of choices in the docs and a union type in a made client. A `pattern` turns an opaque string.

A `description` appears beside the field. An `examples` entry pre-fills the interactive request form. A first-time caller can send a working request instead of guessing.

This is the concrete payback for being exact in your annotations. It's visible to everybody who uses your API rather than only to you.

## A note on this page

There's no server here &mdash; a browser tab can't listen on a port. `client` calls the app through ASGI. This Is the same interface uvicorn uses. Routing, check, status codes and schema making all behave just as they would in production.

The full reason, and the one action that truly differs, is on the [FastAPI compiler](../fastapi-lab/) page.

## Where the boundary between the two libraries falls

It's worth being able to say which library is doing what. It changes where you look when a thing is wrong.

**FastAPI** decides routing, reads the request, chooses which params come from the path, the query and the body, calls your handler. Turns the result into a response. It also assembles the OpenAPI doc.

**Pydantic** validates and converts each one of those values, makes the errors. Makes the schema for each model that goes into the doc.

So a 422 you disagree with is a Pydantic question. A model's annotations, constraints or checkers. A field arriving from the wrong part of the request is a FastAPI question. docs that is missing a constraint is a Pydantic question. The constraint was never in the schema.

Most confusion about "FastAPI check" resolves the moment that split is clear.

## Dependencies and settings

The settings model from the previous module composes on its own here:

```python
@lru_cache
def get_settings() -> Settings:
    return Settings()

@app.get("/health")
def health(settings: Settings = Depends(get_settings)):
    return {"env": settings.env}
```

Cached, so the setting is read and checked once rather than per request. And overridable in tests through FastAPI's dependency replaces. This Is much cleaner than mutating the setting around a test.

The same pattern covers anything made once and used all over. A DB session factory, a client for another service, a pagination object built from checked query params.

## Summary

A model param is the request body, checked before your handler runs. Failures become a 422 whose `detail` is `e.errors()`, with `loc` naming which part of the request was wrong.

`response_model` validates and filters the output. Undeclared fields can't leak. A property worth leaning on on purpose rather than trusting each handler to return just the right keys.

split `Create`, `Update` and `Out` models per resource. Keep facts about the world in the service layer and shape in the model. And prefer constraints to checkers. Only one of them reaches the docs your callers read.


## Mistakes people make

**No `response_model`.** The docs can't say what the endpoint returns. Nothing filters the output. A handler that starts returning an extra key starts leaking it.

**One model for each direction.** all optional so it can serve create, update and read at once. It docs nothing. No client can tell what is sure in a response.

**Dumping the whole update model.** `patch.model_dump()` without `exclude_unset=True` writes each field. Untouched columns are overwritten with `None` or defaults. This is the bug behind "it cleared fields I never edited".

**Putting existence checks in checkers.** "Does this track exist" belongs in the handler. In a model it makes check an I/O call, makes the model untestable without a DB. Returns a 422 where a 404 was correct.

**checkers instead of constraints.** Both reject the same values. Only the constraint appears in the docs and in made clients. Your callers see one of them.

**given a 422 body is opaque.** It's `e.errors()`, with `loc` naming body, path or query and then the field. A lot of clients discard it and report "bad request" when the exact problem was right there.

**Instantiating settings per request.** Reading and checking the setting on each call is wasted work. Cache it with `lru_cache` and inject it with `Depends`. This Is also what makes it overridable in tests.

## A last habit

Open your own `/docs` page at times and read it as a consumer would.

It's made from your models. All this track has argued about being exact in annotations is visible there and nowhere else in your workflow. Fields with no description. A `str` where a `Literal` belongs. An endpoint with no `response_model`. So The response section says nothing. A needed field you meant to default.

None of that shows up in your tests. Your tests know what they're sending. It shows up for the person integrating with you, at the point where it's costly to ask you about it.

Five minutes reading your own docs catches most of it. It's the same five minutes recommended in the schema module. Just from the other end.

## Where to go from here

This is the last module in the track. The one where all else cashes out.

The annotations from tier one decide what a request body accepts. The shapes from tier two. Nested models, sets, discriminated unions, closed sets. Decide how expressive your API can be about its own data. The checkers and config from tier three enforce what annotations can't say. The output and schema work from tier four decides what consumers receive and what your docs tells them.

FastAPI adds routing and an HTTP layer on top. Almost nothing else. Which means the quality of an API built this way is very largely the quality of its models.

That is a good spot to be in. Models are cheap to improve. Narrowing a `str` to a `Literal`, moving a rule from a checker to a constraint, splitting one all-optional model into three honest ones, adding a description to a field whose name isn't self-explanatory. Each is a small edit. Each is visible to everybody who calls you.

## One last thing to check

Before shipping an endpoint, three questions that take a minute each.

**Does it have a `response_model`?** Without one the docs says nothing about the response. Nothing filters what a handler returns.

**Is the update path using `exclude_unset=True`?** Without it, a PATCH overwrites fields the caller never mentioned.

**Would a 422 from this endpoint tell a caller what to fix?** If a field is a bare `str` where a `Literal` belongs, or a rule lives in a checker that the schema can't show, the answer is no. And the caller finds out by being rejected rather than by reading.

''',
    [
        {"q": "What does `response_model` do besides validating the output?",
         "options": ["Nothing", "Filters it to the declared fields, so undeclared keys cannot leak", "Caches it", "Sets the status code"],
         "answer": 1,
         "why": "A handler returning a dict with `password_hash` produces a response without one. It is a real security property, and more reliable than trusting every future edit of the handler."},
        {"q": "What is in a FastAPI 422 response body?",
         "options": ["A plain string", "Essentially `e.errors()` - loc, type, msg and input per failure", "Only the first error", "Nothing useful"],
         "answer": 1,
         "why": "Everything from the errors module applies directly, with `loc` starting at `body`, `path`, `query` or `header` to say which part of the request was wrong."},
        {"q": "Why separate Create, Update and Out models?",
         "options": ["FastAPI requires it", "Each says what that endpoint actually accepts or returns; one all-optional model guarantees nothing", "It is faster", "For nesting"],
         "answer": 1,
         "why": "Create excludes server-assigned fields, Update is all-optional for `exclude_unset`, Out declares exactly what may be seen. Collapsing them produces documentation that promises nothing."},
        {"q": "Where does 'does this track exist?' belong?",
         "options": ["A field validator", "A model validator", "The handler or service layer", "response_model"],
         "answer": 2,
         "why": "It is a fact about the world, not the shape of the payload - and the right answer is a 404 or 409 rather than a 422. Keeping it out also keeps models testable without a database."},
    ],
    wheels=["sniffio-1.3.1-py3-none-any.whl",
            "anyio-4.6.2.post1-py3-none-any.whl",
            "starlette-0.41.3-py3-none-any.whl",
            "fastapi-0.115.6-py3-none-any.whl"],
    prelude=__import__("build_fastapi_lab").PRELUDE,
)


# ---------------------------------------------------------------------------
# 29. Performance and pydantic-core
# ---------------------------------------------------------------------------
topic(
    "performance_and_pydantic_core",
    "Performance and pydantic-core",
    "In Practice",
    "Why v2 is fast, what validation actually costs, and the three habits that "
    "account for most of the difference.",
    _svg(_box(16, 18, 128, 24, S) + _txt(80, 34, "Python: reads annotations", M, 8) +
         _arrow(80, 46, 80, 54) +
         _box(16, 56, 128, 22, S, A) + _txt(80, 71, "Rust core: runs the schema", A, 8)),
    [
        ("Already-correct types are nearly free",
         "Validation cost depends on how much converting there is to do. A value that "
         "is already right is checked and passed through.",
         '''import time
from pydantic import BaseModel

class Point(BaseModel):
    x: float
    y: float

N = 20000

t = time.perf_counter()
for _ in range(N):
    Point(x=1.0, y=2.0)          # already floats
native = time.perf_counter() - t

t = time.perf_counter()
for _ in range(N):
    Point(x="1.0", y="2.0")      # strings needing conversion
converted = time.perf_counter() - t

print("already typed : %.3f s" % native)
print("needing parse : %.3f s" % converted)
print("ratio         : %.2fx" % (converted / native))'''),

        ("Validate once, not at every layer",
         "Re-validating something that has already passed is the most expensive no-op "
         "available. The result is identical.",
         '''import time
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    minutes: int

rows = [{"title": "M%d" % i, "minutes": i % 60} for i in range(3000)]

t = time.perf_counter()
once = [Module.model_validate(r) for r in rows]
first = time.perf_counter() - t

t = time.perf_counter()
again = [Module.model_validate(m) for m in once]     # they are already models
second = time.perf_counter() - t

print("first pass  : %.3f s" % first)
print("second pass : %.3f s" % second)
print("gained      :", once == again, "- nothing at all")'''),

        ("Let the core do the looping",
         "One call into Rust for a whole list beats a Python loop making one call per "
         "item. Same result, less crossing back and forth.",
         '''import time
from typing import List
from pydantic import BaseModel, TypeAdapter

class Module(BaseModel):
    title: str
    minutes: int

rows = [{"title": "M%d" % i, "minutes": i % 60} for i in range(4000)]
adapter = TypeAdapter(List[Module])

t = time.perf_counter()
a = [Module.model_validate(r) for r in rows]
per_item = time.perf_counter() - t

t = time.perf_counter()
b = adapter.validate_python(rows)
whole = time.perf_counter() - t

print("per item   : %.3f s" % per_item)
print("whole list : %.3f s" % whole)
print("ratio      : %.1fx" % (per_item / whole))
print("identical  :", a == b)'''),

        ("Validators are Python in a Rust pipeline",
         "Every custom validator is a call back out of the compiled core. A constraint "
         "doing the same job stays inside it.",
         '''import time
from pydantic import BaseModel, Field, field_validator

class ByConstraint(BaseModel):
    minutes: int = Field(gt=0, le=180)

class ByValidator(BaseModel):
    minutes: int

    @field_validator("minutes")
    @classmethod
    def check(cls, v: int) -> int:
        if not 0 < v <= 180:
            raise ValueError("out of range")
        return v

N = 20000
for cls in (ByConstraint, ByValidator):
    t = time.perf_counter()
    for _ in range(N):
        cls(minutes=30)
    print("%-13s %.3f s" % (cls.__name__, time.perf_counter() - t))

print()
print("Same rule. One runs in Rust, the other calls into Python per item.")'''),

        ("Build schemas once",
         "Constructing a model class or a TypeAdapter compiles a schema. Doing it "
         "inside a loop repeats that work every time.",
         '''import time
from typing import List
from pydantic import TypeAdapter

rows = [[1, 2, 3] for _ in range(400)]

t = time.perf_counter()
for row in rows:
    TypeAdapter(List[int]).validate_python(row)
rebuilt = time.perf_counter() - t

adapter = TypeAdapter(List[int])
t = time.perf_counter()
for row in rows:
    adapter.validate_python(row)
reused = time.perf_counter() - t

print("rebuilt each time : %.4f s" % rebuilt)
print("built once        : %.4f s" % reused)
print("ratio             : %.1fx" % (rebuilt / reused))'''),

        ("Parsing JSON directly",
         "The last of the three habits: hand the text over instead of building an "
         "intermediate dict for it.",
         '''import json, time
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    minutes: int

payload = json.dumps({"title": "Vectors", "minutes": 8})
N = 8000

t = time.perf_counter()
for _ in range(N):
    Module.model_validate(json.loads(payload))
two_step = time.perf_counter() - t

t = time.perf_counter()
for _ in range(N):
    Module.model_validate_json(payload)
one_step = time.perf_counter() - t

print("json.loads + validate : %.3f s" % two_step)
print("model_validate_json   : %.3f s" % one_step)
print("ratio                 : %.2fx" % (two_step / one_step))'''),
    ],
    [
        "Pydantic v2 is two pieces: a Python layer that reads your annotations and builds a schema, and <code>pydantic-core</code>, a Rust engine that executes it.",
        "Cost scales with how much converting is needed. A value already of the right type is checked and passed through cheaply.",
        "Validate <strong>once</strong>, at the boundary. Re-validating an object that has already passed produces the same result for the full price.",
        "Validate a collection in <strong>one call</strong> &mdash; <code>TypeAdapter(List[X])</code> &mdash; so the loop happens inside the core rather than in Python.",
        "Every custom validator is a call back out into Python. A <code>Field</code> constraint doing the same job stays in Rust.",
        "These timings run on WebAssembly, several times slower than a native interpreter. The <em>ratios</em> transfer; the seconds do not.",
    ],
    '''
title: Performance and pydantic-core: What Validation Actually Costs
intro: Why v2 is fast. Here The time goes. The three habits that account for most of the gap.

## Two libraries in a trench coat

People ask whether Pydantic is fast enough. In version 2 the answer is usually yes, because the validation engine is written in Rust. That engine is a separate library called pydantic-core, and the Python library you import sits on top of it. So there are two libraries working together.

Knowing that split helps you reason about speed. The Rust part is quick at the checks it knows how to do. The Python part, including any validator you write, runs at Python speed. So the time goes where your own code runs, not where the library does.

This article starts with how the two libraries fit together. It shows where the time actually goes when you validate data, which is often not where people expect. It gives three habits that keep things quick, such as parsing JSON directly and building adapters once. It then looks at validators, which are the expensive part, and how to keep them cheap. You do not need to optimise early, but you should know which choices cost something. That lets you make sensible decisions without measuring everything first.

Installing `pydantic` installs two things.

A **Python layer** that reads your class, reads the annotations, resolves types. Builds a schema showing how to validate the model. This runs once, when the class is defined.

**`pydantic-core`**, a compiled Rust engine that runs that schema against data. This runs each time you validate.

Almost all about v2's speed follows from that split. check is compiled code walking a prepared schema, not Python reading annotations per call. Version 1 did the latter. This Is why v2 was a rewrite rather than an tuning.

It also shows details you'll have noticed. Error `type` codes look like machine identifiers because they come from the core. `model_validate_json` beats parsing apart because the core parses and validates in one pass. And there's a compiled wheel per platform. There's compiled code in there.

## Where the time actually goes

Three parts, worth separating.

**Schema building** happens once per class or adapter. It's the most costly single step and it should be invisible. Unless you build schemas again and again. This Is the mistake below.

**check** happens per value. Cost scales with how much work there's. A value already of the right type is checked and passed through. One needing conversion costs more. One needing a custom checker costs the most. That means leaving Rust for Python.

**output** is often cheaper than check, and follows the same shape.

## The three habits

Almost all avoidable cost comes down to three things.

### Validate once

The rule from the first module, restated as a speed point. Re-checking an object that has already passed makes an same result for the full price.

It happens more than people expect. A model checked in a request handler, passed to a service that validates it again, handed to a store that makes its own model from it. Each layer is defensively re-checking data that can't have changed.

The discipline is to decide where the boundary is and trust all past it. If a function's arg is a model, it has been checked. Checking again buys nothing.

The exception is truly mutable data. If `validate_assignment` is off and a thing has been assigning freely, the object may no longer match its annotations. But the fix there's to turn on the setting or freeze the model, not to re-validate.

### Validate collections in one call

```python
[Model.model_validate(r) for r in rows]              # per item
TypeAdapter(List[Model]).validate_python(rows)       # whole list
```

same results. The first crosses between Python and Rust once per row. The second makes one call and loops inside the core.

For bulk work &mdash; a file import, a batch job, a large API response &mdash; this is the single most good change on hand, and it's one line.

### Parse JSON directly

`model_validate_json(raw)` rather than `model_validate(json.loads(raw))`.

The two-step form builds a full mid structure of Python objects, then converts it again. The direct form reads the text and makes the final values in one pass.

As the parsing module covered, it's also better for errors and for decimal precision. Three gains for less code.

## Validators are the expensive part

A `field_validator` is Python. each time it runs, the core suspends, calls into the interpreter, and resumes.

For a model built a few times per request that is irrelevant. For a hundred thousand rows it's the dominant cost, and it's worth two questions.

**Could this be a constraint?** `Field(gt=0)` and a checker checking `v > 0` reject the same values. The constraint runs in Rust. It also reaches the schema. This Is the more key reason.

**Is it doing work that could be done once?** A checker that rebuilds a set of permitted values on each call is doing that per item. Hoisting it to module level is often a bigger win than anything else in the model.

## Building schemas repeatedly

The mistake that looks like nothing in review:

```python
for row in rows:
    TypeAdapter(List[int]).validate_python(row)     # recompiles every iteration
```

Adapters belong at module level. The same applies to any pattern that defines a model class inside a function called again and again. Each call builds a new class and a new schema.

Where the type is only known at runtime, cache the adapters in a dict keyed by type, or wrap a factory in `functools.lru_cache`.

## Keeping perspective

Two things worth saying plainly.

**check is often not your bottleneck.** A model checking in single-digit microseconds sits next to a DB query taking milliseconds and a network call taking hundreds. In a common request handler, check is a rounding error. Choosing a dataclass "for speed" in a handler that then makes three SQL queries is optimising the wrong end.

**Measure before changing anything.** The habits above are free. Adopt them because they're also clearer. Anything beyond them should follow a profile, not an intuition.

The place check truly dominates is bulk: large sets, file imports, high-throughput pipelines. That is where the one-call-per-set rule earns real time.

## A note on these timings

each reading on this page runs on CPython compiled to WebAssembly, a few times slower than a native interpreter, on one core.

The **ratios** transfer &mdash; checking a list in one call really is faster than looping, by roughly the factor shown. The **abs seconds** don't. Don't quote them as figures for a server.

That caveat applies to any benchmark run anywhere, including ones you write yourself on your laptop. scaled checks under same rules are helpful. Abs numbers are a property of the machine.

## Summary

Pydantic v2 is a Python layer that builds schemas and a Rust core that runs them. This Is why check is cheap enough to do on each request.

Three habits account for most of the avoidable cost. Validate once at the boundary, validate sets in a single call. Parse JSON right. Prefer constraints over checkers where either would do. Build schemas once rather than in a loop.

Then stop, because check is rarely the slow part. The left questions belong to a profiler rather than to a rule of thumb.

## What not to optimise

A short list of things that look like speed choices and aren't.

**Choosing a dataclass over a model in a request handler.** The handler then makes three DB queries. The check was never the cost.

**Skipping check on data from your own DB.** It's cheap on already-correct types. The promise is worth more than the microseconds. If a column can be null and the model says it can't, you want to know.

**Avoiding nested models to reduce check count.** A flat model with the same fields does the same total work. Nesting is an organisational choice, not a speed one.

**Reaching for `model_construct`.** It skips check fully. This Makes it fast and unsafe. It exists for cases where the data provably came from a trusted source. Rebuilding from your own cache, say. Using it to speed up a normal path drops the property you installed the library for.

## Measuring properly

If you do need to measure, three things make the result real.

**Warm up.** The first build of a model builds its schema. Timing that alongside the validations makes the first run look terrible and tells you nothing about the steady state.

**Time the right thing.** Wrap the check, not the loop that also builds the input data. Making ten thousand dicts isn't free either.

**Compare under same rules.** Same machine, same process, same interpreter. abs numbers don't live a move between any of those. This Is why the timings on this page are presented as ratios.

`time.perf_counter` is enough for A-versus-B. For finding where time goes in a real use, a profiler will point at the DB long before it points at check.

## Mistakes people make

**Re-checking what has already passed.** The most common and most costly no-op. If a function's arg is a model, it was checked. Checking again makes an same result for the full price.

**Looping in Python over a set.** `[Model.model_validate(r) for r in rows]` crosses into Rust once per row. One call with a `TypeAdapter(List[Model])` does the loop inside the core.

**Building schemas again and again.** A `TypeAdapter` made inside a loop, or a model class defined inside a function called per request, recompiles a schema each time. Module level, once.

**Doing work inside a checker that could be done outside.** Rebuilding a set of permitted values on each call does it per item. Hoisting it's often a bigger win than anything else in the model.

**Using `model_construct` to go faster.** It skips check fully. That is correct for rebuilding from a provably trusted source and a way of quietly dropping the promise all over else.

**Optimising check before profiling.** In a handler that makes three DB queries, check is a rounding error. A profiler will point at the DB long before it points here.

**Quoting benchmark seconds.** abs numbers are a property of the machine. Doubly so on this page. This Runs on WebAssembly. Ratios under same rules transfer. Seconds don't.

## Why it was worth rewriting

It's worth understanding what the v2 rewrite really bought. It shows why this module is short.

In v1, check was Python reading annotations on each call. That put Pydantic on the key path of a lot of uses in a way that showed up in profiles. Made "is check too slow?" a fair question to ask routinely.

Moving run into Rust changed the answer from "at times" to "almost never". A model that validates in a few microseconds doesn't compete with anything else in a request.

So the hands-on guidance became much simpler: adopt the three habits because they're also clearer code. Else stop thinking about it. That is a better place to be than a set of tuning tricks. It's the reason most of this module is about what not to optimise.

## The honest summary

Most uses shouldn't think about this module at all.

Adopt the three habits &mdash; validate once, validate sets in one call, parse JSON right &mdash; because each is also clearer code than the option. Then stop. They aren't speed tricks. They're the obvious way to write it. This Happens also to be the fast way.

If a thing is truly slow, profile it. The answer will often be I/O. On the occasions it really is check the answer will often be one of the three habits not being followed, or a checker doing per-item work that belongs outside the loop.

What changed in v2 is that this stopped being a live concern for plain code. check used to be a thing you budgeted for. Now it's a thing you can put at each boundary without thinking about the cost. That is a better outcome than any tuning advice.

## In one line

Validate once at the boundary, validate sets in a single call. Hand JSON straight to Pydantic. Then stop thinking about it. In v2 check is almost never the slow part.

## A closing thought

The most handy speed property of Pydantic v2 isn't that it's fast. It's that it's fast enough to stop being a consideration.

That changes how you write code. check at each boundary stops being a trade-off and turns the default. This Means more of your program can assume its inputs are correct. And that is worth a lot more than the microseconds.
''',
    [
        {"q": "What are the two pieces of Pydantic v2?",
         "options": ["A parser and a serialiser", "A Python layer that builds schemas and a Rust core that executes them", "Two Python packages", "A validator and a model class"],
         "answer": 1,
         "why": "Schema building happens once per class in Python; validation runs compiled Rust against that schema. That split is why v2 is fast and why v1 needed a rewrite rather than tuning."},
        {"q": "Which is faster for validating 4,000 rows?",
         "options": ["A comprehension of model_validate", "TypeAdapter(List[Model]).validate_python(rows)", "Identical", "Depends on the model"],
         "answer": 1,
         "why": "One call lets the loop happen inside the core. The comprehension crosses between Python and Rust once per row - the most effective one-line change for bulk work."},
        {"q": "Why is a `field_validator` more expensive than an equivalent `Field` constraint?",
         "options": ["It is not", "It calls out of the Rust core into Python for every value", "It validates twice", "It rebuilds the schema"],
         "answer": 1,
         "why": "Constraints run inside the compiled core; a validator suspends it to call the interpreter. The constraint also reaches the schema, which is the more important reason to prefer it."},
        {"q": "How should the timings on this page be read?",
         "options": ["As figures for a production server", "As ratios only - WebAssembly is several times slower than a native interpreter", "As worst cases", "They are exact"],
         "answer": 1,
         "why": "Relative comparisons under identical conditions transfer; absolute seconds are a property of the machine. That is true of any benchmark, including ones you run yourself."},
    ],
)


# ---------------------------------------------------------------------------
# 30. Migrating v1 to v2
# ---------------------------------------------------------------------------
topic(
    "migrating_v1_to_v2",
    "Migrating v1 to v2",
    "In Practice",
    "The renames, the behaviour changes that do not raise, and how to tell which "
    "version a tutorial is describing.",
    _svg(_box(12, 24, 56, 24, S) + _txt(40, 40, ".dict()", M, 8) +
         _arrow(72, 36, 90, 36) +
         _box(94, 24, 54, 24, S, A) + _txt(121, 40, "model_dump", A, 8) +
         _txt(80, 68, "v1  ->  v2", M, 8)),
    [
        ("The method renames",
         "The most visible change. The old names still exist in v2 and warn, which is "
         "why so much code and so many tutorials still use them.",
         '''from pydantic import BaseModel

class Module(BaseModel):
    title: str
    minutes: int

m = Module(title="Vectors", minutes=8)

pairs = [
    (".dict()",            "model_dump()"),
    (".json()",            "model_dump_json()"),
    (".parse_obj(d)",      "model_validate(d)"),
    (".parse_raw(s)",      "model_validate_json(s)"),
    (".schema()",          "model_json_schema()"),
    (".copy()",            "model_copy()"),
    (".construct()",       "model_construct()"),
    ("__fields__",         "model_fields"),
    ("__fields_set__",     "model_fields_set"),
]
for old, new in pairs:
    print("  %-18s ->  %s" % (old, new))

print()
print("still works :", m.model_dump())'''),

        ("Validators were renamed and reshaped",
         "<code>@validator</code> became <code>@field_validator</code>, and "
         "<code>@root_validator</code> became <code>@model_validator</code> with an "
         "explicit mode.",
         '''from pydantic import BaseModel, field_validator, model_validator

class Module(BaseModel):
    title: str
    minutes: int
    lessons: int

    # v1: @validator("title")
    @field_validator("title")
    @classmethod
    def tidy(cls, v: str) -> str:
        return v.strip().title()

    # v1: @root_validator  ->  now needs mode= explicitly
    @model_validator(mode="after")
    def fits(self):
        if self.lessons > self.minutes:
            raise ValueError("more lessons than minutes")
        return self

print(Module(title="  vectors ", minutes=30, lessons=5))

# v1 validators took (cls, v, values); v2 takes (cls, v, info) and
# reads earlier fields from info.data.'''),

        ("Config became model_config",
         "The inner <code>class Config</code> is the clearest signal that code or a "
         "tutorial predates v2.",
         '''from pydantic import BaseModel, ConfigDict

# v1:
#   class Module(BaseModel):
#       class Config:
#           extra = "forbid"
#           allow_mutation = False
#           orm_mode = True

class Module(BaseModel):
    model_config = ConfigDict(
        extra="forbid",          # same name
        frozen=True,             # was allow_mutation = False
        from_attributes=True,    # was orm_mode
    )
    title: str

m = Module(title="Vectors")
print(m)

try:
    m.title = "Norms"
except Exception as e:
    print("frozen:", type(e).__name__)'''),

        ("Optional no longer implies a default",
         "The behaviour change most likely to bite, because v1 filled the default in "
         "for you and v2 does not.",
         '''from typing import Optional
from pydantic import BaseModel, ValidationError

class Module(BaseModel):
    title: str
    summary: Optional[str]          # v1: optional. v2: REQUIRED, may be None.

try:
    Module(title="Vectors")
except ValidationError as e:
    print("v2 refuses:", e.errors()[0]["loc"], e.errors()[0]["type"])

print("explicit None works:", Module(title="Vectors", summary=None))

class Fixed(BaseModel):
    title: str
    summary: Optional[str] = None   # what v1 did implicitly

print("with a default     :", Fixed(title="Vectors"))'''),

        ("Constraint arguments were renamed",
         "<code>min_items</code>, <code>max_items</code> and <code>regex</code> are "
         "gone. The replacements are shorter and consistent across types.",
         '''from typing import List
from pydantic import BaseModel, Field, ValidationError

# v1: Field(min_items=1, max_items=4) and Field(regex=...)
class Module(BaseModel):
    slug: str = Field(pattern=r"^[a-z_]+$")       # was regex=
    lessons: List[str] = Field(min_length=1,      # was min_items=
                               max_length=4)      # was max_items=

print(Module(slug="dot_product", lessons=["a", "b"]))

for bad in [{"slug": "Dot Product", "lessons": ["a"]},
            {"slug": "ok", "lessons": []}]:
    try:
        Module.model_validate(bad)
    except ValidationError as e:
        print("%-38s %s" % (str(bad)[:36], e.errors()[0]["type"]))'''),

        ("Errors changed shape",
         "Error codes were renamed and <code>ctx</code>, <code>url</code> and stable "
         "types arrived. Code matching on v1 messages will silently stop working.",
         '''from pydantic import BaseModel, Field, ValidationError

class Module(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

try:
    Module(title="no", minutes=0)
except ValidationError as e:
    for err in e.errors():
        print("loc :", err["loc"])
        print("type:", err["type"], "  <- v1 called these 'value_error.any_str.min_length'")
        print("ctx :", err.get("ctx"))
        print()

print("Match on type, never on msg - that advice exists because of this.")'''),
    ],
    [
        "<code>.dict()</code> &rarr; <code>model_dump()</code>, <code>.json()</code> &rarr; <code>model_dump_json()</code>, <code>.parse_obj()</code> &rarr; <code>model_validate()</code>, <code>.schema()</code> &rarr; <code>model_json_schema()</code>.",
        "<code>@validator</code> &rarr; <code>@field_validator</code> (with <code>@classmethod</code>), <code>@root_validator</code> &rarr; <code>@model_validator(mode=...)</code>.",
        "<code>class Config</code> &rarr; <code>model_config = ConfigDict(...)</code>. <code>orm_mode</code> became <code>from_attributes</code>; <code>allow_mutation=False</code> became <code>frozen=True</code>.",
        "<strong>The one that does not raise a rename error:</strong> <code>Optional[X]</code> no longer defaults to <code>None</code>. It is now required-but-nullable unless you add <code>= None</code>.",
        "<code>min_items</code>/<code>max_items</code> became <code>min_length</code>/<code>max_length</code>; <code>regex</code> became <code>pattern</code>.",
        "Error <code>type</code> codes were renamed wholesale. Anything matching on v1 codes or on message text stops working silently.",
    ],
    '''
title: Migrating v1 to v2: What Changed and What Bites
intro: The renames, the action changes that fail silently, and how to date a tutorial.

## Why this module exists even if you never migrate

Pydantic version 2 was a rewrite. The core moved to Rust, and the API changed in places that matter. Code written for version 1 often fails on version 2, or worse, runs and behaves differently. Many projects still carry some version 1 habits.

Even if you never migrate anything, this article is worth reading. Older tutorials, answers and blog posts are written for version 1, and you will meet them. Knowing what changed lets you tell at a glance which advice still applies and which does not.

The article covers the changes in the order you are likely to hit them. First come the renames, where a familiar method now has a new name. Then come validators, which have a new decorator and a new signature. After that, Config, which is now a dictionary instead of an inner class. The last section covers the change that bites hardest, a shift in behaviour rather than in naming, where the same code gives a different answer. Each point comes with the old way and the new one, so you can translate code in either direction.

Think of it as a translation guide. You are unlikely to rewrite everything in one go, and you do not need to. Reading the changes in sequence makes each one easier to spot when it appears in an old snippet. It also helps you judge how much work a real upgrade would take, which is the question most teams ask first.

Each change is shown briefly and clearly.

Pydantic v1 was common for years. A great deal of writing about it's still the top result for many searches. Reading a v1 answer as though it shows v2 is a genuine source of confusion.

So the most handy thing here may simply be the ability to date a page.

**It's v1 if you see:** `@checker`, `@root_validator`, `.dict()`, `.json()`, `.parse_obj()`, `class Config`, `orm_mode`, `min_items`, `regex=`.

**It's v2 if you see:** `@field_validator`, `@model_validator`, `.model_dump()`, `model_config = ConfigDict(...)`, `from_attributes`, `min_length`, `pattern=`.

If a page uses the first set, treat all in it as historical. Not only the names. The action it shows.

## The renames

The rote part, and the easy part:

`.dict()` → `model_dump()`. `.json()` → `model_dump_json()`. `.parse_obj()` → `model_validate()`. `.parse_raw()` → `model_validate_json()`. `.schema()` → `model_json_schema()`. `.copy()` → `model_copy()`. `.make()` → `model_construct()`. `__fields__` → `model_fields`. `__fields_set__` → `model_fields_set`.

The `model_` prefix is deliberate: it namespaces the library's methods away from your field names. This Is also why Pydantic warns about fields starting with `model_`.

Most old names still exist in v2 and emit deprecation warnings. That is a kindness for migration and the reason so much code still uses them. Nothing forced the change.

## Validators

`@checker` became `@field_validator`, and it now needs `@classmethod` underneath.

The signature changed too. v1 took `(cls, v, values)` where `values` was a dict of before-checked fields. V2 takes `(cls, v, info)` and the same data is `info.data`.

`@root_validator` became `@model_validator`, and the mode is now clear. v1's `pre=True` is `mode="before"`. The default post-checker is `mode="after"` and receives the model rather than a dict of values, returning `self`.

That last change is more than cosmetic. A v1 root checker worked with a dict. A v2 after-checker works with the finished model. Fields are converted and field access works.

## Config

`class Config` became `model_config = ConfigDict(...)`, with a few settings renamed:

`orm_mode` → `from_attributes`. `allow_mutation = False` → `frozen=True`. `allow_population_by_field_name` → `populate_by_name`. `anystr_strip_whitespace` → `str_strip_whitespace`. `min_anystr_length` → `str_min_length`.

An inner `class Config` still works and warns. It's the single clearest signal that code hasn't been migrated.

## The change that bites

all above makes a warning or an error. This one doesn't:

```python
summary: Optional[str]
```

In v1 that was optional and defaulted to `None`. In v2 it's **needed** and nullable. You must pass it, and you may pass `None`.

Nothing warns, because the annotation is still valid. What happens is that code which used to work starts raising `missing` at runtime, in what code path first makes the model without that field.

The fix is one addition per field: `Optional[str] = None`.

The reason for the change is the one the defaults module gave. V1's silent default hid the gap between "may be omitted" and "may be null". This Are truly other contracts. v2 made you say which you meant.

If you're migrating anything large, search for `Optional[` first. It will be the largest single source of failures.

## Constraint renames

`min_items`/`max_items` → `min_length`/`max_length`, now steady with strings.

`regex` → `pattern`.

`allow_mutation` on a field → `frozen`.

`const=True` is gone. Use `Literal[value]`.

Some v1 helper types were removed or changed too. `constr(regex=...)` turns `Annotated[str, Field(pattern=...)]`. This Is the modern spelling anyway.

## Errors

Error `type` codes were renamed wholesale. v1's `value_error.any_str.min_length` is v2's `string_too_short`. v1's `type_error.int` is v2's `int_type` or `int_parsing` based on the cause.

`ctx` now carries the rule's params, and `url` links to docs for the type.

This is where the standing advice in this track. Match on `type`, never on `msg`. Comes from. Code that matched v1 message strings broke on upgrade with no warning at all. This Is just the failure mode that advice blocks.

If you're migrating, any error-handling code is worth reviewing right rather than trusting tests. A broken branch that never matches won't fail loudly.

## A practical order

If you're doing this on a real code:

**Install v2 and run the test suite.** Deprecation warnings tell you where the renames are, and they're rote.

**Search for `Optional[` and add the defaults.** Largest source of genuine failures, and invisible until ran.

**Rewrite checkers.** Add `@classmethod`, rename the decorators, change `values` to `info.data`. Make `mode` clear on root checkers.

**Convert `class Config` blocks**, renaming the settings that moved.

**Review error handling last**, because that is where the failures are silent.

There's a tool, `bump-pydantic`. This Does the rote parts on its own. It's worth running first and reviewing carefully. It handles the renames well and can't know your intent on the `Optional` question.

## What you get for it

The migration isn't free, and it's worth knowing what it buys.

check is much faster, because the core is Rust rather than Python. Strict mode exists. Discriminated unions became a first-class feature. `TypeAdapter` arrived. With it check without a wrapper model. Error output became structured and stable. `computed_field` exists. output gained real control.

Most of this track shows features that are v2-only. If you're reading it against a v1 code, that is the gap.

## Things that were removed outright

A few v1 features have no v2 equal, and finding them late is unpleasant.

`copy_on_model_validation` is gone. The action is controlled by `revalidate_instances` instead.

`GetterDict`, the customisation hook for `orm_mode`, was removed. `from_attributes` reads fields right. Anything more involved belongs in a `model_validator(mode="before")`.

`json_encoders` in Config is deprecated in favour of field and model serialisers. This Are more precise and appear in the right place.

`parse_file` is gone. Read the file yourself and use `model_validate_json` on the bytes. This Is better anyway. The errors name the spot in the doc.

`const=True` is gone. A `Literal` says the same thing and makes a better schema.

## Running both versions at once

For a large migration, `pydantic.v1` is on hand inside v2: `from pydantic.v1 import BaseModel` gives the old library alongside the new one.

That makes an incremental migration possible. Move one module at a time, with both versions installed as a single package.

Two cautions. The two aren't interoperable: a v1 model can't be a field of a v2 model. Mixing them at a boundary means converting through dicts. And a dependency that hasn't migrated may pull in its own expectations. Check what your libraries need before given you can take it slowly.

It's a transitional tool. Code left half-migrated for a year tends to stay that way. The two vocab lists side by side are truly confusing to read.

## Summary

Renames are rote and mostly warn. `Optional[X]` losing its silent `None` is the change that fails silently. Searching for it first will save the most time.

checkers changed shape and name. `@classmethod`, `info.data`, clear modes. Config moved into `model_config` with a few settings renamed. Error codes were replaced wholesale. Error-handling code deserves direct review rather than trust in tests.

`bump-pydantic` handles the rote parts. What it can't do is decide what you meant by `Optional`. This Is just the part that matters.


## Mistakes people make

**Trusting the test suite to find all.** Renames warn and errors are loud. Two groups fail quietly: `Optional` fields that are now needed. Error-handling branches matching v1 codes that simply never match again. Neither always fails a test.

**Running `bump-pydantic` and shipping.** It handles the rote renames well and can't know what you meant by `Optional[X]`. Review its output rather than treating it as a migration.

**Migrating models and not checkers.** A `@checker` still importable from `pydantic` in v2 is the deprecated shim. The signature changed. `values` became `info.data`. And a checker reading the wrong arg name won't behave as it did.

**Leaving `class Config` because it still works.** It warns rather than failing. It lives indefinitely. It's the single clearest marker of code that hasn't really been migrated.

**Living in `pydantic.v1` permanently.** The match import exists for a transition. Two vocab lists side by side in one code are truly confusing. Half-migrated code tends to stay that way.

**Reading v1 answers as v2.** The most common problem for people who never migrate anything. Check for `@checker`, `.dict()` and `class Config` before trusting a page. The action it shows has changed too, not only the spelling.

## Deciding whether to migrate

If you're on v1 and wondering whether it's worth it, the honest spot.

v1 is no longer developed and receives only security fixes. The ecosystem has moved: FastAPI, LangChain, SQLModel and most libraries that integrate with Pydantic now target v2. Staying on v1 increasingly means pinning things around it.

Against that, the migration is real work on a large code. It's work with no visible feature at the end of it.

The pragmatic answer for most teams is to migrate when a thing else forces the question. A dependency that needs v2, or a piece of work that touches the models anyway. Rather than as a standalone project. The `pydantic.v1` match import exists to make that gradual approach viable.

What isn't viable is starting new code on v1. all in this track past the first tier is v2, and the gap widens.

## Where this leaves the track

That is the last module. Thirty of them, from a type annotation that does nothing at runtime to an API whose docs writes itself.

The through-line has been one idea: **be exact at the boundary, once**. exact enough that the annotation says what you mean, that the constraint reaches the schema, that the error names the field. That all downstream can stop defending itself.

all else has been method. Coercion rules so text can arrive as text. checkers for the rules types can't hold. output so output is data rather than presentation. Schemas so other tools can read what you already wrote.

The version history matters here only because v2 is where most of that became true. If you're reading this against a v1 code, the gap isn't stylistic.

## A migration checklist

Condensed, in the order that finds problems soonest.

Install v2 and run the suite. Fix what fails loudly. Imports, removed args, renamed helpers.

Search `Optional[` and add `= None` wherever the field was meant to be omissible. Largest source of silent breakage.

Rewrite checkers: `@field_validator` with `@classmethod`, `@model_validator` with an clear mode, `values` turns `info.data`.

Convert `class Config` blocks, renaming `orm_mode`, `allow_mutation` and the `anystr_` family.

Rename constraint args: `min_items`, `max_items`, `regex`.

Review error handling by hand. Anything matching v1 type codes or message text has stopped matching, silently, and tests may not notice.

Then drop the deprecated method names once the warnings are the only thing left.

## If you are only reading, not migrating

The most common use of this module isn't migration at all. It's dating an answer you found while looking for a thing else.

That skill is worth more than it sounds. A confident, well-written, highly-ranked answer showing v1 action will send you in the wrong direction for an afternoon. Nothing about it announces its age.

The tell is the vocab. `@checker`, `.dict()`, `class Config`, `orm_mode`, `min_items`, `regex=`. Any one of those means the page predates v2. The action it shows may have changed and the spelling. `Optional` being the sharpest example. The code will look correct and simply not work.
''',
    [
        {"q": "In v2, what does `summary: Optional[str]` with no default mean?",
         "options": ["Optional, defaults to None as in v1", "Required, and may be None", "Forbidden", "It warns"],
         "answer": 1,
         "why": "v1 added the default implicitly; v2 does not. Nothing warns, so code that worked starts raising `missing` at runtime - the largest source of failures in a real migration."},
        {"q": "What replaced `@root_validator`?",
         "options": ["@field_validator", "@model_validator with an explicit mode", "@validator", "Nothing"],
         "answer": 1,
         "why": "The mode is now explicit, and an after-validator receives the finished model as `self` rather than a dict of values - so fields are already converted."},
        {"q": "Which of these dates a tutorial as v1?",
         "options": ["model_config", "class Config and .dict()", "field_validator", "TypeAdapter"],
         "answer": 1,
         "why": "An inner `class Config`, `.dict()`, `@validator`, `orm_mode` and `min_items` are all v1 vocabulary. Treat the behaviour such a page describes as historical too."},
        {"q": "Why review error-handling code carefully during a migration?",
         "options": ["It is slower in v2", "Error type codes were renamed wholesale, and a branch that never matches fails silently", "Errors were removed", "It is unchanged"],
         "answer": 1,
         "why": "Code matching v1 codes or message strings stops matching with no exception raised. This is precisely why the advice throughout is to match on `type` rather than `msg`."},
    ],
)
