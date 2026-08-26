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
