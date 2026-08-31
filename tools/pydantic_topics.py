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

Write a function like this and you have made a promise:

```python
def modules_left(count: int) -> str:
    return "You have " + str(count) + " modules to go"
```

The promise is that `count` is a whole number. Python does not keep it. Annotations are stored on the function object and otherwise ignored at runtime &mdash; they exist for human readers, editors and type checkers like mypy, none of which are present when your program is actually running. Call `modules_left("twelve")` and Python does exactly what you asked: it concatenates strings and returns a sentence that reads fine.

That is a small problem when the wrong value is only printed. It becomes a real one the moment something arithmetic happens. A string that has been travelling through three function calls disguised as an integer fails at the point it is finally divided, and the traceback points at the division, not at the front door where the bad value walked in.

This is the gap Pydantic fills. It reads the annotations you already write and enforces them, at a moment you choose.

## Validation is a boundary problem

Almost no bad data originates inside your program. It arrives: from a JSON request body, a form post, a config file, a CSV, a database column that has been nullable since 2019, an environment variable, another team's API. Everything that crosses into your code from outside is, until proven otherwise, a guess.

The useful discipline is to check that data once, at the edge, and convert it into something trustworthy. After that line, every function downstream can assume the shape is right and stop defending itself. The alternative &mdash; an `isinstance` check at the top of every function, or worse, no check and a hope &mdash; spreads the same anxiety through the whole codebase.

A Pydantic model is that boundary written down. It is a class whose annotations describe what you require, and constructing one is the act of checking.

```python
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    minutes: int
    published: bool
```

Three lines, and you now have something that will refuse to exist unless the data fits.

## Coercion: the part people do not expect

The first surprise for most people is that Pydantic does not merely check &mdash; it converts. Hand the model above `minutes="9"` and you get back an integer `9`, not an error.

That is deliberate, and it follows from where models are used. Data crossing a boundary is usually text. A query string has no integers in it. An HTML form sends strings. A CSV is strings all the way down. If a model rejected everything that arrived as text, you would spend your life writing `int(request.args["minutes"])` and catching `ValueError` by hand &mdash; which is precisely the code Pydantic exists to delete.

So the default behaviour, called **lax mode**, is to accept anything that has an unambiguous reading. `"9"` becomes `9`. `9.0` becomes `9`. `"true"`, `"yes"` and `1` all become `True`. But `"nine"` does not become anything, because there is no unambiguous reading, and neither does `9.5`, because turning it into `9` would silently lose information you might have needed.

Where that trade is wrong &mdash; and sometimes it is, particularly deep inside a system where types should already be correct &mdash; strict mode is available, and gets a module of its own later in this track.

## Errors that are worth reading

The second thing that distinguishes Pydantic from a hand-written check is the quality of its refusals.

A hand-written validator usually raises on the first problem it meets. The caller fixes that one, resubmits, and discovers the next. Pydantic checks every field and raises once, carrying the complete list. For a form, that is the difference between one error message at a time and a form that highlights all four broken inputs at once.

Each entry in that list has three parts worth reading separately.

The **location** is a path, not a name. For a flat model it is just the field. For anything nested it describes the route: `address.pin` is one level down, `modules.2.minutes` is the `minutes` field of the third item in a list. When a payload is deep, this is the fastest way to find the offending value.

The **type** is a stable machine-readable code &mdash; `int_parsing`, `string_too_short`, `greater_than` &mdash; not a sentence. It is what you match on if you are converting errors into an API response or a translated message, and it will not change underneath you when the wording is improved.

The **input** is the value that was actually received. Nine times in ten, seeing it is the whole diagnosis: you expected a number and the caller sent `"null"` as a string.

## What else the model buys you

Once the shape of your data is written down precisely enough to validate against, it is written down precisely enough for other things too.

`model_dump()` gives you a plain dictionary. `model_dump_json()` gives you a JSON string, handling the types &mdash; dates, UUIDs, decimals &mdash; that `json.dumps` refuses. And `model_json_schema()` produces a JSON Schema document describing the model.

That last one is quietly the reason Pydantic is everywhere. FastAPI does not have its own validation layer; it uses Pydantic, and it turns those generated schemas into the interactive documentation you get for free at `/docs`. The same mechanism drives structured output in LLM libraries, where the schema tells the model what shape to answer in. You describe your data once, and several tools read that description.

## What it is not

Pydantic is not an ORM, though it is often paired with one. It does not talk to your database, and a model is not a table.

It is not a static type checker either. Mypy analyses code without running it; Pydantic checks values while the program runs. They complement each other rather than compete, and using both is normal.

And it is not free. Validation costs something, which is exactly why the boundary discipline matters: validate on the way in, once, and then trust the result rather than re-checking the same object at every layer.

## What the hand-written version looks like

It is worth seeing the code Pydantic replaces, because the comparison explains several of its design decisions at once.

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

Fifteen lines for two fields, and it is already worse than it looks. It stops at the first error, so a caller with two mistakes discovers them one at a time. Its messages do not say which field failed in a machine-readable way. It has no idea what to do about a third field when somebody adds one, and nothing forces that person to remember this function exists. And it describes the same shape a second time, in prose, in whatever documentation exists.

The Pydantic version is the class definition and nothing else. Every one of those problems is solved as a side effect rather than as an additional feature.

## The cost, and when it matters

Validation is not free, and it is worth being concrete rather than reassuring.

Building a model does real work: reading a compiled schema, checking each field, converting where needed, and constructing the object. A plain class assignment does none of that. If you construct millions of objects in a tight loop, you will measure the difference.

Two things make it matter less than people fear. The first is that Pydantic v2 does the work in Rust rather than Python, which moved it from "noticeable" to "usually irrelevant". The second is scale: a model that validates in single-digit microseconds sits next to a database query taking milliseconds and a network call taking hundreds of milliseconds. In a typical request handler, validation is a rounding error on the request.

Where it genuinely matters is bulk. Validating a hundred thousand rows from a file, or every element of a large array in a numerical pipeline, is a case where you should measure. The answer there is usually not to abandon models but to validate the container once rather than each item through a Python loop, which is a topic the `TypeAdapter` module returns to.

The rule that follows is the one this article opened with: validate at the boundary, once. Re-validating an object that has already passed is pure cost with no information gained.

## Where it came from, and why v2 matters

Pydantic v1 was pure Python. It was popular enough to become a dependency of a large part of the ecosystem, and slow enough that its performance was a recurring complaint.

Version 2, released in 2023, kept the API broadly recognisable and rewrote the engine in Rust as a separate package called `pydantic-core`. When you install `pydantic` you get both: a Python layer that reads your annotations and builds a schema, and a compiled core that executes that schema against data.

This split explains several things you will notice. It is why validation is fast. It is why the error `type` codes look like machine identifiers rather than sentences &mdash; they come from the core. It is why `model_validate_json` beats `json.loads` plus validation, since the core parses and validates in one pass without building intermediate Python objects. And it is why a wheel exists for every platform: there is compiled code in there.

The practical consequence for you is about documentation. A great deal of Pydantic material online predates v2 and describes an API that has moved. The reliable signals: v1 uses `@validator`, `.dict()`, `.json()` and `class Config`; v2 uses `@field_validator`, `.model_dump()`, `.model_dump_json()` and `model_config`. If an article uses the first set, treat everything in it as historical.

## Four things people expect it to be

**An ORM.** It is not, and it does not talk to a database. It pairs well with one &mdash; SQLModel exists precisely to join them &mdash; but a model is not a table and validating one does not persist anything.

**A static type checker.** Also no. Mypy and Pyright analyse code without running it and catch mistakes in your own source. Pydantic checks values at runtime and catches mistakes in data. They overlap in vocabulary and not in job, and a serious codebase uses both.

**A serialisation format.** `model_dump_json` produces JSON, but Pydantic is not competing with `json` or `msgpack`. It describes and checks the shape; the encoding is a service it offers on top.

**Automatic.** Nothing validates until you ask. A function annotated with a model type does not check its argument; only constructing or validating a model does. There is a `@validate_call` decorator that brings the same checking to function arguments, and it is opt-in for the same reason.

## The habit worth forming

When you find yourself writing `if not isinstance(...)`, or reaching into a dictionary with `.get()` and a default, or writing a comment that explains what shape a parameter is meant to have &mdash; that is a model waiting to be written.

The comment in particular is the strongest signal. A sentence describing the shape of data is a schema that cannot be executed, checked or kept honest. Turning it into a model costs about the same number of lines and cannot go stale.

## Where this track goes

The next module builds a first model properly &mdash; fields, required versus optional, and what you get back. After that comes the part everyone trips over: precisely which values Pydantic will convert and which it will refuse, and how to read the error when it refuses.

The fastest way through all of it is to keep changing the values in the editors above and pressing Run. A rule you have watched break is a rule you remember.
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

A Pydantic model is a class that inherits from `BaseModel` and lists its fields as annotations.

```python
from pydantic import BaseModel

class Module(BaseModel):
    title: str
    track: str
    minutes: int
```

That is the entire definition. There is no `__init__`, no assignment of `self.title = title`, no validation code. Pydantic reads the annotations when the class is created and builds the machinery from them &mdash; a constructor, a validator, a serialiser, an equality method and a readable `repr`.

The economy matters more than it first appears. Adding a field is one line. In the hand-written equivalent it is four: the parameter, the assignment, the check, and the line in `to_dict`. Those four drift apart over time, and the drift is where bugs live.

## Creating one

Models take keyword arguments:

```python
m = Module(title="Dot Product", track="maths", minutes=11)
```

Positional arguments are refused, and the refusal is deliberate rather than an oversight. Models grow. A field added in the middle of a class body would silently change what every positional call meant, and nothing would raise &mdash; the values would simply land in the wrong slots. Requiring names makes that class of bug impossible.

When the data is already a dictionary, which it usually is if it came from JSON, there are two ways in:

```python
Module(**data)
Module.model_validate(data)
```

They do the same work. `model_validate` reads better in a pipeline, makes it obvious that validation is happening, and does not break if the dictionary happens to contain a key that is not a valid Python identifier.

## What you get back

An ordinary object. Attribute access works, methods you define work, and the values have the types the annotations promised:

```python
m.title          # "Dot Product"
m.minutes + 1    # 12  - a real int, not a string
```

That last line is the payoff. Downstream code does not need to check or convert anything, because the conversion already happened at the door.

Models are not dictionaries. `m["title"]` raises, and asking for a field that does not exist raises `AttributeError` like any other object. This is a feature: a typo in a dictionary key returns `None` or a `KeyError` deep inside a function, whereas a typo in an attribute name is caught immediately and is visible to your editor's autocomplete.

## Methods and behaviour

Because a model is a class, you can give it methods:

```python
class Module(BaseModel):
    title: str
    minutes: int

    def slug(self) -> str:
        return self.title.lower().replace(" ", "_")
```

This is worth doing. Logic that depends only on a model's own fields belongs on the model, where it is discoverable and testable, rather than in a loose function three modules away.

Later in this track you will meet `@computed_field`, which is the version of this that also appears in the serialised output.

## Getting the data out

Two methods, and the difference between them is worth getting right early.

`model_dump()` returns a dictionary of Python objects. A `datetime` field comes back as a `datetime`, a `Decimal` as a `Decimal`. Use it when the data is staying inside your program &mdash; passing to another function, feeding a template, comparing in a test.

`model_dump_json()` returns a JSON string, converting everything into something JSON can represent. Use it when the data is leaving: an HTTP response, a message queue, a file on disk. It handles the types that plain `json.dumps` refuses outright, which is a small mercy you will appreciate the first time a `datetime` appears in a payload.

Both take arguments that shape the output &mdash; `include`, `exclude`, `exclude_none`, `by_alias` &mdash; and those get a module of their own in the serialisation tier.

If you have read older tutorials you will have seen `.dict()` and `.json()`. Those are the Pydantic v1 names. They still work in v2 but emit deprecation warnings, and a great deal of writing on the internet has not caught up.

## The round trip

Put the two directions together and you have the shape of most web services:

```python
wire = original.model_dump_json()          # going out
received = Module.model_validate_json(wire) # coming back in
original == received                        # True
```

That equality is worth noticing. Models compare by value, not identity, so two separately constructed models with the same contents are equal. In tests this turns a page of field-by-field assertions into one line.

`model_validate_json` is also the right way to accept JSON. It is tempting to write `json.loads` followed by `model_validate`, and it works, but parsing inside Pydantic's Rust core is faster and the errors it produces know where in the document the problem was.

## Two models of the same thing

A pattern that arrives quickly in real work: the same subject needs different shapes in different places. A list endpoint returns a title and a duration; a detail endpoint returns everything; a create endpoint accepts everything except the id, which the server assigns.

The instinct is to build one model with a lot of optional fields. Resist it. Optional-everything means the model no longer documents anything &mdash; every field might be missing, so no reader can tell what is actually guaranteed.

Separate models say what they mean. `ModuleSummary` has two required fields and is honest about it. Converting between them is one line, because a dump from one is valid input to the other whenever the fields line up.

## Field order, and why it exists

Fields have an order &mdash; the order you wrote them &mdash; and although you cannot pass them positionally, the order is not cosmetic.

It determines the order of keys in `model_dump()` and in the generated JSON, which matters when a human reads the output or when something downstream diffs two payloads. It determines the order fields appear in the generated schema, and therefore in API documentation. And it determines validation order, which becomes significant once you write validators that look at previously-validated fields.

The practical advice is to order fields the way you would explain them: identity first, then the important attributes, then the optional extras. It costs nothing and every reader of the output benefits.

## Looking at the model itself

A model knows about its own fields, and that introspection is available to you:

```python
Module.model_fields          # {'title': FieldInfo(...), 'minutes': FieldInfo(...)}
list(Module.model_fields)    # ['title', 'minutes']
```

Each `FieldInfo` carries the annotation, whether the field is required, the default if there is one, and any metadata such as a description. This is what the schema generator reads, and it is available to you for the same kind of work &mdash; building a form, generating a table header, checking that every field has a description before you ship.

`model_fields` is defined on the class, not the instance, so you can inspect a model without having any data for it.

## Copying and changing

Models are ordinary objects and you can assign to their attributes, but that is often not what you want &mdash; particularly if something else is holding a reference to the same object.

`model_copy` makes a new one:

```python
original = Module(title="Vectors", track="maths", minutes=8)
longer = original.model_copy(update={"minutes": 12})
```

Two things to know about it. The copy is shallow by default, so a nested model or a list is shared between the two objects; pass `deep=True` when that matters. And `update` does **not** validate the new values &mdash; it writes them in directly. If the values came from anywhere untrusted, build a new model instead of copying with an update.

## Making a model immutable

By default a model's attributes can be reassigned, and by default that reassignment is not validated:

```python
m.minutes = "not a number"    # allowed, and now the field is a string
```

Two settings fix two different halves of that. `validate_assignment=True` runs validation on assignment, so the line above raises. `frozen=True` forbids assignment entirely and makes the model hashable, so it can be a dictionary key or a set member.

```python
class Module(BaseModel):
    model_config = ConfigDict(frozen=True)
    title: str
```

Frozen models are worth reaching for more often than people do. A value that arrives from outside, is validated once and then read many times has no business being mutable, and freezing it removes a whole class of "who changed this?" question.

## Inheritance

Models inherit, and it works the way you would hope: subclass fields are added to the parent's, and the parent's validators still run.

```python
class ModuleBase(BaseModel):
    title: str
    minutes: int

class ModuleInDB(ModuleBase):
    id: int
    created_by: str
```

This is the standard way to express the family of shapes one concept needs &mdash; a base with the common fields, then `Create`, `Update` and `InDB` variants that add or relax what they must. It keeps the shared fields in one place, so a change to the base reaches all of them.

Be careful with one thing: a subclass cannot make an inherited required field optional in a way that reads clearly. Redeclaring `title: str = "untitled"` works, but a reader now has to check two classes to know what `title` does. If the variants differ a lot, separate models are kinder than deep inheritance.

## What `repr` gives you

Printing a model prints its fields, which is more useful than the default `<Module object at 0x...>` and is one of the small things that makes models pleasant in a REPL or a log line.

You can keep a field out of that output with `Field(repr=False)` &mdash; the obvious use being anything secret. A password hash or an API token in a model that gets logged is a genuine incident waiting to happen, and `repr=False` is the one-word fix.

Note that it only affects the representation. The value is still in `model_dump()`, so a field that must never leave the process needs `exclude=True` as well, or a separate output model that simply does not have it.

## Two mistakes worth avoiding early

**Treating a model like a dictionary.** Models do not support `m["title"]`, and the instinct to reach for it usually signals code that is passing models where it should be passing dicts, or the reverse. Decide which side of the boundary a function is on: if it takes untrusted data, it takes a dict and validates it; if it takes validated data, it takes a model and uses attributes.

**Putting expensive work in a model.** A model is constructed every time data arrives, and anything in a validator runs on that path. A network call, a database lookup or a file read inside a model turns validation into I/O, makes the model impossible to test without mocking, and turns a `ValidationError` into a timeout. Keep models pure: they check the shape of data using only the data. Rules that need to consult the world belong in the layer that owns the world.

## A working shape to copy

Putting the module together, the following is close to what a real model looks like once it has been through a couple of rounds of use:

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

Frozen, because it arrives from outside and is then only read. Two required fields, because a module without a title or a track is not a module. Two defaults with obvious values. One method, because the slug is derived from the title and belongs next to it.

Nothing exotic, and it already gives you validation, coercion, equality, a readable `repr`, JSON in both directions and a schema. That ratio &mdash; how much you get for how little you wrote &mdash; is the reason the library is worth learning properly rather than copying from examples.

## What to try next

Change something in the editors above and watch what happens. Add a field to a model and leave it out of the constructor call. Pass `minutes` as `"11"` and print its type. Remove a field from the JSON before validating it back.

The next module is precisely about those conversions: which values Pydantic will quietly accept and turn into the type you asked for, and which it will refuse.
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
intro: The rules behind the library's most surprising behaviour, one value at a time.

## Why it converts at all

The first time someone sees `minutes="9"` become `9` they usually ask whether that is safe. It is a fair question, and the answer is in where models get used.

Data arriving from outside a program is nearly always text. A query string is text. An HTML form submission is text. A CSV is text. An environment variable is text. If a model refused everything that was not already the right Python type, the code in front of every model would be a pile of `int(...)` calls wrapped in `try`, which is exactly the code the library exists to remove.

So the default &mdash; **lax mode** &mdash; is to accept any value with one unambiguous reading, and refuse the rest. The rules are worth knowing precisely, because "unambiguous" turns out to be a stricter test than most people expect.

## Into int

A string converts if it reads as a whole number, surrounding whitespace included: `"9"` and `"  9  "` both give `9`.

A float converts only if nothing is lost. `9.0` becomes `9`. **`9.5` raises.** This is the rule people are most often surprised by, and it is the right one: rounding silently is how a total ends up being a penny out and nobody can find why. If you want rounding, ask for it explicitly.

`True` becomes `1`, because `bool` is a subclass of `int` in Python and always has been.

Everything else refuses: `"nine"`, `None`, a list, a dict. There is no reading of `"nine"` that is unambiguous without inventing a natural-language parser.

## Into float

More permissive, because floats can represent more. Integers widen (`9` gives `9.0`). Strings that read as numbers convert, and scientific notation like `"1e3"` works. `True` gives `1.0`.

Note that this is one place where information genuinely can be lost &mdash; a very large integer will not survive a trip through a float exactly &mdash; but that is a property of floating point rather than of Pydantic.

## Into str, and the asymmetry

Here is the rule that catches people: **a number does not become a string.** A field annotated `str` given `9` raises.

That seems inconsistent until you think about which direction the mistake usually runs. Text arriving where a number was wanted is normal &mdash; it is what the wire looks like. A number arriving where text was wanted is usually a genuine mistake in the calling code, and converting it would bury that mistake. The asymmetry is doing useful work.

If you actually want numbers accepted as text, say so with a validator that runs before conversion. There is a module on those later.

## Into bool

Booleans have their own table, and it is not Python's.

`True` comes from `True`, `1`, `1.0`, and the strings `"1"`, `"true"`, `"True"`, `"yes"`, `"on"`, `"t"`, `"y"`. `False` comes from `False`, `0`, `0.0`, and the strings `"0"`, `"false"`, `"no"`, `"off"`, `"f"`, `"n"`. Anything else &mdash; `"maybe"`, `2`, `""`, `None` &mdash; raises.

Compare that with plain Python, where `bool("false")` is `True` because the string is non-empty. Pydantic reads the *meaning* of the word rather than the emptiness of the container, which is almost always what you wanted when the value came from a checkbox or a query parameter. It is also why `?published=false` does the right thing without you writing a special case.

## Unions and order

A `Union[int, str]` has to decide which member to try. Pydantic v2 uses **smart mode**: it first looks for a member the value already matches exactly, and only then tries conversion, left to right.

That resolves the common cases sensibly &mdash; an actual `int` stays an `int`, an unconvertible string stays a string &mdash; but it does not remove ambiguity entirely. A string like `"9"` can satisfy both members, and which one wins depends on the order you wrote.

Where the distinction matters, do not lean on order. Say what you mean: a discriminated union picks a member by an explicit tag field, and strict mode removes conversion from the question. Both have modules later in this track.

## Turning it off

Coercion is right at the boundary and often wrong inside. Once data has been validated at the door, a value arriving as the wrong type deeper in the system is a bug in your own code, and quietly fixing it hides the bug.

Strict mode makes conversion an error:

```python
class Strict(BaseModel):
    model_config = ConfigDict(strict=True)
    minutes: int
```

`Strict(minutes="9")` now raises; `Strict(minutes=9)` is fine. Strictness can also be set on a single field, which is the more common need &mdash; lax about most things, exact about the one that matters.

There is a module on strict mode in the next tier that covers when the trade is worth making.

## Reading the type codes

Every refusal carries a stable `type` code, and they are worth recognising because they say precisely which rule fired:

`int_parsing` means a string did not read as an integer. `int_from_float` means a float had a fractional part. `string_type` means a non-string reached a `str` field. `bool_parsing` means a string was not in the boolean table. Matching on these is more reliable than matching on the message, which is prose and may be reworded.

## Dates, times and the other standard types

Pydantic knows the common standard-library types, and the conversions are the ones you would want.

A `datetime` field accepts a `datetime`, an ISO 8601 string such as `"2026-08-26T14:30:00"`, and a Unix timestamp as an integer or float. A `date` accepts `"2026-08-26"`. A `time` accepts `"14:30:00"`. A `timedelta` accepts a number of seconds or an ISO 8601 duration.

`UUID` accepts a `UUID` or its string form. `Decimal` accepts a string, an int or a float &mdash; and for money you want the string, because `Decimal(0.1)` inherits the float's inaccuracy while `Decimal("0.1")` does not. `Path` accepts a string. `Enum` accepts the member or its value.

The pattern is consistent: the type itself always works, and the obvious textual representation works. That is what makes models useful directly against JSON, where none of these types exist natively.

Timezones deserve a warning. A naive `datetime` string produces a naive `datetime`, and comparing one of those to an aware one raises. If your application is timezone-aware, say so in the type with `AwareDatetime`, and the model will reject naive input rather than letting it through to fail later.

## What a collection will accept

Container types coerce their contents, item by item.

`List[int]` given `["1", "2", "3"]` gives `[1, 2, 3]` &mdash; each element goes through the same rules described above. If one element fails, only that element fails, and the error's `loc` names its index.

There is a shape rule as well as a content rule. A `List[int]` accepts a list, and in lax mode also a tuple, a set or a generator, because all of those are sequences of items. It does **not** accept a bare string, even though a string is technically iterable. That exception is deliberate and it is a mercy: `List[str]` given `"abc"` producing `["a", "b", "c"]` would be a memorably bad afternoon.

`Dict[str, int]` coerces keys and values independently. `Set[int]` deduplicates, which means a set field can quietly return fewer items than were sent &mdash; usually what you want, occasionally a surprise.

`Tuple[int, str]` is checked positionally and by length: exactly two items, first an int, second a string. `Tuple[int, ...]` means any number of ints.

## None is not a wildcard

A common early mistake is expecting `None` to be accepted wherever a value is missing. It is not. `None` is a value like any other, and it is accepted only where the type allows it &mdash; which means `Optional[X]`, or `X | None`.

A field annotated `int` given `None` raises, with the type `int_type`. This is right: "no value" and "the number zero" are different facts, and a library that quietly turned one into the other would be hiding information.

If you want missing to mean something specific, say it with a default: `minutes: int = 0` accepts an absent field and gives you a zero, while still refusing an explicit `None`.

## JSON mode is stricter than Python mode

There are two validation modes, and they differ in ways that occasionally matter.

`model_validate` takes Python objects. `model_validate_json` takes a JSON string and parses it in the Rust core.

The distinction shows up because JSON has fewer types than Python. A JSON document has no `datetime`, so a `datetime` field validated from JSON must accept a string &mdash; and it does. But in Python mode, some conversions that would be ambiguous in JSON are allowed because the input type already disambiguates them.

For everyday models the two behave the same and you can ignore the difference. It becomes relevant with custom serialisers and with `Decimal`, where the JSON parser can preserve a number's exact textual form in a way that a Python float has already lost. When precision matters, validating from JSON directly is not just faster &mdash; it is more faithful.

## The rules on one page

Worth committing to memory, because most surprises are one of these:

**To `int`:** whole-number strings yes, whitespace ignored; floats only when exact; `True` gives `1`; anything else raises.

**To `float`:** ints yes, numeric strings yes, scientific notation yes.

**To `str`:** other strings only. Numbers, booleans and `None` all raise.

**To `bool`:** a fixed vocabulary of words and `0`/`1`; everything else raises, including `2`.

**To a container:** the items are coerced individually; a string is never treated as a sequence of characters.

**`None`:** allowed only where the annotation says so.

**Everywhere:** conversion never loses information silently. Where it would, it raises instead.

That last line is the principle the whole table is generated from. If you remember one thing, remember that, and you can usually predict the rest.

## Debugging a conversion you did not expect

When a field comes out as something surprising, there is a quick sequence that finds the cause almost every time.

**Print the type, not the value.** `print(type(m.minutes).__name__, m.minutes)` distinguishes `9` the integer from `9` the string, which `print(m.minutes)` does not.

**Look at the error's `input`.** If it raised, the report shows what actually arrived. It is frequently not what the caller believed they sent &mdash; `"null"` as a four-character string, a number wrapped in a list, an empty string where a missing field was intended.

**Check for a `Union`.** Unexpected types nearly always come from a union member being chosen that you did not have in mind. `Union[int, str]` will hand you a string sometimes and an integer other times, and both are correct behaviour for the annotation you wrote.

**Try it in strict mode.** Temporarily setting `strict=True` turns every silent conversion into an error that names the field. It is the fastest way to find out which conversions a model is actually performing, and you can turn it off again afterwards.

## What to take away

Coercion is the feature people distrust first and rely on most. It exists because the boundary is made of text, and it is bounded by a single principle: convert when the reading is unambiguous and nothing is lost, refuse otherwise.

Once that principle is in your head, the individual rules stop needing to be memorised. `9.5` to an int loses information, so it raises. `"9"` to an int loses nothing, so it converts. `9` to a string loses nothing either, but that direction hides caller mistakes, so it is the one deliberate exception &mdash; and knowing it is an exception is easier than remembering it as an arbitrary rule.

## The practical shape

Run the last editor above and look at what happened. A dictionary of four strings &mdash; exactly what a browser sends &mdash; became a model with a string, an int, a float and a bool, each usable in arithmetic without a single conversion call in sight.

That is the whole value proposition. You wrote the types once, in the annotations, and the messy part happened at the boundary where it belongs.

The next module deals with the fields that are not always there: optional values, defaults, and the difference between "missing" and "null" that trips up nearly everyone.
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
intro: Why Optional does not mean optional, and how to tell "not sent" from "sent as null".

## The rule, first

A field is required when it has no default value. That is the entire rule, and the type annotation plays no part in it.

```python
class Module(BaseModel):
    title: str        # required
    minutes: int = 10 # optional, defaults to 10
```

Leave out `title` and the model refuses to be built, with an error whose `type` is `missing`. Leave out `minutes` and you get `10`.

Everything confusing about this topic comes from one word being borrowed for two jobs.

## Optional does not mean optional

`Optional[str]` comes from the `typing` module, where it means exactly one thing: `str or None`. It is a statement about which *values* are allowed. It says nothing whatsoever about whether the field has to be supplied.

```python
class Strict(BaseModel):
    note: Optional[str]        # nullable, and STILL REQUIRED
```

`Strict(note=None)` works. `Strict()` raises `missing`. This surprises nearly everyone once, and the surprise is entirely the fault of English rather than of Pydantic &mdash; `Optional` was named for type theory, not for form fields.

To get the behaviour people usually mean, add the default:

```python
class Truly(BaseModel):
    note: Optional[str] = None   # nullable AND optional
```

It is worth internalising as two separate questions. *Can this value be null?* is answered by the type. *Must the caller provide it?* is answered by whether there is a default. They are independent, and all four combinations are legitimate and occasionally useful.

Pydantic v1 blurred this: it made `Optional` fields default to `None` automatically. Pydantic v2 stopped, precisely because the implicit default hid the distinction. If you find old code that relies on it, this is one of the changes that will bite during a migration.

## Missing and null are different facts

For most models the difference does not matter. For anything that updates existing data, it matters enormously.

Consider a PATCH endpoint. A client sends `{"title": "New Name"}`. What should happen to `summary`? Obviously nothing &mdash; they did not mention it. Now a client sends `{"summary": null}`. What should happen? Just as obviously, `summary` should be cleared. Those are opposite intentions, and after validation both fields are `None` in the model.

`model_fields_set` recovers the distinction. It is a set of the field names the caller actually supplied:

```python
Update(title="x").model_fields_set   # {"title"}
Update().model_fields_set            # set()
```

And `model_dump(exclude_unset=True)` uses it, returning only the fields that were provided. That output is the correct thing to apply to an existing record: absent keys are absent, and an explicit `None` is present and clears the value.

Getting this wrong is a real and common bug. An update endpoint that dumps the whole model and writes every field will happily overwrite six columns with `None` because the client only mentioned one.

## The mutable default trap, and why it is not one here

Every Python programmer eventually learns this the hard way:

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```

The list is created once, when the function is defined, and shared by every call that does not pass one. The second call sees the first call's data.

Pydantic does not have this bug. A default like `tags: List[str] = []` is deep-copied for each new instance, so two models never share a list. You can write the natural thing and it is safe.

`default_factory` still matters, though, for defaults that must be *computed* rather than copied. A timestamp, a generated id, a counter &mdash; anything whose value should reflect the moment of creation:

```python
created: datetime = Field(default_factory=datetime.now)
```

Written as `= datetime.now()` that would freeze the time the class was defined, and every model would claim to have been created at import.

## Defaults are not checked

This one is quiet and occasionally costly. By default, Pydantic does not validate default values:

```python
class Sloppy(BaseModel):
    minutes: int = "not a number"
```

That class definition raises nothing, and `Sloppy().minutes` is the string. The reasoning is speed &mdash; you wrote the default yourself, so checking it on every instantiation is work with no expected payoff.

The cost is that a mistyped default is invisible until something downstream does arithmetic. If you would rather be told, `model_config = ConfigDict(validate_default=True)` turns the checking on, at a small cost per instance.

For a model with hand-written defaults that never change, the default behaviour is fine. For a model whose defaults come from configuration or a constant defined elsewhere, turning validation on is cheap insurance.

## Choosing well

A few habits that keep models honest.

Prefer required fields. Every default is a decision made on behalf of a caller who did not make it, and a model where everything is optional documents nothing &mdash; a reader cannot tell what is actually guaranteed.

Do not use `None` as a stand-in for a real default. If a missing duration means ten minutes, write `minutes: int = 10`, not `Optional[int] = None` with a `or 10` scattered through the code that follows.

Reserve `None` for values that are genuinely absent in the domain: a summary nobody has written yet, an end date for something still running. Then `None` carries meaning rather than marking a gap in the model.

And when you are modelling an update rather than a creation, reach for `exclude_unset` early. It is easier to build the endpoint correctly than to work out later why six columns went blank.

## The ellipsis, and other spellings of "required"

You will meet `Field(...)` in older code and in a lot of documentation:

```python
title: str = Field(..., min_length=3)
```

The literal `Ellipsis` was Pydantic v1's way of saying "there is no default, this is required", because `Field` needed something in the default position. It still works in v2, and it is redundant: omitting the default says the same thing.

```python
title: str = Field(min_length=3)     # identical, and clearer
```

Prefer the second. The first makes readers who have not met the convention stop and look it up, and it buys nothing.

## Defaults that depend on the environment

A default does not have to be a literal. `default_factory` takes any callable, which means a default can come from configuration, the clock, or a generator:

```python
created: datetime = Field(default_factory=datetime.now)
request_id: str = Field(default_factory=lambda: uuid4().hex)
retries: int = Field(default_factory=lambda: int(os.getenv("RETRIES", "3")))
```

The third one is worth a caution. Reading configuration inside a default factory works, but it happens at model-construction time rather than at import, which makes it harder to reason about and hard to override in tests. For anything that is really configuration, a settings model is the better home &mdash; that is a module in the last tier.

There is also a form of `default_factory` that receives the already-validated data, letting a default depend on other fields. It is powerful and easy to overuse; a value computed from other fields is often better expressed as a `computed_field`, which does not pretend to be an input.

## How this appears in the schema

The distinction between required, optional and nullable is not just a Python concern &mdash; it shows up in the generated JSON Schema, and therefore in your API documentation and any client generated from it.

A field with no default appears in the schema's `required` array. A field with a default does not, and its default is recorded. A nullable field's type becomes an `anyOf` including `null`.

So the four combinations produce four genuinely different contracts for a consumer:

`str` &mdash; must be sent, cannot be null.
`str = "x"` &mdash; may be omitted, cannot be null.
`Optional[str]` &mdash; must be sent, may be null.
`Optional[str] = None` &mdash; may be omitted, may be null.

Reading them as sentences like that is the fastest way to check you have written what you meant. If the sentence sounds wrong for your API, the annotation is wrong.

## Designing create and update models

The place all of this comes together is a resource with more than one shape.

**Create** takes what a caller may supply. The server-assigned id is absent entirely &mdash; not optional, absent &mdash; because including it invites a caller to try setting it.

**Update**, for a PATCH, has every field optional with a `None` default, and is dumped with `exclude_unset=True` so that untouched fields stay untouched.

**Output** has everything the caller is allowed to see, with server-assigned fields required, because by the time you are returning one they exist.

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

Three small classes rather than one clever one. Each says exactly what it means, and none of them needs a comment explaining which fields apply when.

The temptation is always to collapse them into a single model with everything optional. It looks like less code and it is: it is also a model that documents nothing, generates useless API docs, and cannot tell a client what is guaranteed in a response.

## A note on validation order

Fields are validated in declaration order, and defaults are filled as part of that pass. This matters once you write a validator that reads another field: it can only see fields declared *above* it, because the ones below have not been processed yet.

If a rule needs the whole object, that is what `model_validator(mode="after")` is for &mdash; it runs once, after every field is in place. Trying to express a cross-field rule as a field validator on whichever field happens to come last works until somebody reorders the class.

## A checklist for a field you are about to write

Four questions, in order, and the annotation falls out of the answers.

**Can this be absent?** If yes, it needs a default. If no, leave the default off and let the model refuse.

**Can this be null, meaningfully?** Only if "no value" is a real state in your domain &mdash; an unwritten summary, an unfinished end date. If `None` would just mean "nobody bothered", it is not nullable; it is defaulted.

**Is the default a constant or does it depend on when we are?** A constant goes in directly. Anything computed &mdash; a time, an id, a fresh container &mdash; goes in `default_factory`.

**Am I creating or updating?** Creating means required fields are required. Updating means everything is optional and you dump with `exclude_unset=True`.

Most confusing models are the result of answering the second question with "I suppose so" instead of thinking about it. `Optional[X] = None` is the annotation people reach for when they have not decided, and a model full of them has quietly recorded that nothing was ever decided.

## What this buys downstream

The payoff for being precise here shows up somewhere else entirely: in the code that reads the model.

If `summary: Optional[str] = None` genuinely means "may not have been written yet", then `if module.summary:` is a meaningful branch about the domain. If it means "we were not sure", every reader has to defend against `None` on every field, and the type system has stopped helping.

Required fields are a promise to the rest of your program. Each one you make lets code downstream stop checking. That is the actual product of this module: not the syntax, but the discipline of deciding what is guaranteed and then writing it down where the compiler, the schema and the next reader can all see it.

## One last distinction

There is a fourth state people occasionally need, beyond required, defaulted and nullable: a field that may be absent but has no sensible default, where you genuinely want to know whether it was supplied.

That is what `model_fields_set` and `exclude_unset` exist for, and it is worth naming explicitly because the instinct is to invent a sentinel &mdash; a magic string, a `-1`, a custom `UNSET` object &mdash; and thread it through the code. Pydantic already tracks the answer. Reach for the sentinel only when the value has to survive serialisation, which is rare, and think hard before you do, because every consumer of that data now has to know about your magic value.

## Next

The next module is about the moment a model says no: how to read a `ValidationError` in full, what each part of an entry means, and how to turn one into a message a user can act on.
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
intro: Every field checked, every failure in one report - and what each part of an entry is for.

## One raise, every problem

Most hand-written validation gives up at the first thing it does not like. The caller fixes it, resubmits, and meets the next one. Four mistakes take four round trips.

Pydantic checks every field and raises once, carrying the complete list. For a signup form that is the difference between a form which highlights all four broken inputs immediately and one which reveals them slowly, like a bad quiz.

`e.error_count()` tells you how many. `str(e)` gives a readable summary, which is what you saw printed in the first editor above. Both are for humans.

## errors() is the version for code

`e.errors()` returns a list of dictionaries, and this is what you build anything real on top of. Each entry has four parts, and they do different jobs.

**`loc`** is where the problem is. It is a tuple, not a string, and it describes a path rather than naming a field. For a flat model it has one element. For nested data it has as many as it needs to reach the value.

**`type`** is which rule failed, as a short stable identifier: `missing`, `int_parsing`, `string_too_short`, `greater_than`, `value_error`.

**`msg`** is the human sentence, in English, written by Pydantic.

**`input`** is the value that actually arrived.

## loc, in detail

Reading `loc` well is most of debugging a large payload.

Integers in the tuple are sequence indices. Strings are field or key names. So `("lessons", 1, "minutes")` reads as: inside `lessons`, the item at index 1, its `minutes` field. Joining it with dots &mdash; `lessons.1.minutes` &mdash; gives you something you can paste into a search or show to a colleague.

For a union you will sometimes see the union member's name in the path too, because Pydantic reports which branch it was attempting when it failed. That looks noisy at first and is genuinely useful when a discriminated union picks the wrong branch.

The important habit is to render the path rather than the field name. Code that does `err["loc"][0]` works fine until the first nested model arrives, at which point every error appears to be about the top-level container.

## Match on type, not on message

This is the rule that saves the most future pain.

Messages are prose. They get reworded, clarified and occasionally translated between releases. Any code that does `if "should be a valid integer" in err["msg"]` is one minor upgrade away from silently failing.

Types are identifiers. `int_parsing` will still be `int_parsing`. Mapping them to your own copy is a dictionary lookup:

```python
FRIENDLY = {
    "string_too_short": "That needs to be a bit longer.",
    "missing": "This one is required.",
}
```

This is also how you localise. The type is the key; your translation table holds the sentences.

A useful default is to fall back to `err["msg"]` when a type is not in your table. You get good copy for the cases you have thought about, and something serviceable for the ones you have not.

## The shape an API wants

Most front ends want errors grouped by field, so each message can render beside the input that caused it:

```python
problems = {}
for err in e.errors():
    field = ".".join(str(p) for p in err["loc"]) or "_"
    problems.setdefault(field, []).append(err["msg"])
