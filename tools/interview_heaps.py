# -*- coding: utf-8 -*-
"""The heap and top-k questions.

Kth-largest already lives with the list questions, so these are the three that
follow once a heap is on the table: the top k of a stream, merging many sorted
inputs, and keeping a running median.

Every `viz` here is built by running the thing it draws - see
tools/interview_viz.py for why that matters.
"""

import heapq as _heapq

from interview_viz import cost_table, frame, marked, pairs, row, cell, viz

HEAPS = []


def _q(**kw):
    HEAPS.append(kw)


# =========================================================================
# 1. top k frequent
# =========================================================================

def _topk_frames():
    """Recorded by running the size-k heap over the counts."""
    counts = [("a", 5), ("b", 1), ("c", 9), ("d", 3), ("e", 7), ("f", 2)]
    k = 3
    heap, out = [], []
    for i, (key, c) in enumerate(counts):
        if len(heap) < k:
            _heapq.heappush(heap, (c, key))
            note = ("%s appears %d times. The heap is not full yet, so push it "
                    "- nothing can be ruled out until there are k." % (key, c))
            state = "lo"
        elif c > heap[0][0]:
            evicted = heap[0][1]
            _heapq.heapreplace(heap, (c, key))
            note = ("%s appears %d times, which beats the smallest in the heap "
                    "(%s). Replace it: one pop and one push, not a resort."
                    % (key, c, evicted))
            state = "hit"
        else:
            note = ("%s appears %d times, which cannot beat the heap's "
                    "smallest (%d). Skipped entirely - it never enters."
                    % (key, c, heap[0][0]))
            state = "bad"
        marks = {j: ("dim" if j > i else "done") for j in range(len(counts))}
        marks[i] = state
        out.append(frame(
            [marked(["%s:%d" % (kk, cc) for kk, cc in counts], marks,
                    {i: "reading"}, label="counts"),
             marked(["%s:%d" % (kk, cc) for cc, kk in sorted(heap)],
                    {0: "lo"}, label="heap of %d (smallest first)" % k)],
            note, {"seen": i + 1, "smallest kept": heap[0][0]}))
    top = sorted(heap, reverse=True)
    out.append(frame(
        marked(["%s:%d" % (kk, cc) for cc, kk in top],
               {j: "hit" for j in range(len(top))}, label="answer"),
        "The heap holds exactly the top %d, and the root was always the "
        "weakest of them - which is why one comparison was enough to reject "
        "everything else." % k,
        {"seen": len(counts), "smallest kept": heap[0][0]}))
    return viz(out)


