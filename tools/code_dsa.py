# -*- coding: utf-8 -*-
"""The Python program that sits under each dsa/ article.

tools/build_dsa_code.py drops these into the page inside the same editor
/python-lab/ runs, so every one of them is executed by real CPython in the
reader's own browser. That constrains what can be written here, and the
constraints are the useful part:

  * it has to actually run, unchanged, in about a second - no `input()`, no
    files, no network, no packages outside the standard library;
  * it has to print its own trace, because a program that silently returns the
    right answer teaches nothing that the article did not already say;
  * it has to be the algorithm rather than a call to the standard library.
    `sorted(a)` is the right answer in real code and the wrong one here.

Each entry carries:

  file    the tab name on the editor - `binary_search.py`, not `main.py`
  intro   one or two sentences on what pressing Run will show
  code    the program itself, raw (it lands inside <script type="text/plain">)
  walk    (line, explanation) pairs - the line is quoted verbatim from the
          program above so the reader can find it, and the explanation says
          why it is that way rather than restating it
  try     edits worth making, phrased as an instruction with a prediction

A module earns an editor when running the code teaches something the picture
cannot. On this track that turned out to be all forty-one module pages, Big-O
included - the notation page gets a program that counts operations rather than
one that implements anything. The track index has no editor because it explains
nothing to run.
"""

# =========================================================================
# Searching
# =========================================================================

SEARCHING = {

"dsa/linear_search.html": {
    "file": "linear_search.py",
    "intro": "Three searches through the same ten-item list &mdash; one that hits "
             "immediately, one that has to walk the whole way, and one for a value "
             "that is not there at all. The last line counts the average rather "
             "than asserting it.",
    "code": '''# Linear search: check each item in turn until you find the target.
# No assumptions about the data at all - which is the whole point.

def linear_search(a, target):
    for i, value in enumerate(a):
        hit = "yes" if value == target else "no"
        print(f"  index {i:>2}: is {value:>3} == {target}?  {hit}")
        if value == target:
            return i
    return -1


data = [38, 12, 91, 5, 56, 23, 72, 8, 16, 2]

for target in (38, 2, 40):
    print(f"searching for {target} in {len(data)} items")
    i = linear_search(data, target)
    print("  ->", f"found at index {i}" if i != -1 else "not present")
    print()

# The average is not a claim; it is counted over every value in the list.
comparisons = [data.index(x) + 1 for x in data]
print("comparisons per value :", comparisons)
print("average               :", sum(comparisons) / len(data))
print("(n + 1) / 2           :", (len(data) + 1) / 2)
''',
    "walk": [
        ("for i, value in enumerate(a):",
         "The entire algorithm is this loop. There is no precondition to check "
         "and no structure to maintain, which is why linear search works on "
         "anything you can iterate."),
        ("if value == target: return i",
         "Returning inside the loop is what makes the best case O(1). A version "
         "that records the index and keeps going would always cost n."),
        ("return -1",
         "Reached only after every item failed. A miss always costs the full n "
         "&mdash; the worst case and the not-found case are the same case."),
        ("comparisons = [data.index(x) + 1 for x in data]",
         "For each value, how many comparisons finding it took. Averaged, this "
         "lands on (n + 1) / 2: half the list, which is where the usual "
         "“half the array on average” figure comes from."),
    ],
    "try": [
        "Move <code>2</code> to the front of <code>data</code>. The average "
        "does not change &mdash; you made one search cheaper and nine dearer.",
        "Search for a value in a list of one million: replace <code>data</code> "
        "with <code>list(range(1_000_000))</code> and comment out the "
        "<code>print</code> inside the loop. Then compare that with "
        "<a href=\"binary_search.html\">binary search</a> on the same list.",
        "Change the loop to <code>for value in a:</code> and return "
        "<code>True</code>/<code>False</code>. That is what Python's "
        "<code>in</code> operator does on a list, and it is why <code>x in "
        "big_list</code> is slow while <code>x in big_set</code> is not.",
    ],
},

"dsa/binary_search.html": {
    "file": "binary_search.py",
    "intro": "The whole algorithm is nine lines, and it prints the window "
             "<code>[lo, hi]</code> at every step so you can watch it collapse. "
             "The last block searches a million items to show what "
             "O(log n) buys.",
    "code": '''# Binary search. Precondition: the list is SORTED.
import math

def binary_search(a, target):
    lo, hi = 0, len(a) - 1          # inclusive window of candidates
    step = 0
    while lo <= hi:                 # <= : a one-item window still needs checking
        mid = lo + (hi - lo) // 2   # not (lo + hi) // 2 - see the walkthrough
        step += 1
        print(f"step {step}: lo={lo:>2} hi={hi:>2} mid={mid:>2} a[mid]={a[mid]:>3}")
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1            # everything left of mid is too small
        else:
            hi = mid - 1            # everything right of mid is too large
    return -1


data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print("array :", data)
print("target: 23")
print("index :", binary_search(data, 23))

print()
print("target: 7  (not present)")
print("index :", binary_search(data, 7))

print()
big = list(range(1_000_000))
print("searching 1,000,000 items for 999_999")
found = binary_search(big, 999_999)
print("index :", found)
print("worst case, in theory:", math.ceil(math.log2(len(big) + 1)), "comparisons")
''',
    "walk": [
        ("lo, hi = 0, len(a) - 1",
         "The window is inclusive at both ends, so index <code>hi</code> is still "
         "a candidate. The other convention &mdash; <code>hi = len(a)</code>, "
         "exclusive &mdash; is equally correct, and mixing the two is where most "
         "binary search bugs come from."),
        ("while lo <= hi:",
         "Follows from the window being inclusive. With <code>&lt;</code> instead, "
         "a window that has narrowed to a single item is never examined, and a "
         "search for the last remaining candidate returns -1."),
        ("mid = lo + (hi - lo) // 2",
         "Arithmetically the same as <code>(lo + hi) // 2</code>, but that form "
         "overflows once <code>lo + hi</code> exceeds the integer width. Python's "
         "ints are unbounded so it cannot bite here; in Java it sat undetected in "
         "the JDK for nine years."),
        ("lo = mid + 1",
         "The <code>+ 1</code> is load-bearing. <code>mid</code> has just been "
         "compared and ruled out, and leaving it inside the window means a "
         "two-item window can stop shrinking &mdash; an infinite loop rather than "
         "a wrong answer."),
        ("return -1",
         "The loop ends when <code>lo</code> passes <code>hi</code>, i.e. the "
         "window is empty. A failed search costs exactly as much as a successful "
         "one, unlike linear search where failure is always the worst case."),
    ],
    "try": [
        "Break the precondition: add <code>data.reverse()</code> before the "
        "search. It does not raise &mdash; it quietly returns the wrong answer, "
        "which is the failure mode to be afraid of.",
        "Change <code>hi = mid - 1</code> to <code>hi = mid</code> and run it. "
        "The window stops shrinking and the interpreter is killed after ten "
        "seconds. That is the off-by-one, seen from the inside.",
        "Count the steps for <code>2</code>, for <code>91</code> and for "
        "<code>16</code>. The middle element is found instantly and both ends "
        "cost the full log n &mdash; the exact inverse of linear search.",
    ],
},

"dsa/interpolation_search.html": {
    "file": "interpolation_search.py",
    "intro": "The same list searched twice: once evenly spaced, where guessing "
             "the position beats halving it, and once with a single outlier, "
             "where the same code degenerates to a linear scan.",
    "code": '''# Interpolation search: estimate WHERE the target should be, instead of
# always probing the middle. Needs sorted AND roughly uniform data.

def interpolation_search(a, target, label):
    print(label)
    lo, hi, step = 0, len(a) - 1, 0
    while lo <= hi and a[lo] <= target <= a[hi]:
        step += 1
        if a[hi] == a[lo]:                       # flat span: no slope to follow
            pos = lo
        else:
            fraction = (target - a[lo]) / (a[hi] - a[lo])
            pos = lo + int(fraction * (hi - lo))
        print(f"  step {step:>2}: lo={lo:>2} hi={hi:>2} probe={pos:>2} a[probe]={a[pos]}")
        if a[pos] == target:
            return pos, step
        if a[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1, step


uniform = list(range(0, 200, 10))       # 0, 10, 20, ... perfectly even
i, steps = interpolation_search(uniform, 170, "uniform data, target 170")
print(f"  -> index {i} in {steps} step(s)")

print()
skewed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 5000]      # one huge outlier
i, steps = interpolation_search(skewed, 9, "skewed data, target 9")
print(f"  -> index {i} in {steps} step(s)")
print()
print("Same code, same length, same sortedness. Only the spacing changed.")
''',
    "walk": [
        ("while lo <= hi and a[lo] <= target <= a[hi]:",
         "The second half of the condition is an early exit binary search does "
         "not have: if the target is outside the current window's value range, "
         "no probe inside it can succeed."),
        ("fraction = (target - a[lo]) / (a[hi] - a[lo])",
         "How far along the window the target's <em>value</em> sits, between 0 "
         "and 1. Binary search always uses 0.5 here; this is the one line that "
         "makes the two algorithms different."),
        ("pos = lo + int(fraction * (hi - lo))",
         "Turns that value fraction into an index, on the assumption that value "
         "and position rise together at a steady rate. When they do, the probe "
         "lands on or beside the answer immediately."),
        ("if a[hi] == a[lo]: pos = lo",
         "Guards a division by zero when every value in the window is equal. "
         "Reaching for a fraction of a zero-width value range is the crash this "
         "algorithm is famous for."),
        ("skewed = [1, 2, ..., 5000]",
         "The outlier drags <code>a[hi]</code> so high that the computed "
         "fraction is nearly zero every time, so the probe advances one index "
         "per step. Interpolation search is O(log log n) on uniform data and "
         "O(n) on data like this."),
    ],
    "try": [
        "Change the uniform target to <code>0</code> and to <code>190</code>. "
        "Both ends are found in a step or two, where binary search needs its "
        "full log n.",
        "Replace <code>uniform</code> with <code>[i * i for i in range(20)]</code> "
        "&mdash; sorted, but quadratically spaced. Watch the probe consistently "
        "undershoot.",
        "Set <code>fraction = 0.5</code> unconditionally. You have just written "
        "binary search, and on the skewed list it beats the clever version.",
    ],
},

"dsa/fibonacci_search.html": {
    "file": "fibonacci_search.py",
    "intro": "Binary search's split points come from a division. These come from "
             "the Fibonacci sequence, so the whole search runs on addition and "
             "subtraction &mdash; the reason it exists.",
    "code": '''# Fibonacci search: divide the array at Fibonacci offsets rather than in
# half. No division, no multiplication - only + and -.

def fibonacci_search(a, target):
    n = len(a)

    f2, f1 = 0, 1
    fib = f2 + f1
    while fib < n:                     # smallest Fibonacci number >= n
        f2, f1 = f1, fib
        fib = f2 + f1
    print(f"array of {n}; smallest Fibonacci number >= n is {fib}")

    offset, step = -1, 0
    while fib > 1:
        step += 1
        i = min(offset + f2, n - 1)    # clamp: the array may be shorter than fib
        print(f"  step {step}: probe={i:>2} a[probe]={a[i]:>3} (fib={fib}, f2={f2})")
        if a[i] < target:
            fib, f1, f2 = f1, f2, f1 - f2      # cut off the left part
            offset = i
        elif a[i] > target:
            fib, f1, f2 = f2, f1 - f2, f2 - (f1 - f2)   # cut off the right part
        else:
            return i
    if f1 and a[offset + 1] == target:         # one candidate left
        return offset + 1
    return -1


data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91, 96]
print("array:", data)
print()
for target in (72, 2, 40):
    print("target", target)
    print("  -> index", fibonacci_search(data, target))
    print()
''',
    "walk": [
        ("while fib < n: f2, f1 = f1, fib; fib = f2 + f1",
         "Walks up the sequence 1, 2, 3, 5, 8, 13 ... until it covers the array. "
         "Everything afterwards walks back <em>down</em> the same sequence, which "
         "is why no arithmetic beyond addition is ever needed."),
        ("i = min(offset + f2, n - 1)",
         "The probe sits <code>f2</code> past the part already ruled out. The "
         "clamp handles the array being shorter than the Fibonacci number that "
         "covers it &mdash; the sequence overshoots by design."),
        ("fib, f1, f2 = f1, f2, f1 - f2",
         "The target is to the right, so the search moves one place down the "
         "sequence and <code>offset</code> remembers the discarded prefix. Three "
         "subtractions, no division."),
        ("fib, f1, f2 = f2, f1 - f2, f2 - (f1 - f2)",
         "The target is to the left, so the window shrinks by two places instead "
         "of one. The uneven split is why Fibonacci search is not simply binary "
         "search with extra steps &mdash; it is deliberately lopsided."),
        ("if f1 and a[offset + 1] == target:",
         "When <code>fib</code> reaches 1 there is at most one unchecked element "
         "left. Dropping this check loses exactly one array position, which is a "
         "classic way to get an almost-correct implementation."),
    ],
    "try": [
        "Print <code>len(data)</code> against the number of steps for several "
        "targets. It tracks log n, same as binary search &mdash; the win was "
        "never in the step count.",
        "Add an eleventh element and re-run. The first Fibonacci number covering "
        "the array jumps, and the probe pattern changes completely.",
        "Search for a value that is not in the list. Follow how "
        "<code>offset</code> and <code>fib</code> converge until the loop "
        "condition fails.",
    ],
},

}


# =========================================================================
# Sorting
# =========================================================================

