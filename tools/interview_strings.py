# -*- coding: utf-8 -*-
"""The string questions.

Order is the order they are usually asked in: the conceptual ones first,
because "why is `+=` quadratic?" is the answer to half the coding problems
that follow, and then the coding problems themselves roughly by difficulty.

Every `viz` here is built by running the thing it draws - see
tools/interview_viz.py for why that matters.
"""

from interview_viz import (cost_table, frame, growing_window, marked, pairs,
                           row, cell, viz)

STRINGS = []


def _q(**kw):
    STRINGS.append(kw)


# =========================================================================
# Conceptual
# =========================================================================

def _immutable_frames():
    out = [frame(pairs([("s", "'cat'"), ("id(s)", "0x1f40")], {"s": "lo"},
                       label="names -> objects"),
                 "One name, one string object. Nothing surprising yet.",
                 {"objects": 1})]
    out.append(frame(pairs([("s", "'cat'"), ("id(s)", "0x1f40"),
                            ("t", "'cat'"), ("id(t)", "0x1f40")],
                           {"t": "done"}, label="names -> objects"),
                     "t = s binds a second name to the SAME object. No copy was "
                     "made, and none is needed - the object cannot change.",
                     {"objects": 1}))
    out.append(frame(pairs([("s", "'cat'"), ("id(s)", "0x1f40"),
                            ("t", "'CAT'"), ("id(t)", "0x2b90")],
                           {"t": "hit"}, label="names -> objects"),
                     "t = s.upper() built a NEW object and pointed t at it. "
                     "s never changed, because s could not change.",
                     {"objects": 2}))
    out.append(frame(pairs([("s", "'cat'"), ("hash(s)", "stable"),
                            ("d[s]", "works")], {"hash(s)": "done"},
                           label="what that buys"),
                     "Because the value can never change, the hash can never go "
                     "stale - which is the whole reason a string can be a "
                     "dictionary key and a list cannot.",
                     {"objects": 2}))
    return viz(out)


_q(
    slug="why-are-python-strings-immutable",
    kind="concept",
    level="Easy",
    title="Why are Python strings immutable?",
    asked="Why are Python strings immutable, and what does that buy you?",
    desc="Why Python strings cannot be modified in place, what immutability buys "
         "you (hashability, safe sharing, interning), and what it costs.",
    lead="Because a string's value can never change, its hash can never go stale "
         "and a reference to it can never be invalidated by someone else. That is "
         "what makes strings usable as <strong>dictionary keys</strong> and safe "
         "to share without copying. The cost is that every \"modification\" builds "
         "a new object.",
    say="\"Immutable means every operation returns a new string. It buys "
        "hashability - so strings can be dict keys - and it means sharing a "
        "string is free. It costs you concatenation in a loop, which is why you "
        "use join.\"",
    notice=[
        "<code>t = s</code> makes no copy &mdash; both names point at one object.",
        "<code>upper()</code> returns a <em>different</em> object; <code>s</code> "
        "is untouched.",
        "The stable hash at the end is the payoff, not a side effect.",
    ],
    viz=_immutable_frames(),
    sections=[
        ("What immutability actually means",
         "<p>There is no operation in Python that changes a string in place. "
         "<code>s.upper()</code>, <code>s.replace()</code>, <code>s.strip()</code> "
         "and <code>s + t</code> all <em>return</em> a new string and leave the "
         "original exactly as it was. Assigning to an index &mdash; "
         "<code>s[0] = 'A'</code> &mdash; is not slow, it is a "
         "<code>TypeError</code>.</p>"
         "<p>This is enforced, not advisory. There is no private method and no "
         "escape hatch, which is what lets the interpreter make assumptions it "
         "could not otherwise make.</p>"),
        ("The three things it buys",
         "<p><strong>Hashability.</strong> A dictionary stores a key in a slot "
         "chosen from its hash. If the key could change after insertion, its hash "
         "would no longer match its slot and the entry would become unreachable. "
         "Immutable types can be keys; mutable ones cannot, which is why "
         "<code>{[1,2]: 'x'}</code> raises and <code>{(1,2): 'x'}</code> does "
         "not.</p>"
         "<p><strong>Free sharing.</strong> Passing a string to a function, "
         "storing it in two places, closing over it &mdash; none of these need a "
         "defensive copy, because no one can modify it behind your back. In a "
         "language with mutable strings, library code often copies on the way in "
         "just in case.</p>"
         "<p><strong>Interning.</strong> CPython reuses one object for short "
         "string literals that look like identifiers, so equality can often be "
         "settled by an identity check. That is an optimisation immutability "
         "makes legal.</p>"),
        ("What it costs, and the one place it bites",
         "<p>Every edit allocates. Usually that is irrelevant &mdash; one "
         "<code>replace</code> on one line costs nothing you can measure. It "
         "matters in exactly one shape: building a string a piece at a time in a "
         "loop.</p>"
         "<p>Each <code>+=</code> copies everything accumulated so far, so n "
         "appends copy 1 + 2 + 3 + ... + n characters, which is O(n&sup2;). The "
         "fix is <code>\"\".join(parts)</code>: one pass to total the lengths, "
         "one allocation, one copy. The editor below measures both.</p>"),
        ("The follow-up you should expect",
         "<p>\"If strings are immutable, why does <code>s += 'x'</code> sometimes "
         "look fast?\" CPython has a special case that resizes a string in place "
         "when the target is a plain local variable and nothing else refers to "
         "it. It is real, it is invisible, and it stops firing the moment you "
         "store into an attribute or a list. Do not build on it.</p>"),
    ],
    code={
        "file": "immutable.py",
        "intro": "Object identities before and after a \"modification\", then the "
                 "cost of ignoring what that implies &mdash; measured at three "
                 "sizes so the shape of the curve is visible rather than asserted.",
        "code": '''# Immutability, and the one place it costs you.
import time

s = "cat"
t = s                       # a second NAME, not a second object
print("s =", s, " id:", hex(id(s)))
print("t =", t, " id:", hex(id(t)), " same object:", t is s)

u = s.upper()               # a NEW object; s is untouched
print("u =", u, " id:", hex(id(u)), " same object:", u is s)
print("s is still:", s)

try:
    s[0] = "C"
except TypeError as e:
    print("s[0] = 'C' ->", e)

# Hashability is the payoff: the value cannot change, so the hash cannot
# go stale, so a string can be a dictionary key.
print("hash stable:", hash("cat") == hash(s))
try:
    {["c", "a", "t"]: 1}
except TypeError as e:
    print("list as a key ->", e)

# --- the cost, measured -------------------------------------------------
class Buf:                  # an attribute, so CPython's in-place resize
    def __init__(self):     # special case cannot fire and hide the cost
        self.text = ""

print()
print(f"{'n':>7} {'+= in a loop':>14} {'list + join':>13} {'ratio':>7}")
for n in (20_000, 40_000, 80_000):
    b = Buf()
    start = time.time()
    for _ in range(n):
        b.text += "x"
    concat = time.time() - start

    start = time.time()
    parts = []
    for _ in range(n):
        parts.append("x")
    joined_text = "".join(parts)
    joined = time.time() - start
    print(f"{n:>7} {concat:>13.4f}s {joined:>12.4f}s {concat / joined:>6.1f}x")

print("Double n: join doubles, += quadruples. That is O(n) against O(n^2).")
''',
        "walk": [
            ("t = s",
             "Binds a second name to the same object, which <code>t is s</code> "
             "confirms. No copy is made because none is needed &mdash; neither "
             "name can change the value."),
            ("u = s.upper()",
             "A different id. Every string method returns a new object; none of "
             "them has a way to modify the receiver."),
            ("hash(\"cat\") == hash(s)",
             "The hash is a function of the value, and the value is frozen for "
             "the object's whole life. That is the precondition a dictionary key "
             "has to meet."),
            ("self.text += \"x\"",
             "Accumulating into an attribute rather than a local is deliberate: "
             "CPython can resize a local string in place, which would hide the "
             "quadratic the table is there to show."),
        ],
        "try": [
            "Add <code>v = \"cat\"</code> and check <code>v is s</code>. Short "
            "literals are interned, so it is often <code>True</code> &mdash; and "
            "relying on that is still a bug.",
            "Swap <code>b.text</code> for a local variable and re-run. Whether "
            "the quadratic disappears depends on your interpreter, which is "
            "itself the argument for <code>join</code>.",
        ],
    },
    check=[
        {"q": "Why can a string be a dictionary key when a list cannot?",
         "options": ["Strings are shorter",
                     "A string's value cannot change, so its hash cannot go stale",
                     "Lists are not comparable",
                     "Dictionaries only accept text"],
         "answer": 1,
         "why": "A key is stored in a slot chosen from its hash. If the value "
                "could change afterwards the entry would sit in the wrong slot "
                "and become unreachable, so only immutable types are allowed."},
        {"q": "What does s.upper() do to s?",
         "options": ["Uppercases it in place", "Nothing - it returns a new string",
                     "Raises unless you assign it", "Depends on the encoding"],
         "answer": 1,
         "why": "Every string method returns a new object. Forgetting to assign "
                "the result is one of the most common beginner bugs in Python."},
        {"q": "Building a string with += in a loop is O(n²) because each step:",
         "options": ["Re-encodes to UTF-8", "Allocates a new string and copies "
                     "everything so far",
                     "Sorts the characters", "Grows the underlying list"],
         "answer": 1,
         "why": "There is nothing to append to, so the accumulated text is "
                "copied every time. \"\".join(parts) does one allocation and one "
                "copy instead."},
    ],
)


def _slice_frames():
    text = "algorithms"
    out = []
    marks = {i: "dim" for i in range(len(text))}
    out.append(frame(marked(list(text), dict(marks), kind="text", label="s"),
                     "The original string, ten characters, one object.",
                     {"objects": 1, "copied": 0}))
    m2 = {i: ("hit" if 2 <= i < 6 else "dim") for i in range(len(text))}
    out.append(frame([marked(list(text), m2, {2: "start", 6: "stop"},
                             kind="text", label="s"),
                      marked(list("gori"), {i: "done" for i in range(4)},
                             kind="text", label="s[2:6]")],
                     "s[2:6] does not point into s. Four characters were copied "
                     "into a brand-new object.",
                     {"objects": 2, "copied": 4}))
    out.append(frame([marked(list(text), {i: "dim" for i in range(len(text))},
                             kind="text", label="s"),
                      marked(list(text[::-1]), {i: "done" for i in range(len(text))},
                             kind="text", label="s[::-1]")],
                     "A full reversal copies all ten. Slicing is always O(k) time "
                     "AND O(k) memory in the size of the slice.",
                     {"objects": 2, "copied": 10}))
    return viz(out)


_q(
    slug="what-does-string-slicing-cost",
    kind="concept",
    level="Easy",
    title="What does slicing a string cost?",
    asked="What does s[2:6] cost, and is it a view or a copy?",
    desc="Python string slices are copies, not views: O(k) time and O(k) memory "
         "in the size of the slice, and why that matters inside a loop.",
    lead="A slice is a <strong>copy</strong>, never a view. <code>s[2:6]</code> "
         "allocates a new string and copies four characters, so slicing is O(k) "
         "in both time and memory for a slice of length k. One slice is free; a "
         "slice per iteration is how an O(n) scan quietly becomes O(n&sup2;).",
    say="\"Slices copy. It's O(k) time and space for a k-length slice, so inside "
        "a loop I carry indices instead of slicing.\"",
    notice=[
        "The second row is a <em>separate object</em>, not a window into the first.",
        "<code>s[::-1]</code> copies the whole string &mdash; fine once, expensive "
        "in a loop.",
        "Compare with <code>memoryview</code>, which really is a view &mdash; but "
        "only over <code>bytes</code>.",
    ],
    viz=_slice_frames(),
    sections=[
        ("Copy, not view",
         "<p>Some languages hand you a slice that points into the original "
         "buffer, so taking one is O(1). Python does not: <code>s[2:6]</code> "
         "allocates a new string object and memcpys four characters into it. The "
         "cost is proportional to the slice, not to the original.</p>"
         "<p>You can prove it from the interpreter: the id differs, and mutating "
         "is impossible anyway, so there is no aliasing to observe. What you can "
         "measure is the time, which is what the editor below does.</p>"),
        ("Where it actually hurts",
         "<p>One slice costs nothing worth thinking about. The problem is the "
         "shape where a slice is taken per iteration &mdash; checking every "
         "substring, or peeling a character off the front:</p>"
         "<p><code>while s: first, s = s[0], s[1:]</code></p>"
         "<p>Each iteration copies the entire remainder, so an O(n) walk becomes "
         "O(n&sup2;). The same bug appears in recursive solutions that pass "
         "<code>s[1:]</code> down: correct, elegant, and quadratic.</p>"),
        ("What to do instead",
         "<p>Carry indices. Every algorithm on this track that scans text &mdash; "
         "two pointers, sliding window, KMP &mdash; keeps <code>i</code> and "
         "<code>j</code> into the original string and never slices inside the "
         "loop. Slice once at the end, when you need the answer as a string.</p>"
         "<p>If you genuinely need a zero-copy view over a large buffer, that "
         "exists, but only for bytes: <code>memoryview(b)</code> slices in O(1) "
         "and shares the underlying memory.</p>"),
    ],
    code={
        "file": "slicing.py",
        "intro": "The same scan written twice &mdash; once slicing on every "
                 "iteration, once carrying indices &mdash; timed at three sizes so "
                 "the quadratic separates from the linear in front of you.",
        "code": '''# A slice is a copy. One is free; one per iteration is quadratic.
import time

s = "algorithms"
part = s[2:6]
print("s      :", s)
print("s[2:6] :", part, " same object as s:", part is s)
print("reversed:", s[::-1], "- a full copy, O(n) time and space")

# --- the shape that goes quadratic --------------------------------------
def peel_with_slices(text):
    """Walk the string by chopping the front off. Copies the rest each time."""
    n = 0
    while text:
        _first = text[0]
        text = text[1:]          # copies len(text) - 1 characters. Every time.
        n += 1
    return n


def walk_with_index(text):
    """The same walk, carrying an index. Nothing is copied at all."""
    n = 0
    i = 0
    while i < len(text):
        _first = text[i]
        i += 1
        n += 1
    return n


print()
print(f"{'n':>7} {'slicing':>12} {'indexing':>12} {'ratio':>8}")
for n in (5_000, 10_000, 20_000):
    text = "x" * n

    start = time.time()
    peel_with_slices(text)
    slicing = time.time() - start

    start = time.time()
    walk_with_index(text)
    indexing = time.time() - start

    print(f"{n:>7} {slicing:>11.4f}s {indexing:>11.4f}s {slicing / indexing:>7.1f}x")

print("Double n: indexing doubles, slicing quadruples.")
print()
print("memoryview really is a view - but only over bytes:")
buf = memoryview(b"algorithms")
print("  buf[2:6] ->", bytes(buf[2:6]), "- no copy of the underlying buffer")
''',
        "walk": [
            ("part is s",
             "<code>False</code>. The slice is a separate object holding its own "
             "four characters, which is the entire question."),
            ("text = text[1:]",
             "Looks like advancing a pointer and is nothing of the sort: it "
             "allocates a string one shorter and copies into it. Doing that n "
             "times copies about n&sup2;/2 characters."),
            ("i += 1",
             "The same traversal with no allocation at all. This is why every "
             "scanning algorithm here carries indices rather than slicing."),
            ("memoryview(b\"algorithms\")",
             "The zero-copy answer, and the reason to know the difference: "
             "slicing a memoryview is O(1) and shares memory. It works on "
             "<code>bytes</code>, not <code>str</code>."),
        ],
        "try": [
            "Write the recursive version &mdash; <code>def walk(s): return 1 + "
            "walk(s[1:]) if s else 0</code>. Elegant, and quadratic for the same "
            "reason.",
            "Raise n to 40,000 and watch the ratio roughly double again.",
        ],
    },
    check=[
        {"q": "s[2:6] returns:",
         "options": ["A view into s", "A new string holding a copy of four characters",
                     "A list of characters", "A generator"],
         "answer": 1,
         "why": "Python string slices always copy. The cost is O(k) in the length "
                "of the slice, in both time and memory."},
        {"q": "Why does peeling characters off the front with s = s[1:] go "
              "quadratic?",
         "options": ["The loop runs twice", "Each iteration copies the whole "
                     "remaining string",
                     "Strings are re-encoded", "len() is O(n)"],
         "answer": 1,
         "why": "n iterations copying an average of n/2 characters each is "
                "O(n²). Carrying an index copies nothing."},
        {"q": "Which type gives you a genuine zero-copy slice?",
         "options": ["str", "memoryview over bytes", "list", "tuple"],
         "answer": 1,
         "why": "memoryview shares the underlying buffer, so slicing it is O(1). "
                "It works on bytes-like objects, not on str."},
    ],
)


def _len_frames():
    out = []
    out.append(frame(marked(list("cafe"), {i: "done" for i in range(4)},
                            kind="text", label="'cafe'"),
                     "Four characters, four code points, and - in UTF-8 - four "
                     "bytes. Everything agrees.",
                     {"len": 4, "utf8 bytes": 4}))
    out.append(frame(marked(list("café"), {3: "hit"}, kind="text",
                            label="'café'"),
                     "len() is 4 - it counts code points. Encoded as UTF-8 it is "
                     "5 bytes, because e-acute needs two.",
                     {"len": 4, "utf8 bytes": 5}))
    out.append(frame(marked(list("café"), {3: "hit", 4: "bad"}, kind="text",
                            label="'cafe' + combining accent"),
                     "This LOOKS identical and len() is 5: 'e' followed by a "
                     "combining accent. Two strings, same appearance, different "
                     "length and not equal.",
                     {"len": 5, "utf8 bytes": 6}))
    out.append(frame(pairs([("len('café')", "4"),
                            ("len('café')", "5"),
                            ("they are equal", "False"),
                            ("after NFC normalisation", "equal")],
                           {"after NFC normalisation": "hit"}, label="the fix"),
                     "unicodedata.normalize('NFC', ...) collapses the second form "
                     "into the first. This is why user input gets normalised "
                     "before it is compared or stored.",
                     {"len": 4, "utf8 bytes": 5}))
    return viz(out)


