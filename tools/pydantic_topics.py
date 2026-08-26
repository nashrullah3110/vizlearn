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
