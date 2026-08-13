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


def _lru_frames():
    out = [frame([pairs([("cache", "empty"), ("capacity", "2")], {},
                        label="state"),
                  marked(["(front = newest)", "(back = oldest)"], {},
                         label="recency order", index=False)],
                 "A dict for O(1) lookup, and an order for O(1) eviction. "
                 "Neither alone is enough.",
                 {"size": 0, "evictions": 0})]
    order, cache, evictions = [], {}, 0
    for op, key, value in [("put", "a", 1), ("put", "b", 2), ("get", "a", None),
                           ("put", "c", 3), ("get", "b", None)]:
        note = ""
        if op == "put":
            if key in cache:
                order.remove(key)
            cache[key] = value
            order.append(key)
            if len(order) > 2:
                gone = order.pop(0)
                del cache[gone]
                evictions += 1
                note = "put(%s) - over capacity, so evict %r, the least recently used." % (key, gone)
            else:
                note = "put(%s, %s) - added, and it is now the newest." % (key, value)
        else:
            hit = key in cache
            if hit:
                order.remove(key)
                order.append(key)
                note = "get(%s) -> %s, and touching it makes it the newest." % (key, cache[key])
            else:
                note = "get(%s) -> miss. It was evicted earlier." % key
        out.append(frame([pairs([(k, cache[k]) for k in order] or [("cache", "empty")],
                                {order[-1]: "hit"} if order else {}, label="cache"),
                          marked(list(reversed(order)) or ["-"],
                                 {0: "lo"} if order else {},
                                 label="newest -> oldest", index=False)],
                         note, {"size": len(cache), "evictions": evictions}))
    return viz(out)


