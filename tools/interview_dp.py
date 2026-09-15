# -*- coding: utf-8 -*-
"""The dynamic programming questions.

Four problems chosen because between them they cover the whole method: the
overlapping subproblems that make memoisation work, a case where greedy is
simply wrong, a recurrence with a better-than-quadratic reformulation, and the
rolling-variable trick that removes the table.

Every `viz` here is built by running the thing it draws - see
tools/interview_viz.py for why that matters.
"""

import bisect as _bisect

from interview_viz import cost_table, frame, marked, pairs, row, cell, viz

DP = []


def _q(**kw):
    DP.append(kw)


# =========================================================================
# 1. climbing stairs
# =========================================================================

def _stairs_frames():
    """Recorded by counting real calls in the naive version, then filling the table."""
    calls = {"n": 0}

    def naive(n):
        calls["n"] += 1
        if n <= 2:
            return n
        return naive(n - 1) + naive(n - 2)

    out = []
    for n in (5, 10, 20):
        calls["n"] = 0
        v = naive(n)
        out.append(frame(
            pairs([("n", str(n)), ("ways", str(v)),
                   ("calls made", "{:,}".format(calls["n"]))],
                  {"calls made": "bad"}, label="plain recursion"),
            "ways(%d) = %d, and it took %s calls to work out. The count roughly "
            "doubles with each extra step, because the same subproblems are solved "
            "again and again." % (n, v, "{:,}".format(calls["n"])),
            {"n": n, "calls": calls["n"]}))

    table = [0, 1, 2]
    for i in range(3, 11):
        table.append(table[i - 1] + table[i - 2])
        out.append(frame(
            marked([str(v) for v in table[1:]],
                   {j: ("hit" if j == i - 1 else "done")
                    for j in range(len(table) - 1)},
                   label="ways to reach step 1..%d" % i),
            "Filling it forwards instead: ways(%d) = ways(%d) + ways(%d) = %d. "
            "Each entry is computed once, from the two before it."
            % (i, i - 1, i - 2, table[i]),
            {"n": i, "calls": i - 2}))
    out.append(frame(
        pairs([("table", "n entries"), ("two variables", "O(1) space"),
               ("cost", "O(n) either way"),
               ("it is", "Fibonacci")],
              {"two variables": "hit"}, label="what is actually needed"),
        "Only the last two entries are ever read, so the table can collapse to "
        "two variables. The sequence is Fibonacci - which is the answer to "
        "'do you recognise this?'",
        {"n": 10, "calls": 8}))
    return viz(out)