_q(
    slug="does-len-count-characters-or-bytes",
    kind="concept",
    level="Medium",
    title="Does len() count characters or bytes?",
    asked="Is len(s) the number of characters or the number of bytes?",
    desc="len() on a Python 3 string counts code points, not bytes and not "
         "user-perceived characters - and why emoji and accents break the "
         "assumption.",
    lead="Neither, strictly. <code>len(s)</code> counts <strong>code "
         "points</strong>. For ASCII that happens to equal both the byte count "
         "and what a reader would call characters, which is why the distinction "
         "stays hidden until an accent or an emoji arrives.",
    say="\"len counts code points. Bytes is len(s.encode('utf-8')), and neither "
        "is what a user calls a character once you have combining accents or "
        "emoji.\"",
    notice=[
        "The second and third rows <em>look</em> the same and are not equal.",
        "One is <code>e&#769;</code> as a single code point, the other is "
        "<code>e</code> plus a combining mark.",
        "Normalising is what makes the comparison behave.",
    ],
    viz=_len_frames(),
    sections=[
        ("Three different counts",
         "<p>There are three things you could mean by \"length\", and they "
         "coincide only for ASCII:</p>"
         "<p><strong>Code points</strong> &mdash; what <code>len(s)</code> "
         "returns. A Python 3 <code>str</code> is a sequence of code points, and "
         "indexing gives you one.</p>"
         "<p><strong>Bytes</strong> &mdash; <code>len(s.encode('utf-8'))</code>. "
         "Depends entirely on the encoding, which is why the encoding has to be "
         "named. This is the number that matters for a database column or a "
         "network frame.</p>"
         "<p><strong>Grapheme clusters</strong> &mdash; what a human counts. "
         "Python has no built-in for this; it needs a library.</p>"),
        ("Where it goes wrong",
         "<p>Two strings that render identically can have different lengths and "
         "compare unequal, because <code>&eacute;</code> can be one code point "
         "or two (<code>e</code> plus a combining accent). Users produce both, "
         "depending on their keyboard and operating system.</p>"
         "<p>The fix is normalisation: <code>unicodedata.normalize('NFC', s)</code> "
         "before comparing or storing. Any system that accepts names, "
         "usernames or search terms needs this, and most learn it from a bug "
         "report.</p>"
         "<p>Emoji are the other reliable surprise. A family emoji or a "
         "skin-tone modifier is several code points joined by zero-width "
         "joiners, so <code>len</code> says 5 or 7 for something a user counts "
         "as one, and slicing it in half produces garbage.</p>"),
        ("The practical rule",
         "<p>Use <code>len(s)</code> for indexing and slicing your own text. Use "
         "<code>len(s.encode('utf-8'))</code> whenever a limit is a storage or "
         "transport limit. Normalise on input. And if you are truncating text "
         "for display &mdash; a preview, a tweet counter &mdash; know that code "
         "points are an approximation you may have to replace.</p>"),
    ],
    code={
        "file": "lengths.py",
        "intro": "The same visible text three ways, with all three counts printed "
                 "for each. The two strings in the middle look identical in your "
                 "browser and are not equal.",
        "code": '''# len() counts code points. That is not bytes, and not "characters".
import unicodedata

samples = {
    "ascii":            "cafe",
    "precomposed":      "caf\\u00e9",        # e-acute as ONE code point
    "decomposed":       "cafe\\u0301",       # 'e' + combining acute: TWO
    "emoji":            "\\U0001f44d",       # thumbs up
}

print(f"{'name':>14} {'shown':>8} {'len':>5} {'utf-8':>6} {'utf-16':>7}")
for name, s in samples.items():
    print(f"{name:>14} {s:>8} {len(s):>5} "
          f"{len(s.encode('utf-8')):>6} {len(s.encode('utf-16-le')):>7}")

a, b = samples["precomposed"], samples["decomposed"]
print()
print("precomposed == decomposed :", a == b)
print("they render the same, and len differs:", len(a), "vs", len(b))

# Normalising collapses them to one form, which is what makes comparison work.
na = unicodedata.normalize("NFC", a)
nb = unicodedata.normalize("NFC", b)
print("after NFC                 :", na == nb, " len:", len(na), len(nb))

# Slicing by code point can cut a character in half.
flag = "\\U0001f1ee\\U0001f1f3"        # regional indicators: one flag
print()
print("flag       :", flag, " len:", len(flag))
print("flag[:1]   :", flag[:1], "- half a flag is not a flag")

# The count a user would give needs grapheme clusters, which the standard
# library does not provide. This approximates it by dropping combining marks.
def graphemes(s):
    return sum(1 for ch in unicodedata.normalize("NFC", s)
               if not unicodedata.combining(ch))

for name, s in samples.items():
    print(f"{name:>14}: len={len(s)} approx graphemes={graphemes(s)}")
''',
        "walk": [
            ("len(s)",
             "Counts code points, because a Python 3 <code>str</code> <em>is</em> "
             "a sequence of code points. Indexing returns one of them."),
            ("len(s.encode('utf-8'))",
             "The byte count, and the only one that answers \"will this fit in "
             "the column?\". It depends on the encoding, which is why the "
             "encoding must be named rather than assumed."),
            ("a == b",
             "<code>False</code> for two strings that render identically. "
             "Equality is over code points, and the two forms are different "
             "sequences of them."),
            ("unicodedata.normalize(\"NFC\", ...)",
             "Puts both into the same canonical form so they compare equal. Any "
             "system taking user-entered names or search terms needs this on the "
             "way in."),
        ],
        "try": [
            "Add a family emoji. <code>len</code> reports 7 or more &mdash; it is "
            "several people joined by zero-width joiners.",
            "Encode the emoji as <code>utf-32-le</code> and compare the byte "
            "counts. Fixed-width encodings make <code>len</code> and bytes agree "
            "again, at four bytes per code point.",
        ],
    },
    check=[
        {"q": "len(s) on a Python 3 string counts:",
         "options": ["Bytes", "Code points", "Grapheme clusters", "UTF-16 units"],
         "answer": 1,
         "why": "A str is a sequence of code points. Bytes depend on an encoding, "
                "and graphemes need a library the standard library does not ship."},
        {"q": "Two strings render identically but compare unequal. The most "
              "likely cause is:",
         "options": ["A trailing space", "One uses a combining accent and the "
                     "other a precomposed character",
                     "Different encodings", "One is bytes"],
         "answer": 1,
         "why": "é can be one code point or 'e' plus a combining mark. "
                "unicodedata.normalize('NFC', s) collapses them before comparison."},
        {"q": "You need to enforce a 100-character database limit. You should "
              "measure:",
         "options": ["len(s)", "len(s.encode('utf-8')) if the column is measured "
                     "in bytes",
                     "The number of words", "sys.getsizeof(s)"],
         "answer": 1,
         "why": "Storage and transport limits are byte limits. A 100-code-point "
                "string can be 400 bytes in UTF-8."},
    ],
)


def _bytes_frames():
    out = [frame(marked(list("héllo"), {1: "hit"}, kind="text", label="str: code points"),
                 "A str is a sequence of code points. Indexing gives you one of "
                 "them, and no encoding is involved yet.",
                 {"len": 5, "type": "str"})]
    out.append(frame([marked(list("héllo"), {1: "hit"}, kind="text", label="str"),
                      marked(["68", "c3", "a9", "6c", "6c", "6f"], {1: "hit", 2: "hit"},
                             label="utf-8 bytes")],
                     "encode('utf-8') produces bytes. The e-acute became TWO of "
                     "them, so positions no longer line up.",
                     {"len": 6, "type": "bytes"}))
    out.append(frame(pairs([("open(path)", "text mode -> str"),
                            ("open(path, 'rb')", "binary mode -> bytes"),
                            ("socket.recv()", "bytes"),
                            ("json.dumps()", "str")],
                           {"socket.recv()": "hit"}, label="which do you get?"),
                     "The boundary is I/O. Anything crossing a wire or a disk is "
                     "bytes; everything inside your program should be str.",
                     {"len": 6, "type": "bytes"}))
    return viz(out)


_q(
    slug="str-versus-bytes-in-python",
    kind="concept",
    level="Medium",
    title="What is the difference between str and bytes?",
    asked="What is the difference between str and bytes, and when do you need "
          "encode and decode?",
    desc="str is a sequence of code points, bytes is a sequence of 8-bit values, "
         "and encode/decode is the boundary between them - with the errors that "
         "happen when you cross it wrongly.",
    lead="A <code>str</code> is a sequence of <strong>code points</strong> and "
         "carries no encoding. <code>bytes</code> is a sequence of 8-bit values "
         "and carries no meaning until you name one. <code>encode</code> goes "
         "str&nbsp;&rarr;&nbsp;bytes, <code>decode</code> comes back, and the "
         "rule is to do both at the edges of your program and work in "
         "<code>str</code> everywhere inside.",
    say="\"str is text, bytes is data. Encode at the way out, decode at the way "
        "in, and never let bytes travel through your logic.\"",
    notice=[
        "One code point became <em>two</em> bytes &mdash; positions stop matching.",
        "Slicing bytes can split a character in half; slicing str cannot.",
        "The boundary is always I/O: files, sockets, subprocesses.",
    ],
    viz=_bytes_frames(),
    sections=[
        ("Two different things that both print nicely",
         "<p><code>\"hi\"</code> and <code>b\"hi\"</code> look almost identical "
         "and are not comparable: <code>\"hi\" == b\"hi\"</code> is "
         "<code>False</code>, and in Python 3 that is deliberate. A str has no "
         "encoding &mdash; asking for the bytes of a str is meaningless until "
         "you say <em>which</em> bytes, which is why <code>encode</code> takes "
         "an argument.</p>"
         "<p>Indexing differs too. <code>s[0]</code> on a str gives a "
         "one-character str; <code>b[0]</code> on bytes gives an "
         "<code>int</code>. That catches people constantly.</p>"),
        ("The sandwich rule",
         "<p>Decode at the boundary in, encode at the boundary out, and keep the "
         "middle in <code>str</code>. Every layer of a well-behaved program "
         "works in text; only the outermost layer knows about UTF-8.</p>"
         "<p>Violating it produces the two classic errors. "
         "<code>UnicodeDecodeError</code> means you were handed bytes that are "
         "not valid in the encoding you claimed &mdash; usually the encoding is "
         "wrong, not the data. <code>UnicodeEncodeError</code> means you tried "
         "to write a character the target encoding cannot represent, which is "
         "what happens when something defaults to ASCII or latin-1.</p>"),
        ("Where it actually shows up",
         "<p>Reading a file with <code>open(path)</code> gives str and applies "
         "your platform's default encoding, which differs between machines and "
         "is the source of \"works on my laptop\" bugs. Pass "
         "<code>encoding=\"utf-8\"</code> explicitly, always. "
         "<code>open(path, \"rb\")</code> gives bytes and does not guess.</p>"
         "<p>Sockets, subprocess output, hashlib and most binary formats are "
         "bytes. <code>hashlib.sha256(s)</code> is a <code>TypeError</code> until "
         "you encode &mdash; a hash is defined over bytes, so the encoding is "
         "part of the answer.</p>"),
    ],
    code={
        "file": "str_bytes.py",
        "intro": "The same text as both types, with the ways they refuse to mix, "
                 "and both Unicode errors triggered on purpose so you have seen "
                 "the tracebacks before an interviewer describes one.",
        "code": '''# str is text. bytes is data. encode/decode is the border crossing.

s = "h\\u00e9llo"                 # h, e-acute, l, l, o
b = s.encode("utf-8")

print("str   :", s, " len:", len(s), " type:", type(s).__name__)
print("bytes :", b, " len:", len(b), " type:", type(b).__name__)
print("equal :", s == b, "- they are never equal in Python 3")

print()
print("s[1] :", repr(s[1]), "-> a one-character str")
print("b[1] :", repr(b[1]), "-> an int, not a character")
print("round trip:", b.decode("utf-8") == s)

# Slicing bytes can cut a character in half. Slicing str cannot.
print()
print("b[:2] :", b[:2])
try:
    print(b[:2].decode("utf-8"))
except UnicodeDecodeError as e:
    print("b[:2].decode() ->", e)

# The other direction: a character the target encoding cannot represent.
try:
    s.encode("ascii")
except UnicodeEncodeError as e:
    print("s.encode('ascii') ->", e)

# Same bytes, wrong encoding: no error, silently wrong text. This is worse.
print()
print("decoded as latin-1:", repr(b.decode("latin-1")))
print("No exception, and the text is wrong. Mojibake is a decode with the")
print("wrong encoding, not a corrupted file.")

import hashlib
print()
try:
    hashlib.sha256(s)
except TypeError as e:
    print("sha256(str) ->", e)
print("sha256(bytes) ->", hashlib.sha256(b).hexdigest()[:16], "...")
''',
        "walk": [
            ("s.encode(\"utf-8\")",
             "The encoding is an argument because a str genuinely does not have "
             "bytes until you choose. There is no default worth relying on."),
            ("b[1] is an int",
             "Indexing bytes yields the numeric value, not a one-length bytes. "
             "It is the single most common surprise when code written for str "
             "is pointed at bytes."),
            ("b[:2].decode(\"utf-8\")",
             "Raises, because the slice split a two-byte character. Any code "
             "that chunks a byte stream has to respect character boundaries, "
             "which is why streaming decoders exist."),
            ("b.decode(\"latin-1\")",
             "The dangerous one: no exception, wrong text. latin-1 maps every "
             "byte to something, so it never fails and never warns. Mojibake is "
             "this, not a corrupted file."),
        ],
        "try": [
            "Encode as <code>utf-16</code> and print the bytes. Note the "
            "byte-order mark at the front, and that the length roughly doubles.",
            "Call <code>b.decode(\"utf-8\", errors=\"replace\")</code> on the "
            "broken slice. You get U+FFFD instead of an exception &mdash; useful "
            "for logs, wrong for data you intend to keep.",
        ],
    },
    check=[
        {"q": "b[0] where b is a bytes object gives you:",
         "options": ["A one-character bytes", "An int", "A str", "A TypeError"],
         "answer": 1,
         "why": "Indexing bytes yields the numeric value of that byte. Slicing "
                "gives bytes back; indexing does not."},
        {"q": "Decoding UTF-8 data as latin-1 produces:",
         "options": ["A UnicodeDecodeError", "Wrong text, with no error at all",
                     "The same text", "An empty string"],
         "answer": 1,
         "why": "latin-1 maps every possible byte to some character, so it never "
                "fails. That silence is what makes mojibake hard to trace."},
        {"q": "Where should encode and decode happen in a well-structured "
              "program?",
         "options": ["Everywhere, as needed", "Only at the I/O boundaries, with "
                     "str used throughout the middle",
                     "Only on user input", "Never - Python handles it"],
         "answer": 1,
         "why": "The sandwich rule: decode on the way in, encode on the way out, "
                "and let every internal layer work in text."},
    ],
)


def _interning_frames():
    out = [frame(pairs([("a = 'hello'", "0x1a40"), ("b = 'hello'", "0x1a40"),
                        ("a is b", "True")], {"a is b": "done"}, label="literals"),
                 "Two identical literals that look like identifiers: CPython "
                 "interns them, so both names point at one object.",
                 {"objects": 1})]
    out.append(frame(pairs([("a = 'hello world'", "0x1a40"),
                            ("b = 'hello' + ' world'", "0x3f10"),
                            ("a is b", "False"),
                            ("a == b", "True")],
                           {"a is b": "bad", "a == b": "hit"}, label="built at runtime"),
                     "Built at runtime instead of being a literal, so no "
                     "interning. `is` is now False while `==` is still True - "
                     "which is the whole trap.",
                     {"objects": 2}))
    out.append(frame(pairs([("use ==", "compares value - always right"),
                            ("use is", "compares identity - only for None, "
                                       "True, False")],
                           {"use ==": "hit"}, label="the rule"),
                     "The behaviour is an implementation detail that changes "
                     "between versions and between the REPL and a script. Never "
                     "compare strings with `is`.",
                     {"objects": 2}))
    return viz(out)