_q(
    slug="design-an-lru-cache",
    kind="coding",
    level="Hard",
    title="Design an LRU cache",
    asked="Design a cache with O(1) get and put that evicts the least recently "
          "used entry.",
    desc="Why an LRU cache needs both a hash map and a doubly linked list, what "
         "each one buys, and how OrderedDict does the same job in ten lines.",
    lead="Two structures, because neither alone gives you both operations in "
         "O(1). A <strong>hash map</strong> for lookup by key, and a "
         "<strong>doubly linked list</strong> for recency order &mdash; the map "
         "stores the node, so touching an entry unlinks and relinks it in "
         "constant time, and eviction is whatever sits at the tail.",
    say="\"Hash map plus doubly linked list. The map gives O(1) lookup and holds "
        "the node itself, so I can unlink it in O(1) without scanning. Most "
        "recent at the head, evict from the tail. In Python I'd reach for "
        "OrderedDict and move_to_end.\"",
    notice=[
        "A <code>get</code> is not read-only &mdash; it changes the order.",
        "Eviction always takes the oldest, which is why order must be maintained.",
        "The map stores the <em>node</em>, which is what makes unlinking O(1).",
    ],
    viz=_lru_frames(),
    sections=[
        ("Why one structure is not enough",
         "<p>A dictionary gives O(1) lookup and knows nothing about order. A list "
         "keeps order and needs O(n) to find and remove an arbitrary element. "
         "The requirement is both at once, so you carry both.</p>"
         "<p>The join between them is the important part: the map's value is not "
         "the cached value, it is the <em>node</em> in the linked list. That is "
         "what lets you go from a key straight to its position and unlink it "
         "without walking anything.</p>"),
        ("Why the list must be doubly linked",
         "<p>Removing a node in O(1) requires knowing the node before it. A "
         "singly linked list would need a scan to find the predecessor, which "
         "puts you back at O(n). The backward pointer is the whole reason for "
         "the extra memory.</p>"
         "<p>Most implementations also use sentinel head and tail nodes, so no "
         "insertion or removal is ever a special case &mdash; the same trick as "
         "the dummy head in a linked-list delete.</p>"),
        ("The Python answer",
         "<p><code>collections.OrderedDict</code> is exactly a dict plus a "
         "doubly linked list, and it exposes <code>move_to_end</code> and "
         "<code>popitem(last=False)</code>. That is the version to write in real "
         "code, and the ten-line implementation is a fine answer if you can also "
         "explain what it is doing underneath.</p>"
         "<p>Say which one the interviewer wants. \"Implement it from scratch\" "
         "means the nodes; \"use it\" means <code>OrderedDict</code>, or "
         "<code>functools.lru_cache</code> if it is memoisation rather than a "
         "cache you control.</p>"),
    ],
    code={
        "file": "lru_cache.py",
        "intro": "The from-scratch version with sentinel nodes, the "
                 "<code>OrderedDict</code> version, and both run through the same "
                 "sequence of operations so their answers can be compared.",
        "code": '''# LRU cache: a hash map for lookup, a doubly linked list for order.
from collections import OrderedDict

class Node:
    __slots__ = ("key", "value", "prev", "next")
    def __init__(self, key=None, value=None):
        self.key, self.value = key, value
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}                        # key -> NODE, not key -> value
        # Sentinels, so no insert or remove is ever a special case.
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head
        self.evictions = []

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)                   # a get CHANGES the order
        self._push_front(node)
        return node.value

    def put(self, key, value):
        node = self.map.get(key)
        if node:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        node = Node(key, value)
        self.map[key] = node
        self._push_front(node)
        if len(self.map) > self.capacity:
            oldest = self.tail.prev          # O(1): no scan needed
            self._unlink(oldest)
            del self.map[oldest.key]
            self.evictions.append(oldest.key)


class LRUOrderedDict:
    """The same thing, using the structure the standard library already has."""
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()
        self.evictions = []

    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.capacity:
            self.evictions.append(self.data.popitem(last=False)[0])


ops = [("put", "a", 1), ("put", "b", 2), ("get", "a", None),
       ("put", "c", 3), ("get", "b", None), ("get", "c", None), ("get", "a", None)]

for name, cls in (("from scratch", LRUCache), ("OrderedDict", LRUOrderedDict)):
    cache = cls(2)
    results = []
    for op, key, value in ops:
        results.append(cache.get(key) if op == "get" else (cache.put(key, value) or "-"))
    print(f"{name:>13}: {results}  evicted {cache.evictions}")

print()
print("get('b') is -1: putting 'c' evicted it, because 'a' had just been read")
print("and was therefore more recently used.")
''',
        "walk": [
            ("self.map = {}   # key -> NODE",
             "The join between the two structures. Storing the node rather than "
             "the value is what turns \"remove this key from the order\" into a "
             "pointer update instead of a scan."),
            ("self.head, self.tail = Node(), Node()",
             "Sentinels. With a real head and tail always present, unlinking "
             "never has to check for <code>None</code> &mdash; the same trick as "
             "the dummy head in a linked-list delete."),
            ("get() calls _unlink then _push_front",
             "A read mutates the structure. That surprises people, and it is the "
             "definition of \"recently used\" &mdash; a cache where reads did not "
             "count would be FIFO, not LRU."),
            ("oldest = self.tail.prev",
             "Eviction in O(1) because the order is maintained continuously. "
             "Searching for the least recently used at eviction time would be "
             "O(n) and defeat the whole design."),
        ],
        "try": [
            "Change <code>get</code> so it does not reorder. You now have a FIFO "
            "cache, and the eviction sequence changes &mdash; run it and see.",
            "Add a <code>capacity=0</code> case. Every put should evict "
            "immediately; most implementations crash.",
        ],
    },
    check=[
        {"q": "Why does an LRU cache need a doubly linked list rather than a "
              "singly linked one?",
         "options": ["To iterate backwards", "Removing an arbitrary node in O(1) "
                     "requires knowing its predecessor",
                     "To store more data", "It does not"],
         "answer": 1,
         "why": "With only forward pointers you would have to scan to find the "
                "node before, which is O(n) and defeats the requirement."},
        {"q": "What does the hash map store as its value?",
         "options": ["The cached value", "The list node holding that value",
                     "The insertion time", "The key again"],
         "answer": 1,
         "why": "Storing the node is what lets you go from a key straight to its "
                "position in the order and unlink it without walking."},
        {"q": "Does a successful get change the cache?",
         "options": ["No, reads are free", "Yes - it makes that entry the most "
                     "recently used",
                     "Only if the cache is full", "Only for the first read"],
         "answer": 1,
         "why": "That is what distinguishes LRU from FIFO. A cache where reads "
                "did not count would evict on insertion order instead."},
    ],
)


