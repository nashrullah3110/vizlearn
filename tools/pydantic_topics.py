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


def topic(slug, title, cat, lead, svg, steps, notes, article, check):
    """One module. `steps` is a list of (heading, blurb, code) triples."""
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "steps": steps, "notes": notes, "article": article, "check": check,
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