_q(
    slug="string-interning-and-the-is-operator",
    kind="concept",
    level="Medium",
    title="Why does `is` sometimes work on strings?",
    asked="Why does 'a' is 'a' return True, and why should you never rely on it?",
    desc="String interning in CPython: why identical literals share one object, "
         "why runtime-built strings do not, and why == is the only correct "
         "comparison.",
    lead="CPython <strong>interns</strong> short string literals that look like "
         "identifiers, so two of them share one object and <code>is</code> "
         "happens to be <code>True</code>. Build the same text at runtime and it "
         "is <code>False</code>. It is an optimisation, not a guarantee &mdash; "
         "compare strings with <code>==</code>, and keep <code>is</code> for "
         "<code>None</code>.",
    say="\"That's interning - CPython reuses one object for short literals. It's "
        "an implementation detail, so I compare with == and only use `is` for "
        "None.\"",
    notice=[
        "Both rows hold the same text; only how it was built differs.",
        "<code>==</code> is <code>True</code> in every frame. <code>is</code> is "
        "not.",
        "Behaviour differs between the REPL and a script &mdash; which is the "
        "point.",
    ],
    viz=_interning_frames(),
    sections=[
        ("What interning is",
         "<p>CPython keeps a table of strings and reuses the entry rather than "
         "allocating a second identical object. Identifiers, and literals in "
         "compiled code that look like identifiers, go in it automatically. The "
         "payoff is real: comparing interned strings can short-circuit on a "
         "pointer comparison, and attribute lookup does this constantly.</p>"
         "<p>Immutability is what makes it legal. Sharing one object between "
         "unrelated pieces of code would be a disaster if either could modify "
         "it.</p>"),
        ("Why it is a trap",
         "<p>The rules are not part of the language. They vary by CPython "
         "version, by whether the string was a literal in a compiled block, by "
         "whether it contains a space, and by whether the constant folder saw "
         "it. The REPL compiles line by line and a script compiles as a unit, so "
         "the same code can behave differently in the two.</p>"
         "<p>Code that uses <code>is</code> on strings therefore works in "
         "testing, works in the REPL, and fails on the one input that was built "
         "by concatenation. That failure looks like a logic error, not a "
         "comparison error, which is why it takes so long to find.</p>"),
        ("The rule, and the exception",
         "<p>Use <code>==</code> for strings, always. Use <code>is</code> only "
         "for singletons &mdash; <code>None</code>, <code>True</code>, "
         "<code>False</code> &mdash; where identity <em>is</em> the intended "
         "test.</p>"
         "<p>There is one legitimate use of interning: "
         "<code>sys.intern(s)</code>, called deliberately on a large set of "
         "repeated strings such as parsed field names, cuts memory and speeds up "
         "dictionary lookups. That is opting in, which is different from relying "
         "on a coincidence.</p>"),
    ],
    code={
        "file": "interning.py",
        "intro": "Four ways of producing the same five characters, with identity "
                 "and equality printed for each. Some of the <code>is</code> "
                 "results may differ on your interpreter &mdash; that is the "
                 "lesson, not a bug.",
        "code": '''# Interning: why `is` sometimes agrees with `==`, and why you cannot trust it.
import sys

a = "hello"
b = "hello"                      # identical literal - interned
c = "hel" + "lo"                 # folded at compile time - usually interned too
parts = ["hel", "lo"]
d = "".join(parts)               # built at RUNTIME - not interned

for name, value in [("b", b), ("c", c), ("d", d)]:
    print(f"a is {name}: {str(a is value):>5}   a == {name}: {a == value}   "
          f"id: {hex(id(value))}")

print()
# Spaces stop a literal looking like an identifier.
e = "hello world"
f = "hello world"
g = "hello" + " world"
print("e is f (two literals)      :", e is f)
print("e is g (built by +)        :", e is g)
print("e == g                     :", e == g, "<- the only one that matters")

# Opting in deliberately is a different thing entirely.
print()
d2 = sys.intern(d)
print("after sys.intern(d), a is d2:", a is d2)

# Small integers have the same story, and the same trap.
print()
x, y = 256, 256
p, q = 257, 257
print("256 is 256:", x is y, "  257 is 257:", p is q)
print("CPython caches -5..256. Nothing in the language promises that.")
''',
        "walk": [
            ("a is b",
             "Two identical literals in the same compiled block share one "
             "object. This is the result people generalise from, and it is the "
             "narrowest case."),
            ("d = \"\".join(parts)",
             "Built while the program runs, so the interner never sees it. Same "
             "characters, different object, <code>is</code> is "
             "<code>False</code>."),
            ("e is g",
             "The space is the difference. A literal with a space does not look "
             "like an identifier, so the rules that produced <code>True</code> "
             "above do not apply."),
            ("sys.intern(d)",
             "The legitimate use: deliberately deduplicating a large set of "
             "repeated strings to cut memory and speed up dict lookups. Opting "
             "in is not the same as relying on an accident."),
        ],
        "try": [
            "Move the comparisons into a function and call it. Compiling as one "
            "unit can change the answers &mdash; which is exactly why this is "
            "not something to build on.",
            "Try <code>257 is 257</code> across a function boundary. Integers "
            "have the same cache, the same trap and the same rule.",
        ],
    },
    check=[
        {"q": "Why is 'hello' is 'hello' often True?",
         "options": ["Strings are compared by value",
                     "CPython interns identical short literals into one object",
                     "is and == are the same", "Both are empty"],
         "answer": 1,
         "why": "Interning reuses one object. It is an optimisation immutability "
                "makes legal, not a language guarantee."},
        {"q": "'hello world' is ('hello' + ' world') is usually False because:",
         "options": ["The strings differ", "The second is built at runtime, so "
                     "it is not interned",
                     "Spaces are not allowed", "+ returns a list"],
         "answer": 1,
         "why": "The interner sees literals in compiled code. A string assembled "
                "while the program runs is a fresh object."},
        {"q": "The only safe use of `is` is with:",
         "options": ["Short strings", "None, True and False",
                     "Numbers below 257", "Anything immutable"],
         "answer": 1,
         "why": "Those are singletons, so identity is genuinely the test you "
                "want. Everything else should use ==."},
    ],
)


def _find_frames():
    text, needle = "algorithms", "rit"
    out = []
    for i in range(len(text) - len(needle) + 1):
        window = text[i:i + len(needle)]
        ok = window == needle
        marks = {j: ("hit" if ok and i <= j < i + len(needle)
                     else "lo" if i <= j < i + len(needle) else "dim")
                 for j in range(len(text))}
        out.append(frame(marked(list(text), marks, {i: "i"}, kind="text",
                                label="'algorithms'.find('rit')"),
                         "Compare %r at index %d - %s."
                         % (window, i, "match, return %d" % i if ok else "no"),
                         {"i": i, "found": i if ok else -1}))
        if ok:
            break
    out.append(frame(pairs([("find('zzz')", "-1"),
                            ("index('zzz')", "ValueError"),
                            ("'zzz' in s", "False")],
                           {"index('zzz')": "bad"}, label="when it is missing"),
                     "The three differ only in how they report a miss: a "
                     "sentinel, an exception, or a bool.",
                     {"i": -1, "found": -1}))
    return viz(out)


_q(
    slug="find-versus-index-on-strings",
    kind="concept",
    level="Easy",
    title="find() vs index() vs `in` — which one?",
    asked="What is the difference between str.find and str.index, and when would "
          "you use each?",
    desc="find returns -1, index raises ValueError, and `in` returns a bool - "
         "choosing between them is about whether a miss is expected or "
         "exceptional.",
    lead="They do the same search and differ only in how they report a miss. "
         "<code>find</code> returns <code>-1</code>, <code>index</code> raises "
         "<code>ValueError</code>, and <code>in</code> returns a bool. Pick by "
         "whether a miss is <strong>expected</strong> (use <code>find</code> or "
         "<code>in</code>) or a <strong>bug</strong> (use <code>index</code>).",
    say="\"Same search, different failure. find gives -1, index raises, `in` "
        "gives a bool. If missing is normal I use find; if missing means "
        "something upstream is broken I use index so it fails loudly.\"",
    notice=[
        "All three scan the same way &mdash; the difference is only at the end.",
        "<code>-1</code> is a valid index in Python, which is why "
        "<code>find</code> has a sharp edge.",
        "<code>if s.find(x):</code> is a real bug &mdash; index 0 is falsy.",
    ],
    viz=_find_frames(),
    sections=[
        ("The same search, three reports",
         "<p><code>find</code> returns the index of the first occurrence, or "
         "<code>-1</code>. <code>index</code> returns the same index, or raises "
         "<code>ValueError</code>. <code>in</code> answers only yes or no, and "
         "reads better when that is all you need.</p>"
         "<p>All three are the same O(n&middot;m) scan underneath, so this is "
         "not a performance choice. There are <code>rfind</code> and "
         "<code>rindex</code> for the last occurrence, and all of them take "
         "optional start and end bounds &mdash; which is how you find the second "
         "occurrence without slicing.</p>"),
        ("The trap in find's return value",
         "<p><code>-1</code> is a perfectly valid index in Python, so a "
         "<code>find</code> result used without checking silently indexes from "
         "the end. Worse:</p>"
         "<p><code>if s.find(\"a\"):</code> is <code>False</code> when the match "
         "is at index 0 &mdash; the one case you were most likely to want. The "
         "check has to be <code>if s.find(\"a\") != -1:</code>, which is exactly "
         "why <code>in</code> exists.</p>"),
        ("How to choose",
         "<p>Use <code>in</code> when you only need to know whether it is there. "
         "Use <code>find</code> when a miss is a normal outcome you will branch "
         "on. Use <code>index</code> when a miss means something upstream is "
         "already broken and you would rather have a traceback at the real cause "
         "than a <code>-1</code> propagating three functions away.</p>"
         "<p>That last point is the answer interviewers are listening for: it is "
         "a question about error handling wearing a string-methods costume.</p>"),
    ],
    code={
        "file": "find_index.py",
        "intro": "The three calls on a hit and on a miss, then the two bugs "
                 "<code>find</code> invites &mdash; including the falsy-zero one, "
                 "shown giving a confidently wrong answer.",
        "code": '''# find, index and `in`: one search, three ways to report a miss.

s = "algorithms"

print("s.find('rit')   :", s.find("rit"))
print("s.index('rit')  :", s.index("rit"))
print("'rit' in s      :", "rit" in s)

print()
print("s.find('zzz')   :", s.find("zzz"), "  <- a sentinel")
try:
    s.index("zzz")
except ValueError as e:
    print("s.index('zzz')  -> ValueError:", e)
print("'zzz' in s      :", "zzz" in s)

# --- trap 1: -1 is a valid index ---------------------------------------
print()
i = s.find("zzz")
print("s[i] with i = -1 :", repr(s[i]), "- silently the LAST character")

# --- trap 2: index 0 is falsy ------------------------------------------
print()
for needle in ("alg", "rit", "zzz"):
    truthy = bool(s.find(needle))
    correct = s.find(needle) != -1
    flag = "  <-- WRONG" if truthy != correct else ""
    print(f"if s.find({needle!r}): -> {truthy!s:>5}   correct: {correct}{flag}")

# --- bounds find the next one without slicing --------------------------
print()
text = "the cat sat on the mat"
at = text.find("at")
while at != -1:
    print(f"  'at' at index {at}")
    at = text.find("at", at + 1)      # search from just past the last hit
''',
        "walk": [
            ("s.find(\"zzz\") -> -1",
             "A sentinel, not an error. Convenient when a miss is expected, and "
             "dangerous the moment the result is used without being checked."),
            ("s[i] with i = -1",
             "Silently the last character. Python's negative indexing means a "
             "forgotten check does not crash &mdash; it returns something "
             "plausible, which is worse."),
            ("if s.find(needle):",
             "<code>False</code> when the match is at index 0. The table shows "
             "it getting the first case wrong; the test has to be "
             "<code>!= -1</code>."),
            ("text.find(\"at\", at + 1)",
             "The start bound walks through every occurrence without slicing, "
             "which would copy the remainder on each step."),
        ],
        "try": [
            "Swap <code>find</code> for <code>index</code> in the loop and let "
            "it run off the end. The <code>ValueError</code> is the loop "
            "condition you forgot to write.",
            "Use <code>rfind</code> to walk backwards. Same bounds, same "
            "sentinel, opposite direction.",
        ],
    },
    check=[
        {"q": "s.index('zzz') when 'zzz' is absent:",
         "options": ["Returns -1", "Raises ValueError", "Returns None",
                     "Returns 0"],
         "answer": 1,
         "why": "That is the only difference from find. Use index when a miss "
                "means something upstream is broken and you want it to fail loudly."},
        {"q": "Why is `if s.find(x):` a bug?",
         "options": ["find is slow", "A match at index 0 is falsy, so it reads "
                     "as not found",
                     "find returns None", "It only works on lists"],
         "answer": 1,
         "why": "0 is a legitimate result and a falsy value. The test must be "
                "!= -1, which is why `in` is preferred when you only need a bool."},
        {"q": "To find the second occurrence of a substring, the cheapest "
              "approach is:",
         "options": ["Slice the string and search again",
                     "Pass a start index: s.find(x, first + 1)",
                     "Reverse the string", "Use a regex"],
         "answer": 1,
         "why": "The start bound avoids copying the remainder, which slicing in "
                "a loop would do on every iteration."},
    ],
)


# =========================================================================
# Coding problems
# =========================================================================

def _reverse_frames():
    chars = list("stressed")
    out = []
    lo, hi = 0, len(chars) - 1
    while lo < hi:
        marks = {i: "dim" for i in range(len(chars))}
        marks[lo] = "lo"
        marks[hi] = "hi"
        out.append(frame(marked(list(chars), marks, {lo: "lo", hi: "hi"},
                                kind="text", label="chars"),
                         "Swap %r and %r, then step both pointers inwards."
                         % (chars[lo], chars[hi]),
                         {"lo": lo, "hi": hi, "swaps": len(out)}))
        chars[lo], chars[hi] = chars[hi], chars[lo]
        lo, hi = lo + 1, hi - 1
    out.append(frame(marked(chars, {i: "done" for i in range(len(chars))},
                            kind="text", label="chars"),
                     "The pointers met. n/2 swaps, no second buffer - and "
                     "'stressed' happens to reverse into 'desserts'.",
                     {"lo": lo, "hi": hi, "swaps": len(out)}))
    return viz(out)


_q(
    slug="reverse-a-string",
    kind="coding",
    level="Easy",
    title="Reverse a string",
    asked="Reverse a string. Now do it in place, with O(1) extra memory.",
    desc="Reversing a string in Python: the slice idiom, why it costs O(n) "
         "memory, and the two-pointer in-place version an interviewer is "
         "actually asking for.",
    lead="<code>s[::-1]</code> is the idiomatic answer and allocates a full "
         "copy. The follow-up is always \"now in place\", which strings cannot "
         "do &mdash; so you convert to a list and run <strong>two "
         "pointers</strong> inwards, swapping as they go: n/2 swaps and O(1) "
         "extra memory.",
    say="\"s[::-1] in Python, but that's O(n) space. In place you'd take a "
        "character array and swap from both ends inwards until the pointers "
        "meet - n/2 swaps, O(1) extra.\"",
    notice=[
        "The two pointers move towards each other and stop when they meet.",
        "An odd-length string leaves the middle character alone &mdash; correct, "
        "not a bug.",
        "Nothing is allocated: the same list is being rearranged.",
    ],
    viz=_reverse_frames(),
    sections=[
        ("The Python answer, and why it is not the whole answer",
         "<p><code>s[::-1]</code> is correct, fast and what you should write in "
         "real code. It also allocates a second string of the same length, "
         "because Python strings are immutable and there is no in-place option. "
         "An interviewer asking for O(1) space is asking you to leave strings "
         "behind and work on a character array.</p>"),
        ("The two-pointer version",
         "<p>Put one pointer at each end. Swap the characters they name, move "
         "both inwards, stop when they meet. That is n/2 swaps and two integers "
         "of extra memory, regardless of length.</p>"
         "<p>The loop condition is <code>while lo &lt; hi</code>, strictly less "
         "than. With <code>&lt;=</code> an odd-length string swaps its middle "
         "character with itself &mdash; harmless but pointless, and the "
         "condition is the part interviewers check.</p>"),
        ("The variations that follow",
         "<p>\"Reverse the words but not the characters\" &mdash; "
         "<code>\" \".join(s.split()[::-1])</code>, or reverse the whole thing "
         "and then reverse each word in place, which is the O(1)-space trick.</p>"
         "<p>\"Reverse only the vowels\" &mdash; the same two pointers, each "
         "skipping forward until it lands on a vowel. \"Reverse in groups of "
         "k\" &mdash; the same swap loop applied to each block.</p>"),
    ],
    code={
        "file": "reverse.py",
        "intro": "Three reversals of the same text &mdash; the slice, the "
                 "two-pointer swap, and the word-level variant &mdash; with the "
                 "extra memory each one uses printed beside it.",
        "code": '''# Reversing a string: the idiom, and the version an interviewer wants.

def reverse_slice(s):
    return s[::-1]                       # O(n) time, O(n) extra memory


def reverse_in_place(chars):
    """Two pointers, swapping inwards. O(1) extra memory."""
    lo, hi = 0, len(chars) - 1
    swaps = 0
    while lo < hi:                       # strictly <: the middle needs no swap
        chars[lo], chars[hi] = chars[hi], chars[lo]
        swaps += 1
        lo, hi = lo + 1, hi - 1
    return swaps


s = "stressed"
print("original      :", s)
print("s[::-1]       :", reverse_slice(s))

chars = list(s)                          # strings cannot be modified in place
swaps = reverse_in_place(chars)
print("two pointers  :", "".join(chars), f"({swaps} swaps for {len(s)} chars)")

# Odd length: the middle character stays put, which is correct.
odd = list("abcde")
reverse_in_place(odd)
print("odd length    :", "".join(odd))

# --- the follow-ups ----------------------------------------------------
sentence = "the quick brown fox"
print()
print("words reversed:", " ".join(sentence.split()[::-1]))

vowels = "aeiouAEIOU"
def reverse_vowels(s):
    chars = list(s)
    lo, hi = 0, len(chars) - 1
    while lo < hi:
        while lo < hi and chars[lo] not in vowels:
            lo += 1
        while lo < hi and chars[hi] not in vowels:
            hi -= 1
        chars[lo], chars[hi] = chars[hi], chars[lo]
        lo, hi = lo + 1, hi - 1
    return "".join(chars)

print("vowels only   :", reverse_vowels("programming"))
print("(consonants stay where they are - only a, i, o moved)")
''',
        "walk": [
            ("while lo < hi:",
             "Strictly less than. With <code>&lt;=</code> an odd-length string "
             "swaps its middle character with itself &mdash; harmless, and the "
             "kind of detail the question exists to check."),
            ("chars[lo], chars[hi] = chars[hi], chars[lo]",
             "Python evaluates the right side first, so this is a real swap. In "
             "most languages it needs a temporary, and forgetting it overwrites "
             "one of the two values."),
            ("chars = list(s)",
             "The concession immutability forces. There is no in-place reversal "
             "of a <code>str</code>; \"in place\" means in a character array."),
            ("while lo < hi and chars[lo] not in vowels:",
             "The inner skips need the <code>lo &lt; hi</code> guard too, or a "
             "string with no vowels runs a pointer off the end. Nested pointer "
             "loops are where index errors hide."),
        ],
        "try": [
            "Change the loop to <code>while lo &lt;= hi</code> and print the swap "
            "count for an odd-length string. One wasted swap, same output.",
            "Reverse the words with O(1) extra space: reverse the whole array, "
            "then reverse each word in place. That is the real interview "
            "follow-up.",
        ],
    },
    check=[
        {"q": "Why can't you reverse a Python string in place?",
         "options": ["It is too slow", "Strings are immutable - there is no "
                     "in-place operation at all",
                     "Slicing is required", "You can, with s.reverse()"],
         "answer": 1,
         "why": "In-place means working on a character list. str has no reverse() "
                "method for exactly this reason."},
        {"q": "The two-pointer reversal loop uses `while lo < hi` rather than "
              "`<=` because:",
         "options": ["It is faster", "With <= an odd-length string swaps its "
                     "middle character with itself",
                     "<= causes an index error", "The pointers never meet"],
         "answer": 1,
         "why": "Harmless but pointless. The condition is precisely what the "
                "question is testing."},
        {"q": "How many swaps does the in-place reversal make for n characters?",
         "options": ["n", "n/2", "n log n", "n - 1"],
         "answer": 1,
         "why": "Each swap places two characters, and the pointers meet in the "
                "middle. Memory is O(1) regardless of n."},
    ],
)