def _consecutive_frames():
    values = [100, 4, 200, 1, 3, 2]
    pool = set(values)
    out = [frame([marked(values, {}, label="input (unsorted)"),
                  pairs([(str(v), "in the set") for v in sorted(pool)], {},
                        label="set for O(1) membership")],
                 "Put everything in a set first. Every question from here is a "
                 "membership test, which is O(1).",
                 {"checked": 0, "best": 0})]
    best = 0
    for v in sorted(pool):
        is_start = v - 1 not in pool
        marks = {i: ("hit" if values[i] == v and is_start else
                     "dim" if values[i] == v else "dim") for i in range(len(values))}
        if not is_start:
            out.append(frame(marked(values, marks, label="input"),
                             "%d has %d before it, so it is not the start of a "
                             "run - skip it entirely." % (v, v - 1),
                             {"checked": v, "best": best}))
            continue
        length = 1
        while v + length in pool:
            length += 1
        best = max(best, length)
        out.append(frame(marked(values, {i: ("hit" if v <= values[i] < v + length
                                             else "dim") for i in range(len(values))},
                                label="input"),
                         "%d starts a run (no %d in the set). Walk forward: "
                         "length %d." % (v, v - 1, length),
                         {"checked": v, "best": best}))
    return viz(out)


_q(
    slug="longest-consecutive-sequence",
    kind="coding",
    level="Medium",
    title="Longest consecutive sequence",
    asked="Find the length of the longest run of consecutive integers in an "
          "unsorted array, in O(n).",
    desc="Why a set plus a start-of-run check gives O(n) rather than the O(n²) "
         "the nested loop suggests, and why sorting is the wrong answer.",
    lead="Put everything in a <strong>set</strong>, then only start counting "
         "from a value whose predecessor is absent. That single check is what "
         "keeps it O(n): every run is walked exactly once, from its start, so "
         "the inner loop across the whole input does n steps in total rather "
         "than n per element.",
    say="\"Set for O(1) membership, then for each value check whether value-1 is "
        "in the set. If it is, skip - something else starts that run. If it "
        "isn't, walk forward. Every element is visited at most twice, so O(n).\"",
    notice=[
        "Values with a predecessor present are skipped without any work.",
        "Each run is walked exactly once, from its lowest member.",
        "The input is never sorted.",
    ],
    viz=_consecutive_frames(),
    sections=[
        ("Why not just sort",
         "<p>Sorting makes it trivial &mdash; one pass counting adjacent runs "
         "&mdash; and costs O(n&nbsp;log&nbsp;n). The question asks for O(n) "
         "specifically to rule that out, so give the sorting answer, name its "
         "cost, and then improve it.</p>"),
        ("The check that makes it linear",
         "<p>Without the start-of-run test, each value walks its whole run and "
         "the work is quadratic on a long sequence. With it, a value only walks "
         "forward when <code>value - 1</code> is absent &mdash; and each run has "
         "exactly one such value.</p>"
         "<p>So across the entire input the inner loop takes as many steps as "
         "there are elements, not as many as elements times run length. Every "
         "element is touched at most twice: once in the outer loop, once by the "
         "walk of its own run.</p>"),
        ("Saying the complexity convincingly",
         "<p>This is the question where candidates write the right code and then "
         "call it O(n&sup2;) because there is a loop inside a loop. The argument "
         "to make out loud is amortised: the inner loop's <em>total</em> work "
         "across all iterations is bounded by n, because runs do not overlap.</p>"
         "<p>Same shape as the sliding window, where both pointers only move "
         "forward. A nested loop is not automatically quadratic; what matters is "
         "how many times the inner body can run in total.</p>"),
    ],
    code={
        "file": "consecutive.py",
        "intro": "The O(n) version with its inner-loop steps counted against the "
                 "version missing the start check, on an input built to make the "
                 "difference obvious.",
        "code": '''# Longest run of consecutive integers, in O(n).

def longest_run(values):
    pool = set(values)                       # O(1) membership from here on
    best = 0
    inner_steps = 0
    for v in pool:
        if v - 1 in pool:
            continue                         # not the start of a run - skip
        length = 1
        while v + length in pool:            # walk this run, once
            length += 1
            inner_steps += 1
        best = max(best, length)
    return best, inner_steps


def longest_run_no_check(values):
    """Same idea without the start test: every value walks its whole run."""
    pool = set(values)
    best = 0
    inner_steps = 0
    for v in pool:
        length = 1
        while v + length in pool:
            length += 1
            inner_steps += 1
        best = max(best, length)
    return best, inner_steps


def by_sorting(values):
    if not values:
        return 0
    ordered = sorted(set(values))
    best = run = 1
    for a, b in zip(ordered, ordered[1:]):
        run = run + 1 if b == a + 1 else 1
        best = max(best, run)
    return best


data = [100, 4, 200, 1, 3, 2]
best, steps = longest_run(data)
print("input :", data)
print("answer:", best, f"({steps} inner steps)")
print("sorted approach agrees:", by_sorting(data) == best)

# One long run is where the missing check costs you.
print()
big = list(range(1, 2001))
for name, fn in (("with the check", longest_run), ("without it", longest_run_no_check)):
    answer, steps = fn(big)
    print(f"  {name:>15}: answer={answer}, inner steps={steps:,}")

print()
print("Same answer. One does 2,000 steps in total, the other does about two")
print("million - and the code differs by a single `if`.")
''',
        "walk": [
            ("if v - 1 in pool: continue",
             "The line the whole complexity rests on. A value with a predecessor "
             "is somewhere in the middle of a run that another value will walk, "
             "so doing anything here is pure duplication."),
            ("while v + length in pool:",
             "A nested loop that is <em>not</em> quadratic. Runs do not overlap, "
             "so the total number of inner steps across the whole outer loop is "
             "bounded by n."),
            ("pool = set(values)",
             "Membership has to be O(1) for any of this to work. On a list the "
             "same code would be O(n&sup2;) at best."),
            ("for v in pool",
             "Iterating the set rather than the list also removes duplicate "
             "work when the input repeats values."),
        ],
        "try": [
            "Iterate <code>values</code> instead of <code>pool</code> on an "
            "input with many duplicates. Same answer, more work.",
            "Return the run itself rather than its length by remembering "
            "<code>v</code> when <code>best</code> improves.",
        ],
    },
    check=[
        {"q": "What makes the solution O(n) despite a loop inside a loop?",
         "options": ["The set is sorted", "Only the start of each run walks "
                     "forward, so the inner loop does n steps in total",
                     "The inner loop is capped", "It is actually O(n²)"],
         "answer": 1,
         "why": "Runs do not overlap, so total inner work is bounded by n. Each "
                "element is touched at most twice."},
        {"q": "How do you know a value starts a run?",
         "options": ["It is the smallest", "value - 1 is not in the set",
                     "It appears first in the array", "It is even"],
         "answer": 1,
         "why": "If the predecessor exists, some other value will walk this run "
                "from its true start, so this one can be skipped entirely."},
        {"q": "Why is sorting not the accepted answer?",
         "options": ["It gives the wrong result", "It is O(n log n), and the "
                     "question asks for O(n)",
                     "It cannot handle duplicates", "It uses too much memory"],
         "answer": 1,
         "why": "Sorting is correct and simpler - give it first, name its cost, "
                "then improve to the set-based version."},
    ],
)