SORTING = {

"dsa/bubble_sort.html": {
    "file": "bubble_sort.py",
    "intro": "One line printed per pass, so you can watch the largest value "
             "reach the end of the list on pass one and stay there. The second "
             "run shows what the early exit is worth.",
    "code": '''# Bubble sort: repeatedly swap adjacent items that are out of order.

def bubble_sort(a):
    a = a[:]                       # copy, so the original stays printable
    n = len(a)
    passes = swaps = 0
    for i in range(n - 1):
        passes += 1
        swapped = False
        for j in range(n - 1 - i):     # the last i items are already final
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        print(f"pass {passes}: {a}")
        if not swapped:                # a clean pass means it is sorted
            break
    return a, passes, swaps


data = [5, 1, 4, 2, 8, 0, 2]
print("start :", data)
out, passes, swaps = bubble_sort(data)
print("sorted:", out)
print(f"{passes} passes, {swaps} swaps")

print()
print("already sorted:")
_, p, s = bubble_sort([0, 1, 2, 4, 5, 8])
print(f"{p} pass, {s} swaps - the early exit makes the best case O(n)")

print()
print("reversed (the worst case):")
_, p, s = bubble_sort([8, 5, 4, 2, 1, 0])
print(f"{p} passes, {s} swaps")
''',
    "walk": [
        ("for j in range(n - 1 - i):",
         "The <code>- i</code> is the optimisation that makes bubble sort worth "
         "writing. After pass <em>i</em> the last <em>i</em> items are in final "
         "position, so re-scanning them is pure waste."),
        ("a[j], a[j + 1] = a[j + 1], a[j]",
         "Python's tuple assignment evaluates the right side first, so this is a "
         "genuine swap. In most languages it needs a temporary variable, and "
         "forgetting it overwrites one of the two values."),
        ("if not swapped: break",
         "A whole pass with nothing out of order proves the list is sorted. This "
         "single flag turns the best case from O(n²) into O(n) &mdash; and it "
         "is the only reason bubble sort beats selection sort on nearly-sorted "
         "input."),
        ("swaps",
         "The swap count equals the number of inversions in the input, exactly. "
         "That is a real property, not an approximation: each swap fixes one "
         "inverted pair and no more."),
    ],
    "try": [
        "Sort <code>[1, 2, 3, 4, 5, 0]</code>. One small value at the wrong end "
        "costs a full n passes &mdash; bubble sort moves items left one position "
        "per pass, and that is its real weakness.",
        "Delete <code>- i</code> from the inner range. The result stays correct "
        "and the swap count is unchanged; only the wasted comparisons go up.",
        "Change <code>&gt;</code> to <code>&gt;=</code>. Still sorted, but equal "
        "items now get swapped &mdash; the sort is no longer stable.",
    ],
},

"dsa/selection_sort.html": {
    "file": "selection_sort.py",
    "intro": "Selection sort's defining trait is that it makes exactly n &minus; 1 "
             "swaps no matter what you feed it. The program counts both "
             "comparisons and swaps so you can see one stay fixed while the "
             "other does not.",
    "code": '''# Selection sort: find the smallest remaining item, put it in place, repeat.

def selection_sort(a, show=True):
    a = a[:]
    n = len(a)
    comparisons = swaps = 0
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):        # scan the unsorted tail
            comparisons += 1
            if a[j] < a[smallest]:
                smallest = j
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
            swaps += 1
        if show:
            print(f"i={i}: picked {a[i]:>3}  ->  {a}")
    return a, comparisons, swaps


data = [64, 25, 12, 22, 11, 90]
print("start :", data)
out, c, s = selection_sort(data)
print("sorted:", out)
print(f"{c} comparisons, {s} swaps")

print()
for name, sample in [("sorted", [1, 2, 3, 4, 5, 6]),
                     ("reversed", [6, 5, 4, 3, 2, 1]),
                     ("random", [3, 6, 1, 5, 2, 4])]:
    _, c, s = selection_sort(sample, show=False)
    print(f"{name:>9}: {c} comparisons, {s} swaps")
print()
print("The comparison count never moves. That is selection sort.")
''',
    "walk": [
        ("smallest = i",
         "Assume the first unsorted item is the minimum, then try to disprove it. "
         "Tracking the <em>index</em> rather than the value is what lets the swap "
         "at the end be a single operation."),
        ("for j in range(i + 1, n):",
         "The scan always covers the entire unsorted tail, with no early exit "
         "available &mdash; you cannot know something is the minimum without "
         "looking at everything. Hence n(n&minus;1)/2 comparisons, always."),
        ("if smallest != i:",
         "Skips the swap when the item is already where it belongs. It saves a "
         "write, not a comparison, so it does not change the complexity."),
        ("swaps",
         "At most n &minus; 1 swaps for any input. Where a write is expensive "
         "&mdash; flash memory, or records far larger than the key &mdash; that "
         "is a real advantage over bubble or insertion sort."),
    ],
    "try": [
        "Feed it an already sorted list. The comparison count is identical to "
        "the reversed case: selection sort cannot detect that it has no work "
        "to do.",
        "Track the largest instead of the smallest and fill from the right. Same "
        "algorithm, mirrored &mdash; and a good check that you have followed it.",
        "Sort <code>[2, 2, 1]</code> and follow the two 2s. Their order flips, "
        "which is why selection sort is not stable while insertion sort is.",
    ],
},

"dsa/insertion_sort.html": {
    "file": "insertion_sort.py",
    "intro": "The sorted region grows from the left and each new item is shifted "
             "back into place. The printout marks the boundary with "
             "<code>|</code>, and the last section shows why real sort "
             "implementations switch to this one for small inputs.",
    "code": '''# Insertion sort: keep a sorted prefix, and insert each next item into it.

def insertion_sort(a, show=True):
    a = a[:]
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:     # slide bigger items one place right
            a[j + 1] = a[j]
            shifts += 1
            j -= 1
        a[j + 1] = key                   # the hole left behind is where key goes
        if show:
            front = " ".join(f"{x:>2}" for x in a[:i + 1])
            back = " ".join(f"{x:>2}" for x in a[i + 1:])
            print(f"insert {key:>2}: {front} | {back}")
    return a, shifts


data = [12, 11, 13, 5, 6]
print("start :", data)
out, shifts = insertion_sort(data)
print("sorted:", out, f"({shifts} shifts)")

print()
for name, sample in [("sorted", [1, 2, 3, 4, 5, 6, 7, 8]),
                     ("nearly sorted", [1, 2, 4, 3, 5, 6, 8, 7]),
                     ("reversed", [8, 7, 6, 5, 4, 3, 2, 1])]:
    _, s = insertion_sort(sample, show=False)
    print(f"{name:>14}: {s} shifts")
print()
print("Cost tracks disorder, not size. CPython's own sort exploits exactly this.")
''',
    "walk": [
        ("key = a[i]",
         "The item is copied out first, which frees its slot. Everything after "
         "this is shifting items into the hole and finally dropping "
         "<code>key</code> into wherever the hole ended up."),
        ("while j >= 0 and a[j] > key:",
         "Two exits: running off the front, or meeting something that is not "
         "bigger. The second is the early exit that makes an already sorted "
         "input cost O(n) &mdash; the condition fails at once, every time."),
        ("a[j + 1] = a[j]",
         "A shift, not a swap. One write per displaced item rather than three, "
         "which is why insertion sort beats bubble sort in practice even though "
         "they share a complexity class."),
        ("a[j + 1] = key",
         "The <code>+ 1</code> undoes the last <code>j -= 1</code> of the loop. "
         "Getting this index wrong is the single most common bug in this "
         "algorithm."),
        ("shifts",
         "The shift count is the number of inversions in the input. That is why "
         "“nearly sorted” is not a vague description here &mdash; it is a "
         "measurable quantity, and it is exactly what this sort charges you for."),
    ],
    "try": [
        "Run it on a list of 20 random numbers, then on the same list sorted. "
        "The shift count collapses; no O(n²) sort should be able to do that.",
        "Replace the shifting loop with repeated swaps. Same output, three times "
        "the writes &mdash; and now you have written bubble sort inside out.",
        "Binary-search for the insertion point instead of scanning. Comparisons "
        "drop to O(n log n); the shifts, and therefore the running time, do not "
        "move at all.",
    ],
},

"dsa/merge_sort.html": {
    "file": "merge_sort.py",
    "intro": "The recursion prints its own indentation, so the split-then-merge "
             "shape is visible in the output. The merge step is where the sorting "
             "actually happens &mdash; splitting a list in half does no work at all.",
    "code": '''# Merge sort: split until the pieces are trivially sorted, then merge.

def merge(left, right, key):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):   # <= keeps equal items in order
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])             # one side is empty; drain the other
    out.extend(right[j:])
    return out


def merge_sort(a, key=lambda x: x, depth=0, show=True):
    pad = "  " * depth
    if len(a) <= 1:                  # a single item is already sorted
        if show:
            print(f"{pad}{a}  (base case)")
        return a
    mid = len(a) // 2
    if show:
        print(f"{pad}split {a} -> {a[:mid]} + {a[mid:]}")
    left = merge_sort(a[:mid], key, depth + 1, show)
    right = merge_sort(a[mid:], key, depth + 1, show)
    out = merge(left, right, key)
    if show:
        print(f"{pad}merge {left} + {right} -> {out}")
    return out


data = [38, 27, 43, 3, 9, 82, 10]
print("start :", data)
print()
result = merge_sort(data)
print()
print("sorted:", result)

# Stability, run through this same code rather than asserted.
pairs = [("b", 2), ("a", 1), ("c", 2), ("d", 1)]
print()
print("by number:", merge_sort(pairs, key=lambda p: p[1], show=False))
print("a before d, b before c - ties kept the order they arrived in")
''',
    "walk": [
        ("if len(a) <= 1: return a",
         "The base case. A list of one is sorted by definition, and every branch "
         "of the recursion bottoms out here &mdash; which is why merge sort needs "
         "no explicit termination check."),
        ("mid = len(a) // 2",
         "The split is positional and costs nothing to choose. Contrast quicksort, "
         "where choosing the split point <em>is</em> the algorithm and a bad "
         "choice costs O(n²)."),
        ("while i < len(left) and j < len(right):",
         "Both halves are already sorted, so the next smallest item overall is "
         "always at the front of one of them. That single fact is why merging is "
         "linear."),
        ("if left[i] <= right[j]:",
         "The <code>&lt;=</code> is what makes merge sort stable: on a tie the "
         "left half wins, and the left half held the earlier items. Change it to "
         "<code>&lt;</code> and stability is gone, silently."),
        ("out.extend(left[i:]); out.extend(right[j:])",
         "When one side runs out the other is already sorted and every item in it "
         "is larger, so it can be appended wholesale. One of these two lines is "
         "always a no-op."),
    ],
    "try": [
        "Change <code>&lt;=</code> to <code>&lt;</code> in <code>merge</code>, "
        "then sort a list with duplicates and watch stability break.",
        "Count the merge lines the program prints. It is about n log n for any "
        "input &mdash; merge sort has no best case, and no worst case either.",
        "Replace the slices with index ranges into one shared list. That removes "
        "the O(n) copies, and shows why the classic implementation needs O(n) "
        "extra space.",
    ],
},

"dsa/quick_sort.html": {
    "file": "quick_sort.py",
    "intro": "Lomuto partitioning, printed at each level, followed by the case "
             "everyone warns about: a sorted input with a last-element pivot, "
             "counted to show the recursion depth going linear.",
    "code": '''# Quicksort: partition around a pivot, then sort the two sides.
import sys

def partition(a, lo, hi):
    pivot = a[hi]                    # Lomuto: the last item is the pivot
    i = lo - 1                       # end of the "smaller than pivot" region
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]    # drop the pivot into its final place
    return i + 1


def quicksort(a, lo=0, hi=None, depth=0, stats=None, show=True):
    if hi is None:
        hi = len(a) - 1
    if stats is not None:
        stats["depth"] = max(stats["depth"], depth)
        stats["calls"] += 1
    if lo >= hi:
        return
    p = partition(a, lo, hi)
    if show:
        print(f"{'  ' * depth}pivot {a[p]:>3} -> {a[lo:p]} [{a[p]}] {a[p+1:hi+1]}")
    quicksort(a, lo, p - 1, depth + 1, stats, show)
    quicksort(a, p + 1, hi, depth + 1, stats, show)


data = [10, 80, 30, 90, 40, 50, 70]
print("start :", data)
quicksort(data)
print("sorted:", data)

print()
sys.setrecursionlimit(10000)
for name, sample in [("random", [5, 2, 8, 1, 9, 3, 7, 4, 6]),
                     ("already sorted", list(range(1, 10)))]:
    stats = {"depth": 0, "calls": 0}
    quicksort(sample[:], stats=stats, show=False)
    print(f"{name:>15}: depth {stats['depth']:>2}, {stats['calls']} calls")
print()
print("Sorted input is quicksort's worst case, not its best.")
''',
    "walk": [
        ("pivot = a[hi]",
         "The choice that decides everything. Taking the last element is simple "
         "and is exactly why sorted input degrades to O(n²) &mdash; every "
         "partition peels off one item instead of splitting in half."),
        ("i = lo - 1",
         "<code>i</code> marks the end of the region known to be &le; the pivot. "
         "Starting one before <code>lo</code> means that region is empty, which "
         "is true before anything has been examined."),
        ("if a[j] <= pivot: i += 1; swap",
         "Grow the small region by one slot and move the qualifying item into it. "
         "Everything between <code>i</code> and <code>j</code> is known to be "
         "larger than the pivot &mdash; that invariant is the whole partition."),
        ("a[i + 1], a[hi] = a[hi], a[i + 1]",
         "Puts the pivot in the gap between the two regions. It is now in its "
         "final sorted position and is never moved again, which is why the "
         "recursive calls skip index <code>p</code>."),
        ("quicksort(a, lo, p - 1); quicksort(a, p + 1, hi)",
         "Sorting happens in place with no merge step. That is quicksort's real "
         "advantage over merge sort &mdash; not speed on paper, but O(log n) "
         "extra space instead of O(n)."),
    ],
    "try": [
        "Swap in a middle pivot: <code>a[(lo + hi) // 2], a[hi] = a[hi], a[(lo + "
        "hi) // 2]</code> at the top of <code>partition</code>. The sorted-input "
        "depth collapses from n to log n.",
        "Sort a list where every value is identical. Lomuto sends all of it to "
        "one side &mdash; the degenerate case that three-way partitioning exists "
        "to fix.",
        "Raise the sorted sample to <code>range(1, 2000)</code> and run it. The "
        "recursion limit, not the running time, is what stops you.",
    ],
},

"dsa/heap_sort.html": {
    "file": "heap_sort.py",
    "intro": "Two phases, printed separately: build a max-heap out of the raw "
             "list, then repeatedly move the root to the end. Nothing is "
             "allocated &mdash; the heap and the sorted output share one list.",
    "code": '''# Heap sort: build a max-heap in place, then pull the maximum out n times.

def sift_down(a, root, end):
    """Push a[root] down until the subtree below it is a valid max-heap."""
    while True:
        child = 2 * root + 1              # left child
        if child >= end:
            return
        if child + 1 < end and a[child + 1] > a[child]:
            child += 1                    # take the larger of the two children
        if a[root] >= a[child]:
            return                        # heap property already holds
        a[root], a[child] = a[child], a[root]
        root = child


def heap_sort(a):
    a = a[:]
    n = len(a)

    # Phase 1 - heapify. Leaves are heaps already, so start at the last parent.
    for start in range(n // 2 - 1, -1, -1):
        sift_down(a, start, n)
        print(f"heapify from {start}: {a}")

    # Phase 2 - repeatedly swap the root to the end and shrink the heap.
    print()
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)
        print(f"place {a[end]:>3} at index {end}: heap={a[:end]} sorted={a[end:]}")
    return a


data = [4, 10, 3, 5, 1, 8, 2]
print("start :", data)
print()
print("sorted:", heap_sort(data))
''',
    "walk": [
        ("child = 2 * root + 1",
         "The tree is only an idea &mdash; the list <em>is</em> the tree. Node "
         "<code>i</code>'s children are at <code>2i+1</code> and "
         "<code>2i+2</code>, so no pointers, and no node objects, are needed."),
        ("if a[root] >= a[child]: return",
         "The early exit. A sift stops as soon as the heap property holds, which "
         "is what keeps each one at O(log n) rather than always walking to a leaf."),
        ("for start in range(n // 2 - 1, -1, -1):",
         "Everything past <code>n // 2 - 1</code> is a leaf, and a leaf is a valid "
         "heap on its own. Building bottom-up like this is O(n) &mdash; not "
         "O(n log n), which is the surprising part."),
        ("a[0], a[end] = a[end], a[0]",
         "The root is the largest remaining value, so it belongs at the end of "
         "the unsorted region. One swap both extracts it and puts it in final "
         "position."),
        ("sift_down(a, 0, end)",
         "<code>end</code> shrinks each round, so the same list holds a shrinking "
         "heap on the left and a growing sorted run on the right. That is why "
         "heap sort needs O(1) extra space."),
    ],
    "try": [
        "Print <code>a</code> after phase 1 only. It is not sorted &mdash; a heap "
        "is a much weaker ordering than a sorted list, and that weakness is what "
        "makes it cheap to build.",
        "Flip both comparisons in <code>sift_down</code> to build a min-heap. The "
        "output comes out descending.",
        "Sort <code>[3, 1, 3]</code> and follow the two 3s. They swap order "
        "&mdash; heap sort is not stable, unlike merge sort.",
    ],
},

"dsa/counting_sort.html": {
    "file": "counting_sort.py",
    "intro": "No comparison between two elements appears anywhere in this program. "
             "It sorts by counting, which is how it beats the O(n log n) bound "
             "&mdash; and the last block shows what that costs when the value "
             "range is large.",
    "code": '''# Counting sort: count how many of each value there are, then rebuild.
# Not a comparison sort - it never asks "is x < y?" at all.

def counting_sort(a):
    if not a:
        return []
    lo, hi = min(a), max(a)
    k = hi - lo + 1
    print(f"n = {len(a)}, value range k = {k}  ({lo}..{hi})")

    counts = [0] * k
    for value in a:
        counts[value - lo] += 1
    # Only worth printing while it fits on a line - see the second example.
    print("counts   :", counts if k <= 20 else f"<{k} counters, {len(a)} non-zero>")

    # Running total: counts[i] becomes "how many items are <= i".
    for i in range(1, k):
        counts[i] += counts[i - 1]
    print("prefix   :", counts if k <= 20 else f"<{k} counters, summed in order>")

    out = [None] * len(a)
    for value in reversed(a):            # reversed keeps the sort stable
        counts[value - lo] -= 1
        out[counts[value - lo]] = value
    return out


data = [4, 2, 2, 8, 3, 3, 1]
print("start :", data)
print("sorted:", counting_sort(data))

print()
print("Now the same algorithm on a wide range:")
wide = [5, 100_000, 3]
print("start :", wide)
print("sorted:", counting_sort(wide))
print()
print("Three items, a hundred thousand counters, and a pass over every one of")
print("them. O(n + k) is only a win when k behaves.")
''',
    "walk": [
        ("counts[value - lo] += 1",
         "The value itself is the index. That is the trick, and it is also the "
         "restriction: this only works for keys that can be used as array "
         "offsets."),
        ("for i in range(1, k): counts[i] += counts[i - 1]",
         "Turns counts into positions. After this, <code>counts[v]</code> is the "
         "number of items less than or equal to <em>v</em> &mdash; which is "
         "exactly where the last <em>v</em> belongs in the output."),
        ("for value in reversed(a):",
         "Walking backwards, combined with decrementing before writing, keeps "
         "equal items in their original order. Iterate forwards and the sort "
         "still works but is no longer stable &mdash; which would break radix "
         "sort, its main customer."),
        ("out[counts[value - lo]] = value",
         "Each item is placed directly at its final index. No item is ever "
         "compared with another, so the O(n log n) lower bound for comparison "
         "sorts simply does not apply."),
        ("k = hi - lo + 1",
         "The whole cost story. O(n + k) is linear when k is comparable to n, and "
         "a disaster when it is not &mdash; as the three-item example shows."),
    ],
    "try": [
        "Sort exam marks: <code>[random.randint(0, 100) for _ in range(50)]</code>. "
        "Fifty items, 101 counters &mdash; this is the shape counting sort is for.",
        "Iterate forwards instead of <code>reversed(a)</code>, and sort "
        "<code>(value, tag)</code> pairs by value. Watch the tags come out in the "
        "wrong order.",
        "Remove the <code>- lo</code> offset and sort a list with negative "
        "numbers. The <code>IndexError</code> is why the offset is there.",
    ],
},

"dsa/radix_sort.html": {
    "file": "radix_sort.py",
    "intro": "Sorted one digit at a time, least significant first, with the whole "
             "list printed after each pass. It looks wrong until the final digit "
             "goes through &mdash; which is the thing worth understanding here.",
    "code": '''# Radix sort (LSD): sort by the ones digit, then the tens, then the hundreds.
# Each pass MUST be stable, or the work of the previous pass is destroyed.

def counting_sort_by_digit(a, place):
    counts = [0] * 10
    for value in a:
        counts[(value // place) % 10] += 1
    for i in range(1, 10):
        counts[i] += counts[i - 1]

    out = [0] * len(a)
    for value in reversed(a):            # reversed => stable
        digit = (value // place) % 10
        counts[digit] -= 1
        out[counts[digit]] = value
    return out


def radix_sort(a):
    a = a[:]
    place = 1
    while max(a) // place > 0:
        a = counting_sort_by_digit(a, place)
        name = {1: "ones", 10: "tens", 100: "hundreds", 1000: "thousands"}[place]
        print(f"after {name:>9} digit: {a}")
        place *= 10
    return a


data = [170, 45, 75, 90, 802, 24, 2, 66]
print("start :", data)
print()
print("sorted:", radix_sort(data))

print()
digits = len(str(max(data)))
print(f"{len(data)} items, {digits} digits -> {digits} passes over the list.")
print("Cost is O(d * n): the number of DIGITS, not the number of items.")
''',
    "walk": [
        ("(value // place) % 10",
         "Extracts one digit: divide the smaller places away, then take the "
         "remainder. Changing 10 here changes the base, and the base is the one "
         "real tuning knob radix sort has."),
        ("for value in reversed(a):",
         "Stability is not a nicety here, it is a correctness requirement. Each "
         "pass must preserve the order the previous pass established, or sorting "
         "by tens throws away the ones ordering entirely."),
        ("while max(a) // place > 0:",
         "One pass per digit of the largest value. Nothing depends on how many "
         "items there are, which is why radix sort is O(d &middot; n)."),
        ("place *= 10",
         "Least significant digit first. It reads backwards &mdash; the list looks "
         "unsorted after every pass but the last &mdash; and it is what allows a "
         "single linear pass per digit instead of recursion."),
    ],
    "try": [
        "Print only after the ones pass. The list is sorted by last digit and "
        "otherwise scrambled &mdash; every intermediate state looks like a bug.",
        "Make one pass unstable by iterating forwards. The final output is wrong, "
        "and it is wrong in a way that is very hard to read off the result.",
        "Add <code>999999</code> to <code>data</code>. One extra item costs three "
        "extra passes over everything &mdash; d is set by the widest value, not "
        "the typical one.",
    ],
},

}