```

A list per field, because one field can fail several rules at once. The `or "_"` catches model-level errors, whose `loc` is empty because they belong to the whole object rather than any single field &mdash; a cross-field rule like "end date must be after start date" has nowhere else to go.

If you are using FastAPI, this transformation already happens for you: a `ValidationError` on a request body becomes a 422 whose body is essentially `e.errors()`. Knowing the shape means knowing what your own clients receive.

## Your own errors, in the same report

Custom rules do not need a separate channel. A validator that raises `ValueError` is caught and folded into the same list, with the type `value_error` and your message:

```python
@field_validator("track")
@classmethod
def known_track(cls, v: str) -> str:
    if v not in {"maths", "python", "dsa", "ml"}:
        raise ValueError("unknown track %r" % v)
    return v
```

This is a good thing to notice early. It means one piece of error-handling code covers built-in and custom validation alike, and a caller cannot tell &mdash; or need to care &mdash; which kind of rule they broke.

Raise `ValueError`, not `ValidationError`. Constructing a `ValidationError` by hand is awkward and unnecessary; Pydantic wraps yours correctly and adds the location for you. An `AssertionError` also works, but is a poor choice because assertions vanish when Python is run with `-O`.

## What input tells you

Do not skip `input`. It is often the entire diagnosis.

A caller insists they are sending a number, and `input` shows `"12"` with quotes &mdash; they are sending a string, and their JSON serialiser is the culprit. Or it shows `None` for a field they believe they set, and their own code has a missing key. Or it shows `"null"`, the four-character string, and something in the chain stringified a null.

None of that is visible in the message. All of it is visible in one line of the report.

## The parts of an entry you have not used yet

Beyond `loc`, `type`, `msg` and `input`, an error entry carries two more things.

`url` is a link to the documentation page for that error type. It is the `https://errors.pydantic.dev/...` line you see at the end of a printed error. It is genuinely useful while learning and noise in a log, so it can be turned off: `e.errors(include_url=False)`.

`ctx` holds the parameters of the rule that failed, when there are any. A `greater_than` error carries `{"gt": 0}`; a `string_too_short` carries `{"min_length": 3}`. This is what lets you write one message template per type and fill in the actual limit:

```python
TEMPLATES = {
    "greater_than": "Must be more than {gt}.",
    "string_too_short": "Needs at least {min_length} characters.",
}
msg = TEMPLATES[err["type"]].format(**err.get("ctx", {}))
```

That is the difference between "that is too short" and "needs at least 3 characters", without hard-coding the 3 in two places.

## Errors from a JSON string

`model_validate_json` produces the same error entries with one addition: when the JSON itself is malformed, you get a `json_invalid` error whose context includes the position in the document.

That matters for large payloads. A missing comma four hundred lines into a config file produces an error that names the line, which is considerably more use than "invalid JSON".

It is also why validating JSON directly is better than `json.loads` followed by `model_validate`. Go through `json.loads` and a syntax error is a `JSONDecodeError` from a different library, which you have to catch separately and which knows nothing about your model. Validate the JSON directly and malformed documents and invalid data arrive through one exception type, handled in one place.

## Model-level errors have no field

A rule that spans fields belongs to the object, not to any one field, so its `loc` is empty:

```python
@model_validator(mode="after")
def check_window(self):
    if self.ends_at <= self.starts_at:
        raise ValueError("ends_at must be after starts_at")
    return self
```

The resulting entry has `loc: ()`. Any code that assumes `loc[0]` exists will raise an `IndexError` on it &mdash; which is a bug that appears the first time somebody adds a cross-field rule, long after the error handling was written.

Handle it explicitly. Grouping code should fall back to a key like `"_"` or `"__root__"` for empty locations, and the front end should have somewhere to display an error that is not attached to an input.

## Testing that validation fails

Validation logic deserves tests, and the useful ones assert on `type` and `loc` rather than on prose.

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

Asserting on the message makes the test fail when Pydantic rewords something, which teaches your team to distrust the suite. Asserting on `loc` and `type` tests the thing you actually care about: that the right rule fired on the right field.

It is also worth testing the positive case explicitly &mdash; that a valid payload produces the values you expect, coercions included. A test that `minutes="9"` becomes the integer `9` documents an intention that is otherwise invisible.

## Making errors useful to a human

A last thought, because this is where validation meets the person using your software.

The default messages are written for developers. "Input should be a valid integer, unable to parse string as an integer" is precise and it is not what you want beside a form field. A user does not care about parsing; they care that they typed "ten" in a box that wanted a number.

The translation layer is small &mdash; a dictionary from `type` to a sentence &mdash; and it is worth building once, early, for the twenty or so error types your application can actually produce. Fall back to `msg` for anything unmapped so nothing ever renders blank.

And keep the developer version too. Logging the full `errors()` while showing the friendly version means that when a user says "it told me my email was wrong and it wasn't", you have the `input` value that settles it.

## A complete handler you can lift

Putting the pieces together, this is a small function that covers everything above &mdash; grouping by field, using `ctx` for the limits, falling back gracefully, and handling model-level errors:

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

Twelve lines, and it covers every error the application can produce. New error types degrade to Pydantic's own wording rather than to a blank space, so nothing is ever invisible, and adding a nicer message later is one dictionary entry.

## Why the design is the way it is

It is worth noticing what this error model is optimised for, because it explains several choices that look odd in isolation.

It reports everything at once because the expensive part of validation is the round trip to the user, not the checking.

It uses stable codes rather than messages because the consumer is often another program, and programs need identifiers that do not move.

It carries `input` because the most common question after a rejection is "what did they actually send", and the alternative is asking them.

And it makes `loc` a path rather than a name because real payloads nest, and an error that cannot say *where* in a hundred-line document the problem is has told you almost nothing.

Every one of those is a decision made for the person on the other end of the failure. Reading errors well is mostly a matter of noticing that the information you want is already in there.

## One more habit

Log the full error, show the friendly one.

These are different audiences with different needs, and collapsing them serves neither. The user needs a sentence they can act on, in their language, next to the input that caused it. You need `loc`, `type`, `input` and enough context to reproduce the failure without asking anyone anything.

Doing both costs one extra line at the point where you catch the exception, and it is the difference between a support conversation that starts with "can you tell me exactly what you typed" and one that starts with "I can see what happened". The information was in the exception the whole time; the only question is whether you kept it.

## Next

The next module goes the other way: not reading the errors Pydantic produces, but writing the rules that produce them. `Field` constraints let you say more about a value than its type &mdash; a minimum, a length, a pattern &mdash; and every one of them comes back through exactly the machinery described here.
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

`minutes: int` is a weak statement. It permits `0`, `-5000`, and a number larger than the age of the universe in seconds. None of those are durations. The annotation captures the shape of the value and nothing about its meaning.

`Field` closes that gap:

```python
minutes: int = Field(gt=0, le=180)
```

Now the model refuses what the domain refuses. Two things follow from that, and the second matters more than people expect.

The first is that bad data stops at the door. The second is that the rule is now written down in the one place a reader will look. A check buried in a service function is invisible to everyone who does not open that function; a constraint on the field is part of the model's definition, and it appears in the generated schema, the API documentation and your editor's tooltips.

## The number constraints

Four comparisons, named for the operators: `gt`, `ge`, `lt`, `le`. There is no `eq`, because that is what a `Literal` is for.

`multiple_of` constrains the step, which is more useful than it first appears &mdash; prices in whole pence, durations in five-minute blocks, page sizes in powers of ten.

Choosing between `gt=0` and `ge=1` on an integer field is worth a moment. They accept exactly the same values, but they say different things. `gt=0` says *positive*; `ge=1` says *at least one*. Pick the one that matches the sentence you would say out loud, because the error message the caller sees is generated from it.

## The string constraints

`min_length` and `max_length` bound the number of characters.

`pattern` takes a regular expression, and there is one detail that catches people: it is a *match from the start*, not a full-string search. `pattern=r"[a-z]+"` will happily accept `"abc123!!!"`, because the pattern matched at the beginning and nothing said it had to reach the end. If you mean the whole value, anchor it: `r"^[a-z]+$"`.

That single omission is the most common bug in this area, and it fails in the permissive direction &mdash; letting bad values through rather than rejecting good ones &mdash; which is exactly the way a validation bug survives longest.

Keep patterns simple. A regular expression that needs a comment is usually better as a `field_validator`, where you can name the rule and write a clear message. There is a module on those in the next tier.

## Collections

`min_length` and `max_length` work on lists, sets and dicts too, counting items rather than characters.

`min_length=1` is the useful one. "This list must not be empty" is a real rule that would otherwise cost you a validator, and it produces a better error than a downstream `IndexError`.

## Constraints and defaults

`Field` carries the default as well as the rules:

```python
minutes: int = Field(default=10, gt=0, le=180)
```

A field with constraints and no default is still required &mdash; `Field(gt=0)` does not make anything optional. This trips people who read `Field(...)` as being like a default.

For mutable or computed defaults, `default_factory` belongs here too: `Field(default_factory=list, max_length=8)` gives you an empty list per instance and a cap on how many items it may grow to.

You may also see `Field(...)` with a literal ellipsis in older code. That was the v1 way of writing "required", and it still works, but simply omitting the default is clearer.

## Order of operations

Constraints run **after** coercion, and knowing that removes a class of confusion.

A field declared `int = Field(gt=0)` given the string `"5"` first becomes the integer `5`, then is compared against zero. The comparison never sees the text. Likewise a `str` field with `min_length=3` counts characters after any string coercion has happened.

So a value can fail in two distinct ways, with two distinct error types: `int_parsing` if it could not become an integer at all, `greater_than` if it became one and was too small. Your error handling gets both for free, and they mean genuinely different things to a caller.

## Metadata is documentation

`Field` also carries `title`, `description` and `examples`. They change no behaviour whatsoever, and they are the highest-value thing in this module.

They land in `model_json_schema()`. If you are using FastAPI, that schema *is* your API documentation &mdash; the descriptions appear next to the fields, the examples pre-fill the interactive request form, the constraints show as the documented limits. You write a sentence in the model and it appears in the docs your consumers read.

For anything with an audience beyond yourself, describe the fields whose meaning is not obvious from the name. `minutes` needs no description. `weight` badly does &mdash; of what, in what unit?

## What constraints are not for

A constraint is a statement about a single value in isolation. Anything that depends on another field &mdash; an end date after a start date, a discount not exceeding a price &mdash; cannot be expressed here, because a field constraint cannot see its siblings. That is what `model_validator` is for.

Anything requiring a lookup &mdash; does this track exist, is this name taken &mdash; also does not belong here. A model should be able to validate without touching a database. Keep I/O-dependent rules in the layer that owns the I/O.

And a constraint is not a substitute for thinking about the type. If a field can only be one of four strings, `Literal["maths", "python", "dsa", "ml"]` is better than a pattern: it is clearer, it produces a better error, and it appears in the schema as an enumeration a client can render as a dropdown.

## Annotated: the other spelling

Everything in this module can also be written with `Annotated`, and in modern Pydantic that spelling is often the better one:

```python
from typing import Annotated
from pydantic import Field

minutes: Annotated[int, Field(gt=0, le=180)]
```

The two forms behave identically for a simple field. The difference appears when a default is involved, and it is a real improvement:

```python
minutes: Annotated[int, Field(gt=0, le=180)] = 10
```

Here the constraint lives with the type and the default sits where defaults normally sit. In the `= Field(default=10, gt=0)` form the two are tangled together in one call, and it is easy to misread which part is the default.

The bigger win is reuse, which the next section is about.

## Constrained types you can name

Because `Annotated` produces a type, you can give it a name and use it everywhere:

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

This is the single highest-value habit in this module. The rule for what a slug is now exists once. Change it and every model that uses it changes. Without this, the same regular expression gets copied into six models and four of them are updated when it changes.

It also improves the reading. `slug: Slug` says what the field is; `slug: str = Field(pattern=r"^[a-z0-9_]+$")` makes the reader parse a regular expression to find out.

Pydantic ships some of these ready-made &mdash; `PositiveInt`, `NonNegativeInt`, `PositiveFloat`, `StrictStr` and others &mdash; and they are worth using where they fit, for the same reason.

## Strictness on a single field

Whole-model strictness is a blunt instrument. Usually the need is narrower: lax about most of a payload, exact about one field where a silent conversion would be dangerous.

```python
user_id: int = Field(strict=True)
```

Now `user_id="123"` raises while the rest of the model still accepts strings for its numbers. Identifiers are the classic case: an id that arrives as text is usually a sign that something upstream is confused, and quietly converting it hides that.

The `Annotated` form works too: `Annotated[int, Field(strict=True)]`, which can then be named and reused like any other constrained type.

## More than one constraint, and how failures report

A field can carry several constraints, and they are all checked. If more than one fails, you get more than one error entry for that field:

```python
title: str = Field(min_length=3, max_length=10, pattern=r"^[A-Z]")
```

Given `"ab"`, both `min_length` and `pattern` fail, and both appear. That is worth knowing when you build the field-to-messages mapping described in the errors module: a field maps to a *list* of messages, not one.

Constraints are checked after coercion, and a coercion failure short-circuits the rest &mdash; there is no point comparing a value against zero when it never became a number. So a field produces either one `*_parsing` error or one or more constraint errors, never both.

## What the schema does with them

Every constraint has a JSON Schema equivalent, and Pydantic emits it:

`gt` becomes `exclusiveMinimum`, `ge` becomes `minimum`, `lt` becomes `exclusiveMaximum`, `le` becomes `maximum`. `min_length` and `max_length` become `minLength`/`maxLength` for strings and `minItems`/`maxItems` for arrays. `pattern` becomes `pattern`. `multiple_of` becomes `multipleOf`.

This is why constraints are better than validators when either would do. A `field_validator` that checks `v > 0` is invisible to the schema: the documentation says "integer", the client-side form has no idea, and the generated client will happily send `-1`. `Field(gt=0)` appears in the documentation as a documented minimum, and tooling that reads the schema can enforce it before a request is ever made.

The general rule: express a rule as a constraint if a constraint can express it, and reach for a validator only when it cannot.

## Constraints that are really types

Finally, a check worth running on yourself. If a constraint is trying to enumerate a small set of allowed values, it is the wrong tool.

```python
track: str = Field(pattern=r"^(maths|python|dsa|ml)$")     # works
track: Literal["maths", "python", "dsa", "ml"]             # better
```

The second version produces a clearer error, appears in the schema as an enumeration a client can render as a dropdown, and is checked by mypy in your own code. The regular expression does none of that, and it will be the thing somebody forgets to update when a fifth track is added.

## A short catalogue to work from

Everything available, in one place, so you can stop looking it up.

**Numbers:** `gt`, `ge`, `lt`, `le`, `multiple_of`. Also `allow_inf_nan=False` for floats, which is worth setting on anything that will be serialised to JSON &mdash; `Infinity` and `NaN` are not valid JSON, and a value that validated happily will fail on the way out.

**Strings:** `min_length`, `max_length`, `pattern`. Plus the config-level `str_strip_whitespace`, `str_to_lower` and `str_to_upper`, which apply to every string field on a model &mdash; stripping whitespace on input is almost always the right default for form data.

**Collections:** `min_length`, `max_length`.

**Decimals:** `max_digits` and `decimal_places`, which are what you want for money and which no amount of `float` will give you.

**Everything:** `strict`, `frozen` on a single field, `description`, `title`, `examples`, `deprecated`, `repr=False`, `exclude=True`.

## The habit this module is really teaching

Look at the constraints you have written and ask what a reader learns from them. A well-constrained model is a specification: someone can read the class and know what the system considers a valid module, without opening a single function.

An unconstrained model is a list of types, and the actual rules are scattered through the code that consumes it &mdash; a check here, an assertion there, an assumption somewhere else that nobody wrote down. Those rules still exist. They are just not anywhere you can read them, and they disagree with each other more often than anyone expects.

Moving a rule into the model is not primarily about catching bad data, though it does that. It is about having one place where the shape of your domain is stated, which is the same reason the annotations were worth enforcing in the first place.

## Next

That completes the foundations. You can define a model, know exactly what it will and will not convert, control what is required, narrow values to your domain, and read the errors when something does not fit.

The last module in this tier steps back to a question worth answering before you reach for a model at all: when a plain dataclass is the better tool.
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
intro: Both build a class from annotations. Only one checks anything, and that is the whole decision.

## They look almost identical

```python
@dataclass
class Module:
    title: str
    minutes: int

class Module(BaseModel):
    title: str
    minutes: int
```

Two lines of difference, and both give you a constructor, a readable `repr`, equality by value and a way to get a dictionary out. It is entirely reasonable to wonder whether the choice matters.

It matters in exactly one place: what happens when the data is wrong.

## What a dataclass actually does

`@dataclass` reads the annotations to find out which fields exist and in what order, and then generates an `__init__` that assigns them. That is the extent of its interest in the types. The annotation `minutes: int` is used to decide that a field called `minutes` exists. Its being an `int` is never checked, tested or acted on.

So `Module(title=None, minutes=[1, 2, 3], published="perhaps")` constructs perfectly happily. Nothing is wrong until something downstream assumes the annotation was true &mdash; and then it fails somewhere else, with a traceback pointing at the innocent party.

This is not a flaw. A dataclass is a code-generation convenience, and it does what it advertises. It just does not do the thing people sometimes assume it does.

`NamedTuple` and `TypedDict` are in the same position, and it is worth saying because `TypedDict` in particular looks like it should be validating something. It is not. It is a description for static type checkers, invisible at runtime.

## What that guarantee costs

Validation is real work: reading a schema, checking each field, sometimes converting. It is not free, and any honest comparison has to say so.

The timing in the third editor above is worth running. Pydantic 2's core is Rust, so the gap is far smaller than it was in v1, but a dataclass is still faster, for the simple reason that doing nothing is quicker than doing something.

Read the *ratio* rather than the seconds. Everything on this page runs on CPython compiled to WebAssembly, which is several times slower than a native interpreter. The relative comparison holds; the absolute numbers do not transfer to your laptop.

And put the ratio in context. A model that validates in a few microseconds is irrelevant next to a database query taking milliseconds, or a network call taking hundreds. Validation cost matters in tight loops over large collections, and almost nowhere else. Choosing a dataclass "for performance" in a request handler that then makes three SQL queries is optimising the wrong end.

## The answer is usually both

The instinct to pick one and use it everywhere is what makes this question feel harder than it is. The better framing is *where in the system am I*.

At the **boundary** &mdash; a request body, a config file, a CSV, another service's response &mdash; the data is a guess until proven otherwise. Validate. This is the whole point of the library, and the cost is paid once per item arriving.

**Inside**, past that line, the data has already been checked. Re-validating it at every layer buys nothing: the same values, checked again, will pass again. If you have a hot loop over ten thousand records, a dataclass is a reasonable interior representation, and converting is one line:

```python
checked = ModuleIn.model_validate(raw)   # validate once
module = Module(**checked.model_dump())  # then go cheap
```

Be honest about whether you need that, though. For most applications, using models throughout is simpler, and simpler is worth more than a microsecond. The two-representation pattern earns its keep when profiling has actually pointed at validation.

## The middle option

If you like the dataclass API &mdash; or you have a codebase full of them &mdash; `pydantic.dataclasses.dataclass` is a drop-in replacement that validates:

```python
from pydantic.dataclasses import dataclass

@dataclass
class Module:
    title: str
    minutes: int
```

Same decorator shape, same `dataclasses.fields()` introspection, and now `minutes="eight"` raises. It is a good way to add checking to existing code without rewriting it into models.

The trade is that you get less of Pydantic. `model_dump`, aliases, custom serialisers and the richer config surface belong to `BaseModel`. For anything that is going to be serialised, aliased or documented, a real model is the better home.

## Validating without a class at all

`TypeAdapter` is the piece most people meet late and wish they had met early. It applies the whole validation machinery to any annotation, with no model in sight:

```python
TypeAdapter(List[int]).validate_python(["8", "12", 14.0])   # [8, 12, 14]
```

That is genuinely useful. A JSON array of numbers has no natural model wrapped around it. Neither does a `Dict[str, float]` of settings, or the argument to a function you want to check at its edge. Building a one-field model to hold a list is a common workaround, and `TypeAdapter` is the thing it was working around.

It gets a full module in the serialisation tier, because it also handles dumping and schema generation for bare types.

## A short decision list

Reach for **`BaseModel`** when data crosses a boundary, when you need serialisation or aliases, or when the thing should appear in an API schema. This is most of the time.

Reach for **`@dataclass`** for internal values that never leave the process and never arrive from outside it &mdash; and where you have a reason beyond habit.

Reach for **`pydantic.dataclasses.dataclass`** when you want validation on a dataclass that already exists.

Reach for **`TypeAdapter`** when the thing you need to validate is not a class.

## The rest of the field

Dataclasses are not the only alternative, and the others sit in predictable places.

**`attrs`** is the library dataclasses were inspired by, and it is still ahead in features: converters, richer validators, better control over generated methods. It does validate, if you ask it to, and it is a reasonable choice for internal classes with complex construction. It is not aimed at the boundary and does not generate JSON Schema.

**`NamedTuple`** gives you an immutable, tuple-shaped record with named access. It checks nothing at runtime, and its tuple-ness is either the point or a trap depending on whether you wanted something you can unpack and compare positionally.

**`TypedDict`** describes the shape of a dictionary for a static type checker. It is worth being clear about this one: at runtime, a `TypedDict` **is a plain dict**. There is no class, no checking, and no error if a key is missing or the wrong type. It is a comment mypy can read. Where people usually want a `TypedDict` and validation, what they want is a model.

**`SQLModel`** joins Pydantic and SQLAlchemy so one class can be both a table and a validated model. It is convenient and it is a coupling: your API shape and your database schema become the same object, which is fine until they need to differ, which they eventually do.

## Memory, and the shape of an instance

A `BaseModel` instance stores its data in `__dict__` plus some bookkeeping &mdash; `__pydantic_fields_set__` for what was supplied, and a reference to the compiled validator on the class.

A dataclass also uses `__dict__` unless you declare `slots=True`, which trades the ability to add attributes for a smaller, faster object. A `NamedTuple` is the smallest of the lot, being a tuple.

For thousands of objects this is invisible. For millions it is not, and it is a real reason to use something leaner for the interior of a numerical or batch-processing system. It is also a reason not to worry about it before you have measured, because "millions of objects" is a specific situation rather than a general one.

## Moving between them

Conversion is mechanical in every direction, which is what makes the boundary-then-interior pattern practical.

From model to dataclass: `Module(**checked.model_dump())`.

From dataclass to model: `ModuleIn.model_validate(dataclasses.asdict(d))`, or `model_validate(d)` directly, since Pydantic can read attributes off arbitrary objects when the model sets `from_attributes=True`.

That last setting deserves a mention of its own. `from_attributes=True` lets a model validate from any object with matching attributes rather than requiring a dict:

```python
class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    minutes: int

ModuleOut.model_validate(orm_row)
```

This is how a model reads an ORM row, and it is the single most common reason to reach for it. In Pydantic v1 it was called `orm_mode`, which is the name most tutorials still use.

## When a model is genuinely too much

A short list of cases where reaching for `BaseModel` is over-engineering.

A function returning two values does not need a model. A tuple, or a `NamedTuple` if the names help, is fine.

A short-lived internal structure that never leaves the function that built it does not need validation, because nothing untrusted can reach it.

A constant lookup table is a dict. Wrapping it in a model to get attribute access is a lot of ceremony for a dot.

And a value with one field is usually just that value. `class Slug(BaseModel): value: str` is a wrapper that every caller has to unwrap. If you want a validated string type, `Annotated[str, Field(pattern=...)]` gives you that without the box.

## The question to actually ask

Not "which is faster" or "which is more modern", but: **does anything untrusted reach this object, and does it ever leave the process?**

If untrusted data reaches it, you need validation, and `BaseModel` is the tool built for that.

If it leaves the process &mdash; as JSON, in a response, in a schema &mdash; you want serialisation and documentation, and again that is `BaseModel`.

If neither is true, you have an internal value, and the lightest thing that expresses it well is the right answer. That will usually be a dataclass, and occasionally a tuple.

Most objects in most applications are at a boundary, which is why the honest general recommendation is to use models and stop worrying about it. The interesting cases are the exceptions, and now you can recognise them.

## A note on migrating an existing codebase

If you arrive at this with a project full of dataclasses, you do not have to choose in one go.

The cheapest first move is to convert only the classes that sit at a boundary &mdash; whatever parses your config, whatever accepts a request body, whatever reads a file. Those are where bad data enters, and they are usually a small fraction of the classes in a project. Everything else can stay exactly as it is.

The second move, if you want checking without restructuring, is `pydantic.dataclasses.dataclass` on the classes that stay. It is a one-line change per class, keeps `dataclasses.fields()` working for anything that introspects them, and starts raising on wrong types immediately.

What you should not do is convert everything to `BaseModel` mechanically. You will end up validating objects that were constructed by your own code from already-validated data, paying for checks that cannot fail, and the diff will be too large for anyone to review properly.

## Summary

A dataclass generates a class from annotations and never looks at the types again. A model generates a class from annotations and enforces them, converts what can be converted, produces structured errors, serialises in both directions and emits a schema.

The cost of all that is real and small, and it is paid where you decide to pay it. The discipline is the same one this whole tier has been building towards: know where your boundaries are, check there, and trust what you have checked.

Choose a dataclass for internal values that never meet the outside world. Choose a model for everything else. And when you are genuinely unsure, choose the model &mdash; a slightly over-validated program is a much smaller problem than one where nobody can say which values are guaranteed.

## Where this leaves you

That is tier one. You can define a model, predict exactly what it will convert, control what is required and what is merely nullable, narrow values to your domain with constraints, read the errors when data does not fit, and choose between a model and a plain class on grounds better than taste.

The next tier is about data with shape: models inside models, lists of them, unions that pick between alternatives, and the standard-library types &mdash; dates, UUIDs, decimals &mdash; that Pydantic already knows how to handle.
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

There is no special syntax for nesting. A model is a type, and a field can be annotated with any type, so a field can be a model:

```python
class Author(BaseModel):
    name: str
    email: str

class Module(BaseModel):
    title: str
    author: Author
```

That is it. Everything else follows from that one fact, which is worth stating plainly because people often expect a nested schema to need declaring somehow. It does not. If you can write the inner model on its own, you can use it as a field type.

When `Module` is validated, the value for `author` is handed to `Author` for validation. If it is already an `Author`, it passes through. If it is a dict, it becomes one. If it is neither, the error says so.

## Dicts in, objects out

The conversion from dict to object is the part that makes nesting useful rather than merely possible.

JSON has objects, and Python decodes them as dictionaries. Without nested models you would receive `{"author": {"name": "Ada"}}` and reach into it with `data["author"]["name"]` &mdash; two dictionary lookups, each of which can raise `KeyError`, neither of which your editor can help with.

With nesting you get `m.author.name`. It is checked, it is autocompleted, and a typo is an `AttributeError` at the point of the typo rather than a `KeyError` somewhere downstream.

The reverse works too: `model_dump()` recurses, and the result is nested plain dicts. So a model tree converts to and from JSON structure without you writing any of the walking.

## Errors that name the exact value

Nesting is where the `loc` design pays off, and it is worth dwelling on because it is the difference between a debuggable API and an infuriating one.

A failure two levels down produces `loc: ("author", "email")`. Joined with dots, `author.email`. Three levels down with a list in the middle produces `("modules", 0, "lessons", 1, "minutes")` &mdash; the second lesson of the first module.

Compare that with what a hand-rolled validator typically manages: "invalid module". For a payload of any size, the difference is between a caller who can fix the problem in ten seconds and one who has to bisect their own request.

There is a related failure worth recognising. If the value for a nested field is not a mapping at all &mdash; a string, say &mdash; the error is on the field itself, with `loc: ("author",)` and the type `model_attributes_type`. That means "I could not even begin to read this as an Author", which is a different problem from a field inside it being wrong, and the shape of the error tells you which you have.

## Every rule still applies, at every level

A nested model is not a lesser thing. Its constraints run, its validators run, its defaults are filled, its config applies.

```python
class Author(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@]+@[^@]+\\.[^@]+$")
```

Use that as a field type and every parent gets those rules for free. This is the compounding benefit of composition: a well-specified small model is reusable, and each place it is reused inherits the entire specification rather than a copy of it that can drift.

It is also the argument for making small models. `Address`, `Money`, `DateRange`, `Contact` &mdash; anything that appears in more than one place and has rules of its own is a model waiting to be extracted. The alternative is the same four fields and the same three constraints written out in five parent models, four of which get updated when the rule changes.

## Optional and defaulted nested models

The rules from the defaults module apply without modification, and one of them has a specific trap here.

For a nested model that should always exist, use `default_factory`:

```python
reviewer: Author = Field(default_factory=Author)
```

Not `= Author()`. That expression is evaluated once, when the class body runs, so every parent would share one `Author` instance &mdash; and since models are mutable by default, a change through one parent would be visible through all of them. Pydantic deep-copies simple defaults, but constructing the instance at class-definition time is still the wrong shape, and a factory says what you mean.

For a nested model that may genuinely be absent, `Optional[Author] = None` behaves exactly as it does for any other type, with the same distinction between omitted and explicitly null.

Note that a nested model whose own fields all have defaults can be built from an empty dict, which occasionally surprises people: `Module(title="x", author={})` succeeds if every `Author` field has a default. That is correct, and it is a good reason to think about whether those inner defaults should exist.

## Shaping the output

`model_dump` takes `include` and `exclude`, and both understand structure. A set names top-level fields; a dict reaches inside. The two spellings do not mix in one literal, so once any entry needs to reach inside, every entry becomes a key:

```python
m.model_dump(exclude={"internal_notes": True, "author": {"email"}})
```

That drops one top-level field and one field of the nested model, keeping everything else. For lists of models there is a special key, `"__all__"`, which applies the same selection to every item.

This is genuinely useful for the common case of one internal representation and several external views. It is also easy to overuse. Once the exclusion dict is more than a couple of entries, a separate output model is clearer: it is checked, it appears correctly in the schema, and nobody has to trace an exclusion expression to work out what an endpoint actually returns.

The rule of thumb: `exclude` for removing one obviously-internal field, a separate model for anything structural.

## Recursive models

A model can refer to itself, which is how you describe trees &mdash; comment threads, category hierarchies, nested menus:

```python
class Node(BaseModel):
    name: str
    children: List["Node"] = []
```

The quotes are needed because the class does not exist yet at the point the annotation is written. In modern Python with `from __future__ import annotations`, or in files where all annotations are strings, you can drop them.

Recursive models validate to any depth and dump to nested dicts as you would expect. Two cautions. Depth is bounded by the recursion limit, so genuinely deep or maliciously nested input can raise, which is worth thinking about if the data is untrusted. And a cycle &mdash; a node that contains itself &mdash; will not terminate on dump; Pydantic detects some cases and raises, but the honest fix is not to build cyclic data in a model designed as a tree.

## What good nesting looks like

Extract a model when a group of fields travels together and has rules of its own. `Address` is a model; `city: str` sitting beside `postcode: str` in four different parents is four copies of a decision.

Keep the tree shallow where you can. Three levels is normal; six usually means the shape is describing your storage rather than your domain, and a flatter representation with references would read better.

Name inner models for what they are, not for where they sit. `Author` is reusable; `ModuleAuthor` is a name that stops the model being used anywhere else even when it would fit perfectly.

## Reusing a nested model across parents

The strongest argument for extracting a model is that the rules travel with it.

```python
class Address(BaseModel):
    line1: str = Field(min_length=1)
    city: str
    postcode: str = Field(pattern=r"^[A-Z0-9 ]{4,8}$")
```

Use `Address` in `Customer`, `Invoice` and `Warehouse` and all three enforce the postcode rule. Change the rule and all three change. The alternative &mdash; three copies of three fields and one regular expression &mdash; is three chances for the copies to diverge, and they will.