def _subarray_frames():
    values = [3, 4, 7, 2, -3, 1, 4, 2]
    target = 7
    out = []
    seen = {0: 1}
    running = count = 0
    for i, v in enumerate(values):
        running += v
        need = running - target
        found = seen.get(need, 0)
        count += found
        marks = {j: ("done" if j < i else "dim") for j in range(len(values))}
        marks[i] = "hit" if found else "lo"
        out.append(frame([marked(values, marks, {i: "i"}, label="values"),
                          pairs(sorted((str(k), str(n)) for k, n in seen.items()),
                                {str(need): "hit"} if found else {},
                                label="prefix sum -> how many times seen")],
                         "Running sum %d. Looking for %d: %s"
                         % (running, need,
                            "seen %d time(s), so %d new subarray(s) end here."
                            % (found, found) if found
                            else "not seen, so nothing ends here."),
                         {"running": running, "count": count}))
        seen[running] = seen.get(running, 0) + 1
    return viz(out)


_q(
    slug="subarray-sum-equals-k",
    kind="coding",
    level="Medium",
    title="Subarray sum equals k",
    asked="Count the contiguous subarrays that sum to k.",
    desc="Prefix sums in a dictionary turn an O(n²) scan into one pass, why the "
         "map starts with {0: 1}, and why the sliding window does not work here.",
    lead="Carry a <strong>running sum</strong> and a dictionary of how often each "
         "running sum has been seen. A subarray ending here sums to k exactly "
         "when <code>running &minus; k</code> appeared earlier &mdash; so the "
         "count is a lookup, not a search. O(n) time and space.",
    say="\"Prefix sums in a dict. At each index I've got the running sum, and any "
        "earlier prefix equal to running minus k marks the start of a qualifying "
        "subarray. Seed the map with {0: 1} so subarrays starting at index 0 are "
        "counted. O(n).\"",
    notice=[
        "The map counts <em>occurrences</em>, not positions &mdash; duplicates matter.",
        "The lookup happens before the current sum is recorded.",
        "Negative numbers are why a sliding window cannot be used.",
    ],
    viz=_subarray_frames(),
    sections=[
        ("From a difference to a lookup",
         "<p>Let <code>P(i)</code> be the sum of everything up to index i. The "
         "subarray from j+1 to i sums to <code>P(i) &minus; P(j)</code>, so it "
         "equals k exactly when <code>P(j) = P(i) &minus; k</code>.</p>"
         "<p>That converts \"search backwards for a matching start\" into \"have "
         "I seen this value before?\", which a dictionary answers in O(1). It is "
         "the same move as Two Sum &mdash; compute the thing you need rather "
         "than hunting for it.</p>"),
        ("Why {0: 1} and not an empty map",
         "<p>The empty prefix has sum 0, and it must be in the map before the "
         "loop starts. Otherwise a subarray beginning at index 0 &mdash; where "
         "<code>running</code> itself already equals k &mdash; has no earlier "
         "prefix to match against and is never counted.</p>"
         "<p>Seeding with <code>{0: 1}</code> is the single most commonly missed "
         "line in this problem, and it fails on the simplest possible input: "
         "<code>[k]</code>.</p>"),
        ("Why not a sliding window",
         "<p>A sliding window needs the sum to grow when the window grows, so "
         "shrinking from the left is a sound response to overshooting. With "
         "negative numbers that monotonicity is gone: extending the window can "
         "make the sum smaller, so there is nothing to slide on.</p>"
         "<p>If the question guarantees all-positive values, say so and use the "
         "window &mdash; O(1) space instead of O(n). Noticing that the "
         "constraint changes the right answer is worth as much as the code.</p>"),
    ],
    code={
        "file": "subarray_sum.py",
        "intro": "The prefix-sum count against brute force with both operation "
                 "counts, the missing-seed bug failing on a one-element array, "
                 "and the sliding window breaking on a negative number.",
        "code": '''# Count subarrays summing to k: prefix sums in a dictionary.
from collections import defaultdict

def count_subarrays(values, k):
    seen = defaultdict(int)
    seen[0] = 1                       # the empty prefix - see below
    running = count = ops = 0
    for v in values:
        running += v
        ops += 1
        count += seen[running - k]    # look up BEFORE recording this prefix
        seen[running] += 1
    return count, ops


def count_no_seed(values, k):
    """The same code without seed {0: 1}."""
    seen = defaultdict(int)
    running = count = 0
    for v in values:
        running += v
        count += seen[running - k]
        seen[running] += 1
    return count


def brute_force(values, k):
    count = ops = 0
    for i in range(len(values)):
        total = 0
        for j in range(i, len(values)):
            total += values[j]
            ops += 1
            if total == k:
                count += 1
    return count, ops


def sliding_window(values, k):
    """Only valid when every value is positive."""
    lo = total = count = 0
    for hi, v in enumerate(values):
        total += v
        while total > k and lo <= hi:
            total -= values[lo]
            lo += 1
        if total == k:
            count += 1
    return count


data = [3, 4, 7, 2, -3, 1, 4, 2]
k = 7
fast, fast_ops = count_subarrays(data, k)
slow, slow_ops = brute_force(data, k)
print("values:", data, " k =", k)
print(f"  prefix sums : {fast} subarrays in {fast_ops} operations")
print(f"  brute force : {slow} subarrays in {slow_ops} operations")

# --- the seed ----------------------------------------------------------
print()
for sample in ([7], [7, 1], [1, 2, 4]):
    with_seed = count_subarrays(sample, 7)[0]
    without = count_no_seed(sample, 7)
    flag = "   <-- missing {0: 1} undercounts" if with_seed != without else ""
    print(f"  {str(sample):>12} k=7: seeded={with_seed} unseeded={without}{flag}")

# --- why the window fails ----------------------------------------------
print()
positive = [1, 2, 3, 4, 3]
mixed = [3, 4, -7, 7]
for sample in (positive, mixed):
    correct = count_subarrays(sample, 7)[0]
    window = sliding_window(sample, 7)
    flag = "   <-- window is WRONG (negatives)" if window != correct else ""
    print(f"  {str(sample):>18} k=7: prefix={correct} window={window}{flag}")
print()
print("A window assumes extending it can only increase the sum. One negative")
print("number destroys that, and with it the reason sliding is valid at all.")
''',
        "walk": [
            ("seen[0] = 1",
             "The empty prefix. Without it, a subarray starting at index 0 has "
             "no earlier prefix to match and is never counted &mdash; and "
             "<code>[7]</code> with k=7 returns 0."),
            ("count += seen[running - k]",
             "Adds the <em>number of times</em> that prefix occurred, not one. "
             "Several earlier positions can produce the same running sum, and "
             "each is a distinct subarray."),
            ("the lookup precedes seen[running] += 1",
             "Recording first would let the current prefix match itself when "
             "k is 0, counting an empty subarray that does not exist."),
            ("sliding_window",
             "Kept to be broken. It needs the sum to rise monotonically as the "
             "window grows, which one negative number destroys &mdash; the last "
             "block shows it giving the wrong count."),
        ],
        "try": [
            "Set <code>k = 0</code> on an array containing a <code>[2, -2]</code> "
            "pair. The count includes it, which is why the lookup must come "
            "before the record.",
            "Make every value positive and compare the window with the prefix "
            "map. Same answers, and the window uses O(1) space.",
        ],
    },
    check=[
        {"q": "Why is the prefix map seeded with {0: 1}?",
         "options": ["To avoid a KeyError", "So subarrays starting at index 0 "
                     "are counted",
                     "To count the empty subarray", "It is not needed"],
         "answer": 1,
         "why": "The empty prefix has sum 0. Without it, [7] with k=7 returns 0 - "
                "the simplest possible input fails."},
        {"q": "The map stores, for each prefix sum:",
         "options": ["Its index", "How many times it has occurred", "True or "
                     "False", "The subarray"],
         "answer": 1,
         "why": "Several earlier positions can share a running sum, and each is "
                "a distinct qualifying subarray, so counts are needed rather than positions."},
        {"q": "Why can't a sliding window be used here?",
         "options": ["The array is unsorted", "Negative values mean extending "
                     "the window can decrease the sum",
                     "k might be zero", "It is too slow"],
         "answer": 1,
         "why": "A window relies on the sum growing monotonically as it grows. "
                "If everything is positive, the window works and uses O(1) space."},
    ],
)