# =========================================================================
# Graphs
# =========================================================================

GRAPHS = {

"dsa/graph_representations.html": {
    "file": "representations.py",
    "intro": "The same six-node graph stored three ways, with the cost of each "
             "question measured against each store. Nothing here is an opinion "
             "&mdash; the memory figures come from <code>sys.getsizeof</code> and "
             "the operation counts are counted.",
    "code": '''# One graph, three representations, and what each one is good at.

edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"),
         ("D", "E"), ("E", "F")]
nodes = ["A", "B", "C", "D", "E", "F"]

# 1. Edge list - just the pairs.
print("edge list :", edges)

# 2. Adjacency list - for each node, who it reaches.
adj_list = {n: [] for n in nodes}
for u, v in edges:
    adj_list[u].append(v)
    adj_list[v].append(u)            # undirected: store both directions
print("adj list  :", adj_list)

# 3. Adjacency matrix - a full V x V grid of yes/no.
index = {n: i for i, n in enumerate(nodes)}
matrix = [[0] * len(nodes) for _ in nodes]
for u, v in edges:
    matrix[index[u]][index[v]] = 1
    matrix[index[v]][index[u]] = 1
print("adj matrix:")
print("    " + "  ".join(nodes))
for n in nodes:
    row = "  ".join(str(x) for x in matrix[index[n]])
    print(f"  {n} {row}")

print()
# "Is there an edge A-D?" - one lookup vs a scan.
print("matrix answers 'A-D?' in one step   :", bool(matrix[index["A"]][index["D"]]))
print("list scans A's neighbours           :", "D" in adj_list["A"], f"({len(adj_list['A'])} checked)")

print()
# "Who does D reach?" - a scan vs a direct read.
row_scan = [nodes[i] for i, x in enumerate(matrix[index["D"]]) if x]
print("matrix scans a whole row of", len(nodes), ":", row_scan)
print("list reads the answer directly     :", adj_list["D"])

print()
V, E = len(nodes), len(edges)
print(f"V = {V}, E = {E}")
print(f"matrix cells   : V*V = {V * V}  (of which {2 * E} are 1s)")
print(f"list entries   : 2*E = {2 * E}")
print("Sparse graphs waste most of a matrix. Dense ones make the list slower.")
''',
    "walk": [
        ("adj_list[u].append(v); adj_list[v].append(u)",
         "Both directions, because the graph is undirected. Drop the second line "
         "and you have a directed graph &mdash; that one line is the entire "
         "difference in code."),
        ("matrix = [[0] * len(nodes) for _ in nodes]",
         "V&times;V cells allocated up front, whether or not there are edges to "
         "put in them. For a social network of a million users that is 10¹² "
         "cells to store a few hundred million edges."),
        ("matrix[index[\"A\"]][index[\"D\"]]",
         "Constant time, and unbeatable. If the question your program asks most "
         "often is “are these two connected?”, this is the representation."),
        ("adj_list[\"D\"]",
         "Also constant time, and it returns the neighbours themselves. Traversal "
         "algorithms &mdash; BFS, DFS, Dijkstra &mdash; ask this question and "
         "never the other one, which is why they all assume an adjacency list."),
        ("V*V versus 2*E",
         "The whole trade-off in two numbers. Matrices cost O(V²) always; lists "
         "cost O(V + E), which is smaller exactly when the graph is sparse "
         "&mdash; and real graphs almost always are."),
    ],
    "try": [
        "Add the edges to make the graph complete (every node to every other). "
        "The matrix cost does not move; the list cost climbs to meet it.",
        "Delete the <code>adj_list[v].append(u)</code> line and print the result. "
        "You now have a directed graph, and <code>adj_list[\"F\"]</code> is empty.",
        "Store weights instead of 1s in both structures. The matrix takes it "
        "without a change of shape; the list has to hold pairs.",
    ],
},

"dsa/breadth_first_search.html": {
    "file": "bfs.py",
    "intro": "BFS printed level by level, then used for what it is actually for: "
             "the shortest path in an unweighted graph. The queue contents are "
             "shown at every step so the frontier is visible.",
    "code": '''# Breadth-first search: explore everything one step away, then two, then...
from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E", "G"],
    "G": ["F"],
}

def bfs(graph, start):
    visited = {start}                # marked when ENQUEUED, not when dequeued
    queue = deque([start])
    order, parent, dist = [], {start: None}, {start: 0}

    while queue:
        print(f"  queue: {list(queue)}")
        node = queue.popleft()       # popleft = FIFO = breadth-first
        order.append(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                parent[neighbour] = node
                dist[neighbour] = dist[node] + 1
                queue.append(neighbour)
    return order, parent, dist


print("BFS from A:")
order, parent, dist = bfs(graph, "A")
print()
print("visit order:", " -> ".join(order))

print()
levels = {}
for node, d in dist.items():
    levels.setdefault(d, []).append(node)
for d in sorted(levels):
    print(f"  {d} step(s) from A: {levels[d]}")

# Rebuild the path by walking parents backwards from the target.
target = "G"
path, node = [], target
while node is not None:
    path.append(node)
    node = parent[node]
print()
print(f"shortest path A -> {target}:", " -> ".join(reversed(path)),
      f"({dist[target]} edges)")
''',
    "walk": [
        ("queue = deque([start])",
         "A <code>deque</code>, not a list: <code>list.pop(0)</code> is O(n) "
         "because it shifts every remaining item. On a large graph that alone "
         "turns a linear traversal quadratic."),
        ("visited.add(neighbour)  # on enqueue",
         "Marking on enqueue rather than on dequeue is the difference between "
         "BFS and a slow disaster. Mark late and a node with three neighbours "
         "already in the queue gets added three times."),
        ("node = queue.popleft()",
         "First in, first out. Change this one call to <code>pop()</code> and the "
         "same twelve lines become depth-first search &mdash; the container is "
         "the algorithm."),
        ("dist[neighbour] = dist[node] + 1",
         "Because nodes are dequeued in order of distance, the first time BFS "
         "reaches a node is necessarily by a shortest path. This is why BFS "
         "solves shortest paths on unweighted graphs and Dijkstra is not needed."),
        ("while node is not None: path.append(node)",
         "The <code>parent</code> map is a tree rooted at the start, so the path "
         "is recovered by walking up it. Storing the whole path per node instead "
         "would cost O(V) memory per node for no benefit."),
    ],
    "try": [
        "Change <code>popleft()</code> to <code>pop()</code>. The visit order "
        "becomes depth-first and the distances stop being shortest paths.",
        "Move <code>visited.add</code> to just after <code>popleft()</code>, then "
        "print the queue length. Nodes appear more than once &mdash; the classic "
        "BFS bug.",
        "Add the edge <code>\"A\": [\"B\", \"C\", \"G\"]</code>. The path to G "
        "drops to one edge, and the level listing rearranges itself.",
    ],
},

"dsa/depth_first_search.html": {
    "file": "dfs.py",
    "intro": "The same traversal written twice &mdash; once recursively and once "
             "with an explicit stack &mdash; so you can see that the call stack "
             "and the stack you push to by hand are the same object.",
    "code": '''# Depth-first search: follow one path as far as it goes, then back up.

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": ["G"],
    "G": [],
}

# --- 1. recursive: the call stack does the remembering -------------------
def dfs_recursive(node, visited=None, depth=0):
    if visited is None:
        visited = set()
    visited.add(node)
    print(f"{'  ' * depth}enter {node}")
    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs_recursive(neighbour, visited, depth + 1)
    print(f"{'  ' * depth}leave {node}")
    return visited


print("recursive:")
dfs_recursive("A")

# --- 2. iterative: the same stack, made explicit ------------------------
def dfs_iterative(start):
    visited, order = set(), []
    stack = [start]
    while stack:
        node = stack.pop()               # pop = LIFO = depth-first
        if node in visited:
            continue                     # a node can be stacked twice
        visited.add(node)
        order.append(node)
        for neighbour in reversed(graph[node]):   # reversed: match recursion
            if neighbour not in visited:
                stack.append(neighbour)
    return order


print()
print("iterative:", " -> ".join(dfs_iterative("A")))

# Cycle safety: the visited set is the only thing preventing an infinite loop.
graph["G"] = ["A"]
print()
print("with a G -> A edge added back:")
print("iterative:", " -> ".join(dfs_iterative("A")))
''',
    "walk": [
        ("visited.add(node) before recursing",
         "Marking on entry is what makes the traversal terminate. A graph is not "
         "a tree &mdash; without this, the <code>G &rarr; A</code> edge added at "
         "the end sends the function round forever."),
        ("print enter / print leave",
         "The pair brackets each call, so the output is literally the shape of the "
         "call stack over time. Post-order work &mdash; topological sort, subtree "
         "sizes &mdash; belongs on the “leave” line."),
        ("node = stack.pop()",
         "The last node pushed is the next explored, which is what “depth first” "
         "means mechanically. BFS is the same loop with a queue."),
        ("if node in visited: continue",
         "The iterative version needs a second check because a node can be pushed "
         "by several neighbours before it is popped. Skipping this does not loop "
         "forever, but it does visit nodes twice."),
        ("for neighbour in reversed(graph[node]):",
         "A stack reverses order, so pushing the neighbour list backwards makes "
         "the iterative version explore in the same order as the recursive one. "
         "Without it both are valid DFS, just different DFS."),
    ],
    "try": [
        "Delete <code>visited.add(node)</code> from the recursive version and run "
        "it with the <code>G &rarr; A</code> edge in place. The "
        "<code>RecursionError</code> is the base case you removed.",
        "Move the <code>leave</code> print above the loop. The output is no longer "
        "nested, which shows what pre-order and post-order actually mean.",
        "Chain a thousand nodes together and call the recursive version. It hits "
        "Python's recursion limit; the iterative one does not care.",
    ],
},

"dsa/dijkstras.html": {
    "file": "dijkstra.py",
    "intro": "A priority queue, a distance table, and a printout of every pop and "
             "every relaxation. The second half feeds it a negative edge to show "
             "the exact point at which the algorithm is wrong.",
    "code": '''# Dijkstra: always finalise the nearest unfinished node.
import heapq

graph = {
    "A": {"B": 4, "C": 2},
    "B": {"C": 5, "D": 10},
    "C": {"E": 3},
    "D": {"F": 11},
    "E": {"D": 4},
    "F": {},
}

def dijkstra(graph, start):
    dist = {n: float("inf") for n in graph}
    dist[start] = 0
    parent = {start: None}
    done = set()
    heap = [(0, start)]                     # (distance so far, node)

    while heap:
        d, node = heapq.heappop(heap)       # the nearest unfinished node
        if node in done:
            continue                        # a stale copy; skip it
        done.add(node)
        print(f"finalise {node} at {d}")
        for neighbour, weight in graph[node].items():
            if d + weight < dist[neighbour]:
                dist[neighbour] = d + weight
                parent[neighbour] = node
                heapq.heappush(heap, (dist[neighbour], neighbour))
                print(f"   relax {node}->{neighbour}: {dist[neighbour]}")
    return dist, parent


dist, parent = dijkstra(graph, "A")
print()
print("distances:", dist)

path, node = [], "F"
while node is not None:
    path.append(node)
    node = parent[node]
print("A -> F   :", " -> ".join(reversed(path)), "=", dist["F"])

print()
print("Now with a negative edge (B -> C costs -6):")
graph["B"]["C"] = -6
bad, _ = dijkstra(graph, "A")
print("distances:", bad)
print("A->B->C is 4 + -6 = -2, but C was finalised at 2 and never revisited.")
''',
    "walk": [
        ("heap = [(0, start)]",
         "Tuples, so the heap orders by distance first. Python's "
         "<code>heapq</code> is a min-heap over whatever you give it, and putting "
         "the distance first is what makes it a priority queue over distances."),
        ("if node in done: continue",
         "The lazy-deletion trick. <code>heapq</code> cannot update a key in "
         "place, so improved distances are pushed as new entries and the stale "
         "ones are skipped when they surface. Cheaper than a decrease-key "
         "structure, and far easier to get right."),
        ("if d + weight < dist[neighbour]:",
         "The relaxation, and the whole algorithm. “I have a route to "
         "<em>node</em> that costs d; going on to <em>neighbour</em> beats "
         "whatever I had.”"),
        ("done.add(node)",
         "The node's distance is now final and will never be improved. This is "
         "the claim the correctness proof rests on &mdash; and it holds only "
         "because every edge is non-negative, so no later route can be shorter."),
        ("graph[\"B\"][\"C\"] = -6",
         "The counterexample. C is finalised at 2 before B is even examined, so "
         "the cheaper route through B arrives too late. Dijkstra does not detect "
         "this; it just returns a wrong answer. Use "
         "<a href=\"bellman_ford.html\">Bellman-Ford</a> instead."),
    ],
    "try": [
        "Set <code>graph[\"A\"][\"C\"] = 20</code>. The finalisation order "
        "changes and the path to F reroutes &mdash; watch the relax lines that "
        "get superseded.",
        "Print <code>len(heap)</code> each iteration. It exceeds the node count, "
        "which is the stale entries lazy deletion leaves behind.",
        "Replace the heap with a linear scan for the nearest unfinished node. The "
        "answers are identical and the complexity goes from O(E log V) to O(V²).",
    ],
},

"dsa/bellman_ford.html": {
    "file": "bellman_ford.py",
    "intro": "V &minus; 1 rounds of relaxing every edge, with the distance table "
             "printed after each round so you can watch it settle &mdash; and "
             "then one extra round, which is the entire negative-cycle detector.",
    "code": '''# Bellman-Ford: relax EVERY edge, V-1 times. Slower than Dijkstra,
# but it copes with negative weights and can prove a negative cycle exists.

edges = [("A", "B", 4), ("A", "C", 5), ("B", "C", -3),
         ("B", "D", 2), ("C", "E", 4), ("D", "E", -1), ("E", "F", 2)]
nodes = ["A", "B", "C", "D", "E", "F"]

def bellman_ford(nodes, edges, start):
    dist = {n: float("inf") for n in nodes}
    dist[start] = 0
    parent = {start: None}

    for round_no in range(1, len(nodes)):        # V - 1 rounds
        changed = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        shown = {n: (d if d != float("inf") else "inf") for n, d in dist.items()}
        print(f"round {round_no}: {shown}")
        if not changed:                          # nothing moved; it is settled
            print("        no change - stopping early")
            break

    # One more pass. Any further improvement means a negative cycle.
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            return dist, parent, True
    return dist, parent, False


dist, parent, negative = bellman_ford(nodes, edges, "A")
print()
print("distances       :", dist)
print("negative cycle? :", negative)

print()
print("Adding an edge E -> B of -5, which closes a negative loop:")
edges.append(("E", "B", -5))
dist, parent, negative = bellman_ford(nodes, edges, "A")
print("negative cycle? :", negative)
print("B -> D -> E -> B costs 2 + -1 + -5 = -4, so going round again is free money.")
''',
    "walk": [
        ("for round_no in range(1, len(nodes)):",
         "V &minus; 1 rounds, and not one more. A shortest path visits each node "
         "at most once, so it has at most V &minus; 1 edges &mdash; and each "
         "round is guaranteed to settle at least one more edge of it."),
        ("if dist[u] != float(\"inf\") and dist[u] + w < dist[v]:",
         "The infinity guard matters: <code>inf + -5</code> is still "
         "<code>inf</code> in floating point, but relaxing from a node you have "
         "not reached yet is meaningless and pollutes the parent map."),
        ("for u, v, w in edges:",
         "Every edge, every round, in whatever order the list happens to be in. "
         "That brute force is the reason negative weights are safe here where "
         "they break Dijkstra."),
        ("if not changed: break",
         "A round that changes nothing means every later round changes nothing "
         "either. Typical graphs settle long before V &minus; 1 rounds, so this "
         "is most of the practical speed."),
        ("one more pass -> return True",
         "After V &minus; 1 rounds the distances are final <em>if</em> they exist. "
         "An edge that still improves therefore proves a cycle whose total weight "
         "is negative &mdash; there is no shortest path at all, because going "
         "round once more is always cheaper."),
    ],
    "try": [
        "Reverse <code>edges</code> before running. The intermediate rounds differ "
        "&mdash; edge order changes how fast it converges, never the answer.",
        "Print the round number the early exit fires on. On this graph it is well "
        "short of V &minus; 1; construct a path graph A&rarr;B&rarr;C&rarr;... "
        "with the edges listed backwards to force the full count.",
        "Delete the early exit and the final pass, then run the negative-cycle "
        "version. The distances just keep falling &mdash; that is what the "
        "detector is protecting you from.",
    ],
},

"dsa/a_star.html": {
    "file": "a_star.py",
    "intro": "The same grid solved twice: once by Dijkstra and once by A* with a "
             "Manhattan heuristic. Both find a shortest path; the interesting "
             "number is how many cells each one had to expand to do it.",
    "code": '''# A*: Dijkstra plus an estimate of the distance still to go.
import heapq

GRID = [
    "..........#.........",
    ".####.....#.####....",
    ".#..#..####....#....",
    ".#..#..#..........#.",
    "....#..#..####..#.#.",
    ".####..#.....#..#...",
    ".......#####.#..#.#.",
    ".#####.......#....#.",
    ".....#.#######..###.",
    "..#........#........",
]
ROWS, COLS = len(GRID), len(GRID[0])
START, GOAL = (0, 0), (ROWS - 1, COLS - 1)

def neighbours(cell):
    r, c = cell
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and GRID[nr][nc] != "#":
            yield (nr, nc)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def search(heuristic, label):
    g = {START: 0}                       # cost from the start, known
    parent = {START: None}
    h0 = heuristic(START, GOAL)
    heap = [(h0, h0, START)]             # (f, h, cell)
    seen = set()
    expanded = 0

    while heap:
        _, _, node = heapq.heappop(heap)
        if node in seen:
            continue
        seen.add(node)
        expanded += 1
        if node == GOAL:
            break
        for nxt in neighbours(node):
            tentative = g[node] + 1      # every step costs 1
            if tentative < g.get(nxt, float("inf")):
                g[nxt] = tentative
                parent[nxt] = node
                h = heuristic(nxt, GOAL)
                # f = cost so far + estimate of what is left
                heapq.heappush(heap, (tentative + h, h, nxt))

    path, node = [], GOAL
    while node is not None:
        path.append(node)
        node = parent[node]
    print(f"{label:>9}: path length {len(path) - 1}, cells expanded {expanded}")
    return set(path)


search(lambda a, b: 0, "Dijkstra")       # h = 0 is exactly Dijkstra
path = search(manhattan, "A*")

print()
for r in range(ROWS):
    print("  " + "".join("*" if (r, c) in path else GRID[r][c] for c in range(COLS)))
print()
print(f"{sum(row.count('.') for row in GRID)} open cells.")
print("Same path length. A* just wasted less time looking away from the goal.")
''',
    "walk": [
        ("heapq.heappush(heap, (tentative + h, h, nxt))",
         "The one line that separates A* from Dijkstra: the priority is "
         "<code>f = g + h</code>, cost already spent plus cost estimated to "
         "remain, instead of <code>g</code> alone."),
        ("(f, h, cell)",
         "The second element breaks ties. On a grid where every step costs 1 an "
         "enormous number of cells share an f value, and preferring the one "
         "nearest the goal is what turns a fan into a beeline. It changes nothing "
         "about correctness and most of the measured saving here comes from it."),
        ("search(lambda a, b: 0, \"Dijkstra\")",
         "With <code>h = 0</code> the formula collapses to <code>f = g</code>, so "
         "the identical function <em>is</em> Dijkstra. That is the cleanest way "
         "to see that A* is a generalisation, not a different algorithm."),
        ("def manhattan(a, b):",
         "Steps are up/down/left/right and each costs 1, so the Manhattan "
         "distance can never overestimate what remains. That property "
         "&mdash; admissibility &mdash; is what keeps the answer optimal."),
        ("if tentative < g.get(nxt, float(\"inf\")):",
         "Compares on <code>g</code>, never on <code>f</code>. The heuristic "
         "decides what to look at next; it must not be allowed to decide what "
         "the route actually cost."),
        ("expanded",
         "The number that matters. Both runs return a shortest path of the same "
         "length, and A* gets there having opened far fewer cells &mdash; on a "
         "game map or a road network that is the entire point."),
    ],
    "try": [
        "Multiply the heuristic by 5. It is now inadmissible: expansions drop "
        "further, and the path it returns can be longer than the shortest one.",
        "Swap Manhattan for Euclidean (<code>math.hypot</code>). Still "
        "admissible on this grid, but weaker, so more cells get expanded.",
        "Wall the goal off completely. Both searches drain the heap and the "
        "reconstructed path is nonsense &mdash; a real implementation has to "
        "check that the goal was actually reached.",
    ],
},

"dsa/topological_sort.html": {
    "file": "topological_sort.py",
    "intro": "Kahn's algorithm on a small course-prerequisite graph, printing the "
             "in-degree table as it drains. The final block adds one edge that "
             "closes a cycle, which is how the same code detects that no ordering "
             "exists.",
    "code": '''# Topological sort (Kahn): repeatedly take a node nothing depends on.
from collections import deque

prereqs = {
    "intro":    [],
    "maths":    [],
    "python":   ["intro"],
    "data":     ["python", "maths"],
    "ml":       ["data", "maths"],
    "deep":     ["ml"],
    "nlp":      ["deep"],
}

def topological_sort(prereqs):
    indegree = {n: len(deps) for n, deps in prereqs.items()}
    dependents = {n: [] for n in prereqs}
    for node, deps in prereqs.items():
        for d in deps:
            dependents[d].append(node)

    ready = deque(n for n, deg in indegree.items() if deg == 0)
    print("start, in-degrees:", indegree)
    order = []

    while ready:
        node = ready.popleft()
        order.append(node)
        for dependent in dependents[node]:
            indegree[dependent] -= 1        # one prerequisite satisfied
            if indegree[dependent] == 0:
                ready.append(dependent)
        print(f"take {node:>7} -> ready={list(ready)}")

    if len(order) != len(prereqs):          # something never reached zero
        stuck = [n for n, deg in indegree.items() if deg > 0]
        return None, stuck
    return order, []


order, stuck = topological_sort(prereqs)
print()
print("a valid order:", " -> ".join(order))

print()
print("Now make nlp a prerequisite of maths, which closes a cycle:")
prereqs["maths"] = ["nlp"]
order, stuck = topological_sort(prereqs)
print("order:", order)
print("never reached in-degree 0:", stuck)
''',
    "walk": [
        ("indegree = {n: len(deps) for n, deps in prereqs.items()}",
         "How many prerequisites each node is still waiting on. The algorithm is "
         "nothing but keeping this table correct as nodes are removed."),
        ("dependents[d].append(node)",
         "The graph reversed. The input says “what does this need”; the loop "
         "needs “what is unblocked when this is done”, and building both is "
         "cheaper than searching one repeatedly."),
        ("ready = deque(... if deg == 0)",
         "Everything with no prerequisites can start immediately, and in any "
         "order. A graph usually has many valid topological orders, not one."),
        ("indegree[dependent] -= 1",
         "Decrement, never recompute. Each edge is looked at exactly once across "
         "the whole run, which is what makes this O(V + E)."),
        ("if len(order) != len(prereqs):",
         "The cycle test, and it is free. Nodes in a cycle always wait on each "
         "other, so their in-degree never reaches zero and they never enter the "
         "queue &mdash; a short output <em>is</em> the detection."),
    ],
    "try": [
        "Swap <code>popleft()</code> for <code>pop()</code>. A different, equally "
        "valid order comes out &mdash; useful proof that the answer is not unique.",
        "Use a <code>heapq</code> instead of a deque to get the "
        "lexicographically smallest valid order. That is the usual "
        "“deterministic build order” requirement.",
        "Add a node with a prerequisite on itself. In-degree 1 forever, and it "
        "shows up in the stuck list immediately.",
    ],
},

"dsa/cycle_detection.html": {
    "file": "cycle_detection.py",
    "intro": "Two different cycle problems and the two different answers: Floyd's "
             "two pointers on a linked list, in O(1) memory, and three-colour DFS "
             "on a directed graph, which also names the cycle it found.",
    "code": '''# Two cycle problems that look alike and are not.

# --- 1. A linked list: Floyd's tortoise and hare, O(1) memory -----------
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

values = [1, 2, 3, 4, 5, 6]
nodes = [Node(v) for v in values]
for a, b in zip(nodes, nodes[1:]):
    a.next = b
nodes[-1].next = nodes[2]              # 6 points back at 3 - a loop

def find_cycle(head):
    slow = fast = head
    step = 0
    while fast and fast.next:
        slow = slow.next               # one step
        fast = fast.next.next          # two steps
        step += 1
        print(f"  step {step}: slow={slow.value} fast={fast.value}")
        if slow is fast:               # identity, not equality
            break
    else:
        return None

    # Second phase: the distance from head to the entry equals the
    # distance from the meeting point to the entry.
    entry = head
    while entry is not slow:
        entry, slow = entry.next, slow.next
    return entry


print("linked list:")
entry = find_cycle(nodes[0])
print("cycle enters at value:", entry.value if entry else "no cycle")

# --- 2. A directed graph: DFS with three colours ------------------------
graph = {"a": ["b"], "b": ["c"], "c": ["d"], "d": ["b"], "e": ["a"]}
WHITE, GREY, BLACK = 0, 1, 2          # unseen / on the stack / finished

def has_cycle(graph):
    colour = {n: WHITE for n in graph}
    stack = []

    def visit(node):
        colour[node] = GREY           # now on the current path
        stack.append(node)
        for nxt in graph.get(node, []):
            if colour[nxt] == GREY:   # back edge to something still open
                return stack[stack.index(nxt):] + [nxt]
            if colour[nxt] == WHITE:
                found = visit(nxt)
                if found:
                    return found
        colour[node] = BLACK          # finished; safe to meet again
        stack.pop()
        return None

    for node in graph:
        if colour[node] == WHITE:
            found = visit(node)
            if found:
                return found
    return None


print()
print("directed graph:", graph)
print("cycle:", " -> ".join(has_cycle(graph)))
''',
    "walk": [
        ("slow = slow.next; fast = fast.next.next",
         "Two pointers at different speeds. Inside a loop the gap closes by one "
         "node per step, so if there is a cycle they must meet &mdash; and the "
         "whole thing costs two pointers of memory rather than a visited set."),
        ("if slow is fast:",
         "<code>is</code>, not <code>==</code>. The test is whether they are on "
         "the same node; two different nodes holding equal values would fool "
         "<code>==</code> completely."),
        ("while entry is not slow: entry, slow = entry.next, slow.next",
         "The second phase, and the part that looks like magic. The distance from "
         "the head to the loop entry equals the distance from the meeting point "
         "to the entry, so two pointers advancing in step meet exactly there."),
        ("WHITE, GREY, BLACK",
         "Two colours are not enough for a directed graph. GREY means “on the "
         "path I am currently exploring”; BLACK means “finished, and reaching it "
         "again is fine”. Merging them reports a cycle for any diamond shape."),
        ("if colour[nxt] == GREY: return ...",
         "An edge back into the current path is a cycle, by definition. The "
         "explicit <code>stack</code> is only there so the cycle can be printed "
         "&mdash; detection needs the colours alone."),
    ],
    "try": [
        "Point <code>nodes[-1].next</code> at <code>None</code>. The loop exits "
        "through its <code>else</code> branch, which is what makes this a "
        "detector and not just a locator.",
        "Change <code>fast.next.next</code> to <code>fast.next</code>. The two "
        "pointers now move at the same speed and never meet.",
        "In the graph, drop GREY and treat any seen node as a cycle. Then add "
        "<code>\"e\": [\"a\", \"b\"]</code> &mdash; a false positive, on a graph "
        "with no cycle through e at all.",
    ],
},

"dsa/minimum_spanning_tree.html": {
    "file": "mst.py",
    "intro": "Kruskal and Prim on the same weighted graph. They pick edges in "
             "completely different orders and arrive at the same total weight "
             "&mdash; which is the property worth seeing rather than being told.",
    "code": '''# Minimum spanning tree, twice: Kruskal (sort edges) and Prim (grow a tree).
import heapq

edges = [("A", "B", 4), ("A", "C", 8), ("B", "C", 11), ("B", "D", 8),
         ("C", "E", 7), ("D", "E", 2), ("D", "F", 4), ("E", "F", 9),
         ("C", "F", 1)]
nodes = sorted({n for u, v, _ in edges for n in (u, v)})

# --- Kruskal: cheapest edge first, skip any that closes a cycle ---------
def kruskal():
    parent = {n: n for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # path compression
            x = parent[x]
        return x

    tree, total = [], 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru == rv:
            print(f"  skip {u}-{v} ({w}) - would close a cycle")
            continue
        parent[ru] = rv
        tree.append((u, v, w))
        total += w
        print(f"  take {u}-{v} ({w})")
    return tree, total


# --- Prim: grow one tree, always out along its cheapest edge ------------
def prim(start):
    adj = {n: [] for n in nodes}
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    seen = {start}
    heap = list(adj[start])
    heapq.heapify(heap)
    tree, total = [], 0
    while heap and len(seen) < len(nodes):
        w, node = heapq.heappop(heap)
        if node in seen:
            continue
        seen.add(node)
        tree.append((node, w))
        total += w
        print(f"  take {node} ({w})")
        for nxt in adj[node]:
            if nxt[1] not in seen:
                heapq.heappush(heap, nxt)
    return tree, total


print("Kruskal:")
k_tree, k_total = kruskal()
print("Prim from A:")
p_tree, p_total = prim("A")

print()
print("Kruskal edges :", [f"{u}-{v}" for u, v, _ in k_tree], "total", k_total)
print("Prim weights  :", [w for _, w in p_tree], "total", p_total)
print(f"{len(nodes)} nodes -> {len(k_tree)} edges. A spanning tree always has V-1.")
''',
    "walk": [
        ("sorted(edges, key=lambda e: e[2])",
         "Kruskal's entire strategy: cheapest first, globally, ignoring where the "
         "edges are. The sort is also its dominant cost &mdash; O(E log E)."),
        ("if ru == rv: continue",
         "Both ends already connected means this edge adds nothing but a cycle. "
         "Union-find answers that in near-constant time; without it the check "
         "would need a traversal per edge."),
        ("heap = list(adj[start])",
         "Prim starts from one node and only ever considers edges leaving the "
         "tree it has grown. It never sees most of the graph at once, which is "
         "the opposite of Kruskal's global sort."),
        ("if node in seen: continue",
         "Same lazy deletion as Dijkstra &mdash; and Prim really is Dijkstra with "
         "the priority changed from “distance from the start” to “weight of this "
         "one edge”."),
        ("len(k_tree) == len(nodes) - 1",
         "Any spanning tree of V nodes has exactly V &minus; 1 edges. Both "
         "algorithms hit that count and the same total, though the edge sets can "
         "differ when weights tie."),
    ],
    "try": [
        "Print the two edge sets side by side. On this graph they match; make two "
        "edges equal in weight and they can diverge while the totals stay equal.",
        "Delete edge <code>C-F</code>. Kruskal's very first choice changes and the "
        "whole tree reshapes.",
        "Remove an edge so the graph is disconnected. Kruskal returns fewer than "
        "V &minus; 1 edges &mdash; a spanning forest, which is often what you "
        "actually wanted.",
    ],
},

"dsa/union_find.html": {
    "file": "union_find.py",
    "intro": "The same twelve operations run twice: once on a naive "
             "implementation, once with union by rank and path compression, with "
             "pointer hops counted. The difference between the two counts is the "
             "whole reason the optimisations exist.",
    "code": '''# Union-Find (disjoint set union): which things are in the same group?

class NaiveDSU:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.hops = 0

    def find(self, x):
        while self.parent[x] != x:      # walk up to the root
            self.hops += 1
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb        # attach blindly - this is the problem
            return True
        return False


class DSU(NaiveDSU):
    def __init__(self, items):
        super().__init__(items)
        self.rank = {x: 0 for x in items}

    def find(self, x):
        root = x
        while self.parent[root] != root:
            self.hops += 1
            root = self.parent[root]
        while self.parent[x] != root:   # path compression: flatten on the way back
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:       # union by rank: shorter under taller
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


items = list(range(10))
merges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]

for cls in (NaiveDSU, DSU):
    dsu = cls(items)
    for a, b in merges:
        dsu.union(a, b)
    for x in items:                     # now ask about every element
        dsu.find(x)
    print(f"{cls.__name__:>9}: {dsu.hops} pointer hops")

print()
dsu = DSU(items)
for a, b in [(0, 1), (2, 3), (1, 3), (5, 6)]:
    print(f"union({a}, {b}) merged:", dsu.union(a, b))
groups = {}
for x in items:
    groups.setdefault(dsu.find(x), []).append(x)
print("groups:", list(groups.values()))
print("connected(0, 3):", dsu.find(0) == dsu.find(3))
print("connected(0, 5):", dsu.find(0) == dsu.find(5))
''',
    "walk": [
        ("self.parent = {x: x for x in items}",
         "Every element starts as its own root, so there are n groups of one. "
         "“Which group is x in?” is always answered by walking to the root, and "
         "the root's identity is the group's name."),
        ("self.parent[ra] = rb   # naive",
         "Attaching without looking at the shapes is what builds a chain. Merge "
         "in a line, as the sample does, and <code>find</code> degrades to O(n) "
         "&mdash; a linked list wearing a tree's name."),
        ("if self.rank[ra] < self.rank[rb]: ra, rb = rb, ra",
         "Union by rank: hang the shorter tree under the taller one so the depth "
         "does not grow. Rank is an upper bound on height, not the exact height, "
         "which is why compression can leave it stale without breaking anything."),
        ("while self.parent[x] != root: self.parent[x], x = root, self.parent[x]",
         "Path compression. Every node touched on the way up is re-pointed "
         "straight at the root, so the next query on any of them is one hop. The "
         "work of the walk is what pays for the next walk."),
        ("dsu.hops",
         "Together these give near-constant amortised time &mdash; O(α(n)), where "
         "α is the inverse Ackermann function and is below 5 for any n that fits "
         "in a computer. The hop counts printed here are that theory, measured."),
    ],
    "try": [
        "Raise <code>items</code> to <code>range(1000)</code> with the same chain "
        "of merges. The naive count explodes quadratically; the optimised one "
        "barely moves.",
        "Delete only the compression loop, keeping rank. Most of the win survives "
        "&mdash; either optimisation alone is already good.",
        "Add a <code>count</code> field decremented on each successful union. "
        "That is how union-find answers “how many connected components?” "
        "in O(1).",
    ],
},

}


