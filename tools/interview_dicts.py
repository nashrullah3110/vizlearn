# -*- coding: utf-8 -*-
"""The dictionary, set, hashing and complexity-trap questions.

The traps come last on purpose: they are the questions that get asked as
"what's the complexity of this code?", and every one of them is an instance of
something explained earlier in the track.

Same shape as tools/interview_strings.py; see tools/interview.py for the
fields each entry carries.
"""

from interview_viz import counter_fill, frame, marked, pairs, viz

DICTS = []


def _q(**kw):
    DICTS.append(kw)


# =========================================================================
# How dictionaries work
# =========================================================================

def _dict_frames():
    out = [frame([pairs([("hash('apple')", "…8f2c"),
                         ("% 8 slots", "slot 4")], {"% 8 slots": "hit"},
                        label="where does it go?"),
                  marked(["-", "-", "-", "-", "apple", "-", "-", "-"],
                         {4: "hit"}, label="slots")],
                 "The key's hash decides the slot. Nothing is searched for - "
                 "the address is computed.",
                 {"entries": 1, "slots": 8})]
    out.append(frame(marked(["-", "-", "banana", "-", "apple", "-", "cherry", "-"],
                            {2: "done", 4: "done", 6: "hit"}, label="slots"),
                     "More keys, more slots. Lookup is one hash and one probe "
                     "whatever the size.",
                     {"entries": 3, "slots": 8}))
    out.append(frame(marked(["-", "-", "banana", "date", "apple", "-", "cherry", "-"],
                            {3: "bad", 4: "done"}, label="slots"),
                     "'date' also hashed to slot 4. It is occupied, so the probe "
                     "moves on - a collision, resolved by looking elsewhere.",
                     {"entries": 4, "slots": 8}))
    out.append(frame(marked(["-", "-", "-", "-", "-", "-", "-", "-",
                             "-", "-", "-", "-", "-", "-", "-", "-"],
                            {}, label="16 slots, everything rehashed"),
                     "Past about two-thirds full the table doubles and EVERY key "
                     "is rehashed - the index is hash % size, and size changed.",
                     {"entries": 6, "slots": 16}))
    return viz(out)