def _set_frames():
    a = [3, 1, 4, 1, 5]
    out = [frame([marked(a, {1: "bad", 3: "bad"}, label="list (order, duplicates)"),
                  pairs([("len", len(a)), ("x in list", "O(n) scan")],
                        {"x in list": "bad"}, label="properties")],
                 "A list keeps order and duplicates, and answers membership by "
                 "scanning.",
                 {"items": len(a), "distinct": len(set(a))})]
    out.append(frame([marked(sorted(set(a)), {i: "done" for i in range(len(set(a)))},
                             label="set (no order, no duplicates)"),
                      pairs([("len", len(set(a))), ("x in set", "O(1) probe")],
                            {"x in set": "hit"}, label="properties")],
                     "A set drops both, and answers membership by computing "
                     "where the value would be.",
                     {"items": len(a), "distinct": len(set(a))}))
    out.append(frame([marked(list(dict.fromkeys(a)),
                             {i: "hit" for i in range(len(dict.fromkeys(a)))},
                             label="dict.fromkeys (order kept, duplicates gone)"),
                      pairs([("len", len(dict.fromkeys(a))),
                             ("x in dict", "O(1) probe")],
                            {"x in dict": "hit"}, label="properties")],
                     "A dict gives O(1) membership AND insertion order, which is "
                     "the deduplication most people actually want.",
                     {"items": len(a), "distinct": len(set(a))}))
    return viz(out)


