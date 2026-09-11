# -*- coding: utf-8 -*-
"""The Python-semantics questions.

The "do you actually know Python" round: the questions an interviewer asks to
find out whether you have read the language or only used it. They are ordered
roughly by how often they come up.

Every `viz` here is built by running the thing it draws - see
tools/interview_viz.py for why that matters. For these questions "running it"
usually means recording the state of names and objects rather than moving a
pointer along an array, which is what the conceptual string questions already
do.
"""

import copy as _copy
import inspect as _inspect

from interview_viz import cost_table, frame, marked, pairs, row, cell, viz

SEMANTICS = []


def _q(**kw):
    SEMANTICS.append(kw)


# =========================================================================
# 1. yield
# =========================================================================

def _yield_frames():
    """Recorded by actually driving a generator through its states."""
    def countdown(n):
        while n > 0:
            yield n
            n -= 1

    out = []
    g = countdown(3)
    out.append(frame(
        pairs([("g", "<generator>"), ("state", _inspect.getgeneratorstate(g)),
               ("body executed", "nothing yet"), ("values seen", "-")],
              {"state": "lo"}, label="the generator object"),
        "Calling countdown(3) ran none of the body. It built a generator "
        "object and stopped - GEN_CREATED means the frame exists and has "
        "never started.",
        {"resumed": 0}))

    seen = []
    for step in range(3):
        v = next(g)
        seen.append(v)
        out.append(frame(
            pairs([("g", "<generator>"), ("state", _inspect.getgeneratorstate(g)),
                   ("body executed", "up to the yield"),
                   ("values seen", ", ".join(str(x) for x in seen))],
                  {"state": "hi", "values seen": "hit"},
                  label="the generator object"),
            "next(g) ran the body until it hit `yield %d`, handed that value "
            "back, and froze there. GEN_SUSPENDED is a paused stack frame "
            "holding n = %d." % (v, v - 1),
            {"resumed": step + 1}))

    try:
        next(g)
    except StopIteration:
        pass
    out.append(frame(
        pairs([("g", "<generator>"), ("state", _inspect.getgeneratorstate(g)),
               ("body executed", "to the end"),
               ("values seen", ", ".join(str(x) for x in seen))],
              {"state": "done"}, label="the generator object"),
        "The while condition failed, the body returned, and the next call "
        "raised StopIteration. GEN_CLOSED is terminal: a generator is "
        "one-shot, and iterating it again yields nothing.",
        {"resumed": 4}))
    return viz(out)


_q(
    slug="what-does-yield-actually-do",
    kind="concept",
    level="Easy",
    title="What does `yield` actually do?",
    asked="What does yield do, and how is a generator different from a "
          "function that returns a list?",
    desc="What yield actually does to a function: a generator is a paused "
         "stack frame, produced lazily, one-shot, and constant in memory "
         "whatever the length of the sequence.",
    lead="<code>yield</code> turns the function into a <strong>factory for "
         "paused stack frames</strong>. Calling it runs nothing; each "
         "<code>next()</code> runs the body up to the next yield and freezes "
         "it there. The sequence is produced on demand, so memory is constant "
         "in the length &mdash; and it can only be walked once.",
    say="\"A function with yield returns a generator instead of running. Each "
        "next() resumes the body until the next yield, so values are produced "
        "lazily and memory stays constant however long the sequence is. The "
        "trade is that it is one-shot and has no len() - if I need to iterate "
        "twice or index it, I need a list.\"",
    notice=[
        "Calling the function runs <em>none</em> of the body &mdash; the state "
        "starts at <code>GEN_CREATED</code>.",
        "Each resume ends at a <code>yield</code>, which is why the frame is "
        "<em>suspended</em> rather than finished.",
        "<code>GEN_CLOSED</code> is terminal: iterating again produces nothing, "
        "silently.",
    ],
    viz=_yield_frames(),
    sections=[
        ("A generator is a paused frame",
         "<p>An ordinary function runs to a <code>return</code> and its stack "
         "frame is destroyed. A function containing <code>yield</code> does not "
         "run at all when you call it: you get a generator object that owns a "
         "frame which has never started.</p>"
         "<p>Every <code>next()</code> resumes that frame, runs until the next "
         "<code>yield</code>, hands back the value, and freezes the frame "
         "again &mdash; local variables, instruction pointer and all. That is "
         "the whole mechanism, and it is why <code>yield</code> can appear in "
         "the middle of a loop and still work: the loop variable survives "
         "between resumes because the frame was never torn down.</p>"),
        ("What laziness buys, in one number",
         "<p>The list version of a million squares allocates a million "
         "integers and a million pointers before you read the first one. The "
         "generator version allocates one object with a frame in it, and the "
         "editor below prints both sizes: a few megabytes against about a "
         "hundred bytes.</p>"
         "<p>The other half is <em>latency</em>. A generator can hand you its "
         "first item immediately, which matters when the sequence is being "
         "read from a file or a network, and matters absolutely when the "
         "sequence is infinite. <code>itertools.count()</code> is a valid "
         "generator and an impossible list.</p>"),
        ("The three things you give up",
         "<p><strong>It is one-shot.</strong> Once exhausted, it stays "
         "exhausted, and a second <code>for</code> loop over it runs zero "
         "times without error. This is the bug people actually hit: passing a "
         "generator to two functions and finding the second one saw an empty "
         "sequence.</p>"
         "<p><strong>No <code>len()</code>, no indexing, no slicing.</strong> "
         "The length is not known without running it, so there is nothing to "
         "report. <code>itertools.islice</code> is the slicing replacement.</p>"
         "<p><strong>Exceptions surface late.</strong> A generator that will "
         "raise on its fourth item raises on the fourth <code>next()</code>, "
         "which may be a long way from where it was created &mdash; inside a "
         "different function, or after a <code>with</code> block has already "
         "closed the file it was reading.</p>"),
        ("The follow-up you should expect",
         "<p>\"What is the difference between a generator and an iterator?\" An "
         "iterator is the protocol &mdash; anything with <code>__next__</code> "
         "and <code>__iter__</code>. A generator is the easiest way to get one, "
         "written as a function instead of a class. Every generator is an "
         "iterator; most iterators in real code are generators.</p>"
         "<p>And \"what does a generator expression change?\" Nothing but the "
         "syntax: <code>(x*x for x in xs)</code> is the same object as the "
         "equivalent <code>yield</code> function, which is worth knowing "
         "because it means <code>sum(x*x for x in xs)</code> never builds the "
         "list at all.</p>"),
    ],
    code={
        "file": "generators.py",
        "intro": "The three states, the one-shot exhaustion, and the memory "
                 "difference at a million items - printed rather than asserted.",
        "code": '''# What yield does: build a paused frame, resume it on demand.
import inspect, sys

def countdown(n):
    print("  [the body starts only now]")
    while n > 0:
        yield n
        n -= 1

g = countdown(3)
print("calling it returned a:", type(g).__name__)
print("state:", inspect.getgeneratorstate(g))

print("first next() ->", next(g))
print("state:", inspect.getgeneratorstate(g))
print("the rest:", list(g))
print("state:", inspect.getgeneratorstate(g))

try:
    next(g)
except StopIteration:
    print("exhausted: a generator is one-shot")

# The bug that follows from one-shot: the second consumer sees nothing.
squares = (i * i for i in range(5))
print()
print("sum once :", sum(squares))
print("sum again:", sum(squares), "<- not zero by accident; it is empty")

# --- what laziness costs, and saves -------------------------------------
print()
print("memory for a million squares:")
as_list = [i * i for i in range(1_000_000)]
as_gen = (i * i for i in range(1_000_000))
print("  list     ", f"{sys.getsizeof(as_list):>9,}", "bytes")
print("  generator", f"{sys.getsizeof(as_gen):>9,}", "bytes")
print("  ratio    ", f"{sys.getsizeof(as_list) / sys.getsizeof(as_gen):>9,.0f}x")
''',
        "walk": [
            ("g = countdown(3)",
             "No output from the body appears on this line. The call builds a "
             "generator and returns; the <code>print</code> inside the function "
             "has not run."),
            ("inspect.getgeneratorstate(g)",
             "<code>GEN_CREATED</code>, then <code>GEN_SUSPENDED</code> after a "
             "resume, then <code>GEN_CLOSED</code>. The state is the frame's, "
             "not the value's."),
            ("sum(squares)",
             "The second call returns 0. Nothing raised, nothing warned &mdash; "
             "the generator was already closed, so the loop ran zero times. "
             "This is the one-shot bug in its natural habitat."),
            ("sys.getsizeof(as_gen)",
             "About a hundred bytes, and it does not depend on the million. "
             "<code>getsizeof</code> on the list excludes the integers it "
             "points at, so the real gap is larger still."),
        ],
        "try": [
            "Replace <code>list(g)</code> with a second <code>next(g)</code> and "
            "watch the state stay <code>GEN_SUSPENDED</code> until the body "
            "actually returns.",
            "Add <code>len(as_gen)</code>. The <code>TypeError</code> is the "
            "point: the length is not knowable without running it.",
            "Wrap the generator in <code>itertools.tee(as_gen, 2)</code> to get "
            "two independent iterators &mdash; and note it buffers, so it trades "
            "the memory back.",
        ],
    },
    check=[
        {"q": "What does calling a function containing yield do?",
         "options": ["Runs the body and returns a list",
                     "Returns a generator object without running the body",
                     "Runs the body up to the first yield",
                     "Raises unless you iterate it"],
         "answer": 1,
         "why": "The call builds a generator that owns a frame which has never "
                "started. The body runs on the first next(), not on the call."},
        {"q": "Why does iterating a generator a second time produce nothing?",
         "options": ["It is cached",
                     "The frame is closed once the body returns, and that is terminal",
                     "It raises StopIteration immediately",
                     "Only generator expressions behave this way"],
         "answer": 1,
         "why": "GEN_CLOSED is a final state. The second loop runs zero times "
                "and does not error, which is what makes it a hard bug to see."},
        {"q": "The memory advantage of a generator comes from:",
         "options": ["Compression",
                     "Producing items on demand instead of storing them all",
                     "Using C instead of Python",
                     "Reusing one integer object"],
         "answer": 1,
         "why": "Only the current item and the frame exist at any moment, so "
                "the footprint is constant in the length of the sequence."},
        {"q": "Which of these does a generator NOT support?",
         "options": ["for loops", "len()", "next()", "being passed to sum()"],
         "answer": 1,
         "why": "The length is not known without running it to the end, so "
                "there is nothing for len() to report."},
    ],
)