_q(
    slug="top-k-frequent-elements",
    kind="coding",
    level="Medium",
    title="Top k frequent elements",
    asked="Return the k most frequent elements in a list.",
    desc="Top k with a heap of size k: why the root is the one comparison that "
         "rejects most of the input, and when a full sort or bucket sort is "
         "the better answer.",
    lead="Count, then keep a <strong>min-heap of size k</strong>. The root is "
         "the weakest of the current best k, so one comparison rejects any "
         "candidate that cannot beat it &mdash; and most of the input is "
         "rejected that way. O(n log k) rather than O(n log n), and the gap is "
         "real once the number of distinct values is large.",
    say="\"Count with a Counter, then keep a min-heap of size k keyed on the "
        "count. For each item, if the heap is short push it; otherwise compare "
        "against the root and replace only if it is bigger. That is O(n log k). "
        "heapq.nlargest does exactly this. If k is close to n I would just "
        "sort, and if the counts are small integers bucket sort is O(n).\"",
    notice=[
        "The heap never grows past k &mdash; that is what makes each operation "
        "log k.",
        "Most candidates are rejected by <em>one</em> comparison against the "
        "root.",
        "The root is the smallest of the kept values, not the largest.",
    ],
    viz=_topk_frames(),
    sections=[
        ("Why the root is the whole trick",
         "<p>A min-heap of size k has a useful property: its root is the "
         "<em>weakest</em> member of the best k seen so far. So the question "
         "\"could this candidate belong in the answer?\" is one comparison "
         "against the root, and if the answer is no the candidate is discarded "
         "without ever entering the heap.</p>"
         "<p>The editor below counts it: with 200,000 items and k = 10, only "
         "136 of them ever touched the heap. The other 199,864 cost one "
         "comparison each. That is where the log k comes from &mdash; not from "
         "clever bookkeeping, but from rejecting almost everything cheaply.</p>"),
        ("The three answers, and when each is right",
         "<p><strong>Heap of size k</strong> &mdash; O(n log k). The default "
         "answer, and the one to give first. <code>heapq.nlargest(k, ...)</code> "
         "is this, already written.</p>"
         "<p><strong>Full sort</strong> &mdash; O(n log n). Better when k is a "
         "large fraction of n, because then log k is log n and the heap is "
         "paying overhead for nothing. Also better when n is small enough that "
         "constants dominate, which is more often than the complexity suggests: "
         "CPython's sort is C and a heap loop is Python.</p>"
         "<p><strong>Bucket sort</strong> &mdash; O(n). Available because the "
         "counts are bounded: a count cannot exceed n, so you can bucket by "
         "count and read the buckets from the top with no comparisons at all. "
         "It is the answer an interviewer is fishing for when they ask "
         "\"can you do better than n log k?\" &mdash; though note what the "
         "editor measures: it comes out level with <code>nlargest</code> "
         "rather than ahead, because removing a log factor does not beat a C "
         "implementation at this size. The complexity win is real; the "
         "wall-clock win needs a much larger n or k.</p>"),
        ("Quickselect, and why it is usually the wrong answer to give",
         "<p>There is an O(n) average-case option: partition around a pivot "
         "like quicksort but recurse into one side only, stopping when the "
         "pivot lands at position k. It is genuinely O(n) expected and "
         "O(n&sup2;) worst case, and <code>numpy.partition</code> implements "
         "it.</p>"
         "<p>Mentioning it is good; reaching for it first is usually not. It "
         "mutates the input, it does not stream, the worst case needs "
         "median-of-medians to fix, and the constant factor means it rarely "
         "beats <code>nlargest</code> in practice. The strong answer is the "
         "heap, with quickselect named as the theoretical improvement.</p>"),
        ("What the question is testing",
         "<p>Whether you notice that the answer set is bounded. A great many "
         "problems say \"the best k\" and the instinct is to sort everything "
         "and take a slice &mdash; which computes a total order nobody asked "
         "for. Keeping only k candidates and rejecting against the weakest of "
         "them is the reusable move, and it reappears in streaming top-n, "
         "nearest-neighbour search and leaderboards.</p>"
         "<p>The second thing is whether you ask about ties. \"The k most "
         "frequent\" is ambiguous when counts are equal, and saying so before "
         "writing is the difference between a correct answer and a complete "
         "one.</p>"),
    ],
    code={
        "file": "top_k.py",
        "intro": "The size-k heap against a full sort at 200,000 items, the "
                 "count of how many candidates ever entered the heap, and the "
                 "bucket version that beats both.",
        "code": 'import heapq, random, time\nfrom collections import Counter\n\nrandom.seed(7)\nwords = [random.randint(0, 40_000) for _ in range(200_000)]\ncounts = Counter(words)\nk = 10\nprint("n =", len(words), " distinct =", len(counts), " k =", k)\n\n# 1. sort everything, take a slice: O(n log n)\nt0 = time.perf_counter()\nby_sort = [w for w, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:k]]\na = time.perf_counter() - t0\n\n# 2. a heap of size k: O(n log k)\nt0 = time.perf_counter()\nby_heap = [w for w, _ in heapq.nlargest(k, counts.items(), key=lambda kv: kv[1])]\nb = time.perf_counter() - t0\n\n# 3. bucket by count: O(n), because a count cannot exceed n\ndef by_buckets(counts, k):\n    if not counts:\n        return []\n    buckets = [[] for _ in range(max(counts.values()) + 1)]\n    for key, c in counts.items():\n        buckets[c].append(key)\n    out = []\n    for c in range(len(buckets) - 1, 0, -1):\n        for key in buckets[c]:\n            out.append(key)\n            if len(out) == k:\n                return out\n    return out\n\nt0 = time.perf_counter()\nby_bucket = by_buckets(counts, k)\nc = time.perf_counter() - t0\n\nprint("all three pick the same counts:",\n      sorted(counts[w] for w in by_sort)\n      == sorted(counts[w] for w in by_heap)\n      == sorted(counts[w] for w in by_bucket))\nprint(f"  full sort   {a*1000:7.1f} ms   O(n log n)")\nprint(f"  nlargest    {b*1000:7.1f} ms   O(n log k)")\nprint(f"  buckets     {c*1000:7.1f} ms   O(n), level with the heap at this size")\n\n# Where the log k actually comes from: how little ever enters the heap.\ndef top_k(pairs, k):\n    heap = []\n    entered = skipped = 0\n    for key, cnt in pairs:\n        if len(heap) < k:\n            heapq.heappush(heap, (cnt, key)); entered += 1\n        elif cnt > heap[0][0]:\n            heapq.heapreplace(heap, (cnt, key)); entered += 1\n        else:\n            skipped += 1                # rejected by ONE comparison\n    return sorted(heap, reverse=True), entered, skipped\n\nkept, entered, skipped = top_k(counts.items(), k)\nprint()\nprint(f"of {len(counts):,} distinct values:")\nprint(f"  {entered:,} ever entered the heap")\nprint(f"  {skipped:,} were rejected by a single comparison against the root")\nprint(f"  the heap never held more than {k}")\n',
        "walk": [
            ("elif c > heap[0][0]",
             "One comparison against the root. If the candidate cannot beat "
             "the weakest kept value it is discarded without a heap operation "
             "at all &mdash; which is what most of the input does."),
            ("heapq.heapreplace(heap, (c, key))",
             "Pop and push as one operation, which is cheaper than "
             "<code>heappop</code> followed by <code>heappush</code> because "
             "the heap is only rebalanced once."),
            ("(c, key)",
             "The tuple puts the count first so the heap orders on it. Putting "
             "the key first would order alphabetically, which is the classic "
             "silent wrong answer here."),
            ("buckets[c].append(key)",
             "The O(n) version. A count cannot exceed n, so there are at most "
             "n+1 buckets and reading them from the top is linear &mdash; no "
             "comparisons at all."),
        ],
        "try": [
            "Set k equal to the number of distinct values and compare the "
            "timings again. The heap loses, which is the honest boundary of the "
            "recommendation.",
            "Break the ties deliberately: make two values share a count and "
            "decide whether the answer should be alphabetical. The heap's tuple "
            "already decides for you, and probably not the way you intended.",
        ],
    },
    check=[
        {"q": "Why a min-heap rather than a max-heap for top k?",
         "options": ["Min-heaps are faster",
                     "The root is the weakest kept value, so one comparison rejects a candidate",
                     "heapq only provides min-heaps",
                     "To keep the answer sorted"],
         "answer": 1,
         "why": "You need cheap access to the thing you would evict, which is "
                "the smallest of the best k."},
        {"q": "What is the complexity?",
         "options": ["O(n)", "O(n log k)", "O(n log n)", "O(k log n)"],
         "answer": 1,
         "why": "Each of n items costs at most one heap operation on a heap "
                "bounded at size k."},
        {"q": "When is a full sort the better choice?",
         "options": ["Never",
                     "When k is a large fraction of n, so log k is already log n",
                     "When the input is unsorted",
                     "When k is 1"],
         "answer": 1,
         "why": "The heap's advantage is that k is small. Once it is not, the "
                "sort's C implementation wins on constants."},
        {"q": "How can top k be done in O(n)?",
         "options": ["With a faster heap",
                     "Bucket by count, since a count cannot exceed n, then read the buckets from the top",
                     "By sorting with radix sort",
                     "It cannot"],
         "answer": 1,
         "why": "Bounded integer keys make counting sort applicable, which "
                "removes comparisons entirely."},
    ],
)