_q(
    slug="how-does-a-python-dict-work",
    kind="concept",
    level="Medium",
    title="How does a Python dict work?",
    asked="How is a dictionary implemented, and why is lookup O(1)?",
    desc="Dictionaries as hash tables: how the slot is computed, what a "
         "collision costs, why resizing rehashes everything, and when O(1) stops "
         "being true.",
    lead="A <strong>hash table</strong>. The key's hash picks a slot, so a "
         "lookup computes an address rather than searching &mdash; which is why "
         "the size of the dictionary does not appear in the cost. Collisions are "
         "resolved by probing, and the table resizes and rehashes everything "
         "once it gets too full.",
    say="\"Hash table. hash(key) picks a slot, so lookup is a computation, not a "
        "search - O(1) average. Collisions probe to another slot, and it resizes "
        "and rehashes when the load factor gets too high. Worst case is O(n) if "
        "everything collides.\"",
    notice=[
        "The slot is <em>computed</em>, never searched for.",
        "A collision does not break anything &mdash; it costs an extra probe.",
        "A resize invalidates every slot, because the index is <code>hash % "
        "size</code>.",
    ],
    viz=_dict_frames(),
    sections=[
        ("Computing an address instead of searching",
         "<p>Two steps: hash the key to a number, then fold that number into a "
         "slot index. The lookup goes straight to that slot and compares keys "
         "there. Neither step depends on how many entries the dictionary holds, "
         "which is the entire O(1) claim.</p>"
         "<p>The comparison at the end is not optional. Two different keys can "
         "share a slot, so the answer is only correct because the key itself is "
         "checked &mdash; see <a href=\"../dsa/hash_tables.html\">hash "
         "tables</a> for the machinery in full.</p>"),
        ("Collisions and the load factor",
         "<p>When two keys want the same slot, CPython probes for another one "
         "using a sequence derived from the hash. That costs extra comparisons, "
         "and the fuller the table the longer the probe sequences get.</p>"
         "<p>So the table grows before that becomes a problem &mdash; past "
         "roughly two-thirds occupancy it allocates a bigger one and reinserts "
         "everything. A resize is O(n) and every key's slot changes, because "
         "the index is <code>hash % size</code> and <code>size</code> just "
         "moved. Amortised over the insertions that caused it, insertion is "
         "still O(1).</p>"),
        ("When O(1) is not true",
         "<p>If every key hashes to the same slot, every operation degrades to a "
         "linear scan. That is not hypothetical: it was a real denial-of-service "
         "attack, where an attacker sent form fields chosen to collide. Python's "
         "answer is <strong>hash randomisation</strong> &mdash; string hashes "
         "are salted per process, so an attacker cannot precompute a colliding "
         "set.</p>"
         "<p>That is also why dictionary iteration order must never be assumed "
         "to be hash order, and why <code>hash('x')</code> differs between "
         "runs.</p>"),
    ],
    code={
        "file": "how_dicts_work.py",
        "intro": "A miniature hash table built from a list of buckets so the "
                 "slot arithmetic is visible, then the same keys with a "
                 "deliberately terrible hash so you can watch O(1) become O(n).",
        "code": '''# A dictionary is a hash table. Here is one, small enough to read.

class TinyDict:
    def __init__(self, slots=8, hash_fn=hash):
        self.buckets = [[] for _ in range(slots)]
        self.slots = slots
        self.count = 0
        self.hash_fn = hash_fn
        self.probes = 0

    def _slot(self, key):
        return self.hash_fn(key) % self.slots      # fold the hash into range

    def put(self, key, value):
        bucket = self.buckets[self._slot(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1
        if self.count / self.slots > 0.66:         # the load factor
            self._resize()

    def get(self, key):
        for k, v in self.buckets[self._slot(key)]:
            self.probes += 1                       # comparisons, not lookups
            if k == key:
                return v
        raise KeyError(key)

    def _resize(self):
        old = self.buckets
        self.slots *= 2
        self.buckets = [[] for _ in range(self.slots)]
        for bucket in old:
            for k, v in bucket:                    # every key rehashed
                self.buckets[self._slot(k)].append((k, v))
        print(f"  ** resized to {self.slots} slots, rehashed {self.count} keys")

    def show(self):
        for i, bucket in enumerate(self.buckets):
            if bucket:
                print(f"    slot {i:>2}: {[k for k, _ in bucket]}")


words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

good = TinyDict()
for w in words:
    good.put(w, len(w))
print("with a real hash:")
good.show()
for w in words:
    good.get(w)
print(f"  {good.probes} key comparisons for {len(words)} lookups")

# --- the same keys, with a hash that spreads nothing --------------------
bad = TinyDict(hash_fn=lambda k: 1)
for w in words:
    bad.put(w, len(w))
print()
print("with hash_fn = lambda k: 1:")
bad.show()
for w in words:
    bad.get(w)
print(f"  {bad.probes} key comparisons for the same {len(words)} lookups")
print()
print("Same structure, same answers, and every operation is now O(n).")
print("O(1) was always conditional on the hash spreading keys out.")

# --- hash randomisation -------------------------------------------------
print()
print("hash('apple') this run:", hash("apple"))
print("Run this again and it changes: string hashes are salted per process,")
print("which is what stops an attacker crafting colliding keys on purpose.")
''',
        "walk": [
            ("self.hash_fn(key) % self.slots",
             "Two separate jobs. The hash turns a key into a number; the modulo "
             "folds it into a valid index. Change the number of slots and every "
             "index changes."),
            ("for k, v in self.buckets[...]",
             "The comparison that makes the answer correct rather than probable. "
             "Two keys can share a slot, so the key itself has to be checked."),
            ("if self.count / self.slots > 0.66:",
             "The load factor. Probe sequences lengthen sharply as a table "
             "fills, so it grows before that happens rather than after."),
            ("hash_fn=lambda k: 1",
             "Every key in one slot. The structure still works perfectly and "
             "every guarantee has evaporated &mdash; which is the point worth "
             "making about hash tables in general."),
        ],
        "try": [
            "Use <code>hash_fn=len</code>. Words of equal length collide, which "
            "is a far more realistic bad hash than the constant one.",
            "Print the buckets, then run the program again. The layout moves, "
            "because string hashing is salted per process.",
        ],
    },
    check=[
        {"q": "Dictionary lookup is O(1) because:",
         "options": ["Dictionaries are sorted", "The slot is computed from the "
                     "key's hash rather than searched for",
                     "Keys are unique", "It uses binary search"],
         "answer": 1,
         "why": "Neither hashing nor indexing depends on the number of entries. "
                "The key comparison at the slot is what makes it correct."},
        {"q": "Why does a resize have to rehash every key?",
         "options": ["Hashes change over time", "The index is hash % size, and "
                     "size just changed",
                     "To sort them", "To free memory"],
         "answer": 1,
         "why": "The hash is stable; the fold into a slot is not. Doubling the "
                "table moves nearly everything."},
        {"q": "Python randomises string hashes per process in order to:",
         "options": ["Improve distribution", "Stop an attacker crafting keys "
                     "that all collide",
                     "Save memory", "Preserve insertion order"],
         "answer": 1,
         "why": "Deliberately collided input turns every operation into a linear "
                "scan - a real denial-of-service attack. It is also why hash() "
                "differs between runs."},
    ],
)