The signal that a model wants extracting is fields that travel together. If `city` and `postcode` never appear apart, they are one concept with two attributes, and naming that concept makes the parent shorter and the rule reusable.

## Validating against objects, not just dicts

Nested models normally arrive as dicts, because that is what JSON decodes to. Sometimes the source is objects instead &mdash; ORM rows, another library's classes &mdash; and by default a model will not read attributes off an arbitrary object.

`from_attributes` changes that:

```python
class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    author: AuthorOut
```

Now `ModuleOut.model_validate(orm_row)` reads `row.title` and `row.author`, and validates the nested object the same way. This is how a model turns a database row into a response, and it recurses, so a row with a related object becomes a nested model without any manual walking.

In Pydantic v1 this setting was called `orm_mode`, which is the name most existing tutorials use.

## Performance, and what nesting costs

A nested model is a validation of its own. A parent with three nested models does four validations, and a list of fifty nested models does fifty-one.

That is the honest cost, and for a request handler it is irrelevant &mdash; the whole tree still validates in microseconds. It becomes worth thinking about for bulk work, and the advice is the same as everywhere else in this library: validate the tree once at the boundary, then pass the resulting objects around without re-validating.

The specific mistake to avoid is re-validating on the way out. Building a response by constructing an output model from an already-validated input model re-runs every rule in the tree for no benefit. If the shapes are the same, `model_dump()` and a direct construction is cheaper; if they differ, the second validation is doing real work and is fine.

## A worked shape

Most real payloads are two or three levels, and the pattern is consistent:

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

Read it top to bottom and you have the entire contract: a module has a title, exactly one author with a name and an email, and at least one lesson, each with a positive duration. No function needs to be opened to learn any of that, and none of it can drift, because it is the code that runs.

That is what nesting buys. Not the convenience of dotted access, though that is pleasant, but a specification that is executable.

## The habit to take away

Every time you find a group of fields repeated across two models, or a comment explaining what shape a dictionary is meant to have, you have found a nested model waiting to be named.

The cost is three lines. The return is a rule that lives in one place, an error path that says exactly where a failure was, dotted access instead of chained lookups, and a schema that describes the real structure rather than a flat approximation of it.

Composition is the least clever feature in this library and one of the most valuable, precisely because it needs no special syntax. A model is a type. Types go in annotations. Everything else follows.

## A note on how deep to go

Depth in a model tends to mirror depth in whatever produced the data, and that is not always the shape you want to work with.

A payload that nests six levels because a database has six joined tables is describing storage, not domain. Flattening it &mdash; or replacing an inner object with a reference and fetching separately &mdash; usually produces a model that reads better and an API that is easier to consume.

Three levels is comfortable. Four is worth a second look. Beyond that, the question is usually not "how do I model this" but "should the caller be receiving all of this at once".

## Next

Nesting one model inside another is half the picture. The other half is collections: lists of models, dicts keyed by something meaningful, and what happens to the error path when the failure is in the seventeenth item.

## Summary

A model used as a field type is validated with its full rules, dicts become objects recursively, and errors carry the whole path to the failing value.

Extract a model whenever fields travel together or a group of them is repeated. Use `default_factory` for a nested default. Reach for `include`/`exclude` to drop a field or two, and for a separate output model when the difference is structural.
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
intro: Lists, dicts, sets and tuples - what gets validated, what gets converted, and where failures point.

## Item by item

A container annotation describes two things: the shape of the container and the type of what is in it. Both are enforced.

```python
lessons: List[Lesson]
```

Given a list, Pydantic walks it and validates each element as a `Lesson`. A dict becomes a `Lesson` object. An element that is already a `Lesson` passes through. An element that is neither produces an error &mdash; for that element only.

That last part matters more than it sounds. Validation does not abandon the collection at the first bad item. It checks all of them and reports all the failures, which for a bulk import is the difference between fixing one row per attempt and seeing the whole problem at once.

## The index is part of the path

An integer in `loc` is a position. So `("lessons", 1, "minutes")` reads as: the `lessons` field, the item at index 1, its `minutes` field.

For a payload with a hundred items this is the entire diagnosis. Without it, "one of your lessons has an invalid duration" sends the caller looking through a hundred objects by hand.

Note that the index is the position in the *input*, which is what you want &mdash; it lets the caller map the error back to the data they sent. If you are surfacing these to a user editing a form with repeated rows, the index is exactly the row number to highlight.

## Dicts, and what the key does

`Dict[str, Stats]` validates keys against `str` and values against `Stats`, independently.

The key type is a real constraint, and a useful one. `Dict[int, Stats]` will coerce the string keys that JSON forces on you back into integers, which is a small annoyance handled once instead of at every read site. JSON object keys are always strings, so this comes up more often than you would expect.

In the error path, the key appears where an index would: `("tracks", "maths", "minutes")`. Same mechanism, same readability.

A caution about key coercion with untrusted data: `Dict[int, X]` given `{"1": ...}` gives you `{1: ...}`, and two keys that differ only as strings can collide as integers. It is a narrow case, but it is the kind of thing worth knowing before it happens.

## Sets deduplicate

`Set[str]` given `["maths", "vectors", "maths"]` gives a set of two items. No error, no warning &mdash; deduplication is what a set is for.

That is usually the intent. Where it bites is when the duplicates were meaningful and nobody thought about it: a list of tags is fine to deduplicate; a list of readings from a sensor is not, and a `Set[float]` will silently discard every repeated measurement.

Sets are also unordered, so the order you sent is not the order you get back, and `model_dump_json` has to produce an array from something with no defined order. If order matters, use a list &mdash; and if uniqueness matters too, check it in a validator, which gives you an error instead of silent removal.

## Tuples check length and position

There are two spellings and they mean different things.

`Tuple[int, str]` is a fixed shape: exactly two items, the first an int, the second a string. Length is part of the contract, and a three-item input fails with `too_long`.

`Tuple[int, ...]` is a homogeneous sequence of any length &mdash; the same as `List[int]` except immutable on the way out.

Fixed tuples are good for genuinely positional data: coordinates, RGB values, a dimension pair. They are a poor choice for anything where the positions have names, because `point[0]` is worse than `point.x` and nobody can tell what `config[3]` is. If you find yourself writing a comment to explain the positions, you want a model.

## Constraining the container

`min_length` and `max_length` count items:

```python
lessons: List[str] = Field(min_length=1, max_length=4)
```

`min_length=1` is the useful one. "This must not be empty" is a real rule, and expressing it as a constraint rather than a validator means it appears in the schema as `minItems`, so a generated client and the API documentation both know about it.

Empty collections are worth a moment's thought generally. An empty list is a valid list, and code that assumes at least one element will fail on it &mdash; usually with an `IndexError` far from the model. Deciding explicitly whether empty is allowed, and writing that decision down, removes a whole category of downstream surprise.

## Bare arrays and TypeAdapter

Not every payload has an object around it. An endpoint that returns a JSON array of lessons has no natural wrapper model, and the traditional workaround is to invent one:

```python
class LessonList(BaseModel):      # a box built only to hold a list
    items: List[Lesson]
```

`TypeAdapter` is what that workaround was working around:

```python
lessons = TypeAdapter(List[Lesson])
parsed = lessons.validate_json(payload)
```

You get the same validation, the same error paths, and `dump_json` in the other direction. It also works for anything else you can annotate &mdash; `Dict[str, float]`, `Optional[int]`, a bare `Lesson`, a union.

Build the adapter once and reuse it. Constructing a `TypeAdapter` compiles a schema, which is not free; doing it inside a loop is a genuine and easily-missed performance mistake. Module level is the right home.

## Performance with large collections

This is the place in Pydantic where validation cost becomes visible, so it is worth being concrete.

Validating ten thousand items means ten thousand validations. The work happens in Rust, which makes it far faster than a Python loop doing the same checks, but it is not free.

The important thing is to let the core do the looping. `TypeAdapter(List[Lesson]).validate_python(rows)` validates the whole list in one call into the compiled core. Writing `[Lesson.model_validate(r) for r in rows]` does the same work with ten thousand round trips between Python and Rust, and it is measurably slower for no benefit.

If you are streaming a very large file, validate in batches rather than building one enormous list, for memory reasons rather than validation ones.

And apply the rule from the first tier: validate once, at the boundary. Re-validating a list of models that has already been checked is the most expensive no-op available.

## Choosing the container

`List` when order matters or duplicates are meaningful &mdash; which is most of the time.

`Set` when the values are genuinely a set and you want deduplication as a feature, not as an accident.

`Dict` when items are looked up by a key that means something. If you find yourself scanning a list to find the item with a matching id on every read, a dict keyed by that id is the shape you wanted.

`Tuple` for fixed positional data, and only when the positions do not deserve names.

## Mutable defaults, one more time

The rule from the defaults module has a specific shape here that is worth repeating, because collections are where it bites.

```python
lessons: List[Lesson] = []
```

This is safe in Pydantic. The default is deep-copied per instance, so two models never share a list. In plain Python the equivalent would be the classic shared-mutable-default bug, and the habit people bring from there is to reach for `default_factory` reflexively.

That habit is not wrong, and `Field(default_factory=list)` is arguably clearer about intent. But it is worth knowing which of the two rules you are following, because the reason matters: use a factory because the default must be *computed*, not because a literal would be shared.

## Uniqueness without a set

If you want a list &mdash; order preserved, JSON array on the way out &mdash; but duplicates rejected rather than silently dropped, a set is the wrong tool. Deduplication and rejection are different behaviours.

The check belongs in a validator, which is the next tier's subject, but the shape is worth seeing now:

```python
@field_validator("tags")
@classmethod
def unique(cls, v: List[str]) -> List[str]:
    if len(set(v)) != len(v):
        raise ValueError("tags must be unique")
    return v
```

The difference from `Set[str]` is what the caller learns. A set tells them nothing and quietly returns fewer items; the validator tells them their input was wrong. For a form where somebody typed the same tag twice, the second is much more useful.

## Nested collections

Collections nest as freely as models do, and the error paths keep working:

```python
schedule: Dict[str, List[Lesson]]
```

A failure inside produces `("schedule", "monday", 2, "minutes")` &mdash; the key, the index, the field. Four elements, and it names exactly one value in a structure that would otherwise take a while to search by hand.

The practical limit is comprehension rather than capability. `Dict[str, List[Dict[str, List[int]]]]` is valid and nobody can read it. Once an annotation needs more than about three levels, extracting a model for the inner shape makes the outer one legible again &mdash; and gives the inner shape a name, which is usually the thing that was missing.

## Ordering and duplicates in the output

Two small behaviours that surprise people at serialisation time.

A `Set` has no order, so `model_dump_json` produces an array in whatever order the set iterates. That order is stable within a run but is not the input order, and it is not guaranteed across runs. If a client diffs your responses, or a test compares JSON strings, a set field will produce spurious differences. Use a list and sort it if you need determinism.

A `Dict` preserves insertion order in modern Python, so dict fields do round-trip in a stable order. That is a language guarantee rather than a Pydantic one, but it is dependable.

## Choosing well, in practice

Most collection bugs come from picking the container for the wrong reason.

Choosing `Set` because "items should be unique" gives you silent deduplication when what you wanted was an error.

Choosing `Tuple` because "it should not change" gives you positional access when what you wanted was a frozen model.

Choosing `List` when every read starts with a scan for a matching id means you wanted a `Dict` and are paying a linear search for it.

The question that resolves all three: what does the *consumer* of this field do with it? Iterate in order, look one up by key, or check membership? Each of those has an obvious container, and the answer is rarely about what the producer finds convenient to send.

## What the container says to a reader

A last thought that applies to every collection you annotate.

The container type is documentation. `List[Lesson]` says these are ordered and repeats are meaningful. `Set[str]` says order is irrelevant and duplicates are not a thing. `Dict[str, Stats]` says you look these up by name. `Tuple[int, int]` says exactly two, and the positions mean something fixed.

Someone reading the model learns all of that without opening a single function. Choosing the container carelessly &mdash; defaulting to `List` because it is the one that always works &mdash; throws that away and leaves the reader to infer the rules from the code that consumes it, which is exactly the situation models exist to prevent.

## Two failure modes to watch for

**Assuming non-empty.** Code that reads `items[0]` will raise on a valid empty list. Either constrain the field with `min_length=1` so an empty collection never reaches you, or handle the empty case explicitly. Silently assuming is how a rare payload becomes an incident.

**Assuming small.** A list annotation places no upper bound, so a caller can send a million items and your process will try to validate all of them. For any public endpoint, `max_length` is a cheap denial-of-service guard as well as a documented limit, and it costs one argument.

Both are the same oversight: a container's *size* is part of its contract, and leaving it unstated means the contract is whatever the caller decides.

## Next

Collections handle many things of the same type. The next module is about the opposite problem: a field that could be one of several *different* types, and how to make that choice explicit rather than letting Pydantic guess.

## Summary

Containers validate their contents item by item, and every failure carries a path that names the exact position &mdash; index for a sequence, key for a mapping. Nothing is skipped because something earlier failed, so one report covers the whole collection.

Choose the container for what the consumer does with it, not for what is convenient to build. Constrain the size, because an unbounded collection is an unstated contract. And when the payload is a bare array with no object around it, use `TypeAdapter` rather than inventing a wrapper model to hold it.
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
intro: A field that could be several shapes, and how to make the choice explicit.

## The problem a union creates

`Union[A, B]` says a value may be either. What it does not say is how to decide which, and something has to decide.

For simple types the decision is usually obvious and usually right. For models it is frequently neither, and the failure mode is the worst kind: it does not raise, it just gives you the wrong object.

## Smart mode, and what it actually does

Pydantic v2 does not simply try members left to right. It uses **smart mode**, which is a two-pass strategy.

First it looks for a member the value already matches exactly, without any conversion. An `int` input against `Union[int, str]` matches `int`; a `str` input matches `str`. No ambiguity, no order dependence.

Only if nothing matches exactly does it try conversion, left to right, taking the first that succeeds.

This resolves most everyday unions sensibly, and it is a genuine improvement over v1, which was strictly left-to-right and would happily turn an integer into a string because `str` was written first.

But it does not eliminate ambiguity. It relocates it to the cases where nothing matches exactly &mdash; which, for data arriving from JSON as strings, is a lot of cases.

## Where order still decides

`Union[int, float]` given the string `"7"` produces an `int`. `Union[float, int]` given the same string produces a `float`. Neither member matched exactly, so conversion ran left to right and the first success won.

If the difference matters to your program &mdash; and the difference between `7` and `7.0` matters in more places than people expect, from JSON output to dictionary keys to equality comparisons &mdash; then you have a behaviour that depends on the order somebody wrote two words in. That will survive exactly until somebody reorders them for tidiness.

The lesson is not to memorise the rules. It is that a plain union of convertible types is an unstable way to express a real distinction.

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

Both accept `{"title": "Vectors"}`, because the other field has a default in each. Neither matches "exactly" in any meaningful sense, so the first that validates wins &mdash; and that is `Video`, purely because of where it appears in the annotation.

The result is a `Video` that was meant to be a `Quiz`, constructed without any error, and discovered somewhere much later when `questions` is missing.

Defaults make this dramatically more likely, which is worth noticing: adding a default to a field of one union member can change how *other* payloads are classified.

## The fix is a tag

A discriminated union asks the data to say which shape it is. Each member gets a `Literal` field with a distinct value, and the union names it:

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

Now there is no guessing. Pydantic reads `kind`, looks up the corresponding model, and validates against that one only.

This is the same pattern as a tagged union in other languages, and the same one you see in real API payloads everywhere &mdash; Stripe events, webhook bodies, message envelopes. If your data already has a `type` or `kind` field, it is already discriminated and you are just telling Pydantic about it.

## Three things you get

**Correctness.** The tag decides, so the answer does not depend on annotation order, on which fields happen to have defaults, or on which member was added first.

**Better errors.** Without a discriminator, a failure means Pydantic tried every member and none worked, so you get the errors from all of them &mdash; a pile of messages about branches you were never in. With a discriminator, it tried exactly one, and reports exactly that one's problem.

That difference is stark on a union with five members. It turns "here are fifteen errors, work out which three are yours" into "seconds should be a valid integer".

**Speed.** One dictionary lookup on the tag, rather than attempting validation against each member until something sticks.

## When the tag is wrong

The discriminator field is validated too. A value that matches no member produces a single `union_tag_invalid` error listing the permitted tags, which is an excellent error &mdash; it tells the caller both what was wrong and what the options are.

A payload missing the tag entirely gives `union_tag_not_found`. Again, one clear error rather than a scatter.

## Practical shapes

Discriminated unions compose. A `List[Union[Video, Quiz]]` with a discriminator validates each item by its own tag, which is exactly what a feed of mixed content needs, and errors still carry the index.

The tag field is a real field. It appears in `model_dump()`, it is required, and it must be a `Literal` &mdash; a plain `str` will not do, because the whole mechanism depends on the value being known at class-definition time.

For a union that grows over time, `Union` of many members is unwieldy to write. `Annotated` helps:

```python
Content = Annotated[Union[Video, Quiz, Article], Field(discriminator="kind")]
```

Now `Content` is a named type you can use anywhere, and adding a fourth member is one edit in one place.

## Optional is a union too

Worth noticing, because it demystifies a thing people treat as special: `Optional[X]` is exactly `Union[X, None]`, and everything above applies to it.

It happens to be the least ambiguous union possible, since `None` is only ever itself and nothing converts to it. That is why `Optional` never causes the problems this module describes, and why it is safe to reach for without thinking.

## What to reach for

Use a plain union for genuinely simple cases where every member is a distinct, non-convertible type &mdash; `Union[int, None]`, or a union of models with obviously disjoint required fields.

Use a discriminated union for anything polymorphic: content types, event types, message kinds, shape variants. If you are modelling "one of these things", this is the tool.

Consider whether you want a union at all. Sometimes the honest model is one type with optional fields, and sometimes two separate endpoints. A union in an API is a thing every client has to branch on, and the tag makes that branching possible &mdash; but fewer branches is still better than more.

## Left-to-right, when you actually want it

Smart mode is the default, and there is a second mode for the cases where you want the older behaviour:

```python
value: Union[int, str] = Field(union_mode="left_to_right")
```

Now members are tried strictly in order and the first success wins, with no exact-match pass first. That is occasionally what you want &mdash; a deliberate preference order, where you would rather have an `int` if the value can possibly be one.

It is worth knowing this exists mainly so that you recognise the behaviour when reading v1 code, which worked this way always. A union in an old codebase may be relying on order in a way that quietly changed meaning during the v2 migration.

## The performance argument

There is a cost to a plain union that is easy to overlook.

Validating against `Union[A, B, C, D]` may mean attempting up to four validations, each of which builds errors before failing. For a list of a thousand items, a union whose correct member is usually last is doing four times the necessary work and discarding three quarters of it.

A discriminated union does one dictionary lookup and one validation. For large collections of polymorphic data &mdash; an event log, a feed, a batch of webhook payloads &mdash; that difference is measurable rather than theoretical.

So the tag is not only about correctness and error quality. It is also the fast path.

## Nullable unions and the shape of Optional

`Optional[X]` is `Union[X, None]`, and it is the one union that never causes ambiguity, because nothing converts to `None` and `None` converts to nothing.

That is worth stating because it explains why `Optional` feels different from other unions even though it is not special. It is not that Pydantic treats it differently; it is that its members cannot overlap.

A related shape that does need care: `Optional[Union[A, B]]`, or equivalently `Union[A, B, None]`. The `None` part is unambiguous; the `A` versus `B` part has all the problems described above. Adding a discriminator still works &mdash; `None` is handled separately from the tagged members &mdash; so a nullable discriminated union is a perfectly good thing to write.

## Migrating a plain union to a tagged one

If you have an existing union that is misbehaving, the change is usually additive rather than breaking.

Add a `kind` field with a `Literal` to each member and give it a default matching that member's tag:

```python
class Video(BaseModel):
    kind: Literal["video"] = "video"
```

Existing code that constructs `Video(...)` without a tag keeps working, because the default fills it in. Existing *data* without the tag will now fail validation, which is the part to plan for &mdash; either a migration that adds the field, or a `model_validator(mode="before")` that infers the tag from the shape for a transition period.

The inference validator is a useful trick and a temporary one. It looks at which fields are present, decides what the payload must be, and writes the tag in. Keep it until the old data is gone, then delete it, because it is exactly the guessing that the discriminator was introduced to remove.

## Unions in the schema

A plain union becomes `anyOf` in JSON Schema: a list of alternatives with nothing to say how a consumer should choose between them. A generated client will typically produce a type that could be any of them and leave the disambiguation to whoever calls it.

A discriminated union becomes `oneOf` with a `discriminator` object naming the property and mapping its values to schemas. Tooling understands this: generated clients produce a proper tagged type, documentation groups the variants and shows which tag selects which, and validators on the other side can check the same rule you check.

If your API is consumed by generated clients, this alone is a strong reason to tag every polymorphic field. The difference between the two client types &mdash; one you have to narrow by inspection, one that narrows itself &mdash; is felt by every consumer on every call.

## A checklist

If the members are a fixed set of *kinds* of thing, tag them.

If the data already has a `type`, `kind` or `event` field, you have a tag; tell Pydantic about it.

If the members are simple, disjoint scalar types, a plain union is fine.

If you are relying on the order you wrote the members in, stop and add a tag, because that dependency is invisible to the next reader.

And if you cannot find a natural tag, consider whether the union is really modelling one thing with optional parts, which is often what a hard-to-tag union turns out to be.

## What the tag is really doing

A discriminated union works because it moves a decision from inference to declaration.

Without a tag, something has to work out what a payload is by looking at what it contains. That is guessing, however carefully implemented, and guessing has a failure mode where it is confidently wrong. With a tag, the payload states what it is and validation checks that claim against one schema.

That is a pattern well beyond Pydantic. Any time a system decides what something is by examining its shape, adding an explicit marker makes the system simpler, faster and more honest about its failures. The discriminator is the version of that idea you get for one line of annotation.

## Before you reach for a union

One question worth asking first: is this really several shapes, or one shape whose fields vary?

A union of two models that share nine of their ten fields is usually the second thing wearing the costume of the first. One model with an optional field is simpler to write, simpler to consume and simpler to document.

Reach for a union when the alternatives are genuinely different &mdash; different required fields, different meaning, different handling downstream. When they are the same thing with a variation, model the variation.

## Next

Unions choose between shapes. The next module is about choosing between *values*: enums and literals, which are how you say a field may only ever hold one of a small fixed set.
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

`track: str` allows every string ever written. Your application allows four. That gap is where invalid data lives, and closing it is one of the highest-value constraints available &mdash; a misspelt category is a bug that survives for months because nothing rejects it.

There are two good ways to close it, and one common bad one.

## Literal

```python
track: Literal["maths", "python", "dsa", "ml"]
```

The permitted values are written where the type goes. Anything else raises, with an error that lists the options.

It is the smallest thing that works, it needs no imports beyond `typing`, and mypy understands it &mdash; so your own code gets checked against the same set. A comparison against `"mathematics"` is flagged by your editor before it ever runs.

## Why not a regular expression

`Field(pattern=r"^(maths|python|dsa|ml)$")` enforces the same rule. It is worse in four distinct ways, and they are worth listing because the pattern approach is common.

**The error.** A `Literal` says the input should be one of a list, and gives the list. A pattern says the string should match a regular expression, and prints the expression. One of those is usable by a person who did not write your code.

**The schema.** A `Literal` becomes `enum` in JSON Schema. Documentation renders it as a set of choices, a generated client offers a type with four options, a form builder makes a dropdown. A `pattern` becomes a `pattern`, and every tool downstream shrugs.

**Static checking.** Mypy knows the four values of a `Literal` and will tell you when a comparison can never be true. It has no idea what a regular expression permits.

**Maintenance.** Adding a fifth track means editing a regular expression, which is a place people make mistakes, versus adding a word to a list.

The only case for a pattern is a set that is genuinely open &mdash; a format rather than a list. Slugs, postcodes, identifiers. If you can enumerate the values, enumerate them.

## Enum

An `Enum` gives the set an identity:

```python
class Track(str, Enum):
    MATHS = "maths"
    PYTHON = "python"
    DSA = "dsa"
```

Three things follow that a `Literal` does not give you.

**A name to refer to.** `Track.MATHS` instead of `"maths"` in the code that consumes the model. That means a typo is an `AttributeError` at import rather than a comparison that quietly returns `False`.

**One definition.** The set exists once and is used by every model that needs it. A `Literal` written out in four models is four copies &mdash; though `Annotated` fixes that, and a named `Track = Literal[...]` alias is a perfectly good middle ground.

**Somewhere to put behaviour.** A display label, a colour, an ordering, a `from_legacy_name` classmethod. Enums can have methods and properties, and that is often exactly where that logic belongs.

## The str mixin is not optional

Write `class Track(str, Enum)`, not `class Track(Enum)`, unless you have a specific reason.

Without the mixin, members are not strings. `Track.MATHS == "maths"` is `False`, which breaks every comparison in code that does not know about the enum. `json.dumps` refuses them. String formatting produces `Track.MATHS` rather than `maths`.

With the mixin, members *are* strings with extra structure. Every comparison works, serialisation is plain text, and code that was written before the enum existed keeps working.

Python 3.11 added `StrEnum`, which is the same idea with a cleaner spelling. Either is fine; the plain `Enum` is the one to avoid.

## What comes out when you dump

This trips people up, so it is worth being explicit.

`model_dump()` returns Python objects, so an enum field comes back as the enum member. That is usually what you want inside your program.

`model_dump(mode="json")` and `model_dump_json()` convert members to their values, because JSON has no enums. So the wire format is the plain string either way.

With the `str` mixin the distinction rarely bites, since the member behaves like its value anyway. Without it, a member reaching `json.dumps` raises, and that is the shape of the bug.

## Literals do more than strings

Any hashable literal works: `Literal[1, 2]`, `Literal[True]`, `Literal[None]`, and mixtures.

`Literal[1, 2]` for a version field is a genuinely good pattern &mdash; it makes a payload's supported versions explicit and rejects an unsupported one at the boundary with a clear message, rather than somewhere deep in code written for version 1.

One thing to know, because it differs from a plain `int` field: a `Literal` compares the value as given rather than parsing it first. `Literal[1, 2]` given the string `"2"` raises `literal_error`, where `minutes: int` would happily have converted it. If a version number arrives from a query string as text, annotate it `int` and constrain it, or convert before validating.

## The one place Literal is required

A discriminated union reads its tag from a `Literal` field. Nothing else will do &mdash; not a `str` with a default, not an `Enum` member as a default &mdash; because the mechanism needs the value known at class-definition time to build the lookup table.

So if you are writing polymorphic models, `Literal` is not a stylistic choice. It is the mechanism.

## Choosing

Reach for **`Literal`** when the set is small, local, and does not need behaviour. A status field used by one model, a discriminator tag, a version number.

Reach for **`Enum`** when the set is part of your domain vocabulary, is used in several places, or wants methods. Anything you would find yourself writing a constants module for.

Reach for a **named `Literal` alias** &mdash; `Track = Literal["maths", "python"]` &mdash; when you want reuse without the ceremony of a class. It is underused and it is often exactly right.

And avoid a bare `str` with a comment listing the allowed values. That comment is a schema that nothing enforces, and it will be wrong within a year.

## Migration, briefly

One practical warning. Adding a value to a `Literal` or `Enum` is safe. Removing one is a breaking change for anyone who has stored the old value, and validation will start rejecting data that was previously fine &mdash; including rows already in your database.

The usual fix is to keep the old value accepted, mapped to something sensible in a validator, for as long as old data exists. It is worth thinking about before you tighten a set that has been open for a while.

## Named literal aliases

There is a middle option between an inline `Literal` and a full `Enum` that deserves more use than it gets:

```python
Track = Literal["maths", "python", "dsa", "ml"]

class Module(BaseModel):
    track: Track

class Lesson(BaseModel):
    track: Track
```

One definition, reused, with no class to write and no `.value` to remember. Mypy narrows it in your own code, and the schema still gets a proper enumeration.

It is the right answer surprisingly often. The reason to reach past it for a real `Enum` is behaviour &mdash; a label, an ordering, a lookup &mdash; or the ergonomics of `Track.MATHS` over the bare string. If you need neither, the alias is less machinery for the same result.

## Enums in the schema

Both spellings produce an `enum` in JSON Schema, but they differ in one useful way.

A `Literal` inlines the values into the field. An `Enum` produces a named definition in `$defs` that the field references, so a set used by six fields appears once and is referenced six times.

That matters for generated clients. A referenced definition typically becomes a named type in the target language &mdash; a TypeScript union alias, a Java enum &mdash; which is reusable on the consumer's side too. Inlined values become six anonymous unions that happen to have the same members.

So for a set that appears in more than a couple of places in a public API, an `Enum` gives your consumers a better artefact, not just you.

## Defaults and the two spellings

A small ergonomic difference worth knowing.

With a `Literal`, the default is the value: `track: Track = "maths"`.

With an `Enum`, the default is normally the member: `track: Track = Track.MATHS`. The string also works, because validation coerces it, but the member reads better and is checked by your editor.

One caution with enum defaults: `= Track.MATHS` is evaluated once at class-definition time, which is fine because enum members are singletons and immutable. This is one of the few mutable-looking defaults that is genuinely safe.

## Extending a set safely

Adding a value is backwards compatible for the producer and not always for the consumer.

Your model will accept the new value immediately. Every client that has generated a type from your schema will not, until they regenerate &mdash; and a strict client may reject a response containing a tag it has never heard of.

This is a real API design consideration rather than a Pydantic one, and the usual mitigations are: version the endpoint, document that the set is open to extension so clients build tolerant parsers, or introduce the new value behind a flag until consumers have caught up.

Removing a value is worse and worth stating plainly: it will start rejecting data you have already stored. If a `track` column contains `"legacy"` and you remove it from the enum, every read of those rows now raises. The safe path is to keep accepting the old value, map it in a validator, and only remove it once the data is gone.

## Where an enum is the wrong shape

Two cases where reaching for an enum causes more trouble than it prevents.

**A set that genuinely changes at runtime.** Categories a user can create, tags from a database, anything editable through an admin interface. An enum is fixed at import; a set that changes needs a validator that checks against the current list, and that check belongs in the layer that can see the list.

**A set with hundreds of members.** Country codes, currency codes, timezone names. Technically an enum works; practically the schema becomes enormous, the generated client becomes enormous, and the error message lists three hundred options. A pattern plus a lookup is kinder to everybody.

The rule of thumb: enumerate when the set is small, stable and part of your domain's vocabulary. Otherwise validate membership another way.

## Summary

`Literal` for small, local sets and for discriminator tags. A named `Literal` alias when the same small set is used in a few places. `Enum` when the set is domain vocabulary, needs behaviour, or appears across a public API where consumers benefit from a named type. `str, Enum` always, never a bare `Enum`. And never a bare `str` with a comment.

## The underlying point

A closed set is one of the few pieces of domain knowledge that a type system can hold completely.

Most rules are approximations &mdash; a length bound, a range, a pattern that permits things you would reject. "This field is one of these four values" is exact. There is nothing left over, no edge case, no judgement call. Writing it down as a `Literal` or an `Enum` captures the entire truth about that field.

That is why it is worth the small effort of not writing `str`. You get an exact error, a schema a client can render, a static check on your own comparisons, and a definition that cannot drift from the code that uses it &mdash; all from choosing a more specific annotation than the one that would have worked.

## A last practical note

When you add an enum to an existing field, run your data through it before you deploy.

A `str` field that has been accepting anything for a year almost certainly contains values nobody expected &mdash; a trailing space, a different case, an old name from before a rename, a placeholder somebody typed once. Every one of those will start raising the moment the annotation tightens.

Finding them beforehand is a short script and an afternoon. Finding them afterwards is an incident, because the failures arrive on reads of existing data rather than on new input, which is the direction nobody tests.

## Next

The next module covers the types Pydantic already knows how to parse for you &mdash; dates, times, UUIDs and decimals &mdash; and the traps in each, particularly the two that cost money: floats and timezones.
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

JSON has six types: string, number, boolean, null, array and object. Your domain has more. Dates, timestamps, durations, identifiers, money &mdash; none of them exist on the wire, and all of them arrive as strings or numbers that have to be turned back into something useful.

That conversion is tedious, easy to get subtly wrong, and Pydantic already does it. Knowing exactly what it accepts saves writing the parsing, and knowing where the traps are saves the bugs.

## Dates and times

`date` accepts a `date`, an ISO string like `"2026-08-26"`, and a Unix timestamp &mdash; but only one that lands exactly on midnight. A timestamp with a time component raises `date_from_datetime_inexact`, on the reasoning that silently discarding the time would lose information you might have needed.

`datetime` accepts a `datetime`, an ISO 8601 string with or without an offset, and a Unix timestamp as an int or float. Both `"2026-08-26T14:30:00"` and the space-separated variant work, and so does a trailing `Z`.

`time` accepts `"14:30"` and `"14:30:00.123"`.

`timedelta` accepts a number of seconds or an ISO 8601 duration such as `"PT1H30M"`.

The pattern is the one from the coercion module: the type itself always works, and the obvious textual form works. What you get back is a real object, so `.year`, `.weekday()` and arithmetic all work without you having called `strptime` anywhere.

## The timezone trap

This is the first of the two expensive ones.

A `datetime` string without an offset produces a **naive** datetime &mdash; one with no `tzinfo`. A string with an offset produces an **aware** one. Both are valid `datetime` objects and both pass a `datetime` annotation.

They cannot be compared. `naive < aware` raises `TypeError`. Subtracting one from the other raises. So a model that accepts both will work perfectly until the day a client sends the other kind, and then fail somewhere entirely unrelated to the model.

The fix is to be explicit in the type:

```python
from pydantic import AwareDatetime

updated_at: AwareDatetime
```

Now a naive string is rejected at the boundary, with a clear message, at the point the bad data arrived. `NaiveDatetime` exists for the opposite requirement.

The general advice for anything with users in more than one place: store and transmit UTC with an explicit offset, use `AwareDatetime` in your models, and convert to local time only at the moment of display. A system that is consistently aware has no timezone bugs; a system that is inconsistently aware has nothing but.

## Money is not a float

This is the second expensive trap, and it is not a Pydantic quirk &mdash; it is how binary floating point works.

`0.1 + 0.2` is not `0.3` in any language using IEEE 754, because `0.1` cannot be represented exactly in binary any more than one-third can be in decimal. The error is tiny and it accumulates, and financial code that accumulates errors eventually produces a total that is a penny out and an afternoon nobody enjoys.

`Decimal` represents decimal fractions exactly. But the conversion matters enormously:

```python
Decimal(0.1)     # 0.1000000000000000055511151231257827
Decimal("0.1")   # 0.1
```

By the time a float exists, the information is already lost. Passing it to `Decimal` faithfully preserves the wrong number.

So money should travel as a **string** in JSON, and be validated as `Decimal`. That is why so many payment APIs quote amounts as `"12.50"` rather than `12.50`, and it is a convention worth adopting rather than fighting.

If a float is unavoidable on the way in, be aware that you have already lost exactness and any quantisation is damage control, not a fix.

## Constraining a decimal

Two constraints exist for decimals specifically:

```python
amount: Decimal = Field(gt=0, max_digits=8, decimal_places=2)
```

`decimal_places=2` rejects `"12.505"`. `max_digits=8` bounds the total number of significant digits. Together they express "a currency amount" far better than any `float` annotation can, and they appear in the schema.

This is also a good example of a constraint carrying domain meaning. `decimal_places=2` is a statement that this system deals in whole pence, which is a real decision that would otherwise live only in whoever's head made it.

## UUIDs and paths

`UUID` accepts a `UUID` or its string form, and rejects anything that is not a valid UUID &mdash; which is a genuinely useful check, since an id from an untrusted source is a common injection vector when it is treated as an opaque string.