# =========================================================================
# 2. merge k sorted sequences
# =========================================================================

def _merge_frames():
    """Recorded by running the k-way merge and logging the heap each step."""
    lists = [[1, 5, 9], [2, 6], [3, 4, 10]]
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    _heapq.heapify(heap)
    merged, out = [], []
    while heap and len(merged) < 6:
        value, li, ci = _heapq.heappop(heap)
        merged.append(value)
        nxt = ci + 1
        pushed = nxt < len(lists[li])
        if pushed:
            _heapq.heappush(heap, (lists[li][nxt], li, nxt))
        out.append(frame(
            [marked([str(v) for v, _, _ in sorted(heap)] or ["(empty)"],
                    {0: "lo"} if heap else {},
                    label="heap: one candidate per list"),
             marked([str(v) for v in merged],
                    {len(merged) - 1: "hit"}, label="output")],
            "Pop the smallest, %d, from list %d. %s The heap holds at most one "
            "value per list, so it never exceeds k."
            % (value, li,
               "Its successor %d takes its place." % lists[li][nxt] if pushed
               else "That list is exhausted, so nothing replaces it."),
            {"emitted": len(merged), "heap": len(heap)}))
    return viz(out)


_q(
    slug="merge-k-sorted-sequences",
    kind="coding",
    level="Hard",
    title="Merge k sorted sequences",
    asked="Merge k sorted lists into one sorted output. What does it cost?",
    desc="K-way merge with a heap of size k: O(N log k) instead of O(N log N), "
         "why heapq.merge is the streaming answer, and why sorted() still wins "
         "when you want the whole thing in memory.",
    lead="Keep a heap holding <strong>one candidate per list</strong>. Pop the "
         "smallest, emit it, and push that list's successor &mdash; so the heap "
         "never exceeds k and each of the N values costs one log k operation. "
         "<code>heapq.merge</code> is this, lazily. Its real win is memory, not "
         "speed: for materialising everything, <code>sorted()</code> is usually "
         "faster.",
    say="\"A min-heap with one entry per list, each tagged with which list it "
        "came from. Pop the smallest, emit it, push the next value from that "
        "same list. The heap stays at size k, so it is O(N log k) for N total "
        "values. heapq.merge does exactly this and is lazy, which is the "
        "version I would use for streams. If everything fits in memory and I "
        "just want a sorted list, concatenating and calling sorted is usually "
        "faster in CPython, because Timsort exploits the existing runs in C.\"",
    notice=[
        "The heap holds one entry per list &mdash; at most k, never N.",
        "Each popped value is replaced by its own list's successor, which is "
        "what keeps the merge correct.",
        "A list that runs out simply stops being represented.",
    ],
    viz=_merge_frames(),
    sections=[
        ("Why the heap is size k and not N",
         "<p>The next value in the merged output must be the smallest "
         "unconsumed value, and because each input is already sorted, each "
         "list's smallest unconsumed value is its head. So only k values are "
         "ever candidates &mdash; one per list &mdash; and the heap needs to "
         "hold exactly those.</p>"
         "<p>That is the whole complexity argument. N values come out, each "
         "costing one pop and at most one push on a heap of size k, giving "
         "O(N log k). Concatenating and sorting is O(N log N), and log k is "
         "smaller than log N whenever k is smaller than N &mdash; which is "
         "the usual case, with many long lists.</p>"),
        ("The tag, and what happens without it",
         "<p>The heap entries are tuples: <code>(value, list_index, "
         "position)</code>. The list index is not decoration &mdash; it is how "
         "you know which list to pull the successor from. Storing bare values "
         "loses that, and the merge cannot continue.</p>"
         "<p>The index also settles ties deterministically, which matters when "
         "values are equal: the tuple comparison falls through to the list "
         "index and the merge becomes stable. And if the values are objects "
         "that are not comparable, the tuple will try to compare them and "
         "raise &mdash; which is why the index goes <em>second</em>, not "
         "third, in implementations that need to avoid that.</p>"),
        ("What the standard library gives you, and the honest measurement",
         "<p><code>heapq.merge(*lists)</code> is this algorithm, and it "
         "returns a <strong>generator</strong>: it never materialises the "
         "result, so memory is O(k) rather than O(N), and the first value is "
         "available immediately.</p>"
         "<p>The editor below measures both claims and the second one is worth "
         "seeing. Asking for just the smallest value takes 0.3 ms lazily "
         "against 140 ms if you sort first &mdash; a few hundred times less "
         "work for the same answer. But materialising <em>everything</em> is "
         "the other way round: <code>sorted(concatenation)</code> beats "
         "<code>list(heapq.merge(...))</code>, often by two or three times, "
         "because Timsort is C and detects the sorted runs while "
         "<code>heapq.merge</code> is a Python-level generator paying "
         "per-item overhead.</p>"
         "<p>So the honest answer has two halves: O(N log k) is the right "
         "algorithmic answer, and in CPython you reach for "
         "<code>heapq.merge</code> when the input streams or does not fit, and "
         "for <code>sorted()</code> when it does.</p>"),
        ("Where this actually gets used",
         "<p>External sorting: split a file too large for memory into sorted "
         "chunks, then k-way merge the chunks back. That is what "
         "<code>sort(1)</code> does, and it is why the merge has to be lazy "
         "&mdash; the whole point is that the result does not fit either.</p>"
         "<p>The same structure merges sorted posting lists in a search index, "
         "combines time-ordered log files, and is the merge step of an LSM-tree "
         "compaction. Any time several sorted streams have to become one, this "
         "is the shape, and the heap is the part that makes it O(N log k) "
         "rather than O(Nk).</p>"),
    ],
    code={
        "file": "merge_k.py",
        "intro": "The hand-rolled merge, then both of heapq.merge's claims "
                 "measured - the laziness it does win on, and the full "
                 "materialisation it does not.",
        "code": '''import heapq, random, time

def merge_k(lists):
    """One candidate per list: O(N log k)."""
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    out = []
    while heap:
        value, li, ci = heapq.heappop(heap)
        out.append(value)
        if ci + 1 < len(lists[li]):
            heapq.heappush(heap, (lists[li][ci + 1], li, ci + 1))
    return out

demo = [[1, 5, 9], [2, 6], [3, 4, 10]]
print("hand-rolled:", merge_k(demo))
print("heapq.merge:", list(heapq.merge(*demo)))
print("agree:", merge_k(demo) == list(heapq.merge(*demo)))

random.seed(3)
K, N = 50, 4_000
lists = [sorted(random.randint(0, 10**6) for _ in range(N)) for _ in range(K)]
print()
print(f"{K} lists x {N} items = {K*N:,} values")

# heapq.merge is LAZY - it returns an iterator.
m = heapq.merge(*lists)
print("heapq.merge returns a:", type(m).__name__)

# Claim 1: laziness. Just the smallest value.
t0 = time.perf_counter(); lazy_first = next(heapq.merge(*lists)); c = time.perf_counter() - t0
t0 = time.perf_counter(); eager_first = sorted(x for lst in lists for x in lst)[0]; d = time.perf_counter() - t0
print()
print("just the smallest value:")
print(f"  next(heapq.merge(...))  {c*1000:7.2f} ms")
print(f"  sort everything first   {d*1000:7.2f} ms   ({d/c:.0f}x more work)")
print("  same value:", lazy_first == eager_first)

# Claim 2: materialising everything. This one goes the other way.
t0 = time.perf_counter(); a_out = sorted(x for lst in lists for x in lst); a = time.perf_counter() - t0
t0 = time.perf_counter(); b_out = list(heapq.merge(*lists)); b = time.perf_counter() - t0
print()
print("the whole merged list:")
print(f"  sorted(concatenation)   {a*1000:7.1f} ms   <- Timsort, in C, finds the runs")
print(f"  list(heapq.merge(...))  {b*1000:7.1f} ms   <- Python generator, per-item cost")
print("  same result:", a_out == b_out)
print()
print("O(N log k) is the algorithmic answer. In CPython, reach for merge when")
print("the input streams or does not fit, and for sorted() when it does.")
''',
        "walk": [
            ("(lst[0], i, 0)",
             "Value, which list, and where in it. The list index is what lets "
             "you pull the successor after a pop &mdash; without it the merge "
             "cannot continue."),
            ("if ci + 1 < len(lists[li])",
             "The replacement comes from the <em>same</em> list as the value "
             "just emitted. That is the invariant: one candidate per live "
             "list, so the heap stays at k."),
            ("next(heapq.merge(*lists))",
             "The laziness claim, as a measurement. A few hundred times less "
             "work than sorting to get the same first value."),
            ("list(heapq.merge(*lists))",
             "And the claim that does not hold: materialising everything is "
             "slower than concatenating and sorting, because Timsort is C and "
             "already exploits the sorted runs."),
        ],
        "try": [
            "Set K to 2 and compare again. With two lists the heap buys almost "
            "nothing and <code>sorted()</code> wins more clearly &mdash; log k "
            "of 2 is 1.",
            "Merge lists of unequal length, including an empty one. The "
            "<code>if lst</code> guard in the initial heap is what stops an "
            "<code>IndexError</code>, and it is easy to forget.",
        ],
    },
    check=[
        {"q": "How large does the heap get?",
         "options": ["N, the total number of values", "k, one per list",
                     "log k", "k squared"],
         "answer": 1,
         "why": "Only the head of each list can be the next output, so only k "
                "values are ever candidates."},
        {"q": "Why does each heap entry carry the list index?",
         "options": ["To sort the output",
                     "So the popped value can be replaced by its own list's successor",
                     "To count the lists",
                     "It does not need to"],
         "answer": 1,
         "why": "The replacement must come from the same list. Without the tag "
                "there is no way to know which list that is."},
        {"q": "What is heapq.merge's actual advantage over sorted(concatenation)?",
         "options": ["It is always faster",
                     "It is lazy - O(k) memory and the first value immediately",
                     "It handles unsorted input",
                     "It is stable and sorted is not"],
         "answer": 1,
         "why": "For full materialisation sorted() is usually faster in "
                "CPython. The win is memory and first-result latency."},
        {"q": "Where does the k-way merge get used in practice?",
         "options": ["Hash joins",
                     "External sorting: sorted chunks on disk merged back into one stream",
                     "Binary search",
                     "Graph traversal"],
         "answer": 1,
         "why": "It is the merge step whenever the data is too large for "
                "memory, which is also why the laziness matters."},
    ],
)