_q(
    slug="climbing-stairs",
    kind="coding",
    level="Easy",
    title="Climbing stairs: the DP that is Fibonacci",
    asked="You can climb 1 or 2 steps at a time. How many ways to reach step n?",
    desc="Climbing stairs as the smallest complete DP: exponential recursion, "
         "memoisation, a forwards table, and the two-variable version - with "
         "the call counts that justify each step.",
    lead="<code>ways(n) = ways(n-1) + ways(n-2)</code>, because the last move "
         "was either one step or two. That is Fibonacci. Written as plain "
         "recursion it is <strong>exponential</strong>; the same recurrence "
         "computed once per value is O(n), and since only the last two values "
         "are ever needed it is <strong>O(1) space</strong>.",
    say="\"The last move was either a single step from n-1 or a double from "
        "n-2, so ways(n) = ways(n-1) + ways(n-2) with ways(1) = 1 and ways(2) "
        "= 2. It is Fibonacci. Naive recursion is exponential because the "
        "subproblems overlap, so I either memoise or fill a table forwards - "
        "and since only the last two entries are read, two variables are "
        "enough. O(n) time, O(1) space.\"",
    notice=[
        "The call count roughly doubles per extra step &mdash; that is the "
        "overlap, measured.",
        "Filling forwards computes each value exactly once.",
        "Only the last two entries are ever read, which is why the table can "
        "go.",
    ],
    viz=_stairs_frames(),
    sections=[
        ("Where the recurrence comes from",
         "<p>Work backwards from the destination rather than forwards from the "
         "start. To be standing on step <em>n</em>, the previous step was "
         "either <em>n&minus;1</em> (and you took one step) or <em>n&minus;2</em> "
         "(and you took two). Those two sets of routes are disjoint and "
         "together they are all of them, so the counts add.</p>"
         "<p>That is the whole derivation, and it is worth saying in exactly "
         "that form: <em>every route ends with one of two moves, so partition "
         "by the last move</em>. The same sentence derives the recurrence for "
         "coin change, for house robber, and for most one-dimensional DP.</p>"
         "<p>The base cases are where people slip. <code>ways(1) = 1</code> "
         "and <code>ways(2) = 2</code> &mdash; and if you define "
         "<code>ways(0) = 1</code> (one way to stand still) the recurrence "
         "works from <code>n = 2</code> and the sequence lines up with "
         "standard Fibonacci.</p>"),
        ("Why plain recursion is exponential",
         "<p><code>ways(5)</code> calls <code>ways(4)</code> and "
         "<code>ways(3)</code>; <code>ways(4)</code> calls <code>ways(3)</code> "
         "again. The recursion tree has two branches at almost every node and "
         "a depth of n, so the number of calls grows like the golden ratio to "
         "the n &mdash; and the editor below prints it: 109 calls at n = 10, "
         "13,529 at n = 20, over 150,000 at n = 25.</p>"
         "<p>This is <strong>overlapping subproblems</strong>, and it is one of "
         "the two conditions that make a problem a DP problem. The other is "
         "<strong>optimal substructure</strong>: the answer for n is built from "
         "the answers for smaller n, unchanged by how you got there. Naming "
         "both is a good way to show you know why the method applies rather "
         "than pattern-matching to it.</p>"),
        ("Four versions, in the order to present them",
         "<p><strong>Recursion</strong> &mdash; states the recurrence clearly "
         "and is unusable. Write it, say it is exponential, move on.</p>"
         "<p><strong>Memoised recursion</strong> &mdash; "
         "<code>@functools.lru_cache</code> on the same function. One line, "
         "O(n) time, O(n) space, and it keeps the recursive shape that made "
         "the recurrence obvious. This is <em>top-down</em>.</p>"
         "<p><strong>A forwards table</strong> &mdash; <em>bottom-up</em>, no "
         "recursion, no stack depth limit. Same complexity, and it makes the "
         "next step visible.</p>"
         "<p><strong>Two variables</strong> &mdash; because the table is only "
         "ever read two entries back. O(1) space, and the version to end on. "
         "Offering all four in that order, briefly, is worth more than jumping "
         "straight to the last one: the interviewer wants the reasoning, and "
         "the reasoning is the ladder.</p>"),
        ("The follow-ups",
         "<p><strong>\"What if you can climb 1, 2 or 3 steps?\"</strong> The "
         "recurrence gains a term and the rolling window becomes three "
         "variables. The general version &mdash; any set of allowed step sizes "
         "&mdash; is coin change counting combinations, which is the "
         "<a href=\"coin-change.html\">next question</a>.</p>"
         "<p><strong>\"Can it be faster than O(n)?\"</strong> Yes, and this is "
         "the answer that surprises people: Fibonacci has a closed form, and "
         "matrix exponentiation computes it in O(log n) multiplications. Worth "
         "naming; not worth writing unless asked, because the numbers get big "
         "enough that the multiplications stop being O(1).</p>"),
    ],
    code={
        "file": "stairs.py",
        "intro": "The call count for plain recursion at three sizes, then the "
                 "three fixes agreeing on the same answer - with the space "
                 "each one uses.",
        "code": '''import functools, sys

calls = 0

def naive(n):
    """Correct, and exponential: the subproblems overlap."""
    global calls
    calls += 1
    if n <= 2:
        return n
    return naive(n - 1) + naive(n - 2)

print("plain recursion:")
for n in (10, 20, 25):
    calls = 0
    v = naive(n)
    print(f"  ways({n:>2}) = {v:>7,}   calls: {calls:>9,}")
print("  the call count grows exponentially, not linearly")

@functools.lru_cache(maxsize=None)
def memo(n):
    """Top-down: same recurrence, each value computed once."""
    if n <= 2:
        return n
    return memo(n - 1) + memo(n - 2)

def table(n):
    """Bottom-up: no recursion, so no stack limit."""
    if n <= 2:
        return n
    best = [0] * (n + 1)
    best[1], best[2] = 1, 2
    for i in range(3, n + 1):
        best[i] = best[i - 1] + best[i - 2]
    return best[n]

def rolling(n):
    """Only the last two entries are ever read."""
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(n - 2):
        a, b = b, a + b
    return b

n = 30
print()
print(f"ways({n}):")
print(f"  memoised  {memo(n):>8,}   cache holds {memo.cache_info().currsize} entries")
print(f"  table     {table(n):>8,}   list of {n + 1} ints")
print(f"  rolling   {rolling(n):>8,}   2 variables")
print("  all agree:", memo(n) == table(n) == rolling(n))
print("  and they agree with the naive version at n=25:",
      naive(25) == rolling(25))

print()
print("it is Fibonacci:")
print("  ways(1..10) =", [rolling(i) for i in range(1, 11)])

# The reason to prefer bottom-up when n is large.
print()
print("recursion limit:", sys.getrecursionlimit())
try:
    memo.cache_clear()
    memo(4_000)
except RecursionError as e:
    print("  memo(4000) -> RecursionError:", str(e)[:40])
print("  rolling(4000) has", len(str(rolling(4_000))), "digits and no stack cost")
''',
        "walk": [
            ("calls += 1",
             "The counter is the argument. \"Exponential\" is a claim; 150,049 "
             "calls for n = 25 is a measurement, and it is what justifies "
                     "everything that follows."),
            ("@functools.lru_cache(maxsize=None)",
             "Top-down memoisation in one line, keeping the recursive shape. "
             "The cache size printed afterwards is n &mdash; one entry per "
             "distinct subproblem, which is the definition of the fix."),
            ("a, b = b, a + b",
             "The whole table collapsed into two names, because nothing ever "
             "reads further back than two. This is the version to end on."),
            ("memo(4_000) -> RecursionError",
             "Why bottom-up is not just a stylistic preference: the recursive "
             "version has a depth limit and the iterative one does not."),
        ],
        "try": [
            "Raise the naive call to <code>naive(30)</code> and watch the count. "
            "It is about 1.6 times worse per step, which is the golden ratio "
            "showing up in the runtime.",
            "Add a third step size &mdash; <code>a, b, c = b, c, a + b + c</code> "
            "&mdash; and check <code>ways(1..8)</code> against counting by hand "
            "for small n.",
        ],
    },
    check=[
        {"q": "Where does ways(n) = ways(n-1) + ways(n-2) come from?",
         "options": ["Trial and error",
                     "Partitioning routes by the last move, which was either one step or two",
                     "The number of steps",
                     "Counting permutations"],
         "answer": 1,
         "why": "The two sets of routes are disjoint and together are all of "
                "them, so the counts add. The same reasoning derives most 1-D "
                "recurrences."},
        {"q": "Why is plain recursion exponential here?",
         "options": ["Function calls are slow",
                     "The subproblems overlap, so the same values are recomputed many times",
                     "It uses too much memory",
                     "Because of the base case"],
         "answer": 1,
         "why": "ways(3) is computed once for ways(4) and again for ways(5), "
                "and so on down the tree. Overlapping subproblems is the "
                "condition that makes memoisation pay."},
        {"q": "Why can the table be replaced by two variables?",
         "options": ["To save time",
                     "Because the recurrence only ever reads two entries back",
                     "Because n is small",
                     "It cannot; the table is required"],
         "answer": 1,
         "why": "Space in a DP is set by how far back the recurrence reaches, "
                "not by n."},
        {"q": "What does the sequence turn out to be?",
         "options": ["Powers of two", "Fibonacci", "Triangular numbers",
                     "Catalan numbers"],
         "answer": 1,
         "why": "Same recurrence, offset base cases. Recognising it is worth "
                "saying out loud, and it opens the O(log n) follow-up."},
    ],
)


