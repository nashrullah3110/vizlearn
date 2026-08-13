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