# =========================================================================
# Linear and tree structures
# =========================================================================

STRUCTURES = {

"dsa/stacks.html": {
    "file": "stacks.py",
    "intro": "A stack built on a plain list, then put to work on the two jobs it "
             "is famous for: matching brackets and evaluating postfix. Both are "
             "traced push by push.",
    "code": '''# A stack: add and remove at one end only. Last in, first out.

class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)        # append is amortised O(1)

    def pop(self):
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()     # pop() with no index: the END

    def peek(self):
        return self._items[-1] if self._items else None

    def __len__(self):
        return len(self._items)


s = Stack()
for x in "ABC":
    s.push(x)
    print(f"push {x} -> top is {s.peek()}, size {len(s)}")
print(f"pop     -> {s.pop()}, top is now {s.peek()}")

# --- job 1: balanced brackets ------------------------------------------
def balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = Stack()
    for ch in text:
        if ch in "([{":
            stack.push(ch)
        elif ch in pairs:
            if len(stack) == 0 or stack.pop() != pairs[ch]:
                return False         # closer with no matching opener
    return len(stack) == 0           # anything left open is unbalanced


print()
for text in ["(a[b]{c})", "(a[b)c]", "((()", "()"]:
    print(f"{text:>10}: {balanced(text)}")

# --- job 2: evaluating postfix -----------------------------------------
def postfix(expr):
    stack = Stack()
    for token in expr.split():
        if token.isdigit():
            stack.push(int(token))
        else:
            b, a = stack.pop(), stack.pop()      # note the order
            stack.push({"+": a + b, "-": a - b,
                        "*": a * b, "/": a // b}[token])
        print(f"  {token:>3} -> {stack._items}")
    return stack.pop()


print()
print("3 4 + 2 * =")
print("result:", postfix("3 4 + 2 *"))
''',
    "walk": [
        ("self._items.append(x) / self._items.pop()",
         "Both act on the end of the list, which is why both are O(1). Using "
         "<code>insert(0, x)</code> and <code>pop(0)</code> would be the same "
         "stack with every operation turned into O(n)."),
        ("if not self._items: raise IndexError",
         "Popping an empty stack is a bug in the caller, not a value to return. "
         "Returning <code>None</code> instead hides the mistake until something "
         "far away fails."),
        ("if len(stack) == 0 or stack.pop() != pairs[ch]:",
         "Two different failures: a closer with nothing open, and a closer that "
         "does not match what is open. Both have to be checked, and forgetting "
         "the first crashes on <code>\")\"</code>."),
        ("return len(stack) == 0",
         "The last check catches <code>\"((()\"</code> &mdash; every closer "
         "matched, but three openers were never closed. A stack that is not "
         "empty at the end is the whole test."),
        ("b, a = stack.pop(), stack.pop()",
         "The second operand comes off first, because it went on last. Reverse "
         "these two names and <code>+</code> and <code>*</code> still look "
         "correct while <code>-</code> and <code>/</code> silently invert."),
    ],
    "try": [
        "Feed <code>balanced</code> a string of 10,000 unmatched openers. It "
        "returns False without slowing down &mdash; the stack only ever grows.",
        "Evaluate <code>\"5 1 2 + 4 * + 3 -\"</code> by hand, then run it. This "
        "is the notation compilers actually emit.",
        "Add a <code>min()</code> in O(1) by pushing <code>(value, min_so_far)</code> "
        "pairs. A classic interview question, and four lines here.",
    ],
},

"dsa/queues.html": {
    "file": "queues.py",
    "intro": "Three queues: the naive list version, the <code>deque</code> that "
             "fixes it, and a fixed-size circular buffer. The middle block times "
             "the first two so the O(n) is a measurement, not a claim.",
    "code": '''# A queue: add at the back, remove from the front. First in, first out.
from collections import deque
import time

# --- 1. the obvious version, and why it is wrong -----------------------
class ListQueue:
    def __init__(self):
        self._items = []

    def enqueue(self, x):
        self._items.append(x)

    def dequeue(self):
        return self._items.pop(0)     # O(n): every other item shifts left


class DequeQueue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, x):
        self._items.append(x)

    def dequeue(self):
        return self._items.popleft()  # O(1): no shifting at all


q = DequeQueue()
for x in "ABC":
    q.enqueue(x)
    print(f"enqueue {x} -> {list(q._items)}")
print(f"dequeue   -> {q.dequeue()} (the oldest), left: {list(q._items)}")

# --- 2. the cost, measured --------------------------------------------
print()
N = 30_000
for cls in (ListQueue, DequeQueue):
    q = cls()
    for i in range(N):
        q.enqueue(i)
    start = time.time()
    for _ in range(N):
        q.dequeue()
    print(f"{cls.__name__:>12}: {N} dequeues in {time.time() - start:.3f}s")

# --- 3. a circular buffer: fixed memory, no shifting -------------------
class RingQueue:
    def __init__(self, capacity):
        self._items = [None] * capacity
        self._head = self._size = 0
        self._cap = capacity

    def enqueue(self, x):
        if self._size == self._cap:
            raise OverflowError("queue is full")
        self._items[(self._head + self._size) % self._cap] = x
        self._size += 1

    def dequeue(self):
        x = self._items[self._head]
        self._head = (self._head + 1) % self._cap    # wrap around
        self._size -= 1
        return x


print()
ring = RingQueue(4)
for x in "ABCD":
    ring.enqueue(x)
print("full ring   :", ring._items, "head", ring._head)
ring.dequeue(); ring.dequeue()
ring.enqueue("E")
print("after 2 out, 1 in:", ring._items, "head", ring._head)
print("E landed in the slot A left behind - nothing was ever moved.")
''',
    "walk": [
        ("self._items.pop(0)",
         "The bug that hides in plain sight. Removing the first element of a "
         "Python list moves every remaining element one place left, so a queue "
         "built this way is O(n) per dequeue and quadratic overall."),
        ("self._items.popleft()",
         "<code>deque</code> is a doubly linked list of blocks, so both ends are "
         "O(1). This is the right answer in Python, and the timing loop above "
         "shows the gap on 50,000 items."),
        ("(self._head + self._size) % self._cap",
         "The modulo is what makes the buffer circular: index 4 of a 4-slot ring "
         "is index 0. Writing past the end wraps to the space the front has "
         "already vacated."),
        ("self._head = (self._head + 1) % self._cap",
         "Dequeuing moves a pointer instead of moving data. That is the whole "
         "idea &mdash; the same fixed block of memory is reused forever, which is "
         "why ring buffers run in device drivers and audio pipelines."),
        ("if self._size == self._cap: raise OverflowError",
         "A ring must track size separately: head and tail meeting is ambiguous "
         "between full and empty. Getting this wrong silently overwrites the "
         "oldest entry."),
    ],
    "try": [
        "Raise <code>N</code> to 200,000. The deque timing scales linearly; the "
        "list version takes roughly sixteen times as long, not four.",
        "Make <code>RingQueue</code> overwrite the oldest item instead of raising. "
        "You have just written the standard “last N events” log buffer.",
        "Build a BFS on top of <code>ListQueue</code> instead of "
        "<code>deque</code>, then run it on a large graph. Same answer, "
        "unrecognisable running time.",
    ],
},

"dsa/linked_lists.html": {
    "file": "linked_list.py",
    "intro": "A singly linked list with insert, delete, search and an in-place "
             "reversal &mdash; the operation that is genuinely hard to get right "
             "and the reason this structure keeps appearing in interviews.",
    "code": '''# A singly linked list: each node holds a value and a reference to the next.

class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self, values=()):
        self.head = None
        for v in reversed(list(values)):     # build back to front
            self.head = Node(v, self.head)

    def __repr__(self):
        parts, node = [], self.head
        while node:
            parts.append(str(node.value))
            node = node.next
        return " -> ".join(parts) + " -> None"

    def push_front(self, value):             # O(1) - no shifting, ever
        self.head = Node(value, self.head)

    def insert_after(self, target, value):   # O(1) once you hold the node
        node = self.find(target)
        if node:
            node.next = Node(value, node.next)

    def find(self, value, verbose=False):    # O(n) - no random access
        node, steps = self.head, 0
        while node:
            steps += 1
            if node.value == value:
                if verbose:
                    print(f"find({value})    : {steps} hop(s) from the head")
                return node
            node = node.next
        return None

    def delete(self, value):
        # The dummy head removes the "deleting the first node" special case.
        dummy = Node(None, self.head)
        prev = dummy
        while prev.next:
            if prev.next.value == value:
                prev.next = prev.next.next   # unlink; nothing moves
                self.head = dummy.next
                return True
            prev = prev.next
        return False

    def reverse(self):
        prev, node = None, self.head
        while node:
            nxt = node.next        # save it BEFORE overwriting
            node.next = prev       # flip the arrow
            prev, node = node, nxt # step both forward
        self.head = prev


ll = LinkedList([10, 20, 30, 40])
print("start        :", ll)
ll.push_front(5)
print("push_front(5):", ll)
ll.insert_after(20, 25)
print("insert 25    :", ll)
ll.delete(10)
print("delete 10    :", ll)
ll.find(40, verbose=True)
ll.reverse()
print("reversed     :", ll)
''',
    "walk": [
        ("self.head = Node(value, self.head)",
         "Inserting at the front is O(1) and involves no movement at all &mdash; "
         "the new node simply points at the old head. The same insert into a "
         "Python list costs O(n)."),
        ("while node: ... node = node.next",
         "There is no arithmetic that jumps to element 5. Every access starts at "
         "the head and hops, which is why linked lists lose to arrays on almost "
         "every read-heavy workload despite the better insert."),
        ("dummy = Node(None, self.head)",
         "The sentinel trick. Without it, deleting the first node needs its own "
         "branch because there is no previous node to re-point &mdash; and that "
         "branch is where the bug always is."),
        ("prev.next = prev.next.next",
         "Deletion is one assignment. Nothing is shifted and no memory is moved, "
         "which is the operation linked lists exist for."),
        ("nxt = node.next; node.next = prev",
         "The order is the whole exercise. Overwrite <code>node.next</code> "
         "before saving it and the rest of the list is unreachable &mdash; not "
         "corrupted, just gone."),
    ],
    "try": [
        "Delete the <code>nxt = node.next</code> line in <code>reverse</code> and "
        "print the result. The list is one node long, and the other three are "
        "lost.",
        "Build a list of 100,000 nodes and time <code>find</code> on the last "
        "value against the same lookup on a Python list. Both are O(n), and the "
        "linked version is far slower &mdash; cache locality, not complexity.",
        "Add a <code>prev</code> pointer to make it doubly linked. Deletion no "
        "longer needs the node before it, which is exactly what "
        "<code>collections.deque</code> buys with the extra memory.",
    ],
},

"dsa/hash_tables.html": {
    "file": "hash_table.py",
    "intro": "A hash table built from a plain list of buckets, with the collision "
             "chains printed so you can see them form. The last block deliberately "
             "picks a terrible hash function to show what the structure degrades "
             "into.",
    "code": '''# A hash table with separate chaining: buckets of (key, value) pairs.

class HashTable:
    def __init__(self, size=8, hash_fn=None):
        self.buckets = [[] for _ in range(size)]
        self.size = size
        self.count = 0
        self.hash_fn = hash_fn or (lambda k: hash(k))

    def _index(self, key):
        return self.hash_fn(key) % self.size      # fold the hash into range

    def put(self, key, value):
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)          # update in place
                return
        bucket.append((key, value))
        self.count += 1
        if self.count / self.size > 0.75:         # load factor
            self._resize()

    def get(self, key):
        bucket = self.buckets[self._index(key)]
        for k, v in bucket:                       # scan the chain
            if k == key:
                return v
        raise KeyError(key)

    def _resize(self):
        old = self.buckets
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        for bucket in old:
            for k, v in bucket:                   # every key rehashed
                self.buckets[self._index(k)].append((k, v))
        print(f"  ** resized to {self.size} buckets and rehashed everything")

    def show(self):
        for i, bucket in enumerate(self.buckets):
            if bucket:
                print(f"  bucket {i:>2}: {[k for k, _ in bucket]}")


table = HashTable(size=8)
for word in ["apple", "banana", "cherry", "date", "elder", "fig", "grape"]:
    table.put(word, len(word))
print("buckets:")
table.show()
print("get('cherry') ->", table.get("cherry"))
print(f"load factor: {table.count}/{table.size} = {table.count / table.size:.2f}")

print()
print("Now the same keys with a deliberately awful hash:")
bad = HashTable(size=8, hash_fn=lambda k: 1)      # everything to one bucket
for word in ["apple", "banana", "cherry", "date"]:
    bad.put(word, len(word))
bad.show()
print("Every lookup now scans a list. O(1) was never about hashing being magic -")
print("it was about the keys being spread out.")
''',
    "walk": [
        ("self.hash_fn(key) % self.size",
         "Two separate jobs: the hash turns a key into a number, the modulo folds "
         "that number into a valid index. Changing the table size changes every "
         "index, which is why resizing has to rehash."),
        ("for i, (k, _) in enumerate(bucket):",
         "The chain has to be scanned even on a hit, because two different keys "
         "can land in the same bucket. Comparing keys, not hashes, is what makes "
         "the answer correct rather than probable."),
        ("if self.count / self.size > 0.75:",
         "The load factor. Past roughly three-quarters full, collisions rise "
         "sharply, so the table doubles before that happens rather than after. "
         "CPython's own dicts resize on the same principle."),
        ("for bucket in old: ... self._index(k)",
         "A resize is O(n) and touches every key. Amortised over the n inserts "
         "that caused it that is O(1) each &mdash; but any single insert can be "
         "the expensive one, which matters for latency."),
        ("hash_fn=lambda k: 1",
         "Every key in one bucket. The structure still works and every operation "
         "is now O(n): a hash table's guarantee is entirely conditional on the "
         "hash spreading keys evenly."),
    ],
    "try": [
        "Run it twice. The bucket numbers move, because Python randomises string "
        "hashing per process &mdash; a defence against deliberately collided "
        "input, and a reason never to rely on dictionary order across runs.",
        "Insert enough keys to trigger two resizes and watch the bucket layout "
        "reshuffle completely each time.",
        "Use <code>hash_fn=len</code>. Words of the same length collide, which is "
        "a much more realistic bad hash than the constant one.",
        "Swap chaining for open addressing: on a collision, step to the next free "
        "slot. Deletion becomes the hard part &mdash; and that is why tombstones "
        "exist.",
    ],
},

"dsa/binary_search_trees.html": {
    "file": "bst.py",
    "intro": "Insert, search, in-order traversal and delete &mdash; including the "
             "two-child delete that everyone gets wrong. The last block inserts "
             "sorted keys to show the tree collapsing into a linked list.",
    "code": '''# A binary search tree: everything left is smaller, everything right larger.

class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None


def insert(node, key):
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)     # rebuild the link on the way out
    elif key > node.key:
        node.right = insert(node.right, key)
    return node                                # equal keys: ignored


def search(node, key, depth=1):
    if node is None:
        return None, depth
    if key == node.key:
        return node, depth
    if key < node.key:
        return search(node.left, key, depth + 1)
    return search(node.right, key, depth + 1)


def inorder(node, out=None):
    if out is None:
        out = []
    if node:
        inorder(node.left, out)                # left
        out.append(node.key)                   # self
        inorder(node.right, out)               # right
    return out


def height(node):
    return 0 if node is None else 1 + max(height(node.left), height(node.right))


def delete(node, key):
    if node is None:
        return None
    if key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:
        if node.left is None:                  # 0 or 1 child: promote it
            return node.right
        if node.right is None:
            return node.left
        successor = node.right                 # 2 children: smallest on the right
        while successor.left:
            successor = successor.left
        node.key = successor.key               # copy it up
        node.right = delete(node.right, successor.key)
    return node


root = None
for key in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, key)

print("in-order  :", inorder(root), "  <- always sorted")
print("height    :", height(root))
for key in (40, 65):
    node, depth = search(root, key)
    print(f"search {key}: {'found' if node else 'not found'} after {depth} comparisons")

root = delete(root, 30)          # one child
root = delete(root, 50)          # two children - the interesting case
print("after deleting 30 and 50:", inorder(root))

print()
degenerate = None
for key in [10, 20, 30, 40, 50, 60, 70]:        # sorted input
    degenerate = insert(degenerate, key)
print("sorted input -> height", height(degenerate), "for 7 nodes")
print("That is a linked list. Search is O(n), and this is why AVL and")
print("red-black trees exist.")
''',
    "walk": [
        ("node.left = insert(node.left, key)",
         "Assigning the result back is what builds the tree. The recursive call "
         "returns either the existing subtree or a brand-new node, and this line "
         "does not need to know which."),
        ("if key < node.key: ... else: right",
         "One comparison discards an entire subtree, exactly like binary search "
         "on an array &mdash; the tree is that algorithm made into a structure "
         "that can also be inserted into cheaply."),
        ("inorder: left, self, right",
         "Visiting in that order emits the keys in sorted order, for free and "
         "without sorting anything. Change the position of the "
         "<code>append</code> and you have pre-order or post-order instead."),
        ("successor = node.right; while successor.left:",
         "Deleting a node with two children means finding the next key in sorted "
         "order &mdash; the leftmost node of the right subtree &mdash; copying it "
         "up, and deleting that instead. It is guaranteed to have at most one "
         "child, so the hard case reduces to an easy one."),
        ("sorted input -> height 7",
         "A BST's O(log n) is a property of its <em>shape</em>, not its "
         "definition. Sorted input produces one long spine, and every operation "
         "degrades to O(n). Self-balancing trees exist entirely to prevent this."),
    ],
    "try": [
        "Insert <code>[50, 30, 70, ...]</code> shuffled with "
        "<code>random.shuffle</code> and print the height each time. Random order "
        "gives O(log n) with high probability &mdash; that is the usual defence.",
        "Delete a leaf, a one-child node and the root, and print the traversal "
        "after each. It stays sorted, which is the invariant to test against.",
        "Add a <code>count</code> to each node instead of ignoring duplicate "
        "keys. That is how a BST becomes a multiset.",
    ],
},

"dsa/heaps_and_priority_queues.html": {
    "file": "heap.py",
    "intro": "A binary heap written from scratch on a plain list, then the same "
             "job handed to <code>heapq</code>. The point of the first half is "
             "that the tree is entirely imaginary &mdash; there are no nodes and "
             "no pointers.",
    "code": '''# A min-heap: the smallest item is always at index 0.
import heapq

class MinHeap:
    def __init__(self):
        self.a = []

    def push(self, x):
        self.a.append(x)                 # put it at the end...
        i = len(self.a) - 1
        while i > 0:                     # ...and bubble it up
            parent = (i - 1) // 2
            if self.a[parent] <= self.a[i]:
                break
            self.a[parent], self.a[i] = self.a[i], self.a[parent]
            i = parent

    def pop(self):
        smallest = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last             # move the last item to the root...
            i = 0
            while True:                  # ...and sift it down
                left, right = 2 * i + 1, 2 * i + 2
                child = left
                if right < len(self.a) and self.a[right] < self.a[left]:
                    child = right
                if child >= len(self.a) or self.a[i] <= self.a[child]:
                    break
                self.a[i], self.a[child] = self.a[child], self.a[i]
                i = child
        return smallest


h = MinHeap()
for x in [5, 3, 8, 1, 9, 2]:
    h.push(x)
    print(f"push {x} -> {h.a}")
print()
print("popped in order:", [h.pop() for _ in range(6)])

print()
print("The list IS the tree. Index i's children are 2i+1 and 2i+2:")
tree = [1, 3, 2, 5, 9, 8]
for i, value in enumerate(tree):
    kids = [tree[j] for j in (2 * i + 1, 2 * i + 2) if j < len(tree)]
    print(f"  index {i} = {value:>2}, children {kids}")

# --- the same thing, using the standard library ------------------------
print()
tasks = [(3, "write tests"), (1, "fix the outage"), (2, "review PR")]
heapq.heapify(tasks)                     # O(n), not O(n log n)
while tasks:
    priority, name = heapq.heappop(tasks)
    print(f"  priority {priority}: {name}")

# Top-k without sorting the whole list.
data = [17, 4, 92, 8, 55, 23, 71, 3]
print()
print("3 largest:", heapq.nlargest(3, data), "- O(n log k), not O(n log n)")
''',
    "walk": [
        ("parent = (i - 1) // 2",
         "The tree exists only as arithmetic. A node at index <em>i</em> has its "
         "parent at <code>(i-1)//2</code> and children at <code>2i+1</code> and "
         "<code>2i+2</code> &mdash; no pointers are stored, and none are needed."),
        ("if self.a[parent] <= self.a[i]: break",
         "A heap is a much weaker promise than a sorted list: each parent beats "
         "its own children, and nothing is claimed about siblings. That weakness "
         "is why push and pop cost O(log n) instead of O(n)."),
        ("last = self.a.pop(); self.a[0] = last",
         "Popping the root leaves a hole, and the only item that can be removed "
         "without leaving a second hole is the last one. Moving it to the root "
         "and sifting down repairs the heap in one pass."),
        ("if right < len(self.a) and self.a[right] < self.a[left]:",
         "Always sift towards the <em>smaller</em> child. Choosing the larger one "
         "makes it a valid-looking heap that returns wrong answers &mdash; a "
         "quiet bug rather than a crash."),
        ("heapq.nlargest(3, data)",
         "Keeps a heap of size k rather than sorting everything: O(n log k). For "
         "“top 10 of a billion” that is the difference between practical and not."),
    ],
    "try": [
        "Print <code>h.a</code> after all the pushes. It is not sorted &mdash; "
        "only <code>a[0]</code> is guaranteed, and expecting more is the usual "
        "misunderstanding.",
        "Flip both comparisons to build a max-heap. Python's "
        "<code>heapq</code> has no max version, so real code pushes "
        "<code>-value</code> instead.",
        "Push <code>(priority, task)</code> tuples where two priorities tie and "
        "the second item is not comparable. The <code>TypeError</code> is why "
        "production code pushes a counter as a tie-breaker.",
    ],
},

"dsa/trie_prefix_tree.html": {
    "file": "trie.py",
    "intro": "A trie built from a handful of words, with the node count printed "
             "against the character count so the sharing is visible. Then "
             "autocomplete, which is the operation a hash table cannot do at all.",
    "code": '''# A trie: one node per character, with common prefixes shared.

class TrieNode:
    def __init__(self):
        self.children = {}           # character -> TrieNode
        self.is_word = False         # does a word END here?


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.nodes = 1

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self.nodes += 1      # a genuinely new node
            node = node.children[ch]
        node.is_word = True          # mark the end, do not add a node

    def _walk(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def contains(self, word):
        node = self._walk(word)
        return node is not None and node.is_word     # both conditions matter

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def complete(self, prefix):
        node = self._walk(prefix)
        found = []
        def collect(node, so_far):
            if node.is_word:
                found.append(so_far)
            for ch, child in sorted(node.children.items()):
                collect(child, so_far + ch)
        if node:
            collect(node, prefix)
        return found


words = ["car", "card", "care", "careful", "cat", "dog", "do"]
trie = Trie()
for w in words:
    trie.insert(w)

print("words     :", words)
print("characters:", sum(len(w) for w in words))
print("trie nodes:", trie.nodes, "- shared prefixes are stored once")

print()
for probe in ["car", "ca", "cart", "do"]:
    print(f"  contains({probe!r:>8}) = {str(trie.contains(probe)):>5}   "
          f"starts_with = {trie.starts_with(probe)}")

print()
for prefix in ["car", "d", "z"]:
    print(f"  complete({prefix!r}) -> {trie.complete(prefix)}")
print()
print("Lookup costs O(length of the word) - the number of words never enters into it.")
''',
    "walk": [
        ("self.children = {}",
         "A dictionary per node rather than a fixed array of 26. It costs more "
         "per node and handles any alphabet, including Unicode &mdash; the "
         "array version is faster and quietly assumes lowercase ASCII."),
        ("self.is_word = False",
         "The flag is why <code>\"ca\"</code> is not a word even though the path "
         "exists, and why <code>\"do\"</code> is one even though "
         "<code>\"dog\"</code> continues past it. Without it a trie can only "
         "answer prefix questions."),
        ("for ch in word: node = node.children[ch]",
         "Lookup walks one node per character, so it costs O(length) no matter "
         "how many words are stored. A hash table also gets O(1)-ish, but it "
         "must hash the whole string first &mdash; also O(length)."),
        ("trie.nodes vs sum(len(w))",
         "The saving is real but modest, and it comes entirely from shared "
         "prefixes. A trie over unrelated strings uses more memory than storing "
         "them in a set."),
        ("def collect(node, so_far):",
         "Autocomplete is a DFS from the prefix node. This is the operation a "
         "hash table simply cannot perform &mdash; hashing destroys the "
         "relationship between <code>\"car\"</code> and <code>\"card\"</code>."),
    ],
    "try": [
        "Insert <code>\"carpet\"</code> and re-print the node count. It adds "
        "three nodes, not six &mdash; <code>car</code> was already there.",
        "Insert a hundred unrelated random strings and compare "
        "<code>trie.nodes</code> with the character count. The saving vanishes.",
        "Add <code>delete</code>. The awkward part is knowing when a node may be "
        "removed: only when it ends no word and has no children.",
    ],
},

}