# =========================================================================
# 2. coin change
# =========================================================================

def _coin_frames():
    """Recorded by filling the real DP table, and by running greedy alongside."""
    coins, amount = [1, 3, 4], 6
    INF = float("inf")
    best = [0] + [INF] * amount
    out = []
    for a in range(1, amount + 1):
        picked = None
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
                picked = c
        shown = ["0" if v == 0 else ("-" if v == INF else str(int(v)))
                 for v in best]
        out.append(frame(
            marked(shown, {j: ("hit" if j == a else
                               ("done" if best[j] != INF else "dim"))
                           for j in range(len(shown))},
                   label="fewest coins for 0..%d" % amount),
            "amount %d: the best option is a %d coin on top of the answer for "
            "%d, giving %d. Every entry is built from an earlier one."
            % (a, picked, a - picked, int(best[a])),
            {"amount": a, "coins": int(best[a])}))

    greedy_used, left = [], amount
    for c in sorted(coins, reverse=True):
        while left >= c:
            left -= c
            greedy_used.append(c)
    out.append(frame(
        pairs([("greedy picks", " + ".join(str(c) for c in greedy_used)),
               ("greedy total", "%d coins" % len(greedy_used)),
               ("optimal", "%d coins" % int(best[amount])),
               ("optimal picks", "3 + 3")],
              {"greedy total": "bad", "optimal": "hit"},
              label="why greedy fails here"),
        "Greedy takes the 4 first and is then stuck with two 1s. Taking the "
        "smaller coin twice is better - which is exactly the lookahead greedy "
        "does not have.",
        {"amount": amount, "coins": int(best[amount])}))
    return viz(out)