# =========================================================================
# 2. the mutable default argument
# =========================================================================

def _default_frames():
    """Recorded by actually calling the buggy function three times."""
    def collect(item, into=[]):
        into.append(item)
        return into

    out = [frame(
        pairs([("collect.__defaults__[0]", "[]"), ("built", "once, at def time"),
               ("calls so far", "0")], {"built": "lo"},
              label="the default object"),
        "The default is evaluated when the `def` runs, not when the function "
        "is called. One list object now exists and belongs to the function.",
        {"calls": 0, "length": 0})]

    for i, item in enumerate("abc"):
        got = collect(item)
        out.append(frame(
            [pairs([("collect.__defaults__[0]", repr(got)),
                    ("built", "once, at def time"),
                    ("calls so far", str(i + 1))],
                   {"collect.__defaults__[0]": "hit"},
                   label="the default object"),
             marked(list(got), {j: "done" for j in range(len(got))},
                    label="what the caller got back")],
            "collect(%r) appended to the SAME list the last call appended to. "
            "The caller asked for a fresh one and got the accumulated one."
            % item,
            {"calls": i + 1, "length": len(got)}))

    def collect_ok(item, into=None):
        if into is None:
            into = []
        into.append(item)
        return into

    results = [collect_ok(ch) for ch in "abc"]
    out.append(frame(
        pairs([("into=None", "the sentinel"),
               ("call 1", repr(results[0])), ("call 2", repr(results[1])),
               ("call 3", repr(results[2]))],
              {"into=None": "done", "call 3": "hit"}, label="the fix"),
        "With None as the default, the list is built inside the body, so each "
        "call gets its own. Three calls, three lists, no shared state.",
        {"calls": 3, "length": 1}))
    return viz(out)


_q(
    slug="the-mutable-default-argument",
    kind="concept",
    level="Medium",
    title="Why does this default argument remember?",
    asked="What does def f(x, acc=[]) do on the second call, and why?",
    desc="Why a mutable default argument is shared across calls: the default "
         "is evaluated once when def runs, and the fix is a None sentinel.",
    lead="Because the default is evaluated <strong>once, when the "
         "<code>def</code> statement runs</strong> &mdash; not on each call. "
         "One list is created, attached to the function object, and reused by "
         "every call that does not pass its own, so mutations accumulate "
         "across calls. The fix is <code>None</code> as the default and build "
         "the real value inside the body.",
    say="\"Defaults are evaluated once at definition time, so a mutable "
        "default is one shared object for the life of the function. The second "
        "call sees what the first one appended. I use None as the sentinel and "
        "create the list inside the function.\"",
    notice=[
        "The list exists before any call &mdash; it is stored on "
        "<code>f.__defaults__</code>.",
        "Each call appends to the <em>same</em> object, so the return value "
        "grows.",
        "The <code>None</code> version builds a new list per call, which is "
        "what the caller expected all along.",
    ],
    viz=_default_frames(),
    sections=[
        ("Defaults are evaluated once",
         "<p>A <code>def</code> statement is executable code. When it runs, "
         "Python evaluates the default expressions and stores the resulting "
         "objects on the function &mdash; you can read them back from "
         "<code>f.__defaults__</code>. They are not re-evaluated per call, "
         "because there is nothing left to evaluate.</p>"
         "<p>For an immutable default that distinction is invisible: sharing "
         "one <code>0</code> or one <code>\"\"</code> between calls has no "
         "consequences, because nothing can change it. For a list, a dict, a "
         "set or a class instance it is the whole bug, because the shared "
         "object accumulates every mutation any call makes.</p>"),
        ("The sentinel, and why None",
         "<p>The fix is two lines:</p>"
         "<pre><code>def collect(item, into=None):\n"
         "    if into is None:\n"
         "        into = []</code></pre>"
         "<p>Now the list is built by the body, so each call gets its own. "
         "<code>None</code> is the conventional sentinel because it is a "
         "singleton and <code>is None</code> is unambiguous.</p>"
         "<p>Use a private sentinel object instead when <code>None</code> is a "
         "legitimate value a caller might pass &mdash; "
         "<code>_MISSING = object()</code>, then <code>if into is "
         "_MISSING</code>. That distinction matters for wrappers and "
         "configuration functions where \"not given\" and \"given as None\" "
         "mean different things.</p>"),
        ("Where it actually bites",
         "<p>Almost never with a literal <code>[]</code>, because that is the "
         "version everybody has been warned about. It bites through things that "
         "do not look like defaults at all:</p>"
         "<p><code>def f(when=datetime.now())</code> freezes one timestamp at "
         "import time and returns it forever, which is the same bug wearing a "
         "clock. <code>def f(cfg={})</code> in a class body gives every "
         "instance the same dictionary. And a default whose value comes from a "
         "module-level mutable &mdash; <code>def f(opts=DEFAULT_OPTS)</code> "
         "&mdash; hands callers a reference they can mutate for everyone.</p>"
         "<p>The general rule that covers all of them: a default should be an "
         "immutable value, or <code>None</code>.</p>"),
        ("Why the language does not just fix it",
         "<p>Re-evaluating defaults per call would make every call pay for the "
         "expression, and it would make the value depend on when the call "
         "happened rather than on the definition &mdash; which is its own class "
         "of surprise. Early binding is also what makes the "
         "<code>lambda i=i: i</code> trick work for "
         "<a href=\"closures-and-late-binding.html\">late-bound closures</a>, "
         "where evaluating once at definition time is exactly the behaviour you "
         "want. It is a consistent rule that is wrong for one kind of value, "
         "rather than an oversight.</p>"),
    ],
    code={
        "file": "defaults.py",
        "intro": "The accumulation, the shared object read straight off the "
                 "function, and the two-line fix - plus the same bug wearing a "
                 "clock.",
        "code": '''# The default is built once, when the def runs.
def collect(item, into=[]):
    into.append(item)
    return into

print("first  call:", collect("a"))
print("second call:", collect("b"))
print("third  call:", collect("c"))

# It is not hidden state - it is stored on the function object.
print("collect.__defaults__ ->", collect.__defaults__)
print("the same list every time:", collect.__defaults__[0] is collect("d"))

# --- the fix -------------------------------------------------------------
def collect_ok(item, into=None):
    if into is None:                 # build it per call, in the body
        into = []
    into.append(item)
    return into

print()
print("fixed, first :", collect_ok("a"))
print("fixed, second:", collect_ok("b"))
print("and passing your own still works:", collect_ok("c", ["x"]))

# --- the same bug wearing a clock ---------------------------------------
import time

def stamped(value, at=time.time()):   # frozen at import time
    return (value, at)

first = stamped("one")
time.sleep(0.05)
second = stamped("two")
print()
print("same timestamp for both calls:", first[1] == second[1])
print("because time.time() ran once, when def ran")
''',
        "walk": [
            ("into=[]",
             "Evaluated when the <code>def</code> executes. From then on there "
             "is exactly one list, owned by the function."),
            ("collect.__defaults__",
             "The shared object, readable from outside. Printing it is what "
             "turns \"mysterious behaviour\" into \"an object with a value\"."),
            ("if into is None:",
             "The sentinel check. <code>is</code> rather than <code>==</code> "
             "because <code>None</code> is a singleton and a caller's object "
             "might define a surprising <code>__eq__</code>."),
            ("at=time.time()",
             "The same rule with no list in sight. One timestamp, captured at "
             "definition time, returned by every call &mdash; which is how this "
             "bug reaches production."),
        ],
        "try": [
            "Call <code>collect(\"z\", [])</code> between two bare calls. Passing "
            "your own argument leaves the shared default untouched, which is why "
            "the bug hides in tests that always pass one.",
            "Change the default to <code>into=()</code> and watch it raise "
            "instead. An immutable default cannot accumulate &mdash; it can only "
            "fail loudly, which is better.",
        ],
    },
    check=[
        {"q": "When is a default argument expression evaluated?",
         "options": ["On every call",
                     "Once, when the def statement runs",
                     "On the first call only",
                     "When the module is garbage collected"],
         "answer": 1,
         "why": "The def statement evaluates the defaults and stores the "
                "objects on the function, so there is nothing left to "
                "re-evaluate per call."},
        {"q": "Why is def f(x=0) harmless while def f(x=[]) is not?",
         "options": ["Integers are faster",
                     "The int is immutable, so sharing one between calls has no consequences",
                     "0 is falsy",
                     "Python special-cases numbers"],
         "answer": 1,
         "why": "Both are shared. Only the mutable one can accumulate changes, "
                "so only the mutable one is a bug."},
        {"q": "The conventional fix is:",
         "options": ["Copy the default at the top of the body",
                     "Use None as the default and build the value in the body",
                     "Declare the argument global",
                     "Use a tuple instead and convert it"],
         "answer": 1,
         "why": "None is an immutable singleton, so the shared default is "
                "harmless, and the real value is created per call."},
        {"q": "Why prefer a private sentinel over None in some APIs?",
         "options": ["It is faster",
                     "Because None may be a legitimate value the caller wants to pass",
                     "None cannot be compared with is",
                     "Sentinels are required by type checkers"],
         "answer": 1,
         "why": "If None is meaningful input, you cannot use it to mean \"not "
                "given\". _MISSING = object() distinguishes the two."},
    ],
)


# =========================================================================
# 3. is versus ==
# =========================================================================