# =========================================================================
# Techniques
# =========================================================================

TECHNIQUES = {

"dsa/recursion_and_call_stack.html": {
    "file": "recursion.py",
    "intro": "Factorial with its frames printed as they are pushed and popped, "
             "then the same problem written as a loop, then the recursion limit "
             "hit on purpose &mdash; because a stack overflow is much easier to "
             "understand once you have caused one.",
    "code": '''# Recursion, and the stack that makes it work.
import sys

def factorial(n, depth=0):
    pad = "|  " * depth
    print(f"{pad}call factorial({n})")
    if n <= 1:                       # base case: stop, do not recurse
        print(f"{pad}return 1")
        return 1
    result = n * factorial(n - 1, depth + 1)     # frame waits here
    print(f"{pad}return {n} * {result // n} = {result}")
    return result


print(factorial(4))

# The same computation with no stack at all.
def factorial_loop(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


print()
print("iterative:", factorial_loop(4))

# --- what the stack costs ----------------------------------------------
def depth_reached(n):
    """How deep can we go before Python refuses?"""
    try:
        return 1 + depth_reached(n + 1)
    except RecursionError:
        return 0


print()
print("Python's recursion limit:", sys.getrecursionlimit())
print("frames we actually got   :", depth_reached(0))
print("Each frame holds arguments, locals and a return address. That is memory,")
print("and it is why deep recursion is a space cost, not just a style choice.")

# --- the cost of recomputing -------------------------------------------
calls = 0

def fib(n):
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print()
for n in (10, 20, 25):
    calls = 0
    value = fib(n)
    print(f"fib({n}) = {value:>6}  after {calls:>7} calls")
print("Calls roughly double per +1. The tree of frames is the problem, and")
print("memoisation - see the dynamic programming module - is the fix.")
''',
    "walk": [
        ("if n <= 1: return 1",
         "The base case, and the only thing standing between this function and a "
         "crash. Every recursive function needs one, and every call must make "
         "measurable progress towards it."),
        ("result = n * factorial(n - 1, depth + 1)",
         "The multiplication happens <em>after</em> the recursive call returns, so "
         "the frame has to stay alive while the whole subtree below it runs. That "
         "is precisely what the call stack is holding."),
        ("the indented print pairs",
         "Each <code>call</code> line has a matching <code>return</code> at the "
         "same indent. Read downwards for the pushes and upwards for the pops "
         "&mdash; the output is the stack, drawn over time."),
        ("except RecursionError: return 0",
         "Python caps the depth deliberately, because the real C stack underneath "
         "would otherwise be overrun and the process would die rather than raise. "
         "The limit is a guard rail, not the actual capacity."),
        ("calls += 1 in fib",
         "Naive <code>fib</code> recomputes the same subproblems exponentially "
         "often. Recursion is not slow; recursion without memory is."),
    ],
    "try": [
        "Delete the base case from <code>factorial</code>. The "
        "<code>RecursionError</code> traceback is what an infinite recursion "
        "looks like from the inside.",
        "Call <code>fib(30)</code> and then <code>fib(32)</code>. Roughly four "
        "times the calls for two more terms &mdash; and it is about to get much "
        "worse.",
        "Rewrite <code>factorial</code> so the recursive call is the last thing "
        "it does (pass the accumulator down). That is tail recursion &mdash; and "
        "CPython still will not optimise it away.",
    ],
},

"dsa/dynamic_programming.html": {
    "file": "dynamic_programming.py",
    "intro": "The same Fibonacci written three ways, with the call counts printed "
             "side by side, then a coin-change table you can read row by row. "
             "The gap between 240,000 calls and 26 is the entire subject.",
    "code": '''# Dynamic programming: solve each subproblem once, then reuse the answer.

calls = {"naive": 0, "memo": 0}

def fib_naive(n):
    calls["naive"] += 1
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n, cache=None):
    if cache is None:
        cache = {}
    calls["memo"] += 1
    if n in cache:                      # already solved: reuse it
        return cache[n]
    value = n if n < 2 else fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    cache[n] = value                    # top-down: remember on the way out
    return value


def fib_table(n):
    table = [0, 1] + [0] * (n - 1)      # bottom-up: no recursion at all
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]


N = 25
print(f"fib({N}) =", fib_naive(N), f"in {calls['naive']} calls")
print(f"fib({N}) =", fib_memo(N), f"in {calls['memo']} calls")
print(f"fib({N}) =", fib_table(N), "in one loop, O(1) memory if you keep two values")

# --- coin change: the classic table ------------------------------------
def coin_change(coins, target):
    # best[t] = fewest coins that make t; inf means "cannot be made"
    best = [0] + [float("inf")] * target
    for t in range(1, target + 1):
        for c in coins:
            if c <= t and best[t - c] + 1 < best[t]:
                best[t] = best[t - c] + 1
    return best


coins = [1, 3, 4]
target = 11
best = coin_change(coins, target)
print()
print(f"coins {coins}, making every amount up to {target}:")
print("  amount:", "".join(f"{t:>4}" for t in range(target + 1)))
print("  coins :", "".join(f"{c:>4}" for c in best))
print()
print(f"{target} needs {best[target]} coins (4+4+3).")
print("Greedy would take 4+4+1+1+1 = 5. Each cell here was computed once and")
print("read many times - that is the whole method.")
''',
    "walk": [
        ("if n in cache: return cache[n]",
         "Memoisation in one line. The recursion is unchanged; it simply stops "
         "descending into a subtree whose answer is already known, which collapses "
         "an exponential tree into a linear path."),
        ("cache[n] = value",
         "Top-down: the answer is stored on the way back out. The structure of "
         "the code still mirrors the recurrence, which is why memoisation is "
         "usually the easier of the two directions to write."),
        ("table = [0, 1] + [0] * (n - 1)",
         "Bottom-up: fill the small cases first and build upwards, so no call "
         "stack is involved at all. Same complexity, no recursion limit, and "
         "usually faster in practice."),
        ("if c <= t and best[t - c] + 1 < best[t]:",
         "The recurrence, and it is the only piece of real thinking in the whole "
         "method: the best way to make <em>t</em> is one coin on top of the best "
         "way to make <em>t &minus; c</em>, for whichever c wins."),
        ("best[t - c]",
         "Reading a cell that was filled earlier in the same loop. Dynamic "
         "programming needs subproblems that <em>overlap</em> &mdash; if each one "
         "were used once, a table would buy nothing over plain recursion."),
    ],
    "try": [
        "Raise <code>N</code> to 30 and watch the naive count. Around 35 it stops "
        "being a demonstration and starts being a wait.",
        "Print the whole <code>best</code> row for <code>coins = [1, 5, 10, 25]</code>. "
        "Every value matches the greedy answer &mdash; which is exactly why greedy "
        "appears to work on real currency.",
        "Track which coin won each cell in a second list, then walk it backwards "
        "to recover the actual coins rather than just the count.",
    ],
},

"dsa/greedy_algorithms.html": {
    "file": "greedy.py",
    "intro": "Two greedy algorithms: one that is provably optimal and one that is "
             "confidently wrong, on inputs that differ only in the coin "
             "denominations. Both are checked against an exhaustive answer in the "
             "same run.",
    "code": '''# Greedy: take the best-looking option now and never reconsider.
from itertools import combinations

def greedy_coins(coins, target):
    chosen = []
    for c in sorted(coins, reverse=True):    # biggest first
        while target >= c:
            target -= c
            chosen.append(c)
    return chosen if target == 0 else None


def optimal_coins(coins, target):
    """Brute force, for checking the greedy answer against."""
    best = [0] + [float("inf")] * target
    for t in range(1, target + 1):
        for c in coins:
            if c <= t:
                best[t] = min(best[t], best[t - c] + 1)
    return best[target]


for coins, target in [([1, 5, 10, 25], 63), ([1, 3, 4], 6), ([1, 7, 10], 15)]:
    got = greedy_coins(coins, target)
    best = optimal_coins(coins, target)
    verdict = "optimal" if len(got) == best else f"WRONG - {best} would do"
    print(f"coins {str(coins):>14} target {target:>3}: greedy took {len(got)} "
          f"{got}  {verdict}")

# --- a greedy algorithm that is always right ---------------------------
meetings = [("a", 1, 4), ("b", 3, 5), ("c", 0, 6), ("d", 5, 7),
            ("e", 3, 9), ("f", 5, 9), ("g", 6, 10), ("h", 8, 11)]

def activity_selection(meetings):
    chosen, finish = [], 0
    for name, start, end in sorted(meetings, key=lambda m: m[2]):   # by END time
        if start >= finish:
            chosen.append(name)
            finish = end
            print(f"  take {name} ({start}-{end}), room free again at {finish}")
        else:
            print(f"  skip {name} ({start}-{end}), clashes")
    return chosen


print()
print("booking one room, most meetings possible:")
chosen = activity_selection(meetings)
print("chosen:", chosen, f"({len(chosen)} meetings)")

# The same problem, greedy on the WRONG key.
by_start = []
finish = 0
for name, start, end in sorted(meetings, key=lambda m: m[1]):       # by START
    if start >= finish:
        by_start.append(name)
        finish = end
print("greedy by start time instead:", by_start, f"({len(by_start)} meetings)")
''',
    "walk": [
        ("for c in sorted(coins, reverse=True):",
         "The greedy choice: largest coin that still fits. It is optimal for "
         "British, US and euro denominations, and that familiarity is exactly why "
         "people assume it is optimal in general."),
        ("([1, 3, 4], 6)",
         "The counterexample. Greedy takes 4 + 1 + 1; two 3s would do. Nothing "
         "about the algorithm changed &mdash; only the denominations &mdash; and "
         "it fails silently, with a plausible-looking answer."),
        ("optimal_coins(...)",
         "A dynamic programming check run alongside, so the verdict is computed "
         "rather than asserted. This is also the practical test for whether a "
         "greedy idea is safe: compare it to brute force on small inputs."),
        ("sorted(meetings, key=lambda m: m[2])   # by END",
         "Sorting by finish time is what makes activity selection provably "
         "optimal: taking the meeting that frees the room earliest can never "
         "shut out a better schedule. There is a real exchange argument behind "
         "that, and it is what separates this from the coin case."),
        ("sorted by m[1]   # by START",
         "The same greedy structure on a different key, and it loses immediately "
         "&mdash; one long early meeting blocks several short ones. Greedy is "
         "not a strategy on its own; the choice of key <em>is</em> the algorithm."),
    ],
    "try": [
        "Find another denomination set where greedy fails. They are easy to "
        "construct once you look for a coin that is more than twice the one "
        "below it.",
        "Sort the meetings by duration instead. Shortest-first sounds "
        "reasonable and is also wrong; build the input that breaks it.",
        "Add a meeting that spans the entire day. Both strategies now have to "
        "reject something, and only one of them rejects the right thing.",
    ],
},

"dsa/divide_and_conquer.html": {
    "file": "divide_and_conquer.py",
    "intro": "Two problems that look nothing alike solved by the same shape: fast "
             "exponentiation, which turns 1,000 multiplications into 10, and "
             "counting inversions during a merge, which does in n log n what the "
             "obvious loop does in n².",
    "code": '''# Divide and conquer: split, solve the pieces, combine.

# --- 1. exponentiation by squaring -------------------------------------
def power(base, exp, depth=0):
    pad = "  " * depth
    if exp == 0:
        return 1
    half = power(base, exp // 2, depth + 1)      # ONE recursive call, not two
    result = half * half
    if exp % 2:
        result *= base                           # odd: one extra factor
    print(f"{pad}power({base}, {exp}) = {result}")
    return result


print("2 ** 10 by squaring:")
print("result:", power(2, 10))
print("multiplications: about log2(10) = 4, not 10")

# --- 2. counting inversions while merge sorting ------------------------
def sort_and_count(a):
    if len(a) <= 1:
        return a, 0
    mid = len(a) // 2
    left, x = sort_and_count(a[:mid])
    right, y = sort_and_count(a[mid:])

    merged, z = [], 0
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            # left[i:] are ALL bigger than right[j], so they are all inversions
            z += len(left) - i
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, x + y + z


def count_brute(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


data = [2, 4, 1, 3, 5, 8, 7, 6]
sorted_data, inversions = sort_and_count(data)
print()
print("list       :", data)
print("sorted     :", sorted_data)
print("inversions :", inversions, "(brute force agrees:", count_brute(data), ")")
print()
print("Brute force compares every pair: O(n^2).")
print("The merge counts them in blocks while it is sorting anyway: O(n log n).")
''',
    "walk": [
        ("half = power(base, exp // 2, depth + 1)",
         "One recursive call, and its result is used twice. Writing "
         "<code>power(b, n//2) * power(b, n//2)</code> instead looks identical "
         "and is exponentially slower &mdash; the saving is in reusing the value, "
         "not in the halving."),
        ("if exp % 2: result *= base",
         "Handles the odd case, where halving loses a factor. This is where "
         "off-by-one errors live in every implementation of this function."),
        ("left, x = sort_and_count(a[:mid])",
         "The divide step. Each half is solved independently, and the returned "
         "count is the number of inversions <em>within</em> that half."),
        ("z += len(left) - i",
         "The combine step, and the clever line. When an item from the right half "
         "wins, every remaining item on the left is greater than it, so they are "
         "all inversions &mdash; counted in one addition instead of one by one."),
        ("x + y + z",
         "Left, right, and across. Every inversion is in exactly one of those "
         "three categories, which is the proof that the count is complete. That "
         "decomposition is the divide-and-conquer pattern in general."),
    ],
    "try": [
        "Compute <code>power(2, 1000)</code>. Ten recursive calls, and Python's "
        "unbounded integers print the whole 302-digit result.",
        "Run the inversion counter on a reversed list of 12 items. The answer is "
        "n(n&minus;1)/2, the maximum possible &mdash; and it is the same number "
        "insertion sort would charge you in shifts.",
        "Time both counters on a list of 2,000 random numbers. The brute force "
        "does two million comparisons; the merge does about twenty thousand.",
    ],
},

"dsa/backtracking.html": {
    "file": "backtracking.py",
    "intro": "Eight queens, solved by placing one and undoing it when it fails, "
             "with the number of positions actually examined printed against the "
             "number a brute-force search would have tried. The ratio is why "
             "backtracking exists.",
    "code": '''# Backtracking: place, recurse, and undo the placement if it fails.

N = 8
nodes = 0

def safe(queens, row, col):
    for r, c in enumerate(queens):
        if c == col or abs(r - row) == abs(c - col):    # same column or diagonal
            return False
    return True


def solve(queens, first_only=True, found=None):
    global nodes
    found = [] if found is None else found
    row = len(queens)
    if row == N:                          # all N placed: a solution
        found.append(list(queens))
        return found
    for col in range(N):
        nodes += 1
        if safe(queens, row, col):
            queens.append(col)            # place
            solve(queens, first_only, found)
            queens.pop()                  # UNDO - this is the backtrack
            if first_only and found:
                return found
    return found


solutions = solve([], first_only=True)
board = solutions[0]
print(f"first solution for {N} queens: {board}")
for row, col in enumerate(board):
    print("  " + " ".join("Q" if c == col else "." for c in range(N)))

print()
print(f"positions examined      : {nodes:,}")
brute = N ** N
print(f"brute force would try   : {brute:,}  (every column for every row)")
print(f"pruning removed          : {100 * (1 - nodes / brute):.4f}% of the space")

nodes = 0
all_solutions = solve([], first_only=False)
print()
print(f"all solutions for {N} queens: {len(all_solutions)}")
print(f"positions examined       : {nodes:,}")
''',
    "walk": [
        ("row = len(queens)",
         "The state is just a list of column choices, one per row, so the depth "
         "of the recursion <em>is</em> the row being filled. Encoding one queen "
         "per row also removes the entire “two queens in a row” case for free."),
        ("if c == col or abs(r - row) == abs(c - col):",
         "The whole conflict test. Two squares are on a diagonal exactly when the "
         "row difference equals the column difference &mdash; no board array is "
         "needed at all."),
        ("queens.append(col) ... queens.pop()",
         "Place, explore, undo. The <code>pop</code> is the backtrack, and "
         "forgetting it is the classic bug: the state leaks into sibling branches "
         "and the search quietly explores nonsense."),
        ("if safe(queens, row, col):",
         "The pruning. A partial placement that already conflicts is abandoned "
         "before any of its N^(remaining rows) completions are generated &mdash; "
         "which is where the percentage printed at the end comes from."),
        ("nodes vs N ** N",
         "16.7 million positions in the naive space against a few thousand "
         "actually examined. Backtracking is still exponential in the worst case; "
         "it is simply exponential in a far smaller space."),
    ],
    "try": [
        "Drop <code>N</code> to 4 and print the board at every placement. On a "
        "small board the place-and-undo rhythm is short enough to read in full.",
        "Delete <code>queens.pop()</code>. The search finds nothing and examines "
        "far fewer nodes &mdash; a wrong answer that looks like an optimisation.",
        "Raise <code>N</code> to 10 with <code>first_only=False</code>. 724 "
        "solutions, and the node count shows what one extra row costs.",
    ],
},

"dsa/two_pointers.html": {
    "file": "two_pointers.py",
    "intro": "Three uses of the same idea &mdash; pair sum, in-place duplicate "
             "removal, and palindrome checking &mdash; each with its pointer "
             "positions printed, and each replacing a nested loop.",
    "code": '''# Two pointers: walk a sorted list from both ends, or at two speeds.

# --- 1. find a pair that sums to the target ----------------------------
def pair_sum(a, target):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        total = a[lo] + a[hi]
        print(f"  lo={lo} ({a[lo]:>2})  hi={hi} ({a[hi]:>2})  sum={total:>3}", end="")
        if total == target:
            print("  <- match")
            return lo, hi
        if total < target:
            print("  too small, move lo right")
            lo += 1                     # only a bigger left value can help
        else:
            print("  too big, move hi left")
            hi -= 1                     # only a smaller right value can help
    return None


data = [1, 3, 4, 6, 8, 10, 13]
print("sorted:", data, " target 14")
print("pair:", pair_sum(data, 14))
print(f"comparisons: at most {len(data)}, against {len(data) ** 2 // 2} for nested loops")

# --- 2. remove duplicates in place, O(1) extra memory ------------------
def dedupe(a):
    if not a:
        return 0
    write = 1                           # slow pointer: end of the kept region
    for read in range(1, len(a)):       # fast pointer: scans everything
        if a[read] != a[write - 1]:
            a[write] = a[read]
            write += 1
    return write


values = [1, 1, 2, 2, 2, 3, 4, 4, 5]
n = dedupe(values)
print()
print("deduped:", values[:n], f"(kept {n}, list not reallocated)")
print("tail left over:", values[n:])

# --- 3. palindrome, ignoring anything that is not a letter -------------
def is_palindrome(text):
    lo, hi = 0, len(text) - 1
    while lo < hi:
        while lo < hi and not text[lo].isalnum():
            lo += 1
        while lo < hi and not text[hi].isalnum():
            hi -= 1
        if text[lo].lower() != text[hi].lower():
            return False
        lo, hi = lo + 1, hi - 1
    return True


print()
for text in ["A man, a plan, a canal: Panama", "race a car"]:
    print(f"  {text!r:>34}: {is_palindrome(text)}")
''',
    "walk": [
        ("while lo < hi:",
         "Strictly less than, so the two pointers never land on the same element "
         "&mdash; which would pair a value with itself. Every two-pointer loop "
         "lives or dies on this condition."),
        ("if total < target: lo += 1",
         "The move is justified, not guessed. The list is sorted, so with "
         "<code>a[hi]</code> as the largest available partner, <code>a[lo]</code> "
         "cannot be part of any solution &mdash; discarding it is safe."),
        ("lo += 1 / hi -= 1",
         "Each step eliminates a whole row or column of the pair table, so the "
         "n² candidates are covered in n steps. That is the trick, and it only "
         "works because the input is sorted."),
        ("write = 1; for read in range(1, len(a)):",
         "The other variant: both pointers move forwards, at different rates. "
         "<code>write</code> marks the end of the kept prefix and "
         "<code>read</code> scans ahead &mdash; nothing is allocated."),
        ("while lo < hi and not text[lo].isalnum():",
         "The inner skips also need the <code>lo &lt; hi</code> guard, or a string "
         "of pure punctuation runs a pointer off the end. Nested pointer loops "
         "are where the index errors hide."),
    ],
    "try": [
        "Shuffle <code>data</code> before calling <code>pair_sum</code>. It "
        "returns <code>None</code> for a pair that exists &mdash; sortedness is a "
        "precondition, not a nicety.",
        "Print <code>values</code> in full after <code>dedupe</code>. The tail is "
        "stale data, which is why the function returns a length rather than a "
        "list.",
        "Extend <code>pair_sum</code> to three numbers: fix one, two-pointer the "
        "rest. O(n²) instead of O(n³), and the standard answer to 3Sum.",
    ],
},

"dsa/sliding_window.html": {
    "file": "sliding_window.py",
    "intro": "A fixed window and a variable one. The first shows the recomputation "
             "the technique removes; the second grows and shrinks on demand, which "
             "is where most of the real problems live.",
    "code": '''# Sliding window: reuse the previous window instead of recomputing it.

# --- 1. fixed size: best sum of k consecutive items ---------------------
def max_sum_naive(a, k):
    ops = 0
    best = float("-inf")
    for i in range(len(a) - k + 1):
        total = 0
        for j in range(i, i + k):       # recompute the whole window
            total += a[j]
            ops += 1
        best = max(best, total)
    return best, ops


def max_sum_window(a, k):
    ops = 0
    total = sum(a[:k])
    ops += k
    best = total
    for i in range(k, len(a)):
        total += a[i] - a[i - k]        # one add, one subtract. That is all.
        ops += 2
        print(f"  window {a[i-k+1:i+1]} sum={total}")
        best = max(best, total)
    return best, ops


data = [2, 1, 5, 1, 3, 2, 7, 1]
k = 3
print(f"data {data}, window {k}")
best, ops = max_sum_window(data, k)
print("best:", best)
naive_best, naive_ops = max_sum_naive(data, k)
print(f"operations: window {ops}, recomputing {naive_ops}")

# --- 2. variable size: longest run with no repeated character ----------
def longest_unique(text):
    seen = {}                           # character -> last index it appeared at
    start = best = 0
    best_text = ""
    for i, ch in enumerate(text):
        if ch in seen and seen[ch] >= start:
            start = seen[ch] + 1        # jump the left edge past the repeat
        seen[ch] = i
        if i - start + 1 > best:
            best = i - start + 1
            best_text = text[start:i + 1]
        print(f"  i={i} {ch!r} window={text[start:i+1]!r}")
    return best, best_text


print()
print("longest substring with no repeats, in 'abcabcbb':")
length, text = longest_unique("abcabcbb")
print("best:", length, repr(text))
''',
    "walk": [
        ("total += a[i] - a[i - k]",
         "The whole technique in one line: add what just entered, subtract what "
         "just left. The window's value is carried forward rather than rebuilt, "
         "turning O(n&middot;k) into O(n)."),
        ("total = sum(a[:k])",
         "The first window still has to be computed the slow way. Every sliding "
         "window has this setup step, and it is a common place to get the bounds "
         "wrong by one."),
        ("if ch in seen and seen[ch] >= start:",
         "The second condition is the subtle one. A repeat only matters if it is "
         "<em>inside</em> the current window; an older occurrence already fell "
         "off the left edge and must be ignored."),
        ("start = seen[ch] + 1",
         "The left edge jumps straight past the previous occurrence instead of "
         "creeping forward one at a time. Both are correct; this one keeps the "
         "whole scan linear."),
        ("i - start + 1",
         "The window length, and the reason the dictionary stores indices rather "
         "than counts. Storing counts works too, but then the left edge has to "
         "walk, and the code gets longer."),
    ],
    "try": [
        "Raise <code>k</code> to 6 and compare the two operation counts again. "
        "The gap grows with the window, because the naive version pays for it "
        "every step.",
        "Run <code>longest_unique</code> on <code>\"abba\"</code>. The second "
        "<code>a</code> is what the <code>seen[ch] &gt;= start</code> guard is "
        "protecting against &mdash; drop it and the answer is wrong.",
        "Adapt the fixed window to a running <em>average</em>. Same two lines, "
        "and it is how a moving average over a data stream is actually computed.",
    ],
},

"dsa/kmp_string_matching.html": {
    "file": "kmp.py",
    "intro": "The prefix table built and printed for a pattern with real internal "
             "repetition, then the search, then a comparison count against the "
             "naive matcher on the input that makes naive matching look bad.",
    "code": '''# Knuth-Morris-Pratt: never re-examine a character of the text.

def build_lps(pattern):
    """lps[i] = length of the longest proper prefix of pattern[:i+1]
    that is also a suffix of it."""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]     # fall back, do NOT restart at 0
        else:
            lps[i] = 0
            i += 1
    return lps


pattern = "ababaca"
lps = build_lps(pattern)
print("pattern:", " ".join(pattern))
print("lps    :", " ".join(str(x) for x in lps))
print("lps[4]=3 because 'ababa' starts and ends with 'aba'.")


def kmp_search(text, pattern):
    lps = build_lps(pattern)
    hits, comparisons = [], 0
    i = j = 0                            # i walks the text, j the pattern
    while i < len(text):
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                hits.append(i - j)
                j = lps[j - 1]           # keep going for overlapping matches
        elif j:
            j = lps[j - 1]               # slide the pattern, i never moves back
        else:
            i += 1
    return hits, comparisons


def naive_search(text, pattern):
    hits, comparisons = [], 0
    for i in range(len(text) - len(pattern) + 1):
        for j in range(len(pattern)):
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
        else:
            hits.append(i)
    return hits, comparisons


text = "abababacabababacaba"
print()
print("text   :", text)
print("KMP    :", kmp_search(text, pattern))
print("naive  :", naive_search(text, pattern))

# The input designed to make naive matching look bad.
print()
bad_text = "a" * 300 + "b"
bad_pattern = "a" * 20 + "b"
for name, fn in [("naive", naive_search), ("KMP", kmp_search)]:
    hits, comparisons = fn(bad_text, bad_pattern)
    print(f"  {name:>5}: {comparisons:>6} comparisons, hits at {hits}")
''',
    "walk": [
        ("length = lps[length - 1]",
         "The line that makes the table build linear, and the one that looks "
         "wrong. On a mismatch the fallback is to the next-best border already "
         "computed &mdash; the table is built using itself."),
        ("lps[i]",
         "For each prefix, how much of it is also a suffix of itself. That "
         "overlap is the only thing KMP needs in order to know how far it may "
         "safely slide after a mismatch."),
        ("elif j: j = lps[j - 1]",
         "The search's whole trick. On a mismatch the pattern slides forward "
         "while <code>i</code> stays put, because the table already proves the "
         "skipped alignments cannot match."),
        ("i never decreases",
         "Every character of the text is looked at a bounded number of times, "
         "which is the O(n + m) guarantee. Naive matching restarts at "
         "<code>i - j + 1</code> and can re-read the same characters over and "
         "over."),
        ("j = lps[j - 1] after a hit",
         "Falling back rather than resetting to 0 is what finds overlapping "
         "occurrences. Set it to 0 and searching for <code>\"aaa\"</code> in "
         "<code>\"aaaaa\"</code> reports one match instead of three."),
    ],
    "try": [
        "Build the table for <code>\"aaaa\"</code> and for <code>\"abcd\"</code>. "
        "One is all overlap, the other has none &mdash; the two extremes of what "
        "the table can say.",
        "Lengthen <code>bad_text</code> to 3,000 a's. The naive count grows "
        "quadratically while the KMP count grows linearly.",
        "Search for <code>\"aa\"</code> in <code>\"aaaa\"</code>. Three "
        "overlapping hits &mdash; then set the post-hit line to "
        "<code>j = 0</code> and watch one disappear.",
    ],
},

"dsa/big_o_notation.html": {
    "file": "big_o.py",
    "intro": "Five complexity classes, each with its operations counted rather "
             "than argued about, at three input sizes. The last block shows an "
             "O(n²) algorithm beating an O(n log n) one, which is the part the "
             "notation deliberately hides.",
    "code": '''# Big-O, counted. Every function below returns how much work it did.
import time

def constant(a):                     # O(1)
    ops = 1
    return a[len(a) // 2], ops

def logarithmic(a, target):          # O(log n)
    lo, hi, ops = 0, len(a) - 1, 0
    while lo <= hi:
        ops += 1
        mid = (lo + hi) // 2
        if a[mid] == target:
            break
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return ops

def linear(a):                       # O(n)
    ops = 0
    for _ in a:
        ops += 1
    return ops

def linearithmic(a):                 # O(n log n) - merge sort's shape
    if len(a) <= 1:
        return 0
    mid = len(a) // 2
    return len(a) + linearithmic(a[:mid]) + linearithmic(a[mid:])

def quadratic(a):                    # O(n^2)
    ops = 0
    for _ in a:
        for _ in a:
            ops += 1
    return ops


print(f"{'n':>7} {'O(1)':>6} {'O(log n)':>9} {'O(n)':>8} "
      f"{'O(n log n)':>11} {'O(n^2)':>10}")
for n in (10, 100, 1000):
    a = list(range(n))
    print(f"{n:>7} {constant(a)[1]:>6} {logarithmic(a, n - 1):>9} "
          f"{linear(a):>8} {linearithmic(a):>11} {quadratic(a):>10}")

print()
print("n grew 100x. O(log n) grew by 7. O(n^2) grew by 10,000.")

# --- constants, which big-O throws away --------------------------------
print()
def insertion(a):                    # O(n^2), tiny constant
    a = a[:]
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge(a):                        # O(n log n), heavier constant
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge(a[:mid]), merge(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

for n in (8, 16, 1000):
    sample = [(i * 7919) % n for i in range(n)]
    # A single small sort finishes faster than the clock can measure, so
    # repeat it enough times to land on something the timer can see.
    repeats = max(1, 100_000 // (n * n))
    times = {}
    for name, fn in (("insertion", insertion), ("merge", merge)):
        start = time.time()
        for _ in range(repeats):
            fn(sample)
        times[name] = (time.time() - start) / repeats
    winner = min(times, key=times.get)
    print(f"n={n:>5} (averaged over {repeats:>4}): "
          f"insertion {times['insertion']*1000:>8.4f} ms, "
          f"merge {times['merge']*1000:>8.4f} ms  -> {winner} wins")
''',
    "walk": [
        ("return a[len(a) // 2], ops",
         "Indexing is O(1) because the address is computed, not searched for. "
         "The size of the list never enters into it &mdash; that is the whole "
         "meaning of constant time."),
        ("mid = (lo + hi) // 2",
         "Halving the range each step means the op count rises by 1 when n "
         "doubles. In the table, n going from 10 to 1000 costs about seven more "
         "operations in total."),
        ("for _ in a: for _ in a:",
         "Nested loops over the same collection: n² operations. At n = 1000 that "
         "is a million, and it is the single most common accidental complexity "
         "in real code."),
        ("return len(a) + linearithmic(...) + ...",
         "Merge sort's recurrence made literal: linear work at each level, and "
         "log n levels. The number this returns is n log n up to a constant."),
        ("insertion beats merge at n = 16",
         "Big-O describes growth as n gets large and deliberately discards the "
         "constant factor. At small n that constant is everything &mdash; which "
         "is why CPython's sort switches to insertion sort for short runs."),
    ],
    "try": [
        "Add an O(2ⁿ) row using naive Fibonacci. Stop at n = 30; the table cannot "
        "reach 100.",
        "Find the crossover: try n = 100, 200, 400 in the timing loop and see "
        "where merge overtakes insertion. Real libraries hard-code a number "
        "found exactly this way.",
        "Feed the timing loop an already sorted list. Insertion sort's best case "
        "is O(n) and it wins at every size &mdash; complexity classes describe "
        "worst cases unless someone says otherwise.",
    ],
},

}