_q(
    slug="coin-change",
    kind="coding",
    level="Medium",
    title="Coin change, and why greedy is wrong",
    asked="Given coin denominations and an amount, what is the fewest coins "
          "that make it?",
    desc="Coin change as the canonical case where greedy fails: the [1,3,4] "
         "counterexample, the O(amount x coins) table, and why the currency in "
         "your pocket is the special case.",
    lead="Take the biggest coin first and you get the wrong answer: with "
         "<code>[1, 3, 4]</code> for 6, greedy picks 4+1+1 &mdash; three coins "
         "&mdash; where 3+3 is two. The fix is a table: "
         "<code>best[a] = 1 + min(best[a - c])</code> over the coins that fit, "
         "in <strong>O(amount &times; coins)</strong>.",
    say="\"Greedy does not work in general - with coins 1, 3, 4 and amount 6 it "
        "gives three coins where two is optimal. So a table: best[a] is one "
        "plus the minimum over best[a - c] for each coin c that fits, filled "
        "upwards from 0. O(amount times number of coins) time, O(amount) "
        "space. Greedy happens to be optimal for canonical systems like real "
        "currency, which is why the intuition is so strong.\"",
    notice=[
        "Every entry is built from a <em>smaller</em> amount, which is why "
        "filling upwards works.",
        "Greedy commits to the 4 and cannot undo it.",
        "Unreachable amounts stay at infinity and become &minus;1.",
    ],
    viz=_coin_frames(),
    sections=[
        ("The counterexample is the answer",
         "<p>Almost everyone offers greedy first, because it is what people do "
         "with actual money and it works. The single most useful thing to have "
         "ready is the smallest case where it fails: <strong>coins 1, 3, 4 and "
         "amount 6</strong>. Greedy takes 4, then can only use 1s, and ends at "
         "three coins. The optimum is 3 + 3.</p>"
         "<p>Offering that unprompted is worth more than the DP itself, "
         "because it shows you tested the obvious approach instead of "
         "assuming it. And it explains why the intuition is so strong: "
         "greedy <em>is</em> optimal for canonical coin systems, which is what "
         "every real currency is designed to be. The editor checks [1, 5, 10, "
         "25] and greedy matches the DP on every amount.</p>"),
        ("The recurrence, and the direction to fill it",
         "<p>Partition by the last coin. If the final coin used is "
         "<code>c</code>, the rest of the amount cost <code>best[a - c]</code> "
         "&mdash; so <code>best[a] = 1 + min(best[a - c])</code> over every "
         "coin that fits.</p>"
         "<p>Fill upwards from <code>best[0] = 0</code>, because every entry "
         "depends only on smaller ones. That ordering is the whole of "
         "bottom-up DP and it is why no recursion is needed: by the time you "
         "reach <code>a</code>, everything it depends on is already "
         "final.</p>"
         "<p>Use <code>float(\"inf\")</code> for unreachable amounts rather "
         "than a sentinel like &minus;1. Infinity survives the "
         "<code>min</code> and the <code>+ 1</code> correctly; &minus;1 does "
         "not, and mixing the sentinel into the arithmetic is the standard "
         "bug in this problem.</p>"),
        ("Fewest coins versus how many ways",
         "<p>Two different questions share this setup and the difference is a "
         "loop order, which is worth knowing because interviewers switch "
         "between them.</p>"
         "<p><strong>Fewest coins</strong> &mdash; this page. The loops can go "
         "in either order, because <code>min</code> does not care.</p>"
         "<p><strong>How many ways to make the amount</strong> &mdash; "
         "<code>ways[0] = 1</code> and <code>ways[a] += ways[a - c]</code>. "
         "Here the order decides <em>what you are counting</em>: coins on the "
         "outside and amounts inside counts combinations (order does not "
         "matter); amounts outside and coins inside counts permutations. It is "
         "the same two loops swapped, and the results differ &mdash; a "
         "genuinely nasty detail and a favourite follow-up.</p>"),
        ("What it costs, and when it is too much",
         "<p>O(amount &times; coins) time and O(amount) space. Note that "
         "<code>amount</code> is a <em>value</em>, not an input length, so the "
         "table is exponential in the number of bits of the input &mdash; this "
         "is a pseudo-polynomial algorithm, and coin change with unbounded "
         "denominations is NP-hard in general.</p>"
         "<p>In practice that means it is fine for amounts in the thousands "
         "and wrong for amounts in the billions. Saying \"O(amount times "
         "coins), and note amount is the value so this is pseudo-polynomial\" "
         "is a strong close, because it shows you know the difference between "
         "the size of an input and the magnitude of it.</p>"),
    ],
    code={
        "file": "coin_change.py",
        "intro": "Greedy against the table on the case that separates them, "
                 "then the currency where greedy is safe, and the reconstructed "
                 "coin list.",
        "code": '''def greedy(coins, amount):
    """Biggest coin first. Correct for some systems, not in general."""
    used, left = [], amount
    for c in sorted(coins, reverse=True):
        while left >= c:
            left -= c
            used.append(c)
    return used if left == 0 else None


def fewest(coins, amount):
    """best[a] = 1 + min(best[a - c]) over coins that fit."""
    INF = float("inf")
    best = [0] + [INF] * amount
    pick = [None] * (amount + 1)          # for reconstructing the coins
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
                pick[a] = c
    if best[amount] == INF:
        return -1, []
    coins_used, a = [], amount
    while a > 0:
        coins_used.append(pick[a])
        a -= pick[a]
    return int(best[amount]), sorted(coins_used)


coins, amount = [1, 3, 4], 6
g = greedy(coins, amount)
n, used = fewest(coins, amount)
print(f"coins {coins}  amount {amount}")
print(f"  greedy : {g} -> {len(g)} coins")
print(f"  optimal: {used} -> {n} coins")
print("  greedy loses because it commits to the 4 and cannot undo it")

# Greedy IS optimal for canonical systems - which is why the intuition sticks.
print()
print("real currency [1, 5, 10, 25]:")
agree = True
for amt in range(1, 100):
    gg = greedy([1, 5, 10, 25], amt)
    dd, _ = fewest([1, 5, 10, 25], amt)
    if len(gg) != dd:
        agree = False
        print(f"  disagree at {amt}: greedy {len(gg)}, optimal {dd}")
print("  greedy matches the optimum for every amount 1..99:", agree)

# The edges.
print()
print("amount 0 needs no coins:", fewest([1, 2, 5], 0))
print("unreachable amounts give -1:", fewest([5, 10], 3))
print("a single coin that fits exactly:", fewest([7], 7))

# Cost, and the word that matters.
amount = 5_000
n, _ = fewest([1, 3, 4], amount)
print()
print(f"amount {amount:,} with 3 coins -> {n} coins")
print(f"  table entries filled: {amount:,}  (amount x coins operations)")
print("  note 'amount' is a VALUE, not a length: this is pseudo-polynomial")
''',
        "walk": [
            ("for c in coins: if c <= a",
             "Partition by the last coin used. Each candidate asks \"what did "
             "the remaining amount cost?\" &mdash; a question already answered, "
             "because it is smaller."),
            ("best = [0] + [INF] * amount",
             "Infinity rather than &minus;1 for unreachable. It survives the "
             "<code>+ 1</code> and the comparison correctly; a &minus;1 "
             "sentinel does not, and that is the usual bug here."),
            ("pick[a] = c",
             "Recording which coin won turns the answer from a count into the "
             "actual coins. Interviewers ask for this as a follow-up more often "
             "than not."),
            ("for amt in range(1, 100)",
             "Checking greedy against the optimum across a whole range, rather "
             "than on one example. It agrees everywhere for real currency, "
             "which is the honest reason the wrong intuition is so "
             "persistent."),
        ],
        "try": [
            "Find another coin set where greedy fails. <code>[1, 5, 12]</code> "
            "for 15 is one &mdash; greedy gives 12+1+1+1, four coins, against "
            "5+5+5.",
            "Change it to count the <em>number of ways</em> instead, then swap "
            "the two loops. The answers differ, and working out which one "
            "counts combinations is the standard follow-up.",
        ],
    },
    check=[
        {"q": "Why is greedy wrong for coins [1, 3, 4] and amount 6?",
         "options": ["It runs too slowly",
                     "It takes the 4 first and is then forced into two 1s, three coins against the optimal two",
                     "It cannot handle a 1 coin",
                     "It is not wrong"],
         "answer": 1,
         "why": "Committing to the largest coin removes the 3+3 option. "
                "Greedy has no lookahead."},
        {"q": "What is the recurrence?",
         "options": ["best[a] = best[a-1] + 1",
                     "best[a] = 1 + min(best[a - c]) over coins c that fit",
                     "best[a] = sum of best[a - c]",
                     "best[a] = a // max(coins)"],
         "answer": 1,
         "why": "Partition by the last coin used; the rest of the amount is a "
                "smaller subproblem that is already solved."},
        {"q": "Why use infinity for unreachable amounts rather than -1?",
         "options": ["It is faster",
                     "Infinity survives the min and the +1 correctly, where a -1 sentinel corrupts the arithmetic",
                     "-1 is not a valid list value",
                     "There is no difference"],
         "answer": 1,
         "why": "min(-1, anything) picks the sentinel and then +1 makes it 0, "
                "which is silently wrong."},
        {"q": "Why is O(amount x coins) called pseudo-polynomial?",
         "options": ["Because it is approximate",
                     "Because amount is a value, not an input length - the table is exponential in the number of bits",
                     "Because the coins are unsorted",
                     "Because it uses recursion"],
         "answer": 1,
         "why": "Doubling the number of digits in the amount multiplies the "
                "work by ten, not by two. It is fine for thousands and hopeless "
                "for billions."},
    ],
)


# =========================================================================
# 3. longest increasing subsequence
# =========================================================================