def _palindrome_frames():
    text = "A man, a plan, a canal: Panama"
    out = []
    lo, hi = 0, len(text) - 1
    steps = 0
    while lo < hi and steps < 7:
        while lo < hi and not text[lo].isalnum():
            lo += 1
        while lo < hi and not text[hi].isalnum():
            hi -= 1
        same = text[lo].lower() == text[hi].lower()
        marks = {i: "dim" for i in range(len(text))}
        marks[lo] = "hit" if same else "bad"
        marks[hi] = "hit" if same else "bad"
        out.append(frame(marked(list(text), marks, {lo: "lo", hi: "hi"},
                                kind="text", label="text"),
                         "%r vs %r - %s. Punctuation and case were skipped, not "
                         "removed." % (text[lo], text[hi],
                                       "match" if same else "MISMATCH, stop"),
                         {"lo": lo, "hi": hi, "compared": steps + 1}))
        if not same:
            break
        lo, hi = lo + 1, hi - 1
        steps += 1
    out.append(frame(marked(list(text), {i: "done" for i in range(len(text))},
                            kind="text", label="text"),
                     "The pointers meet with every pair matching, so it is a "
                     "palindrome - checked without building a cleaned copy.",
                     {"lo": lo, "hi": hi, "compared": steps}))
    return viz(out)


_q(
    slug="valid-palindrome",
    kind="coding",
    level="Easy",
    title="Check whether a string is a palindrome",
    asked="Check whether a string is a palindrome, ignoring punctuation and case.",
    desc="Two-pointer palindrome checking in O(1) space, why the s == s[::-1] "
         "one-liner costs O(n) memory, and the guards the skip loops need.",
    lead="<code>s == s[::-1]</code> is the one-liner and allocates a reversed "
         "copy. The O(1)-space answer walks <strong>two pointers</strong> "
         "inwards, each skipping non-alphanumeric characters, comparing "
         "case-folded. It also short-circuits on the first mismatch, which the "
         "one-liner cannot.",
    say="\"Two pointers from both ends, skip anything that isn't alphanumeric, "
        "compare lowercased. O(n) time, O(1) space, and it bails on the first "
        "mismatch.\"",
    notice=[
        "Commas and spaces are <em>skipped</em>, not stripped into a new string.",
        "Both skip loops need the <code>lo &lt; hi</code> guard.",
        "A mismatch stops immediately &mdash; no need to check the rest.",
    ],
    viz=_palindrome_frames(),
    sections=[
        ("The one-liner and its cost",
         "<p><code>s == s[::-1]</code> is correct and reads well. It builds a "
         "full reversed copy first, so it is O(n) extra memory, and it always "
         "compares the entire string even when the first and last characters "
         "already disagree.</p>"
         "<p>Cleaning first &mdash; <code>clean = \"\".join(c.lower() for c in s "
         "if c.isalnum())</code> then comparing &mdash; is readable and costs a "
         "second full copy on top.</p>"),
        ("The two-pointer version",
         "<p>One pointer at each end. Advance each past anything that is not "
         "alphanumeric, compare the two characters case-folded, then step both "
         "inwards. No copy is made and the first mismatch ends it.</p>"
         "<p>The subtlety is the guards: both inner skip loops need "
         "<code>lo &lt; hi</code> in their condition, or a string of pure "
         "punctuation runs a pointer off the end. That is the bug this question "
         "is really probing.</p>"),
        ("The follow-up",
         "<p>\"Now allow one character to be deleted.\" On a mismatch, try "
         "skipping the left character or the right one and check whether either "
         "remaining span is a plain palindrome. That is still O(n): you only get "
         "one chance to branch, so the two checks do not nest.</p>"),
    ],
    code={
        "file": "palindrome.py",
        "intro": "Both approaches on the same inputs, with the comparison counts "
                 "printed &mdash; which is where the two-pointer version's "
                 "short-circuit shows up. The last section is the delete-one "
                 "follow-up.",
        "code": '''# Palindrome check, ignoring punctuation and case.

def is_palindrome_slice(s):
    clean = "".join(c.lower() for c in s if c.isalnum())   # a full copy
    return clean == clean[::-1]                            # and another


def is_palindrome_two_pointers(s):
    lo, hi = 0, len(s) - 1
    compared = 0
    while lo < hi:
        while lo < hi and not s[lo].isalnum():     # the lo < hi guard matters
            lo += 1
        while lo < hi and not s[hi].isalnum():
            hi -= 1
        compared += 1
        if s[lo].lower() != s[hi].lower():
            return False, compared                 # stop at the first mismatch
        lo, hi = lo + 1, hi - 1
    return True, compared


tests = ["A man, a plan, a canal: Panama", "race a car", "", ".,!?", "ab@ba"]
for t in tests:
    slice_answer = is_palindrome_slice(t)
    ok, compared = is_palindrome_two_pointers(t)
    agree = "" if ok == slice_answer else "   <-- DISAGREE"
    print(f"{t!r:>32}: {str(ok):>5}  ({compared} comparisons){agree}")

print()
print("'race a car' fails on the first pair - the slice version still")
print("builds and compares the whole cleaned string.")

# --- the follow-up: allow one deletion ---------------------------------
def valid_after_one_deletion(s):
    def plain(lo, hi):
        while lo < hi:
            if s[lo] != s[hi]:
                return False
            lo, hi = lo + 1, hi - 1
        return True

    lo, hi = 0, len(s) - 1
    while lo < hi:
        if s[lo] != s[hi]:
            # One chance: drop the left character or the right one.
            return plain(lo + 1, hi) or plain(lo, hi - 1)
        lo, hi = lo + 1, hi - 1
    return True

print()
for t in ("abca", "abc", "deeee"):
    print(f"  {t!r:>8} palindrome after one deletion: {valid_after_one_deletion(t)}")
''',
        "walk": [
            ("while lo < hi and not s[lo].isalnum():",
             "The guard is the whole trick. Without <code>lo &lt; hi</code> in "
             "the inner condition, a string of pure punctuation walks a pointer "
             "straight off the end."),
            ("s[lo].lower() != s[hi].lower()",
             "Case folding happens at the comparison, so no cleaned copy is ever "
             "built. <code>casefold()</code> is the more correct choice for "
             "non-English text."),
            ("return False, compared",
             "The short-circuit. <code>\"race a car\"</code> is settled by the "
             "first pair; the slice version compares everything regardless."),
            ("plain(lo + 1, hi) or plain(lo, hi - 1)",
             "The delete-one follow-up. Only one branch is ever taken, so the "
             "two checks do not nest and the whole thing stays O(n)."),
        ],
        "try": [
            "Feed it <code>\".,!?\"</code>. Both return True and the two-pointer "
            "version does it without allocating &mdash; check the guards are why.",
            "Drop <code>lo &lt; hi</code> from one inner loop and run the "
            "punctuation-only case. The <code>IndexError</code> is what the "
            "guard prevents.",
        ],
    },
    check=[
        {"q": "The main advantage of the two-pointer palindrome check over "
              "s == s[::-1] is:",
         "options": ["It is shorter", "O(1) extra space, and it stops at the "
                     "first mismatch",
                     "It handles Unicode", "It is the only correct one"],
         "answer": 1,
         "why": "The slice builds a full reversed copy and always compares "
                "everything. Both are O(n) time in the worst case."},
        {"q": "Why do the inner skip loops need `lo < hi` in their condition?",
         "options": ["To count comparisons", "Otherwise a string of pure "
                     "punctuation runs a pointer off the end",
                     "To handle uppercase", "To make it stable"],
         "answer": 1,
         "why": "Nothing else stops the skip. It is the bug the question is "
                "really probing."},
        {"q": "In the 'allow one deletion' variant, why is it still O(n)?",
         "options": ["The string is short", "The branch happens at most once, so "
                     "the two sub-checks never nest",
                     "It uses a set", "It is O(n²)"],
         "answer": 1,
         "why": "You get exactly one chance to delete, so it is one linear scan "
                "plus at most two more - not a recursive explosion."},
    ],
)


def _anagram_frames():
    a, b = "listen", "silent"
    out = []
    counts = {}
    for i, ch in enumerate(a):
        counts[ch] = counts.get(ch, 0) + 1
        marks = {j: ("hit" if j == i else "done" if j < i else "dim")
                 for j in range(len(a))}
        out.append(frame([marked(list(a), marks, kind="text", label="'listen' (add)"),
                          pairs(sorted(counts.items()), {ch: "hit"}, label="counts")],
                         "Counting %r up to %d." % (ch, counts[ch]),
                         {"balance": sum(counts.values())}))
    for i, ch in enumerate(b):
        counts[ch] -= 1
        if counts[ch] == 0:
            del counts[ch]
        marks = {j: ("bad" if j == i else "done" if j < i else "dim")
                 for j in range(len(b))}
        out.append(frame([marked(list(b), marks, kind="text", label="'silent' (subtract)"),
                          pairs(sorted(counts.items()) or [("(empty)", "0")],
                                {ch: "bad"}, label="counts")],
                         "Subtracting %r. Anything left at the end means the two "
                         "differ." % ch,
                         {"balance": sum(counts.values())}))
    out.append(frame(pairs([("counts", "empty"), ("anagram", "True")],
                           {"anagram": "hit"}, label="verdict"),
                     "Every count cancelled, so the two strings use exactly the "
                     "same letters. One pass each, O(n).",
                     {"balance": 0}))
    return viz(out)


_q(
    slug="valid-anagram",
    kind="coding",
    level="Easy",
    title="Are two strings anagrams?",
    asked="Check whether two strings are anagrams of each other.",
    desc="Anagram checking with a counter in O(n) versus sorting in O(n log n), "
         "and the follow-ups about Unicode and memory.",
    lead="Sorting both and comparing is O(n&nbsp;log&nbsp;n) and fits on one "
         "line. <strong>Counting</strong> is O(n): add up the letters of the "
         "first, subtract the letters of the second, and if every count reaches "
         "zero they are anagrams. Check lengths first &mdash; it is a free "
         "rejection.",
    say="\"Sorted comparison is the one-liner, O(n log n). Better is a Counter: "
        "add one string, subtract the other, and everything should cancel. O(n) "
        "time, O(k) space in the alphabet size.\"",
    notice=[
        "The counts rise on the first string and fall on the second.",
        "Reaching zero and being <em>deleted</em> is what makes the final check a "
        "simple emptiness test.",
        "A length mismatch rejects before any counting starts.",
    ],
    viz=_anagram_frames(),
    sections=[
        ("Sorting versus counting",
         "<p><code>sorted(a) == sorted(b)</code> is correct, obvious and "
         "O(n&nbsp;log&nbsp;n). It is a perfectly good answer to give first, and "
         "then improve.</p>"
         "<p>Counting is O(n). Build a frequency map of the first string, walk "
         "the second decrementing, and check nothing is left over. With a "
         "<code>Counter</code> that is two lines; done by hand it is a loop and "
         "a dictionary.</p>"
         "<p>Both need the length check first. Different lengths cannot be "
         "anagrams, and rejecting there avoids the work entirely.</p>"),
        ("Space, and the alphabet",
         "<p>The counter holds one entry per distinct character, so space is "
         "O(k) in the alphabet rather than O(n) in the input. For lowercase "
         "ASCII that is at most 26 entries, which is why interviewers sometimes "
         "ask for a fixed 26-element array instead &mdash; the same algorithm "
         "with the dictionary replaced by an offset from <code>ord('a')</code>.</p>"
         "<p>Say out loud that this assumes an alphabet. For arbitrary Unicode "
         "the fixed array is wrong and the dictionary is the right structure.</p>"),
        ("The follow-up that catches people",
         "<p>\"Group all the anagrams in a list of words.\" The instinct is to "
         "compare every pair, which is O(n&sup2;) comparisons of O(m) strings. "
         "The answer is to give every word a <em>canonical key</em> &mdash; its "
         "sorted letters, or its count tuple &mdash; and group by that key in "
         "one pass. That is the next question on this track.</p>"),
    ],
    code={
        "file": "anagram.py",
        "intro": "Three implementations timed against each other on real words, "
                 "so the O(n) against O(n&nbsp;log&nbsp;n) claim is measured "
                 "rather than asserted &mdash; and a Unicode case that breaks the "
                 "fixed-array version.",
        "code": '''# Anagram check: sorting, counting, and a fixed-size array.
from collections import Counter
import time

def by_sorting(a, b):
    return sorted(a) == sorted(b)                # O(n log n)


def by_counting(a, b):
    if len(a) != len(b):
        return False                             # free rejection
    counts = {}
    for ch in a:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in b:
        if ch not in counts:
            return False
        counts[ch] -= 1
        if counts[ch] == 0:
            del counts[ch]                       # so "empty" means "cancelled"
    return not counts


def by_array(a, b):
    """Only correct for lowercase a-z - state that assumption out loud."""
    if len(a) != len(b):
        return False
    seen = [0] * 26
    for ch in a:
        seen[ord(ch) - ord("a")] += 1
    for ch in b:
        seen[ord(ch) - ord("a")] -= 1
    return not any(seen)


pairs_to_test = [("listen", "silent"), ("rat", "car"), ("aab", "abb"), ("", "")]
for a, b in pairs_to_test:
    print(f"{a!r:>9} vs {b!r:<9} sorting={by_sorting(a, b)!s:>5} "
          f"counting={by_counting(a, b)!s:>5} array={by_array(a, b)}")

print()
print("Counter does it in one line:", Counter("listen") == Counter("silent"))

# --- the cost, measured ------------------------------------------------
a = "abcdefghij" * 4000
b = "jihgfedcba" * 4000
print()
for name, fn in (("sorting", by_sorting), ("counting", by_counting)):
    start = time.time()
    fn(a, b)
    print(f"  {name:>8} on {len(a):,} chars: {time.time() - start:.4f}s")

# The fixed array assumes an alphabet. This is where that assumption dies.
print()
print("by_counting on 'café'/'éfac':", by_counting("café", "éfac"))
try:
    print("by_array   on 'café'/'éfac':", by_array("café", "éfac"))
except IndexError as e:
    print("by_array   on 'café'/'éfac': IndexError -", e)
''',
        "walk": [
            ("if len(a) != len(b): return False",
             "Free, and it removes a whole class of input before any counting. "
             "Interviewers notice when it is missing."),
            ("del counts[ch]",
             "Deleting on zero is what lets the final test be "
             "<code>not counts</code>. Leaving zeros in means comparing against "
             "a dictionary of zeros instead, which works and reads worse."),
            ("if ch not in counts: return False",
             "Catches a character that is in <code>b</code> and not in "
             "<code>a</code> without letting the count go negative. Skipping it "
             "gives wrong answers on inputs of equal length."),
            ("seen = [0] * 26",
             "The fixed-array version, and its assumption. Fast and small for "
             "lowercase ASCII, and an <code>IndexError</code> the moment an "
             "accent arrives &mdash; which the last line demonstrates."),
        ],
        "try": [
            "Compare <code>Counter(a) == Counter(b)</code> in the timing loop. "
            "It is the C implementation of the same idea and wins comfortably.",
            "Make the array version case-insensitive with "
            "<code>a.lower()</code>. It fixes one assumption and leaves the "
            "alphabet one in place.",
        ],
    },
    check=[
        {"q": "Counting beats sorting for anagram checks because it is:",
         "options": ["O(1) instead of O(n)", "O(n) instead of O(n log n)",
                     "More readable", "Stable"],
         "answer": 1,
         "why": "One pass over each string versus a comparison sort of both. "
                "Space goes from O(1) to O(k) in the alphabet size."},
        {"q": "Why delete a key when its count reaches zero?",
         "options": ["To save memory", "So the final check is simply 'is the "
                     "dictionary empty?'",
                     "To avoid negatives", "Counter requires it"],
         "answer": 1,
         "why": "Leaving zeros in means comparing against a dict of zeros. "
                "Deleting makes the terminal condition trivial."},
        {"q": "A fixed 26-element array version breaks on:",
         "options": ["Long strings", "Any character outside a-z, such as an "
                     "accented letter",
                     "Empty strings", "Repeated letters"],
         "answer": 1,
         "why": "ord(ch) - ord('a') indexes out of range. Say the alphabet "
                "assumption out loud when you offer that optimisation."},
    ],
)


def _group_frames():
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    out = []
    groups = {}
    for i, w in enumerate(words):
        key = "".join(sorted(w))
        groups.setdefault(key, []).append(w)
        marks = {j: ("hit" if j == i else "done" if j < i else "dim")
                 for j in range(len(words))}
        out.append(frame([marked(words, marks, kind="cells", label="words"),
                          pairs([(k, ", ".join(v)) for k, v in sorted(groups.items())],
                                {key: "hit"}, label="key -> group")],
                         "%r sorts to %r, so it joins that bucket. One lookup, "
                         "no comparison with any other word." % (w, key),
                         {"words": i + 1, "groups": len(groups)}))
    out.append(frame(pairs([(k, ", ".join(v)) for k, v in sorted(groups.items())],
                           {k: "done" for k in groups}, label="final groups"),
                     "Six words, one pass, three groups. Comparing every pair "
                     "would have been fifteen comparisons instead of six lookups.",
                     {"words": len(words), "groups": len(groups)}))
    return viz(out)