def _identity_frames():
    """Recorded from real identity comparisons, including the folding trap."""
    a, b = int("256"), int("256")
    c, d = int("257"), int("257")
    e = 257
    f = 257
    out = [frame(
        pairs([("a = int('256')", "256"), ("b = int('256')", "256"),
               ("a == b", str(a == b)), ("a is b", str(a is b))],
              {"a is b": "hit"}, label="small integers"),
        "Both names point at the same object, because CPython pre-creates the "
        "integers from -5 to 256 and hands out the cached one. `is` is True "
        "here as an implementation detail, not a language rule.",
        {"objects": 1}),
        frame(
        pairs([("c = int('257')", "257"), ("d = int('257')", "257"),
               ("c == d", str(c == d)), ("c is d", str(c is d))],
              {"c is d": "bad"}, label="past the cache"),
        "257 is one past the cache, so each int() built its own object. Equal "
        "values, different identities - which is the whole distinction.",
        {"objects": 2}),
        frame(
        pairs([("e = 257", "257"), ("f = 257", "257"),
               ("e == f", str(e == f)), ("e is f", str(e is f))],
              {"e is f": "lo"}, label="the trap in the demo"),
        "Written as literals in one code block, the compiler folds them into "
        "ONE constant, so `is` is True again - for a third reason unrelated to "
        "the cache. This is why the classic demo is unreliable.",
        {"objects": 1}),
        frame(
        pairs([("x = [1, 2]", "[1, 2]"), ("y = [1, 2]", "[1, 2]"),
               ("x == y", "True"), ("x is y", "False")],
              {"x == y": "done", "x is y": "bad"}, label="the rule that holds"),
        "Two equal lists, two objects. `==` asks about value and `is` asks "
        "about identity; they agree only by coincidence, and the coincidences "
        "are interpreter details.",
        {"objects": 2})]
    return viz(out)


_q(
    slug="is-versus-equals",
    kind="concept",
    level="Medium",
    title="`is` vs `==`, and why 257 is not 257",
    asked="What is the difference between is and ==, and why does `a is b` "
          "sometimes surprise you with integers?",
    desc="Identity versus equality in Python: what the small-integer cache "
         "does, why constant folding makes the classic demo lie, and the only "
         "places is belongs.",
    lead="<code>==</code> asks \"same value\", <code>is</code> asks \"same "
         "object\". They coincide for small integers and short strings because "
         "CPython <strong>caches</strong> those objects, and they coincide for "
         "repeated literals because the compiler <strong>folds</strong> them "
         "&mdash; two different accidents, neither of which the language "
         "promises. Use <code>is</code> only for singletons.",
    say="\"== compares values through __eq__; is compares object identity. "
        "They agree on small ints and interned strings because CPython caches "
        "them, which is an implementation detail I would never rely on. I use "
        "is only for None, True, False and sentinel objects.\"",
    notice=[
        "<code>int('256')</code> twice gives one object; "
        "<code>int('257')</code> gives two.",
        "Writing <code>257</code> twice as literals gives one object again "
        "&mdash; that is the compiler, not the cache.",
        "For lists, <code>==</code> and <code>is</code> never agree unless you "
        "aliased deliberately.",
    ],
    viz=_identity_frames(),
    sections=[
        ("Two different questions",
         "<p><code>a == b</code> calls <code>a.__eq__(b)</code>, which a type "
         "defines however it likes. <code>a is b</code> compares the addresses "
         "of the two objects and cannot be overridden by anything.</p>"
         "<p>So <code>==</code> is a question about values and <code>is</code> "
         "is a question about storage. Confusing them usually works, which is "
         "the problem: the code passes its tests on small inputs and fails on a "
         "value that happens to fall outside a cache.</p>"),
        ("The small-integer cache, and the folding on top of it",
         "<p>CPython pre-creates every integer from &minus;5 to 256 at startup "
         "and hands out the same object whenever one is needed. So "
         "<code>int('256') is int('256')</code> is <code>True</code> and "
         "<code>int('257') is int('257')</code> is <code>False</code>.</p>"
         "<p>There is a second, separate mechanism that makes this hard to "
         "demonstrate. Constants written in one code block are folded by the "
         "compiler, so <code>e = 257; f = 257</code> puts <em>one</em> constant "
         "in the code object and <code>e is f</code> is <code>True</code> "
         "&mdash; nothing to do with the cache, and it is why the same "
         "experiment gives different answers in a script and at a REPL "
         "prompt.</p>"
         "<p>Short strings that look like identifiers get the same treatment "
         "through interning. The lesson is not the boundaries; it is that these "
         "are decisions an interpreter is free to change.</p>"),
        ("Where is belongs",
         "<p>Three cases, and essentially nothing else.</p>"
         "<p><strong>Singletons.</strong> <code>x is None</code>, "
         "<code>x is True</code>, <code>x is False</code>. There is exactly one "
         "of each, so identity is the correct test and it is faster than "
         "<code>==</code> besides.</p>"
         "<p><strong>Sentinels.</strong> <code>_MISSING = object()</code>, then "
         "<code>if arg is _MISSING</code>. The whole point of the object is that "
         "nothing else can be it.</p>"
         "<p><strong>Genuine aliasing questions.</strong> \"Are these two names "
         "the same list?\" is an identity question, and it is what you want when "
         "checking whether a caller handed you the object you already hold.</p>"),
        ("The follow-up: `==` that disagrees with itself",
         "<p>\"Can <code>x == x</code> be False?\" Yes. "
         "<code>float('nan') == float('nan')</code> is <code>False</code> by "
         "IEEE rule, and so is <code>nan == nan</code> for the same object "
         "&mdash; while <code>nan is nan</code> is <code>True</code>. That is "
         "the cleanest possible demonstration that the two operators are "
         "answering different questions, and it is why <code>x in "
         "[float('nan')]</code> can be True: the container check tries "
         "<code>is</code> first as a shortcut.</p>"),
    ],
    code={
        "file": "identity.py",
        "intro": "The cache boundary, the folding that hides it, and the nan "
                 "case where equality and identity openly disagree.",
        "code": '''# == asks about value. is asks about identity. They are not the same.
a, b = int("256"), int("256")      # built at runtime, so no constant folding
c, d = int("257"), int("257")
print("256:  a == b", a == b, "| a is b", a is b, " <- cached")
print("257:  c == d", c == d, "| c is d", c is d, " <- past the cache")

# The trap in every version of this demo: literals in ONE block are folded
# into one constant, which makes `is` True for a different reason.
e = 257
f = 257
print("literals: e is f", e is f, " <- the compiler, not the cache")

# Lists are never shared implicitly.
x, y = [1, 2], [1, 2]
print()
print("lists: x == y", x == y, "| x is y", x is y)
y = x                               # NOW they are the same object
print("after y = x:      x is y", x is y)

# Where identity is the right question.
print()
print("None is a singleton, so `is None` is correct:", None is None)
MISSING = object()
print("a sentinel is only ever itself:", MISSING is object())

# And the case where the two operators openly disagree.
nan = float("nan")
print()
print("nan == nan:", nan == nan, "  <- IEEE says not equal to itself")
print("nan is nan:", nan is nan, "   <- but it is the same object")
print("nan in [nan]:", nan in [nan], " <- `in` tries identity first")
''',
        "walk": [
            ("int(\"256\") / int(\"257\")",
             "Built at runtime so the compiler cannot fold them. This is the "
             "only reliable way to see the cache boundary."),
            ("e = 257; f = 257",
             "<code>True</code>, and not because of the cache. One constant in "
             "the code object serves both names, which is why this experiment "
             "behaves differently in a file and at a prompt."),
            ("MISSING is object()",
             "<code>False</code>: every <code>object()</code> call makes a new "
             "one. That is exactly the property a sentinel needs."),
            ("nan in [nan]",
             "<code>True</code> while <code>nan == nan</code> is "
             "<code>False</code>, because <code>in</code> short-circuits on "
             "identity. The two operators are answering different questions and "
             "here you can see both answers at once."),
        ],
        "try": [
            "Change 257 to 256 in the <code>int()</code> lines and watch "
            "<code>is</code> flip. Then try &minus;6, which is one below the "
            "cache at the other end.",
            "Compare <code>\"hello\" is \"hello\"</code> with "
            "<code>\"hello world\" is \"hello world\"</code>. Identifier-like "
            "strings are interned; ones with a space often are not.",
        ],
    },
    check=[
        {"q": "What does `is` compare?",
         "options": ["Values, using __eq__",
                     "Object identity, which cannot be overridden",
                     "Types",
                     "Hashes"],
         "answer": 1,
         "why": "It compares whether the two names refer to the same object. "
                "No type can change its behaviour."},
        {"q": "Why is int('257') is int('257') False?",
         "options": ["257 is not hashable",
                     "Only integers from -5 to 256 are cached, so each call built a new object",
                     "int() always returns a new object",
                     "It is a bug"],
         "answer": 1,
         "why": "CPython pre-creates a small range of integers. Outside it, "
                "equal values are separate objects."},
        {"q": "Why does e = 257; f = 257; e is f give True?",
         "options": ["The cache extends further for literals",
                     "The compiler folds repeated constants in one code block into one object",
                     "Assignment always aliases",
                     "It does not"],
         "answer": 1,
         "why": "A second, unrelated mechanism. It is why the classic demo "
                "gives different answers depending on how you run it."},
        {"q": "When should you use `is`?",
         "options": ["For all comparisons, it is faster",
                     "For None, True, False and sentinel objects",
                     "For strings and numbers",
                     "Never"],
         "answer": 1,
         "why": "Singletons and sentinels are the cases where identity is "
                "genuinely the question being asked."},
    ],
)


# =========================================================================
# 4. shallow versus deep copy
# =========================================================================

def _copy_frames():
    """Recorded by performing the copies and the mutation."""
    original = [[1, 2], [3, 4]]
    shallow = _copy.copy(original)
    deep = _copy.deepcopy(original)
    out = [frame(
        pairs([("original", repr(original)),
               ("shallow is original", str(shallow is original)),
               ("deep is original", str(deep is original))],
              {"original": "lo"}, label="three names"),
        "Both copies are new outer lists - neither is the original. So far "
        "copy.copy and copy.deepcopy look identical.",
        {"outer objects": 3}),
        frame(
        pairs([("original[0] is shallow[0]", str(original[0] is shallow[0])),
               ("original[0] is deep[0]", str(original[0] is deep[0]))],
              {"original[0] is shallow[0]": "bad",
               "original[0] is deep[0]": "done"},
              label="the inner lists"),
        "Here they diverge. The shallow copy copied the outer list and reused "
        "the SAME inner lists; deepcopy rebuilt them.",
        {"outer objects": 3})]
    original[0].append(99)
    out.append(frame(
        [marked(original, {0: "hit"}, label="original after append(99)"),
         marked(shallow, {0: "bad"}, label="shallow"),
         marked(deep, {0: "done"}, label="deep")],
        "Appending to original[0] changed what the shallow copy sees, because "
        "it is the same object. The deep copy is untouched.",
        {"outer objects": 3}))
    sliced = original[:]
    out.append(frame(
        pairs([("original[:]", "a new outer list"),
               ("original[0] is original[:][0]",
                str(original[0] is sliced[0])),
               ("list(original)", "also shallow"),
               ("dict.copy()", "also shallow")],
              {"original[0] is original[:][0]": "bad"},
              label="everything else is shallow too"),
        "Slicing, list(), dict.copy() and set.copy() are all one level deep. "
        "If you did not call deepcopy, you have a shallow copy.",
        {"outer objects": 4}))
    return viz(out)