def _lis_frames():
    """Recorded by running the patience version and logging the tails array."""
    a = [10, 9, 2, 5, 3, 7, 101, 18]
    tails, out = [], []
    for i, x in enumerate(a):
        j = _bisect.bisect_left(tails, x)
        appended = j == len(tails)
        if appended:
            tails.append(x)
        else:
            replaced = tails[j]
            tails[j] = x
        marks = {k: ("dim" if k > i else "done") for k in range(len(a))}
        marks[i] = "hit"
        out.append(frame(
            [marked([str(v) for v in a], marks, {i: "x"}, label="input"),
             marked([str(v) for v in tails],
                    {j: ("hit" if appended else "lo")}, label="tails")],
            ("%d is larger than every tail, so it extends the longest run: "
             "length is now %d." % (x, len(tails)) if appended else
             "%d replaces %d at position %d. The length does not change - but "
             "a smaller tail at that length is easier to extend later."
             % (x, replaced, j)),
            {"i": i, "length": len(tails)}))
    out.append(frame(
        pairs([("length", str(len(tails))),
               ("tails array", str(tails)),
               ("is it a subsequence here?", "yes, by luck"),
               ("always?", "no - see the editor")],
              {"always?": "bad", "length": "hit"},
              label="what tails means"),
        "tails[k] is the smallest possible tail of an increasing run of length "
        "k+1. Its LENGTH is the answer. Its contents happen to be a valid "
        "subsequence on this input and are not in general - the editor shows "
        "an input where they are not.",
        {"i": len(a) - 1, "length": len(tails)}))
    return viz(out)