_q(
    slug="group-anagrams",
    kind="coding",
    level="Medium",
    title="Group anagrams together",
    asked="Given a list of words, group the anagrams together.",
    desc="Grouping anagrams by canonical key in O(n·m log m) instead of comparing "
         "every pair, and why the count tuple beats the sorted string for long "
         "words.",
    lead="Do not compare words with each other. Give each word a "
         "<strong>canonical key</strong> &mdash; its letters sorted, or a tuple "
         "of letter counts &mdash; and use a dictionary to collect words sharing "
         "a key. One pass, no pairwise comparison, and the whole O(n&sup2;) "
         "instinct disappears.",
    say="\"Map each word to a canonical form - sorted letters - and group by "
        "that in a dict. O(n·m log m) for n words of length m, instead of n² "
        "pairwise comparisons.\"",
    notice=[
        "Each word is looked at <em>once</em> and never compared with another word.",
        "The key is the group's identity &mdash; that is the whole idea.",
        "Six words: six lookups here, fifteen comparisons the naive way.",
    ],
    viz=_group_frames(),
    sections=[
        ("The instinct, and why it is wrong",
         "<p>The obvious approach compares every word with every other word to "
         "see whether they are anagrams. That is n(n&minus;1)/2 comparisons, "
         "each costing O(m&nbsp;log&nbsp;m) or O(m), so the whole thing is "
         "O(n&sup2;&middot;m).</p>"
         "<p>The realisation that fixes it: being anagrams is an "
         "<em>equivalence relation</em>, so instead of testing pairs you can "
         "give every word a label that all its anagrams share, and group by "
         "label. Dictionaries group by label in O(1) each.</p>"),
        ("Choosing the key",
         "<p><strong>Sorted letters.</strong> <code>\"\".join(sorted(word))</code>. "
         "Simple, obviously correct, O(m&nbsp;log&nbsp;m) per word. This is the "
         "answer to give.</p>"
         "<p><strong>A count tuple.</strong> A 26-element tuple of letter counts, "
         "built in O(m). Faster for long words, and the improvement to mention "
         "when asked. It must be a <code>tuple</code>, not a list &mdash; keys "
         "have to be hashable.</p>"
         "<p>Total cost is O(n&middot;m&nbsp;log&nbsp;m) with sorting, or "
         "O(n&middot;m) with counts. Either way the n&sup2; is gone.</p>"),
        ("The pattern behind it",
         "<p>\"Canonicalise, then group\" solves a whole family of questions: "
         "find duplicate files by hashing contents, group points by slope, "
         "detect isomorphic strings by normalising the pattern. Whenever a "
         "question asks you to find things that are equivalent under some "
         "transformation, look for the canonical form before you look for a "
         "clever comparison.</p>"),
    ],
    code={
        "file": "group_anagrams.py",
        "intro": "Both keys, plus the pairwise version with its comparisons "
                 "counted, so the difference between six lookups and fifteen "
                 "comparisons is a number on the screen rather than a claim.",
        "code": '''# Group anagrams: canonicalise, then group. Never compare pairs.
from collections import defaultdict

words = ["eat", "tea", "tan", "ate", "nat", "bat"]

# --- key 1: sorted letters. O(m log m) per word ------------------------
def group_by_sorted(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return dict(groups)


# --- key 2: a count tuple. O(m) per word, and hashable -----------------
def group_by_counts(words):
    groups = defaultdict(list)
    for w in words:
        counts = [0] * 26
        for ch in w:
            counts[ord(ch) - ord("a")] += 1
        groups[tuple(counts)].append(w)      # tuple, not list: keys must hash
    return dict(groups)


# --- the naive version, with its comparisons counted -------------------
def group_pairwise(words):
    comparisons = 0
    groups = []
    for w in words:
        placed = False
        for g in groups:
            comparisons += 1
            if sorted(g[0]) == sorted(w):
                g.append(w)
                placed = True
                break
        if not placed:
            groups.append([w])
    return groups, comparisons


print("by sorted key:")
for key, group in group_by_sorted(words).items():
    print(f"  {key:>4} -> {group}")

print()
print("by count key :", list(group_by_counts(words).values()))

groups, comparisons = group_pairwise(words)
print()
print(f"pairwise     : {len(groups)} groups after {comparisons} comparisons")
print(f"keyed        : {len(words)} dictionary lookups, no comparisons at all")

# A list cannot be a key. This is the mistake the tuple exists to avoid.
try:
    {[0] * 26: "x"}
except TypeError as e:
    print()
    print("list as a key ->", e)
''',
        "walk": [
            ("groups[\"\".join(sorted(w))].append(w)",
             "The whole algorithm. Sorting the letters produces a label every "
             "anagram of that word shares, and the dictionary does the grouping "
             "in O(1)."),
            ("tuple(counts)",
             "Must be a tuple. A list is mutable and therefore unhashable, so it "
             "cannot be a dictionary key &mdash; the last lines of the program "
             "show the exact error."),
            ("defaultdict(list)",
             "Removes the \"is this key here yet?\" branch. "
             "<code>setdefault</code> does the same job in one line if you would "
             "rather not import anything."),
            ("group_pairwise",
             "Kept only for its comparison count. It is O(n&sup2;&middot;m) and "
             "the number it prints is the argument against writing it."),
        ],
        "try": [
            "Add twenty more words and compare the two counts again. Lookups "
            "grow linearly, comparisons quadratically.",
            "Feed it a word with an accent. The count-tuple version raises &mdash; "
            "that is the alphabet assumption, and it is worth saying out loud "
            "before you offer the optimisation.",
        ],
    },
    check=[
        {"q": "The key idea in grouping anagrams efficiently is:",
         "options": ["Sorting the whole list first",
                     "Giving each word a canonical key that all its anagrams share",
                     "Comparing each word to the first", "Using a set"],
         "answer": 1,
         "why": "Being anagrams is an equivalence relation, so you group by label "
                "rather than testing pairs. That removes the n² entirely."},
        {"q": "Why must the count key be a tuple rather than a list?",
         "options": ["Tuples are faster", "Lists are unhashable, so they cannot "
                     "be dictionary keys",
                     "Tuples are shorter", "It does not matter"],
         "answer": 1,
         "why": "A key's hash must stay valid for the life of the entry, so only "
                "immutable types are allowed."},
        {"q": "For n words of length m, grouping by sorted key costs:",
         "options": ["O(n²·m)", "O(n·m log m)", "O(n log n)", "O(m²)"],
         "answer": 1,
         "why": "One sort per word, then O(1) to place it. The count-tuple key "
                "drops it to O(n·m)."},
    ],
)


_q(
    slug="longest-substring-without-repeating-characters",
    kind="coding",
    level="Medium",
    title="Longest substring without repeating characters",
    asked="Find the length of the longest substring with no repeated character.",
    desc="The variable-size sliding window, why the left edge jumps rather than "
         "creeps, and the guard that stops a stale index shrinking the window.",
    lead="A <strong>sliding window</strong> with a dictionary of last-seen "
         "positions. Extend the right edge one character at a time; when a "
         "character repeats <em>inside</em> the current window, jump the left "
         "edge past its previous occurrence. Every character is visited once, so "
         "it is O(n).",
    say="\"Sliding window with a last-seen map. Right edge always advances; on a "
        "repeat inside the window the left edge jumps past the old occurrence. "
        "O(n) time, O(k) space in the alphabet.\"",
    notice=[
        "The right edge never goes backwards &mdash; that is what keeps it linear.",
        "On a repeat, the left edge <em>jumps</em> rather than creeping.",
        "A repeat that already fell off the left is ignored &mdash; watch "
        "<code>abba</code>.",
    ],
    viz=viz(growing_window("abcabcbb")),
    sections=[
        ("Why brute force is quadratic",
         "<p>Checking every substring is O(n&sup2;) substrings, each needing a "
         "uniqueness test &mdash; O(n&sup3;) naively, O(n&sup2;) with a set per "
         "start. The waste is that each restart throws away everything the "
         "previous one learned.</p>"
         "<p>The window keeps it. When the right edge advances, the answer for "
         "the new window is derived from the old one instead of recomputed.</p>"),
        ("The jump, and the guard",
         "<p>Store each character's <em>last index</em>. When the character at "
         "the right edge has been seen, the left edge moves to "
         "<code>seen[ch] + 1</code> &mdash; one past the previous occurrence, in "
         "a single step.</p>"
         "<p>The guard is the subtle part: only jump if <code>seen[ch] &gt;= "
         "start</code>. Without it, a character last seen <em>before</em> the "
         "current window drags the left edge backwards, shrinking the window for "
         "no reason. <code>\"abba\"</code> is the shortest input that exposes "
         "it: at the final <code>a</code>, the earlier <code>a</code> is already "
         "outside the window.</p>"),
        ("Cost, and what to say about space",
         "<p>Time is O(n): the right edge advances n times and the left edge only "
         "ever moves forwards, so both pointers together make at most 2n moves. "
         "Space is O(k) in the size of the alphabet, not O(n) &mdash; the map "
         "holds one entry per distinct character.</p>"
         "<p>Interviewers like the space answer because most candidates say "
         "O(n).</p>"),
    ],
    code={
        "file": "longest_unique.py",
        "intro": "The window printed at every step, then the same input run "
                 "against brute force so the operation counts sit side by side, "
                 "and finally the <code>abba</code> case with the guard removed.",
        "code": '''# Longest substring with no repeated character: a sliding window.

def longest_unique(text, show=True):
    seen = {}                        # character -> last index it appeared at
    start = best = 0
    best_text = ""
    steps = 0
    for i, ch in enumerate(text):
        steps += 1
        if ch in seen and seen[ch] >= start:      # the guard: inside the window?
            start = seen[ch] + 1                  # jump, do not creep
        seen[ch] = i
        if i - start + 1 > best:
            best = i - start + 1
            best_text = text[start:i + 1]
        if show:
            print(f"  i={i} {ch!r} window={text[start:i+1]!r:>10} best={best}")
    return best, best_text, steps


def brute_force(text):
    best, best_text, steps = 0, "", 0
    for i in range(len(text)):
        seen = set()
        for j in range(i, len(text)):
            steps += 1
            if text[j] in seen:
                break
            seen.add(text[j])
            if j - i + 1 > best:
                best, best_text = j - i + 1, text[i:j + 1]
    return best, best_text, steps


text = "abcabcbb"
print(f"sliding window on {text!r}:")
best, best_text, steps = longest_unique(text)
print(f"  -> {best} ({best_text!r}) in {steps} steps")

b2, t2, s2 = brute_force(text)
print(f"brute force        -> {b2} ({t2!r}) in {s2} steps")

# --- the guard, and what happens without it ----------------------------
def without_guard(text):
    seen, start, best = {}, 0, 0
    for i, ch in enumerate(text):
        if ch in seen:                # no "is it still in the window?" check
            start = seen[ch] + 1
        seen[ch] = i
        best = max(best, i - start + 1)
    return best

print()
for t in ("abba", "abcabcbb", "tmmzuxt"):
    good = longest_unique(t, show=False)[0]
    bad = without_guard(t)
    flag = "   <-- WRONG without the guard" if good != bad else ""
    print(f"  {t!r:>10}: correct={good}  no guard={bad}{flag}")
''',
        "walk": [
            ("if ch in seen and seen[ch] >= start:",
             "The guard. A repeat only matters while it is inside the window; an "
             "older occurrence has already fallen off the left edge and must be "
             "ignored."),
            ("start = seen[ch] + 1",
             "One jump instead of walking the left edge forward one character at "
             "a time. Both are correct; this one keeps the whole scan clearly "
             "linear."),
            ("seen[ch] = i",
             "Storing the index rather than a count is what makes the jump "
             "possible. A count-based window works too and needs the left edge "
             "to walk."),
            ("i - start + 1",
             "The window length. Off-by-one here is the most common way to get "
             "an answer that is right on most inputs and wrong on the edges."),
        ],
        "try": [
            "Run <code>\"abba\"</code> through both. The guard is the entire "
            "difference between 2 and 3.",
            "Return the substring rather than the length by tracking "
            "<code>start</code> at the moment <code>best</code> improves &mdash; "
            "the usual follow-up.",
        ],
    },
    check=[
        {"q": "Why is `seen[ch] >= start` needed as well as `ch in seen`?",
         "options": ["To handle the first character",
                     "A character last seen before the window must not drag the "
                     "left edge backwards",
                     "To count repeats", "To keep it O(n)"],
         "answer": 1,
         "why": "Only repeats inside the current window matter. 'abba' is the "
                "shortest input that gets the wrong answer without it."},
        {"q": "The time complexity is O(n) because:",
         "options": ["The string is short", "Both pointers only ever move "
                     "forwards, for at most 2n moves total",
                     "The dictionary is O(1)", "It uses recursion"],
         "answer": 1,
         "why": "The right edge advances n times and the left edge never "
                "retreats, so the total work is linear despite the nested feel."},
        {"q": "The space complexity is:",
         "options": ["O(n)", "O(k), one entry per distinct character", "O(1)",
                     "O(n²)"],
         "answer": 1,
         "why": "The map holds distinct characters, so it is bounded by the "
                "alphabet - the answer most candidates get wrong."},
    ],
)


def _first_unique_frames():
    text = "swiss"
    out = []
    counts = {}
    for i, ch in enumerate(text):
        counts[ch] = counts.get(ch, 0) + 1
        marks = {j: ("hit" if j == i else "done" if j < i else "dim")
                 for j in range(len(text))}
        out.append(frame([marked(list(text), marks, kind="text", label="pass 1: count"),
                          pairs(sorted(counts.items()), {ch: "hit"}, label="counts")],
                         "%r seen %d time(s)." % (ch, counts[ch]),
                         {"pass": 1, "at": i}))
    for i, ch in enumerate(text):
        unique = counts[ch] == 1
        marks = {j: ("hit" if j == i and unique else "bad" if j == i else "dim")
                 for j in range(len(text))}
        out.append(frame([marked(list(text), marks, kind="text", label="pass 2: find"),
                          pairs(sorted(counts.items()), {ch: "hit" if unique else "bad"},
                                label="counts")],
                         "%r has count %d - %s." % (ch, counts[ch],
                                                    "the first unique one, index %d" % i
                                                    if unique else "skip"),
                         {"pass": 2, "at": i}))
        if unique:
            break
    return viz(out)


_q(
    slug="first-non-repeating-character",
    kind="coding",
    level="Easy",
    title="First non-repeating character",
    asked="Find the first character in a string that does not repeat.",
    desc="Two passes and a counter solve it in O(n); why one pass is not enough, "
         "and how insertion order removes the need to track positions.",
    lead="<strong>Two passes.</strong> Count every character, then walk the "
         "string again and return the first with a count of one. One pass cannot "
         "do it &mdash; you cannot know a character is unique until you have seen "
         "the whole string. O(n) time, O(k) space.",
    say="\"Count in one pass, then scan again for the first count of one. Two "
        "passes is O(n) - and you can't do it in one, because uniqueness isn't "
        "decidable until the end.\"",
    notice=[
        "Pass one fills the counter; nothing is decided during it.",
        "Pass two returns at the first count of 1 &mdash; order comes from the "
        "<em>string</em>, not the dictionary.",
        "<code>swiss</code>: <code>w</code> wins, because <code>s</code> repeats.",
    ],
    viz=_first_unique_frames(),
    sections=[
        ("Why one pass is impossible",
         "<p>Reading left to right, the first character might be unique or might "
         "repeat at the very end. Nothing can be returned until the whole string "
         "has been read, so a single pass that emits an answer as it goes is "
         "wrong by construction.</p>"
         "<p>What a single pass <em>can</em> do is record enough to answer at the "
         "end &mdash; which is what the counter is. The second pass is not extra "
         "work in the complexity sense: two linear passes is still O(n).</p>"),
        ("Why the second pass walks the string",
         "<p>The answer must be the <em>first</em> such character, and \"first\" "
         "is a property of the string, not of the counter. Walking the string "
         "gets the order for free.</p>"
         "<p>Since Python 3.7 dictionaries preserve insertion order, so walking "
         "<code>counts.items()</code> also works and touches only distinct "
         "characters. Say which guarantee you are relying on &mdash; it is a "
         "language guarantee since 3.7, and was an implementation detail in "
         "3.6.</p>"),
        ("The stream variant",
         "<p>The real follow-up: \"characters arrive one at a time and you must "
         "answer at any moment.\" Keep a counter <em>and</em> a queue of "
         "candidates. On each arrival, push it to the queue, then pop from the "
         "front while the front has a count above one. The head of the queue is "
         "always the current answer, in O(1) amortised.</p>"),
    ],
    code={
        "file": "first_unique.py",
        "intro": "The two-pass version, then the same answer read straight out "
                 "of the ordered dictionary, then the streaming variant that "
                 "answers after every single character.",
        "code": '''# First non-repeating character: count, then find.
from collections import Counter, deque

def first_unique(s):
    counts = Counter(s)                      # pass 1: nothing is decided here
    for i, ch in enumerate(s):               # pass 2: order comes from the string
        if counts[ch] == 1:
            return i, ch
    return -1, None


def first_unique_via_dict(s):
    """Same answer from the dictionary - insertion order is guaranteed >= 3.7."""
    counts = Counter(s)
    for ch, n in counts.items():
        if n == 1:
            return s.index(ch), ch
    return -1, None


for s in ("swiss", "aabbcc", "leetcode", "z"):
    i, ch = first_unique(s)
    j, ch2 = first_unique_via_dict(s)
    agree = "" if (i, ch) == (j, ch2) else "   <-- DISAGREE"
    print(f"{s!r:>10}: index {i:>2} {ch!r}{agree}")

# --- the follow-up: a stream, answerable at any moment -----------------
class Stream:
    def __init__(self):
        self.counts = Counter()
        self.candidates = deque()

    def add(self, ch):
        self.counts[ch] += 1
        self.candidates.append(ch)
        # Drop from the front anything that is no longer unique.
        while self.candidates and self.counts[self.candidates[0]] > 1:
            self.candidates.popleft()
        return self.candidates[0] if self.candidates else None


print()
stream = Stream()
for ch in "swiss":
    print(f"  after {ch!r}: first unique so far is {stream.add(ch)!r}")
print("Each add is O(1) amortised - every character enters and leaves once.")
''',
        "walk": [
            ("counts = Counter(s)",
             "The first pass. It decides nothing; it only records enough that "
             "the second pass can decide immediately."),
            ("for i, ch in enumerate(s):",
             "Walking the string, not the counter, because \"first\" is a "
             "property of the string. Iterating the dict works too and relies on "
             "insertion order &mdash; a language guarantee only since 3.7."),
            ("while self.candidates and self.counts[...] > 1:",
             "The streaming variant. The queue front is always the answer, and "
             "each character is pushed once and popped at most once, so it is "
             "O(1) amortised per arrival."),
            ("return -1, None",
             "Every character repeated. The sentinel has to be something the "
             "caller can distinguish from index 0 &mdash; the same trap as "
             "<code>str.find</code>."),
        ],
        "try": [
            "Feed the stream <code>\"aabbcc\"</code> and print after each "
            "character. The answer becomes <code>None</code> and stays there.",
            "Replace the deque with a list and <code>pop(0)</code>. Same answers, "
            "and the amortised O(1) is gone.",
        ],
    },
    check=[
        {"q": "Why can this not be solved in a single pass?",
         "options": ["Strings are immutable", "A character's uniqueness is not "
                     "decidable until the whole string has been read",
                     "Counters are slow", "It can be"],
         "answer": 1,
         "why": "The first character might repeat at the very end. A pass can "
                "record enough to answer afterwards, which is what the counter is."},
        {"q": "The second pass walks the string rather than the counter because:",
         "options": ["It is faster", "'First' is a property of the string's order",
                     "Counters are unordered", "It uses less memory"],
         "answer": 1,
         "why": "Walking the dict also works since 3.7, when insertion order "
                "became a guarantee - but you should say which you are relying on."},
        {"q": "In the streaming version, what makes each add O(1) amortised?",
         "options": ["The counter is O(1)", "Every character is pushed once and "
                     "popped at most once",
                     "The queue is sorted", "It only stores unique characters"],
         "answer": 1,
         "why": "The while loop can run several times on one call, but across "
                "the whole stream it does at most n pops in total."},
    ],
)