_q(
    slug="shallow-versus-deep-copy",
    kind="concept",
    level="Medium",
    title="Shallow copy vs deep copy",
    asked="What is the difference between a shallow and a deep copy, and which "
          "one does list(x) give you?",
    desc="What a shallow copy actually copies, why slicing and list() are "
         "shallow, when deepcopy is the answer and what it costs.",
    lead="A shallow copy builds a <strong>new container holding the same "
         "objects</strong>. A deep copy rebuilds the objects too, recursively. "
         "Slicing, <code>list()</code>, <code>dict.copy()</code> and "
         "<code>copy.copy()</code> are all shallow &mdash; so mutating a nested "
         "value through one name is visible through the other.",
    say="\"A shallow copy copies the outer container and shares the contents, "
        "so nested mutation leaks between them. copy.deepcopy rebuilds the "
        "whole tree. Slicing and list() are shallow, which is fine for flat "
        "data and a bug for nested data.\"",
    notice=[
        "Both copies are new <em>outer</em> objects &mdash; that part is not the "
        "difference.",
        "The shallow copy shares the inner lists, which is where the mutation "
        "leaks.",
        "<code>original[:]</code> and <code>list(original)</code> behave "
        "exactly like <code>copy.copy</code>.",
    ],
    viz=_copy_frames(),
    sections=[
        ("What \"shallow\" means precisely",
         "<p>A shallow copy allocates a new container and fills it with the "
         "<em>same references</em> the original holds. So the outer objects are "
         "independent &mdash; appending to the copy does not lengthen the "
         "original &mdash; and every element is shared.</p>"
         "<p>For flat data that distinction never appears. A list of integers "
         "or strings copies shallowly and behaves exactly as you would want, "
         "because the shared elements are immutable and nobody can change them. "
         "The bug needs two ingredients: nesting, and mutation.</p>"),
        ("Everything is shallow unless you asked",
         "<p>These are all the same operation: <code>b = a[:]</code>, "
         "<code>b = list(a)</code>, <code>b = a.copy()</code>, "
         "<code>b = copy.copy(a)</code>, <code>b = [*a]</code>, and "
         "<code>dict(d)</code> for dictionaries. One level.</p>"
         "<p><code>copy.deepcopy</code> is the only one in that list that "
         "recurses. It also handles the two things a naive recursion would get "
         "wrong: <strong>cycles</strong>, via a memo of objects already copied, "
         "so a list containing itself does not hang; and "
         "<strong>identity sharing</strong>, so if the same object appears "
         "twice in the source it appears twice as the same object in the "
         "result rather than being duplicated.</p>"),
        ("What deepcopy costs, and when to avoid it",
         "<p>It walks the entire object graph and rebuilds it, so it is "
         "proportional to the total size rather than the top-level length, and "
         "it is slow enough to notice in a loop. It also copies things you may "
         "not want copied: a nested object holding a database connection, an "
         "open file or a lock either fails or produces a duplicate that is "
         "meaningless.</p>"
         "<p>Classes control this. <code>__deepcopy__</code> and "
         "<code>__copy__</code> let a type define what copying means, and "
         "<code>copy.deepcopy</code> falls back to the pickle protocol "
         "(<code>__reduce_ex__</code>) &mdash; which is why objects that cannot "
         "be pickled frequently cannot be deep-copied either, for the same "
         "reason.</p>"
         "<p>The cheapest fix is often neither: restructure so the nested "
         "mutable is not shared in the first place, or use immutable values so "
         "copying is unnecessary.</p>"),
        ("The follow-up: the nested-list multiplication bug",
         "<p>\"What does <code>[[0] * 3] * 3</code> give you?\" A list of three "
         "references to <em>one</em> inner list, so setting "
         "<code>grid[0][0]</code> sets the first cell of every row. It is the "
         "same fact as this page &mdash; the outer sequence was copied and the "
         "inner one was shared &mdash; arriving through multiplication rather "
         "than through a copy call. The fix is a comprehension, which evaluates "
         "<code>[0] * 3</code> once per row.</p>"),
    ],
    code={
        "file": "copies.py",
        "intro": "The divergence at the inner level, the leak demonstrated by "
                 "one append, and the cycle deepcopy survives.",
        "code": '''import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

print("outer objects all differ:")
print("  shallow is original:", shallow is original)
print("  deep is original   :", deep is original)

print()
print("but the inner lists are shared by the shallow copy:")
print("  original[0] is shallow[0]:", original[0] is shallow[0])
print("  original[0] is deep[0]   :", original[0] is deep[0])

original[0].append(99)
print()
print("after original[0].append(99):")
print("  original:", original)
print("  shallow :", shallow, "<- changed too")
print("  deep    :", deep, "<- untouched")

# Every other "copy" you know is also shallow.
print()
for label, made in (("original[:]", original[:]),
                    ("list(original)", list(original)),
                    ("original.copy()", original.copy())):
    print(f"  {label:<18} shares inner:", made[0] is original[0])

# deepcopy handles what a naive recursion cannot.
cyclic = [1, 2]
cyclic.append(cyclic)              # a list containing itself
clone = copy.deepcopy(cyclic)
print()
print("deepcopy of a cyclic list terminated:", clone[2] is clone)

shared = [0]
twice = [shared, shared]
dcopy = copy.deepcopy(twice)
print("sharing is preserved, not duplicated:", dcopy[0] is dcopy[1])
''',
        "walk": [
            ("copy.copy(original)",
             "A new outer list holding the same two inner lists. The outer "
             "independence is real and is not what the question is about."),
            ("original[0].append(99)",
             "One mutation, visible through two names. Nothing was assigned to "
             "<code>shallow</code> &mdash; it changed because it was never a "
             "separate object at that level."),
            ("made[0] is original[0]",
             "<code>True</code> for slicing, <code>list()</code> and "
             "<code>.copy()</code> alike. There is one shallow copy operation "
             "with several spellings."),
            ("clone[2] is clone",
             "deepcopy kept a memo of what it had already copied, so the "
             "self-reference became a reference to the <em>copy</em> rather "
             "than an infinite descent."),
        ],
        "try": [
            "Make the inner values immutable &mdash; <code>[(1, 2), (3, 4)]</code> "
            "&mdash; and try to reproduce the leak. You cannot, which is the "
            "argument for immutable values over defensive copying.",
            "Put an open file in the structure and call <code>deepcopy</code>. "
            "The failure is the same one <code>pickle</code> gives, because "
            "deepcopy falls back to the same protocol.",
        ],
    },
    check=[
        {"q": "A shallow copy of [[1,2],[3,4]] gives you:",
         "options": ["A completely independent structure",
                     "A new outer list holding the same two inner lists",
                     "The same object",
                     "A new outer list with new empty inner lists"],
         "answer": 1,
         "why": "The container is new and the contents are shared, which is "
                "exactly where nested mutation leaks between the two."},
        {"q": "Which of these is NOT shallow?",
         "options": ["a[:]", "list(a)", "copy.deepcopy(a)", "a.copy()"],
         "answer": 2,
         "why": "deepcopy is the only one that recurses into the contents. The "
                "rest are one level deep with different spellings."},
        {"q": "Why does deepcopy not hang on a list that contains itself?",
         "options": ["It detects lists specially",
                     "It keeps a memo of objects already copied and reuses it",
                     "It has a recursion limit",
                     "It refuses cyclic input"],
         "answer": 1,
         "why": "The memo makes the self-reference point at the new copy, which "
                "terminates and preserves the shape."},
        {"q": "When is a shallow copy perfectly safe?",
         "options": ["Never",
                     "When the elements are immutable, so sharing them has no consequences",
                     "Only for lists of length 1",
                     "When the copy is read-only"],
         "answer": 1,
         "why": "The bug needs nesting and mutation. Immutable elements remove "
                "the second ingredient."},
    ],
)


# =========================================================================
# 5. closures and late binding
# =========================================================================

def _closure_frames():
    """Recorded from real closures and their real cell contents."""
    late = [lambda: i for i in range(3)]
    early = [lambda i=i: i for i in range(3)]

    def make(i):
        return lambda: i
    factory = [make(i) for i in range(3)]

    out = [frame(
        pairs([("functions built", "3"),
               ("each closes over", "the name i"),
               ("i after the loop", "2")],
              {"i after the loop": "bad"}, label="the loop finished"),
        "Three functions were built and none has run. Each one closed over "
        "the NAME i, not the value i had at the time.",
        {"cells": 1}),
        frame(
        pairs([("late[0]()", str(late[0]())), ("late[1]()", str(late[1]())),
               ("late[2]()", str(late[2]())),
               ("shared cell holds", str(late[0].__closure__[0].cell_contents))],
              {"late[0]()": "bad", "late[1]()": "bad", "late[2]()": "bad"},
              label="calling them now"),
        "All three answer 2. They look up i when CALLED, and by then the loop "
        "has left it at 2 - one cell, shared by all three closures.",
        {"cells": 1}),
        frame(
        pairs([("early[0]()", str(early[0]())), ("early[1]()", str(early[1]())),
               ("early[2]()", str(early[2]())),
               ("mechanism", "default argument")],
              {"early[0]()": "done", "early[1]()": "done",
               "early[2]()": "done"}, label="fix 1: bind at definition"),
        "lambda i=i: i evaluates the default when the lambda is created, so "
        "each function captures a value instead of a name. The same early "
        "binding that makes mutable defaults a bug is the fix here.",
        {"cells": 0}),
        frame(
        pairs([("factory[0]()", str(factory[0]())),
               ("factory[1]()", str(factory[1]())),
               ("factory[2]()", str(factory[2]())),
               ("separate cells",
                str([f.__closure__[0].cell_contents for f in factory]))],
              {"separate cells": "hit"}, label="fix 2: a new scope each time"),
        "Each make(i) call has its own frame, so each lambda closes over a "
        "different cell. Three cells with three values, which is what the "
        "loop looked like it was doing.",
        {"cells": 3})]
    return viz(out)