_q(
    slug="longest-increasing-subsequence",
    kind="coding",
    level="Medium",
    title="Longest increasing subsequence, twice",
    asked="Find the length of the longest strictly increasing subsequence. Can "
          "you do better than O(n squared)?",
    desc="LIS in O(n squared) and then O(n log n) with patience sorting: what "
         "the tails array actually holds, and why it is not the subsequence.",
    lead="The quadratic version is the honest first answer: "
         "<code>best[i]</code> is the longest run ending at <code>i</code>, "
         "found by looking back at every earlier element. The O(n log n) "
         "version keeps a <strong>tails</strong> array where "
         "<code>tails[k]</code> is the smallest tail of any increasing run of "
         "length <code>k+1</code>, and binary searches it. Its length is the "
         "answer &mdash; its contents are not the subsequence.",
    say="\"The O(n squared) version: best[i] is the length of the longest "
        "increasing run ending at i, computed by scanning everything before i. "
        "For O(n log n) I keep an array where position k holds the smallest "
        "possible tail of a run of length k+1 - it stays sorted, so each "
        "element is placed with a binary search: extend the array if it beats "
        "every tail, otherwise overwrite the first tail that is not smaller. "
        "The length of that array is the answer. If I need the actual "
        "subsequence I keep predecessor pointers, because the tails array is "
        "not it.\"",
    notice=[
        "<code>tails</code> stays sorted, which is what licenses the binary "
        "search.",
        "A replacement never changes the length &mdash; it lowers a tail so it "
        "is easier to extend.",
        "The final <code>tails</code> contents are <em>not</em> a valid "
        "subsequence.",
    ],
    viz=_lis_frames(),
    sections=[
        ("The quadratic version first",
         "<p><code>best[i]</code> = the length of the longest increasing "
         "subsequence <em>ending at index i</em>. To compute it, look at every "
         "<code>j &lt; i</code> with <code>a[j] &lt; a[i]</code> and take the "
         "best of those, plus one. The answer is the maximum over all "
         "<code>best[i]</code>.</p>"
         "<p>It is O(n&sup2;), it is four lines, and it is the right thing to "
         "write first. The \"ending at i\" framing is the part worth saying "
         "aloud: without it people try to define <code>best[i]</code> as "
         "\"the answer for the first i elements\", which does not admit a "
         "recurrence, because you cannot tell whether the run can be "
         "extended.</p>"),
        ("What the tails array actually holds",
         "<p>This is the part that is usually recited without being "
         "understood. <code>tails[k]</code> is the <strong>smallest value that "
         "can end an increasing subsequence of length k+1</strong>, among "
         "everything seen so far.</p>"
         "<p>Two facts follow. It is sorted, because a longer run must end "
         "higher than the best ending of a shorter one &mdash; which is what "
         "makes the binary search legal. And overwriting an entry never breaks "
         "anything: replacing a tail with a smaller value keeps the same "
         "achievable length while making future extensions easier.</p>"
         "<p>So each element does one of two things. If it exceeds every tail, "
         "it extends the longest run and the array grows. Otherwise it replaces "
         "the first tail that is not smaller than it &mdash; "
         "<code>bisect_left</code> &mdash; and the length is unchanged.</p>"),
        ("The trap: tails is not the answer",
         "<p>Run it on <code>[2, 6, 8, 3, 4, 5, 1]</code> and the final tails "
         "array is <code>[1, 3, 4, 5]</code>. The length, 4, is correct. The "
         "contents are not a subsequence of the input at all &mdash; the 1 is "
         "the <em>last</em> element, so it cannot precede the 3. The real "
         "answer is <code>[2, 3, 4, 5]</code>.</p>"
         "<p>What makes this trap dangerous is that tails often "
         "<em>is</em> a valid subsequence by coincidence: on "
         "<code>[10, 9, 2, 5, 3, 7, 101, 18]</code> it comes out as "
         "<code>[2, 3, 7, 18]</code>, which is genuinely increasing and "
         "genuinely a subsequence. Checking one example proves nothing here. "
         "If the actual subsequence is wanted, keep a predecessor index for "
         "each element as it is placed and walk the chain backwards &mdash; "
         "the editor below does that, and checks both against the input rather "
         "than asserting.</p>"),
        ("Strict, non-strict, and the follow-ups",
         "<p><code>bisect_left</code> gives <em>strictly</em> increasing: an "
         "equal value replaces rather than extends. <code>bisect_right</code> "
         "gives non-decreasing, where equal values extend the run. One "
         "function call, two different problems &mdash; and the problem "
         "statement often does not say which it wants.</p>"
         "<p>The name to know is <strong>patience sorting</strong>, after the "
         "card game: each tail is the top card of a pile, and you place each "
         "new card on the leftmost pile whose top is not smaller. The number "
         "of piles is the answer. It is also the basis of the "
         "<code>difflib</code> patience diff, which is a good thing to be able "
         "to mention.</p>"),
    ],
    code={
        "file": "lis.py",
        "intro": "Both versions agreeing, the comparison count and timing that "
                 "separate them, and the predecessor chain that recovers the "
                 "actual subsequence the tails array does not give you.",
        "code": '''import bisect, random, time

def lis_quadratic(a):
    """best[i] = longest increasing run ENDING at i."""
    if not a:
        return 0, 0
    best = [1] * len(a)
    comparisons = 0
    for i in range(len(a)):
        for j in range(i):
            comparisons += 1
            if a[j] < a[i] and best[j] + 1 > best[i]:
                best[i] = best[j] + 1
    return max(best), comparisons


def lis_nlogn(a):
    """tails[k] = smallest possible tail of an increasing run of length k+1."""
    tails = []
    for x in a:
        i = bisect.bisect_left(tails, x)   # bisect_right for non-decreasing
        if i == len(tails):
            tails.append(x)                # extends the longest run
        else:
            tails[i] = x                   # lowers a tail; length unchanged
    return len(tails), tails


def lis_with_sequence(a):
    """The same algorithm, keeping predecessors so the run can be rebuilt."""
    tails, tail_idx, prev = [], [], [-1] * len(a)
    for i, x in enumerate(a):
        k = bisect.bisect_left(tails, x)
        if k == len(tails):
            tails.append(x); tail_idx.append(i)
        else:
            tails[k] = x; tail_idx[k] = i
        prev[i] = tail_idx[k - 1] if k > 0 else -1
    out, cur = [], tail_idx[-1]
    while cur != -1:
        out.append(a[cur]); cur = prev[cur]
    return list(reversed(out))


demo = [10, 9, 2, 5, 3, 7, 101, 18]
q, comps = lis_quadratic(demo)
n, tails = lis_nlogn(demo)
print("input:", demo)
print(f"  quadratic: {q}   ({comps} comparisons)")
print(f"  n log n  : {n}   tails = {tails}")
print("  agree on the length:", q == n)

def is_subsequence(sub, a):
    it = iter(a)
    return all(any(x == y for y in it) for x in sub)

print()
print("tails is not, in general, the subsequence. Checked rather than claimed:")
for case in ([10, 9, 2, 5, 3, 7, 101, 18], [2, 6, 8, 3, 4, 5, 1]):
    _, t = lis_nlogn(case)
    seq = lis_with_sequence(case)
    print(f"  input {case}")
    print(f"    tails {t}  -> a valid subsequence of the input? {is_subsequence(t, case)}")
    print(f"    rebuilt {seq}  -> valid? {is_subsequence(seq, case)}")
print("  on the second input the 1 is the LAST element, so it cannot precede")
print("  the 3 - the length is right and the contents are not the answer.")

random.seed(5)
big = [random.randint(0, 10**6) for _ in range(1_200)]
t0 = time.perf_counter(); a1, c1 = lis_quadratic(big); x = time.perf_counter() - t0
t0 = time.perf_counter(); a2, _  = lis_nlogn(big);      y = time.perf_counter() - t0
print()
print(f"n = {len(big)}")
print(f"  quadratic {x*1000:7.1f} ms   ({c1:,} comparisons)  -> {a1}")
print(f"  n log n   {y*1000:7.1f} ms                         -> {a2}")
print(f"  agree: {a1 == a2}   speed-up {x/y:.0f}x")

# Strict against non-decreasing: one function call.
flat = [1, 3, 3, 3, 5]
def lis_non_decreasing(a):
    tails = []
    for x in a:
        i = bisect.bisect_right(tails, x)
        if i == len(tails): tails.append(x)
        else:               tails[i] = x
    return len(tails)

print()
print("input", flat)
print("  strictly increasing (bisect_left) :", lis_nlogn(flat)[0])
print("  non-decreasing      (bisect_right):", lis_non_decreasing(flat))
''',
        "walk": [
            ("best = [1] * len(a)",
             "Every element is an increasing run of length 1 on its own, which "
             "is the base case. The quadratic version is worth writing first "
             "because it makes the recurrence obvious."),
            ("i = bisect.bisect_left(tails, x)",
             "The binary search is legal only because <code>tails</code> is "
             "sorted &mdash; and it is sorted because a longer run must end "
             "higher than the best ending of a shorter one."),
            ("tails[i] = x",
             "A replacement, not an extension. The length is unchanged; what "
             "improves is how easy that length is to extend next time."),
            ("prev[i] = tail_idx[k - 1] if k > 0 else -1",
             "The predecessor chain, which is what actually recovers the "
             "subsequence. Without it you have the length and nothing else."),
        ],
        "try": [
            "Print <code>tails</code> after every element of "
            "<code>[2, 6, 8, 3, 4, 5, 1]</code> and watch the final 1 overwrite "
            "the 2. That single step is where the array stops being a "
            "subsequence of the input.",
            "Swap <code>bisect_left</code> for <code>bisect_right</code> and "
            "re-run on <code>[1, 3, 3, 3, 5]</code>. One call, and the answer "
            "changes from 3 to 5.",
        ],
    },
    check=[
        {"q": "In the quadratic version, what does best[i] mean?",
         "options": ["The answer for the first i elements",
                     "The length of the longest increasing run ending at index i",
                     "The value at position i",
                     "The number of comparisons so far"],
         "answer": 1,
         "why": "\"Ending at i\" is what admits a recurrence - you need to know "
                "what the run ends with to know whether it can be extended."},
        {"q": "What does tails[k] hold?",
         "options": ["The kth element of the answer",
                     "The smallest possible tail of an increasing run of length k+1",
                     "The kth largest value",
                     "A count"],
         "answer": 1,
         "why": "Which is why it stays sorted, and why replacing an entry with "
                "a smaller value never loses anything."},
        {"q": "Is the final tails array the longest increasing subsequence?",
         "options": ["Yes, always",
                     "No - only its length is the answer; the contents need not be a subsequence in order",
                     "Only if the input is sorted",
                     "Only for strictly increasing runs"],
         "answer": 1,
         "why": "On [10,9,2,5,3,7,101,18] tails ends as [2,3,7,18], but 18 "
                "comes after 101 in the input. Recovering the real run needs "
                "predecessor pointers."},
        {"q": "How do you switch from strictly increasing to non-decreasing?",
         "options": ["Sort the input first",
                     "Use bisect_right instead of bisect_left",
                     "Reverse the array",
                     "Change the base case"],
         "answer": 1,
         "why": "bisect_left makes an equal value replace; bisect_right makes "
                "it extend. One call, two problems."},
    ],
)