What you get back is a real `UUID`, so `.version` and `.hex` work. Note that `model_dump()` gives you the `UUID` object and the JSON forms give the string, which matters if you pass the dump to something expecting text.

`Path` accepts a string and gives you a `pathlib.Path`, with `.suffix`, `.parent` and the rest. A caution: validating something as a `Path` does not make it safe. It does not check the path exists, and it certainly does not prevent `../../etc/passwd`. Path traversal is a security check you still have to write.

`EmailStr` deserves a mention because people look for it: it exists, but it lives in a separate package (`email-validator`) that must be installed. Without it, a plain `str` with a pattern is the pragmatic option &mdash; and worth remembering that no regular expression genuinely validates an email address. The only real check is sending a message to it.

## What comes out

Because none of these types exist in JSON, serialisation has to convert them, and the mode decides whether it does.

`model_dump()` returns Python objects: a `date` stays a `date`, a `Decimal` stays a `Decimal`. Right for passing data within your program.

`model_dump(mode="json")` returns JSON-compatible values: dates become ISO strings, decimals become strings, UUIDs become strings.

`model_dump_json()` returns the JSON text directly.

The mistake worth avoiding is `json.dumps(model.model_dump())`. That passes `date` and `Decimal` objects to a serialiser that cannot handle them, and raises `TypeError: Object of type date is not JSON serializable` &mdash; a confusing error, since the model clearly supports JSON. Use `model_dump_json()`, or `model_dump(mode="json")` if you need the dict first.

## A checklist for these types

Use `AwareDatetime` rather than `datetime` for anything that crosses a timezone boundary, which in practice means anything with users.

Use `Decimal` with a string input for money, always, and add `decimal_places`.

Use `UUID` rather than `str` for identifiers that are UUIDs &mdash; the validation is free and catches malformed input at the door.

Use `date` rather than `datetime` when there is no time, because a date that is secretly midnight in some timezone is a bug waiting for a daylight-saving transition.

And use `model_dump_json()` rather than assembling JSON yourself, so the conversions happen where they are already correct.

## Formatting on the way out

Pydantic serialises dates and datetimes as ISO 8601, which is the right default and is not always the format a consumer wants.

Changing it is a field serialiser, which is the next tier's material, but the shape is short:

```python
@field_serializer("published_on")
def show_date(self, value: date) -> str:
    return value.strftime("%d %B %Y")
```

Worth a word of caution though. A model that serialises dates in a human format is producing display output, and display formatting usually belongs in the layer that knows the reader's locale rather than in the data model. For an API, ISO 8601 is almost always the correct answer and the consumer formats it.

The one common exception is a date-only field where the ISO string is already right and the concern is the *type* &mdash; making sure a `date` does not accidentally serialise as a full datetime with a spurious midnight. Using `date` rather than `datetime` handles that at the source.

## Timestamps, seconds and milliseconds

A practical trap when accepting Unix timestamps: JavaScript's `Date.now()` returns **milliseconds**, and most of the rest of the world uses **seconds**.

Pydantic assumes seconds. Hand it a millisecond timestamp and you get a date tens of thousands of years in the future, validated happily, because it is a perfectly valid datetime.

There is no way for the library to know which you meant, so the check is yours. A constraint on the datetime range is the cheapest guard:

```python
updated_at: AwareDatetime = Field(le=datetime(2100, 1, 1, tzinfo=timezone.utc))
```

Anything from a millisecond timestamp fails that immediately and obviously, at the boundary, rather than appearing in a report as the year 57,000.

## Decimals and JSON output

`Decimal` serialises to a JSON **string** by default, not a number. That is deliberate and it is correct: a JSON number is a float to most parsers, so writing `12.50` as a number would hand the receiving end the same inexactness you used `Decimal` to avoid.

It does mean a consumer expecting a number gets a string, which occasionally surprises people integrating with an existing client. The answer is nearly always to fix the client rather than the serialisation &mdash; but if you must emit a number, a field serialiser can do it, and you should be aware you are choosing convenience over exactness.

The same reasoning explains why money should arrive as a string. A payload that sends `"12.50"` and validates it as `Decimal` is exact from end to end. One that sends `12.50` as a JSON number has already lost the guarantee before your model saw it.

## Comparing and storing

Two habits that prevent most date bugs downstream.

**Store UTC, display local.** Convert at the edges only. A system where everything internal is UTC with an explicit offset has no ambiguity anywhere; one that stores local times has an unanswerable question every time the clocks change.

**Use the narrowest type.** If a field is genuinely a date, annotate it `date`, not `datetime`. A `datetime` standing in for a date carries a time that means nothing, and that meaningless midnight will eventually be shifted by a timezone conversion into the previous day. Choosing `date` makes that impossible rather than unlikely.

## A quick reference

`date` &mdash; ISO string, or a timestamp landing exactly on midnight.

`datetime` &mdash; ISO string with or without offset, or a Unix timestamp in seconds. Prefer `AwareDatetime`.

`time` &mdash; `"14:30"` or `"14:30:00.123"`.

`timedelta` &mdash; seconds as a number, or an ISO duration like `"PT1H30M"`.

`Decimal` &mdash; a string, always, for anything financial. Constrain with `decimal_places`.

`UUID` &mdash; the UUID or its string form; invalid strings are rejected.

`Path` &mdash; a string; note that validation says nothing about safety or existence.

None of these exist in JSON, so all of them are strings on the wire, and `model_dump_json()` is the thing that knows how to make them.

## Why these traps are expensive

The two traps in this module &mdash; naive datetimes and floats for money &mdash; share a shape worth recognising, because it is the shape of most expensive bugs.

Neither fails at the point of the mistake. A naive datetime validates perfectly and sits in the model until something compares it to an aware one, possibly weeks later, in a different module, written by somebody else. A float price validates perfectly and is exactly right for every value anyone tests with, and wrong by fractions of a penny in aggregate.

That delay is what makes them costly. A bug that raises immediately costs minutes. A bug that produces plausible wrong answers costs however long it takes for somebody to notice the totals do not reconcile, plus the work of finding out why.

Annotating `AwareDatetime` and `Decimal` moves both failures to the boundary, where they are named, located and cheap. That is the same argument as the whole library, applied to the two types where getting it wrong costs the most.

## The general lesson

Every type in this module exists because JSON is poorer than your domain, and the gap has to be closed somewhere.

Closing it in the model means the conversion happens once, in a place that is declared, tested and visible in the schema. Closing it in the consuming code means it happens everywhere, differently, and one of those places will forget the timezone or the decimal places.

Choosing the precise type is not pedantry. It is deciding that the gap gets closed at the boundary rather than scattered through everything downstream.

## Next

That completes the shapes. The last module in this tier returns to coercion with a sharper question: now that you know what Pydantic will convert, when should you stop it?
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

Everything in this tier has assumed lax mode, which is the default: convert anything with an unambiguous reading, refuse the rest.

That is exactly right at a boundary. A query string is text. A form post is text. A CSV is text. If validation refused everything that was not already the right Python type, the code in front of every model would be a pile of `int()` calls in `try` blocks, which is the code the library exists to delete.

It is exactly wrong three layers in. If a function inside your own system passes a string where an integer was expected, that is a bug you wrote. Converting it silently means the bug survives, and the symptom appears somewhere else &mdash; usually as a number that is subtly wrong rather than an error that names the cause.

Same behaviour, opposite value, depending on which side of the boundary you are standing on. Which is why the setting exists.

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

Or as a reusable type, which is generally the nicest:

```python
UserId = Annotated[int, Field(strict=True)]
```

Pydantic also ships `StrictInt`, `StrictStr`, `StrictBool` and `StrictFloat`, which are the same thing pre-named.

## Per field is the usual answer

Whole-model strictness sounds tidy and is often impractical, because a real payload mixes fields that arrive as text with fields that do not.

The narrower need is much more common: be lax about most of a model and exact about the one or two fields where a quiet conversion would be dangerous.

**Identifiers** are the classic case. A `user_id` arriving as `"42"` rather than `42` usually means something upstream lost a type &mdash; a JSON serialiser configured oddly, a value that went through a URL and was never converted back. Accepting it papers over that. Refusing it tells you where the problem is while it is still cheap to find.

**Money** is the other. A `Decimal` field that accepts a float will accept an already-inexact value and validate it happily, which is the worst possible outcome for a currency amount.

**Booleans** are worth considering too. `bool` is generous in lax mode &mdash; `"yes"`, `"on"`, `"t"` all work &mdash; and that is genuinely useful for a checkbox and genuinely alarming for a flag that controls whether money moves.

## What strict still allows

Strict does not mean "no conversion whatsoever", and the exceptions are principled.

An `int` is still accepted for a `float` field, because widening an integer to a float loses nothing and Python treats the two as numerically compatible throughout.

A `bool` is still accepted for an `int` field, because `bool` genuinely is a subclass of `int` in Python. That one occasionally surprises people, and if it matters, a validator is the way to exclude it.

What strict removes is **parsing** &mdash; turning text into something else. `"3.0"` to a float is parsing, and strict refuses it.

## Strict and JSON

There is a subtlety worth understanding, because it looks like an inconsistency and is not.

In strict mode, validating from a JSON string still accepts the textual forms JSON has no alternative to. A `date` field validated from JSON accepts `"2026-08-26"`, because JSON has no date type and there is no stricter form available.

Validated from Python, the same strict model refuses that string, because in Python a real `date` object *was* available and a string means somebody skipped a step.

The principle is consistent once stated: strict mode refuses *unnecessary* conversion. When the format offers no alternative, accepting the only available representation is not laxity.

This is one more reason `model_validate_json` is worth preferring over `json.loads` plus `model_validate`. It knows the input was JSON and applies the right rules; going via Python objects loses that context.

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

The boundary model absorbs the messiness of the wire. The interior model is a statement that everything past this point has been checked, and a mistake in your own code will be caught rather than converted.

Adding `frozen=True` to the interior model is a natural companion: validated data that only gets read has no reason to be mutable, and freezing it removes another class of question.

Whether this is worth two classes depends on the system. For a small application it is over-engineering, and one lax model is fine. For a large one with several layers and several teams, the strict interior model is a contract that catches real mistakes.

## A middle path

If two models feels like too much, there is a lighter version that gets most of the benefit: turn on `validate_assignment` and make the important fields strict.

```python
class Module(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    user_id: Annotated[int, Field(strict=True)]
    minutes: int
```

Now the payload can arrive as text and be converted, but the identifier must be right, and later assignments are checked rather than trusted. One class, and the two most common bug sources are closed.

## When to reach for strict

**Do** use it on identifiers, money, and any flag with consequences.

**Do** use it for interior models in a layered system, where wrong types indicate your own bugs.

**Do** use it in tests, where you want to assert on exactly what a function produced without coercion smoothing it over.

**Do not** use it on a public API's request model. Your clients send JSON, JSON sends text, and refusing `"12"` for a duration will generate support tickets rather than better data.

**Do not** reach for it as a general "safer" setting. Lax mode is not sloppy; it is the correct behaviour for the job it was designed for. Strictness applied indiscriminately just moves work back into your callers.

## Strictness in tests

There is a use for strict mode that has nothing to do with production, and it is one of the most valuable.

In a test, coercion can hide the thing you are asserting. A test that checks a function returned `minutes=12` will pass if the function returned `"12"` and the model converted it &mdash; so the test does not actually verify the behaviour it claims to.

Validating the result with a strict model closes that gap. The assertion becomes about the real type, and a function that starts returning strings fails the test rather than quietly relying on coercion downstream.

The same applies to fixtures. A fixture built with `minutes="12"` is not exercising the same code path as production data that arrives as an integer, and strictness makes that visible.

## What strict does not protect you from

Worth being clear about the limits, because "strict" sounds like a general safety setting and is not.

It does not check ranges. `StrictInt` accepts `-999999` happily; that is what `Field(gt=0)` is for.

It does not check meaning. A strict `str` accepts an empty string, a string of spaces, and a string containing a script tag.

It does not make a model safe to expose. Strictness is about types, not about authorisation, sanitisation or business rules.

And it does not remove the need to think about the boundary. A strict model at the edge of a public API does not make the API safer; it makes it harder to call correctly, which pushes the conversion into your consumers' code where you cannot see it.

## Reading the errors

Strict failures have their own error types, and recognising them saves a moment's confusion.

Where a lax model would report `int_parsing` for `"twelve"`, a strict model reports `int_type` for `"12"` &mdash; the message is about the *type* being wrong rather than the value being unparseable.

That distinction is genuinely useful in a log. `int_parsing` means somebody sent nonsense. `int_type` on a strict field means somebody sent a well-formed value in the wrong representation, which is usually a wiring problem in a caller rather than bad input from a user, and the two deserve different responses.

## A decision you can apply mechanically

For each field, ask where its value comes from.

**From a human, a form, a URL or a CSV** &mdash; lax. It is text, it will always be text, and refusing it moves work to the caller with no benefit.

**From another service's JSON** &mdash; lax for anything JSON has no type for, strict for identifiers. A partner sending `"user_id": "42"` is worth knowing about.

**From your own code, past the boundary** &mdash; strict. A wrong type here is your bug and you want it loud.

**From a test** &mdash; strict, so the assertion means what it says.

Applied field by field, that produces models that are permissive exactly where permissiveness helps and exact everywhere else &mdash; which is the whole point, and is not something a single global setting can express.

## The principle underneath

Both modes exist because validation answers a different question in different places.

At the boundary the question is "can I make sense of this?", and being generous is correct, because the sender had no better option than text.

Inside the question is "is this what I think it is?", and being generous is wrong, because the sender is you and a mismatch means something is broken.

Getting this right is mostly a matter of noticing which question you are asking. The setting is small; the habit of asking is the thing worth taking away.

## One more reason it matters

Coercion is the feature people are most suspicious of when they meet Pydantic and most dependent on within a week. That reversal is worth understanding, because it is the same reversal that makes the strict/lax choice feel difficult.

The suspicion is reasonable: a library that silently changes your data sounds like a library that will eventually change it wrongly. The dependence is also reasonable: the boundary really is made of text, and something has to do the converting.

What resolves it is that Pydantic's conversion is bounded by a rule you can state in one sentence &mdash; convert when the reading is unambiguous and nothing is lost &mdash; and that you can switch it off, per field, wherever that rule is not the one you want.

Very few libraries give you both the sensible default and the precise override. Knowing that the override exists, and where to apply it, is what turns coercion from something you tolerate into something you have decided about.

## Where to start if you are unsure

If this is a new codebase, the pragmatic default is: lax everywhere, plus `strict=True` on identifiers and money.

That combination takes ten seconds to apply, keeps every request model easy to call, and closes the two cases where a silent conversion most often indicates a real problem upstream. It is a better starting point than either extreme, and you can tighten specific fields later as you learn where your data actually goes wrong.

The one thing worth doing deliberately rather than by default is choosing, once, for each new field. Strictness applied by habit is no better than laxity applied by habit.

## Where tier two leaves you

You can now describe data with real shape: models inside models, collections with meaningful error paths, unions that say which branch they are, closed sets of values, and the standard-library types that JSON cannot carry. And you can decide, per field, how much conversion you are willing to accept.

What you cannot yet do is express a rule that no annotation can hold &mdash; a value that must be checked against another value, a field computed from the rest, a normalisation applied before checking. That is the next tier, and it starts with validators.

## Summary

Lax mode converts anything unambiguous and is correct at the boundary, because the boundary is text. Strict mode requires the annotated type and is correct inside, because a mismatch there is your own bug.

Set it per field rather than per model in most cases. Strict still permits lossless widening, and still accepts the string forms JSON has no alternative to. Identifiers, money and consequential flags are the fields where it earns its place first.
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
intro: Custom checks and normalisation, and exactly where in the pipeline they run.

## What is left after types and constraints

Annotations describe the kind of value. Constraints narrow it to a range, a length or a pattern. Between them they cover a great deal, and then they stop.

They cannot check membership of a set that lives in a database. They cannot normalise whitespace before checking a length. They cannot say "if this looks like a legacy identifier, convert it". They cannot express any rule whose logic is longer than a comparison.

`field_validator` is where those live. It is a classmethod that receives one field's value, and either returns a value or raises.

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

**`@classmethod` is required**, and it must sit *below* `@field_validator`. Decorators apply bottom-up, so this order gives `field_validator` a classmethod to register. Reversed, you get an error that does not obviously say what is wrong, and it is one of the most common mistakes people make with this API.

**Raise `ValueError`**, not `ValidationError`. Pydantic catches it, attaches the field's location, gives it the type `value_error`, and folds it into the same report as every built-in failure. Constructing a `ValidationError` yourself is awkward and unnecessary. `AssertionError` also works but is a poor choice, because `python -O` removes assertions and your validation would silently stop running.

**Return the value.** This is the mistake that bites hardest, because it fails quietly: a validator that checks and forgets to return sets the field to `None`. If a field mysteriously becomes `None` after you add a validator, this is why.

**Name the failure usefully.** The message goes to whoever sent the data. `"unknown track 'astrology'; try one of dsa, maths, ml, python"` is worth the extra few characters over `"invalid"`.

## Validation is also normalisation

Because the returned value becomes the field, a validator is the natural place to clean data.

Stripping whitespace, collapsing runs of spaces, lowercasing an identifier, deduplicating a list, normalising a phone number &mdash; all of these belong here, and doing them here means every consumer downstream gets the clean version. The alternative is normalising at each use site, where one place will forget.

There is a small config-level shortcut for the most common case: `str_strip_whitespace=True` in `model_config` strips every string field, which removes a lot of trivial validators in one line.

Be careful about how much you transform. A validator that substantially rewrites its input is doing work a reader will not expect from the annotation, and a caller may be surprised that what they sent is not what came back. Normalising whitespace is uncontroversial; silently correcting a misspelt category is not, and probably deserves to be an error instead.

## Several fields at once

The decorator takes multiple names:

```python
@field_validator("title", "summary")
```

And `"*"` applies to every field, which is occasionally useful for a cross-cutting concern &mdash; rejecting control characters, say &mdash; though a validator that runs on every field has to be careful, because it will receive values of every type.

`ValidationInfo`, the optional second argument, carries `field_name`, which is what lets one validator produce a message naming the specific field it was applied to.

## Seeing other fields, and the limit of that

`info.data` is a dict of the fields validated *before* this one:

```python
@field_validator("lessons")
@classmethod
def enough_time(cls, v, info):
    minutes = info.data.get("minutes")
```

Fields are validated in declaration order, so `minutes` is visible to `lessons` only because it is declared above it. Reorder the class and the validator silently stops seeing it.

That fragility is the reason to treat `info.data` as a convenience rather than the tool for cross-field rules. Use `.get()` rather than indexing, because a field that failed its own validation is simply absent, and a `KeyError` inside a validator is a much worse error than the one it was trying to report.

For any rule that genuinely depends on more than one field, `model_validator(mode="after")` is the correct tool. It runs once, after everything is populated, and it does not care what order the class was written in. That is the next module.

## Before and after

By default a validator runs in `mode="after"` &mdash; after coercion, so the value is already the annotated type. That is what you want for almost every rule, because you are checking a real `int` rather than something that might be a string.

`mode="before"` runs on the raw input, before Pydantic has tried anything. Its use is fixing the *shape* of data rather than the value:

```python
@field_validator("tags", mode="before")
@classmethod
def split_csv(cls, v):
    if isinstance(v, str):
        return [p.strip() for p in v.split(",")]
    return v
```

A caller sends `"maths,vectors"` where a list was wanted. In `after` mode you would never see it &mdash; validation would already have failed, because a string is not a list. In `before` mode you can convert it and let normal validation proceed.

Two rules for `before` validators. Accept whatever might arrive, since the value has not been checked and could be anything, so guard with `isinstance` rather than assuming. And pass through anything you do not handle, unchanged, so the normal path still runs.

## Validators and inheritance

Validators are inherited like any other classmethod, so a base model's rules apply to every subclass. That makes a base a good home for cross-cutting normalisation.

A subclass can override a validator by defining one with the same name, which replaces it entirely rather than adding to it. If you want both, give them different names &mdash; several validators can target the same field and they run in definition order.

## When not to reach for one

Three cases where a validator is the wrong answer.

**When a constraint would do.** `Field(gt=0)` and a validator that checks `v > 0` both reject the same values, but only the constraint appears in the JSON Schema. That means the documentation says the minimum, the generated client knows it, and a form can enforce it before a request is sent. A validator is invisible to all of that.

**When it needs I/O.** A validator that queries a database to check a foreign key turns validation into a network call, makes the model untestable without a database, and turns a validation error into a timeout. Keep models pure: they check data using only data. Existence checks belong in the layer that owns the storage.

**When it is really a type.** A validator enforcing membership of four strings should be a `Literal`. A validator checking a value is one of a set with behaviour should be an `Enum`. Both produce better errors and both appear in the schema.

## Several validators on one field

More than one validator can target the same field, and they run in definition order:

```python
@field_validator("slug")
@classmethod
def strip(cls, v): return v.strip()

@field_validator("slug")
@classmethod
def lower(cls, v): return v.lower()
```

Splitting rules like this is usually clearer than one function doing four things, and each has a name that says what it enforces. The name matters more than it looks &mdash; it appears in tracebacks and it is what a reader scans for when asking "where is the rule about slugs?".

The counter-argument is that a chain of tiny validators can obscure the order dependency between them. If step two only makes sense after step one, saying so in one function with two comments is honest; splitting them and hoping nobody reorders is not.

## What info carries

The optional second parameter is a `ValidationInfo`, and beyond `field_name` and `data` it has two more things.

`config` exposes the model's configuration, which lets a validator behave differently depending on, say, whether the model is strict.

`context` is arbitrary data you pass in at validation time:

```python
Module.model_validate(payload, context={"tenant": "acme"})
```

Inside a validator, `info.context` holds that dict. This is the supported way to give validation access to something external without reaching for a global &mdash; a tenant, a feature flag, a set of permitted values loaded once per request.

It is genuinely useful and easy to overuse. A model whose rules depend heavily on context is a model that cannot be understood on its own, and the checks may belong in a service instead.

## Reusing a rule across models

If two models need the same validator, do not copy it. There are two clean options.

Put it on a shared base model, so every subclass inherits it. Good when the models are genuinely related.

Or make it part of a type with `AfterValidator`, so the rule travels with the annotation rather than with the class. That is the `Annotated` module's subject, and it is usually the better answer when the models are unrelated but the field means the same thing in both.

Copying the same `@field_validator` into four classes is the thing both of those exist to prevent.

## Errors worth writing well

The message you raise is seen by whoever sent the data, and it is worth a moment's thought.

Include what was wrong and what would be right. `"unknown track 'astrology'; try one of dsa, maths, ml, python"` costs a few characters and saves a support message.

Do not include the value if it might be sensitive. The error report already carries `input`, and a message that also embeds a token puts it in a second place.

And keep the message about the data, not the code. `"validation failed in known_track"` tells the caller nothing they can act on.

## Summary

`field_validator` handles what annotations and constraints cannot: logic. It runs after coercion by default, receives one field, and whatever it returns becomes that field &mdash; which makes it as much a normalisation hook as a check.

Remember the four mechanics: `@classmethod` underneath, raise `ValueError`, always return, and use `mode="before"` only when you are fixing shape rather than value.

And reach for it second. Types first, constraints next, validators for what is left.

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

Two validators, two jobs, two modes. The first repairs the shape when a caller sends a string. The second normalises and deduplicates once the value really is a list.

Splitting them this way is deliberate. Doing both in a single `before` validator would mean the cleaning logic runs on unvalidated input and has to defend itself; doing both in `after` would mean the string never arrives. Each piece runs where its assumptions hold.

The result is a field that accepts `"Maths, maths, VECTORS "` or `["Maths", "maths", "VECTORS "]` and produces `["maths", "vectors"]` either way &mdash; and every consumer downstream gets the clean version without knowing any of this happened.

## The order to reach for things

Types, then constraints, then validators. Working down that list rather than up produces models where most rules are visible in the annotations and only the genuinely complex ones are in code &mdash; which is also the order of how much each rule tells your schema, your documentation and your consumers.

## Validators and the schema

Worth restating once more, because it is the trade this whole module sits inside.

A validator enforces a rule perfectly and tells nobody. The value is rejected, the caller gets an error, and every tool that reads your schema &mdash; documentation, generated clients, form builders, contract tests &mdash; remains unaware that the rule exists.

That is not an argument against validators. It is an argument for using them for what genuinely needs them, and for reaching first for the annotations and constraints that can say the same thing in a form other tools can read.

When a rule can only be a validator, consider describing it in the model's docstring, which becomes the schema's description. The rule still will not be machine-readable, but a human reading your documentation will at least know it is there rather than discovering it through a rejection.
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
intro: The checks a per-field validator structurally cannot make, and the two modes that make them.

## Why a field validator is not enough

A `field_validator` receives one value. That is the right shape for most rules, and it is structurally incapable of expressing a large and important class of them.

An end date must be after a start date. A discount must not exceed the price. Either an email or a phone number must be present. A waitlist only makes sense when every seat is taken. None of these is a statement about a single field &mdash; each field is individually fine, and it is the combination that is wrong.

`info.data` looks like a way round this, and it half is. It exposes fields validated *earlier*, which means the rule only works if the fields happen to be declared in the right order and silently stops working when somebody reorders the class for tidiness. That is not a foundation to build on.

`model_validator` is the tool built for the job.

## mode="after"

The common case. It runs once, after every field has been validated and converted, and receives the finished model:

```python
@model_validator(mode="after")
def ends_after_start(self):
    if self.ends_on <= self.starts_on:
        raise ValueError("ends_on must be after starts_on")
    return self
```

Three mechanics. It takes `self`, not `cls`, and is not a classmethod &mdash; which is the opposite of `field_validator` and catches people out. It must **return `self`**, and forgetting is the same silent failure as forgetting to return from a field validator. And by the time it runs, the fields are real Python objects, so `self.ends_on` is a `date` and comparing it works.

That last point is worth dwelling on. Because coercion has already happened, an after validator can compare, subtract and sort without any defensive conversion. The rule reads exactly like the sentence you would say out loud.

## The empty location

An error raised here has `loc: ()` &mdash; an empty tuple.

That is correct: the failure belongs to the object, not to any single field. There is no one input to highlight, because the problem is the relationship between two of them.

It is also the thing most likely to break error-handling code written before the first cross-field rule was added. Anything doing `err["loc"][0]` will raise `IndexError`, and it will do so the first time somebody adds a validator like this &mdash; long after the handler was written and tested.

Handle it explicitly. Group under a key like `"_form"`, and give the interface somewhere to display an error that is not attached to an input. Every form library has a concept for this; the model just needs to feed it.

## mode="before"

A before validator receives the raw input for the entire model, before any field has been looked at. It is a classmethod, and it returns the data that will then be validated normally.

Its main use is accepting a shape you did not design:

```python
@model_validator(mode="before")
@classmethod
def accept_old_shape(cls, data):
    if isinstance(data, dict) and "name" in data:
        data = dict(data)
        data["title"] = data.pop("name")
    return data
```

This is the translation layer for a legacy payload, a third-party API with different names, or a version of your own format you no longer want in the model. The model stays clean and describes the shape you want; the adapter sits in one visible place.

Two rules, both the same as for field-level before validators. Guard with `isinstance`, because the input has not been checked and may not be a dict at all. And copy before mutating &mdash; `dict(data)` &mdash; because modifying the caller's dictionary in place is a surprise nobody enjoys debugging.

Use `before` sparingly. It runs before everything, so any error it raises is reported without the field context that makes Pydantic errors useful, and complex logic there is hard to follow. For anything that is genuinely per-field, a field validator says more.

## Setting values, not just checking

An after validator can modify the model, which makes it a way to derive one field from others:

```python
@model_validator(mode="after")
def fill_slug(self):
    if self.slug is None:
        object.__setattr__(self, "slug", self.title.lower().replace(" ", "-"))
    return self
```

The `object.__setattr__` is needed on a frozen model and is harmless otherwise; on a mutable model a plain assignment works, though it will re-trigger validation if `validate_assignment` is on.

Before reaching for this, ask whether the value is ever legitimately supplied by the caller. If it is &mdash; a slug that defaults from the title but can be overridden &mdash; this is right. If it never is, and is always derived, then it is not really an input at all and `computed_field` is the better tool. That is the next module.

## Order, and short-circuiting

Several model validators can coexist, and they run in definition order. The first to raise stops the rest.

That has a practical consequence: put the cheap, foundational checks first. If `taken > seats` is nonsense, there is no value in also evaluating a rule about the waitlist that assumes those numbers make sense &mdash; and the second error would only confuse the caller.

It also means model validators do not accumulate errors the way field validation does. Field errors all appear together; model-level errors appear one at a time. If you want a caller to see every cross-field problem at once, you have to collect them yourself in a single validator and raise one error describing all of them.

## Keeping it pure

The strongest advice in this module: a model validator should decide using only the data in front of it.

The temptation is real. "Does this track exist?" is a validation question, and the answer is in a database. Putting the query in a validator makes it run on every construction, makes the model impossible to test without a database, turns a `ValidationError` into a possible timeout, and hides an I/O call somewhere nobody expects one.

The rule that keeps this clean: models check *shape and internal consistency*; the service layer checks *facts about the world*. A date range being backwards is shape. A track existing is a fact. They are different concerns and they fail differently &mdash; one is a 422, the other is arguably a 404.

## Choosing between the three tools

**A constraint** when the rule is a bound, a length or a pattern on one field. It reaches the schema.

**A field validator** when one field needs logic, or normalising.

**A model validator** when the rule involves more than one field, or the shape of the whole payload.

Working down that list rather than up produces models where most rules are visible in the annotations and only the genuinely complex ones are in code.

## Collecting several problems at once

Model validators stop at the first failure, which means a caller fixing cross-field errors discovers them one at a time &mdash; exactly the experience field validation avoids.

If several rules should report together, collect them in one validator:

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

It is less tidy than separate validators and it gives the caller everything in one response. Which matters depends on whether a human is fixing a form or a service is failing a request.

## Validators and assignment

With `validate_assignment=True`, after validators run again on every assignment.

That is usually what you want &mdash; a cross-field invariant should hold after a change, not only at construction. It has two consequences worth knowing.

An expensive validator now runs on every assignment, not once.

And an intermediate state may be invalid. Setting `starts_on` to a date after the current `ends_on` raises, even though you were about to fix `ends_on` on the next line. There is no transaction; each assignment is validated alone.

Where that bites, the functional approach is cleaner: build a new model with `model_copy(update={...})` giving both fields at once, or construct a fresh one. It is also a good argument for `frozen=True` on models with cross-field rules &mdash; if it cannot be mutated, it cannot pass through an invalid intermediate state.

## Inheritance

Model validators are inherited, so a base can carry an invariant that every subclass enforces.

A subclass redefining a validator with the same name replaces it. Give it a different name to have both, and remember that the parent's runs first.

This makes a base model a reasonable home for a rule shared across a family &mdash; "no model in this system may have an end before its start" &mdash; while each subclass adds its own.

## What belongs where, once more

The line worth holding, because it is the one people cross first.

A model validator answers: **is this object internally consistent?** Dates in order, totals adding up, at least one contact method present. All answerable from the data in front of it.

A service answers: **is this true of the world?** Does the track exist, is the name taken, does this user have permission. All requiring something the model cannot see.

Keeping that line means models are testable with plain data, validation cannot make a network call, and a `ValidationError` always means the payload was malformed rather than that something external was unavailable. Those are three properties worth protecting.

## Summary

`model_validator(mode="after")` takes `self`, returns `self`, and sees every field already converted &mdash; the right place for any rule about relationships between fields. `mode="before"` is a classmethod taking raw input, for translating a payload shape.

Model-level errors carry an empty `loc`, which your error handling needs to expect. Validators run in definition order and stop at the first failure. And keep them pure, so that validating a model never touches the world.

## A short checklist

Before writing one, three questions.

**Does the rule involve more than one field?** If not, a field validator or a constraint is more specific and gives a better error location.

**Can it be decided from the data alone?** If it needs a lookup, it belongs in the service layer, not here.

**Should the caller see every failure at once?** If so, collect them in a single validator rather than writing several that stop at the first.

## What this buys

A model with cross-field rules is a model that cannot exist in a nonsensical state. A cohort whose end precedes its start is not merely flagged somewhere &mdash; it cannot be constructed.

That is a strong guarantee, and it is what makes the rest of the codebase simpler. Every function receiving that model can stop checking, because the object could not have been built if the check would have failed. The rule exists once, at the boundary, instead of being re-asserted defensively wherever the data travels.


## Mistakes people make

**Using `info.data` in a field validator for a cross-field rule.** It only exposes fields declared earlier, so the rule works until somebody reorders the class for readability and then silently stops.

**Forgetting to return `self`.** The same silent failure as everywhere else in this library.

**Doing I/O.** A validator that queries a database makes the model untestable without one, turns a `ValidationError` into a possible timeout, and hides a network call somewhere nobody expects one.

**Writing several validators when the caller needs every failure at once.** Model validators stop at the first raise, so a form with three cross-field problems reveals them one at a time. Collect them into one validator when they should be reported together.

**Assuming `loc[0]` exists.** Model-level errors carry an empty `loc`. Error-handling code written before the first cross-field rule will raise `IndexError` the day one is added.

**Mutating in an after validator on a model with `validate_assignment`.** The assignment re-triggers validation, which re-runs the validator. Use `object.__setattr__`, or set the value in a `before` validator instead.

## Where the errors go

One practical consequence of the empty `loc` deserves a final mention, because it shapes how the front end has to work.

A field error can be rendered beside its input. A model error cannot &mdash; there is no single input it belongs to. Every form needs somewhere to display it: a banner above the fields, a summary at the top, a message near the submit button.

If that place does not exist, cross-field errors are either invisible or attached arbitrarily to whichever field the code happened to pick. Both are worse than a plain sentence in an obvious place.

It is a small piece of interface design that follows directly from a modelling decision, and it is easiest to get right by knowing it is coming.
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
intro: Values calculated from other fields that belong in the response but were never an input.

## The gap it fills

Some values are not data you receive; they are consequences of data you receive. A full name from a first and last. A total from a quantity and a price. A reading time from a word count. An `is_expired` flag from an expiry date and the clock.

Storing them as fields is wrong, because they can then disagree with the values they came from. Accepting them from a caller is worse, because the caller can lie.

The obvious answer is a `@property`, and it is half right. A property computes from the current values and cannot drift. But it is invisible to serialisation &mdash; `model_dump()` does not include it, `model_dump_json()` does not include it, and the schema does not know it exists. For a value that exists purely for internal use, that is fine. For one your API consumers need, it is not.

`@computed_field` closes the gap: the value is derived, and it appears in the output.

## The shape

```python
@computed_field
@property
def pace(self) -> float:
    return round(self.minutes / self.lessons, 1)
```

Three mechanics.

**Decorator order.** `@computed_field` goes above `@property`. The reverse does not work, and the failure is not self-explanatory.

**The return annotation is required.** It becomes the field's type in the serialisation schema, and Pydantic will complain if it is missing. It is not merely documentation.

**It reads the model.** Because it takes `self`, everything on the model is available &mdash; and validation has already happened, so those values are real converted types.

## Output only, and why that matters

A computed field is not an input. It does not appear in the constructor signature, it is not validated, and passing it is ignored &mdash; or rejected, if you have set `extra="forbid"`.

That asymmetry is the whole point. The value is a function of the model, so allowing it to be supplied would allow it to be supplied *wrongly*, and you would have two sources of truth for one fact.

It also means the value is always current. Change `minutes` and `pace` changes with it, because it is recomputed on access rather than stored. There is no stale-derived-value bug available, which is the class of bug this feature eliminates.

## The schema, and the two modes

A computed field appears in the **serialisation** schema and not the validation one, which is exactly right: it is something you emit, never something you accept.