_q(
    slug="closures-and-late-binding",
    kind="concept",
    level="Medium",
    title="Why do all these functions return the same value?",
    asked="What does [lambda: i for i in range(3)] give you when you call each "
          "one, and why?",
    desc="Late binding in Python closures: a closure captures the variable, "
         "not its value, and the two standard fixes with what each one "
         "actually does.",
    lead="A closure captures the <strong>variable</strong>, not the value it "
         "had when the function was defined. All three lambdas share one cell "
         "holding <code>i</code>, and they read it when called &mdash; by which "
         "time the loop has finished and left it at 2. Bind a value with a "
         "default argument, or make a new scope with a factory.",
    say="\"Python closures are late-binding: they look the variable up at call "
        "time, not definition time. So every lambda in that loop sees the final "
        "value. I fix it with a default argument, lambda i=i: i, which "
        "evaluates i when the lambda is created, or with a factory function so "
        "each closure gets its own scope.\"",
    notice=[
        "The three functions share <em>one</em> cell &mdash; that is why they "
        "agree.",
        "<code>lambda i=i: i</code> captures a value because defaults are "
        "evaluated at definition time.",
        "The factory version has three separate cells, each with its own value.",
    ],
    viz=_closure_frames(),
    sections=[
        ("Capturing a name, not a value",
         "<p>When a nested function refers to a variable from an enclosing "
         "scope, Python does not copy the value in. It stores a reference to a "
         "<strong>cell</strong> &mdash; a small box holding that variable "
         "&mdash; and reads the cell when the function runs. You can see them: "
         "<code>f.__closure__</code> is a tuple of cells, and "
         "<code>.cell_contents</code> is what each holds right now.</p>"
         "<p>A loop body is not a new scope in Python, so every iteration "
         "refers to the same <code>i</code> and therefore the same cell. Three "
         "lambdas, one cell, one answer. This is not a quirk of "
         "<code>lambda</code>: a nested <code>def</code> in the same loop "
         "behaves identically.</p>"),
        ("The two fixes, and what they really do",
         "<p><strong>A default argument.</strong> <code>lambda i=i: i</code> "
         "works because default expressions are evaluated when the function "
         "object is created, so the current value is captured and stored on the "
         "function. It is the shortest fix and it changes the signature, which "
         "means a caller can override it &mdash; usually harmless, occasionally "
         "surprising.</p>"
         "<p><strong>A factory.</strong> <code>def make(i): return lambda: "
         "i</code> gives each closure a genuinely separate scope, because each "
         "call to <code>make</code> creates its own frame and its own cell. It "
         "is more code and it is the version that scales to closing over "
         "several variables. <code>functools.partial(op, i)</code> is the same "
         "idea from the standard library.</p>"),
        ("Why late binding is the right default",
         "<p>It is easy to read this as a design mistake. It is the behaviour "
         "that makes ordinary closures work: a function that closes over "
         "<code>self</code>, a counter, or a configuration dictionary is "
         "supposed to see the <em>current</em> value, not a snapshot from "
         "whenever it was defined. Mutual recursion between two nested "
         "functions relies on it, and so does any callback that reads state "
         "updated after it was registered.</p>"
         "<p>The loop case is the one place where you wanted a snapshot and the "
         "language gave you a reference. Every other closure in your program is "
         "benefiting from the same rule.</p>"),
        ("Where it bites in real code",
         "<p>Callbacks registered in a loop &mdash; buttons, handlers, retry "
         "functions &mdash; all firing with the last item. Tasks created in a "
         "loop and appended to a list. And "
         "<code>functools.reduce</code>-style pipelines built by stacking "
         "lambdas over a loop variable.</p>"
         "<p>The tell is always the same: several functions built in a loop, "
         "called after it. If they are called inside the loop, late binding "
         "reads the value you expected and the bug never appears &mdash; which "
         "is why this survives testing so well.</p>"),
    ],
    code={
        "file": "closures.py",
        "intro": "The shared cell, both fixes, and the same bug with def "
                 "instead of lambda so it is clear the syntax is not the cause.",
        "code": '''# A closure captures the VARIABLE, not its value.
late = [lambda: i for i in range(3)]
print("late binding: ", [f() for f in late], "<- all 2")

# Look at the machinery: one cell, shared by all three.
print("cells per function:", [len(f.__closure__) for f in late])
print("the shared cell holds:", late[0].__closure__[0].cell_contents)
print("same cell object:", late[0].__closure__[0] is late[1].__closure__[0])

# Fix 1: a default argument is evaluated at definition time.
early = [lambda i=i: i for i in range(3)]
print()
print("default-arg fix:", [f() for f in early])
print("no closure needed:", [f.__closure__ for f in early][0])

# Fix 2: a factory gives each function its own scope.
def make(i):
    return lambda: i

factory = [make(i) for i in range(3)]
print("factory fix:    ", [f() for f in factory])
print("separate cells: ", [f.__closure__[0].cell_contents for f in factory])

# It is not about lambda. A nested def does exactly the same thing.
def build():
    out = []
    for i in range(3):
        def show():
            return i
        out.append(show)
    return out

print()
print("with def instead:", [f() for f in build()], "<- identical")

# And called INSIDE the loop, late binding is what you wanted.
print("called in the loop:", [(lambda: i)() for i in range(3)])
''',
        "walk": [
            ("late[0].__closure__[0] is late[1].__closure__[0]",
             "<code>True</code>. This is the whole explanation in one line: "
             "there is one box, and all three functions read it."),
            ("lambda i=i: i",
             "The right-hand <code>i</code> is evaluated now; the left-hand one "
             "is a parameter name. The value is stored on the function, so "
             "<code>__closure__</code> is <code>None</code> &mdash; there is "
             "nothing to close over any more."),
            ("[f.__closure__[0].cell_contents for f in factory]",
             "<code>[0, 1, 2]</code>. Three calls to <code>make</code> made "
             "three frames, so there are three cells to read."),
            ("[(lambda: i)() for i in range(3)]",
             "<code>[0, 1, 2]</code>, because each is called before the loop "
             "moves on. Late binding only hurts when the call is deferred, "
             "which is why the bug survives casual testing."),
        ],
        "try": [
            "Rebind <code>i = 99</code> after building <code>late</code> and "
            "call them again. They all return 99 &mdash; the cell is live, not a "
            "snapshot.",
            "Replace the factory with "
            "<code>functools.partial(lambda x: x, i)</code> and check it gives "
            "<code>[0, 1, 2]</code> too. Same idea, different spelling.",
        ],
    },
    check=[
        {"q": "What do the three lambdas in [lambda: i for i in range(3)] return?",
         "options": ["0, 1, 2", "2, 2, 2", "None", "A TypeError"],
         "answer": 1,
         "why": "They share one cell holding i and read it when called, by "
                "which time the loop has left it at 2."},
        {"q": "A Python closure captures:",
         "options": ["A copy of the value",
                     "A reference to the variable's cell, read at call time",
                     "The whole enclosing frame",
                     "Nothing; it re-executes the enclosing function"],
         "answer": 1,
         "why": "That is what late binding means, and it is why the value can "
                "change between definition and call."},
        {"q": "Why does lambda i=i: i fix it?",
         "options": ["Defaults are re-evaluated per call",
                     "Defaults are evaluated at definition time, so the current value is captured",
                     "It creates a new cell",
                     "Parameters cannot be closed over"],
         "answer": 1,
         "why": "The same early-binding rule that makes a mutable default a "
                "bug is exactly what you want here."},
        {"q": "Is this specific to lambda?",
         "options": ["Yes",
                     "No - a nested def in the same loop behaves identically",
                     "Only in comprehensions",
                     "Only in Python 2"],
         "answer": 1,
         "why": "The rule is about scopes and cells, not about which syntax "
                "created the function."},
    ],
)


# =========================================================================
# 6. decorators
# =========================================================================

def _decorator_frames():
    """Recorded by actually decorating two functions and reading the result."""
    import functools

    def shout(fn):
        def wrapper(*a, **k):
            return fn(*a, **k).upper()
        return wrapper

    def shout_wraps(fn):
        @functools.wraps(fn)
        def wrapper(*a, **k):
            return fn(*a, **k).upper()
        return wrapper

    def greet(name):
        "Say hello politely."
        return "hello " + name

    plain_name, plain_doc = greet.__name__, greet.__doc__
    bare = shout(greet)
    wrapped = shout_wraps(greet)

    out = [frame(
        pairs([("greet.__name__", plain_name), ("greet.__doc__", plain_doc),
               ("greet('ada')", greet("ada"))],
              {"greet.__name__": "done"}, label="before decoration"),
        "An ordinary function with its own name and docstring.",
        {"objects": 1}),
        frame(
        pairs([("@shout means", "greet = shout(greet)"),
               ("the name greet now points at", "wrapper"),
               ("result", bare("ada"))],
              {"the name greet now points at": "hit"},
              label="what the @ line does"),
        "Decoration is one assignment. The original function still exists, "
        "captured inside wrapper - but the NAME greet now refers to wrapper.",
        {"objects": 2}),
        frame(
        pairs([("__name__", bare.__name__), ("__doc__", str(bare.__doc__)),
               ("cost", "introspection is broken")],
              {"__name__": "bad", "__doc__": "bad"},
              label="without functools.wraps"),
        "Because greet is now wrapper, every tool that reads metadata - help(), "
        "tracebacks, Sphinx, pytest - sees 'wrapper' and no docstring.",
        {"objects": 2}),
        frame(
        pairs([("__name__", wrapped.__name__),
               ("__doc__", str(wrapped.__doc__)),
               ("__wrapped__", wrapped.__wrapped__.__name__)],
              {"__name__": "done", "__doc__": "done", "__wrapped__": "hit"},
              label="with functools.wraps"),
        "wraps copies __name__, __doc__, __module__ and __qualname__ across, "
        "and leaves __wrapped__ pointing at the original so tools can still "
        "find it.",
        {"objects": 2})]
    return viz(out)