def _parens_frames():
    text = "{[()]}"
    out = []
    stack = []
    closers = {")": "(", "]": "[", "}": "{"}
    for i, ch in enumerate(text):
        if ch in "([{":
            stack.append(ch)
            note = "%r is an opener - push it." % ch
            state = "lo"
        else:
            want = closers[ch]
            got = stack.pop() if stack else None
            note = ("%r closes %r - matched, pop." % (ch, got) if got == want
                    else "%r expected %r but found %r - unbalanced."
                         % (ch, want, got))
            state = "hit" if got == want else "bad"
        marks = {j: ("dim" if j > i else "done") for j in range(len(text))}
        marks[i] = state
        out.append(frame([marked(list(text), marks, {i: "i"}, kind="text",
                                 label="input"),
                          marked(stack or ["(empty)"],
                                 {len(stack) - 1: "lo"} if stack else {},
                                 label="stack")],
                         note, {"i": i, "depth": len(stack)}))
    out.append(frame(marked(["(empty)"], {0: "hit"}, label="stack"),
                     "The stack is empty at the end, so every opener was closed. "
                     "A non-empty stack here means something was left open.",
                     {"i": len(text) - 1, "depth": 0}))
    return viz(out)


_q(
    slug="valid-parentheses",
    kind="coding",
    level="Easy",
    title="Valid parentheses",
    asked="Check whether a string of brackets is balanced.",
    desc="Bracket matching with a stack: the two failure modes, and why the "
         "empty-stack check at the end is not optional.",
    lead="A <strong>stack</strong>. Push every opener; on a closer, pop and check "
         "it matches. Two things fail: a closer with nothing to match, and a "
         "closer matching the wrong opener. A third check at the end catches "
         "openers that were never closed &mdash; miss it and "
         "<code>\"(((\"</code> passes.",
    say="\"Stack. Push openers, pop and compare on closers, and at the end the "
        "stack must be empty. Three failure modes: wrong match, closer with an "
        "empty stack, and leftovers at the end.\"",
    notice=[
        "The stack depth is the current nesting level.",
        "A match pops; a mismatch stops immediately.",
        "The final empty-stack check is what rejects <code>\"(((\"</code>.",
    ],
    viz=_parens_frames(),
    sections=[
        ("Why a stack and not a counter",
         "<p>With one bracket type, counting works: increment on open, decrement "
         "on close, fail if it goes negative or ends non-zero. With several "
         "types it does not &mdash; <code>\"([)]\"</code> has balanced counts and "
         "is wrong.</p>"
         "<p>A stack captures the thing a counter loses: not just how many are "
         "open, but <em>which</em>, and in what order. Nesting is inherently "
         "last-in-first-out, which is exactly what a stack is.</p>"),
        ("The three failure modes",
         "<p><strong>Mismatch.</strong> The popped opener does not correspond to "
         "the closer. <code>\"(]\"</code>.</p>"
         "<p><strong>Empty stack on a closer.</strong> A closer arrived with "
         "nothing open. <code>\")(\"</code> &mdash; and forgetting this check "
         "gives an <code>IndexError</code> rather than a <code>False</code>.</p>"
         "<p><strong>Non-empty stack at the end.</strong> Openers never closed. "
         "<code>\"(((\"</code> passes every in-loop check and is still "
         "unbalanced.</p>"),
        ("What it generalises to",
         "<p>This is the shape of every nesting problem: matching HTML tags, "
         "checking JSON structure, the call stack itself, and the "
         "shunting-yard algorithm that turns infix expressions into postfix. "
         "Once you see \"most recent unclosed thing\" in a problem, the answer is "
         "a stack.</p>"),
    ],
    code={
        "file": "parentheses.py",
        "intro": "The matcher with its stack printed at each step, run over "
                 "inputs chosen so each of the three failure modes fires once, "
                 "and a counter-based version that gets one of them wrong.",
        "code": '''# Balanced brackets: a stack, and the three ways it can fail.

PAIRS = {")": "(", "]": "[", "}": "{"}

def balanced(text, show=False):
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in PAIRS:
            if not stack:                       # failure 2: closer, nothing open
                return False, "closer %r with an empty stack" % ch
            if stack.pop() != PAIRS[ch]:        # failure 1: wrong opener
                return False, "%r does not close what was open" % ch
        if show:
            print(f"  {ch}  stack={''.join(stack) or '-'}")
    if stack:                                   # failure 3: never closed
        return False, "%d opener(s) never closed" % len(stack)
    return True, "balanced"


print("{[()]}, step by step:")
balanced("{[()]}", show=True)

print()
for text in ["{[()]}", "(]", ")(", "(((", "([)]", "", "()[]{}"]:
    ok, why = balanced(text)
    print(f"  {text!r:>10}: {str(ok):>5}  {why}")

# --- why a counter is not enough ---------------------------------------
def balanced_by_counting(text):
    """Correct for ONE bracket type. Wrong the moment there are two."""
    depth = 0
    for ch in text:
        if ch in "([{":
            depth += 1
        elif ch in PAIRS:
            depth -= 1
            if depth < 0:
                return False
    return depth == 0

print()
for text in ["([)]", "{[()]}", "(()"]:
    print(f"  {text!r:>8}: stack={balanced(text)[0]!s:>5}  "
          f"counter={balanced_by_counting(text)}")
print("'([)]' has balanced counts and is not balanced. A counter cannot see")
print("WHICH bracket is open, only how many.")
''',
        "walk": [
            ("stack.append(ch)",
             "Openers are remembered in order. The stack's top is always the "
             "most recent unclosed bracket, which is the only one a closer is "
             "allowed to match."),
            ("if not stack: return False",
             "A closer with nothing open. Skipping this check does not give a "
             "wrong answer &mdash; it gives an <code>IndexError</code>, which is "
             "worse in an interview."),
            ("if stack.pop() != PAIRS[ch]:",
             "Pop and compare in one step. The dictionary maps each closer to "
             "the opener it requires, which keeps the check to a single "
             "comparison."),
            ("if stack: return False",
             "The check people forget. <code>\"(((\"</code> passes every "
             "in-loop test and is still unbalanced."),
        ],
        "try": [
            "Delete the final <code>if stack:</code> and run <code>\"(((\"</code>. "
            "It reports balanced &mdash; the exact bug the check exists for.",
            "Extend it to HTML tags: push <code>&lt;div&gt;</code>, pop on "
            "<code>&lt;/div&gt;</code>. Same algorithm, and now it is a parser.",
        ],
    },
    check=[
        {"q": "Why is a counter not enough for multiple bracket types?",
         "options": ["Counters overflow", "'([)]' has balanced counts but the "
                     "wrong nesting order",
                     "Counters cannot go negative", "It is enough"],
         "answer": 1,
         "why": "A counter records how many are open, not which ones. Nesting is "
                "last-in-first-out, so it needs a stack."},
        {"q": "Which input passes every in-loop check and is still unbalanced?",
         "options": ["'(]'", "')('", "'((('", "'()'"],
         "answer": 2,
         "why": "Nothing inside the loop rejects unclosed openers. The final "
                "'is the stack empty?' test is what catches it."},
        {"q": "Forgetting the empty-stack check before popping gives you:",
         "options": ["A wrong answer", "An IndexError", "An infinite loop",
                     "The correct answer"],
         "answer": 1,
         "why": "Popping an empty list raises. It is the failure mode most "
                "likely to appear live in an interview."},
    ],
)


def _compress_frames():
    text = "aabcccccaaa"
    out = []
    parts = []
    i = 0
    while i < len(text):
        j = i
        while j < len(text) and text[j] == text[i]:
            j += 1
        parts.append("%s%d" % (text[i], j - i))
        marks = {k: ("hit" if i <= k < j else "done" if k < i else "dim")
                 for k in range(len(text))}
        out.append(frame([marked(list(text), marks, {i: "run"}, kind="text",
                                 label="input"),
                          marked(list("".join(parts)),
                                 {k: "done" for k in range(len("".join(parts)))},
                                 kind="text", label="output so far")],
                         "A run of %d %r, written as %r." % (j - i, text[i], parts[-1]),
                         {"runs": len(parts), "out len": len("".join(parts))}))
        i = j
    compressed = "".join(parts)
    shorter = len(compressed) < len(text)
    out.append(frame(pairs([("original", "%s (%d)" % (text, len(text))),
                            ("compressed", "%s (%d)" % (compressed, len(compressed))),
                            ("return", "compressed" if shorter else "original")],
                           {"return": "hit"}, label="verdict"),
                     "Only return the compressed form if it is actually shorter - "
                     "'abc' compresses to 'a1b1c1', which is worse.",
                     {"runs": len(parts), "out len": len(compressed)}))
    return viz(out)


_q(
    slug="string-compression",
    kind="coding",
    level="Medium",
    title="Run-length string compression",
    asked="Compress 'aabcccccaaa' to 'a2b1c5a3'. Return the original if the "
          "compressed form is not shorter.",
    desc="Run-length encoding with a builder rather than concatenation, the "
         "return-the-shorter rule, and the in-place variant on a character array.",
    lead="Walk the string counting runs of equal characters and append each "
         "<code>char + count</code> to a <strong>list</strong>, joined at the "
         "end. Building with <code>+=</code> makes it O(n&sup2;) &mdash; which is "
         "half of why this question is asked. Return the original unless the "
         "compressed form is genuinely shorter.",
    say="\"Count runs, append to a list, join at the end - never += in the loop. "
        "And return the original if compression didn't help, which 'abc' doesn't.\"",
    notice=[
        "Each highlighted block is one run, consumed in a single step.",
        "The output grows by two characters per run, not per input character.",
        "The final check is the part most people forget.",
    ],
    viz=_compress_frames(),
    sections=[
        ("The algorithm, and the trap inside it",
         "<p>Two pointers: one at the start of the current run, one scanning "
         "forward while the character stays the same. When it changes, emit "
         "<code>char</code> and <code>count</code> and move on. One pass, O(n).</p>"
         "<p>The trap is what you emit <em>into</em>. "
         "<code>result += ch + str(n)</code> allocates a new string on every "
         "run, which makes the whole thing quadratic in the output length. "
         "Appending to a list and joining once is O(n). Interviewers ask this "
         "question partly to see which you reach for.</p>"),
        ("Return the shorter one",
         "<p><code>\"abc\"</code> compresses to <code>\"a1b1c1\"</code>, which is "
         "twice as long. The specification almost always says to return the "
         "original when compression does not help, and the check is one "
         "comparison at the end.</p>"
         "<p>A common refinement is to bail out early once the output has "
         "already exceeded the input length, since it can never recover.</p>"),
        ("The in-place variant",
         "<p>The harder version gives you a character array and asks you to "
         "compress it in place, returning the new length. Because the compressed "
         "form is never longer than the original when it wins, a "
         "read-pointer/write-pointer pair works: read scans runs, write emits "
         "behind it, and write never overtakes read. That is the same two-pointer "
         "shape as the in-place dedupe.</p>"),
    ],
    code={
        "file": "compression.py",
        "intro": "The list-and-join version against the <code>+=</code> version, "
                 "timed on a long input so the quadratic is visible, plus the "
                 "in-place variant on a character array.",
        "code": '''# Run-length compression, and the concatenation trap inside it.
import time

def compress(text):
    if not text:
        return text
    parts = []                          # a list, joined once at the end
    i = 0
    while i < len(text):
        j = i
        while j < len(text) and text[j] == text[i]:
            j += 1
        parts.append(text[i])
        parts.append(str(j - i))
        i = j
    out = "".join(parts)
    return out if len(out) < len(text) else text        # only if it helps


def compress_slow(text):
    """Same algorithm, quadratic output building."""
    out = ""
    i = 0
    while i < len(text):
        j = i
        while j < len(text) and text[j] == text[i]:
            j += 1
        out += text[i] + str(j - i)     # a new string every run
        i = j
    return out if len(out) < len(text) else text


for text in ["aabcccccaaa", "abc", "aaaa", "", "a"]:
    print(f"{text!r:>14} -> {compress(text)!r}")
print("'abc' is returned unchanged: 'a1b1c1' would be longer.")

# --- the cost of building with += --------------------------------------
big = "".join(ch * 3 for ch in "abcdefghij" * 3000)
print()
for name, fn in (("list + join", compress), ("+= in a loop", compress_slow)):
    start = time.time()
    fn(big)
    print(f"  {name:>13}: {time.time() - start:.4f}s on {len(big):,} chars")

# --- the in-place variant ----------------------------------------------
def compress_in_place(chars):
    """Compress a character array in place. Returns the new length."""
    write = read = 0
    while read < len(chars):
        ch, run = chars[read], 0
        while read < len(chars) and chars[read] == ch:
            read += 1
            run += 1
        chars[write] = ch
        write += 1
        if run > 1:
            for digit in str(run):
                chars[write] = digit
                write += 1
    return write

chars = list("aabcccccaaa")
n = compress_in_place(chars)
print()
print("in place:", "".join(chars[:n]), f"(new length {n}, nothing allocated)")
''',
        "walk": [
            ("parts.append(...)",
             "The list is the whole point. <code>out += ...</code> allocates a "
             "new string per run, so the output building is quadratic even "
             "though the scan is linear."),
            ("while j < len(text) and text[j] == text[i]:",
             "The inner loop consumes an entire run in one go, so the outer loop "
             "runs once per run rather than once per character. Both pointers "
             "only move forwards."),
            ("return out if len(out) < len(text) else text",
             "The rule people forget. <code>\"abc\"</code> compresses to "
             "something twice as long, and the specification almost always asks "
             "for the shorter of the two."),
            ("write never overtakes read",
             "Why the in-place version is safe: whenever compression wins, the "
             "written prefix is shorter than the part already consumed, so it "
             "cannot clobber unread input."),
        ],
        "try": [
            "Compress a string of 10,000 distinct characters. The output is "
            "twice the input and the original comes back &mdash; check the early "
            "exit would have saved the work.",
            "Add the early bail-out: stop as soon as the output length reaches "
            "the input length, since it can never recover.",
        ],
    },
    check=[
        {"q": "Why append to a list rather than build the result with +=?",
         "options": ["Lists are shorter", "+= allocates a new string per run, "
                     "making the output building quadratic",
                     "Strings cannot be concatenated", "join is required"],
         "answer": 1,
         "why": "The scan is linear either way; the difference is entirely in "
                "how the output is assembled."},
        {"q": "compress('abc') should return:",
         "options": ["'a1b1c1'", "'abc'", "''", "'abc3'"],
         "answer": 1,
         "why": "The compressed form is longer, so the original is returned. "
                "That final comparison is the most commonly forgotten line."},
        {"q": "The in-place variant is safe because:",
         "options": ["The array is copied first", "The write pointer can never "
                     "overtake the read pointer when compression wins",
                     "Runs are always long", "It uses recursion"],
         "answer": 1,
         "why": "Each run of length k is written as at most k characters, so "
                "written output stays behind consumed input."},
    ],
)


def _prefix_frames():
    words = ["flower", "flow", "flight"]
    out = []
    prefix = words[0]
    for i, w in enumerate(words[1:], start=1):
        keep = 0
        while keep < len(prefix) and keep < len(w) and prefix[keep] == w[keep]:
            keep += 1
        marks = {j: ("hit" if j < keep else "bad") for j in range(len(prefix))}
        out.append(frame([marked(list(prefix), marks, kind="text",
                                 label="prefix so far"),
                          marked(list(w), {j: ("hit" if j < keep else "dim")
                                           for j in range(len(w))},
                                 kind="text", label="next word")],
                         "%r agrees with the prefix for %d character(s), so the "
                         "prefix shrinks to %r." % (w, keep, prefix[:keep]),
                         {"word": i, "prefix len": keep}))
        prefix = prefix[:keep]
        if not prefix:
            break
    out.append(frame(marked(list(prefix) or ["(empty)"],
                            {j: "done" for j in range(max(len(prefix), 1))},
                            kind="text", label="answer"),
                     "The prefix can only ever shrink, so one pass through the "
                     "list settles it.",
                     {"word": len(words) - 1, "prefix len": len(prefix)}))
    return viz(out)