# =========================================================================
# 4. house robber
# =========================================================================

def _robber_frames():
    """Recorded by filling the table and by rolling two variables alongside."""
    houses = [2, 7, 9, 3, 1]
    best = [0] * (len(houses) + 1)
    best[1] = houses[0]
    out = [frame(
        [marked([str(h) for h in houses], {0: "hit"}, label="houses"),
         marked([str(v) for v in best[1:2]], {0: "done"}, label="best so far")],
        "With one house there is no choice: take it. best(1) = %d."
        % houses[0],
        {"i": 1, "best": best[1]})]
    for i in range(2, len(houses) + 1):
        skip, take = best[i - 1], best[i - 2] + houses[i - 1]
        best[i] = max(skip, take)
        took = take >= skip
        marks = {j: ("dim" if j >= i else "done") for j in range(len(houses))}
        marks[i - 1] = "hit" if took else "bad"
        out.append(frame(
            [marked([str(h) for h in houses], marks, {i - 1: "here"},
                    label="houses"),
             marked([str(v) for v in best[1:i + 1]],
                    {i - 1: "hit"}, label="best for the first k houses")],
            "House %d holds %d. Skip it and keep %d, or take it and add to "
            "best(%d) = %d, giving %d. %s"
            % (i, houses[i - 1], skip, i - 2, best[i - 2], take,
               "Taking wins." if took else "Skipping wins."),
            {"i": i, "best": best[i]}))
    out.append(frame(
        pairs([("answer", str(best[-1])),
               ("table", "%d entries" % (len(houses) + 1)),
               ("actually needed", "2 variables"),
               ("why", "the recurrence looks back 2")],
              {"actually needed": "hit"}, label="space"),
        "Nothing ever reads further back than best(i-2), so the whole table "
        "collapses into two rolling variables - O(1) space for the same "
        "answer.",
        {"i": len(houses), "best": best[-1]}))
    return viz(out)