_q(
    slug="what-a-decorator-replaces",
    kind="concept",
    level="Medium",
    title="What does a decorator actually replace?",
    asked="What does the @ syntax do, and why do decorated functions need "
          "functools.wraps?",
    desc="A decorator is one assignment: name = decorator(name). Why that "
         "breaks introspection, what functools.wraps copies, and how "
         "decorators with arguments add a third layer.",
    lead="<code>@shout</code> above <code>def greet</code> is exactly "
         "<code>greet = shout(greet)</code>. The name now refers to whatever "
         "the decorator returned &mdash; usually a wrapper function &mdash; so "
         "the original's name and docstring are gone unless you copy them "
         "across with <code>functools.wraps</code>.",
    say="\"The @ line is syntax for reassigning the name: greet = "
        "shout(greet). So the name ends up pointing at the wrapper, which is "
        "why __name__ and __doc__ change and tracebacks get less useful. "
        "functools.wraps copies the metadata over and sets __wrapped__ so "
        "introspection still works.\"",
    notice=[
        "Decoration happens once, at definition time &mdash; not per call.",
        "Without <code>wraps</code>, <code>__name__</code> becomes "
        "<code>wrapper</code> and the docstring disappears.",
        "<code>__wrapped__</code> is the escape hatch back to the original.",
    ],
    viz=_decorator_frames(),
    sections=[
        ("It is one assignment",
         "<p>There is no special decorator machinery. These two are the same "
         "program:</p>"
         "<pre><code>@shout\n"
         "def greet(name): ...\n\n"
         "# is exactly\n"
         "def greet(name): ...\n"
         "greet = shout(greet)</code></pre>"
         "<p>Which tells you three things immediately. It runs once, when the "
         "<code>def</code> is executed, not on every call. The decorator "
         "receives the function object and can return literally anything "
         "&mdash; a different function, a class instance, or a string, though "
         "the last one will confuse everybody. And stacked decorators apply "
         "bottom-up: the one nearest the <code>def</code> wraps first.</p>"),
        ("Why wraps exists",
         "<p>If the decorator returns a new function, the name now refers to "
         "that function, and it has its own <code>__name__</code>, its own "
         "empty <code>__doc__</code> and its own signature. Everything that "
         "reads those breaks quietly: <code>help()</code> becomes useless, "
         "documentation tools generate entries for a function called "
         "<code>wrapper</code>, and test frameworks that discover by name "
         "misbehave.</p>"
         "<p><code>functools.wraps</code> is a decorator for your wrapper that "
         "copies <code>__name__</code>, <code>__doc__</code>, "
         "<code>__module__</code>, <code>__qualname__</code> and "
         "<code>__dict__</code> across, and sets <code>__wrapped__</code> to "
         "the original. That last one is what lets "
         "<code>inspect.signature</code> report the real signature rather than "
         "<code>(*args, **kwargs)</code>.</p>"),
        ("Decorators that take arguments",
         "<p><code>@repeat(3)</code> needs one more layer, and the reason "
         "follows from the assignment rule. <code>@X</code> calls "
         "<code>X(fn)</code>; so if <code>X</code> is written as "
         "<code>repeat(3)</code>, then <code>repeat(3)</code> must itself "
         "<em>return</em> a decorator:</p>"
         "<pre><code>def repeat(times):            # takes the argument\n"
         "    def decorator(fn):        # takes the function\n"
         "        @functools.wraps(fn)\n"
         "        def wrapper(*a, **k): # takes the call\n"
         "            for _ in range(times):\n"
         "                result = fn(*a, **k)\n"
         "            return result\n"
         "        return wrapper\n"
         "    return decorator</code></pre>"
         "<p>Three levels, one per thing being received. Getting the count "
         "wrong is the standard mistake, and the symptom is a "
         "<code>TypeError</code> about a function not being callable, or a "
         "decorator that returns <code>None</code>.</p>"),
        ("The follow-up: what else can decorate",
         "<p>Anything callable. A class with <code>__call__</code> is a common "
         "choice when the decorator needs state &mdash; a cache, a call count, "
         "a registry &mdash; because instance attributes are tidier than "
         "<code>nonlocal</code>. And the standard library's own decorators are "
         "worth naming: <code>functools.lru_cache</code> for "
         "<a href=\"../interview/memoisation-with-a-dictionary.html\">memoisation</a>, "
         "<code>property</code>, <code>staticmethod</code>, "
         "<code>classmethod</code>, <code>contextlib.contextmanager</code> and "
         "<code>dataclasses.dataclass</code> &mdash; which returns the same "
         "class with methods added rather than a wrapper, proving the return "
         "value need not be a function at all.</p>"),
    ],
    code={
        "file": "decorators.py",
        "intro": "The metadata before and after, the wraps fix, and a "
                 "decorator with an argument so the three layers are visible.",
        "code": '''import functools

def shout(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).upper()
    return wrapper

@shout
def greet(name):
    "Say hello politely."
    return f"hello {name}"

print("it works:", greet("ada"))
print("but the name now refers to the wrapper:")
print("  __name__:", greet.__name__)
print("  __doc__ :", greet.__doc__)

# @shout was exactly this:
def plain(name):
    "Say hello politely."
    return f"hello {name}"
plain = shout(plain)
print("  manual version gives the same __name__:", plain.__name__)

# --- the fix -------------------------------------------------------------
def shout_wraps(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).upper()
    return wrapper

@shout_wraps
def greet2(name):
    "Say hello politely."
    return f"hello {name}"

print()
print("with functools.wraps:")
print("  __name__   :", greet2.__name__)
print("  __doc__    :", greet2.__doc__)
print("  __wrapped__:", greet2.__wrapped__.__name__)

import inspect
print("  signature  :", inspect.signature(greet2), "<- not (*args, **kwargs)")

# --- a decorator with an argument needs three layers --------------------
def repeat(times):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return decorator

calls = []

@repeat(3)
def record():
    calls.append(1)
    return len(calls)

print()
print("@repeat(3) ->", record(), "calls made:", len(calls))
''',
        "walk": [
            ("plain = shout(plain)",
             "The manual form, printed beside the decorated one to show they "
             "produce the same result. There is no extra machinery in the "
             "<code>@</code>."),
            ("@functools.wraps(fn)",
             "A decorator applied to the wrapper. It copies the metadata from "
             "<code>fn</code> onto <code>wrapper</code>, which is why the name "
             "and docstring survive."),
            ("inspect.signature(greet2)",
             "Reports the original signature because <code>wraps</code> set "
             "<code>__wrapped__</code>. Without it you get "
             "<code>(*args, **kwargs)</code>, which is what makes wrapped "
             "APIs unpleasant to use."),
            ("def repeat(times): def decorator(fn): def wrapper(...)",
             "Three layers because three things arrive separately: the "
             "argument, the function, and the call. Count them from the "
             "inside out."),
        ],
        "try": [
            "Remove the <code>@functools.wraps</code> line and call "
            "<code>help(greet2)</code>. What disappears is what every "
            "documentation tool also loses.",
            "Stack <code>@shout</code> and <code>@repeat(2)</code> in both "
            "orders. The one nearest the <code>def</code> wraps first, and the "
            "outputs differ.",
        ],
    },
    check=[
        {"q": "@shout above def greet is equivalent to:",
         "options": ["greet = shout", "greet = shout(greet)",
                     "shout(greet()) on every call", "greet.shout()"],
         "answer": 1,
         "why": "Decoration is one assignment performed at definition time, "
                "which is why everything else about decorators follows."},
        {"q": "Why does __name__ become 'wrapper'?",
         "options": ["functools renames it",
                     "Because the name now refers to the wrapper function, which has its own metadata",
                     "Decorators delete the docstring",
                     "It does not"],
         "answer": 1,
         "why": "The original object is unchanged; the name simply points at a "
                "different function now."},
        {"q": "What does functools.wraps set that helps inspect.signature?",
         "options": ["__signature__", "__wrapped__", "__code__", "__globals__"],
         "answer": 1,
         "why": "__wrapped__ points back at the original, so signature() "
                "reports the real parameters instead of (*args, **kwargs)."},
        {"q": "Why does a decorator taking an argument need three nested functions?",
         "options": ["For performance",
                     "Because the argument, the function and the call each arrive separately",
                     "To support stacking",
                     "It does not; two is enough"],
         "answer": 1,
         "why": "@X calls X(fn), so if X is repeat(3), then repeat(3) has to "
                "return a decorator, which returns the wrapper."},
    ],
)


# =========================================================================
# 7. with, and what __exit__ guarantees
# =========================================================================

def _with_frames():
    """Recorded by actually running the three cases through a tracked manager."""
    log = []

    class Tracked:
        def __init__(self, name, swallow=False):
            self.name, self.swallow = name, swallow

        def __enter__(self):
            log.append(("enter", self.name, None))
            return self

        def __exit__(self, exc_type, exc, tb):
            log.append(("exit", self.name,
                        exc_type.__name__ if exc_type else None))
            return self.swallow

    with Tracked("A"):
        log.append(("body", "A", None))
    normal = list(log)

    log.clear()
    try:
        with Tracked("B"):
            raise ValueError("boom")
    except ValueError:
        log.append(("caught", "B", "ValueError"))
    raised = list(log)

    log.clear()
    with Tracked("C", swallow=True):
        raise ValueError("silenced")
    log.append(("continued", "C", None))
    swallowed = list(log)

    def show(entries):
        return [("%s %s" % (w, n), exc or "-") for w, n, exc in entries]

    out = [frame(
        pairs(show(normal), {"exit A": "done"}, label="normal exit"),
        "__enter__, the body, then __exit__ with no exception. Nothing "
        "surprising, and the exit is guaranteed from here on.",
        {"exit ran": 1}),
        frame(
        pairs(show(raised), {"exit B": "hit", "caught B": "bad"},
              label="the body raises"),
        "__exit__ still ran, and it was TOLD what went wrong - the exception "
        "type is an argument. It returned a falsy value, so the exception "
        "carried on to the except clause.",
        {"exit ran": 2}),
        frame(
        pairs(show(swallowed), {"exit C": "hit", "continued C": "done"},
              label="__exit__ returns True"),
        "A truthy return from __exit__ SWALLOWS the exception: execution "
        "continues after the with block and no except clause is needed. This "
        "is how contextlib.suppress works.",
        {"exit ran": 3})]
    return viz(out)