# =========================================================================
# 3. running median
# =========================================================================

def _median_frames():
    """Recorded by feeding a stream through the real two-heap structure."""
    low, high = [], []          # low is a max-heap (negated), high a min-heap

    def add(x):
        _heapq.heappush(low, -x)
        _heapq.heappush(high, -_heapq.heappop(low))
        if len(high) > len(low):
            _heapq.heappush(low, -_heapq.heappop(high))

    def median():
        if len(low) > len(high):
            return float(-low[0])
        return (-low[0] + high[0]) / 2

    out = []
    for x in (5, 2, 8, 1):
        add(x)
        lows = sorted((-v for v in low), reverse=True)
        highs = sorted(high)
        out.append(frame(
            [marked([str(v) for v in lows] or ["(empty)"],
                    {0: "lo"} if lows else {}, label="low half (max-heap)"),
             marked([str(v) for v in highs] or ["(empty)"],
                    {0: "hi"} if highs else {}, label="high half (min-heap)")],
            "After %d: the two heaps hold %d and %d values, and the median is "
            "%s - read off one or both roots, with no scan."
            % (x, len(low), len(high), median()),
            {"seen": len(low) + len(high), "median": median()}))
    out.append(frame(
        pairs([("insert", "O(log n)"), ("median", "O(1)"),
               ("invariant", "len(low) - len(high) is 0 or 1"),
               ("why it holds", "every add rebalances")],
              {"median": "hit"}, label="the cost"),
        "The roots are the two middle values, so the median is always one or "
        "two reads. Keeping the sizes within one of each other is what "
        "guarantees that.",
        {"seen": len(low) + len(high), "median": median()}))
    return viz(out)