def _hashable_frames():
    out = [frame(pairs([("(1, 2)", "hashable -> valid key"),
                        ("'abc'", "hashable -> valid key"),
                        ("frozenset()", "hashable -> valid key"),
                        ("[1, 2]", "unhashable -> TypeError")],
                       {"[1, 2]": "bad"}, label="can it be a key?"),
                 "Mutable containers are unhashable by design. The rule is not "
                 "arbitrary - the next frames show why.",
                 {"keys": 3})]
    out.append(frame([marked(["-", "-", "-", "key", "-", "-", "-", "-"],
                             {3: "hit"}, label="slots"),
                      pairs([("key", "[1, 2]"), ("hash", "-> slot 3")],
                            {"hash": "done"}, label="if lists were allowed")],
                     "Suppose a list could be a key. It hashes to slot 3 and is "
                     "stored there.",
                     {"keys": 1}))
    out.append(frame([marked(["-", "-", "-", "key", "-", "-", "-", "-"],
                             {3: "bad", 6: "lo"}, label="slots"),
                      pairs([("key", "[1, 2, 3]  (mutated!)"),
                             ("hash", "-> slot 6"),
                             ("d[key]", "KeyError")],
                            {"d[key]": "bad"}, label="after key.append(3)")],
                     "Mutating the key changes its hash. The lookup now goes to "
                     "slot 6, the entry is still in slot 3, and it is "
                     "unreachable forever.",
                     {"keys": 1}))
    return viz(out)