_q(
    slug="what-with-guarantees",
    kind="concept",
    level="Medium",
    title="What does `with` guarantee when the body raises?",
    asked="What does the with statement actually do, and what happens to an "
          "exception raised inside it?",
    desc="The context manager protocol: __enter__ and __exit__, why the exit "
         "runs on exceptions and returns, what a truthy __exit__ suppresses, "
         "and when to reach for contextlib.",
    lead="<code>with</code> calls <code>__enter__</code>, runs the body, and "
         "calls <code>__exit__</code> <strong>however the body ends</strong> "
         "&mdash; normally, by <code>return</code>, or by exception. "
         "<code>__exit__</code> is told what went wrong, and if it returns "
         "something truthy the exception is suppressed.",
    say="\"with is the context manager protocol: __enter__ before the body, "
        "__exit__ after it, guaranteed, including on an exception or a return. "
        "__exit__ receives the exception details, and returning True from it "
        "suppresses the exception - which is exactly what contextlib.suppress "
        "does. I use it for anything with a cleanup that must happen.\"",
    notice=[
        "<code>__exit__</code> runs in all three cases &mdash; that is the "
        "guarantee being bought.",
        "It is <em>told</em> the exception type, so cleanup can behave "
        "differently on failure.",
        "Returning <code>True</code> swallows the exception; returning "
        "<code>None</code> lets it propagate.",
    ],
    viz=_with_frames(),
    sections=[
        ("The protocol, in full",
         "<p><code>with expr as name:</code> does four things. It evaluates "
         "<code>expr</code>. It calls <code>__enter__()</code> on the result "
         "and binds the return value to <code>name</code> &mdash; note that "
         "this is <em>not</em> necessarily the object itself, which is why "
         "<code>open()</code> can return a file and a lock can return "
         "<code>None</code>. It runs the body. Then it calls "
         "<code>__exit__(exc_type, exc, traceback)</code>.</p>"
         "<p>The last step is the point. It happens on a normal fall-through, "
         "on a <code>return</code> from inside the body, on a "
         "<code>break</code>, and on an exception. That is a stronger promise "
         "than <code>try/finally</code> written by hand, only because it is "
         "harder to forget.</p>"),
        ("Suppression, and why it is rare",
         "<p>A truthy return from <code>__exit__</code> tells Python the "
         "exception has been handled, and execution continues after the block. "
         "It is a real feature with one common use &mdash; "
         "<code>contextlib.suppress(FileNotFoundError)</code> is a context "
         "manager whose entire job is to return <code>True</code> for the types "
         "you named.</p>"
         "<p>Writing it yourself is usually a mistake, because a manager that "
         "swallows exceptions silently is a manager that hides bugs. The "
         "convention is to return <code>None</code> and let the exception "
         "through, doing cleanup on the way out. If you do suppress, suppress "
         "one specific type and nothing else.</p>"),
        ("contextlib, and the generator form",
         "<p>Writing a class with two dunder methods for a two-line cleanup is "
         "heavy, and <code>contextlib.contextmanager</code> removes it:</p>"
         "<pre><code>@contextmanager\n"
         "def timed(label):\n"
         "    start = time.perf_counter()\n"
         "    try:\n"
         "        yield                  # the body runs here\n"
         "    finally:\n"
         "        print(label, time.perf_counter() - start)</code></pre>"
         "<p>Everything before the <code>yield</code> is <code>__enter__</code>; "
         "everything after is <code>__exit__</code>. The "
         "<code>try/finally</code> is not optional &mdash; without it, an "
         "exception in the body propagates out of the <code>yield</code> and "
         "the cleanup never runs, which quietly defeats the entire purpose.</p>"
         "<p><code>ExitStack</code> is the other one worth knowing: it manages "
         "a variable number of managers, so you can enter a list of files "
         "without a nested <code>with</code> per file.</p>"),
        ("The follow-up: why not just use try/finally",
         "<p>You can, and <code>with</code> compiles to roughly that. The "
         "difference is that the cleanup lives with the <em>resource</em> "
         "rather than with every call site, so it cannot be forgotten at the "
         "twelfth place the resource is used. It also composes: "
         "<code>with a, b:</code> nests correctly, and both exits run even if "
         "the first one raises.</p>"
         "<p>The async counterpart is <code>async with</code> and "
         "<code>__aenter__</code>/<code>__aexit__</code>, which is what an "
         "async HTTP client or database session uses &mdash; same protocol, "
         "awaitable methods.</p>"),
    ],
    code={
        "file": "with_statement.py",
        "intro": "All three exits observed from inside __exit__, the "
                 "suppression case, and a return from the body that still runs "
                 "the cleanup.",
        "code": '''class Tracked:
    def __init__(self, name, swallow=False):
        self.name, self.swallow = name, swallow

    def __enter__(self):
        print(f"  enter {self.name}")
        return self                      # this is what `as` binds

    def __exit__(self, exc_type, exc, tb):
        seen = exc_type.__name__ if exc_type else None
        print(f"  exit  {self.name}  (exception seen: {seen})")
        return self.swallow              # truthy SWALLOWS the exception

print("1. normal exit:")
with Tracked("A"):
    print("  body")

print()
print("2. the body raises - __exit__ still runs, and is told what:")
try:
    with Tracked("B"):
        raise ValueError("boom")
except ValueError as e:
    print("  propagated to here:", e)

print()
print("3. __exit__ returns True, so the exception is suppressed:")
with Tracked("C", swallow=True):
    raise ValueError("silenced")
print("  execution continues, with no except clause")

print()
print("4. a return from inside the body does not skip the exit:")
def f():
    with Tracked("D"):
        return "returned"
print("  f() ->", f())

# The generator form, and why the try/finally matters.
from contextlib import contextmanager

@contextmanager
def guarded(label):
    print(f"  enter {label}")
    try:
        yield label
    finally:
        print(f"  exit  {label}  (finally always runs)")

print()
print("5. contextlib version, with the body raising:")
try:
    with guarded("E") as name:
        raise RuntimeError("from " + name)
except RuntimeError as e:
    print("  propagated:", e)
''',
        "walk": [
            ("return self",
             "What <code>__enter__</code> returns is what <code>as</code> "
             "binds. Returning <code>self</code> is a convention, not a rule "
             "&mdash; <code>open()</code> returns a file, and a lock returns "
             "<code>None</code>."),
            ("return self.swallow",
             "The return value of <code>__exit__</code> is the suppression "
             "decision. Falsy lets the exception through; truthy stops it "
             "dead. Returning nothing means <code>None</code>, which is "
             "falsy, which is the right default."),
            ("with Tracked(\"D\"): return \"returned\"",
             "The exit prints before <code>f()</code> hands its value back. "
             "A <code>return</code> inside the block cannot skip the cleanup."),
            ("try: yield ... finally:",
             "In the generator form the <code>finally</code> is what makes the "
             "cleanup unconditional. Omit it and an exception in the body "
             "escapes through the <code>yield</code>, leaving the cleanup "
             "unrun."),
        ],
        "try": [
            "Delete the <code>try/finally</code> from <code>guarded</code> and "
            "re-run case 5. The exit line disappears &mdash; the bug that makes "
            "a hand-written context manager worse than none.",
            "Replace case 3 with "
            "<code>contextlib.suppress(ValueError)</code> and confirm it "
            "behaves the same. That is all <code>suppress</code> is.",
        ],
    },
    check=[
        {"q": "When is __exit__ called?",
         "options": ["Only on a normal exit",
                     "However the body ends: normally, by return, or by exception",
                     "Only if no exception occurred",
                     "Only when the object is garbage collected"],
         "answer": 1,
         "why": "That unconditional call is the entire guarantee the with "
                "statement buys."},
        {"q": "What does returning True from __exit__ do?",
         "options": ["Re-raises the exception",
                     "Suppresses the exception, so execution continues after the block",
                     "Logs it",
                     "Nothing"],
         "answer": 1,
         "why": "It tells Python the exception was handled. contextlib.suppress "
                "is a context manager built entirely on this."},
        {"q": "What does `as name` bind?",
         "options": ["The context manager object",
                     "Whatever __enter__ returns",
                     "The exception",
                     "The result of the body"],
         "answer": 1,
         "why": "Which is why open() gives a file object and some managers "
                "give None."},
        {"q": "In the @contextmanager form, why is try/finally around the yield required?",
         "options": ["To satisfy the decorator",
                     "Because an exception in the body propagates through the yield and would skip the cleanup",
                     "To return a value",
                     "It is optional and only stylistic"],
         "answer": 1,
         "why": "Without it the cleanup does not run on failure, which defeats "
                "the purpose of using a context manager at all."},
    ],
)


# =========================================================================
# 8. comprehensions
# =========================================================================

def _comprehension_frames():
    """Recorded from the real per-iteration bytecode of both forms.

    The names of the opcodes differ between interpreter versions - and this
    runs on the BUILD machine while the editor runs on Pyodide 3.12 - so the
    frames report what the instructions *do* rather than what they are called.
    Those facts hold on every version; the raw names are left to the editor,
    which prints them for whatever interpreter the reader has.
    """
    import dis

    def with_loop(n):
        out = []
        for i in range(n):
            out.append(i * i)
        return out

    def with_comprehension(n):
        return [i * i for i in range(n)]

    def per_iteration(fn):
        """The ops between FOR_ITER and the jump back, on any version.

        Before 3.12 a comprehension compiled to its own code object, so the
        loop is not in the outer function at all - PEP 709 inlined it. Both
        layouts are handled, which is itself the point the article makes.
        """
        code = fn.__code__
        ops = [i.opname for i in dis.get_instructions(code)]
        if "FOR_ITER" not in ops:
            nested = [c for c in code.co_consts
                      if hasattr(c, "co_code")]
            if not nested:
                return []
            ops = [i.opname for i in dis.get_instructions(nested[0])]
        if "FOR_ITER" not in ops:
            return []
        body = ops[ops.index("FOR_ITER") + 1:]
        for i, o in enumerate(body):
            if o.startswith("JUMP"):
                return body[:i]
        return body

    loop_ops = per_iteration(with_loop)
    comp_ops = per_iteration(with_comprehension)

    def facts(ops):
        return {
            "instructions": len(ops),
            "attribute lookup": any("ATTR" in o or "METHOD" in o for o in ops),
            "function call": any(o.startswith("CALL") for o in ops),
            "dedicated append": any("LIST_APPEND" in o for o in ops),
        }

    lf, cf = facts(loop_ops), facts(comp_ops)

    def as_rows(f):
        return [(k, "yes" if v is True else ("no" if v is False else str(v)))
                for k, v in f.items()]

    out = [frame(
        pairs(as_rows(lf),
              {"attribute lookup": "bad", "function call": "bad"},
              label="the loop, per iteration"),
        "Every iteration looks up the append method on the list and then "
        "calls it. Those two are the work the comprehension does not do.",
        {"instructions": lf["instructions"]}),
        frame(
        pairs(as_rows(cf), {"dedicated append": "hit"},
              label="the comprehension, per iteration"),
        "No lookup and no call: the append is one dedicated instruction "
        "operating on the list being built, which is not in a variable at "
        "all.",
        {"instructions": cf["instructions"]}),
        frame(
        pairs([("instructions saved per item",
                str(lf["instructions"] - cf["instructions"])),
               ("complexity", "O(n) either way"),
               ("so the win is", "a constant factor"),
               ("honest answer", "a bit faster, not 3x")],
              {"so the win is": "hit", "honest answer": "done"},
              label="what it adds up to"),
        "The gap is per-item overhead, not a change in growth. That is why "
        "the right answer to the interview question is 'a little faster, "
        "because of a lookup and a call', and why readability decides it.",
        {"instructions": lf["instructions"] - cf["instructions"]})]
    return viz(out)