# =========================================================================
# Python's own structures, for the pages that teach them
# =========================================================================

PYTHON_BASICS = {

"dsa/lists_in_python.html": {
    "file": "lists.py",
    "intro": "What a Python list actually is underneath &mdash; a resizable array "
             "of references &mdash; and the four consequences that follow, each "
             "measured: O(1) indexing, O(n) inserts at the front, over-allocated "
             "growth, and the aliasing trap.",
    "code": '''# A Python list is a resizable array of references. Everything follows.
import sys, time

a = [10, 20, 30, 40, 50]
print("list      :", a)
print("a[2]      :", a[2], "- computed address, O(1), whatever the length")
print("a[-1]     :", a[-1], "- negative indices count from the end")
print("a[1:4]    :", a[1:4], "- a slice is a NEW list, O(k) to build")

# --- where the cost is -------------------------------------------------
N = 30_000
for label, action in [
    ("append (end)", lambda lst: lst.append(1)),
    ("insert (front)", lambda lst: lst.insert(0, 1)),
]:
    lst = []
    start = time.time()
    for _ in range(N):
        action(lst)
    print(f"{label:>15}: {N} operations in {time.time() - start:.3f}s")
print("insert(0, x) shifts every existing element one place right.")

# --- growth is over-allocated ------------------------------------------
print()
lst = []
previous = sys.getsizeof(lst)
print("length  bytes")
for i in range(1, 18):
    lst.append(i)
    size = sys.getsizeof(lst)
    if size != previous:
        print(f"{i:>6}  {size:>5}  <- reallocated, with room to spare")
        previous = size

# --- lists hold references, not copies ---------------------------------
print()
grid_wrong = [[0] * 3] * 3          # three references to ONE list
grid_right = [[0] * 3 for _ in range(3)]
grid_wrong[0][0] = 9
grid_right[0][0] = 9
print("[[0]*3]*3          ->", grid_wrong, "  all three rows changed")
print("[[0]*3 for _ in ..] ->", grid_right, "  only the first")

b = a                                # another name for the same list
c = a[:]                             # a copy
a.append(60)
print()
print("b is a:", b is a, "->", b)
print("c is a:", c is a, "->", c)
''',
    "walk": [
        ("a[2]",
         "One multiplication and one memory read. The list stores references "
         "contiguously, so element <em>i</em> is at a computable address &mdash; "
         "this is the difference between a list and a "
         "<a href=\"linked_lists.html\">linked list</a>."),
        ("lst.insert(0, 1)",
         "Everything after the insertion point moves one slot right, so this is "
         "O(n). Doing it in a loop is O(n²), and it is the usual reason a "
         "“queue” written on a list is slow &mdash; see "
         "<a href=\"queues.html\">queues</a>."),
        ("sys.getsizeof(lst)",
         "The size jumps in steps, not per item. CPython over-allocates on growth "
         "so that most appends need no reallocation, which is what “amortised "
         "O(1)” means concretely."),
        ("[[0] * 3] * 3",
         "Multiplying a list repeats the <em>reference</em> three times, so all "
         "three rows are one object. This is the single most common Python bug in "
         "grid and matrix code."),
        ("b = a versus c = a[:]",
         "Assignment binds another name to the same object; slicing builds a new "
         "one. <code>is</code> asks which object, <code>==</code> asks about "
         "contents, and confusing them is how mutation surprises happen."),
    ],
    "try": [
        "Raise <code>N</code> to 60,000. The append timing doubles; the "
        "front-insert timing roughly quadruples.",
        "Replace the front-insert loop with <code>collections.deque</code> and "
        "<code>appendleft</code>. Same result, back to linear.",
        "Print <code>sys.getsizeof</code> for a list of 1,000 items and for 1,000 "
        "separate integers. The list stores references, so it is far smaller than "
        "the things in it.",
    ],
},

"dsa/dictionaries_in_python.html": {
    "file": "dictionaries.py",
    "intro": "A dict is a hash table with the sharp edges filed off. This program "
             "times a lookup against a list scan, shows the four idioms worth "
             "knowing, and then demonstrates the two rules people trip over: keys "
             "must be hashable, and equal keys are the same key.",
    "code": '''# A dict is a hash table: keys hashed to slots, so lookup does not scan.
from collections import Counter, defaultdict
import time

stock = {"apple": 12, "banana": 3, "cherry": 40}
print("dict      :", stock)
print("stock['apple']  :", stock["apple"], "- one hash, one probe")
print("'fig' in stock  :", "fig" in stock)
print("stock.get('fig', 0):", stock.get("fig", 0), "- no KeyError")

# --- why it matters ----------------------------------------------------
N = 200_000
haystack_list = list(range(N))
haystack_set = set(haystack_list)
for label, container in (("list", haystack_list), ("set/dict", haystack_set)):
    start = time.time()
    for probe in (0, N // 2, N - 1, -1):
        probe in container
    print(f"{label:>9}: 4 membership tests in {time.time() - start:.4f}s")
print("The list scans. The hash table computes where the answer would be.")

# --- the idioms worth knowing -----------------------------------------
words = "the quick brown fox jumps over the lazy dog the fox".split()

counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1          # 1. get with a default

groups = defaultdict(list)
for w in words:
    groups[len(w)].append(w)                  # 2. defaultdict, no setup

print()
print("counts   :", Counter(words).most_common(3))   # 3. Counter does it for you
print("by length:", dict(groups))
print("inverted :", {v: k for k, v in stock.items()})  # 4. comprehension

# --- the two rules ----------------------------------------------------
print()
try:
    {[1, 2]: "x"}                             # a list can change; its hash cannot
except TypeError as e:
    print("list as key   ->", e)
print("tuple as key  ->", {(1, 2): "fine"})

print()
d = {1: "int one", 1.0: "float one", True: "bool one"}
print("{1: ..., 1.0: ..., True: ...} ->", d)
print("hash(1) == hash(1.0) == hash(True):", hash(1) == hash(1.0) == hash(True))
print("They are equal AND hash the same, so they are one key with one value.")
''',
    "walk": [
        ("stock[\"apple\"]",
         "Hash the key, go to the slot, compare. No part of that depends on how "
         "many keys there are, which is the whole reason dictionaries are "
         "everywhere &mdash; see "
         "<a href=\"hash_tables.html\">hash tables</a> for the machinery."),
        ("probe in haystack_list",
         "A list has to compare against every element until it finds one, so "
         "<code>in</code> is O(n). Swapping a list for a set is the single "
         "highest-value optimisation in most beginner Python."),
        ("counts.get(w, 0) + 1",
         "The default avoids a <code>KeyError</code> on the first sight of a word "
         "without needing an <code>if</code>. <code>defaultdict</code> and "
         "<code>Counter</code> are the same idea, pre-packaged."),
        ("{[1, 2]: \"x\"}",
         "Keys must be hashable, which in practice means immutable. If a key "
         "could change after insertion, its hash would no longer point at the "
         "slot it lives in and it would become unreachable."),
        ("{1: ..., 1.0: ..., True: ...}",
         "One entry, not three. <code>1 == 1.0 == True</code> and they hash "
         "identically, so each assignment overwrites the previous value while "
         "keeping the first key object."),
    ],
    "try": [
        "Time <code>-1 in haystack_list</code> alone. The miss is the worst case: "
        "the entire list, every time.",
        "Insert keys in a scrambled order and print the dict. Since Python 3.7 "
        "insertion order is preserved &mdash; a guarantee, not an accident.",
        "Use a tuple <code>(row, col)</code> as a key to build a sparse grid. That "
        "is how you store a large mostly-empty matrix without allocating it.",
    ],
},

"dsa/strings_in_python.html": {
    "file": "strings.py",
    "intro": "Strings are immutable, and nearly everything surprising about them "
             "follows from that one fact. The middle block times the loop that "
             "every beginner writes against the idiom that replaces it.",
    "code": '''# Strings are immutable. Every "change" builds a new string.
import time

s = "algorithms"
print("s          :", s)
print("s[0], s[-1]:", s[0], s[-1])
print("s[2:6]     :", s[2:6], "- a new string, not a view")
print("s[::-1]    :", s[::-1], "- the standard reversal idiom")

try:
    s[0] = "A"
except TypeError as e:
    print("s[0] = 'A' ->", e)
print("s.replace('a', 'A') ->", s.replace("a", "A"), "  original still:", s)

# --- the loop everyone writes first ------------------------------------
class Accumulator:
    def __init__(self):
        self.text = ""

print()
print(f"{'n':>7} {'+= in a loop':>14} {'list + join':>13} {'ratio':>7}")
for n in (20_000, 40_000, 80_000):
    acc = Accumulator()
    start = time.time()
    for _ in range(n):
        acc.text += "x"           # a new string each time: O(n) per step
    concat = time.time() - start

    start = time.time()
    parts = []
    for _ in range(n):
        parts.append("x")         # O(1) each...
    text = "".join(parts)         # ...then one allocation: O(n) overall
    joined = time.time() - start

    print(f"{n:>7} {concat:>13.4f}s {joined:>12.4f}s {concat / joined:>6.1f}x")

print("Double n: the join column doubles. The += column quadruples.")

# --- the methods that do the work --------------------------------------
line = "  Name , Age ,  City  "
print()
print("split+strip:", [f.strip() for f in line.strip().split(",")])
print("startswith :", "algorithms".startswith("algo"))
print("find       :", "algorithms".find("rit"), "- index, or -1")
print("join       :", "-".join(["a", "b", "c"]))

# --- characters are strings too ----------------------------------------
print()
word = "level"
print(f"{word!r} is a palindrome:", word == word[::-1])
print("counts:", {ch: word.count(ch) for ch in sorted(set(word))})
print("ord/chr:", ord("a"), chr(98), "- the numbers behind the characters")
''',
    "walk": [
        ("s[0] = \"A\" -> TypeError",
         "Immutability is enforced, not advisory. It is also what lets strings be "
         "hashable, and therefore usable as dictionary keys &mdash; a mutable "
         "string could not be."),
        ("acc.text += \"x\"",
         "Each <code>+=</code> allocates a new string and copies everything so "
         "far, so building n characters costs O(n²). The table measures growth "
         "rather than one timing, because that is the part that does not depend "
         "on the machine."),
        ("why an attribute, not a local variable",
         "CPython has a special case that can resize a string in place when the "
         "target is a plain local and nothing else refers to it, which makes the "
         "textbook example look fine on some builds and not others. Storing into "
         "an attribute takes that variable out of the measurement &mdash; and a "
         "rescue that depends on the interpreter build is not one to write code "
         "against."),
        ("\"\".join(parts)",
         "One pass to compute the total length, one allocation, one copy. It is "
         "the idiomatic answer, it is the fast one, and it does not depend on an "
         "interpreter detail to stay fast."),
        ("s[2:6]",
         "Slicing copies. On a large string in a loop that is a real cost, and it "
         "is why algorithms that scan text carry indices around instead of "
         "slicing as they go."),
        ("word == word[::-1]",
         "Readable, and it allocates a full reversed copy. The "
         "<a href=\"two_pointers.html\">two-pointer</a> version uses O(1) memory "
         "&mdash; worth knowing which one you are writing."),
    ],
    "try": [
        "Swap <code>acc.text</code> for a plain local variable <code>out</code> "
        "and re-run. Whether the quadratic disappears depends on the interpreter "
        "you are running &mdash; which is the argument for <code>join</code> in "
        "one line.",
        "Check whether two words are anagrams with <code>sorted(a) == "
        "sorted(b)</code>, then again with <code>Counter</code>. O(n log n) "
        "against O(n).",
        "Try <code>\"café\"[::-1]</code> and <code>len(\"café\")</code>. Python 3 "
        "strings are sequences of code points, so this behaves &mdash; and an "
        "emoji with a skin-tone modifier still will not.",
    ],
},

}



# =========================================================================

CODE = {}
for _group in (SEARCHING, SORTING, GRAPHS, STRUCTURES, TECHNIQUES, PYTHON_BASICS):
    CODE.update(_group)