That distinction surfaces in `model_json_schema(mode=...)`. The default, `mode="validation"`, describes what the model accepts, and computed fields are absent. `mode="serialization"` describes what it produces, and they are present.

For a FastAPI response model this is handled for you: the response schema is the serialisation one, so computed fields appear in the documentation as fields consumers can expect. That is usually the reason to reach for the feature in the first place.

You can pass `description`, `title` and `examples` to the decorator, and they land in the schema like any other field's metadata. A derived value often needs a description more than a stored one does, because the name alone rarely explains the formula.

## Excluding them

Computed fields behave like fields for `include` and `exclude`:

```python
m.model_dump(exclude={"cost_pence", "margin"})
```

This is worth knowing because derived values are frequently the ones you do not want in a public response. A margin computed from a cost is a perfectly reasonable internal field and an unfortunate thing to leak, and it is easy to forget that adding a computed field changes what every existing serialisation emits.

That is genuinely a footgun: unlike a normal field, which you had to add to the model deliberately, a computed field can be added for one internal purpose and silently appear in every API response the model feeds.

## The cost

A computed field runs on **every** serialisation. There is no caching.

For arithmetic on a couple of fields that is irrelevant. For anything heavier it is not, and the cost multiplies: serialising a list of a thousand models runs every computed field a thousand times.

If a value is expensive and genuinely needs to be in the output, compute it once and store it in a real field &mdash; accepting that you now own keeping it consistent. `functools.cached_property` is not a substitute here, because it does not participate in serialisation.

The rule: computed fields are for cheap derivations. Arithmetic, string formatting, a comparison, a lookup in a small dict. Anything that touches I/O or loops over data does not belong.

## The failure mode to guard against

This is the sharpest edge in the module, and it is easy to walk into.

A computed field that can raise turns a valid model into one that cannot be serialised.

```python
@computed_field
@property
def pace(self) -> float:
    return self.minutes / self.lessons     # lessons could be 0
```

`Module(minutes=30, lessons=0)` validates perfectly. Every field is the right type and within its constraints. And then `model_dump()` raises `ZeroDivisionError` &mdash; not a `ValidationError`, not at the boundary, but at the moment you try to send a response.

The failure is far from the cause and it is not a validation error, so none of the error handling you built for validation catches it.

Two defences. Make the impossible state impossible: `lessons: int = Field(gt=0)` means the divisor cannot be zero and the computed field cannot fail. Or handle the edge inside the property and return something sensible. The first is better, because it fixes the model rather than the symptom.

The general principle: a computed field should be **total** &mdash; defined for every combination of values the model permits. If it is not, either the model is too permissive or the value is not really a computed field.

## Computed field, property, or stored?

**Plain `@property`** when the value is for internal use and should not be serialised. Most helper methods on a model are this.

**`@computed_field`** when the value is derived, cheap, total, and consumers need it in the output.

**A stored field** when the value is expensive, when it must be preserved as it was at a point in time (a price at the moment of sale, not the current price), or when it genuinely is an input.

That middle case &mdash; historical values &mdash; is worth flagging. A computed field always reflects the *current* inputs. If you need what the total was when the order was placed, that is data, not a derivation, and it belongs in a column.

## Naming and the schema

A computed field's name is the method name, and it appears in the output exactly as written. That is worth a moment's care, because renaming it later is a breaking change for every consumer.

The return annotation is not optional, and it does real work: it becomes the field's type in the serialisation schema, so consumers and generated clients know what to expect.

A `description` in the decorator is more valuable here than on ordinary fields. `total` does not explain whether tax is included; `minutes` does not explain the margin applied. The name is a label, and derived values usually need a sentence.

## Serialisation aliases work too

Computed fields accept `alias`, which matters if the rest of your API is camelCase:

```python
@computed_field(alias="estimatedMinutes")
@property
def estimated_minutes(self) -> int:
    ...
```

Without it, a model whose ordinary fields are aliased will emit one stubbornly snake_case key among them. An `alias_generator` on the model does not apply to computed fields, so this is one place the whole-model convention needs a per-field top-up.

## Ordering in the output

Computed fields appear after regular fields in the serialised output, in the order they are defined.

That is stable and predictable, and worth knowing if anything downstream cares about key order &mdash; a snapshot test, a diff, a human reading a log. You cannot interleave them with declared fields.

## A pattern: flags derived from state

One of the most useful applications is turning internal state into a flag a consumer can act on:

```python
@computed_field
@property
def is_expired(self) -> bool:
    return self.expires_at < datetime.now(timezone.utc)
```

The consumer does not have to know your expiry rules, parse a date, or get the timezone right. They get a boolean.

Two cautions with this specific shape. It depends on the clock, so serialising the same model twice can produce different output &mdash; which breaks snapshot tests and can surprise a cache. And it makes the model's output non-deterministic, which is a property worth being deliberate about rather than discovering.

If determinism matters, pass the reference time in rather than reading the clock, or compute the flag in the layer that is producing the response.

## Summary of the trade

A computed field buys you a derived value in the output that can never disagree with its inputs, described in the schema, with no storage and no synchronisation.

It costs a function call on every serialisation, and it demands that the function be total &mdash; defined for every state the model permits &mdash; because a failure there breaks serialisation of an object that validated perfectly.

Cheap, total, and genuinely derived. Those three conditions are the whole rule.

## Summary

`@computed_field` above `@property`, with a return annotation. The value is derived, output-only, recomputed every time, and appears in the serialisation schema.

Keep them cheap, because they run on every dump. Keep them total, because a computed field that raises breaks serialisation of a model that validated perfectly. And remember that adding one changes the output of every serialisation the model already feeds &mdash; including the public ones.

## One more use worth knowing

A computed field is a good place to expose a value the model stores in a form consumers should not have to understand.

Storage often wants one shape and a consumer wants another: a duration in seconds internally, minutes in the response; a status code internally, a readable label outside; separate first and last names, a display name in the output.

The computed field bridges that without duplicating state. The stored field remains the single source of truth, and the derived view is guaranteed to agree with it because it is computed from it.

This is a better pattern than storing both, which is where the two eventually disagree and nobody can say which is right.


## Mistakes people make

**Writing one that can raise.** A division by a field that might be zero turns a perfectly valid model into one that cannot be serialised &mdash; and the failure is not a `ValidationError`, so none of your validation error handling catches it. Constrain the inputs so the impossible state cannot occur.

**Putting expensive work in one.** It runs on every serialisation with no caching, and serialising a thousand models runs it a thousand times. Anything touching I/O or looping over data does not belong.

**Forgetting the return annotation.** It is not documentation; it is the field's type in the serialisation schema, and Pydantic requires it.

**Reading the clock.** A field derived from `datetime.now()` makes serialisation non-deterministic, which breaks snapshot tests and surprises caches. Pass the reference time in, or compute the flag where the response is produced.

**Not aliasing it.** An `alias_generator` on the model does not reach computed fields, so a camelCase API ends up with one stubbornly snake_case key. The decorator takes `alias` for exactly this.

**Adding one without checking what already consumes the model.** Unlike a regular field, which you deliberately added to a schema, a computed field written for one internal purpose immediately appears in every existing serialisation &mdash; including the public ones.

## Deciding, in one line

Cheap, total, and genuinely derived.

Cheap, because it runs on every serialisation and there is no caching. Total, because a failure breaks the output of a model that validated perfectly. Genuinely derived, because if a caller could reasonably supply it, it is an input with a default rather than a computed value.

Fail any of those three and the answer is something else &mdash; a stored field, a plain property, or a value computed in the layer producing the response.
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
intro: Extra keys, mutability, assignment checking and string handling - the switches worth knowing.

## Where behaviour lives

Everything so far has been per field. `model_config` is per model: a `ConfigDict` assigned in the class body that changes how the whole thing behaves.

```python
class Module(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    title: str
```

In Pydantic v1 this was an inner `class Config`. That still works and is deprecated, and it is the clearest signal that a tutorial predates v2.

There are a lot of settings. These are the ones that come up constantly.

## extra: what to do with keys you did not declare

The default is `"ignore"` &mdash; unknown keys are silently dropped.

That is forgiving, and it hides mistakes. A caller sending `minuets` instead of `minutes` gets no error and no field; the model is built with whatever default `minutes` has, and the bug surfaces later as a value that is inexplicably wrong.

`extra="forbid"` rejects them:

```python
model_config = ConfigDict(extra="forbid")
```

Now the typo is an error naming the offending key. For an internal API, a config file, or anything where you control both ends, this is almost always the better default. It converts a silent misunderstanding into an immediate one.

The argument for `"ignore"` is forward compatibility on a public API: a client sending fields from a newer version should not break against an older server. That is a real consideration, and it applies to *your* API's request models rather than to every model in your codebase.

`extra="allow"` keeps unknown keys, storing them on the model and exposing them through `model_extra`. It is right for a genuine passthrough &mdash; a webhook body you forward, an envelope whose payload you do not own. Everywhere else it turns your model into a dictionary with extra steps, and loses the guarantee that the fields on the object are the fields you declared.

## Validation happens once

This surprises people, and it is worth being explicit about.

A model is validated when it is constructed. Assigning to an attribute afterwards is a plain Python assignment: no checking, no coercion.

```python
m = Module(minutes=8)
m.minutes = "not a number"      # allowed, and now the field is a string
```

The reasoning is speed &mdash; most models are built, read and discarded, and checking every assignment would be work for a case that rarely arises.

`validate_assignment=True` turns it on. Assignments are then validated and coerced like constructor arguments, so `m.minutes = "12"` gives you `12` and `m.minutes = "ages"` raises.

Turn it on for any model that is genuinely mutated after construction, especially one holding configuration or accumulating state. It costs a little per assignment and removes a class of bug where a model's declared types quietly stop being true.

Note that it also makes any `model_validator(mode="after")` run again on each assignment, which is usually what you want and is worth knowing if those validators are expensive.

## frozen: the other answer to mutation

`frozen=True` forbids assignment altogether. An attempt raises a `ValidationError` with type `frozen_instance`.

It also makes the model **hashable**, so it can be a dictionary key or a set member &mdash; which unlocks a lot of ordinary Python that mutable models cannot do.

For validated data that arrives from outside and is then only read, frozen is the right default and is under-used. It removes the question "did anything change this?" entirely, it makes the object safe to share across threads or pass anywhere without defensive copying, and it makes the intent explicit.

`model_copy(update={...})` still works on a frozen model, so producing a modified version is one line. That is the functional-update pattern, and it is usually clearer than mutation anyway.

Individual fields can be frozen with `Field(frozen=True)` when only part of the model should be fixed &mdash; an id that must never change while the rest of the record can.

## String settings for human input

Three settings that apply to every string field:

`str_strip_whitespace=True` strips leading and trailing whitespace. For form data this is nearly always correct, and it removes a pile of one-line validators.

`str_to_lower=True` and `str_to_upper=True` normalise case. Useful for emails, codes and identifiers; wrong for anything with display text, so apply it to models that are all identifiers rather than reaching for it globally.

`str_min_length=1` sets a floor for every string. Combined with stripping, this is the compact way to say "no blank strings anywhere in this model", which is a rule most form models want and few state.

## from_attributes: reading objects

By default `model_validate` expects a mapping. `from_attributes=True` lets it read attributes off any object:

```python
class ModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    minutes: int

ModuleOut.model_validate(orm_row)
```

This is how a model turns a database row into a response, and it recurses, so a row with related objects becomes nested models without any manual conversion.

It was `orm_mode` in v1, which is the name most existing material uses.

Two cautions. It reads attributes, so a lazy-loading ORM relationship will be *loaded* when the model touches it &mdash; which is how a single serialisation quietly becomes fifty queries. And it will read any attribute matching a field name, so a model with a field called `password_hash` pointed at a user row will faithfully put the hash in your response. Output models should list only what may be seen.

## A few more worth knowing

`populate_by_name=True` lets a field be filled by either its alias or its Python name. It pairs with aliases and gets a module of its own next tier.

`use_enum_values=True` stores the value rather than the enum member. It makes dumps simpler and loses the member's behaviour; usually the `str, Enum` mixin is the better answer.

`validate_default=True` checks default values, which are otherwise trusted.

`arbitrary_types_allowed=True` permits fields of types Pydantic knows nothing about, validated only by `isinstance`. It is an escape hatch for wrapping a third-party object, and a sign you might want a custom type instead.

## Config is inherited

A base model's config applies to every subclass, and a subclass can override individual settings.

That makes a house base model a genuinely good pattern:

```python
class Base(BaseModel):
    model_config = ConfigDict(extra="forbid",
                              str_strip_whitespace=True,
                              validate_assignment=True)
```

Every model in the codebase inherits from it and gets the same defaults, decided once. It is much better than the same `ConfigDict` copied into forty classes, four of which will end up different for no reason anybody remembers.

## Suggested defaults

For **request models** on a public API: `extra="ignore"` for forward compatibility, `str_strip_whitespace=True`.

For **internal and config models**: `extra="forbid"`, so a typo is an error rather than a mystery.

For **validated data that is then only read**: `frozen=True`.

For **anything mutated after construction**: `validate_assignment=True`.

## Settings that catch mistakes

Three more worth knowing because each closes a specific hole.

`validate_default=True` checks default values, which are otherwise trusted. A mistyped default sits silently until something downstream does arithmetic on a string. Worth turning on for models whose defaults come from constants defined elsewhere.

`revalidate_instances="always"` re-validates a model instance passed into another model. By default an object that is already the right class is accepted as-is, on the reasonable assumption it was validated when built. If it was mutated afterwards without `validate_assignment`, that assumption is wrong, and this setting closes the gap at the cost of re-running validation.

`ser_json_timedelta` and `ser_json_bytes` control how those two types serialise, which matters when a consumer expects seconds rather than an ISO duration.

## Protected namespaces

By default Pydantic reserves the `model_` prefix and warns if you declare a field starting with it, because that is where its own methods live &mdash; `model_dump`, `model_validate`, `model_fields`.

That is a genuine problem if your domain has fields like `model_name` or `model_version`, which is common in anything ML-adjacent.

`protected_namespaces=()` turns the warning off, and `protected_namespaces=("model_config",)` narrows it. Be aware that a field literally named `model_dump` would shadow the method, so the warning is doing real work &mdash; disable it deliberately rather than to silence noise.

## Where to set config

Three places, in increasing order of scope.

On the class, as `model_config = ConfigDict(...)`. Explicit and local.

On a shared base model, inherited by everything. Best for house conventions.

As a keyword in the class definition &mdash; `class Module(BaseModel, frozen=True)` &mdash; which is compact and less discoverable.

For a codebase of any size, the base model is the answer. One file states the conventions, every model follows them, and changing a convention is one edit rather than forty.

## Config and inheritance

Config merges rather than replaces. A subclass setting one key keeps its parent's other settings, which is what makes the base-model pattern practical.

That also means an inherited setting can be surprising in a subclass that did not ask for it. If a base sets `extra="forbid"` and a subclass genuinely needs passthrough, it must say so explicitly &mdash; which is the right default, since silently permissive is worse than explicitly permissive.

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

Five decisions, made once. Typos in keys are errors. Whitespace never reaches a field. Assignments are checked. Fields accept either spelling. The whole API speaks camelCase.

Every model inheriting from that is consistent with every other, and a new developer inherits the conventions without being told them.

The one thing to avoid is a base so opinionated that half the models override half of it. If a setting is wrong for a third of your models, it does not belong in the shared base.

## Summary

`model_config` is where model-wide behaviour is decided. The four that matter most: `extra` for unknown keys, `validate_assignment` for mutation, `frozen` for immutability and hashability, and the `str_*` family for human input.

Set them deliberately rather than by default, put your house settings on a shared base, and remember that the two most common silent bugs in this area &mdash; an ignored typo in a key and an unvalidated assignment &mdash; are both one config entry away from being loud.

## The short version

Four settings account for most of the value.

`extra="forbid"` turns a typo in a key from a silent nothing into a named error. Set it anywhere you control both ends.

`validate_assignment=True` extends validation past construction, so a model's declared types stay true for its whole life.

`frozen=True` makes validated data immutable and hashable, which is the right shape for anything that arrives from outside and is then only read.

`str_strip_whitespace=True` removes a category of trivial validator and a category of trivial bug.

Put them on a shared base, decide them once, and let every model in the codebase inherit the same conventions.


## Mistakes people make

**Leaving `extra` at its default where you control both ends.** A typo in a key produces no error, no field and a value that silently falls back to a default. `extra="forbid"` turns a mystery into a message.

**Assuming assignment is validated.** It is not. A model built correctly can hold anything at all a moment later, and the declared types quietly stop being true.

**Copying the same `ConfigDict` into forty classes.** They drift. Four of them end up different for no reason anybody remembers. A shared base makes the convention one edit.

**Using `from_attributes` on an output model without listing fields carefully.** It reads whatever attribute matches a field name, so a model pointed at a user row will faithfully serialise a password hash. It also triggers lazy ORM relationships, which is how one serialisation becomes fifty queries.

**Silencing the protected-namespace warning reflexively.** A field literally named `model_dump` would shadow the method. Disable the warning deliberately for a domain that needs `model_` names, not to quieten noise.

**Building a base so opinionated that half the models override it.** If a setting is wrong for a third of your models, it is not a house convention and does not belong in the shared base.

## What it is really for

Config is where a codebase records the decisions it has made about its own data.

Whether an unexpected key is a mistake or a courtesy. Whether validated objects may change. Whether the wire speaks camelCase. Whether a blank string is a value.

Those are real decisions, and every codebase makes them &mdash; usually implicitly, differently in different files, and rediscovered by each new person. Writing them once, on a shared base, turns a set of accidents into a convention.
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

You write a slug field with a pattern. Then another model needs a slug, so the pattern is copied. Then a third. Six months later the rule changes to permit hyphens, and four of the six get updated.

This is the most ordinary form of drift there is, and it does not need a clever solution &mdash; it needs the rule to exist once.

## Annotated is the mechanism

`Annotated[T, ...]` is standard `typing`. It means "this is a `T`, with extra metadata attached", and static type checkers see straight through to the `T` while libraries can read the metadata.

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

One definition, every use site consistent, and one place to change it.

## It reads better, too

Beyond reuse, there is a readability argument that applies even to a type used once.

`slug: str = Field(pattern=r"^[a-z0-9_]+$")` tells the reader this is a string and then makes them parse a regular expression to learn anything more. `slug: Slug` tells them what the field *is*. If they need the details, the definition is one jump away and has a name attached.

The default placement is better as well. Compare:

```python
minutes: int = Field(default=10, gt=0, le=180)
minutes: Annotated[int, Field(gt=0, le=180)] = 10
```

Both behave identically. The second separates the two concerns &mdash; what kind of value this is, and what it defaults to &mdash; and reads as a sentence: a `Minutes`, defaulting to 10.

## Putting logic in the type

Constraints are not the only thing that can live in an `Annotated`. Validators can too, which means a rule needing actual code can still be part of a reusable type rather than a method bolted to one model.

```python
def must_be_known(v: str) -> str:
    if v not in KNOWN_TRACKS:
        raise ValueError("unknown track %r" % v)
    return v

Track = Annotated[str, AfterValidator(must_be_known)]
```

Every model with a `Track` field now enforces it. Without this, the same `@field_validator` gets copied into each model, which is the original problem with extra steps.

`BeforeValidator` does the same at the other end of the pipeline, which makes it the tool for normalisation:

```python
Slug = Annotated[str, BeforeValidator(to_slug), Field(pattern=r"^[a-z0-9_]+$")]
```

That type cleans its input and then checks it. Any model using it gets both behaviours, and neither is written twice.

There is also `WrapValidator`, which wraps the whole validation step and can catch and replace failures. It is the most powerful and least often needed; reach for it when you want to supply a fallback rather than propagate an error.

## The order things run in

With several pieces of metadata, the pipeline is worth knowing:

A `BeforeValidator` runs first, on the raw input. Then coercion to the base type. Then constraints from `Field`. Then an `AfterValidator`, on the final value.

So `Annotated[str, BeforeValidator(to_slug), Field(pattern=...)]` normalises `"  The Chain RULE "` into `the_chain_rule` and *then* checks it against the pattern. Written the other way round, the pattern would reject the original before anything cleaned it.

Multiple validators of the same kind run in the order they appear.

## What ships already

Before building your own, check what exists. Pydantic includes a good set:

`PositiveInt`, `NegativeInt`, `NonNegativeInt`, `NonPositiveInt`, and the `Float` equivalents.

`StrictInt`, `StrictStr`, `StrictBool`, `StrictFloat` for per-field strictness.

`AwareDatetime`, `NaiveDatetime`, `PastDate`, `FutureDate` for time.

`Json` for a field that holds a JSON string and should be parsed and validated as structured data.

`SecretStr` and `SecretBytes`, which are worth knowing: they hide their value in `repr` and logs, so a password or token cannot leak into a traceback by accident. The real value comes from `.get_secret_value()`, which makes every access deliberate and greppable.

## Composing types

Named types compose, which is where this starts paying compound interest:

```python
Minutes = Annotated[int, Field(gt=0, le=180)]
Schedule = Dict[str, List[Minutes]]
```

Every integer in that nested structure is validated as a `Minutes`. The constraint applies at every depth, and the annotation stays readable.

This is also how to keep deep annotations comprehensible. `Dict[str, List[Annotated[int, Field(gt=0, le=180)]]]` is technically the same thing and nobody can read it.

## Where to put them

A `types.py` module beside your models is the usual answer, and it turns out to be a genuinely useful file. Read it and you learn the vocabulary of the domain &mdash; what a slug is, what a duration may be, what an identifier looks like &mdash; without reading a single model.

That is worth more than the deduplication. A named set of domain types is documentation that cannot go stale, because it is the code that runs.

## When not to bother

Do not name a type used once with no rule attached. `Title = Annotated[str, Field()]` is ceremony.

Do not build a custom type where a `Literal` or `Enum` is the honest answer. A pattern matching four values is a worse enumeration than an enumeration.

And do not go so far that a reader cannot tell what a field actually is. `slug: Slug` is clear. `slug: NormalisedConstrainedIdentifier` is a name that has stopped helping.

## Types that carry documentation

Metadata inside `Annotated` reaches the schema exactly as it would from a `Field`, which means a named type can carry its own description:

```python
Minutes = Annotated[
    int,
    Field(gt=0, le=180, description="Reading time in minutes."),
]
```

Now every field of that type is documented identically, everywhere, with no repetition. For an API with a dozen models sharing a vocabulary, that consistency is visible in the generated documentation and would be impossible to maintain by hand.

## Composing with unions and containers

Named types combine with everything else:

```python
Slug = Annotated[str, Field(pattern=r"^[a-z0-9_]+$")]
OptionalSlug = Optional[Slug]
SlugList = Annotated[List[Slug], Field(min_length=1)]
```

The last one is worth reading twice: the outer `Field` constrains the *list*, and each item is still validated as a `Slug`. Constraints at two levels, one line, still legible.

That legibility is the point. The equivalent written inline is a nested `Annotated` that nobody will want to modify.

## Custom types with `__get_pydantic_core_schema__`

For a type Pydantic knows nothing about &mdash; a third-party class, a domain object with its own parsing &mdash; there is a protocol to teach it:

```python
class Money:
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        ...
```

This is the full escape hatch, and it is genuinely the right answer for a library wrapping its own types.

For application code it is almost never necessary. `Annotated` with a `BeforeValidator` that constructs the object, plus `arbitrary_types_allowed` if needed, covers nearly every case with a fraction of the machinery. Reach for the protocol when you are writing a library others will use with Pydantic, not when you have one awkward field.

## Where a named type goes wrong

**Naming the type after the field.** `ModuleTitle` cannot be reused by `Lesson`, which defeats the purpose. Name it after what it is: `Title`, `Slug`, `Minutes`.

**Too many layers.** A type built from three other named types is impressive and unreadable. If a reader has to follow three definitions to learn what a field accepts, the abstraction has stopped paying.

**Hiding a `Literal`.** A custom type validating membership of four strings is worse than the enumeration it is imitating.

**Naming something with no rule.** `Name = Annotated[str, Field()]` is ceremony with no content.

## The file this produces

A `types.py` in a mature project is one of its most useful documents. Ten or twenty lines defining what a slug is, what a duration may be, what an identifier looks like, what money means here.

Read it and you have the domain's vocabulary before opening a single model. That is the real return &mdash; not saved keystrokes, but a single place where the shape of the domain is stated and cannot drift from the code that enforces it.

## Summary

`Annotated[T, Field(...)]` makes a constraint into a named, reusable type. `AfterValidator` and `BeforeValidator` put logic inside that type so rules needing code are reusable too. Metadata runs left to right: before-validators, coercion, constraints, after-validators.

Use the types Pydantic already ships. Collect your own in one module. And reach for this the second time you write the same rule, not the sixth.

## When to start

The rule of thumb is the second occurrence. The first time you write a constraint, write it inline. The second time you need the same one, name it.

That threshold is low on purpose. The cost of naming a type is one line and the cost of not naming it compounds quietly &mdash; six copies of a rule, four of which are updated when it changes, and nobody notices the other two until something invalid gets through.

Naming early also improves the models immediately, before any reuse happens, because `slug: Slug` reads better than a regular expression embedded in a field declaration. The reuse is the payoff; the readability is the down payment.


## Mistakes people make

**Naming the type after the field it first appeared on.** `ModuleTitle` is a type no other model can reasonably use, which removes the only reason to have named it. `Title` can be used by `Lesson`, `Track` and everything else.

**Building a type where a `Literal` is the honest answer.** A constrained string validating membership of four values produces a worse error, a worse schema and worse static checking than the enumeration it is imitating.

**Stacking layers until nobody can read it.** A type composed from three other named types is impressive and opaque. If understanding a field means following three definitions, the abstraction has stopped paying for itself.

**Reaching for `__get_pydantic_core_schema__` too early.** The full protocol exists for library authors teaching Pydantic about their own types. Application code almost always wants an `Annotated` with a `BeforeValidator` instead, at a fraction of the complexity.

**Putting the metadata in the wrong order.** `Annotated[str, Field(pattern=p), BeforeValidator(f)]` still runs the normaliser first &mdash; before-validators always precede coercion &mdash; but reading it in that order misleads whoever maintains it next. Write the pipeline in the order it executes.

**Naming a type with no rule in it.** `Annotated[str, Field()]` is ceremony. If there is nothing to say about the type beyond `str`, write `str`.

## The return

A named type is not primarily about saving keystrokes.

It is about there being one place where the shape of a domain idea is stated, and about every model that uses it inheriting that statement rather than a copy of it.

The reuse prevents drift. The name improves every model it appears in. And the file they live in becomes the closest thing a codebase has to a written description of its own vocabulary &mdash; one that cannot go stale, because it is the code doing the work.

## How this changes a codebase

The visible effect is smaller models. The real effect is that decisions stop being scattered.

Before: six models each declare a slug, each with its own copy of a pattern, and the definition of a slug exists only as an emergent property of six places agreeing.

After: one line says what a slug is, and six models refer to it. The definition exists, in one place, with a name.

That shift matters most at the moments codebases usually go wrong &mdash; when a rule changes, when somebody new adds a seventh model, when a bug turns out to be one of the six copies having been updated and the others not.

It also changes how the code reads to somebody arriving. Models built from named domain types describe the domain. Models built from `str` and `int` with regular expressions attached describe a serialisation format, and the domain has to be inferred.

The mechanism is a single line of `typing`. The return is a codebase where the vocabulary is written down.

## A last practical note

Introduce named types gradually rather than in one refactor.

The natural moment is when you next write a rule for the second time. Extract it then, use it in both places, and move on. Repeat that for a few weeks and a `types.py` accumulates on its own, containing exactly the rules that actually repeat &mdash; which is a better selection than any up-front attempt to guess them.

The reverse approach, sitting down to define a full vocabulary before it is needed, tends to produce types nothing uses and abstractions that do not match how the domain turned out.
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
intro: What runs when, relative to coercion, and why the choice decides what a validator can do.
## The pipeline

Validating one field is a sequence, and every mode is a slot in it:

1. **before** validators run on the raw input, exactly as it arrived.
2. **Coercion** converts the value to the annotated type.
3. **Constraints** from `Field` are checked.
4. **after** validators run on the final, converted value.

`plain` and `wrap` are different: they replace or surround the whole thing rather than sitting inside it.

Almost every confusion about validators dissolves once this sequence is clear, because the question "why did my validator not run?" nearly always has the answer "it was in after mode and the value failed at step 2".

## after: the default

An after validator receives the value already converted. `n: int` given `"12"` reaches an after validator as the integer `12`.

That is what you want for nearly everything. Checking membership of a set, comparing against a bound that a constraint cannot express, normalising a string, deduplicating a list &mdash; all of these are simpler when the value is known to be the right type, because you can operate on it directly with no defensive `isinstance`.

It is also safer. An after validator cannot receive an arbitrary object, so it cannot fail in surprising ways on input it never anticipated.

## before: fixing the shape

A before validator sees the raw input. Nothing has been checked, so the value could be anything.

Its purpose is repairing the *shape* of data before normal validation gets to it. The canonical case is a field that should be a list, from a caller that sends a comma-separated string:

```python
def split_csv(v):
    return [p.strip() for p in v.split(",")] if isinstance(v, str) else v
```

In after mode this code would never run. A string is not a list, so validation fails at step 2 and step 4 is never reached. This is the single most common validator mistake, and the symptom &mdash; "my validator is not being called" &mdash; sounds like a bug in Pydantic rather than a mode choice.

Two rules for before validators, both consequences of receiving unchecked input. Guard with `isinstance` rather than assuming a type. And return anything you do not handle unchanged, so normal validation still runs on it.

Keep them small. Complex logic operating on unvalidated input is hard to reason about, and errors raised there lack the context that makes Pydantic's messages useful.

## plain: taking over

A plain validator replaces validation for that field. No coercion runs, no constraints are checked, and whatever it returns becomes the value &mdash; unvalidated.

```python
minutes: Annotated[int, PlainValidator(parse_duration)]
```

The annotation still says `int`, and that now serves as documentation and as the schema type rather than as something enforced. Your function is entirely responsible for producing an integer.

This is the right tool for a genuinely custom input format: durations like `"1h30m"`, a coordinate string, a domain-specific identifier. Trying to express those with before validators plus normal coercion is more convoluted than simply owning the parse.

The cost is that you have taken on the whole job, including producing sensible errors. Raise `ValueError` for bad input rather than returning something wrong, or you have built a field that silently accepts nonsense.

## wrap: around the outside

A wrap validator receives the value *and* a handler that performs the normal validation. That lets it act before, after, and instead of:

```python
def default_on_failure(v, handler):
    try:
        return handler(v)
    except ValidationError:
        return 0
```

The main uses are supplying a fallback instead of failing, adding context to an error before re-raising, and short-circuiting expensive validation for a known-good sentinel.

Use it sparingly, and be honest about the fallback case. Swallowing a `ValidationError` and substituting a default is a decision to lose information: the caller sent something wrong and will never know. That is occasionally right &mdash; a metrics field where a bad value should not fail the whole request &mdash; and frequently a way to hide a bug for months.

## Order

Several validators of the same kind run in the order written. Read the annotation left to right and you are reading the pipeline top to bottom.

Mixed kinds follow the sequence: all before validators, then coercion and constraints, then all after validators.

That makes a normalise-then-check type read naturally:

```python
Slug = Annotated[str, BeforeValidator(to_slug), Field(pattern=r"^[a-z0-9_]+$")]
```

Normalise, then coerce, then check. Swap the order of the metadata and the intent changes.

## Two spellings

Everything here exists in both forms.

`Annotated[T, BeforeValidator(f)]` makes the rule part of a type, so it is reusable across models. This is the better default for anything a second model will ever need.

`@field_validator("x", mode="before")` attaches the rule to one model. Better when the logic is genuinely specific to that model, or when it needs `info.data` to see other fields &mdash; which the `Annotated` form does not provide.

`model_validator` also takes `mode`, with `before` receiving the whole raw payload and `after` receiving the finished model. Same vocabulary, model-wide scope.

## Choosing

Ask what the value looks like when your logic needs to see it.

**Already the right type** &mdash; after. This covers most cases.

**Still in its raw form, wrong shape** &mdash> before.

**A format Pydantic has no idea about** &mdash; plain.

**Need to catch or replace a failure** &mdash; wrap.

And when a validator does not seem to run, check the mode first. It is the answer far more often than anything else.

## A worked example

A duration field accepting `90`, `"90"` and `"1h30m"`, rejecting nonsense, and constrained to a sensible range.

`plain` is the honest choice: the input format is not something coercion can be expected to handle, and taking over the parse is clearer than a chain of before-validators trying to massage `"1h30m"` into something `int()` will accept.

Since a plain validator skips constraints, the range check moves into the function or into a separate after validator. That is the trade: full control over parsing, full responsibility for everything downstream of it.

## Modes on model validators

The same vocabulary applies at model level, with different scope.

`model_validator(mode="before")` receives the raw input for the whole payload &mdash; usually a dict, but it can be anything. It is a classmethod, and it returns the data to be validated. Use it to translate a legacy shape or fill in a derived key before field validation runs.

`model_validator(mode="after")` receives the finished model as `self` and returns it. This is where cross-field rules belong.

There is a `mode="wrap"` at model level too, receiving the payload and a handler, which can catch a whole-model failure and substitute something. It is rare and powerful; the same caution about swallowing errors applies.

## What each mode can and cannot do

Worth a table in your head.

A **before** validator can change the shape, cannot rely on the type, and its errors carry less context because nothing has been located yet.

An **after** validator can rely on the type, cannot repair a shape that already failed, and gets good error locations for free.

A **plain** validator controls everything and inherits nothing &mdash; no coercion, no constraints, so anything you want enforced you must enforce yourself.

A **wrap** validator can do all of the above and is the only one that can observe a failure and decide what to do about it.

## Debugging when a validator misbehaves

Three questions, in order, that resolve nearly every case.

**Is it running at all?** Put a `print` at the top. If nothing appears, the mode is wrong &mdash; almost always an after validator whose input failed coercion first.

**What type is it receiving?** Print `type(v)`. A before validator gets raw input and an after validator gets the coerced value; assuming the wrong one is the second most common mistake.

**Is it returning?** A validator with no `return` sets the field to `None`, silently. If a field becomes `None` after you added a validator, that is the cause.

## Constraints still run in the middle

A detail that is easy to forget: `Field` constraints sit between the two validator slots.

So `Annotated[int, BeforeValidator(f), Field(gt=0), AfterValidator(g)]` runs `f` on raw input, coerces, checks `> 0`, then runs `g`. An after validator never sees a value that failed a constraint, because the constraint raised first.

That is usually convenient &mdash; the after validator can assume the bounds hold &mdash; and occasionally the reason a validator meant to *fix* an out-of-range value never runs. Clamping belongs in `before`, or in the constraint's absence.

## Performance

Validators are Python, and Python is the slow part of an otherwise Rust pipeline.

For a model built a few times per request this is irrelevant. For validating a large collection it is the dominant cost, because each item's validators are a round trip out of the core and back.

If profiling points at validation on a hot path, the questions are: can this rule be a constraint instead, since constraints run in Rust; and is the validator doing work that could be done once outside rather than per item. A validator that rebuilds a set of permitted values on every call is a common and easily fixed version of the second.

## Summary

Four slots around one pipeline: before, coerce, constrain, after. `plain` replaces the pipeline; `wrap` surrounds it.

Choose by asking what the value looks like when your logic needs to see it. When a validator does not run, check the mode before anything else. And remember that constraints sit between the two ordinary slots, so an after validator only ever sees values that already passed them.

## The mental model

One sentence holds most of it: **before sees what arrived, after sees what it became.**

Everything else follows. A validator repairing a shape must run before, because after the shape has already failed. A validator checking meaning should run after, because it can then rely on the type. Constraints sit between them, so an after validator never sees a value that broke one.

`plain` and `wrap` step outside that sequence &mdash; one replacing it, the other surrounding it &mdash; and both are for cases where the standard pipeline is not what you want at all.