_q(
    slug="why-must-dict-keys-be-hashable",
    kind="concept",
    level="Medium",
    title="Why must dictionary keys be hashable?",
    asked="Why can a tuple be a dictionary key but a list cannot?",
    desc="Hashability is what keeps an entry findable: mutating a key would "
         "change its hash and orphan the entry, so only immutable types are "
         "allowed.",
    lead="Because the entry is stored in a slot chosen from the key's hash. If "
         "the key could change afterwards, its hash would change, the lookup "
         "would go to a different slot, and the entry would be "
         "<strong>unreachable</strong>. So keys must be immutable &mdash; "
         "tuples and strings qualify, lists and dicts do not.",
    say="\"The key's hash decides where the entry lives. If the key could mutate, "
        "the hash would change and you could never find the entry again - so "
        "keys have to be immutable. A tuple works; a list doesn't.\"",
    notice=[
        "The rule follows from the storage, not from taste.",
        "Mutating a key would leave the entry in a slot nothing looks at.",
        "A tuple <em>containing</em> a list is also unhashable &mdash; it goes "
        "all the way down.",
    ],
    viz=_hashable_frames(),
    sections=[
        ("The invariant being protected",
         "<p>Equal objects must have equal hashes, and an object's hash must not "
         "change while it is in use as a key. Both follow from how the table "
         "works: the hash is the address, so a moving hash is a moving "
         "address.</p>"
         "<p>Python enforces this by making mutable built-ins unhashable. "
         "<code>list</code>, <code>dict</code> and <code>set</code> all set "
         "<code>__hash__ = None</code>, which is why the error is "
         "<code>unhashable type</code> rather than something about "
         "dictionaries.</p>"),
        ("It goes all the way down",
         "<p>A tuple is hashable only if everything in it is. "
         "<code>(1, 2)</code> is a fine key; <code>(1, [2])</code> is not, "
         "because the tuple's hash is derived from its contents and one of them "
         "can change.</p>"
         "<p><code>frozenset</code> is the immutable set, and it is hashable "
         "for the same reason. <code>set</code> is not, which is why you cannot "
         "have a set of sets without it.</p>"),
        ("Custom objects",
         "<p>By default a custom object hashes by identity, so two equal-looking "
         "instances are different keys. Define <code>__eq__</code> and Python "
         "sets <code>__hash__</code> to <code>None</code> &mdash; because you "
         "have redefined equality and the default hash no longer agrees with "
         "it.</p>"
         "<p>To make it usable as a key, define <code>__hash__</code> too, over "
         "the same fields <code>__eq__</code> uses, and do not mutate those "
         "fields afterwards. <code>@dataclass(frozen=True)</code> does all of "
         "this correctly for you.</p>"),
    ],
    code={
        "file": "hashable.py",
        "intro": "What is and is not hashable, then a class that breaks the "
                 "contract on purpose &mdash; mutating a key after insertion and "
                 "losing the entry, exactly as the visualisation describes.",
        "code": '''# Keys must be hashable, because the hash is the address.
from dataclasses import dataclass

for value in [(1, 2), "abc", frozenset([1, 2]), 3.5, None]:
    print(f"  hashable: {str(value):>18}  hash={hash(value) % 1000:>4}")

print()
for value in [[1, 2], {"a": 1}, {1, 2}, (1, [2])]:
    try:
        hash(value)
    except TypeError as e:
        print(f"  NOT hashable: {str(value):>14}  -> {e}")
print("(1, [2]) fails because a tuple's hash comes from its contents.")

# --- breaking the contract on purpose ----------------------------------
class Sloppy:
    """Hashes on a field it then allows you to change. Do not do this."""
    def __init__(self, tag):
        self.tag = tag

    def __hash__(self):
        return hash(self.tag)

    def __eq__(self, other):
        return isinstance(other, Sloppy) and self.tag == other.tag

    def __repr__(self):
        return f"Sloppy({self.tag!r})"


key = Sloppy("a")
d = {key: "stored under 'a'"}
print()
print("before mutation:", d[key])

key.tag = "b"                        # the hash has now changed
print("after  mutation:")
try:
    print("  d[key] ->", d[key])
except KeyError as e:
    print("  d[key] -> KeyError:", e)
print("  but it is still in there:", list(d.items()))
print("  the entry is unreachable by its own key - this is the whole reason")
print("  mutable types are refused as keys.")

# --- the correct way to make an object a key ---------------------------
@dataclass(frozen=True)               # frozen: immutable AND hashable
class Point:
    x: int
    y: int


grid = {Point(0, 0): "origin", Point(1, 2): "somewhere"}
print()
print("frozen dataclass as a key:", grid[Point(1, 2)])
print("equal points are the same key:", Point(1, 2) == Point(1, 2),
      hash(Point(1, 2)) == hash(Point(1, 2)))
try:
    Point(1, 2).x = 5
except Exception as e:
    print("and it cannot be mutated:", type(e).__name__, "-", e)
''',
        "walk": [
            ("hash((1, [2]))",
             "Fails, because a tuple's hash is computed from its contents. "
             "Immutability has to hold all the way down, not just at the top "
             "level."),
            ("key.tag = \"b\"",
             "The contract broken deliberately. The entry stays in the slot "
             "chosen by the old hash while lookups go to the new one, so it is "
             "lost while still occupying memory."),
            ("list(d.items())",
             "The entry is still there and still iterable &mdash; only lookup by "
             "key is broken. That is what makes this class of bug so hard to "
             "diagnose."),
            ("@dataclass(frozen=True)",
             "Generates <code>__eq__</code> and <code>__hash__</code> over the "
             "same fields and blocks assignment. It is the correct way to make a "
             "value object usable as a key."),
        ],
        "try": [
            "Define <code>__eq__</code> on a class without <code>__hash__</code> "
            "and try to use it as a key. Python sets the hash to None for you "
            "&mdash; deliberately.",
            "Use a plain <code>@dataclass</code> instead of a frozen one. It is "
            "unhashable, for exactly the reason this page is about.",
        ],
    },
    check=[
        {"q": "A list cannot be a dictionary key because:",
         "options": ["Lists are too large", "Mutating it would change its hash "
                     "and orphan the entry",
                     "Lists are not comparable", "Lists have no order"],
         "answer": 1,
         "why": "The hash is the address. A moving hash means a moving address, "
                "and the entry becomes unreachable."},
        {"q": "Is (1, [2]) hashable?",
         "options": ["Yes, tuples are always hashable", "No - a tuple's hash "
                     "comes from its contents, and a list is mutable",
                     "Only if the list is empty", "Yes, but slowly"],
         "answer": 1,
         "why": "Immutability has to hold all the way down. frozenset exists so "
                "that set-like values can be keys."},
        {"q": "Defining __eq__ on a class without __hash__ makes instances:",
         "options": ["Hash by identity", "Unhashable - Python sets __hash__ to "
                     "None",
                     "Hash by value automatically", "Immutable"],
         "answer": 1,
         "why": "You redefined equality, so the identity-based default hash no "
                "longer agrees with it. @dataclass(frozen=True) does both correctly."},
    ],
)