_q(
    slug="longest-common-prefix",
    kind="coding",
    level="Easy",
    title="Longest common prefix",
    asked="Find the longest common prefix of a list of strings.",
    desc="Shrinking a candidate prefix across the list, why the answer is "
         "bounded by the shortest string, and the sorting trick.",
    lead="Take the first word as a candidate prefix and shrink it against each "
         "following word. The prefix only ever gets shorter, so one pass "
         "settles it &mdash; O(n&middot;m) in the worst case, and it exits early "
         "the moment the prefix is empty.",
    say="\"Start with the first string as the candidate and trim it against each "
        "of the others. It can only shrink, so one pass is enough - O(total "
        "characters), and it stops early on an empty prefix.\"",
    notice=[
        "The prefix shrinks and never grows.",
        "Comparison stops at the length of the shorter of the two.",
        "An empty prefix ends it immediately &mdash; nothing later can help.",
    ],
    viz=_prefix_frames(),
    sections=[
        ("The shrinking candidate",
         "<p>The answer is a prefix of every string, so it is certainly a prefix "
         "of the first one. Start there and remove characters as each new word "
         "disagrees. Because it only shrinks, no backtracking is possible and "
         "one pass is enough.</p>"
         "<p>Two bounds to state: the answer is at most the length of the "
         "<em>shortest</em> string, and the total work is O(sum of all "
         "characters) in the worst case &mdash; usually far less, because the "
         "candidate collapses quickly on real input.</p>"),
        ("The sorting trick",
         "<p>Sort the list and compare only the first and last strings. In "
         "lexicographic order those two are the most different, so their common "
         "prefix is the whole list's. It is O(n&nbsp;log&nbsp;n&middot;m) &mdash; "
         "worse asymptotically, and a nice observation to offer as an "
         "alternative rather than as the answer.</p>"),
        ("Vertical scanning, and tries",
         "<p>The other framing compares column by column: check index 0 across "
         "every word, then index 1, stopping at the first disagreement. Same "
         "complexity, and it exits earlier when the prefix is short and the "
         "strings are long.</p>"
         "<p>If the question becomes \"answer this repeatedly for many "
         "queries\", the answer is a trie: insert every word, then walk down "
         "from the root while each node has exactly one child and ends no word. "
         "That is the structure this question is a warm-up for.</p>"),
    ],
    code={
        "file": "common_prefix.py",
        "intro": "Three approaches on the same input with their character "
                 "comparisons counted, so \"horizontal versus vertical\" is a "
                 "measurement rather than a preference.",
        "code": '''# Longest common prefix: shrink a candidate, or scan columns.

def horizontal(words):
    """Take the first word and trim it against each of the others."""
    if not words:
        return "", 0
    prefix, comparisons = words[0], 0
    for w in words[1:]:
        keep = 0
        while keep < len(prefix) and keep < len(w) and prefix[keep] == w[keep]:
            comparisons += 1
            keep += 1
        comparisons += 1
        prefix = prefix[:keep]
        if not prefix:                  # nothing later can bring it back
            break
    return prefix, comparisons


def vertical(words):
    """Compare column by column across every word at once."""
    if not words:
        return "", 0
    comparisons = 0
    for i in range(len(words[0])):
        ch = words[0][i]
        for w in words[1:]:
            comparisons += 1
            if i >= len(w) or w[i] != ch:
                return words[0][:i], comparisons
    return words[0], comparisons


def by_sorting(words):
    """In lexicographic order, only the extremes matter."""
    if not words:
        return ""
    lo, hi = min(words), max(words)
    i = 0
    while i < len(lo) and i < len(hi) and lo[i] == hi[i]:
        i += 1
    return lo[:i]


for words in ([["flower", "flow", "flight"], ["dog", "racecar", "car"],
               ["same", "same"], []]):
    h, hc = horizontal(words)
    v, vc = vertical(words)
    print(f"{str(words):>34}: {h!r:>8}  horizontal={hc:>2} vertical={vc:>2} "
          f"sorted={by_sorting(words)!r}")

print()
print("On ['dog','racecar','car'] the prefix dies immediately - vertical")
print("notices on the first column, horizontal after the first word.")
''',
        "walk": [
            ("prefix = prefix[:keep]",
             "The candidate can only shrink, which is what rules out any need to "
             "backtrack. Each word is examined once."),
            ("if not prefix: break",
             "Once empty, nothing later in the list can extend it. On input with "
             "no shared first letter this turns the whole thing into one "
             "comparison."),
            ("keep < len(prefix) and keep < len(w)",
             "Both bounds are needed. The answer is capped by the shortest "
             "string, and dropping either check indexes past the end of one of "
             "them."),
            ("lo, hi = min(words), max(words)",
             "The sorting trick: in lexicographic order the extremes are the "
             "most different, so their shared prefix is the whole list's. "
             "Asymptotically worse, and a good thing to offer as an aside."),
        ],
        "try": [
            "Make the first word the longest and the last word a single "
            "character. Vertical scanning wins comfortably.",
            "Return the prefix length instead of the string to avoid the slice "
            "&mdash; the same reasoning as the slicing question.",
        ],
    },
    check=[
        {"q": "Why does one pass suffice?",
         "options": ["The list is sorted", "The candidate prefix can only shrink, "
                     "never grow",
                     "Strings are immutable", "It does not"],
         "answer": 1,
         "why": "No word can lengthen a prefix that an earlier word already "
                "trimmed, so there is nothing to backtrack over."},
        {"q": "The longest possible answer is bounded by:",
         "options": ["The first string", "The shortest string in the list",
                     "The number of strings", "The longest string"],
         "answer": 1,
         "why": "The prefix must be a prefix of every string, including the "
                "shortest one."},
        {"q": "Sorting the list and comparing only the first and last works "
              "because:",
         "options": ["Sorting groups similar strings",
                     "In lexicographic order those two are the most different, so "
                     "their shared prefix bounds every other pair",
                     "It removes duplicates", "It is faster"],
         "answer": 1,
         "why": "Neat, and asymptotically worse - O(n log n · m). Offer it as an "
                "alternative, not as the main answer."},
    ],
)