Keep the sentence and the rest is derivable.


## Mistakes people make

**Shape-fixing logic in after mode.** The single most common, and it presents as "my validator never runs". The value failed coercion at step two and step four was never reached.

**Assuming the type in a before validator.** It receives raw input, which can be anything at all. Guard with `isinstance` and pass through unchanged whatever you do not handle, so the normal path still runs.

**Forgetting to return.** Silent, and it sets the field to `None`. If a field mysteriously becomes `None` after a validator is added, this is why.

**Expecting constraints to run after a plain validator.** `plain` replaces the pipeline entirely: no coercion and no constraints. Anything you want enforced is now yours to enforce.

**Swallowing errors in a wrap validator.** Catching a `ValidationError` and substituting a default is a decision to lose information &mdash; the caller sent something wrong and will never be told. Occasionally correct, frequently a bug hidden for months.

**Rebuilding data inside a validator on every call.** A validator that constructs a set of permitted values each time it runs does that work once per item validated. Hoist it out; on a large collection it is the dominant cost.

## A closing note

Nearly every question about validators reduces to a question about position.

Not "how do I write this rule" but "where in the sequence does it need to sit". Once that is settled the code is usually short and obvious, and when a validator behaves strangely the position is almost always what is wrong.

Before, coerce, constrain, after. Four slots, one order, and everything else follows from knowing which one you are in.
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
intro: Two methods, several filters, and the one mistake that raises TypeError.
## Two methods, and the difference that matters

`model_dump()` returns a dictionary of Python objects. A `date` field is a `date`. A `Decimal` is a `Decimal`. An enum member is the member.

`model_dump_json()` returns a JSON string, converting everything to something JSON can carry.

The rule of thumb: **dump for inside, dump_json for outside**. If the data is going to another function, a template, a test assertion, use `model_dump()`. If it is going into an HTTP response, a queue, or a file, use `model_dump_json()`.

There is a third form worth knowing: `model_dump(mode="json")` gives you a dictionary whose values are already JSON-compatible. That is what you want when something else will do the encoding &mdash; a framework, a JSON logger, an SDK that takes a dict.

In Pydantic v1 these were `.dict()` and `.json()`. They still exist in v2 and warn, and they are all over the internet.

## The TypeError

Everybody meets this once:

```python
json.dumps(m.model_dump())
# TypeError: Object of type date is not JSON serializable
```

It is confusing because the model obviously supports JSON, and the error blames a `date`.

The explanation is that `model_dump()` deliberately did not convert anything. It handed you real Python objects, and `json.dumps` does not know what to do with a `date`.

Three correct forms: `model_dump_json()` if you want the string, `json.dumps(model_dump(mode="json"))` if something else must do the encoding, or `model_dump(mode="json")` alone if you need the dict.

## Shaping the output

`include` and `exclude` select fields. A set names top-level fields; a dict reaches into nested models. The two spellings do not mix in one literal, so once anything needs to reach inside, every entry becomes a key with `True`.

For lists of models there is a special key, `"__all__"`, applying a selection to every item.

Both are useful for removing one obviously-internal field. Beyond that, a separate output model reads better, appears correctly in the schema, and does not require anyone to trace an exclusion expression to work out what an endpoint returns.

## The three exclusions that look similar

These get confused constantly, and the difference is the whole point of the update module.

`exclude_unset=True` omits fields the caller never supplied. Fields explicitly sent, *including explicit nulls*, are kept.

`exclude_defaults=True` omits fields whose value equals their default, whether supplied or not.

`exclude_none=True` omits every field that is `None`, however it got that way.

For a PATCH endpoint, `exclude_unset` is the correct one and the other two are wrong.

Consider a client sending `{"summary": null}` meaning "clear the summary". With `exclude_unset` the output is `{"summary": None}` &mdash; the instruction survives. With `exclude_none` the output is `{}` &mdash; the instruction is gone, and the summary stays as it was. That is a bug users report as "the clear button does not work", and it is one argument away.

`exclude_defaults` has a narrower use: producing a minimal config file, or a payload where anything unspecified should fall back to the receiver's defaults.

## Keeping secrets out

Two mechanisms, for two different exposures.

`Field(exclude=True)` keeps a field out of every serialisation. It is still on the object and still accessible; it simply never appears in a dump. This is right for a password hash, an internal id, or anything the model needs and consumers must not see.

`SecretStr` addresses a different risk: the value appearing in a `repr`, a log line or a traceback. It displays as `**********` and requires `.get_secret_value()` to read, which makes every access deliberate and easy to grep for.

They are complementary. A token that must neither be logged nor serialised wants both.

The safest structure of all is a separate output model that simply does not have the field. You cannot leak what is not there, and no future refactor can accidentally remove a flag.

## Round tripping

A dump is valid input to the same model:

```python
Module.model_validate(m.model_dump()) == m
```

That is genuinely useful for copying, for caching, and for tests.

It stops being true the moment you filter. `model_dump(exclude={"minutes"})` produces a dict missing a required field, and validating it raises. Worth remembering when a filtered dump is being stored and later read back &mdash; the filter that made the output tidy also made it un-reloadable.

Round tripping through JSON works too, and is exact for the types Pydantic knows.

## Nested behaviour

Everything recurses. `model_dump()` on a model containing models returns nested plain dicts, and `model_dump_json()` produces nested JSON.

One thing to check when a nested model is a *different* class than you expect: serialisation follows the field's declared type. If you assign a subclass instance to a field annotated with the parent, by default the extra fields are not serialised, because the model serialises according to what it promised rather than what it happens to hold.

That behaviour is deliberate &mdash; it stops a subclass leaking fields through an API that documented the parent &mdash; and it surprises people who expected the subclass's data. `SerializeAsAny` opts out where you genuinely want the richer output.

## Warnings

Pydantic will warn when serialisation encounters something it did not expect &mdash; typically a field holding a value that does not match its annotation, which happens when `validate_assignment` is off and something assigned freely.

Those warnings are worth listening to rather than silencing. They mean the object's real contents have diverged from what the model claims, and the serialised output may not be what the schema promises.

## Rounding trips and warnings

Pydantic emits a warning when serialisation meets a value that does not match its field's annotation. That happens when `validate_assignment` is off and something assigned freely, leaving the object's contents at odds with what the model claims.

Those warnings are worth reading rather than filtering. They mean the serialised output may not match the schema you publish, which is a defect a consumer will find before you do.

If you see them regularly, the fix is upstream: turn on `validate_assignment`, or freeze the model so the divergence cannot happen.

## Subclasses and what gets emitted

If a field is annotated with a parent model and holds a subclass instance, the extra fields are **not** serialised by default. The model emits what it promised, not what it happens to hold.

That is deliberate, and it is a safety property: a subclass carrying internal fields cannot leak them through an endpoint documented as returning the parent.

It also surprises people who expected the richer output. `SerializeAsAny[Parent]` opts out where you genuinely want whatever the object actually is &mdash; and where you have satisfied yourself that everything a subclass might carry is safe to expose.

## Context

Both dump methods accept a `context` dict, and serialisers can read it through their `info` argument.

That is the supported way to make output depend on something external without a global &mdash; a locale, a viewer's permissions, a feature flag:

```python
m.model_dump(context={"role": "admin"})
```

Used sparingly it is the clean solution to "this field is only visible to some callers". Used heavily it produces output nobody can predict from the model alone, and separate output models are clearer.

## Choosing between filtering and separate models

The recurring question in this module: `exclude` or a second model?

Use `exclude` for one or two obviously-internal fields, where the shapes are otherwise identical and the intent is plain at the call site.

Use a separate model when the difference is structural, when the same difference is needed in more than one place, or when the output is part of a public contract. A model is checked, appears correctly in the schema, cannot be forgotten at a new call site, and is impossible to get wrong by mistyping a field name in a set.

The exclusion set is the thing that quietly stops matching the model. A field renamed in the model and not in the exclusion set silently starts appearing in your public output, and nothing raises.

## Performance

Serialisation happens in Rust and is fast, but it is not free, and two habits cost more than people expect.

Serialising more than you send. Building a full dump and then picking three keys out of it does the work for every field including nested trees. `include` does the same job without the waste.

Serialising the same object repeatedly. Inside a loop that renders one object per row, hoisting the dump out is the obvious fix and easy to miss.

Neither matters at small scale. Both are visible when a response contains thousands of models.

## Summary

`model_dump()` for Python objects, `model_dump_json()` for text, `model_dump(mode="json")` for a JSON-safe dict.

`json.dumps(model_dump())` is the classic mistake; the dict is full of real objects.

`exclude_unset` for PATCH, and not `exclude_none`, which discards the difference between "not mentioned" and "please clear this".

`Field(exclude=True)` and `SecretStr` for secrets, and a separate output model when you want the guarantee rather than the setting.

## A last habit

Look at what your model actually emits, once, before it goes anywhere public.

One `print(m.model_dump_json(indent=2))` shows you the keys, the casing, the formats, and anything present that should not be. It is the same five-minute review as printing the schema, and it catches a different set of problems &mdash; a secret that was never excluded, a nested field nobody meant to expose, snake_case where the rest of the API is camelCase.

The output of a model is a contract with everyone who consumes it. It is worth having read it.


## Mistakes people make

**`json.dumps(model_dump())`.** The classic. The dict holds real `date` and `Decimal` objects, and the standard encoder refuses them. The error blames a date and the cause is the wrong method.

**`exclude_none` where `exclude_unset` was meant.** On an update endpoint this discards a caller's explicit instruction to clear a field. It presents as "the clear button does not work" and is one argument away from correct.

**Filtering a dump that is later reloaded.** An unfiltered dump round-trips; a filtered one is missing required fields and will not validate. This bites when the tidy output is stored and read back later.

**Trusting an exclusion set to stay correct.** Rename a field in the model, forget the exclusion set, and something internal silently begins appearing in your public output. Nothing raises. A separate output model cannot fail this way.

**Serialising more than you need.** Building a full dump of a nested tree to pick three keys out of it does all the work for every field. `include` does the same job without it.

**Ignoring serialisation warnings.** They mean an object's contents no longer match what the model claims, usually because something was assigned without `validate_assignment`. The published schema and the actual output have diverged, and a consumer will find it first.

## The two mistakes

If only two things survive from this module, make them these.

`json.dumps(model_dump())` raises, because the dict is full of real Python objects. Use `model_dump_json()`, or `mode="json"` when something else does the encoding.

`exclude_none` is not `exclude_unset`. The first throws away a caller's explicit instruction to clear a field; the second preserves it. On a PATCH endpoint that difference is a bug users report and nobody can reproduce.

## Output as a contract

The output of a model is a contract, whether or not anybody wrote it down.

Somebody is parsing those keys. Something depends on that date format. A client somewhere assumes a field is present because it always has been. None of that is in a document; it is in the behaviour, and it becomes binding the moment anyone builds against it.

That is why the choices in this module deserve more care than they usually get. Adding a computed field changes every response the model feeds. Renaming a field breaks parsers. Changing an exclusion set alters what leaves your system, silently and without any test failing.

The practical habit is to treat a model that reaches the outside world as a published interface: know what it emits, be deliberate about changing it, and prefer a separate output model whenever the shape you send differs from the shape you hold. A dedicated class makes the contract explicit, checkable and hard to alter by accident &mdash; which is exactly what a contract should be.
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

**The wire is camelCase.** JavaScript clients and a great many APIs use `publishedAt`. Python uses `published_at`. Renaming your attributes to match makes every Python file read badly; renaming their payload is not an option.

**The key is a reserved word.** A payload with `from`, `class`, `import` or `id` cannot map onto an attribute with the same name.

**The name is bad.** A third-party API calls something `dt2`. You do not have to.

**The name changed.** You are renaming a field and both spellings must work through a deprecation window.

## The simple form

```python
published_at: str = Field(alias="publishedAt")
```

One alias, used for input and output. There is one behaviour here that catches everyone: **by default the alias replaces the Python name as input**. `Module(published_at="...")` now raises, which is surprising when you have been constructing the model in your own tests.

`populate_by_name=True` fixes it:

```python
model_config = ConfigDict(populate_by_name=True)
```

Now either spelling works on the way in. This is almost always what you want, and it is worth setting on a base model so nobody has to rediscover it.

## by_alias on the way out

Aliases are not used for output unless you ask:

```python
m.model_dump()                 # {"published_at": ...}
m.model_dump(by_alias=True)    # {"publishedAt": ...}
```

Forgetting this is the most common alias bug, and the symptom is "my API accepts camelCase but returns snake_case". The aliases were configured correctly; the serialisation call did not ask for them.

In FastAPI, `response_model_by_alias` defaults to `True`, so responses use aliases automatically &mdash; which means a manual `model_dump()` elsewhere in the same codebase behaves differently from the endpoint. Worth knowing before you spend an afternoon on it.

## Separating the directions

A single `alias` uses the same name both ways. When the directions differ, use the two specific settings:

```python
minutes: int = Field(validation_alias="durationMinutes",
                     serialization_alias="reading_minutes")
```

Read one name, write another. That sounds exotic and comes up whenever you sit between two systems that disagree &mdash; consuming a partner API and exposing your own shape, or migrating a field where you must accept the old name and emit the new one.

Where both are set, they win over a plain `alias` in their respective directions.

## Several accepted spellings

`AliasChoices` takes the first key present:

```python
minutes: int = Field(validation_alias=AliasChoices("minutes", "readingMinutes", "duration"))
```

This is the clean way to run a rename. Add the new name to the front, keep the old one, ship. Clients migrate at their own pace, and neither your model nor your handlers need a branch for it. Remove the old entry when the traffic stops.

It also handles the ordinary mess of a payload assembled by several teams over several years, where the same value appears under three names depending on which service produced it.

## Reaching into nested data

`AliasPath` pulls a value out of a nested structure:

```python
author_name: str = Field(validation_alias=AliasPath("author", "name"))
first_tag: str = Field(validation_alias=AliasPath("tags", 0))
```

Strings are keys, integers are indices. A deeply nested third-party response becomes a flat model with no manual digging and no intermediate models you did not want.

Use it with judgement. Flattening two or three values from a response is exactly right. Flattening twenty produces a model whose relationship to the payload is impossible to see, and modelling the real structure with nested models is clearer.

Note that `AliasPath` is validation-only. There is no serialisation equivalent, because rebuilding a nested shape from flat fields is not a rename &mdash; if you need that, a custom serialiser or a separate output model is the answer.

## Doing it for the whole model

Writing `alias="..."` on forty fields is tedious and drifts. `alias_generator` applies a rule to every field:

```python
class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
```

Inherit from that and every model in your API speaks camelCase, with no per-field configuration at all. Pydantic ships `to_camel` and `to_pascal` in `pydantic.alias_generators`, so you usually do not even write the function.

An explicit `alias` on a field overrides the generator, which is what you want for the handful of exceptions every real API has.

This is the right shape for a codebase-wide convention: one base model, one setting, every model consistent, and one place to change it.

## Aliases in the schema

The generated JSON Schema uses aliases, which is correct &mdash; the schema describes the wire format, and the wire format is what the alias names.

So consumers of your OpenAPI document see `publishedAt`, generated clients produce `publishedAt`, and the documentation matches what the endpoint actually accepts. This is one of the places where getting aliases right pays off beyond your own code.

## Things that go wrong

**Forgetting `by_alias=True`** on a manual dump. The most common one.

**Forgetting `populate_by_name`** and then being unable to construct the model in tests using Python names.

**Aliasing to a name that collides** with another field's name, which produces confusing behaviour rather than a clear error.

**Using aliases to paper over a bad model.** If half your fields need aliases to make sense, the model may be describing someone else's payload rather than your domain. A translation layer &mdash; an input model matching their shape, converted to yours &mdash; is sometimes clearer than twenty aliases.

## Aliases and nested models

An alias applies to the field it is declared on, and nesting is unaffected: a nested model's own aliases apply when it is validated, and `by_alias=True` propagates through the whole tree on the way out.

So a camelCase convention applied through a shared base model reaches every level without extra work, which is the main reason to prefer `alias_generator` on a base over per-field aliases.

The one thing to check is consistency. A tree where the parent is aliased and one nested model is not produces output that is camelCase at the top and snake_case two levels down &mdash; valid, confusing, and exactly the kind of thing that survives review.

## What the schema says

Generated schemas use aliases, which is correct: the schema describes the wire, and the alias is the wire name.

That has a practical consequence worth knowing. If you generate a schema for internal purposes and expect Python names, you will not get them. `model_json_schema(by_alias=False)` produces the Python-named version when that is genuinely what you need.

For anything published, the aliased schema is the right one, because it matches what the endpoint accepts and returns.

## Aliases in error messages

An error's `loc` uses the **alias**, not the Python name, when validation failed on an aliased field.

That is the right behaviour &mdash; the caller sent `publishedAt` and should be told about `publishedAt`, not about an attribute name they have never seen. But it means error-handling code cannot assume `loc` matches your attribute names, which occasionally matters when mapping errors back to internal state.

## A migration recipe

Renaming a field in a live API, without breaking anyone:

**Step one.** Add the new name as the primary, keep the old one accepted:

```python
minutes: int = Field(validation_alias=AliasChoices("minutes", "readingMinutes"))
```

Both work on the way in. Output uses whichever you set as the serialisation alias &mdash; keep emitting the old name for now.

**Step two.** Switch the serialisation alias to the new name. Clients reading the response see the new one; clients sending either still work.

**Step three.** Once traffic on the old name stops, remove it from `AliasChoices`.

Three small deploys, no coordinated cutover, no broken clients. This is the pattern aliases make possible and it is worth knowing before you need it.

## Deciding whether you need them at all

A model full of aliases is sometimes a sign that the model is describing someone else's payload rather than your domain.

If you consume a third-party API with thirty oddly-named fields, two models can be cleaner than thirty aliases: one matching their shape exactly, with their names, and a conversion into yours. The first model documents their API honestly; the second is your domain, unpolluted.

Aliases are best when the difference is a *convention* &mdash; camelCase versus snake_case, a reserved word, a rename in progress. When the difference is a whole foreign vocabulary, a translation layer says more.

## Summary

`alias` for one name both ways; `validation_alias` and `serialization_alias` when the directions differ. `populate_by_name=True` so Python names still work as input. `by_alias=True` to emit them.

`AliasChoices` for several accepted spellings, which makes renames painless. `AliasPath` for flattening nested payloads. `alias_generator` on a shared base for a whole-API convention.

And the one to remember: aliases are not used on output unless you ask for them.

## The one-line summary

Aliases exist so your Python can read like Python while your API reads like whatever your consumers expect.

Set the convention once on a shared base with `alias_generator` and `populate_by_name`, remember `by_alias=True` when dumping by hand, and reach for `AliasChoices` the moment you need to rename something without breaking anyone.

Everything else in this module is a variation on those three.


## Mistakes people make

**Forgetting `by_alias=True`.** Comfortably the most common. Aliases are not used on output unless requested, and the symptom &mdash; an API accepting camelCase and returning snake_case &mdash; looks like a configuration problem rather than a missing argument on one call.

**Forgetting `populate_by_name`.** An alias replaces the Python name as input, so your own tests can no longer construct the model with the names you wrote. The fix is one config entry and it belongs on a shared base.

**Inconsistent nesting.** A parent with an alias generator and a nested model without one produces output that is camelCase at the top and snake_case two levels down. Valid, confusing, and exactly the sort of thing that survives review.

**Assuming `loc` matches your attribute names.** Errors report the alias, because that is the name the caller used. Code mapping errors back to internal state has to account for it.

**Expecting `AliasPath` to work on the way out.** It is validation-only. Rebuilding a nested shape from flat fields is not a rename, and needs a serialiser or a separate output model.

**Aliasing an entire foreign vocabulary.** Thirty aliases usually means the model is describing someone else's payload rather than your domain. Two models &mdash; one matching their shape, one matching yours, with a conversion between &mdash; says more and stays readable.

## The failure mode to expect

If something about aliases is not working, check `by_alias=True` first.

It accounts for most alias problems, it produces no error, and the symptom &mdash; an API that accepts one convention and returns another &mdash; looks like a configuration problem rather than a missing argument on a single call.

The second thing to check is `populate_by_name`, which is what stops your own tests being able to construct the model using the names you wrote.

## The convention decision

Behind the mechanics is one decision worth making deliberately rather than per model.

Does your API speak the wire's convention, or your language's? Both are defensible. Consistency is what matters, because a mixed API is worse than either choice made badly.

If your consumers are browsers and JavaScript clients, camelCase on the wire is what they expect, and an `alias_generator` on a shared base gives it to every model at once with no per-field work.

If your consumers are Python services, snake_case throughout is simpler and needs no aliases at all.

What produces trouble is deciding case by case: some endpoints camelCase, some not, some models aliased and their nested models not. Every consumer then needs to know which is which, and no amount of documentation makes that pleasant.

Make the choice once, express it in a base model, and let the exceptions be genuine exceptions rather than accidents.

## One thing to remember

If exactly one fact survives this module, make it `by_alias=True`.

Aliases configured perfectly still do nothing on output until that argument is passed, the failure is silent, and the symptom looks like a configuration problem rather than a missing keyword on a single call. It is the first thing to check whenever aliases appear not to work.
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

Most people write this:

```python
data = json.loads(raw)
model = Module.model_validate(data)
```

It works. The better form is:

```python
model = Module.model_validate_json(raw)
```

It is not merely shorter. It is faster, produces better errors, and is more faithful with numbers. Three separate reasons, and they compound.

## Speed

The two-step version parses JSON into Python objects &mdash; dicts, lists, strings, floats &mdash; and then validates those objects, converting again into what the model wants.

Every intermediate object is allocated and thrown away. For a large payload that is a lot of garbage created for no purpose.

`model_validate_json` parses and validates in a single pass inside `pydantic-core`, the Rust engine. It reads the JSON text and constructs the final values directly, skipping the intermediate representation entirely.

The saving grows with payload size. For a small request body it is unimportant; for a large document, or a high-throughput endpoint, it is a real difference for a change that makes the code shorter.

## Error quality

This is the argument that matters most day to day.

With `json.loads`, malformed JSON raises `json.JSONDecodeError` &mdash; a different exception, from a different library, that knows nothing about your model. Your handler needs two `except` clauses producing two shapes of error response, and the JSON one has no field information because there are no fields yet.

`model_validate_json` folds it in. Malformed JSON becomes a `ValidationError` with the type `json_invalid`, arriving through exactly the same channel as a missing field or a failed constraint.

That means one handler. The function that turns a `ValidationError` into a 422 response now covers syntax errors too, without a special case.

The error also carries the **position** in the document. For a missing comma four hundred lines into a config file, being told the line and column is the difference between a fix and a search.

## Fidelity with numbers

The subtlest of the three, and the one that costs money.

`json.loads` turns `0.1` into a Python float, because that is what JSON numbers are in Python. The float is already inexact at that moment. Handing it to a `Decimal` field faithfully preserves the wrong value.

`model_validate_json` reads the characters. When the target is a `Decimal`, it can construct it from the exact text, so `0.1` in the document becomes `Decimal("0.1")` rather than the float's approximation.

For anything financial, that is not a micro-optimisation &mdash; it is the difference between correct and quietly wrong. It also means the advice from the types module ("send money as a string") has a companion: even when a partner sends money as a JSON number, parsing directly recovers more of it than going via Python.

## The other direction

`model_dump_json()` is the matching call, and it is symmetric for the same reasons: it serialises from the model's data straight to text, without building an intermediate dict.

A round trip is exact for every type Pydantic knows. A `date` becomes an ISO string and parses back to the same `date`. A `Decimal` becomes a string and returns as the same `Decimal`. A UUID survives. This makes JSON a reasonable format for caching validated objects, and makes equality assertions in tests trustworthy.

## Bytes work too

Both methods accept `bytes` as well as `str`, which is what an HTTP body actually is.

That saves a decode step, and avoids a class of bug where the wrong encoding is assumed. If you are reading a request body or a file, pass the bytes straight in.

## Non-model shapes

Not every payload is an object. `TypeAdapter` provides the same one-step parsing for anything you can annotate:

```python
TypeAdapter(List[Lesson]).validate_json(payload)
TypeAdapter(Dict[str, float]).validate_json(payload)
```

Same speed benefit, same error handling, same fidelity. And `dump_json` in the other direction, which returns `bytes`.

Build the adapter once at module level. Constructing one compiles a schema, and doing that inside a loop is a real and easily-missed performance mistake.

## When to keep the two steps

There are legitimate reasons to parse separately.

**You need the raw structure first.** Inspecting a `type` field to choose a model, logging the payload, or routing on something before validating. Though a discriminated union often removes the first of those.

**The input is not JSON.** YAML, TOML and msgpack all produce Python objects, and `model_validate` is the right entry point for them.

**You already have a dict** from a database driver, another library, or your own code. There is nothing to parse.

The rule is simple: if you are holding JSON text or bytes, use `model_validate_json`. If you are holding Python objects, use `model_validate`. The mistake is converting text to objects yourself purely to hand them to a validator that would rather have had the text.

## In practice with a framework

FastAPI already does this for request bodies, so an endpoint annotated with a model gets the fast path without you asking.

Where it matters in application code is everywhere else: reading a config file, consuming a queue message, calling another service and validating the response, loading a fixture in a test. Those are all places where the two-step habit is common and the one-step version is strictly better.

## Strictness and JSON

The strict-mode module noted that a strict model validating from JSON still accepts the string forms JSON has no alternative to &mdash; a date as text, for instance.

That behaviour depends on Pydantic knowing the input was JSON, which it only does when you use `model_validate_json`. Parse with `json.loads` first and that context is gone: the model sees a Python string where a `date` was wanted, and in strict mode refuses it.

So the two-step form is not merely slower, it can be *stricter in the wrong way*. Another reason to hand the text straight over.

## Large payloads

For very large documents, two things are worth knowing.

Parsing is a single pass and memory-bounded by the result rather than by intermediate objects, so `model_validate_json` uses meaningfully less memory than the two-step form on a big document.

There is no streaming. The whole document is parsed before validation completes, so a hundred-megabyte file is a hundred megabytes in memory. If that matters, the answer is at a different level &mdash; a streaming JSON reader producing records, each validated individually or in batches with a `TypeAdapter`.

## Reading from a file

The natural spelling reads bytes and hands them straight over:

```python
config = Settings.model_validate_json(Path("config.json").read_bytes())
```

No decode step, no `json.load`, and a malformed file produces a `ValidationError` naming the position rather than a `JSONDecodeError` from elsewhere.

For a config file that is a genuinely nice pattern: one call, one exception type, and errors that say which key was wrong and where in the file it was.

## Other formats

Only JSON gets the fast path, because only JSON has a parser inside the core.

YAML, TOML and msgpack all go through their own libraries, which produce Python objects, which then go to `model_validate`. That is the correct shape for those formats and there is nothing to optimise &mdash; but it does mean a YAML config gets none of the fidelity benefit for decimals, and a syntax error arrives as that library's exception.

If exactness matters in a YAML config, quoting the number so it arrives as a string is the pragmatic fix.

## What to take away

The habit is small: when you are holding JSON text or bytes, hand it to Pydantic rather than to `json.loads`.

It is faster, because it skips an entire intermediate representation. It produces better errors, because syntax and validation failures arrive through one channel with positions attached. It is more faithful, because decimals keep the digits as written. And it is shorter to write.

Very few changes improve four things at once for one fewer line of code.

## Summary

`model_validate_json` for JSON text or bytes; `model_validate` for Python objects. One pass in Rust rather than two with garbage in between. Malformed JSON becomes a `ValidationError` with a position, so one handler covers syntax and validation alike. And decimals keep the precision that a trip through Python floats would have destroyed.

`model_dump_json` on the way out, `TypeAdapter` for shapes that are not models, and build adapters once rather than per call.

## Where this fits

This is a small change with an unusually good ratio, and it applies in more places than request handling.

Reading a config file. Consuming a queue message. Validating another service's response. Loading a test fixture. Anywhere JSON text or bytes are in hand and a model is about to be built from them.

In each of those the two-step habit is common, and in each of them the one-step form is faster, produces better errors and keeps more precision. It is worth grepping for `json.loads` once and seeing how many of them are immediately followed by a validation call.


## Mistakes people make

**Parsing first out of habit.** `json.loads` followed immediately by `model_validate` is the shape to grep for. Every instance of it is slower, produces worse errors and loses decimal precision compared with handing the text over directly.

**Catching two exception types.** Code with an `except JSONDecodeError` beside an `except ValidationError` is code that parsed separately. Validating the text directly collapses both into one channel and one handler.

**Decoding bytes unnecessarily.** An HTTP body is bytes and both methods accept bytes. Decoding to `str` first adds a step and a chance to assume the wrong encoding.

**Expecting streaming.** There is none. The whole document is parsed before validation completes, so a very large file is entirely in memory. Streaming needs a different tool producing records, each validated individually or in batches.

**Assuming the fast path applies to YAML or TOML.** Only JSON has a parser inside the core. Other formats go through their own libraries and produce Python objects, which then take the ordinary route &mdash; including losing decimal exactness on the way.

**Using it when you already have a dict.** There is nothing to parse. The rule is simply which you are holding: text or bytes go to `model_validate_json`, Python objects go to `model_validate`.

## One line, four improvements

Speed, because an entire intermediate representation is skipped. Errors, because syntax and validation failures arrive through one channel with positions attached. Fidelity, because decimals keep the digits as written. Strictness, because the parser knows the input was JSON and applies the right rules.

All of it from handing Pydantic the text instead of parsing it first &mdash; which is also less code than the alternative.

## Why the habit persists

The two-step form is not the result of anyone deciding it was better. It is what you write when you learn `json` before you learn Pydantic, which is the order nearly everybody learns them in.

`json.loads` is the obvious way to turn text into data, and once the data exists, validating it is the obvious next step. Both halves are reasonable and the combination is worse than either author intended.

That is worth naming because it explains why the pattern is everywhere, including in a lot of documentation and answers online, and why changing it is a matter of noticing rather than of understanding.

The check takes a minute: search a codebase for `json.loads` and look at the line after each one. Wherever it is a validation call, the two lines collapse into one that is faster, more precise about numbers, and produces errors that say where in the document the problem was.

There is rarely a reason to keep the two-step version once seen &mdash; unless something genuinely needs the raw structure in between, which is a real case and a small one.
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
intro: Per-field and per-model output control, and the strong argument for not using it.
## What they do

Pydantic's defaults are good: dates become ISO strings, decimals become strings, enums become values, nested models become nested objects. For most fields there is nothing to decide.

When the default is genuinely wrong, `@field_serializer` replaces the output for one field:

```python
@field_serializer("amount")
def show_money(self, value: Decimal) -> str:
    return "£%.2f" % value
```

The method takes `self` and the value, and returns whatever should appear.

## Only the output changes

This is the important property. A serialiser does not change validation, and does not change what the field holds.

`p.amount` is still a `Decimal`. Arithmetic works, comparisons work, and every rule you attached still ran. The serialiser is the last step on the way out, not a conversion applied to the model.

That separation is what makes the feature safe. You are not weakening the model to satisfy a consumer's format preference.

## Two modes, two outputs

`when_used` restricts a serialiser to one direction:

`"always"` is the default. `"json"` applies only to `model_dump_json()` and `model_dump(mode="json")`. `"unless-none"` skips it for null values.

The `"json"` case is the useful one. It lets `model_dump()` keep a real `date` for code inside your program while JSON output gets whatever format a consumer needs. Without it, a formatting serialiser makes the Python dump useless for anything that wanted the object.

## Serialising the whole model

`@model_serializer` replaces the entire output:

```python
@model_serializer
def as_envelope(self) -> dict:
    return {"type": "module", "attributes": {...}}
```

This is for shapes that are not simply your fields &mdash; a JSON:API envelope, a legacy format you must emit, a payload where the structure differs from your internal one.

It is powerful and it is a big hammer. Every field is now your responsibility, so a field added to the model does not appear in the output until somebody remembers to add it to the serialiser. That divergence is exactly the drift models exist to prevent.

A `mode="wrap"` variant receives a handler that produces the default output, letting you take that and adjust it rather than rebuilding it. That is much safer, because new fields still flow through:

```python
@model_serializer(mode="wrap")
def add_meta(self, handler):
    data = handler(self)
    data["_type"] = "module"
    return data
```

Prefer the wrap form whenever you are augmenting rather than replacing.

## The schema problem

Here is the sharp edge, and it is easy to miss.

A serialiser changes the output. It does not change the schema. So a `Decimal` field serialised as `"£12.50"` still appears in the generated schema as a decimal, your API documentation says one thing, and the endpoint returns another.

For a public API that is a real defect: generated clients will produce a type that does not match the data they receive.

`return_type` fixes it:

```python
@field_serializer("amount", return_type=str)
```

Now the serialisation schema reports a string, and the documentation matches reality. Set it whenever the serialised type differs from the field type, which is most of the time.

## Secrets: a serialiser is the weakest option

Masking a token with a serialiser is a common idea and the worst of the three available.

`@field_serializer` producing `tok_…ef` keeps the value out of dumps and leaves it in `repr`, in logs, in tracebacks, and in any code that reads the attribute.

`SecretStr` hides it from `repr` and requires `.get_secret_value()`, which makes access deliberate and greppable.

`Field(exclude=True)` keeps it out of every serialisation entirely.

For anything genuinely secret, use the type and the exclusion. Reach for a serialiser only when you want a *partial* value in the output on purpose &mdash; showing the last four digits of a card, which is a product decision rather than a security one.

## The argument against most custom serialisers

Most custom serialisers are display formatting that has ended up in the wrong layer.

`"26 August 2026"` is a formatting choice. It assumes English, a date order, and a reader rather than a program. A client receiving it cannot sort by it, cannot filter on it, cannot show it in another language, and has to parse it back to do anything useful.

`"2026-08-26"` is data. Every client can sort it, compare it and format it however that client's user needs.

The same argument applies to currency symbols, thousands separators, relative times ("3 days ago") and rounded numbers. All of them are decisions that belong where the audience is known, which is the presentation layer, not the data model.

So the honest guidance: before writing a serialiser, ask whether the default was wrong or merely unfamiliar. If it is being changed for a human reader, that logic probably belongs closer to the human.

## When they are genuinely right

**Emitting a legacy format** you do not control and cannot change.

**Redacting deliberately**, where a partial value is the intended product behaviour.

**Wrapping in an envelope** required by a specification, best done with `mode="wrap"`.

**Computing a representation** that is expensive to store but cheap to derive, where a computed field would be the alternative.

**Interoperating with something specific** &mdash; a system that wants timestamps in milliseconds, or booleans as `"Y"`/`"N"`.

Each of those is a real constraint from outside, rather than a preference from inside.

## The info argument

Both decorators accept an optional `info` parameter carrying `mode`, `context` and the exclusion settings in force.

`mode` lets one serialiser behave differently for Python and JSON output without needing `when_used`.

`context` is the interesting one. It is a dict passed to the dump call, which makes output dependent on something the model does not know:

```python
@field_serializer("salary")
def maybe_hide(self, v, info):
    if (info.context or {}).get("role") != "hr":
        return None
    return v
```

Used carefully that is a clean answer to field-level visibility rules. Used freely it produces an endpoint whose output cannot be predicted from the model, and separate output models per audience are easier to reason about and to document.

## Serialising unusual types

The other legitimate reason to write a serialiser is a field whose type Pydantic has no opinion about &mdash; a third-party object accepted via `arbitrary_types_allowed`.

Such a field has no default serialisation, so a dump either fails or produces something unhelpful. A serialiser turning it into a dict or a string is not a formatting preference; it is the only way the model can be serialised at all.

If you find yourself doing this for a type used in several models, the better shape is a custom type that knows how to serialise itself, so the knowledge lives with the type rather than being repeated in every model that holds one.

## Testing what you emit

Custom serialisation is worth testing directly, because it is the part of a model that no other test exercises.