_q(
    slug="counting-with-dictionaries",
    kind="coding",
    level="Easy",
    title="Count things with a dictionary",
    asked="Count the frequency of each item in a sequence. Now find the k most "
          "common.",
    desc="get, setdefault, defaultdict and Counter compared, plus top-k with a "
         "heap in O(n log k) rather than sorting everything.",
    lead="Four ways to write the same loop &mdash; <code>get</code>, "
         "<code>setdefault</code>, <code>defaultdict</code> and "
         "<code>Counter</code> &mdash; all O(n). For the k most common, do not "
         "sort everything: a <strong>heap of size k</strong> gives "
         "O(n&nbsp;log&nbsp;k), which matters when n is huge and k is ten.",
    say="\"Counter for the counting. For top-k I'd use heapq.nlargest rather "
        "than sorting - O(n log k) instead of O(n log n), which is the "
        "difference that matters when n is a billion.\"",
    notice=[
        "Each item costs one lookup and one write, whatever the dictionary holds.",
        "The counter grows only with <em>distinct</em> items.",
        "Nothing is ever searched for.",
    ],
    viz=viz(counter_fill(list("abracadabra"))),
    sections=[
        ("The four idioms",
         "<p><code>counts[x] = counts.get(x, 0) + 1</code> needs no import and "
         "makes the default explicit. <code>counts.setdefault(x, 0)</code> is "
         "the same idea and reads worse for counting. "
         "<code>defaultdict(int)</code> lets you write <code>counts[x] += "
         "1</code> directly. <code>Counter(seq)</code> does the whole loop in "
         "C.</p>"
         "<p>They are all O(n). Reach for <code>Counter</code> in real code and "
         "be able to write the <code>get</code> version when an interviewer asks "
         "you not to import anything.</p>"),
        ("One trap in defaultdict",
         "<p>Reading a missing key from a <code>defaultdict</code> "
         "<em>creates</em> it. <code>if counts[x] &gt; 5</code> silently inserts "
         "<code>x</code> with value 0, so a loop that only reads can grow the "
         "dictionary without anyone noticing.</p>"
         "<p>Use <code>.get()</code> or <code>in</code> when you are only "
         "asking. <code>Counter</code> does not have this problem: reading a "
         "missing key returns 0 without inserting.</p>"),
        ("Top-k without sorting",
         "<p>Sorting all the counts is O(m&nbsp;log&nbsp;m) in the number of "
         "distinct items. Keeping a heap of size k is O(m&nbsp;log&nbsp;k), "
         "which is what <code>heapq.nlargest</code> and "
         "<code>Counter.most_common(k)</code> do.</p>"
         "<p>For \"top 10 of a billion\" that is the difference between a "
         "practical job and an impossible one, and it is the answer the question "
         "is actually fishing for. Bucket sort by count is O(m) when the counts "
         "are bounded &mdash; worth mentioning as the linear option.</p>"),
    ],
    code={
        "file": "counting.py",
        "intro": "The four idioms producing identical counts, the "
                 "<code>defaultdict</code> read trap caught in the act, and "
                 "top-k timed three ways on a large input.",
        "code": '''# Counting: four spellings of one loop, then top-k without sorting.
from collections import Counter, defaultdict
import heapq, random, time

words = "the quick brown fox jumps over the lazy dog the fox".split()

by_get = {}
for w in words:
    by_get[w] = by_get.get(w, 0) + 1

by_setdefault = {}
for w in words:
    by_setdefault.setdefault(w, 0)
    by_setdefault[w] += 1

by_default = defaultdict(int)
for w in words:
    by_default[w] += 1

by_counter = Counter(words)

print("all four agree:",
      by_get == by_setdefault == dict(by_default) == dict(by_counter))
print("counts:", dict(sorted(by_counter.items(), key=lambda kv: -kv[1])))

# --- the defaultdict read trap -----------------------------------------
d = defaultdict(int)
d["seen"] += 1
print()
print("before reading a missing key:", dict(d))
if d["never_added"] > 5:              # a READ that inserts
    pass
print("after  reading a missing key:", dict(d), "<- it was created")

c = Counter()
c["seen"] += 1
_ = c["never_added"]                  # a read that does NOT insert
print("Counter after the same read :", dict(c))

# --- top-k: sorting versus a heap --------------------------------------
random.seed(7)
big = [random.randint(0, 50_000) for _ in range(300_000)]
counts = Counter(big)
k = 10
print()
print(f"{len(big):,} items, {len(counts):,} distinct, k = {k}")

start = time.time()
by_sorting = sorted(counts.items(), key=lambda kv: -kv[1])[:k]
sort_time = time.time() - start

start = time.time()
by_heap = heapq.nlargest(k, counts.items(), key=lambda kv: kv[1])
heap_time = time.time() - start

print(f"  sort everything : {sort_time:.4f}s   O(m log m)")
print(f"  heap of size k  : {heap_time:.4f}s   O(m log k)")
print(f"  same answer     : {[v for _, v in by_sorting] == [v for _, v in by_heap]}")
print()
print("At m = 50,000 the gap is small. At a billion distinct keys it is the")
print("difference between a job that finishes and one that does not.")
''',
        "walk": [
            ("counts.get(x, 0) + 1",
             "The version to write when told not to import anything. The default "
             "removes the \"first time?\" branch without hiding what is "
             "happening."),
            ("d[\"never_added\"] > 5",
             "A read that inserts. <code>defaultdict</code> creates on any "
             "missing lookup, so a loop that only inspects can grow the "
             "dictionary silently."),
            ("heapq.nlargest(k, ...)",
             "Keeps a heap of size k rather than sorting m items: "
             "O(m&nbsp;log&nbsp;k). <code>Counter.most_common(k)</code> does the "
             "same thing."),
            ("Counter(big)",
             "One pass in C. The counting is never the bottleneck &mdash; the "
             "question is always what you do with the counts afterwards."),
        ],
        "try": [
            "Raise the value range to 5,000,000 so nearly every item is "
            "distinct. The sort/heap gap widens as m grows.",
            "Implement top-k with bucket sort by count. O(m) when counts are "
            "bounded, which beats both.",
        ],
    },
    check=[
        {"q": "Reading a missing key from a defaultdict:",
         "options": ["Returns None", "Creates it with the default value",
                     "Raises KeyError", "Returns 0 without inserting"],
         "answer": 1,
         "why": "A read can grow the dictionary. Counter returns 0 without "
                "inserting, which is why it is safer for inspection."},
        {"q": "Finding the k most common items is best done with:",
         "options": ["Sorting all counts, O(m log m)", "A heap of size k, "
                     "O(m log k)",
                     "A linear scan, O(m²)", "Binary search"],
         "answer": 1,
         "why": "heapq.nlargest and Counter.most_common(k) both do this. For "
                "'top 10 of a billion' it is the whole question."},
        {"q": "Counting n items with a dictionary costs:",
         "options": ["O(n log n)", "O(n)", "O(n²)", "O(k) in the distinct count"],
         "answer": 1,
         "why": "One lookup and one write per item, each O(1) on average. Space "
                "is O(k) in the number of distinct items."},
    ],
)