_q(
    slug="sets-versus-lists-and-deduplication",
    kind="concept",
    level="Easy",
    title="When should you use a set instead of a list?",
    asked="What does a set give you that a list does not, and how do you "
          "deduplicate while keeping order?",
    desc="Sets buy O(1) membership and lose order and duplicates; dict.fromkeys "
         "keeps order while deduplicating; and the set operators that replace "
         "whole loops.",
    lead="A set buys <strong>O(1) membership</strong> and pays for it by losing "
         "order and duplicates, and by requiring hashable elements. When you "
         "need the speed <em>and</em> the order, "
         "<code>dict.fromkeys(seq)</code> deduplicates in one pass and keeps "
         "insertion order.",
    say="\"Sets are for membership and uniqueness - O(1) instead of O(n). They "
        "lose order and need hashable elements. If I need dedup with order I use "
        "dict.fromkeys, since dicts have kept insertion order since 3.7.\"",
    notice=[
        "The set is smaller: duplicates are gone, and so is the order.",
        "<code>dict.fromkeys</code> keeps both the order and the O(1) lookup.",
        "All three hold the same distinct values.",
    ],
    viz=_set_frames(),
    sections=[
        ("What you gain and what you give up",
         "<p><strong>Gain:</strong> membership in O(1) rather than O(n), and "
         "uniqueness enforced for free.</p>"
         "<p><strong>Give up:</strong> order, duplicates, indexing "
         "(<code>s[0]</code> is a <code>TypeError</code>), and the ability to "
         "hold unhashable elements. You cannot put a list in a set, though you "
         "can put a tuple.</p>"
         "<p>Converting costs O(n), so a single membership test on a small list "
         "is not worth it. More than a couple of tests, or a large collection, "
         "and it is.</p>"),
        ("Deduplicating three ways",
         "<p><code>set(seq)</code> &mdash; fastest, order destroyed.</p>"
         "<p><code>sorted(set(seq))</code> &mdash; deduplicated and in sorted "
         "order, which is not the same as original order and is often what "
         "people accidentally ship.</p>"
         "<p><code>list(dict.fromkeys(seq))</code> &mdash; deduplicated in "
         "<em>first-seen</em> order, one pass, and the one to remember. Dicts "
         "have preserved insertion order since 3.7, so this is a guarantee "
         "rather than a trick.</p>"),
        ("The operators that replace loops",
         "<p><code>a &amp; b</code> intersection, <code>a | b</code> union, "
         "<code>a - b</code> difference, <code>a ^ b</code> symmetric "
         "difference, <code>a &lt;= b</code> subset. Each replaces a loop with a "
         "membership test inside it &mdash; which is to say, each replaces an "
         "accidental O(n&middot;m) with an O(n + m).</p>"
         "<p>\"Which users are in A but not B\" is <code>a - b</code>. Writing "
         "that as a comprehension over a list is the most common form of the "
         "quadratic trap.</p>"),
    ],
    code={
        "file": "sets.py",
        "intro": "The three deduplication idioms and what each does to order, "
                 "the set operators against their loop equivalents, and the "
                 "membership timing that motivates all of it.",
        "code": '''# Sets: O(1) membership, at the price of order and duplicates.
import time

items = ["b", "a", "c", "a", "b", "d"]
print("original           :", items)
print("set()              :", sorted(set(items)), "  order destroyed")
print("sorted(set())      :", sorted(set(items)), "  sorted, not original order")
print("dict.fromkeys()    :", list(dict.fromkeys(items)), "  first-seen order kept")

# --- what a set refuses ------------------------------------------------
print()
try:
    {[1, 2]}
except TypeError as e:
    print("a list in a set ->", e)
print("a tuple in a set ->", {(1, 2)})
try:
    sorted(set(items))[0]
    set(items)[0]
except TypeError as e:
    print("indexing a set  ->", e)

# --- the operators, and the loops they replace -------------------------
a = {"alice", "bob", "carol", "dave"}
b = {"carol", "dave", "erin"}
print()
print("a & b (in both)        :", sorted(a & b))
print("a | b (in either)      :", sorted(a | b))
print("a - b (in a only)      :", sorted(a - b))
print("a ^ b (in exactly one) :", sorted(a ^ b))
print("{'carol'} <= a         :", {"carol"} <= a)

# --- why it matters ----------------------------------------------------
big_a = list(range(6_000))
big_b = list(range(3_000, 9_000))

start = time.time()
loop = [x for x in big_a if x in big_b]            # O(n * m)
loop_time = time.time() - start

start = time.time()
operator = sorted(set(big_a) & set(big_b))         # O(n + m)
op_time = time.time() - start

print()
print(f"intersection of two {len(big_a):,}-item collections:")
print(f"  list comprehension : {loop_time:.4f}s")
print(f"  set operator       : {op_time:.4f}s   ({loop_time / op_time:.0f}x faster)")
print(f"  same answer        : {loop == operator}")
''',
        "walk": [
            ("list(dict.fromkeys(items))",
             "Deduplicates in first-seen order, in one pass. The idiom worth "
             "memorising, and a language guarantee rather than an implementation "
             "detail since 3.7."),
            ("sorted(set(items))",
             "Deduplicated <em>and reordered</em>. It looks like a tidy version "
             "of the previous line and quietly changes the output order, which "
             "is a real bug when the order carried meaning."),
            ("{[1, 2]}",
             "A <code>TypeError</code>: set elements must be hashable for the "
             "same reason dictionary keys must be. A tuple works."),
            ("set(big_a) & set(big_b)",
             "Two O(n) conversions and an O(min) intersection, against a "
             "comprehension that scans one list for every element of the other. "
             "The timing at the end is that difference."),
        ],
        "try": [
            "Deduplicate a list of dictionaries. It raises &mdash; and the usual "
            "fix is to key on something hashable, such as an id or a tuple of "
            "fields.",
            "Compare <code>a.isdisjoint(b)</code> with <code>not (a &amp; b)</code>. "
            "The first can stop at the first shared element instead of building "
            "the whole intersection.",
        ],
    },
    check=[
        {"q": "Which deduplicates a list while preserving the original order?",
         "options": ["set(items)", "list(dict.fromkeys(items))",
                     "sorted(set(items))", "items.unique()"],
         "answer": 1,
         "why": "Dicts have preserved insertion order since 3.7. sorted(set(...)) "
                "deduplicates and reorders, which is often shipped by accident."},
        {"q": "What can a list hold that a set cannot?",
         "options": ["Strings", "Unhashable elements such as lists", "Integers",
                     "None"],
         "answer": 1,
         "why": "Set elements must be hashable, for the same reason dictionary "
                "keys must be. A tuple works where a list does not."},
        {"q": "'Which items are in A but not in B' is best written as:",
         "options": ["A loop with `if x not in b`", "set_a - set_b",
                     "sorted(a) != sorted(b)", "a.remove(b)"],
         "answer": 1,
         "why": "The loop is O(n·m) when b is a list. The difference operator is "
                "O(n + m) and says what it means."},
    ],
)