Validation tests construct models; they do not check what comes out. A serialiser can be broken for months while every validation test passes.

The test is short &mdash; build a model, dump it, assert on the result &mdash; and it is the only thing standing between a formatting change and a silently altered API response.

Assert on `model_dump()` and `model_dump_json()` separately when `when_used` is involved, since that is precisely the case where they differ.

## The decision, restated

Before writing one, three questions.

**Is the default actually wrong, or just unfamiliar?** ISO dates and decimal strings look odd and are correct.

**Is this for a machine or a person?** Machines want data. People want formatting, and that belongs where the person is.

**Will the schema still be true?** If not, set `return_type`, or you are publishing a document that lies about your own output.

Most proposed serialisers fail one of those, which is the reason this module argues against its own subject as much as for it.

## Summary

`@field_serializer` for one field, `@model_serializer` for the whole output, `mode="wrap"` when augmenting rather than replacing so new fields still flow through.

`when_used="json"` keeps Python dumps useful. `return_type` keeps the schema honest. `info.context` makes output conditional when that is genuinely needed.

For secrets prefer `SecretStr` and `Field(exclude=True)`. And reach for a serialiser when an external constraint demands a shape &mdash; not when a default merely looks unfamiliar.

## What to remember

Serialisation is the last thing that happens and the first thing a consumer sees.

Pydantic's defaults are chosen so that output is data: sortable, comparable, parseable, unambiguous across locales. Most reasons to override them turn out to be formatting for a human, and humans are downstream of the layer that knows who they are.

Override when something outside genuinely demands a shape. Set `return_type` so the schema keeps telling the truth. And test what you emit, because no other test does.


## Mistakes people make

**Formatting for a person in a data layer.** Covered at length, and still the most common. A date rendered as "26 August 2026" cannot be sorted, filtered or localised by anyone receiving it.

**Forgetting `return_type`.** The output changes, the schema does not, and your documentation quietly starts describing something the endpoint no longer returns. Generated clients then produce a type that does not match the data, and the failure surfaces in someone else's codebase.

**Using a plain `@model_serializer` for a small addition.** Replacing the entire output to add one key means every field is now hand-maintained, and a field added to the model six months later never appears. `mode="wrap"` adds the key and lets everything else flow through untouched.

**Masking a secret with a serialiser and stopping there.** The dump is clean and the value is still in `repr`, still in logs, still in tracebacks, still readable by any code holding the model. `SecretStr` and `Field(exclude=True)` address the parts a serialiser cannot.

**Not testing the output.** Validation tests construct models; they never look at what comes out. A serialiser can be broken for months while the suite stays green, and the first person to notice is a consumer.

**Depending on context that is not always passed.** A serialiser reading `info.context` needs a sensible default for every call that does not supply one, including the ones in tests and the ones a framework makes internally. `(info.context or {})` rather than `info.context[...]` is the difference between a graceful default and a `TypeError` during a response.

## The test

Is the default wrong for a machine, or merely unformatted for a person?

Only the first is a serialiser's job. Everything else &mdash; currency symbols, readable dates, relative times, rounded numbers &mdash; is a decision about an audience, and belongs where the audience is known.

Applying that one question honestly removes most proposed serialisers, and makes the remaining ones easy to justify.

## A final framing

It helps to think of serialisation as the boundary in the other direction.

Validation is where you stop trusting the outside world and convert its text into your types. Serialisation is where you stop assuming your types and produce something the outside world can read.

Both are conversions at an edge, and both work best when they convert to something *neutral*. Validation does not try to guess what a caller meant; it accepts unambiguous readings and refuses the rest. Serialisation should be symmetrical: emit data with a single unambiguous reading, and let the consumer decide how to present it.

A custom serialiser that formats for a human breaks that symmetry. It takes a value with one meaning and produces one with a presentation baked in, which the next layer has to undo before it can do anything else.

That is the underlying reason the advice in this module runs against its own subject. The feature is well designed and occasionally essential. It is just that most of the reasons people reach for it are reasons to do the work somewhere else.
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
intro: What the generated schema contains, and why it is the reason Pydantic is everywhere.

## The output you did not write

`Module.model_json_schema()` returns a dictionary that is a valid JSON Schema document: types, required fields, defaults, constraints, descriptions, and definitions for nested models.

You wrote none of it. It is derived entirely from the annotations, `Field` arguments and docstrings already in the class.

This is quietly the reason Pydantic became a dependency of half the modern Python ecosystem. Validation is useful; a *machine-readable description of your data that cannot drift from the code* is what other tools can build on.

## What reads it

**FastAPI** turns these schemas into your OpenAPI document, which becomes the interactive docs at `/docs`. The descriptions you wrote on fields appear next to those fields. The examples pre-fill the request form. The constraints show as documented limits.

**Client generators** turn OpenAPI into typed clients in TypeScript, Go, Java and the rest. The quality of that generated client is a direct function of the quality of your schema.

**LLM tooling** uses schemas to constrain structured output: the schema tells the model what shape to answer in, and the same model then validates the answer.

**Form builders and validators** on the other side of the wire read the same document, so a browser can enforce your `minLength` before a request is ever sent.

One class definition feeds all of them.

## Constraints versus validators, concretely

This is the strongest practical argument in the whole track, and the schema is where you can see it.

`Field(gt=0, le=180)` produces `"exclusiveMinimum": 0, "maximum": 180`. A generated client knows the range. The documentation states it. A form can enforce it.

A `field_validator` that checks the same thing produces **nothing**. The schema says `"type": "integer"` and the rule is invisible to every consumer. It is still enforced &mdash; a bad value is still rejected &mdash; but the caller only finds out by being rejected.

Same enforcement, completely different experience for whoever is calling you. That is why the guidance has been: express a rule as a constraint whenever a constraint can express it.

The same holds for `Literal` against a `pattern`. A `Literal` becomes `"enum": ["draft", "published"]` and a client can render a dropdown. A pattern matching the same two values becomes a regular expression the client cannot do anything with.

## Definitions and references

A nested model appears once in `$defs` and is referenced with `$ref` wherever it is used.

That matters for generated clients: a referenced definition typically becomes a named type in the target language. `Author` used in two fields becomes one `Author` type used twice, rather than two anonymous objects that happen to match.

It also keeps the document small when a model is reused heavily, and it is why recursive models produce a schema at all &mdash; a self-reference is just a `$ref` back to the same definition.

## The two modes

`model_json_schema(mode="validation")` is the default and describes what the model **accepts**.

`mode="serialization"` describes what it **emits**.

They differ in real ways. Computed fields appear only in the serialisation schema, because they are output and can never be supplied. A field with `exclude=True` appears in validation and not serialisation. Serialisation aliases apply to one and validation aliases to the other.

Frameworks pick the right one for you: FastAPI uses the validation schema for request bodies and the serialisation schema for response models. Knowing the distinction matters when you generate a schema yourself and wonder why a field is missing.

## Metadata is the cheap win

`description`, `title` and `examples` on a field change no behaviour and flow straight into the document.

For anything with consumers beyond yourself, this is the highest-value writing you can do per character. A field called `weight` needs a description &mdash; of what, in what unit? A field called `title` does not.

`examples` deserve particular attention because they populate the interactive documentation's request form. A developer trying your API for the first time gets a working request they can send, rather than an empty box. That difference shows up in how many of them succeed.

`json_schema_extra` attaches anything else the schema format supports that Pydantic has no dedicated argument for &mdash; vendor extensions like `x-` keys, or keywords from a newer draft. It takes a dict, or a callable that receives and modifies the generated schema.

## What does not translate

Some things simply cannot be expressed in JSON Schema, and knowing which keeps expectations right.

**Validator logic.** Arbitrary Python has no schema equivalent.

**Cross-field rules.** A `model_validator` enforcing "end after start" has no representation. Document it in the model's docstring, which becomes the schema's description, so at least a human reading the docs learns about it.

**Custom serialisation.** As the previous module covered, a serialiser changes output without changing the schema unless you set `return_type`.

Where a rule cannot be expressed, the honest thing is to describe it in prose so the documentation is not silently incomplete.

## A habit worth adopting

Print the schema for a model you have just written. It takes one line, and it shows you what your consumers will actually see.

Constraints you thought you had documented and did not. Fields with no description whose names are not self-explanatory. A `pattern` where a `Literal` would have produced a set of choices. A required field you meant to make optional.

It is the fastest review available for an API model, and it uses information the model already contains.

## Customising the whole document

`model_config` accepts `json_schema_extra`, which can be a dict merged into the model's schema or a callable that receives and edits it:

```python
model_config = ConfigDict(
    json_schema_extra={"examples": [{"title": "Vectors", "minutes": 8}]})
```

Model-level examples appear in documentation as complete sample payloads, which is more useful to a first-time caller than per-field examples: they can copy one and send it.

For deeper control there is `GenerateJsonSchema`, a class you can subclass to change how schemas are produced across a whole application &mdash; renaming definitions, altering how optionals are represented, adding vendor extensions everywhere. It is the right tool for a house style applied to an entire API and considerable overkill for one model.

## Docstrings become descriptions

A model's docstring becomes the schema's `description`. That is worth knowing because it is free documentation for the rules that cannot be expressed structurally.

A cross-field invariant &mdash; "ends_on must be after starts_on" &mdash; has no schema representation. Writing it in the docstring means a consumer reading the documentation learns about it, instead of discovering it through a 422.

`use_attribute_docstrings=True` extends this to fields, taking the string literal beneath an attribute as its description. It keeps the documentation next to what it describes, which is where it stays accurate.

## Reading the schema as a review

The most practical use of this module is as a review tool. One line, and you see what your consumers see:

```python
print(json.dumps(Module.model_json_schema(), indent=2))
```

Things it reliably surfaces: fields whose name does not explain them and which have no description; a `pattern` where a `Literal` would have produced a set of choices; a rule you thought was documented that turns out to live in a validator; a field in `required` that you meant to default; a nested model inlined because it is used once, where a named definition would give clients a better type.

None of that requires running the API. It is the highest-value five minutes available on a model that other people will consume.

## Where schemas end up

Worth knowing the chain, because it explains why the small things matter.

Your model generates a schema. FastAPI collects those into an OpenAPI document. That document is read by the interactive docs, by client generators in several languages, by API gateways, by contract-testing tools, and increasingly by LLM tooling deciding what shape to produce.

A description you write once is read by everybody in that chain. So is a missing one.

## What to remember

The schema is generated from what you already wrote, so its quality is a direct function of how specific your annotations are.

Constraints appear; validators do not. `Literal` and `Enum` become choices; patterns become opaque. Nested models become named definitions and therefore named client types. Descriptions and examples cost nothing and are read by every tool downstream.

The habit worth forming is simply printing it. Everything above becomes visible the moment you look at the document your model already produces.

## Summary

`model_json_schema()` generates a standard document from what you already wrote. Constraints become keywords; validators become nothing. Nested models become referenced definitions and therefore named types in generated clients. `Literal` and `Enum` become renderable choices.

Two modes, for input and output. Metadata &mdash; descriptions and examples especially &mdash; is the cheapest documentation you will ever write, and it is read by tools you may never see.

## The habit

Print the schema for the next model you write.

It takes one line and it is the only view of your model that matches what consumers get. Everything this module describes &mdash; a validator that documented nothing, a pattern that should have been a `Literal`, a field with no description, a required field you meant to default &mdash; becomes visible immediately.

The schema was generated from work you had already done. Looking at it is the cheapest quality check available.


## Mistakes people make

**Expressing a rule as a validator when a constraint would do.** The rule is enforced and invisible. Documentation, generated clients and browser-side forms all remain unaware of it, so the caller only learns the limit by breaching it.

**Using a `pattern` where a `Literal` belongs.** A regular expression matching four values becomes an opaque string in the schema. The enumeration becomes a set of choices a form can render as a dropdown and a client can turn into a union type.

**Leaving fields undescribed.** `weight` needs a description &mdash; of what, in what unit. Names that are not self-explanatory and have no description produce documentation that technically exists and helps nobody.

**Never looking at it.** The schema is one line away and it is the only view of your model that matches what consumers actually receive. Everything above becomes obvious the moment you print it.

**Expecting cross-field rules to appear.** A `model_validator` has no schema representation at all. Where a rule cannot be expressed structurally, put it in the model's docstring so at least a human reading the documentation learns about it.

**Forgetting the two modes.** Generating a validation schema and wondering why a computed field is missing, or a serialisation schema and wondering why an excluded field is absent, are both the same misunderstanding: one describes what goes in, the other what comes out.

## Why this is the reason

Validation is useful and other libraries do it.

What made Pydantic a dependency of half the modern Python ecosystem is this: a machine-readable description of your data, generated from the code that enforces it, and therefore incapable of drifting from it.

Documentation that cannot go stale. Clients generated from the truth. Forms enforcing the same rules as the server. All from annotations you were going to write anyway.

## What good looks like

A well-specified model produces a schema somebody could implement a client against without asking you a question.

Every field has a type narrow enough to be useful &mdash; `Literal` rather than `str` where the set is closed, `date` rather than `str` where it is a date. Every constraint that exists in your head exists in the document. Every field whose name is not self-explanatory has a description. There is at least one complete example. Nested concepts are named models rather than inline objects, so the generated client has named types.

A poorly-specified model produces a document that is technically valid and useless: everything is a string, nothing has bounds, no field is described, and the real rules live in validators the consumer cannot see.

Both are generated automatically from code that validates identically. The difference is entirely in how specific the annotations were &mdash; which is the argument this whole track has been making, arriving finally at the place where it becomes visible to somebody other than you.
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
intro: The same machinery applied to any annotation - and the fastest way to validate a large collection.
## The thing people work around

A model validates a model. But plenty of data is not shaped like one.

An endpoint returns a bare JSON array. A config value is a `Dict[str, float]`. A function takes a `List[UUID]` and you would like to check it. A queue message is a single integer.

The common workaround is a wrapper model:

```python
class LessonList(BaseModel):
    items: List[Lesson]
```

A box built only so that something can be inside it, and every caller has to reach through `.items` to get at the actual data.

`TypeAdapter` is what that was working around:

```python
lessons = TypeAdapter(List[Lesson])
lessons.validate_python(rows)
```

## The same surface as a model

An adapter has the methods you already know, applied to the annotation instead of to a class:

`validate_python` and `validate_json` for input. `dump_python` and `dump_json` for output. `json_schema` for the schema.

So everything from the previous modules applies. Coercion works the same way. Constraints inside `Annotated` are honoured. Errors have the same `loc`, `type`, `msg` and `input`, so the error handler you already wrote covers adapters without modification.

That last point is worth emphasising: this is not a parallel API with its own conventions. It is the same machinery, addressed differently.

## What you can pass it

Anything you can write as an annotation.

Scalars: `TypeAdapter(int)`. Containers: `List`, `Dict`, `Set`, `Tuple`. Optionals and unions, including discriminated ones. Models. Constrained types from `Annotated`. Any nesting of those.

`TypeAdapter(Annotated[int, Field(gt=0)])` validates a bare positive integer, which is occasionally exactly what a function argument needs.

## Build it once

This is the mistake worth naming loudly, because it is invisible and common.

Constructing a `TypeAdapter` **compiles a schema**. That is real work &mdash; the same work that happens once when a model class is defined.

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

The difference is large and it does not look like a performance bug in review, which is exactly why it survives.

## Validating a collection in one call

The second performance point is the more valuable one, and it applies to models too.

Two ways to validate a thousand rows:

```python
[Lesson.model_validate(r) for r in rows]              # per item
TypeAdapter(List[Lesson]).validate_python(rows)       # whole list
```

Both produce the same result. The first crosses from Python into Rust and back a thousand times. The second makes one call, and the loop happens inside the compiled core.

For bulk work &mdash; importing a file, processing a batch, validating a large response &mdash; that is the single most effective optimisation available in this library, and it is one line.

This is also the answer to the concern raised back in the first tier about validation cost on large collections. The cost is real; the way to reduce it is to let the core do the looping rather than to skip validating.

## Where it earns its place

**Bare arrays.** An endpoint that accepts or returns a JSON list.

**Configuration.** A `Dict[str, str]` from environment or a file, validated without inventing a settings model for three values.

**Function arguments.** Checking an argument at a public function's edge without wrapping it.

**Bulk validation.** The performance case above.

**Dynamic types.** Because it takes a type at runtime, you can build one from a type computed at runtime &mdash; useful in generic code and in libraries.

## Schemas without models

`json_schema()` produces a schema document for the annotation, which is how a framework documents an endpoint whose body is a bare array.

That is the piece that makes the wrapper model genuinely unnecessary. Previously you needed the model to get a schema; now the annotation is enough, and your API documentation describes an array as an array rather than as an object with an `items` field nobody sends.

## When a model is still better

`TypeAdapter` is not a replacement for models, and reaching for it everywhere would be a mistake.

A model gives you a **name**. `Lesson` means something; `Dict[str, Any]` does not. Named types are how a codebase stays comprehensible.

A model gives you a place for **validators, config and methods**. An adapter has no class body.

A model gives you **attribute access**. `lesson.minutes` beats `data["minutes"]`, and your editor can help with the first.

So: models for the domain concepts, adapters for the shapes around them. A `List[Lesson]` is an adapter wrapping a model, and that is the usual arrangement &mdash; the model names the thing, the adapter handles the collection.

## A small caution

An adapter validates and hands back plain Python objects. `TypeAdapter(Dict[str, float])` gives you a dict, not something with guarantees attached.

Nothing stops later code putting a string in that dict. Validation happened at a moment; it is not a permanent property of the object, which is the same as everywhere else in Pydantic and worth remembering when the validated thing is a mutable builtin rather than a model with `frozen=True` available.

## Adapters and constrained types

Because an adapter takes any annotation, it takes constrained ones:

```python
Port = Annotated[int, Field(ge=1, le=65535)]
PORTS = TypeAdapter(List[Port])

PORTS.validate_python(["80", "443"])     # [80, 443]
PORTS.validate_python([0])               # ValidationError
```

That is a compact way to validate a list of values against a domain rule with no model anywhere. Configuration lists, command-line arguments and query parameters are all natural fits.

## Validating function arguments

An adapter at a public function's edge gives you the same guarantees a model would, without wrapping the arguments in an object:

```python
IDS = TypeAdapter(List[UUID])

def fetch(ids):
    ids = IDS.validate_python(ids)
    ...
```

Pydantic also ships `@validate_call`, which reads a function's own annotations and validates arguments automatically. That is usually the nicer spelling when a whole function should be checked; an adapter is better when only one argument needs it, or when the check is conditional.

## The schema for a bare shape

`json_schema()` is what makes the wrapper model genuinely unnecessary rather than merely inconvenient.

Before adapters, an endpoint accepting a bare JSON array needed a model to produce a schema, and the resulting documentation described an object with an `items` field that no client ever sent. With an adapter the schema describes an array, because an array is what it is.

FastAPI uses this internally, which is why annotating a request body as `List[Item]` produces correct documentation with no wrapper in sight.

## Adapters are cheap to hold, not to build

The distinction that matters for performance: an adapter is expensive to *construct* and cheap to *use*.

Constructing compiles a schema. Using it runs compiled code. So the pattern is always the same &mdash; build at module level, use anywhere:

```python
LESSONS = TypeAdapter(List[Lesson])
```

Uppercase by convention, because it is a module-level constant, and putting it at the top makes it obvious it is built once.

If a type is only known at runtime, cache the adapters in a dict keyed by type rather than rebuilding. `functools.lru_cache` on a small factory function is the usual shape.

## A short list of uses

A bare JSON array in or out. A configuration dict. A function argument at a public edge. Bulk validation of a large collection in one call. A shape whose type is computed at runtime. A schema for something that is not a model.

Each of those has a wrapper-model workaround, and each is cleaner without one.

## Summary

`TypeAdapter` applies the whole machinery &mdash; validation, coercion, constraints, serialisation, schemas, errors &mdash; to any annotation, with the same behaviour and the same error shapes as a model.

Build it once at module level. Prefer one call over a Python loop for collections. Use models where a thing deserves a name and a class body; use adapters for the shapes around them.

It is the piece most people find late, and the one that removes the most awkward code when they do.

## Why it is worth learning early

Most people discover `TypeAdapter` after writing several wrapper models, and then go back and delete them.

The habit it replaces is small but pervasive: reaching for a class because validation seemed to require one. Once you know an annotation is enough, a whole category of awkward code stops being written &mdash; the box around the list, the `.items` every caller has to unwrap, the schema that describes an object where the data is an array.

Models for things that deserve names. Adapters for the shapes around them. That division is most of the judgement this module is trying to pass on.


## Mistakes people make

**Constructing inside a loop.** The single most costly mistake here, and the one that looks fine in review. Building an adapter compiles a schema; doing it per iteration repeats that work every time. Module level, uppercase, once.

**Looping in Python over a collection.** `[Model.model_validate(r) for r in rows]` crosses between Python and Rust once per row. `TypeAdapter(List[Model]).validate_python(rows)` makes one call and loops inside the compiled core. For bulk work it is the highest-value one-line change available.

**Using an adapter where a model belongs.** A `Dict[str, Any]` passed around a codebase is a shape with no name, no methods, no attribute access and no place to put a rule. If the thing is a domain concept, it deserves a class.

**Assuming validation persists.** An adapter hands back plain Python objects. A validated `Dict[str, float]` is an ordinary dict, and nothing stops later code putting a string in it. Validation happened at a moment; it is not a property the object carries afterwards.

**Forgetting it can serialise and generate schemas.** People discover `validate_python` and stop. `dump_json` and `json_schema` are the other half, and the schema in particular is what makes the wrapper model genuinely unnecessary rather than merely inconvenient.

**Rebuilding adapters for runtime types without caching.** When the type is computed, cache the adapters in a dict keyed by type, or wrap a small factory in `functools.lru_cache`.

## The short version

Any annotation, the whole machinery, no class required.

Build it once at module level, because construction compiles a schema. Validate collections in one call rather than looping in Python. And use it wherever the data has no natural model around it &mdash; which is more often than the wrapper-model habit suggests.

## A note on naming and discovery

One reason `TypeAdapter` is found late is that it does not look like the thing people are searching for. Someone with a bare JSON array searches for how to validate a list, finds examples using models, and builds the wrapper. Nothing in that path mentions adapters.

So it is worth stating the shape plainly: **if you can write it as a type annotation, you can validate it, serialise it, and generate a schema for it, without a class.**

That covers a great deal. A list of models. A dictionary of settings. A single constrained integer. An optional union. Anything nested from those.

The corollary is equally useful: if you are writing a class purely so that something can be validated, stop and check whether an annotation would do. The wrapper model is a real and widespread pattern, and almost every instance of it predates its author discovering this.

Where a class still earns its place is where a class was always the right answer &mdash; a domain concept that deserves a name, somewhere to hang methods, attribute access instead of subscripting, a place for validators and config. Those are properties of a model, not of validation, and adapters were never competing for them.

## Where it sits in the library

It is easy to read this module as being about an optimisation or a convenience. It is really about a boundary in how Pydantic is organised.

`BaseModel` is a way of *declaring* a shape and getting behaviour attached to it. `TypeAdapter` is a way of *using* the same machinery against a shape declared some other way.

Everything the library does &mdash; coercion rules, constraints, error paths, JSON parsing, serialisation, schema generation &mdash; lives underneath both. A model is not a more capable validator; it is a class with that validator bound to it, plus a namespace for methods and configuration.

Seeing it that way makes the choice obvious rather than a matter of taste. Ask whether you need the class. If the answer is yes &mdash; because the thing has a name, needs methods, wants attribute access &mdash; write a model. If the answer is no, an annotation and an adapter give you identical validation with nothing extra to maintain.
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
intro: The pattern behind every paginated response, written once instead of once per resource.
## The duplication

Every API with more than one list endpoint grows the same class several times:

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

Identical apart from one type. A third resource means a third copy, and a change to pagination means editing all of them &mdash; or, more realistically, editing most of them.

## The generic version

```python
T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int = 1
```

Inherit from `BaseModel` and `Generic[T]`, use `T` where the varying type goes, and parameterise at the point of use:

```python
Page[Module](items=[...], total=1)
```

One definition. Adding a field to the envelope reaches every resource at once, and there is no possibility of the copies disagreeing because there are no copies.

## It is still validated

A common assumption is that a generic loosens things. It does not.

`Page[Module]` validates `items` as a list of `Module`, with every rule `Module` carries. Coercion works, constraints run, errors have the usual paths &mdash; `("items", 0, "minutes")` names the first item's field exactly as it would in a non-generic model.

`Page[int]` validates a list of integers, with the same coercion rules as anywhere else. The parameter can be any type Pydantic understands, not only models.

## Each parameterisation is a real class

`Page[Module]` is a distinct class, created the first time you write it and cached afterwards.

That has two consequences worth knowing.

It has a name, `Page[Module]`, which appears in the schema and in error messages, so a consumer sees a specific type rather than a vague envelope.

And building it costs something. The cost is small and paid once per parameterisation, but it means `Page[Module]` inside a hot function is doing a lookup that a module-level alias would avoid:

```python
ModulePage = Page[Module]
```

That alias is also better style: it names the type once and every use site is shorter.

## Bounded parameters

An unbounded `TypeVar` can be anything, so a generic cannot assume anything about it. A bound fixes that:

```python
TResource = TypeVar("TResource", bound=Resource)

class Page(BaseModel, Generic[TResource]):
    items: List[TResource]

    def ids(self):
        return [item.id for item in self.items]
```

Because the parameter must be a `Resource`, every item is guaranteed to have `id`, and the method is safe. Without the bound, mypy would object and the method would be a runtime gamble.

Bounds are also documentation. `Generic[TResource]` with a bound says what kind of thing this envelope is for; a bare `T` says nothing.

## Several parameters

More than one is allowed, and the result-or-error envelope is the common case:

```python
class Result(BaseModel, Generic[D, E]):
    ok: bool
    data: Optional[D] = None
    error: Optional[E] = None
```

Written once, used as `Result[Module, Problem]` everywhere. This is a pattern many codebases reinvent per endpoint.

Keep the count low. Two parameters is comfortable, three is a stretch, and beyond that the type is usually trying to be several types at once.

## Schemas and clients

Each parameterisation generates its own schema, titled with the parameterised name.

That is the practical payoff for consumers. A generated TypeScript client gets `PageModule` and `PageLesson` as distinct types, each with correctly typed `items`. Without generics you would have written those classes by hand and got the same result at more cost; with a hand-rolled `items: List[Any]` envelope you would get a client that types `items` as `any` and helps nobody.

FastAPI handles generic response models directly &mdash; `response_model=Page[Module]` &mdash; and documents it correctly.

## Inheritance and generics together

A generic model can be subclassed, and a subclass can fix the parameter:

```python
class ModulePage(Page[Module]):
    facets: Dict[str, int] = {}
```

That gives you the shared envelope plus something specific to one resource. It is a good pattern when one endpoint genuinely needs an extra field, and a bad one if every subclass adds something &mdash; at that point the envelope is not actually shared.

## When not to reach for one

**Two use sites.** Two near-identical classes are easier to read than a generic. The pattern earns its keep at three or four, and the cost of waiting is small.

**The classes differ in more than one type.** A generic with a parameter and three overridden fields is not a shared shape.

**A union would say it better.** If the payload is one of a fixed small set rather than arbitrary, a discriminated union describes that precisely and a generic does not.

**The envelope has no structure.** `Generic[T]` wrapping a single field of type `T` is a box. `TypeAdapter` validates the payload directly without one.

## Generics and validation cost

Parameterising is not free, and it is worth knowing where the cost falls.

`Page[Module]` builds a class the first time it is written: resolving the type variable, constructing a schema, caching the result. Every subsequent use of the same parameterisation reuses it.

So the cost is per distinct parameterisation, paid once, and it is the same cost a hand-written `ModulePage` would have paid at import. Validation itself is identical &mdash; the schema the generic produces is the schema the hand-written class would have produced.

The mistake, as with `TypeAdapter`, is doing the parameterisation somewhere repetitive. `Page[Module]` inside a function called per request performs a cached lookup each time; a module-level alias performs it once. The difference is small and free to avoid.

## Generics with FastAPI

`response_model=Page[Module]` works directly, and the documentation names the type correctly &mdash; `PageModule` in the generated schema, with `items` typed as an array of `Module`.

That is worth doing rather than falling back to an untyped envelope. A response model of `Page[Module]` gives every consumer a real type; a model with `items: List[Any]` gives them nothing, and they will write the type by hand on their side and get it wrong when yours changes.

The same applies to a `Result[Data, Error]` envelope. If your API wraps every response, making that wrapper generic is the difference between a client library that knows what each endpoint returns and one that unwraps `any`.

## Summary

`class Page(BaseModel, Generic[T])`, used as `Page[Module]`. The parameter is fully validated with its own rules. Each parameterisation is a real, named class that appears correctly in the schema and in generated clients.

Bound the type variable when the generic needs to rely on what the parameter provides. Alias parameterisations at module level. Keep the parameter count to one or two.

And reach for it at the third copy of an envelope, not the second &mdash; two similar classes are easier to read than a generic, and the pattern earns its keep as soon as there are more.


## Mistakes people make

**Reaching for one at the second copy.** Two similar classes read better than a generic. The pattern earns its keep around the third or fourth, and waiting costs almost nothing.

**Parameterising in a hot path.** `Page[Module]` performs a cached class lookup every time it is evaluated. A module-level alias does it once and reads better at every use site.

**Leaving the type variable unbounded when methods need it.** A method calling `item.id` on a bare `T` is a runtime gamble that mypy will object to. `TypeVar(bound=Resource)` makes the guarantee real and documents what the envelope is for.

**Too many parameters.** Two is comfortable. Three is a stretch. Beyond that the type is trying to be several types, and separate classes will be clearer.

**Wrapping a single field.** `Generic[T]` around a model with one field of type `T` is a box. `TypeAdapter` validates the payload directly and produces a schema that describes what the data actually is.

**Assuming a generic is looser.** It is not. `Page[Module]` validates its items with every rule `Module` carries, and the error paths are identical to a hand-written envelope's.

**Forgetting `response_model=Page[Module]`.** Falling back to an untyped envelope in FastAPI means every consumer gets `any` and writes the type by hand on their side &mdash; where it will be wrong the first time yours changes.

## Reading a generic model

One practical note for anyone maintaining these.

A generic reads worse than the classes it replaces, and that is the trade. `class ModulePage(BaseModel)` with three concrete fields can be understood at a glance; `class Page(BaseModel, Generic[T])` requires the reader to hold a type variable in their head and then find the parameterisations to know what it is ever filled with.

Two things make that cost small. Name the type variable meaningfully &mdash; `TResource` says more than `T` once there is more than one. And alias the parameterisations at module level, so a reader searching for "what does the modules endpoint return" finds `ModulePage = Page[Module]` rather than an expression buried in a decorator.

Neither costs anything, and both turn a generic from something clever into something ordinary.

## A worked shape

Most APIs end up with two generic envelopes and nothing else.

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

Two definitions and a handful of aliases replace one envelope class per resource, which in a system of fifteen resources is fifteen classes all saying the same thing.

The aliases matter as much as the generics. They give each parameterisation a name a reader can search for, keep the parameterisation out of hot paths, and make endpoint signatures short: `response_model=ModulePage` rather than a bracketed expression in a decorator.

Adding a field to pagination &mdash; a cursor, a `has_more` flag &mdash; is then one edit that reaches every list endpoint at once, correctly, including in the documentation and in every generated client. That is the property worth having, and the reason the pattern survives contact with a real codebase.

## Generics and static checking

One benefit that does not show up at runtime at all.

Mypy and Pyright understand `Generic[T]`, so `Page[Module]` is a type they can reason about. `page.items[0].title` is checked; `page.items[0].name` is flagged before the code runs.

A hand-written `ModulePage` gives the same static benefit, so this is not an argument for generics over concrete classes. It is an argument against the shortcut people reach for when they tire of writing envelopes:

```python
class Page(BaseModel):
    items: List[Any]
```

That validates nothing about the payload, tells mypy nothing, and produces a schema in which `items` is an array of anything. Every consumer &mdash; your own code, a static checker, a generated client &mdash; is worse off.

The choice is not really "generic or concrete". It is "typed or untyped", and the generic is what makes the typed option cheap enough that nobody reaches for the untyped one.

## Why envelopes end up generic

It is worth noticing why this pattern appears in nearly every API of any size, because it is not really about generics.

An API with fifteen list endpoints has fifteen responses that differ in exactly one place. That is a shape, and shapes want names. Writing fifteen classes to express one shape is the kind of duplication that looks harmless in a small codebase and becomes a maintenance surface in a large one &mdash; not because typing it is hard, but because changing it later means finding all fifteen.

The generic is simply the language feature that lets the shape have a name. `Page` is the concept; `Page[Module]` is that concept applied. Once written, adding a field to pagination is a single edit that cannot miss a case, and every consumer sees the change consistently.

That is the same argument as extracting a nested model, or naming a constrained type, or putting config on a shared base. Each is a different mechanism for the same principle: state a decision once, in a place that has a name, and let everything that needs it refer to that rather than to a copy.
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
intro: Typed, validated configuration from the environment - and why start-up is the right place to fail.
## Configuration is untrusted input

Everything in this track has argued that data crossing into your program should be validated at the boundary. Configuration is such data, and it is usually treated as though it is not.

The typical code is `int(os.environ.get("PORT", "8000"))` scattered through a codebase, with no central statement of what configuration exists, no defaults in one place, and no check that anything required is actually set. A missing variable becomes a `None` that travels until something fails on it.

`pydantic-settings` applies the model discipline to it. `BaseSettings` is a `BaseModel` that reads its values from the environment.

```python
class Settings(BaseSettings):
    app_port: int = 8000
    app_debug: bool = False
    database_url: str
```

Field names map to environment variables case-insensitively, so `app_port` reads `APP_PORT`. Values arrive as strings and are coerced by the ordinary rules &mdash; which is exactly the case lax coercion was designed for.

Note `app_debug: bool`. The boolean vocabulary from the coercion module means `APP_DEBUG=yes`, `=1`, `=true` and `=on` all work, and `=maybe` raises. That is a much better outcome than `bool(os.environ.get("APP_DEBUG"))`, where the string `"false"` is `True`.

## Failing at start-up

The single biggest benefit is *when* the failure happens.

`database_url: str` has no default, so it is required. If the variable is not set, constructing `Settings()` raises immediately, naming the field. A deployment missing a variable fails at boot, visibly, before serving anything.

The alternative is a `None` that sits quietly until the first request touching the database, which may be minutes or hours later, and produces an error about `NoneType` far from the cause.

That is why settings should be instantiated once at start-up, not lazily on first use. The whole value is in failing before the process claims to be ready.

## Naming

Three mechanisms, in increasing specificity.

**Implicit.** `app_port` reads `APP_PORT`. Case-insensitive.

**Prefix.** `env_prefix="VIZ_"` in `SettingsConfigDict` makes every field read `VIZ_`-prefixed variables. This is how you keep an application's configuration from colliding with everything else in a container.

**Explicit.** `Field(validation_alias="DATABASE_URL")` pins one field to one variable, which is what you need for the shared names that do not follow your prefix &mdash; `DATABASE_URL`, `PORT`, `TZ`.

`AliasChoices` works here too, which is the clean way to accept both an old and a new variable name during a migration.

## Checking, not just typing

A settings model is a model, so everything from the earlier tiers applies &mdash; and configuration is a place where that matters more than people expect.

```python
port: int = Field(ge=1, le=65535)
env: Literal["dev", "test", "prod"]
workers: int = Field(gt=0)
```

`ENV=staging` now fails at boot with a message naming the three permitted values. Without it, `staging` propagates through the application and produces behaviour nobody intended, because some `if env == "prod"` was false and nothing said so.

This is the strongest argument for settings models over a config dict: configuration errors are among the most common causes of production incidents, and almost all of them are typos or values outside a permitted set. Both are exactly what validation catches.