# =========================================================================
# The complexity traps
# =========================================================================

def _trap_frames():
    out = [frame(pairs([("for x in items:", "n iterations"),
                        ("  if x in seen_list:", "O(n) each"),
                        ("total", "O(n^2)")],
                       {"total": "bad"}, label="the shape"),
                 "A linear scan inside a loop. Each line looks harmless; the "
                 "product is quadratic.",
                 {"n": 1000, "operations": 1000 * 1000})]
    out.append(frame(pairs([("seen = set(seen_list)", "O(n), once"),
                            ("for x in items:", "n iterations"),
                            ("  if x in seen:", "O(1) each"),
                            ("total", "O(n)")],
                           {"total": "hit"}, label="the fix"),
                     "One line moved out of the loop and one type changed. Same "
                     "answer, linear cost.",
                     {"n": 1000, "operations": 2000}))
    out.append(frame(pairs([("in on a list", "O(n)"),
                            ("+= on a string", "O(n) per step"),
                            ("pop(0) / insert(0, x)", "O(n)"),
                            ("sorted() inside a loop", "O(n log n) per step")],
                           {k: "bad" for k in ("in on a list", "+= on a string",
                                               "pop(0) / insert(0, x)",
                                               "sorted() inside a loop")},
                           label="the four to watch for"),
                     "All four are cheap once and quadratic in a loop. These are "
                     "what 'what is the complexity of this code?' is asking about.",
                     {"n": 1000, "operations": 1000000}))
    return viz(out)