_q(
    slug="house-robber",
    kind="coding",
    level="Medium",
    title="House robber: the 0-1 choice",
    asked="Each house holds some money and you cannot rob two adjacent ones. "
          "What is the most you can take?",
    desc="The take-or-skip recurrence, why it needs only two rolling "
         "variables, and the circular variant that runs it twice.",
    lead="At each house there are exactly two options: <strong>skip it</strong> "
         "and keep the best from the previous house, or <strong>take it</strong> "
         "and add it to the best from two houses back. "
         "<code>best(i) = max(best(i-1), best(i-2) + house[i])</code> &mdash; "
         "and since nothing reaches further back than two, two variables "
         "replace the whole table.",
    say="\"At each house I either skip it, keeping best(i-1), or take it and "
        "add house[i] to best(i-2), because the neighbour is then off limits. "
        "So best(i) is the max of those two. That is O(n) time, and because "
        "the recurrence only looks two back I keep two variables instead of an "
        "array, so O(1) space. If the houses are in a circle, the first and "
        "last are adjacent, so I run it twice - once excluding the first house, "
        "once excluding the last - and take the better.\"",
    notice=[
        "Two options per house, and the recurrence is just the better of them.",
        "Taking a house means the answer comes from <em>two</em> back, not one.",
        "Nothing reads further back than two, which is why the table can go.",
    ],
    viz=_robber_frames(),
    sections=[
        ("Partition by the last decision",
         "<p>The same move as every other question in this group: look at the "
         "final choice. Either the last house was robbed or it was not.</p>"
         "<p>If it was not, the answer is whatever was best for the houses "
         "before it &mdash; <code>best(i-1)</code>. If it was, its neighbour "
         "cannot have been, so the answer is its value plus the best for "
         "everything up to two houses back &mdash; "
         "<code>best(i-2) + house[i]</code>. Those two cases are exhaustive "
         "and disjoint, so the answer is the larger.</p>"
         "<p>The base cases are worth stating explicitly, because off-by-ones "
         "here are common: <code>best(0) = 0</code> (no houses) and "
         "<code>best(1) = house[0]</code>. Indexing the table from 1 while "
         "the list is indexed from 0 is where the confusion comes from, and "
         "the rolling version below makes it disappear.</p>"),
        ("Why greedy fails, and what to check",
         "<p>\"Take every other house\" is the intuition, and it is wrong: "
         "<code>[2, 1, 1, 2]</code> gives 3 taking the odd positions, where "
         "taking the two 2s gives 4. \"Always take the biggest remaining\" is "
         "also wrong, for the same reason it fails in "
         "<a href=\"coin-change.html\">coin change</a> &mdash; no lookahead.</p>"
         "<p>The editor checks the DP against brute force over every valid "
         "subset on several inputs, including the empty list and a single "
         "house. That is worth doing rather than asserting, because the "
         "recurrence is short enough to look obviously right while being "
         "wrong at the edges.</p>"),
        ("The rolling version, and why it is the one to write",
         "<pre><code>skip = take = 0\n"
         "for h in houses:\n"
         "    skip, take = max(skip, take), skip + h\n"
         "return max(skip, take)</code></pre>"
         "<p>Two names, one pass, no indices. <code>skip</code> is the best "
         "with the current house not taken, <code>take</code> the best with it "
         "taken &mdash; and the simultaneous assignment is what makes it "
         "correct: <code>take</code> uses the <em>old</em> "
         "<code>skip</code>, which is exactly the two-houses-back value.</p>"
         "<p>Writing it in two steps instead, without the tuple assignment, is "
         "the bug: updating <code>skip</code> first means <code>take</code> "
         "adds the current house to a value that already includes its "
         "neighbour. It is the same hazard as swapping without a "
         "temporary.</p>"),
        ("The circular variant",
         "<p>\"Now the houses are in a circle.\" The first and last are "
         "adjacent, so they cannot both be robbed &mdash; and the neat "
         "resolution is to run the linear solution twice: once on "
         "<code>houses[1:]</code> and once on <code>houses[:-1]</code>, then "
         "take the better. Every valid selection excludes at least one of the "
         "two ends, so one of the runs contains the optimum.</p>"
         "<p>The single-house case needs a guard, because both slices are "
         "empty and the answer should be that house. That edge is the whole "
         "difficulty of the variant, and volunteering it is what an "
         "interviewer is listening for.</p>"),
    ],
    code={
        "file": "robber.py",
        "intro": "The table, the two-variable version and brute force over "
                 "every valid subset, checked against each other - then the "
                 "circular variant and the edge it needs.",
        "code": '''def brute(houses):
    """Every subset with no two adjacent. Exponential, and the ground truth."""
    best = 0
    for mask in range(1 << len(houses)):
        if mask & (mask >> 1):            # two adjacent bits set: invalid
            continue
        best = max(best, sum(h for i, h in enumerate(houses) if mask >> i & 1))
    return best


def table(houses):
    """best(i) = max(best(i-1), best(i-2) + house[i])."""
    if not houses:
        return 0
    best = [0] * (len(houses) + 1)
    best[1] = houses[0]
    for i in range(2, len(houses) + 1):
        best[i] = max(best[i - 1], best[i - 2] + houses[i - 1])
    return best[-1]


def rolling(houses):
    """Two variables, because the recurrence only looks two back."""
    skip = take = 0
    for h in houses:
        skip, take = max(skip, take), skip + h
    return max(skip, take)


cases = [[2, 7, 9, 3, 1], [2, 1, 1, 2], [5], [], [1, 2, 3, 1], [4, 1, 2, 7, 5, 3, 1]]
print(f"{'houses':<24} {'brute':>6} {'table':>6} {'rolling':>8}  agree")
for houses in cases:
    b, t, r = brute(houses), table(houses), rolling(houses)
    print(f"{str(houses):<24} {b:>6} {t:>6} {r:>8}  {b == t == r}")

# Greedy fails, and this is the case that shows it.
def every_other(houses):
    return max(sum(houses[0::2]), sum(houses[1::2]))

print()
print("take every other house:")
for houses in ([2, 1, 1, 2], [2, 7, 9, 3, 1]):
    print(f"  {houses}  every-other {every_other(houses)}  optimal {rolling(houses)}",
          "<- greedy loses" if every_other(houses) != rolling(houses) else "")

# The tuple assignment is load-bearing.
def rolling_broken(houses):
    skip = take = 0
    for h in houses:
        skip = max(skip, take)            # updated FIRST: now wrong
        take = skip + h                   # adds h to a value including its neighbour
    return max(skip, take)

print()
print("updating skip before take, instead of simultaneously:")
for houses in ([2, 7, 9, 3, 1], [2, 1, 1, 2]):
    print(f"  {houses}  correct {rolling(houses)}  broken {rolling_broken(houses)}")

# The circular variant: run it twice, and mind the single house.
def circular(houses):
    if len(houses) == 1:
        return houses[0]                  # both slices would be empty
    return max(rolling(houses[1:]), rolling(houses[:-1]))

print()
print("houses in a circle (first and last are adjacent):")
for houses in ([2, 3, 2], [1, 2, 3, 1], [5], [2, 7, 9, 3, 1]):
    print(f"  {str(houses):<16} linear {rolling(houses):>3}   circular {circular(houses):>3}")
''',
        "walk": [
            ("if mask & (mask >> 1)",
             "Two adjacent bits set means two adjacent houses chosen. It is "
             "the whole validity test, and it makes brute force short enough "
             "to be trustworthy as ground truth."),
            ("best[i] = max(best[i - 1], best[i - 2] + houses[i - 1])",
             "Skip or take, and nothing else is possible. The "
             "<code>i - 1</code> in the list index against <code>i</code> in "
             "the table is the off-by-one the rolling version removes."),
            ("skip, take = max(skip, take), skip + h",
             "Simultaneous, so <code>take</code> reads the <em>old</em> "
             "<code>skip</code> &mdash; the two-houses-back value. This is the "
             "line to get right."),
            ("max(rolling(houses[1:]), rolling(houses[:-1]))",
             "Every valid circular selection must exclude at least one end, so "
             "running the linear version on each slice covers all of them."),
        ],
        "try": [
            "Add a negative house value and decide what should happen. The "
            "recurrence still works because skipping is always allowed, which "
            "is worth checking rather than assuming.",
            "Change the rule to \"no two houses within k of each other\". The "
            "recurrence becomes <code>best(i-k-1) + house[i]</code>, and the "
            "rolling window grows from two variables to k+1.",
        ],
    },
    check=[
        {"q": "What is the recurrence?",
         "options": ["best(i) = best(i-1) + house[i]",
                     "best(i) = max(best(i-1), best(i-2) + house[i])",
                     "best(i) = max(house[i], best(i-1))",
                     "best(i) = sum of every other house"],
         "answer": 1,
         "why": "Skip the house and keep the previous best, or take it and add "
                "to the best from two back. Those two cases are exhaustive."},
        {"q": "Why does taking a house use best(i-2) rather than best(i-1)?",
         "options": ["To save space",
                     "Because the adjacent house is then off limits",
                     "Because the array is 0-indexed",
                     "It is arbitrary"],
         "answer": 1,
         "why": "That is the constraint: robbing a house rules out its "
                "neighbour, so the rest of the answer comes from two back."},
        {"q": "Why can the table be replaced by two variables?",
         "options": ["Because n is small",
                     "Because the recurrence never reads further back than two entries",
                     "Because the values are positive",
                     "It cannot"],
         "answer": 1,
         "why": "DP space is set by how far back the recurrence reaches. Here "
                "that is two, so two names suffice."},
        {"q": "For houses in a circle, the standard solution is:",
         "options": ["A different recurrence",
                     "Run the linear version twice - excluding the first house, then the last - and take the better",
                     "Sort the houses first",
                     "Double the array"],
         "answer": 1,
         "why": "Every valid selection excludes at least one end, so one of "
                "the two runs contains the optimum. A single house needs its "
                "own guard."},
    ],
)