Validators work too, for cross-field rules &mdash; "if `TLS_ENABLED`, then `CERT_PATH` must be set" is a `model_validator` and a genuinely useful one.

## Nesting

Grouped configuration can be a nested model, filled two ways.

From JSON in one variable: `REDIS='{"host": "cache", "port": 6380}'`.

Or from delimited names, with `env_nested_delimiter="__"`: `REDIS__HOST=cache` and `REDIS__PORT=6380`.

The delimited form is usually nicer operationally &mdash; each value is its own variable, so it can be set independently and overridden per environment without rewriting a JSON blob.

## Files

`env_file=".env"` in `SettingsConfigDict` reads a dotenv file, which is where local development configuration usually lives. Real environment variables take precedence, so a deployed process is never affected by a file that happened to ship.

There is also `secrets_dir`, which reads each field from a file of that name in a directory &mdash; the shape Docker and Kubernetes secrets use, where a secret is mounted as a file rather than exposed in the environment.

The precedence order, highest first: values passed directly to `Settings(...)`, then the environment, then the dotenv file, then the secrets directory, then defaults. That is worth knowing when a value is not what you expected.

## Secrets

Use `SecretStr` for credentials, and the reason is specific.

A settings object is the single thing most likely to be printed. Log it at start-up to record the configuration, and a plain `str` password is in your logs forever. Include it in an error report and it goes to your error tracker. `repr` it in a debugger session that gets pasted into a ticket, and it is in the ticket.

`SecretStr` displays as `**********` everywhere and requires `.get_secret_value()` to read, which makes every real access deliberate and greppable.

Note that a `SecretStr` in `model_dump()` stays hidden, so a settings dump is safe to log &mdash; which is the property you want.

## One instance

Build it once and pass it around, or use a cached accessor:

```python
@lru_cache
def get_settings() -> Settings:
    return Settings()
```

Constructing settings reads the environment and validates, and doing that per request is wasted work. The cached function is also convenient in FastAPI, where it can be a dependency and overridden in tests.

Avoid a module-level global constructed at import. It runs at import time, which makes it awkward to test with different values and can fail before logging is configured &mdash; producing a start-up crash with no useful output.

## Testing

Two habits make settings testable.

Instantiate with explicit values: `Settings(app_port=1234)` bypasses the environment entirely, which is what a unit test wants.

And use `monkeypatch.setenv` for tests that genuinely exercise the environment reading. Do not mutate `os.environ` directly, because the change leaks into every test that follows.

## Layering environments

Most applications need the same settings with different values per environment, and the clean shape uses ordinary inheritance:

```python
class Settings(BaseSettings):
    env: Literal["dev", "test", "prod"] = "dev"
    debug: bool = False
    db_pool_size: int = 5

class ProdSettings(Settings):
    debug: bool = False
    db_pool_size: int = 20
```

That is better than branching on `env` inside the application, because each environment's configuration is stated in one place and can be read without tracing conditionals.

Where it goes wrong is depth. Three levels of settings inheritance with overrides at each is harder to reason about than a flat model whose values come from the environment. Prefer supplying different values to the same model wherever you can, and reserve subclassing for genuine structural differences.

## What belongs in settings

Not everything configurable belongs here.

**Yes:** anything that differs between environments (URLs, credentials, pool sizes, log levels), anything secret, anything an operator may need to change without a deploy.

**No:** application constants that never vary, feature logic dressed up as configuration, or anything a caller supplies per request &mdash; that is a request model.

The test is whether a value could reasonably differ between your laptop and production. If it could not, it is a constant, and making it configurable adds a failure mode with no benefit: another variable that can be unset, misspelt or set to something nonsensical.

## Summary

`BaseSettings` treats configuration as untrusted input crossing a boundary, which is what it is. Field names map to environment variables, `env_prefix` namespaces them, `validation_alias` pins the exceptions.

Required fields with no default make a misconfigured deployment fail at boot with the variable named, rather than hours later. Constraints and `Literal` catch the typos and out-of-range values behind most configuration incidents. `SecretStr` keeps credentials out of the logs a settings object is uniquely likely to reach.

Build it once, cache it, and let it refuse to start when something is wrong.


## Mistakes people make

**Instantiating settings lazily.** The entire benefit is failing at boot with the variable named. Construct them at start-up; a settings object built on first use turns a configuration error into a runtime one, hours later.

**Giving everything a default.** A default on `DATABASE_URL` means a misconfigured deployment starts happily and points at the wrong database. Required fields should be required.

**A module-level global built at import.** It runs before logging is configured, so a failure produces a crash with no useful output, and it is awkward to test with different values. A cached accessor function is better.

**Plain `str` for credentials.** A settings object is the thing most likely to be logged at start-up or attached to an error report. `SecretStr` is the difference between that being routine and being an incident.

**`env: str` instead of a `Literal`.** `ENV=staging` then silently takes every else-branch in the application, and nothing anywhere says the value was not recognised.

**Mutating `os.environ` in tests.** It leaks into every test that follows and produces failures that depend on ordering. `monkeypatch.setenv`, or pass values directly.

**Configuring things that never vary.** Every setting is another variable that can be unset, misspelt or set to something nonsensical. If it could not reasonably differ between your laptop and production, it is a constant.

## Testing configuration

Two habits keep settings testable.

Instantiate with explicit values where the test is not about the environment: `Settings(port=1234)` bypasses reading it entirely, which is what a unit test wants and is far clearer than arranging variables around the call.

Use `monkeypatch.setenv` when the test genuinely exercises the reading, never a direct mutation of `os.environ` &mdash; that leaks into every test after it and produces failures that depend on ordering.

And test the failure case. A test asserting that a missing `DATABASE_URL` raises is worth having, because it is the behaviour the whole module exists for, and it is the one nobody notices has broken until a deployment comes up healthy with no database.

## A last note on start-up

There is a general principle behind this module worth stating on its own.

The best time to discover that something is misconfigured is before the process claims to be ready. Not on the first request, not when a code path is first taken, and not at three in the morning when the only person who knows what `WORKERS` should be is asleep.

A settings model turns configuration from something an application discovers gradually into something it asserts at boot. Every required variable is checked, every value is converted to the type the code expects, every constrained field is inside its range, and if any of that fails the process stops with a message naming exactly what is wrong.

That is the same argument as validating a request body, applied to the other kind of input a program takes. It is just that request bodies are obviously untrusted and configuration usually is not treated that way &mdash; which is precisely why configuration errors cause so many incidents.

## One habit

Instantiate settings on the first line of your application's start-up, before anything else runs.

That single placement decision is what converts a class of production incident into a failed deploy. Everything else in this module is detail around it.
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
         "body is essentially <code>errors()</code>.",
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
        "A <code>ValidationError</code> becomes a 422 whose <code>detail</code> is essentially <code>e.errors()</code> &mdash; the shape you already know how to read.",
        "Path and query parameters are validated by the same rules, and <code>loc</code> starts with <code>path</code>, <code>query</code> or <code>body</code>.",
        "<code>response_model</code> validates <em>and filters</em> the output, so a field it does not declare cannot leak from a handler that returned too much.",
        "Use separate <code>Create</code>, <code>Update</code> and <code>Out</code> models. One model with everything optional documents nothing.",
        "Your constraints, descriptions and examples are the OpenAPI document, which is the interactive docs and every generated client.",
    ],
    '''
title: Pydantic with FastAPI: Where It All Arrives
intro: Request bodies, response models and documentation, all from annotations you already wrote.
## Why this is the common entry point

Most people meet Pydantic through FastAPI, and often without realising they are two libraries. That is a compliment to the integration and it leaves a gap: everything that looks like FastAPI magic is Pydantic doing what the previous tiers described.

FastAPI has no validation layer of its own. It reads your annotations, hands the request body to a Pydantic model, converts the resulting `ValidationError` into a 422, and turns the generated JSON Schema into your documentation. That is the whole of it, and knowing where the line falls makes both easier to reason about.

## The request body

```python
@app.post("/modules/", status_code=201)
def create(module: ModuleIn):
    return {"created": module.title}
```

A parameter annotated with a model is the body. FastAPI reads the request, validates it with `model_validate_json`, and calls your handler with a real object.

By the time your code runs, `module.minutes` is an integer &mdash; even if the client sent `"8"` &mdash; and every constraint has passed. There is no checking to do at the top of the handler, which is the point.

Scalars annotated with ordinary types become query or path parameters, and the same coercion applies: `?verbose=yes` becomes `True` because of the boolean vocabulary from the coercion module.

## 422, and what it contains

When validation fails, the handler never runs. FastAPI returns 422 with a body whose `detail` is essentially `e.errors()`.

So everything from the errors module applies directly to what your API returns. `loc` is a path, and its first element is `body`, `path`, `query` or `header` &mdash; telling the caller which part of the request was wrong before naming the field within it.

That is worth showing your API's consumers. A 422 from a FastAPI service is more informative than most people realise, and clients frequently discard it and report "bad request".

If you want a different shape, an exception handler for `RequestValidationError` lets you reformat it globally &mdash; and the grouping code from the errors module drops straight in.

## response_model does two things

```python
@app.get("/users/{user_id}", response_model=UserOut)
```

It **validates** the output, which catches a handler returning the wrong shape before a client does.

And it **filters** the output to the model's fields. A handler returning a dict with `password_hash` in it produces a response without one, because `UserOut` does not declare it.

That second behaviour is a genuine security property and worth relying on deliberately. The pattern to internalise: a response model should list exactly what a caller may see, and then over-returning from a handler cannot leak. Relying instead on the handler returning precisely the right keys means every future edit to that handler is a chance to leak something.

It also fixes the schema. Without `response_model` the documentation cannot say what an endpoint returns; with it, consumers get a typed response.

## Three models, not one

The instinct is one `Module` model everywhere. Resist it, for the reasons the defaults module gave.

**Create** takes what a caller may supply. No `id` &mdash; not optional, absent &mdash; because the server assigns it.

**Update** has everything optional, and the handler applies `model_dump(exclude_unset=True)` so untouched fields stay untouched. This is the correct PATCH shape, and getting it wrong is how six columns become `None`.

**Out** declares exactly what may be seen, with server-assigned fields required.

Three small classes, each honest. One model with everything optional produces documentation that guarantees nothing and a response type no client can rely on.

## Dependencies

`Depends` composes validated values the same way:

```python
def pagination(page: int = 1, size: int = Query(default=20, le=100)) -> Page:
    return Page(page=page, size=size)

@app.get("/modules/")
def list_modules(p: Page = Depends(pagination)):
    ...
```

The dependency's parameters are validated like any others, so the constraint on `size` is enforced and documented, and every endpoint using it inherits both.

`get_settings` from the settings module is the same pattern, and being a dependency makes it overridable in tests.

## Where validation stops

The line from the validators module matters here more than anywhere.

A model checks shape and internal consistency. "Does this track exist?" is a fact about the world, and it belongs in the handler or the service layer &mdash; not least because the right response is a 404 or a 409, not a 422.

Keeping that separation means your models stay testable without a database, and your status codes stay meaningful.

## The documentation is your schema

`app.openapi()` is assembled from `model_json_schema()` for every model you used. Which means every recommendation from the schema module cashes out here:

A `Field(gt=0)` appears as a documented minimum; a validator checking the same thing appears as nothing.

A `Literal` becomes a set of choices in the docs and a union type in a generated client; a `pattern` becomes an opaque string.

A `description` appears beside the field. An `examples` entry pre-fills the interactive request form, so a first-time caller can send a working request instead of guessing.

This is the concrete payback for being specific in your annotations, and it is visible to everybody who uses your API rather than only to you.

## A note on this page

There is no server here &mdash; a browser tab cannot listen on a port. `client` calls the app through ASGI, which is the same interface uvicorn uses, so routing, validation, status codes and schema generation all behave exactly as they would in production.

The full explanation, and the one behaviour that genuinely differs, is on the [FastAPI compiler](../fastapi-lab/) page.

## Where the boundary between the two libraries falls

It is worth being able to say which library is doing what, because it changes where you look when something is wrong.

**FastAPI** decides routing, reads the request, chooses which parameters come from the path, the query and the body, calls your handler, and turns the result into a response. It also assembles the OpenAPI document.

**Pydantic** validates and converts every one of those values, produces the errors, and generates the schema for each model that goes into the document.

So a 422 you disagree with is a Pydantic question &mdash; a model's annotations, constraints or validators. A field arriving from the wrong part of the request is a FastAPI question. Documentation that is missing a constraint is a Pydantic question, because the constraint was never in the schema.

Most confusion about "FastAPI validation" resolves the moment that split is clear.

## Dependencies and settings

The settings model from the previous module composes naturally here:

```python
@lru_cache
def get_settings() -> Settings:
    return Settings()

@app.get("/health")
def health(settings: Settings = Depends(get_settings)):
    return {"env": settings.env}
```

Cached, so the environment is read and validated once rather than per request. And overridable in tests through FastAPI's dependency overrides, which is much cleaner than mutating the environment around a test.

The same pattern covers anything constructed once and used everywhere &mdash; a database session factory, a client for another service, a pagination object built from validated query parameters.

## Summary

A model parameter is the request body, validated before your handler runs. Failures become a 422 whose `detail` is `e.errors()`, with `loc` naming which part of the request was wrong.

`response_model` validates and filters the output, so undeclared fields cannot leak &mdash; a property worth relying on deliberately rather than trusting each handler to return exactly the right keys.

Separate `Create`, `Update` and `Out` models per resource. Keep facts about the world in the service layer and shape in the model. And prefer constraints to validators, because only one of them reaches the documentation your callers read.


## Mistakes people make

**No `response_model`.** The documentation cannot say what the endpoint returns, and nothing filters the output, so a handler that starts returning an extra key starts leaking it.

**One model for every direction.** Everything optional so it can serve create, update and read at once. It documents nothing, and no client can tell what is guaranteed in a response.

**Dumping the whole update model.** `patch.model_dump()` without `exclude_unset=True` writes every field, so untouched columns are overwritten with `None` or defaults. This is the bug behind "it cleared fields I never edited".

**Putting existence checks in validators.** "Does this track exist" belongs in the handler. In a model it makes validation an I/O call, makes the model untestable without a database, and returns a 422 where a 404 was correct.

**Validators instead of constraints.** Both reject the same values; only the constraint appears in the documentation and in generated clients. Your callers see one of them.

**Assuming a 422 body is opaque.** It is `e.errors()`, with `loc` naming body, path or query and then the field. A lot of clients discard it and report "bad request" when the exact problem was right there.

**Instantiating settings per request.** Reading and validating the environment on every call is wasted work. Cache it with `lru_cache` and inject it with `Depends`, which is also what makes it overridable in tests.

## A last habit

Open your own `/docs` page occasionally and read it as a consumer would.

It is generated from your models, so everything this track has argued about being specific in annotations is visible there and nowhere else in your workflow. Fields with no description. A `str` where a `Literal` belongs. An endpoint with no `response_model`, so the response section says nothing. A required field you meant to default.

None of that shows up in your tests, because your tests know what they are sending. It shows up for the person integrating with you, at the point where it is expensive to ask you about it.

Five minutes reading your own documentation catches most of it, and it is the same five minutes recommended in the schema module &mdash; just from the other end.

## Where to go from here

This is the last module in the track, and the one where everything else cashes out.

The annotations from tier one decide what a request body accepts. The shapes from tier two &mdash; nested models, collections, discriminated unions, closed sets &mdash; decide how expressive your API can be about its own data. The validators and config from tier three enforce what annotations cannot say. The serialisation and schema work from tier four decides what consumers receive and what your documentation tells them.

FastAPI adds routing and an HTTP layer on top, and almost nothing else. Which means the quality of an API built this way is very largely the quality of its models.

That is a good position to be in, because models are cheap to improve. Narrowing a `str` to a `Literal`, moving a rule from a validator to a constraint, splitting one all-optional model into three honest ones, adding a description to a field whose name is not self-explanatory &mdash; each is a small edit, and each is visible to everybody who calls you.

## One last thing to check

Before shipping an endpoint, three questions that take a minute each.

**Does it have a `response_model`?** Without one the documentation says nothing about the response, and nothing filters what a handler returns.

**Is the update path using `exclude_unset=True`?** Without it, a PATCH overwrites fields the caller never mentioned.

**Would a 422 from this endpoint tell a caller what to fix?** If a field is a bare `str` where a `Literal` belongs, or a rule lives in a validator that the schema cannot show, the answer is no &mdash; and the caller finds out by being rejected rather than by reading.

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
intro: Why v2 is fast, where the time goes, and the three habits that account for most of the difference.
## Two libraries in a trench coat

Installing `pydantic` installs two things.

A **Python layer** that reads your class, interprets the annotations, resolves types, and builds a schema describing how to validate the model. This runs once, when the class is defined.

**`pydantic-core`**, a compiled Rust engine that executes that schema against data. This runs every time you validate.

Almost everything about v2's performance follows from that split. Validation is compiled code walking a prepared schema, not Python interpreting annotations per call. Version 1 did the latter, which is why v2 was a rewrite rather than an optimisation.

It also explains details you will have noticed. Error `type` codes look like machine identifiers because they come from the core. `model_validate_json` beats parsing separately because the core parses and validates in one pass. And there is a compiled wheel per platform, because there is compiled code in there.

## Where the time actually goes

Three components, worth separating.

**Schema building** happens once per class or adapter. It is the most expensive single operation and it should be invisible &mdash; unless you build schemas repeatedly, which is the mistake below.

**Validation** happens per value. Cost scales with how much work there is: a value already of the right type is checked and passed through; one needing conversion costs more; one needing a custom validator costs the most, because that means leaving Rust for Python.

**Serialisation** is generally cheaper than validation, and follows the same shape.

## The three habits

Almost all avoidable cost comes down to three things.

### Validate once

The rule from the first module, restated as a performance point: re-validating an object that has already passed produces an identical result for the full price.

It happens more than people expect. A model validated in a request handler, passed to a service that validates it again, handed to a repository that constructs its own model from it. Each layer is defensively re-checking data that cannot have changed.

The discipline is to decide where the boundary is and trust everything past it. If a function's argument is a model, it has been validated; checking again buys nothing.

The exception is genuinely mutable data. If `validate_assignment` is off and something has been assigning freely, the object may no longer match its annotations &mdash; but the fix there is to turn on the setting or freeze the model, not to re-validate.

### Validate collections in one call

```python
[Model.model_validate(r) for r in rows]              # per item
TypeAdapter(List[Model]).validate_python(rows)       # whole list
```

Identical results. The first crosses between Python and Rust once per row; the second makes one call and loops inside the core.

For bulk work &mdash; a file import, a batch job, a large API response &mdash; this is the single most effective change available, and it is one line.

### Parse JSON directly

`model_validate_json(raw)` rather than `model_validate(json.loads(raw))`.

The two-step form builds a complete intermediate structure of Python objects, then converts it again. The direct form reads the text and constructs the final values in one pass.

As the parsing module covered, it is also better for errors and for decimal precision. Three benefits for less code.

## Validators are the expensive part

A `field_validator` is Python. Every time it runs, the core suspends, calls into the interpreter, and resumes.

For a model built a few times per request that is irrelevant. For a hundred thousand rows it is the dominant cost, and it is worth two questions.

**Could this be a constraint?** `Field(gt=0)` and a validator checking `v > 0` reject the same values, and the constraint runs in Rust. It also reaches the schema, which is the more important reason.

**Is it doing work that could be done once?** A validator that rebuilds a set of permitted values on every call is doing that per item. Hoisting it to module level is usually a bigger win than anything else in the model.

## Building schemas repeatedly

The mistake that looks like nothing in review:

```python
for row in rows:
    TypeAdapter(List[int]).validate_python(row)     # recompiles every iteration
```

Adapters belong at module level. The same applies to any pattern that defines a model class inside a function called repeatedly &mdash; each call builds a new class and a new schema.

Where the type is only known at runtime, cache the adapters in a dict keyed by type, or wrap a factory in `functools.lru_cache`.

## Keeping perspective

Two things worth saying plainly.

**Validation is usually not your bottleneck.** A model validating in single-digit microseconds sits next to a database query taking milliseconds and a network call taking hundreds. In a typical request handler, validation is a rounding error. Choosing a dataclass "for performance" in a handler that then makes three SQL queries is optimising the wrong end.

**Measure before changing anything.** The habits above are free &mdash; adopt them because they are also clearer. Anything beyond them should follow a profile, not an intuition.

The place validation genuinely dominates is bulk: large collections, file imports, high-throughput pipelines. That is where the one-call-per-collection rule earns real time.

## A note on these timings

Every measurement on this page runs on CPython compiled to WebAssembly, several times slower than a native interpreter, on one core.

The **ratios** transfer &mdash; validating a list in one call really is faster than looping, by roughly the factor shown. The **absolute seconds** do not. Do not quote them as figures for a server.

That caveat applies to any benchmark run anywhere, including ones you write yourself on your laptop. Relative comparisons under identical conditions are informative; absolute numbers are a property of the machine.

## Summary

Pydantic v2 is a Python layer that builds schemas and a Rust core that runs them, which is why validation is cheap enough to do on every request.

Three habits account for most of the avoidable cost: validate once at the boundary, validate collections in a single call, and parse JSON directly. Prefer constraints over validators where either would do, and build schemas once rather than in a loop.

Then stop, because validation is rarely the slow part, and the remaining questions belong to a profiler rather than to a rule of thumb.

## What not to optimise

A short list of things that look like performance decisions and are not.

**Choosing a dataclass over a model in a request handler.** The handler then makes three database queries. The validation was never the cost.

**Skipping validation on data from your own database.** It is cheap on already-correct types, and the guarantee is worth more than the microseconds. If a column can be null and the model says it cannot, you want to know.

**Avoiding nested models to reduce validation count.** A flat model with the same fields does the same total work; nesting is an organisational choice, not a performance one.

**Reaching for `model_construct`.** It skips validation entirely, which makes it fast and unsafe. It exists for cases where the data provably came from a trusted source &mdash; reconstructing from your own cache, say. Using it to speed up a normal path removes the property you installed the library for.

## Measuring properly

If you do need to measure, three things make the result meaningful.

**Warm up.** The first construction of a model builds its schema. Timing that alongside the validations makes the first run look terrible and tells you nothing about the steady state.

**Time the right thing.** Wrap the validation, not the loop that also builds the input data. Constructing ten thousand dictionaries is not free either.

**Compare under identical conditions.** Same machine, same process, same interpreter. Absolute numbers do not survive a move between any of those, which is why the timings on this page are presented as ratios.

`time.perf_counter` is sufficient for A-versus-B. For finding where time goes in a real application, a profiler will point at the database long before it points at validation.

## Mistakes people make

**Re-validating what has already passed.** The most common and most expensive no-op. If a function's argument is a model, it was validated; checking again produces an identical result for the full price.

**Looping in Python over a collection.** `[Model.model_validate(r) for r in rows]` crosses into Rust once per row. One call with a `TypeAdapter(List[Model])` does the loop inside the core.

**Building schemas repeatedly.** A `TypeAdapter` constructed inside a loop, or a model class defined inside a function called per request, recompiles a schema every time. Module level, once.

**Doing work inside a validator that could be done outside.** Rebuilding a set of permitted values on every call does it per item. Hoisting it is often a bigger win than anything else in the model.

**Using `model_construct` to go faster.** It skips validation entirely. That is correct for reconstructing from a provably trusted source and a way of quietly removing the guarantee everywhere else.

**Optimising validation before profiling.** In a handler that makes three database queries, validation is a rounding error. A profiler will point at the database long before it points here.

**Quoting benchmark seconds.** Absolute numbers are a property of the machine &mdash; doubly so on this page, which runs on WebAssembly. Ratios under identical conditions transfer; seconds do not.

## Why it was worth rewriting

It is worth understanding what the v2 rewrite actually bought, because it explains why this module is short.

In v1, validation was Python interpreting annotations on every call. That put Pydantic on the critical path of a lot of applications in a way that showed up in profiles, and made "is validation too slow?" a reasonable question to ask routinely.

Moving execution into Rust changed the answer from "sometimes" to "almost never". A model that validates in a few microseconds does not compete with anything else in a request.

So the practical guidance became much simpler: adopt the three habits because they are also clearer code, and otherwise stop thinking about it. That is a better place to be than a set of tuning tricks, and it is the reason most of this module is about what not to optimise.

## The honest summary

Most applications should not think about this module at all.

Adopt the three habits &mdash; validate once, validate collections in one call, parse JSON directly &mdash; because each is also clearer code than the alternative, and then stop. They are not performance tricks; they are the obvious way to write it, which happens also to be the fast way.

If something is genuinely slow, profile it. The answer will usually be I/O, and on the occasions it really is validation the answer will usually be one of the three habits not being followed, or a validator doing per-item work that belongs outside the loop.

What changed in v2 is that this stopped being a live concern for ordinary code. Validation used to be something you budgeted for; now it is something you can put at every boundary without thinking about the cost. That is a better outcome than any tuning advice.

## In one line

Validate once at the boundary, validate collections in a single call, and hand JSON straight to Pydantic &mdash; then stop thinking about it, because in v2 validation is almost never the slow part.

## A closing thought

The most useful performance property of Pydantic v2 is not that it is fast. It is that it is fast enough to stop being a consideration.

That changes how you write code. Validation at every boundary stops being a trade-off and becomes the default, which means more of your program can assume its inputs are correct &mdash; and that is worth considerably more than the microseconds.
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
intro: The renames, the behaviour changes that fail silently, and how to date a tutorial.
## Why this module exists even if you never migrate

Pydantic v1 was popular for years, and a great deal of writing about it is still the top result for many searches. Reading a v1 answer as though it describes v2 is a genuine source of confusion.

So the most useful thing here may simply be the ability to date a page.

**It is v1 if you see:** `@validator`, `@root_validator`, `.dict()`, `.json()`, `.parse_obj()`, `class Config`, `orm_mode`, `min_items`, `regex=`.

**It is v2 if you see:** `@field_validator`, `@model_validator`, `.model_dump()`, `model_config = ConfigDict(...)`, `from_attributes`, `min_length`, `pattern=`.

If a page uses the first set, treat everything in it as historical &mdash; not only the names, but the behaviour it describes.

## The renames

The mechanical part, and the easy part:

`.dict()` → `model_dump()`. `.json()` → `model_dump_json()`. `.parse_obj()` → `model_validate()`. `.parse_raw()` → `model_validate_json()`. `.schema()` → `model_json_schema()`. `.copy()` → `model_copy()`. `.construct()` → `model_construct()`. `__fields__` → `model_fields`. `__fields_set__` → `model_fields_set`.

The `model_` prefix is deliberate: it namespaces the library's methods away from your field names, which is also why Pydantic warns about fields starting with `model_`.

Most old names still exist in v2 and emit deprecation warnings. That is a kindness for migration and the reason so much code still uses them &mdash; nothing forced the change.

## Validators

`@validator` became `@field_validator`, and it now requires `@classmethod` underneath.

The signature changed too. v1 took `(cls, v, values)` where `values` was a dict of previously-validated fields; v2 takes `(cls, v, info)` and the same data is `info.data`.

`@root_validator` became `@model_validator`, and the mode is now explicit. v1's `pre=True` is `mode="before"`; the default post-validator is `mode="after"` and receives the model rather than a dict of values, returning `self`.

That last change is more than cosmetic. A v1 root validator worked with a dict; a v2 after-validator works with the finished model, so fields are converted and attribute access works.

## Config

`class Config` became `model_config = ConfigDict(...)`, with several settings renamed:

`orm_mode` → `from_attributes`. `allow_mutation = False` → `frozen=True`. `allow_population_by_field_name` → `populate_by_name`. `anystr_strip_whitespace` → `str_strip_whitespace`. `min_anystr_length` → `str_min_length`.

An inner `class Config` still works and warns. It is the single clearest signal that code has not been migrated.

## The change that bites

Everything above produces a warning or an error. This one does not:

```python
summary: Optional[str]
```

In v1 that was optional and defaulted to `None`. In v2 it is **required** and nullable &mdash; you must pass it, and you may pass `None`.

Nothing warns, because the annotation is still valid. What happens is that code which used to work starts raising `missing` at runtime, in whatever code path first constructs the model without that field.

The fix is one addition per field: `Optional[str] = None`.

The reason for the change is the one the defaults module gave: v1's implicit default hid the distinction between "may be omitted" and "may be null", which are genuinely different contracts. v2 made you say which you meant.

If you are migrating anything substantial, search for `Optional[` first. It will be the largest single source of failures.

## Constraint renames

`min_items`/`max_items` → `min_length`/`max_length`, now consistent with strings.

`regex` → `pattern`.

`allow_mutation` on a field → `frozen`.

`const=True` is gone; use `Literal[value]`.

Some v1 helper types were removed or changed too. `constr(regex=...)` becomes `Annotated[str, Field(pattern=...)]`, which is the modern spelling anyway.

## Errors

Error `type` codes were renamed wholesale. v1's `value_error.any_str.min_length` is v2's `string_too_short`. v1's `type_error.integer` is v2's `int_type` or `int_parsing` depending on the cause.

`ctx` now carries the rule's parameters, and `url` links to documentation for the type.

This is where the standing advice in this track &mdash; match on `type`, never on `msg` &mdash; comes from. Code that matched v1 message strings broke on upgrade with no warning at all, which is exactly the failure mode that advice prevents.

If you are migrating, any error-handling code is worth reviewing directly rather than trusting tests, because a broken branch that never matches will not fail loudly.

## A practical order

If you are doing this on a real codebase:

**Install v2 and run the test suite.** Deprecation warnings tell you where the renames are, and they are mechanical.

**Search for `Optional[` and add the defaults.** Largest source of genuine failures, and invisible until executed.

**Rewrite validators.** Add `@classmethod`, rename the decorators, change `values` to `info.data`, and make `mode` explicit on root validators.

**Convert `class Config` blocks**, renaming the settings that moved.

**Review error handling last**, because that is where the failures are silent.

There is a tool, `bump-pydantic`, which does the mechanical parts automatically. It is worth running first and reviewing carefully; it handles the renames well and cannot know your intent on the `Optional` question.

## What you get for it

The migration is not free, and it is worth knowing what it buys.

Validation is substantially faster, because the core is Rust rather than Python. Strict mode exists. Discriminated unions became a first-class feature. `TypeAdapter` arrived, and with it validation without a wrapper model. Error output became structured and stable. `computed_field` exists. Serialisation gained real control.

Most of this track describes features that are v2-only. If you are reading it against a v1 codebase, that is the gap.

## Things that were removed outright

A few v1 features have no v2 equivalent, and finding them late is unpleasant.

`copy_on_model_validation` is gone; the behaviour is controlled by `revalidate_instances` instead.

`GetterDict`, the customisation hook for `orm_mode`, was removed. `from_attributes` reads attributes directly, and anything more involved belongs in a `model_validator(mode="before")`.

`json_encoders` in Config is deprecated in favour of field and model serialisers, which are more precise and appear in the right place.

`parse_file` is gone. Read the file yourself and use `model_validate_json` on the bytes, which is better anyway &mdash; the errors name the position in the document.

`const=True` is gone; a `Literal` says the same thing and produces a better schema.

## Running both versions at once

For a large migration, `pydantic.v1` is available inside v2: `from pydantic.v1 import BaseModel` gives the old library alongside the new one.

That makes an incremental migration possible &mdash; move one module at a time, with both versions installed as a single package.

Two cautions. The two are not interoperable: a v1 model cannot be a field of a v2 model, and mixing them at a boundary means converting through dicts. And a dependency that has not migrated may pull in its own expectations, so check what your libraries require before assuming you can take it slowly.

It is a transitional tool. Code left half-migrated for a year tends to stay that way, and the two vocabularies side by side are genuinely confusing to read.

## Summary

Renames are mechanical and mostly warn. `Optional[X]` losing its implicit `None` is the change that fails silently, and searching for it first will save the most time.

Validators changed shape as well as name &mdash; `@classmethod`, `info.data`, explicit modes. Config moved into `model_config` with several settings renamed. Error codes were replaced wholesale, so error-handling code deserves direct review rather than trust in tests.

`bump-pydantic` handles the mechanical parts. What it cannot do is decide what you meant by `Optional`, which is precisely the part that matters.


## Mistakes people make

**Trusting the test suite to find everything.** Renames warn and errors are loud, but two categories fail quietly: `Optional` fields that are now required, and error-handling branches matching v1 codes that simply never match again. Neither necessarily fails a test.

**Running `bump-pydantic` and shipping.** It handles the mechanical renames well and cannot know what you meant by `Optional[X]`. Review its output rather than treating it as a migration.

**Migrating models and not validators.** A `@validator` still importable from `pydantic` in v2 is the deprecated shim. The signature changed &mdash; `values` became `info.data` &mdash; and a validator reading the wrong argument name will not behave as it did.

**Leaving `class Config` because it still works.** It warns rather than failing, so it survives indefinitely, and it is the single clearest marker of code that has not really been migrated.

**Living in `pydantic.v1` permanently.** The compatibility import exists for a transition. Two vocabularies side by side in one codebase are genuinely confusing, and half-migrated code tends to stay that way.

**Reading v1 answers as v2.** The most common problem for people who never migrate anything. Check for `@validator`, `.dict()` and `class Config` before trusting a page &mdash; the behaviour it describes has changed too, not only the spelling.

## Deciding whether to migrate

If you are on v1 and wondering whether it is worth it, the honest position.

v1 is no longer developed and receives only security fixes. The ecosystem has moved: FastAPI, LangChain, SQLModel and most libraries that integrate with Pydantic now target v2, and staying on v1 increasingly means pinning things around it.

Against that, the migration is real work on a large codebase, and it is work with no visible feature at the end of it.

The pragmatic answer for most teams is to migrate when something else forces the question &mdash; a dependency that needs v2, or a piece of work that touches the models anyway &mdash; rather than as a standalone project. The `pydantic.v1` compatibility import exists to make that gradual approach viable.

What is not viable is starting new code on v1. Everything in this track past the first tier is v2, and the gap widens.

## Where this leaves the track

That is the last module. Thirty of them, from a type annotation that does nothing at runtime to an API whose documentation writes itself.

The through-line has been one idea: **be specific at the boundary, once**. Specific enough that the annotation says what you mean, that the constraint reaches the schema, that the error names the field, and that everything downstream can stop defending itself.

Everything else has been mechanism. Coercion rules so text can arrive as text. Validators for the rules types cannot hold. Serialisation so output is data rather than presentation. Schemas so other tools can read what you already wrote.

The version history matters here only because v2 is where most of that became true. If you are reading this against a v1 codebase, the gap is not stylistic.

## A migration checklist

Condensed, in the order that finds problems soonest.

Install v2 and run the suite. Fix what fails loudly &mdash; imports, removed arguments, renamed helpers.

Search `Optional[` and add `= None` wherever the field was meant to be omissible. Largest source of silent breakage.

Rewrite validators: `@field_validator` with `@classmethod`, `@model_validator` with an explicit mode, `values` becomes `info.data`.

Convert `class Config` blocks, renaming `orm_mode`, `allow_mutation` and the `anystr_` family.

Rename constraint arguments: `min_items`, `max_items`, `regex`.

Review error handling by hand. Anything matching v1 type codes or message text has stopped matching, silently, and tests may not notice.

Then remove the deprecated method names once the warnings are the only thing left.

## If you are only reading, not migrating

The most common use of this module is not migration at all &mdash; it is dating an answer you found while looking for something else.

That skill is worth more than it sounds. A confident, well-written, highly-ranked answer describing v1 behaviour will send you in the wrong direction for an afternoon, and nothing about it announces its age.

The tell is the vocabulary. `@validator`, `.dict()`, `class Config`, `orm_mode`, `min_items`, `regex=`. Any one of those means the page predates v2, and the behaviour it describes may have changed as well as the spelling &mdash; `Optional` being the sharpest example, since the code will look correct and simply not work.
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