_q(
    slug="why-a-comprehension-is-faster",
    kind="concept",
    level="Easy",
    title="Why is a comprehension faster than the same loop?",
    asked="Is a list comprehension faster than an equivalent for loop, and if "
          "so why?",
    desc="Why a comprehension beats the equivalent append loop: a dedicated "
         "LIST_APPEND opcode instead of a per-iteration attribute lookup and "
         "call - and why the win is a constant factor, not a complexity change.",
    lead="Yes, by a little, and for a specific reason: the loop looks up "
         "<code>out.append</code> and calls it on <strong>every "
         "iteration</strong>, while the comprehension appends with a single "
         "dedicated opcode, <code>LIST_APPEND</code>. It is a constant factor, "
         "not a change in complexity &mdash; both are O(n).",
    say="\"A bit faster. The loop does an attribute lookup and a function call "
        "per item; the comprehension uses a dedicated LIST_APPEND opcode with "
        "neither. It is a constant factor, so I would choose between them on "
        "readability, and reach for a generator expression when I do not need "
        "the list in memory - which saves the memory, not the time.\"",
    notice=[
        "The loop's per-iteration bytecode contains "
        "<code>LOAD_ATTR</code> and <code>CALL</code>; the comprehension's "
        "does not.",
        "Both forms are O(n) &mdash; the difference is per-item overhead.",
        "The measured gap is modest, which is the honest answer to the "
        "question.",
    ],
    viz=_comprehension_frames(),
    sections=[
        ("The difference, in bytecode",
         "<p><code>out.append(x)</code> is three separate things: find the "
         "attribute <code>append</code> on the list, build a call, and make "
         "it. That happens once per item. The comprehension compiles the "
         "append into <code>LIST_APPEND</code>, a single instruction that "
         "pushes the value onto the list being built &mdash; no name to "
         "resolve and no call to make.</p>"
         "<p>The explorer above is those two instruction sequences, taken from "
         "<code>dis</code> rather than described, so you can count the "
         "difference. It is a handful of opcodes per item.</p>"),
        ("Why the number is smaller than people expect",
         "<p>Folklore puts comprehensions at two or three times faster, and "
         "that has not been true for a while. Two things narrowed it.</p>"
         "<p>The <strong>specialising interpreter</strong> added in 3.11 "
         "rewrites hot instruction sequences in place, and a repeated "
         "attribute-lookup-then-call on the same type is exactly the pattern "
         "it specialises, so the loop's overhead shrank.</p>"
         "<p>And in 3.12 comprehensions were <strong>inlined</strong> (PEP "
         "709). Before that, a list comprehension created and called a hidden "
         "function object on every evaluation &mdash; real overhead that "
         "partly cancelled the LIST_APPEND saving. Removing it made "
         "comprehensions faster in a way that has nothing to do with the "
         "append path.</p>"
         "<p>So the answer to give is \"a bit faster, because of a "
         "per-iteration lookup and call\", not a multiplier. The editor below "
         "measures it on whichever interpreter you are running.</p>"),
        ("When the loop is the right answer anyway",
         "<p>A comprehension has to be one expression. The moment the body "
         "needs a statement &mdash; a <code>try</code>, a "
         "<code>break</code>, a log line, two things per item &mdash; the "
         "loop is the only option, and forcing a comprehension produces the "
         "unreadable nested version everybody has met.</p>"
         "<p>The real decision is readability at a glance. One "
         "transformation and one filter reads better as a comprehension; "
         "three levels of nesting with two conditions does not, whatever it "
         "costs. And if the result is only going to be consumed once, the "
         "better answer is often neither: a generator expression skips building "
         "the list at all. That is a memory win rather than a speed one "
         "&mdash; the editor below measures the two as roughly equal in time "
         "&mdash; but constant memory against a list of a million items is a "
         "larger practical difference than the constant factor this page is "
         "about.</p>"),
        ("The follow-up: what about map and filter",
         "<p><code>map(f, xs)</code> can beat a comprehension when "
         "<code>f</code> is already a function, because it avoids a Python-level "
         "call per item by doing the loop in C &mdash; but "
         "<code>map(lambda x: x * x, xs)</code> is usually slower than the "
         "comprehension, because the lambda reintroduces exactly the "
         "per-item Python call you were trying to avoid. So "
         "<code>map(str, xs)</code> is a reasonable choice and "
         "<code>map</code> with a lambda rarely is.</p>"),
    ],
    code={
        "file": "comprehensions.py",
        "intro": "Best-of-five timings, because these are noisy, and then the "
                 "per-iteration bytecode of each form so the cause is visible "
                 "rather than asserted.",
        "code": '''import dis, time

def with_loop(n):
    out = []
    for i in range(n):
        out.append(i * i)          # attribute lookup + call, every iteration
    return out

def with_comprehension(n):
    return [i * i for i in range(n)]

def best_of(fn, n, rounds=5):
    best = None
    for _ in range(rounds):
        t0 = time.perf_counter()
        fn(n)
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
    return best                    # best-of: these timings are noisy

N = 200_000
a = best_of(with_loop, N)
b = best_of(with_comprehension, N)
print(f"loop          {a*1000:5.0f} ms")
print(f"comprehension {b*1000:5.0f} ms   ({a/b:.2f}x faster)")

def body(fn):
    ops = [i.opname for i in dis.get_instructions(fn)]
    return ops[ops.index("FOR_ITER") + 1:ops.index("JUMP_BACKWARD")]

print()
print("what actually runs per iteration:")
print("  loop         ", body(with_loop))
print("  comprehension", body(with_comprehension))
print()
print("the loop pays LOAD_ATTR + CALL per item; the comprehension pays")
print("LIST_APPEND. Same complexity, different constant.")

# And the version that avoids building the list at all. Note what it does
# and does not buy: the time is about the same, the memory is not.
import sys
print()
t0 = time.perf_counter(); total_a = sum([i * i for i in range(N)]); as_list = time.perf_counter() - t0
t0 = time.perf_counter(); total_b = sum(i * i for i in range(N));   as_gen = time.perf_counter() - t0
print(f"sum of a list comprehension   {as_list*1000:5.0f} ms")
print(f"sum of a generator expression {as_gen*1000:5.0f} ms")
print("same answer:", total_a == total_b)
print()
print("the generator's win is memory, not time:")
print(f"  the list holds {sys.getsizeof([i * i for i in range(N)]):,} bytes")
print(f"  the generator  {sys.getsizeof(i * i for i in range(N)):,} bytes")
''',
        "walk": [
            ("best_of(fn, n, rounds=5)",
             "Timing the same code twice here can differ by 50%, so a single "
             "measurement would be a coin flip. Taking the minimum of several "
             "runs reports the least-interrupted one."),
            ("body(with_loop)",
             "The instructions between <code>FOR_ITER</code> and the jump back "
             "&mdash; that is, one iteration. <code>LOAD_ATTR</code> and "
             "<code>CALL</code> are the two the comprehension does not have."),
            ("LIST_APPEND",
             "One opcode that appends to the list under construction. There is "
             "no name lookup because the list is on the interpreter stack, not "
             "in a variable."),
            ("sum(i * i for i in range(N))",
             "No brackets and no list, so the memory is constant rather than "
             "proportional to N. The <em>time</em> is about the same or "
             "slightly worse &mdash; each item costs a <code>__next__</code> "
             "call, which is roughly what the list build was costing. Reach "
             "for it to avoid holding the data, not to go faster."),
        ],
        "try": [
            "Hoist the lookup out of the loop with <code>append = "
            "out.append</code> and re-measure. This is classic advice and the "
            "result may surprise you on a modern interpreter &mdash; measure "
            "rather than assume.",
            "Compare <code>map(str, range(N))</code> against "
            "<code>[str(i) for i in range(N)]</code>, then against "
            "<code>map(lambda i: str(i), ...)</code>. The lambda undoes the "
            "advantage.",
        ],
    },
    check=[
        {"q": "Why is a comprehension faster than an append loop?",
         "options": ["It runs in C",
                     "It uses a dedicated LIST_APPEND opcode instead of a per-iteration attribute lookup and call",
                     "It preallocates the list",
                     "It is parallelised"],
         "answer": 1,
         "why": "The saving is the per-item lookup and call. Everything else "
                "about the two loops is the same."},
        {"q": "How does the speed-up scale with n?",
         "options": ["It grows with n",
                     "It is a constant factor - both forms are O(n)",
                     "It only applies below 1000 items",
                     "It disappears for large n"],
         "answer": 1,
         "why": "Per-item overhead differs; the number of items does not. "
                "Neither form changes complexity."},
        {"q": "When must you use a loop instead?",
         "options": ["When the list is large",
                     "When the body needs a statement - try, break, logging, or two operations",
                     "When filtering",
                     "When the input is a generator"],
         "answer": 1,
         "why": "A comprehension's body is one expression, so anything "
                "needing statements does not fit."},
        {"q": "If the result is consumed once, a generator expression saves you:",
         "options": ["Time, by a large factor",
                     "Memory - the time is about the same",
                     "Both time and memory, always",
                     "Nothing"],
         "answer": 1,
         "why": "It never builds the list, so memory is constant instead of "
                "proportional to n. Per-item __next__ calls mean the runtime "
                "is roughly a wash, which the editor measures."},
    ],
)