def _strstr_frames():
    text, pat = "abcabcabd", "abcabd"
    out = []
    lps = [0] * len(pat)
    length, i = 0, 1
    while i < len(pat):
        if pat[i] == pat[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    out.append(frame([marked(list(pat), {j: "lo" for j in range(len(pat))},
                             kind="text", label="pattern"),
                      marked([str(x) for x in lps],
                             {4: "hit"}, label="lps table")],
                     "First: the overlap table. lps[4]=3 because 'abcab' starts "
                     "and ends with 'ab'... plus one more.",
                     {"built": len(pat)}))
    i = j = 0
    comparisons = 0
    while i < len(text) and len(out) < 8:
        comparisons += 1
        if text[i] == pat[j]:
            marks = {k: ("hit" if i - j <= k <= i else "dim")
                     for k in range(len(text))}
            out.append(frame([marked(list(text), marks, {i: "i"}, kind="text",
                                     label="text"),
                              marked(list(pat), {k: ("hit" if k <= j else "dim")
                                                 for k in range(len(pat))},
                                     kind="text", label="pattern")],
                             "%r matches at text[%d]; advance both." % (text[i], i),
                             {"i": i, "j": j, "comparisons": comparisons}))
            i += 1
            j += 1
        elif j:
            old = j
            j = lps[j - 1]
            marks = {k: ("bad" if k == i else "dim") for k in range(len(text))}
            out.append(frame([marked(list(text), marks, {i: "i"}, kind="text",
                                     label="text"),
                              marked(list(pat), {k: "lo" for k in range(j)},
                                     kind="text", label="pattern slides")],
                             "Mismatch. The table says %d characters already "
                             "match, so j drops %d -> %d and i does NOT move back."
                             % (j, old, j),
                             {"i": i, "j": j, "comparisons": comparisons}))
        else:
            i += 1
    return viz(out)


_q(
    slug="implement-substring-search",
    kind="coding",
    level="Hard",
    title="Implement substring search (strStr)",
    asked="Find the first occurrence of a pattern in a text, without using the "
          "built-in.",
    desc="Naive substring search versus KMP: the prefix table, why the text "
         "index never moves backwards, and the input that separates them.",
    lead="The naive scan re-reads text after every mismatch, which is "
         "O(n&middot;m) and genuinely quadratic on repetitive input. "
         "<strong>KMP</strong> precomputes how far the pattern can safely slide, "
         "so the text index <em>never moves backwards</em> and the whole search "
         "is O(n + m).",
    say="\"Naive is O(n·m) and fine for most inputs. KMP builds a prefix table "
        "so on a mismatch the pattern slides instead of the text rewinding - "
        "O(n + m), and the text pointer only ever moves forward.\"",
    notice=[
        "The table is built first, from the pattern alone.",
        "On a mismatch the <em>pattern</em> slides; <code>i</code> stays put.",
        "That single property is the whole complexity difference.",
    ],
    viz=_strstr_frames(),
    sections=[
        ("What naive search wastes",
         "<p>Align the pattern at position 0, compare until a mismatch, then "
         "restart at position 1. The waste is that the comparisons already made "
         "are thrown away: on <code>\"aaaaaab\"</code> against "
         "<code>\"aaab\"</code>, almost every alignment re-reads the same "
         "characters.</p>"
         "<p>Worst case O(n&middot;m). Average case on natural text is close to "
         "O(n), which is why naive search is a perfectly reasonable answer to "
         "give first &mdash; then improve it.</p>"),
        ("The prefix table",
         "<p><code>lps[i]</code> is the length of the longest proper prefix of "
         "<code>pattern[:i+1]</code> that is also a suffix of it. That overlap "
         "is exactly the information needed: after a mismatch, the characters "
         "already matched end in something that also begins the pattern, so the "
         "pattern can slide to that alignment without re-reading anything.</p>"
         "<p>The table is built in O(m) using itself &mdash; on a mismatch while "
         "building, it falls back to <code>lps[length-1]</code> rather than "
         "restarting. That line looks wrong and is the reason the build is "
         "linear.</p>"),
        ("The property to state",
         "<p><code>i</code> never decreases. Every character of the text is "
         "examined a bounded number of times, so the search is O(n) after an "
         "O(m) preprocessing pass.</p>"
         "<p>Say what you would actually ship: <code>text.find(pattern)</code>, "
         "which in CPython is a tuned hybrid of Boyer-Moore and Horspool. The "
         "point of implementing KMP is the reasoning, and interviewers know "
         "that.</p>"),
    ],
    code={
        "file": "strstr.py",
        "intro": "Both searches with their comparisons counted, on ordinary text "
                 "and then on the repetitive input designed to make naive "
                 "matching look bad. The gap is the argument for the table.",
        "code": '''# Substring search: naive, then KMP.

def build_lps(pattern):
    """lps[i] = longest proper prefix of pattern[:i+1] that is also a suffix."""
    lps = [0] * len(pattern)
    length, i = 0, 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]     # fall back, do NOT restart at zero
        else:
            lps[i] = 0
            i += 1
    return lps


def naive_search(text, pattern):
    comparisons = 0
    for start in range(len(text) - len(pattern) + 1):
        k = 0
        while k < len(pattern):
            comparisons += 1
            if text[start + k] != pattern[k]:
                break
            k += 1
        else:
            return start, comparisons
    return -1, comparisons


def kmp_search(text, pattern):
    lps = build_lps(pattern)
    comparisons = 0
    i = j = 0
    while i < len(text):
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j, comparisons
        elif j:
            j = lps[j - 1]               # slide the pattern; i does not move
        else:
            i += 1
    return -1, comparisons


pattern = "abcabd"
print("pattern:", " ".join(pattern))
print("lps    :", " ".join(str(x) for x in build_lps(pattern)))
print("lps[4]=2: 'abcab' starts and ends with 'ab'.")

print()
for text in ["abcabcabd", "hello world", "a" * 60 + "b"]:
    pat = "aaab" if text.startswith("aaa") else pattern
    n_at, n_cmp = naive_search(text, pat)
    k_at, k_cmp = kmp_search(text, pat)
    label = text if len(text) < 20 else text[:12] + "..."
    print(f"{label:>16} looking for {pat!r:>8}: index {n_at:>3}  "
          f"naive={n_cmp:>4} kmp={k_cmp:>4}")

print()
print("On repetitive input naive re-reads the same characters over and over.")
print("KMP's i never moves backwards, which is the whole guarantee.")
print()
print("In production:", "abcabcabd".find("abcabd"),
      "- CPython's find is a tuned Boyer-Moore hybrid.")
''',
        "walk": [
            ("length = lps[length - 1]",
             "The line that makes the build linear, and the one that looks "
             "wrong. On a mismatch it falls back to the next-best border already "
             "computed &mdash; the table is built using itself."),
            ("elif j: j = lps[j - 1]",
             "The search's whole trick. The pattern slides forward while "
             "<code>i</code> stays put, because the table proves the skipped "
             "alignments cannot match."),
            ("i never decreases",
             "State this explicitly in an interview. It is the property that "
             "turns O(n&middot;m) into O(n + m), and it is what the table was "
             "built to guarantee."),
            ("text.find(pattern)",
             "What you would actually ship. Implementing KMP demonstrates the "
             "reasoning; using the built-in demonstrates judgement, and saying "
             "both is the complete answer."),
        ],
        "try": [
            "Lengthen the repetitive input to 500 a's. The naive count grows "
            "quadratically while KMP's stays linear.",
            "Build the table for <code>\"aaaa\"</code> and for <code>\"abcd\"</code>. "
            "All overlap and none &mdash; the two extremes of what it can say.",
        ],
    },
    check=[
        {"q": "In KMP's search loop, which index never moves backwards?",
         "options": ["j, the pattern index", "i, the text index", "Both", "Neither"],
         "answer": 1,
         "why": "That is the O(n + m) guarantee. Naive search restarts at "
                "start + 1 and re-reads characters it has already seen."},
        {"q": "lps[i] stores:",
         "options": ["The character at i", "The length of the longest proper "
                     "prefix of pattern[:i+1] that is also its suffix",
                     "How many matches so far", "The next index to check"],
         "answer": 1,
         "why": "That overlap is exactly what tells the algorithm how far the "
                "pattern may slide without re-reading text."},
        {"q": "Naive substring search is genuinely quadratic on:",
         "options": ["Random text", "Highly repetitive text such as 'aaaa...ab' "
                     "searched for 'aaab'",
                     "Short patterns", "Unicode text"],
         "answer": 1,
         "why": "Nearly every alignment matches a long way before failing, so "
                "the same characters are read again and again."},
    ],
)


def _isomorphic_frames():
    a, b = "paper", "title"
    out = []
    fwd, back = {}, {}
    for i, (x, y) in enumerate(zip(a, b)):
        ok = fwd.get(x, y) == y and back.get(y, x) == x
        fwd[x], back[y] = y, x
        marks = {j: ("hit" if j == i and ok else "bad" if j == i else "done"
                     if j < i else "dim") for j in range(len(a))}
        out.append(frame([marked(list(a), marks, kind="text", label="paper"),
                          marked(list(b), marks, kind="text", label="title"),
                          pairs(sorted(fwd.items()), {x: "hit"}, label="a -> b")],
                         "%r maps to %r%s." % (x, y,
                                               "" if ok else " - but it already "
                                               "mapped elsewhere, so no"),
                         {"pairs": len(fwd), "at": i}))
        if not ok:
            break
    out.append(frame(pairs([("a -> b", ", ".join("%s>%s" % kv for kv in sorted(fwd.items()))),
                            ("b -> a", ", ".join("%s>%s" % kv for kv in sorted(back.items()))),
                            ("isomorphic", "True")],
                           {"isomorphic": "hit"}, label="both directions"),
                     "Both maps stayed consistent. ONE map is not enough - it "
                     "would accept 'badc' -> 'baba'.",
                     {"pairs": len(fwd), "at": len(a) - 1}))
    return viz(out)


_q(
    slug="isomorphic-strings",
    kind="coding",
    level="Medium",
    title="Isomorphic strings",
    asked="Do two strings have the same character pattern? 'egg' and 'add' do; "
          "'foo' and 'bar' do not.",
    desc="Checking a one-to-one character mapping with two dictionaries, and why "
         "a single map accepts strings it should reject.",
    lead="Walk both strings together, maintaining <strong>two</strong> maps: "
         "a&nbsp;&rarr;&nbsp;b and b&nbsp;&rarr;&nbsp;a. Every pair must agree "
         "with both. One map alone allows two characters to collapse onto one, "
         "so it wrongly accepts <code>\"badc\"</code> and "
         "<code>\"baba\"</code> &mdash; which is exactly the case interviewers "
         "test.",
    say="\"Two dictionaries, one each way, because the mapping has to be a "
        "bijection. With only the forward map you'd accept two letters mapping "
        "onto the same one.\"",
    notice=[
        "Each step checks the pair against <em>both</em> maps.",
        "A character already mapped elsewhere fails immediately.",
        "The two maps at the end are inverses of each other.",
    ],
    viz=_isomorphic_frames(),
    sections=[
        ("What isomorphic means here",
         "<p>There must be a one-to-one correspondence between the characters: "
         "replacing every character of the first string according to a fixed "
         "rule produces the second, and no two characters map to the same "
         "target. \"Same shape, different letters\".</p>"
         "<p>A length check is a free first rejection, and the empty string is "
         "isomorphic to itself.</p>"),
        ("Why one map is not enough",
         "<p>Track only a&nbsp;&rarr;&nbsp;b and <code>\"badc\"</code> against "
         "<code>\"baba\"</code> passes: <code>b&rarr;b</code>, "
         "<code>a&rarr;a</code>, <code>d&rarr;b</code>, <code>c&rarr;a</code> "
         "&mdash; every forward rule is consistent, and two distinct characters "
         "have collapsed onto one target.</p>"
         "<p>The reverse map catches it: <code>b</code> is already claimed by "
         "<code>b</code>, so <code>d&rarr;b</code> is rejected. Both directions "
         "are needed because a bijection is a constraint in both directions.</p>"),
        ("The canonical-form alternative",
         "<p>Normalise each string to the pattern of first appearances &mdash; "
         "<code>\"paper\"</code> and <code>\"title\"</code> both become "
         "<code>[0,1,2,0,3]</code> &mdash; and compare the patterns. One pass "
         "each, no paired bookkeeping, and it extends naturally to comparing "
         "many strings at once by using the pattern as a dictionary key.</p>"
         "<p>That is the same \"canonicalise, then compare\" idea as grouping "
         "anagrams, which is worth pointing out.</p>"),
    ],
    code={
        "file": "isomorphic.py",
        "intro": "The two-map version and the single-map version run side by "
                 "side, on the input that separates them, plus the canonical-form "
                 "alternative reaching the same verdicts.",
        "code": '''# Isomorphic strings: the mapping has to work in BOTH directions.

def isomorphic(a, b):
    if len(a) != len(b):
        return False
    forward, backward = {}, {}
    for x, y in zip(a, b):
        if forward.setdefault(x, y) != y:      # x already maps elsewhere
            return False
        if backward.setdefault(y, x) != x:     # y is already claimed
            return False
    return True


def isomorphic_one_map(a, b):
    """The version with the bug, kept to show what it accepts."""
    if len(a) != len(b):
        return False
    forward = {}
    for x, y in zip(a, b):
        if forward.setdefault(x, y) != y:
            return False
    return True


def pattern(s):
    """Canonical form: the order in which distinct characters first appear."""
    seen = {}
    return tuple(seen.setdefault(ch, len(seen)) for ch in s)


tests = [("egg", "add"), ("foo", "bar"), ("paper", "title"),
         ("badc", "baba"), ("ab", "aa"), ("", "")]

print(f"{'a':>8} {'b':>8} {'two maps':>9} {'one map':>8} {'pattern':>8}")
for a, b in tests:
    two = isomorphic(a, b)
    one = isomorphic_one_map(a, b)
    pat = pattern(a) == pattern(b)
    flag = "   <-- one map is WRONG" if one != two else ""
    print(f"{a!r:>8} {b!r:>8} {str(two):>9} {str(one):>8} {str(pat):>8}{flag}")

print()
print("pattern('paper') =", pattern("paper"))
print("pattern('title') =", pattern("title"), "- same shape, so isomorphic")
print()
print("'badc' -> 'baba' is the case one map accepts: d and c both land on")
print("characters already claimed, which only the reverse map can see.")
''',
        "walk": [
            ("forward.setdefault(x, y) != y",
             "Insert on first sight, compare on every later sight, in one "
             "expression. If <code>x</code> already maps somewhere else, this is "
             "the check that catches it."),
            ("backward.setdefault(y, x) != x",
             "The direction people omit. Without it two distinct characters can "
             "map onto the same target, and <code>\"badc\"</code>/"
             "<code>\"baba\"</code> passes."),
            ("zip(a, b)",
             "Walks both together and stops at the shorter, which is why the "
             "length check has to come first &mdash; otherwise "
             "<code>\"ab\"</code> and <code>\"a\"</code> would compare equal on "
             "their overlap."),
            ("seen.setdefault(ch, len(seen))",
             "The canonical form: each new character gets the next number, so "
             "the tuple describes the shape rather than the letters. Same idea "
             "as the anagram key."),
        ],
        "try": [
            "Add <code>(\"abcd\", \"aabb\")</code>. Two characters collapsing "
            "onto one is exactly what the reverse map exists to reject.",
            "Use the pattern as a dictionary key to group many strings by shape "
            "in one pass &mdash; the same move as grouping anagrams.",
        ],
    },
    check=[
        {"q": "Why are two maps needed rather than one?",
         "options": ["For speed", "A single map allows two characters to map "
                     "onto the same target",
                     "To handle the empty string", "To keep it O(n)"],
         "answer": 1,
         "why": "'badc' against 'baba' passes every forward rule and is not "
                "isomorphic. The mapping has to be a bijection."},
        {"q": "The canonical-form approach compares:",
         "options": ["Sorted characters", "The order in which distinct "
                     "characters first appear",
                     "Character counts", "String lengths"],
         "answer": 1,
         "why": "'paper' and 'title' both become (0,1,2,0,3). It is the same "
                "'canonicalise then compare' move as grouping anagrams."},
        {"q": "Why must the length check come before zip?",
         "options": ["zip is slow", "zip stops at the shorter string, so unequal "
                     "lengths would compare only the overlap",
                     "zip needs equal lengths", "It does not"],
         "answer": 1,
         "why": "'ab' and 'a' would otherwise be reported isomorphic on the "
                "basis of their first character alone."},
    ],
)


def _palindrome_expand_frames():
    text = "babad"
    out = []
    best = (0, 1)
    for centre in range(len(text)):
        for lo0, hi0 in ((centre, centre), (centre, centre + 1)):
            lo, hi = lo0, hi0
            while lo >= 0 and hi < len(text) and text[lo] == text[hi]:
                lo -= 1
                hi += 1
            lo, hi = lo + 1, hi - 1
            if hi - lo + 1 > best[1] - best[0]:
                best = (lo, hi + 1)
            if hi >= lo and len(out) < 7:
                marks = {i: ("hit" if lo <= i <= hi else "dim")
                         for i in range(len(text))}
                out.append(frame(marked(list(text), marks, {centre: "centre"},
                                        kind="text", label="expand from a centre"),
                                 "Centre %s: %r expands to %r."
                                 % ("at %d" % centre if lo0 == hi0
                                    else "between %d and %d" % (centre, centre + 1),
                                    text[centre], text[lo:hi + 1]),
                                 {"centre": centre, "best": best[1] - best[0]}))
    out.append(frame(marked(list(text), {i: ("hit" if best[0] <= i < best[1] else "dim")
                                         for i in range(len(text))},
                            kind="text", label="answer"),
                     "Longest is %r. Every centre was tried - 2n-1 of them, "
                     "because a palindrome can sit between two characters."
                     % text[best[0]:best[1]],
                     {"centre": len(text) - 1, "best": best[1] - best[0]}))
    return viz(out)


_q(
    slug="longest-palindromic-substring",
    kind="coding",
    level="Medium",
    title="Longest palindromic substring",
    asked="Find the longest palindromic substring.",
    desc="Expand around centres in O(n²) with O(1) space, why there are 2n-1 "
         "centres rather than n, and where the O(n) algorithm fits.",
    lead="<strong>Expand around every centre.</strong> A palindrome is symmetric "
         "about its middle, so try each possible middle and grow outwards while "
         "the characters match. There are <strong>2n&nbsp;&minus;&nbsp;1</strong> "
         "centres, not n, because an even-length palindrome is centred between "
         "two characters. O(n&sup2;) time, O(1) space.",
    say="\"Expand around centres. 2n-1 centres because even-length palindromes "
        "sit between characters. O(n²) time but O(1) space, which beats the DP "
        "table. There's an O(n) algorithm - Manacher's - but I'd only reach for "
        "it if you want it.\"",
    notice=[
        "Each centre grows outwards until the characters stop matching.",
        "Odd and even centres are tried separately &mdash; that is the 2n&minus;1.",
        "Nothing is allocated; only indices move.",
    ],
    viz=_palindrome_expand_frames(),
    sections=[
        ("Why 2n − 1 centres",
         "<p>An odd-length palindrome like <code>aba</code> is centred on a "
         "character. An even-length one like <code>abba</code> is centred on the "
         "gap between two. So there are n character centres and n&nbsp;&minus;&nbsp;1 "
         "gap centres.</p>"
         "<p>Forgetting the even case is the classic bug here: the code passes "
         "on <code>racecar</code> and fails on <code>abba</code>, which is "
         "exactly the sort of half-correct that survives a quick test.</p>"),
        ("Why not dynamic programming",
         "<p>The DP formulation &mdash; <code>dp[i][j]</code> is true when "
         "<code>s[i:j+1]</code> is a palindrome &mdash; is also O(n&sup2;) time "
         "and additionally O(n&sup2;) <em>space</em>. Expanding around centres "
         "gets the same time in O(1) space and is shorter to write.</p>"
         "<p>Mention the DP version, then say why you are not using it. "
         "Recognising that two solutions share a time bound and differ on space "
         "is the judgement being tested.</p>"),
        ("The O(n) answer, and when to mention it",
         "<p>Manacher's algorithm is O(n): it reuses the palindromes already "
         "found to skip work, in the same spirit as KMP's prefix table. It is "
         "long, fiddly, and almost never expected.</p>"
         "<p>Name it, say it exists and that you would look it up rather than "
         "reconstruct it under time pressure. That reads as calibration; "
         "attempting it from memory and stalling does not.</p>"),
    ],
    code={
        "file": "longest_palindrome.py",
        "intro": "Expansion from both kinds of centre with each one's result "
                 "printed, then the odd-only version failing on an even-length "
                 "palindrome, and a brute-force check for agreement.",
        "code": '''# Longest palindromic substring: expand around every centre.

def expand(s, lo, hi):
    """Grow outwards while the ends match. Returns the widest span found."""
    while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
        lo -= 1
        hi += 1
    return lo + 1, hi - 1          # step back inside the last failed match


def longest_palindrome(s):
    if not s:
        return ""
    start, end = 0, 0
    for centre in range(len(s)):
        for lo, hi in ((centre, centre),        # odd length: centred on a char
                       (centre, centre + 1)):   # even length: centred on a gap
            a, b = expand(s, lo, hi)
            if b - a > end - start:
                start, end = a, b
    return s[start:end + 1]


def odd_centres_only(s):
    """The version that forgets even-length palindromes."""
    if not s:
        return ""
    start, end = 0, 0
    for centre in range(len(s)):
        a, b = expand(s, centre, centre)
        if b - a > end - start:
            start, end = a, b
    return s[start:end + 1]


def brute_force(s):
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            part = s[i:j + 1]
            if part == part[::-1] and len(part) > len(best):
                best = part
    return best


for text in ["babad", "cbbd", "abba", "racecar", "a", ""]:
    fast = longest_palindrome(text)
    odd = odd_centres_only(text)
    slow = brute_force(text)
    flag = "   <-- odd-only is WRONG" if odd != slow else ""
    print(f"{text!r:>10}: {fast!r:>9} (brute force agrees: {fast == slow}) "
          f"odd-only={odd!r}{flag}")

print()
print(f"For a string of length n there are 2n-1 centres, not n:")
for n in (1, 5, 10):
    print(f"  n={n:>2} -> {2 * n - 1} centres")
print()
print("Time O(n^2), space O(1). The DP table is the same time and O(n^2) space.")
''',
        "walk": [
            ("return lo + 1, hi - 1",
             "The loop exits one step past the last match, so both indices step "
             "back inside. Returning <code>lo, hi</code> directly is the "
             "off-by-one this function exists to contain."),
            ("(centre, centre) and (centre, centre + 1)",
             "The two kinds of centre. Odd-length palindromes sit on a "
             "character, even-length ones between two &mdash; which is where "
             "2n&nbsp;&minus;&nbsp;1 comes from."),
            ("odd_centres_only",
             "Kept to be wrong. It handles <code>racecar</code> correctly and "
             "misses <code>abba</code> entirely, which is the sort of failure "
             "that survives a careless test."),
            ("b - a > end - start",
             "Compares spans rather than slicing to compare lengths. Slicing "
             "inside the loop would allocate on every centre for no reason."),
        ],
        "try": [
            "Feed it a string of 2,000 identical characters. Every centre "
            "expands the whole way, which is the O(n&sup2;) worst case in full.",
            "Return the span instead of the substring and slice once at the end "
            "&mdash; the same reasoning as the slicing question.",
        ],
    },
    check=[
        {"q": "How many centres does the expansion approach try?",
         "options": ["n", "2n - 1", "n²", "log n"],
         "answer": 1,
         "why": "n character centres for odd-length palindromes plus n-1 gap "
                "centres for even-length ones. Forgetting the gaps is the classic bug."},
        {"q": "Compared with the DP table, expanding around centres is:",
         "options": ["Faster asymptotically", "The same time, but O(1) space "
                     "instead of O(n²)",
                     "Slower", "Only correct for odd lengths"],
         "answer": 1,
         "why": "Both are O(n²) time. The space difference is the reason to "
                "prefer expansion, and noticing that is the point of the question."},
        {"q": "The O(n) algorithm for this problem is:",
         "options": ["Binary search", "Manacher's algorithm", "KMP", "Kadane's"],
         "answer": 1,
         "why": "It reuses already-found palindromes to skip work, in the same "
                "spirit as KMP's prefix table. Naming it is usually enough."},
    ],
)


def _edit_frames():
    a, b = "cat", "cut"
    rows = len(a) + 1
    cols = len(b) + 1
    table = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        table[i][0] = i
    for j in range(cols):
        table[0][j] = j
    out = [frame(pairs([("row 0", " ".join(str(x) for x in table[0])),
                        ("col 0", " ".join(str(table[i][0]) for i in range(rows)))],
                       {"row 0": "lo"}, label="base cases"),
                 "The edges are free: turning a prefix into the empty string "
                 "costs one deletion per character.",
                 {"filled": rows + cols - 1})]
    for i in range(1, rows):
        for j in range(1, cols):
            same = a[i - 1] == b[j - 1]
            table[i][j] = (table[i - 1][j - 1] if same
                           else 1 + min(table[i - 1][j - 1], table[i - 1][j],
                                        table[i][j - 1]))
            out.append(frame([marked([str(x) for x in table[i]],
                                     {j: "hit"}, label="row %d (%r)" % (i, a[i - 1])),
                              pairs([("comparing", "%r vs %r" % (a[i - 1], b[j - 1])),
                                     ("cost here", table[i][j])],
                                    {"cost here": "hit"}, label="cell")],
                             "%s so the cost is %s."
                             % ("They match," if same else "They differ,",
                                "whatever the diagonal held" if same
                                else "1 + the cheapest of the three neighbours"),
                             {"i": i, "j": j, "cost": table[i][j]}))
    out.append(frame(marked([str(x) for x in table[-1]], {cols - 1: "hit"},
                            label="last row"),
                     "Bottom-right is the answer: %d edit(s) to turn %r into %r."
                     % (table[-1][-1], a, b),
                     {"i": rows - 1, "j": cols - 1, "cost": table[-1][-1]}))
    return viz(out)


_q(
    slug="edit-distance",
    kind="coding",
    level="Hard",
    title="Edit distance (Levenshtein)",
    asked="What is the minimum number of insertions, deletions and substitutions "
          "to turn one string into another?",
    desc="The Levenshtein DP table: what each of the three neighbours means, why "
         "the base cases are the edges, and how to drop the space to O(min(m, n)).",
    lead="A <strong>table</strong> where <code>dp[i][j]</code> is the cost of "
         "turning the first i characters of one string into the first j of the "
         "other. Each cell is either the diagonal unchanged (characters match) "
         "or one more than the cheapest of its three neighbours. "
         "O(m&middot;n) time and space, reducible to O(min(m, n)).",
    say="\"Classic DP. dp[i][j] is the cost for the two prefixes. If the "
        "characters match it's the diagonal; otherwise it's 1 plus the min of "
        "diagonal, left and up - substitute, insert, delete. O(m·n), and you "
        "only need two rows so space can be O(min(m,n)).\"",
    notice=[
        "The edges are free to fill: i deletions to reach the empty string.",
        "A match copies the diagonal &mdash; no cost added at all.",
        "Each neighbour corresponds to one specific edit.",
    ],
    viz=_edit_frames(),
    sections=[
        ("What each neighbour means",
         "<p>The three options are not arbitrary; each is one edit:</p>"
         "<p><strong>Diagonal</strong> (<code>dp[i-1][j-1]</code>) &mdash; "
         "substitute one character for the other. Free when they already "
         "match.</p>"
         "<p><strong>Up</strong> (<code>dp[i-1][j]</code>) &mdash; delete a "
         "character from the first string.</p>"
         "<p><strong>Left</strong> (<code>dp[i][j-1]</code>) &mdash; insert a "
         "character into the first string.</p>"
         "<p>Being able to say which is which is what separates understanding "
         "the recurrence from having memorised it.</p>"),
        ("The base cases",
         "<p>Row 0 and column 0 are the edges: turning a prefix of length i into "
         "the empty string costs i deletions, and building a prefix of length j "
         "from nothing costs j insertions. Filling them with zeros instead is the "
         "most common mistake, and it produces answers that are too small.</p>"),
        ("Cutting the space",
         "<p>Each cell depends only on the row above and the cell to its left, "
         "so the whole table is never needed at once &mdash; two rows suffice, "
         "and iterating over the shorter string makes it "
         "O(min(m,&nbsp;n)).</p>"
         "<p>The trade is that you can no longer walk the table backwards to "
         "recover the actual sequence of edits. If the question asks which edits, "
         "keep the full table; if it asks only for the count, the two-row "
         "version is strictly better.</p>"),
    ],
    code={
        "file": "edit_distance.py",
        "intro": "The full table printed for a small pair so the shape is "
                 "visible, the two-row version checked against it, and the "
                 "zeroed-base-case bug producing a confidently wrong answer.",
        "code": '''# Edit distance: three neighbours, three edits.

def edit_distance(a, b, show=False):
    rows, cols = len(a) + 1, len(b) + 1
    dp = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        dp[i][0] = i                      # i deletions to reach ""
    for j in range(cols):
        dp[0][j] = j                      # j insertions to build b[:j]

    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]           # match: free
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1],  # substitute
                                   dp[i - 1][j],      # delete
                                   dp[i][j - 1])      # insert
    if show:
        print("      " + "  ".join(f"{c:>2}" for c in " " + b))
        for i, row in enumerate(dp):
            label = " " if i == 0 else a[i - 1]
            print(f"   {label}  " + "  ".join(f"{v:>2}" for v in row))
    return dp[-1][-1]


def edit_distance_two_rows(a, b):
    """Same answer in O(min(m, n)) space - but no way to recover the edits."""
    if len(a) < len(b):
        a, b = b, a                       # iterate over the shorter one
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            current[j] = (previous[j - 1] if ca == cb
                          else 1 + min(previous[j - 1], previous[j], current[j - 1]))
        previous = current
    return previous[-1]


def zeroed_base_cases(a, b):
    """The version that fills the edges with zeros instead."""
    rows, cols = len(a) + 1, len(b) + 1
    dp = [[0] * cols for _ in range(rows)]
    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = (dp[i - 1][j - 1] if a[i - 1] == b[j - 1]
                        else 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]))
    return dp[-1][-1]


print("kitten -> sitting")
print("distance:", edit_distance("kitten", "sitting"))
print()
print("the table for cat -> cut:")
edit_distance("cat", "cut", show=True)

print()
for a, b in [("kitten", "sitting"), ("cat", "cut"), ("", "abc"), ("same", "same")]:
    full = edit_distance(a, b)
    rows2 = edit_distance_two_rows(a, b)
    zeroed = zeroed_base_cases(a, b)
    flag = "   <-- zeroed edges is WRONG" if zeroed != full else ""
    print(f"{a!r:>9} -> {b!r:<9} full={full} two-row={rows2} zeroed={zeroed}{flag}")
''',
        "walk": [
            ("dp[i][0] = i",
             "The base case people zero out by accident. Turning a prefix into "
             "the empty string costs one deletion per character, and starting "
             "from zero makes every answer too small."),
            ("dp[i][j] = dp[i - 1][j - 1]",
             "A match costs nothing at all &mdash; it copies the diagonal rather "
             "than adding to it. Adding 1 here is the other common slip."),
            ("min(diagonal, up, left)",
             "Substitute, delete, insert, in that order. Being able to name which "
             "neighbour is which edit is what shows you understand the "
             "recurrence rather than remember it."),
            ("previous = current",
             "The two-row version. Each cell needs only the row above and the "
             "cell to its left, so the full table is never required &mdash; "
             "unless you want to reconstruct the edits."),
        ],
        "try": [
            "Swap the argument order. The distance is symmetric, and watching "
            "the table transpose is a good check that you have the axes right.",
            "Add a fourth move for transposition (swapping adjacent characters). "
            "That turns it into Damerau-Levenshtein, which is what spell "
            "checkers actually use.",
        ],
    },
    check=[
        {"q": "In the DP table, the cell above dp[i][j] corresponds to which edit?",
         "options": ["Insert", "Delete a character from the first string",
                     "Substitute", "No edit"],
         "answer": 1,
         "why": "Up is delete, left is insert, diagonal is substitute. Naming "
                "them is what shows the recurrence is understood rather than memorised."},
        {"q": "Filling row 0 and column 0 with zeros instead of 0..n gives:",
         "options": ["The same answer", "Answers that are too small",
                     "An IndexError", "Answers that are too large"],
         "answer": 1,
         "why": "The edges encode the cost of reaching the empty string. Zeroing "
                "them makes those conversions free."},
        {"q": "The space can be reduced to O(min(m, n)) because:",
         "options": ["The strings are short", "Each cell depends only on the "
                     "previous row and the cell to its left",
                     "The table is symmetric", "Most cells are zero"],
         "answer": 1,
         "why": "Two rows suffice. The cost is that you can no longer walk the "
                "table back to recover which edits were made."},
    ],
)