_q(
    slug="accidental-quadratic-complexity",
    kind="concept",
    level="Medium",
    title="What is the complexity of this code?",
    asked="Here is a loop. What is its complexity? (The four traps interviewers "
          "actually use.)",
    desc="The four accidental quadratics in everyday Python - `in` on a list, "
         "+= on a string, pop(0) as a queue, and sorting inside a loop - with "
         "each one measured.",
    lead="Four shapes turn linear code quadratic, and interviewers use all of "
         "them: <code>in</code> on a <strong>list</strong> inside a loop, "
         "<code>+=</code> on a <strong>string</strong> in a loop, "
         "<code>pop(0)</code> used as a queue, and <code>sorted()</code> called "
         "inside a loop. Each is cheap once and fatal repeated.",
    say="\"That's O(n²) - the membership test inside the loop is a linear scan. "
        "Build a set once before the loop and it's O(n).\"",
    notice=[
        "Every individual line here is idiomatic and fine.",
        "The cost comes from the <em>nesting</em>, which is invisible on small "
        "input.",
        "Each fix is one line, and each is a different structure.",
    ],
    viz=_trap_frames(),
    sections=[
        ("The four shapes",
         "<p><strong>1. <code>x in a_list</code> inside a loop.</strong> The "
         "membership test is O(n). Fix: build a <code>set</code> once, before "
         "the loop.</p>"
         "<p><strong>2. <code>result += piece</code> in a loop.</strong> Strings "
         "are immutable, so each step copies everything so far. Fix: collect "
         "into a list and <code>\"\".join</code> at the end.</p>"
         "<p><strong>3. <code>list.pop(0)</code> or <code>insert(0, x)</code>.</strong> "
         "Both shift every other element. Fix: "
         "<code>collections.deque</code>.</p>"
         "<p><strong>4. <code>sorted()</code> inside a loop.</strong> Usually "
         "the data has not changed and the sort belongs outside it. Fix: sort "
         "once, or keep a heap if it really does change.</p>"),
        ("Why they survive code review",
         "<p>None of them looks wrong. Each line is idiomatic Python that would "
         "be fine on its own, and on a hundred elements every version is "
         "instant. The bug ships, and then someone doubles the input and "
         "everything takes four times as long.</p>"
         "<p>The habit worth building is to read the cost of a line rather than "
         "its appearance, and to notice when a linear operation has ended up "
         "inside a loop. \"What is this line's complexity, and how many times "
         "does it run?\" catches all four.</p>"),
        ("How to answer in the room",
         "<p>Name the shape, give the complexity, and give the fix in one "
         "sentence: <em>\"the membership test is a linear scan, so it's O(n&sup2;) "
         "&mdash; build a set before the loop and it's O(n)\"</em>. Do not "
         "hedge; these have definite answers.</p>"
         "<p>If asked to prove it, double the input and show the time going up "
         "fourfold. That is what the program below does for all four.</p>"),
    ],
    code={
        "file": "traps.py",
        "intro": "All four traps and all four fixes, each timed at two input "
                 "sizes so you can watch the broken version quadruple while the "
                 "fixed one doubles.",
        "code": '''# The four accidental quadratics, measured at two sizes each.
import time
from collections import deque

def timed(fn, *args):
    start = time.time()
    fn(*args)
    return time.time() - start


# --- 1. membership testing against a list ------------------------------
def in_list(items, pool):
    return [x for x in items if x in pool]


def in_set(items, pool):
    lookup = set(pool)                       # once, outside the loop
    return [x for x in items if x in lookup]


# --- 2. building a string with += --------------------------------------
class Buf:                                   # an attribute defeats CPython's
    def __init__(self):                      # in-place resize special case
        self.text = ""

def concat(n):
    b = Buf()
    for i in range(n):
        b.text += "x"
    return b.text


def join(n):
    parts = []
    for i in range(n):
        parts.append("x")
    return "".join(parts)


# --- 3. a queue built on a list ----------------------------------------
def queue_list(n):
    q = list(range(n))
    while q:
        q.pop(0)                             # shifts everything left


def queue_deque(n):
    q = deque(range(n))
    while q:
        q.popleft()                          # O(1)


# --- 4. sorting inside a loop ------------------------------------------
def sort_inside(values):
    out = []
    for _ in range(len(values)):
        out.append(sorted(values)[0])        # re-sorts every iteration
    return out


def sort_once(values):
    ordered = sorted(values)
    return [ordered[0] for _ in range(len(values))]


print(f"{'trap':>26} {'small':>9} {'2x input':>9} {'growth':>8}")
cases = [
    ("in on a list",   in_list,   in_set,      lambda n: (list(range(n)), list(range(n)))),
    ("+= on a string", concat,    join,        lambda n: (n,)),
    ("pop(0) as a queue", queue_list, queue_deque, lambda n: (n,)),
    ("sorted() in a loop", sort_inside, sort_once, lambda n: (list(range(n, 0, -1)),)),
]

for name, broken, fixed, make in cases:
    small = timed(broken, *make(2_000))
    large = timed(broken, *make(4_000))
    print(f"{name:>26} {small:>8.4f}s {large:>8.4f}s {large / max(small, 1e-9):>7.1f}x")

print()
print("Doubling the input roughly QUADRUPLES each of those. Now the fixes:")
print()
print(f"{'fixed version':>26} {'small':>9} {'2x input':>9} {'growth':>8}")
for name, broken, fixed, make in cases:
    small = timed(fixed, *make(2_000))
    large = timed(fixed, *make(4_000))
    print(f"{name:>26} {small:>8.4f}s {large:>8.4f}s {large / max(small, 1e-9):>7.1f}x")

print()
print("Roughly 2x, not 4x. Same answers, one line different in each.")
''',
        "walk": [
            ("lookup = set(pool)",
             "Built once, outside the loop. That single line converts "
             "O(n&middot;m) into O(n + m) and is the fix for the most common "
             "trap of the four."),
            ("parts.append(...) then \"\".join(parts)",
             "One allocation at the end instead of one per step. The "
             "<code>Buf</code> class exists so CPython's in-place string resize "
             "cannot hide the cost."),
            ("q.popleft()",
             "<code>deque</code> is a doubly linked list of blocks, so both ends "
             "are O(1). A queue on a list is the second most common accidental "
             "quadratic."),
            ("the growth column",
             "The number to read. Doubling the input roughly quadruples a "
             "quadratic and roughly doubles a linear one &mdash; which is how "
             "you demonstrate a complexity claim without arguing about it."),
        ],
        "try": [
            "Double the sizes again. The ratios hold, which is the point of "
            "measuring growth rather than absolute time.",
            "Move <code>set(pool)</code> inside the comprehension. It becomes "
            "worse than the list version &mdash; the fix is building it once, "
            "not using a set.",
        ],
    },
    check=[
        {"q": "for x in items: if x in a_list: ... has complexity:",
         "options": ["O(n)", "O(n²)", "O(n log n)", "O(1)"],
         "answer": 1,
         "why": "n iterations times an O(n) membership scan. Building a set "
                "before the loop makes it O(n)."},
        {"q": "Which fixes a queue built on list.pop(0)?",
         "options": ["Sorting the list", "collections.deque", "A set", "A tuple"],
         "answer": 1,
         "why": "pop(0) shifts every remaining element, so it is O(n) each and "
                "O(n²) overall. deque is O(1) at both ends."},
        {"q": "How do you demonstrate a quadratic without arguing about it?",
         "options": ["Read the source", "Double the input and show the time "
                     "going up about fourfold",
                     "Count the lines", "Profile one call"],
         "answer": 1,
         "why": "Growth is the observable property. Linear roughly doubles; "
                "quadratic roughly quadruples."},
    ],
)