_q(
    slug="running-median-of-a-stream",
    kind="coding",
    level="Hard",
    title="Find the median of a data stream",
    asked="Numbers arrive one at a time. Report the median after each one.",
    desc="Two heaps for a running median: a max-heap of the low half and a "
         "min-heap of the high half, with the roots as the middle values and "
         "the rebalance that keeps them there.",
    lead="Split the values in half: a <strong>max-heap of the lower "
         "half</strong> and a <strong>min-heap of the upper half</strong>. "
         "Their roots are the two middle values, so the median is one or two "
         "reads. Each insert pushes, moves one across and rebalances &mdash; "
         "O(log n) in, O(1) out.",
    say="\"Two heaps. A max-heap for the lower half, a min-heap for the upper "
        "half, kept within one element of each other in size. The median is "
        "the root of the larger heap, or the average of the two roots when "
        "they are equal. Insert is O(log n) and the median is O(1). Python "
        "only has a min-heap, so the low half stores negated values.\"",
    notice=[
        "The two roots are the middle of the data &mdash; that is the whole "
        "design.",
        "Every insert goes through both heaps, which is what keeps them "
        "balanced.",
        "The low half is negated, because <code>heapq</code> is a min-heap "
        "only.",
    ],
    viz=_median_frames(),
    sections=[
        ("Why two heaps and not one sorted list",
         "<p>A sorted list gives an O(1) median and an O(n) insert, because "
         "everything after the insertion point shifts. A single heap gives an "
         "O(log n) insert and no useful median at all &mdash; a heap knows its "
         "extreme, not its middle.</p>"
         "<p>Two heaps back to back give both. The largest of the small half "
         "and the smallest of the large half sit next to each other in sorted "
         "order, and both are heap roots. So the structure keeps exactly the "
         "two values you need at exactly the two positions a heap makes "
         "cheap.</p>"),
        ("The insert, and why it is three operations",
         "<p>The naive version &mdash; compare against a root and push to the "
         "appropriate side &mdash; is correct and has an awkward number of "
         "cases. The compact form has none:</p>"
         "<pre><code>heappush(low, -x)                      # always to the low side\n"
         "heappush(high, -heappop(low))          # move its largest across\n"
         "if len(high) &gt; len(low):\n"
         "    heappush(low, -heappop(high))      # rebalance</code></pre>"
         "<p>Pushing then immediately moving the largest guarantees the value "
         "lands on the correct side whatever it was, because the max-heap has "
         "already floated the biggest low value to the top. The third line "
         "keeps the sizes within one. Three heap operations, no branching on "
         "value, and it is the version worth memorising.</p>"),
        ("The negation, and what it costs",
         "<p><code>heapq</code> implements a min-heap only, so a max-heap is "
         "built by negating on the way in and again on the way out. It works "
         "for numbers and it is the standard trick.</p>"
         "<p>It does not work for anything that is not negatable &mdash; "
         "strings, tuples, objects. For those, either wrap each item in a class "
         "with a reversed <code>__lt__</code>, or push "
         "<code>(-priority, item)</code> when only the key needs reversing. "
         "Mentioning the limitation is worth doing, because the negation trick "
         "is the first thing that breaks when the question changes from "
         "integers to records.</p>"),
        ("The follow-ups",
         "<p><strong>\"What about a sliding window median?\"</strong> Harder, "
         "because values now leave as well as arrive and a heap cannot remove "
         "an arbitrary element. The standard answer is <em>lazy deletion</em>: "
         "keep a count of values due to be removed and discard them when they "
         "reach a root. The other answer is a structure built for it, like a "
         "sorted container with O(log n) insert and delete.</p>"
         "<p><strong>\"What if you only need an approximate median?\"</strong> "
         "Then this is overkill, and the real-world answer is a sketch &mdash; "
         "t-digest or a reservoir sample &mdash; which trades exactness for "
         "constant memory. Worth naming, because production percentile "
         "monitoring is built on those rather than on two heaps.</p>"),
    ],
    code={
        "file": "running_median.py",
        "intro": "The three-line insert, checked against statistics.median at "
                 "every step, then the cost against re-sorting the stream each "
                 "time it is queried.",
        "code": '''import heapq, random, statistics, time

class RunningMedian:
    def __init__(self):
        self.low = []      # max-heap, stored negated
        self.high = []     # min-heap

    def add(self, x):
        heapq.heappush(self.low, -x)                        # always push low
        heapq.heappush(self.high, -heapq.heappop(self.low)) # move its largest
        if len(self.high) > len(self.low):                  # rebalance
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2


random.seed(11)
stream = [random.randint(0, 1000) for _ in range(2_000)]

m = RunningMedian()
seen, ok = [], True
for i, x in enumerate(stream):
    m.add(x); seen.append(x)
    if abs(m.median() - statistics.median(seen)) > 1e-9:
        ok = False; print("MISMATCH at", i); break
print("matches statistics.median at every one of", len(stream), "steps:", ok)
print("invariant len(low) - len(high) in (0, 1):",
      len(m.low) - len(m.high) in (0, 1))
print("heap sizes:", len(m.low), len(m.high))

# Against re-sorting on every query.
def by_sorting(stream):
    out, data = [], []
    for x in stream:
        data.append(x); data.sort()
        n = len(data)
        out.append(float(data[n // 2]) if n % 2
                   else (data[n // 2 - 1] + data[n // 2]) / 2)
    return out

t0 = time.perf_counter()
heap_out, mm = [], RunningMedian()
for x in stream:
    mm.add(x); heap_out.append(mm.median())
a = time.perf_counter() - t0

t0 = time.perf_counter(); sort_out = by_sorting(stream); b = time.perf_counter() - t0
print()
print("same medians throughout:", heap_out == sort_out)
print(f"  two heaps          {a*1000:7.1f} ms   O(log n) per insert")
print(f"  re-sort each time  {b*1000:7.1f} ms   ({b/a:.0f}x slower)")

# The negation is the only reason this looks odd.
print()
print("low half holds:", sorted((-v for v in mm.low), reverse=True)[:5], "...")
print("high half holds:", sorted(mm.high)[:5], "...")
print("the two roots are the middle:", -mm.low[0], mm.high[0])
''',
        "walk": [
            ("heapq.heappush(self.low, -x)",
             "Every value goes to the low side first, whatever it is. That is "
             "what removes the case analysis."),
            ("heapq.heappush(self.high, -heapq.heappop(self.low))",
             "Immediately move the low half's largest across. Because the "
             "max-heap has floated the biggest value to the root, this "
             "guarantees the new value ends up on the correct side."),
            ("if len(self.high) > len(self.low)",
             "The rebalance. Without it the high half grows by one each "
             "insert and the roots stop being the middle."),
            ("(-self.low[0] + self.high[0]) / 2",
             "Two reads for an even count, one for an odd count. No scan, "
             "which is the O(1) being claimed."),
        ],
        "try": [
            "Remove the rebalance line and watch the medians drift. It fails "
            "silently rather than raising, which is why the check against "
            "<code>statistics.median</code> is in the code.",
            "Feed it a sorted stream instead of a random one. The heaps still "
            "balance, because the rebalance depends on sizes rather than on "
            "values.",
        ],
    },
    check=[
        {"q": "What do the two heap roots represent?",
         "options": ["The minimum and maximum",
                     "The two middle values of the data seen so far",
                     "The first and last inserted",
                     "The mean and the mode"],
         "answer": 1,
         "why": "The largest of the low half and the smallest of the high "
                "half are adjacent in sorted order - the middle."},
        {"q": "Why push to the low heap and immediately move its largest across?",
         "options": ["To save memory",
                     "It puts the value on the correct side without any case analysis",
                     "heapq requires it",
                     "To keep the heaps sorted"],
         "answer": 1,
         "why": "The max-heap floats the biggest low value to the root, so "
                "moving it across is always the right transfer."},
        {"q": "Why is the low half stored negated?",
         "options": ["To save space",
                     "Because heapq is a min-heap only, so negation makes it behave as a max-heap",
                     "To handle negative inputs",
                     "For stability"],
         "answer": 1,
         "why": "Python has no max-heap. Negating on the way in and out is the "
                "standard workaround, and it only works for negatable values."},
        {"q": "What are the costs?",
         "options": ["O(1) insert, O(log n) median",
                     "O(log n) insert, O(1) median",
                     "O(n) insert, O(1) median",
                     "O(log n) for both"],
         "answer": 1,
         "why": "Three heap operations per insert, and the median is one or "
                "two root reads."},
    ],
)
