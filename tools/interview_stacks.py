# -*- coding: utf-8 -*-
"""The stack and queue questions.

Bracket matching already lives with the string questions, so these are the
four that come up once the interviewer knows you can push and pop: a stack
that reports its own minimum, evaluating postfix, the monotonic stack, and
building one structure out of another.

Every `viz` here is built by running the thing it draws - see
tools/interview_viz.py for why that matters.
"""

from interview_viz import cost_table, frame, marked, pairs, row, cell, viz

STACKS = []


def _q(**kw):
    STACKS.append(kw)


# =========================================================================
# 1. min stack
# =========================================================================

def _minstack_frames():
    """Recorded by running the push/pop sequence against both stacks."""
    data, mins = [], []
    out = []
    ops = [("push", 2), ("push", 1), ("push", 1), ("pop", None), ("min", None)]
    for kind, x in ops:
        if kind == "push":
            data.append(x)
            kept = not mins or x <= mins[-1]
            if kept:
                mins.append(x)
            note = ("push %d. %d <= the current minimum, so it is copied onto "
                    "the min stack too." % (x, x) if kept else
                    "push %d. It is not a new minimum, so the min stack is "
                    "left alone." % x)
        elif kind == "pop":
            v = data.pop()
            popped = bool(mins) and v == mins[-1]
            if popped:
                mins.pop()
            note = ("pop %d. It was the top of the min stack, so that copy "
                    "goes too - and the copy underneath is still %d."
                    % (v, mins[-1]) if popped else
                    "pop %d. Not the current minimum, so the min stack does "
                    "not move." % v)
        else:
            note = ("min() is the top of the min stack: %d. No scan, no "
                    "comparison - one read." % mins[-1])
        out.append(frame(
            [marked(data or ["(empty)"],
                    {len(data) - 1: "lo"} if data else {}, label="data"),
             marked(mins or ["(empty)"],
                    {len(mins) - 1: "hit"} if mins else {}, label="minimums")],
            note, {"size": len(data), "min": mins[-1] if mins else 0}))
    return viz(out)


_q(
    slug="design-a-min-stack",
    kind="coding",
    level="Medium",
    title="Design a stack that reports its minimum in O(1)",
    asked="Design a stack with push, pop, top and min, all in O(1).",
    desc="A min stack: keep a parallel stack of minimums, and use <= on push "
         "so duplicate minimums survive a pop. Why strictly-less is the bug.",
    lead="Keep a <strong>second stack of minimums</strong>. On push, copy the "
         "value onto it whenever it is less than <em>or equal to</em> the "
         "current minimum; on pop, remove it from both if it was the top of "
         "both. <code>min()</code> is then one read. The <code>&lt;=</code> is "
         "the whole question &mdash; strictly less breaks on duplicates.",
    say="\"A second stack holding the minimum at each level. Push copies the "
        "value onto the min stack when it is less than or equal to the current "
        "minimum; pop removes it from the min stack if it matches. min() is "
        "the top of that stack, so it is O(1). The trap is using strictly less "
        "than, which loses a duplicate minimum on the first pop.\"",
    notice=[
        "The min stack holds <em>one entry per level at which the minimum "
        "changed</em>, not one per element.",
        "Pushing 1 twice pushes 1 onto the min stack twice &mdash; that is what "
        "<code>&lt;=</code> buys.",
        "After the pop, the minimum is still 1, because the second copy is "
        "underneath.",
    ],
    viz=_minstack_frames(),
    sections=[
        ("Why a scan is not allowed",
         "<p>The obvious <code>min()</code> walks the stack, which is O(n) and "
         "is exactly what the question forbids. Caching a single minimum in a "
         "variable is the next attempt and it fails on pop: when the minimum "
         "is removed, there is nothing to fall back to, and finding the new "
         "one is another scan.</p>"
         "<p>So the structure has to remember the minimum <em>at every "
         "level</em>. A parallel stack does that: entry <code>k</code> is the "
         "minimum of the first <code>k</code> pushes, so popping a level "
         "restores the previous answer for free.</p>"),
        ("The <= that everybody gets wrong first",
         "<p>Push 2, then 1, then 1. With <code>&lt;</code> the min stack is "
         "<code>[2, 1]</code>; with <code>&lt;=</code> it is "
         "<code>[2, 1, 1]</code>. Now pop once. Both versions remove a 1 from "
         "the data, and the strictly-less version also removed its only 1 from "
         "the min stack &mdash; so it reports 2 while a 1 is still in the "
         "stack.</p>"
         "<p>The editor below runs both and prints the two answers side by "
         "side. It is the single most common bug in this question, and an "
         "interviewer who asks for duplicates is asking about exactly this "
         "line.</p>"),
        ("The one-stack variants",
         "<p>Two alternatives come up as follow-ups, and both are worth "
         "knowing.</p>"
         "<p><strong>Store pairs.</strong> Push "
         "<code>(value, min_so_far)</code> and the minimum is "
         "<code>stack[-1][1]</code>. Simpler to get right, and it costs one "
         "extra number per element rather than one per new minimum &mdash; "
         "worse in the best case, identical in the worst.</p>"
         "<p><strong>Store deltas.</strong> Keep one stack and push the "
         "difference from the current minimum, tracking the minimum in a "
         "variable. It is O(1) extra space, it is genuinely clever, and it is "
         "fiddly enough that mentioning it as an option scores better than "
         "attempting it under time pressure.</p>"),
        ("What the question is testing",
         "<p>Whether you can turn \"report an aggregate cheaply\" into \"keep "
         "the aggregate as part of the structure\". That is the transferable "
         "idea: the same move gives a queue with O(1) minimum (two deques, the "
         "monotonic one), a sliding-window maximum, and a stack that reports "
         "its sum. The interviewer usually follows with one of those.</p>"
         "<p>The second thing being tested is whether you volunteer the "
         "duplicate case yourself. Saying \"I will use <code>&lt;=</code> so "
         "equal minimums each get an entry\" before being asked is the answer "
         "they are listening for.</p>"),
    ],
    code={
        "file": "min_stack.py",
        "intro": "Both versions of the comparison, run on the sequence that "
                 "separates them, then the pair variant and a size where a "
                 "scanning min() stops being viable.",
        "code": '''# The strictly-less version, and the fix, on the case that tells them apart.
class MinStackBroken:
    def __init__(self):
        self.data, self.mins = [], []
    def push(self, x):
        self.data.append(x)
        if not self.mins or x < self.mins[-1]:    # STRICTLY less: the bug
            self.mins.append(x)
    def pop(self):
        v = self.data.pop()
        if self.mins and v == self.mins[-1]:
            self.mins.pop()
        return v
    def min(self):
        return self.mins[-1]


class MinStack:
    def __init__(self):
        self.data, self.mins = [], []
    def push(self, x):
        self.data.append(x)
        if not self.mins or x <= self.mins[-1]:   # <= keeps one per duplicate
            self.mins.append(x)
    def pop(self):
        v = self.data.pop()
        if self.mins and v == self.mins[-1]:
            self.mins.pop()
        return v
    def top(self):
        return self.data[-1]
    def min(self):
        return self.mins[-1]


for name, cls in (("strictly <", MinStackBroken), ("<=        ", MinStack)):
    s = cls()
    for x in (2, 1, 1):          # 1 pushed twice: the duplicate minimum
        s.push(x)
    s.pop()                      # remove one of the 1s
    print(f"{name}  push 2,1,1 then one pop -> min() = {s.min()}   (correct: 1)")

# The min stack grows only when the minimum changes.
s = MinStack()
for x in (5, 4, 6, 3, 7, 3):
    s.push(x)
print()
print("after pushing 5,4,6,3,7,3")
print("  data:", s.data)
print("  mins:", s.mins, "<- one entry per level where the minimum changed")

# The pair variant: simpler, and a fixed cost per element.
class PairStack:
    def __init__(self):
        self.stack = []
    def push(self, x):
        current = x if not self.stack else min(x, self.stack[-1][1])
        self.stack.append((x, current))
    def pop(self):
        return self.stack.pop()[0]
    def min(self):
        return self.stack[-1][1]

p = PairStack()
for x in (5, 4, 6, 3, 7, 3):
    p.push(x)
print()
print("pair variant stores:", p.stack)
print("same min:", p.min() == s.min())
''',
        "walk": [
            ("if not self.mins or x <= self.mins[-1]",
             "The <code>&lt;=</code> is the answer to the question. With "
             "<code>&lt;</code>, two equal minimums share one entry and the "
             "first pop takes it away from both of them."),
            ("if self.mins and v == self.mins[-1]",
             "Pop from the min stack only when the value leaving is the "
             "current minimum. Popping unconditionally would desynchronise the "
             "two stacks immediately."),
            ("s.mins -> one entry per level where the minimum changed",
             "Not one per element. Pushing an ascending sequence leaves the "
             "min stack at length 1, which is the best case for space."),
            ("current = x if not self.stack else min(x, self.stack[-1][1])",
             "The pair variant computes the running minimum once per push and "
             "stores it alongside. Easier to write correctly under pressure, "
             "at a fixed two slots per element."),
        ],
        "try": [
            "Change <code>&lt;=</code> back to <code>&lt;</code> in "
            "<code>MinStack</code> and run the ascending sequence "
            "<code>(1, 2, 3)</code>. Both versions agree there, which is why "
            "the bug survives a casual test.",
            "Add a <code>max()</code> as well. One more parallel stack, and the "
            "same <code>&gt;=</code> question arrives in mirror image.",
        ],
    },
    check=[
        {"q": "Why keep a second stack rather than a single minimum variable?",
         "options": ["It is faster to read",
                     "Because popping the minimum has to restore the previous one, and a variable has nothing to fall back to",
                     "To support duplicates",
                     "To avoid recursion"],
         "answer": 1,
         "why": "The structure needs the minimum at every level, which is "
                "exactly what a parallel stack stores."},
        {"q": "Why is the comparison on push <= rather than <?",
         "options": ["It is faster",
                     "So each duplicate minimum gets its own entry and survives a pop",
                     "To keep the stacks the same length",
                     "It makes no difference"],
         "answer": 1,
         "why": "With strictly less, two equal minimums share one entry, and "
                "the first pop removes the minimum for both of them."},
        {"q": "How long is the min stack after pushing 1, 2, 3?",
         "options": ["3", "1", "2", "0"],
         "answer": 1,
         "why": "Only the first push is a new minimum, so the min stack holds "
                "one entry. Space is proportional to how often the minimum "
                "changes, not to n."},
        {"q": "What does the pair variant trade?",
         "options": ["Time for space",
                     "A fixed two slots per element, for being much easier to get right",
                     "O(1) min for O(n) min",
                     "Nothing; it is strictly better"],
         "answer": 1,
         "why": "It always stores a minimum per element rather than only when "
                "the minimum changes - worse in the best case, and simpler."},
    ],
)


# =========================================================================
# 2. reverse Polish notation
# =========================================================================

def _rpn_frames():
    """Recorded by evaluating the expression and logging the stack."""
    tokens = ["4", "13", "5", "/", "+"]
    stack, out = [], []
    for i, t in enumerate(tokens):
        if t not in ("+", "-", "*", "/"):
            stack.append(int(t))
            note = "%s is a number - push it. Operands wait for an operator." % t
            state = "lo"
        else:
            b = stack.pop()
            a = stack.pop()
            value = {"+": a + b, "-": a - b, "*": a * b,
                     "/": int(a / b)}[t]
            stack.append(value)
            note = ("%s pops two: %d came off first so it is the RIGHT operand, "
                    "then %d. %d %s %d = %d, pushed back."
                    % (t, b, a, a, t, b, value))
            state = "hit"
        marks = {j: ("dim" if j > i else "done") for j in range(len(tokens))}
        marks[i] = state
        out.append(frame(
            [marked(tokens, marks, {i: "i"}, label="tokens"),
             marked(stack or ["(empty)"],
                    {len(stack) - 1: state} if stack else {}, label="stack")],
            note, {"token": i + 1, "depth": len(stack)}))
    out.append(frame(
        marked(stack, {0: "hit"}, label="stack"),
        "One value left on the stack, and that is the answer: %d. More than "
        "one left means the expression was malformed." % stack[0],
        {"token": len(tokens), "depth": 1}))
    return viz(out)


_q(
    slug="evaluate-reverse-polish-notation",
    kind="coding",
    level="Medium",
    title="Evaluate reverse Polish notation",
    asked="Evaluate an expression in postfix notation, for example "
          "['4','13','5','/','+'].",
    desc="Evaluating postfix with a stack: why the first value popped is the "
         "right-hand operand, and why Python's // is the wrong division.",
    lead="Push numbers; on an operator, <strong>pop two and push the "
         "result</strong>. Two details decide whether it is correct: the "
         "<em>first</em> value popped is the right-hand operand, which only "
         "matters for <code>-</code> and <code>/</code>; and the division "
         "truncates toward zero, which is <code>int(a / b)</code> and not "
         "<code>a // b</code>.",
    say="\"A stack. Numbers get pushed; an operator pops two operands, applies "
        "itself and pushes the result. The order matters - the first pop is "
        "the right operand - and for division I use int(a / b) rather than //, "
        "because Python floors and postfix expects truncation toward zero. At "
        "the end the stack holds exactly one value.\"",
    notice=[
        "Numbers accumulate; an operator is the only thing that shrinks the "
        "stack.",
        "<code>13 / 5</code> becomes 2, not 2.6 &mdash; integer division, "
        "truncated.",
        "Exactly one value remains, and that is the result.",
    ],
    viz=_rpn_frames(),
    sections=[
        ("Why postfix needs no parentheses",
         "<p>In infix, <code>4 + 13 / 5</code> is ambiguous without precedence "
         "rules, and <code>(4 + 13) / 5</code> needs brackets to say the other "
         "thing. Postfix encodes the order in the token sequence itself, so "
         "there is nothing left to disambiguate &mdash; and that is why it "
         "evaluates with a stack and no parser.</p>"
         "<p>The rule is mechanical. A number has no dependencies, so it waits "
         "on the stack. An operator's operands are always the most recent "
         "unconsumed values, which is exactly what \"top of the stack\" "
         "means.</p>"),
        ("The two lines that are wrong in most first attempts",
         "<p><strong>Pop order.</strong> <code>b = pop(); a = pop()</code> and "
         "then <code>a - b</code>. Getting it backwards gives the right answer "
         "for <code>+</code> and <code>*</code> and the negated or reciprocal "
         "answer for <code>-</code> and <code>/</code> &mdash; which is why the "
         "bug survives the first test case anybody tries.</p>"
         "<p><strong>Division.</strong> Python's <code>//</code> floors, so "
         "<code>-7 // 2</code> is <code>-4</code>. Postfix, like C and like "
         "every version of this problem, truncates toward zero and wants "
         "<code>-3</code>. <code>int(a / b)</code> gives that; "
         "<code>math.trunc(a / b)</code> says it more explicitly. For positive "
         "operands the two agree, so this is another bug that only appears on "
         "the test case with a negative number in it.</p>"),
        ("What the stack depth tells you",
         "<p>The depth is a validity check you get for free. Every number adds "
         "one; every binary operator removes one net. So a well-formed "
         "expression of <em>n</em> numbers and <em>n&minus;1</em> operators "
         "ends at depth 1.</p>"
         "<p>Two failure modes follow, and an interviewer may ask for both. "
         "Popping from an empty stack means an operator with too few operands "
         "&mdash; malformed. Finishing with more than one value means numbers "
         "that nothing consumed, which is also malformed. Checking both is "
         "three lines and is the difference between a solution and a robust "
         "one.</p>"),
        ("The follow-up: converting from infix",
         "<p>\"How would you get postfix in the first place?\" The shunting-yard "
         "algorithm, and it is the same structure twice: one stack for "
         "operators, one output list. Numbers go straight to the output; an "
         "operator pops every operator of higher or equal precedence before "
         "pushing itself; brackets push and pop. Worth being able to name even "
         "if you are not asked to write it &mdash; it is the reason postfix "
         "exists as an intermediate form.</p>"),
    ],
    code={
        "file": "rpn.py",
        "intro": "The evaluator, the two orderings that separate right from "
                 "wrong, and the division that differs on negative operands.",
        "code": '''def evaluate(tokens):
    stack = []
    for t in tokens:
        if t not in ("+", "-", "*", "/"):
            stack.append(int(t))
            continue
        b = stack.pop()                  # FIRST pop is the right operand
        a = stack.pop()
        if t == "+":   stack.append(a + b)
        elif t == "-": stack.append(a - b)
        elif t == "*": stack.append(a * b)
        else:          stack.append(int(a / b))   # truncate toward zero
    if len(stack) != 1:
        raise ValueError("malformed: %d values left" % len(stack))
    return stack[0]

print("4 13 5 / +        ->", evaluate(["4", "13", "5", "/", "+"]), "(expect 6)")
print("5 1 2 + 4 * + 3 - ->", evaluate(["5","1","2","+","4","*","+","3","-"]),
      "(expect 14)")

# Pop order: wrong for - and / , right for + and *.
def evaluate_swapped(tokens):
    stack = []
    for t in tokens:
        if t not in ("+", "-", "*", "/"):
            stack.append(int(t)); continue
        a = stack.pop(); b = stack.pop()          # swapped on purpose
        stack.append({"+": a + b, "-": a - b, "*": a * b,
                      "/": int(a / b)}[t])
    return stack[0]

print()
print("3 4 -   correct:", evaluate(["3","4","-"]),
      " swapped:", evaluate_swapped(["3","4","-"]))
print("3 4 +   correct:", evaluate(["3","4","+"]),
      " swapped:", evaluate_swapped(["3","4","+"]), " <- agrees, so + hides it")

# Division: Python floors, postfix truncates.
print()
print("the division trap:")
for a, b in ((-7, 2), (7, -2), (7, 2)):
    print(f"  {a:>3} / {b:<3}  a // b = {a // b:>3}   int(a / b) = {int(a / b):>3}")
print("only the negative cases differ, which is why this bug ships")

# The depth check, and the two ways an expression can be malformed.
print()
for bad in (["1", "+"], ["1", "2", "3", "+"]):
    try:
        evaluate(bad)
    except (IndexError, ValueError) as e:
        print(f"  {bad} -> {type(e).__name__}: {e}")
''',
        "walk": [
            ("b = stack.pop(); a = stack.pop()",
             "The order is the answer to half this question. <code>b</code> "
             "came off first, so it is the right-hand operand of "
             "<code>a - b</code>."),
            ("int(a / b)",
             "Truncation toward zero. <code>a // b</code> floors, which differs "
             "for exactly the cases where one operand is negative &mdash; and "
             "agrees everywhere else, which is what makes it a late-arriving "
             "bug."),
            ("if len(stack) != 1: raise",
             "The depth is a free validity check. One value means well-formed; "
             "more means numbers nothing consumed."),
            ("evaluate_swapped([\"3\",\"4\",\"+\"])",
             "Printed beside the correct version to make the point that "
             "<code>+</code> and <code>*</code> cannot detect the swap. Test "
             "with subtraction or you will not find it."),
        ],
        "try": [
            "Add <code>%</code> and <code>**</code>. The modulo has the same "
            "sign disagreement as division, and exponentiation is the first "
            "operator here that is not commutative <em>or</em> associative.",
            "Feed it <code>[\"2\", \"0\", \"/\"]</code>. Decide whether the right "
            "answer is an exception or a sentinel, and say which before you "
            "write it.",
        ],
    },
    check=[
        {"q": "In a - b, which value was popped first?",
         "options": ["a", "b", "Either; it does not matter", "Both at once"],
         "answer": 1,
         "why": "The first pop is the top of the stack, which is the "
                "right-hand operand. Getting it backwards negates the result."},
        {"q": "Why int(a / b) rather than a // b?",
         "options": ["It is faster",
                     "// floors, and postfix truncates toward zero - they differ when one operand is negative",
                     "// does not work on integers",
                     "They are identical"],
         "answer": 1,
         "why": "-7 // 2 is -4 while int(-7 / 2) is -3. They agree for "
                "positive operands, so the bug only appears on a negative "
                "test case."},
        {"q": "What does the stack depth at the end tell you?",
         "options": ["Nothing useful",
                     "Exactly one value means well-formed; more means operands nothing consumed",
                     "The number of operators",
                     "The recursion depth"],
         "answer": 1,
         "why": "Each number adds one and each binary operator nets minus one, "
                "so a valid expression ends at depth 1."},
        {"q": "Why does postfix need no parentheses?",
         "options": ["It only allows two operands",
                     "The token order already fixes the evaluation order",
                     "Operators have no precedence",
                     "It is evaluated right to left"],
         "answer": 1,
         "why": "An operator's operands are always the most recent unconsumed "
                "values, which is what the top of the stack holds."},
    ],
)


# =========================================================================
# 3. daily temperatures - the monotonic stack
# =========================================================================

def _monotonic_frames():
    """Recorded by running the monotonic stack and logging every resolution."""
    temps = [73, 74, 75, 71, 69, 72, 76]
    answer = [0] * len(temps)
    stack, out = [], []
    for i, t in enumerate(temps):
        resolved = []
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            answer[j] = i - j
            resolved.append(j)
        stack.append(i)
        marks = {k: "dim" for k in range(len(temps))}
        for k in stack:
            marks[k] = "lo"
        for k in resolved:
            marks[k] = "hit"
        marks[i] = "lo"
        note = ("day %d is %d. Warmer than %s, so %s now have their answer, "
                "then %d is pushed."
                % (i, t, ", ".join("day %d" % k for k in resolved),
                   "they" if len(resolved) > 1 else "it", i)
                if resolved else
                "day %d is %d. Not warmer than the day on top, so nothing "
                "resolves - push and move on." % (i, t))
        out.append(frame(
            [marked(temps, marks, {i: "i"}, label="temperatures"),
             marked([temps[k] for k in stack] or ["(empty)"],
                    {len(stack) - 1: "lo"} if stack else {},
                    label="stack (decreasing)"),
             marked(answer, {k: ("done" if answer[k] else "dim")
                             for k in range(len(answer))}, label="answer")],
            note, {"i": i, "waiting": len(stack)}))
    out.append(frame(
        [marked(temps, {k: ("bad" if k in stack else "done")
                        for k in range(len(temps))}, label="temperatures"),
         marked(answer, {k: ("done" if answer[k] else "bad")
                         for k in range(len(answer))}, label="answer")],
        "Whatever is left on the stack never found a warmer day, so those "
        "entries stay 0. Every index was pushed once and popped at most once "
        "- that is why this is O(n) despite the inner loop.",
        {"i": len(temps) - 1, "waiting": len(stack)}))
    return viz(out)


_q(
    slug="daily-temperatures",
    kind="coding",
    level="Medium",
    title="Daily temperatures, and the monotonic stack",
    asked="For each day, how many days until a warmer temperature? Return 0 "
          "if there is none.",
    desc="The monotonic stack: keep indices whose answer is still unknown, "
         "resolve them when a bigger value arrives, and why the inner while "
         "loop is still O(n) overall.",
    lead="Keep a stack of <strong>indices whose answer is not known yet</strong>, "
         "with temperatures decreasing from the bottom. When a warmer day "
         "arrives it resolves every index it beats, popping them. Each index is "
         "pushed once and popped at most once, so the nested loop is still "
         "<strong>O(n)</strong>.",
    say="\"A monotonic decreasing stack of indices. For each day I pop every "
        "index whose temperature is lower than today's and record the "
        "difference as their answer, then push today. Each index is pushed and "
        "popped at most once, so it is O(n) time and O(n) space - the inner "
        "while loop does not make it quadratic.\"",
    notice=[
        "The stack holds <em>indices</em>, not temperatures &mdash; the answer "
        "is a distance.",
        "One warm day can resolve several waiting days at once.",
        "Anything still on the stack at the end never found a warmer day, so "
        "it stays 0.",
    ],
    viz=_monotonic_frames(),
    sections=[
        ("The question behind the question",
         "<p>\"Days until something bigger\" is the <strong>next greater "
         "element</strong> problem, and recognising it is most of the value "
         "here. The brute force is a scan forward from every position, O(n"
         "&sup2;), and it is doing the same comparisons over and over.</p>"
         "<p>The insight is to invert it. Instead of asking each day to look "
         "forward for its answer, let each day <em>announce itself</em> to the "
         "days still waiting. A day is waiting precisely because nothing "
         "warmer has arrived, which means the waiting days are in decreasing "
         "order of temperature &mdash; and a decreasing sequence you only ever "
         "append to or trim from the end is a stack.</p>"),
        ("Why the nested loop is not quadratic",
         "<p>This is the part interviewers probe, because the code has a "
         "<code>while</code> inside a <code>for</code> and looks O(n&sup2;).</p>"
         "<p>Count the work by element rather than by iteration. Each index is "
         "pushed exactly once. Each index is popped at most once, and once "
         "popped it never returns. So the total number of stack operations "
         "across the whole run is at most 2n, whatever the shape of the input "
         "&mdash; the inner loop can be long on one iteration only by being "
         "empty on others.</p>"
         "<p>The editor below prints the push and pop counts, including for a "
         "2,000-element worst case, so the 2n bound is a number rather than an "
         "assertion. This accounting argument is called amortised analysis, "
         "and naming it is worth doing.</p>"),
        ("Decreasing or increasing, and strict or not",
         "<p>Two decisions define the variant, and they are where the "
         "off-by-one errors live.</p>"
         "<p><strong>Direction.</strong> A decreasing stack finds the next "
         "<em>greater</em> element; an increasing stack finds the next "
         "<em>smaller</em> one. The comparison in the <code>while</code> is "
         "the only thing that changes.</p>"
         "<p><strong>Strictness.</strong> <code>&lt;</code> versus "
         "<code>&lt;=</code> decides what happens on equal values &mdash; "
         "whether \"warmer\" means strictly warmer. With <code>&lt;</code> an "
         "equal temperature does not resolve the earlier day, which is the "
         "usual reading of this problem. If the interviewer says \"at least as "
         "warm\", it flips.</p>"),
        ("Where else this shape appears",
         "<p>Once the pattern is visible it is everywhere: the largest "
         "rectangle in a histogram, trapping rain water, the stock span "
         "problem, sliding-window maximum (with a deque rather than a stack), "
         "and removing k digits to make the smallest number. All of them keep "
         "a monotonic sequence of candidates and discard the ones that a new "
         "arrival has made irrelevant.</p>"
         "<p>The tell, in any problem statement: \"the next\" or \"the "
         "previous\" element that is bigger or smaller. That phrasing is the "
         "monotonic stack asking to be used.</p>"),
    ],
    code={
        "file": "monotonic.py",
        "intro": "The brute force and the stack side by side with their "
                 "operation counts, then the 2n bound measured on a 2,000-element "
                 "worst case.",
        "code": '''def brute(temps):
    out = [0] * len(temps)
    checks = 0
    for i in range(len(temps)):
        for j in range(i + 1, len(temps)):
            checks += 1
            if temps[j] > temps[i]:
                out[i] = j - i
                break
    return out, checks


def monotonic(temps):
    out = [0] * len(temps)
    stack = []                        # indices, temperatures decreasing
    pushes = pops = 0
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop(); pops += 1
            out[j] = i - j            # i is the first warmer day for j
        stack.append(i); pushes += 1
    return out, pushes, pops


temps = [73, 74, 75, 71, 69, 72, 76, 73]
b_out, checks = brute(temps)
m_out, pushes, pops = monotonic(temps)
print("temps    :", temps)
print("brute    :", b_out, " comparisons:", checks)
print("monotonic:", m_out, " pushes:", pushes, "pops:", pops)
print("same answer:", b_out == m_out)

print()
print("each index is pushed once and popped at most once, so the total is")
print(f"{pushes} + {pops} = {pushes + pops} operations for n = {len(temps)}")

# The shape that looks worst for the inner loop: one warm day at the end.
worst = list(range(2_000, 0, -1)) + [9_999]
_, p2, q2 = monotonic(worst)
print()
print(f"n = {len(worst)} (all decreasing, then one spike)")
print(f"  pushes {p2:,}  pops {q2:,}  total {p2 + q2:,}  <- about 2n, not n^2")
print(f"  n^2 would be {len(worst) ** 2:,}")

# Strictness: what happens on equal temperatures.
def monotonic_loose(temps):
    out = [0] * len(temps); stack = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] <= t:     # <= instead of <
            j = stack.pop(); out[j] = i - j
        stack.append(i)
    return out

flat = [70, 70, 70, 71]
print()
print("temps", flat)
print("  strictly warmer (<) :", monotonic(flat)[0])
print("  at least as warm (<=):", monotonic_loose(flat))
''',
        "walk": [
            ("while stack and temps[stack[-1]] < t",
             "The day on top of the stack is the most recent unresolved one. "
             "If today beats it, its answer is known now &mdash; and possibly "
             "the one beneath it too, which is why this is a loop."),
            ("out[j] = i - j",
             "The stack holds indices precisely so this subtraction is "
             "available. Storing temperatures instead loses the distance, "
             "which is the answer being asked for."),
            ("pushes + pops",
             "The amortised argument, as a number. Each index enters once and "
             "leaves at most once, so this total is bounded by 2n regardless "
             "of the input's shape."),
            ("while stack and temps[stack[-1]] <= t",
             "The loose variant, printed on a run of equal temperatures. "
             "Whether equal counts as warmer is a question to ask, not to "
             "assume."),
        ],
        "try": [
            "Reverse the comparison to <code>&gt;</code> and you have "
            "\"days until a colder temperature\" &mdash; the same code, an "
            "increasing stack, a different question.",
            "Return the <em>index</em> of the next warmer day instead of the "
            "distance. One character changes, and it is the version most other "
            "next-greater-element problems actually want.",
        ],
    },
    check=[
        {"q": "What does the stack hold?",
         "options": ["Temperatures", "Indices whose answer is not yet known",
                     "The answers", "Days already resolved"],
         "answer": 1,
         "why": "Indices, so the answer can be computed as a difference - and "
                "they are exactly the days still waiting for a warmer one."},
        {"q": "Why is the algorithm O(n) despite a while loop inside a for loop?",
         "options": ["The while loop runs at most twice",
                     "Each index is pushed once and popped at most once, so the total work is bounded by 2n",
                     "Because the input is sorted",
                     "It is not; it is O(n log n)"],
         "answer": 1,
         "why": "Count by element, not by iteration. A long inner loop on one "
                "step is paid for by empty inner loops on others."},
        {"q": "What happens to indices still on the stack at the end?",
         "options": ["They are resolved with the last value",
                     "Their answer stays 0, because no warmer day ever arrived",
                     "They cause an error",
                     "They are popped and discarded"],
         "answer": 1,
         "why": "Being on the stack means nothing warmer was found, which is "
                "exactly what 0 is supposed to mean."},
        {"q": "To find the next SMALLER element instead, you would:",
         "options": ["Reverse the input",
                     "Flip the comparison, making the stack increasing",
                     "Use a queue",
                     "Sort first"],
         "answer": 1,
         "why": "Direction of monotonicity and the comparison are the same "
                "decision; nothing else in the algorithm changes."},
    ],
)


# =========================================================================
# 4. a queue from two stacks
# =========================================================================

def _twostack_frames():
    """Recorded by running the operations against the real implementation."""
    inbox, outbox, out = [], [], []
    ops = [("enq", "a"), ("enq", "b"), ("deq", None), ("enq", "c"),
           ("deq", None), ("deq", None)]
    for kind, x in ops:
        note = ""
        moved = 0
        if kind == "enq":
            inbox.append(x)
            note = ("enqueue %r: straight onto the inbox. Nothing is "
                    "reordered, which is why enqueue is always O(1)." % x)
        else:
            if not outbox:
                while inbox:
                    outbox.append(inbox.pop())
                    moved += 1
                note = ("dequeue: the outbox was empty, so the inbox is poured "
                        "into it - %d move%s - which REVERSES the order. "
                        % (moved, "" if moved == 1 else "s"))
            else:
                note = "dequeue: the outbox already has items, so nothing moves. "
            v = outbox.pop()
            note += "Then pop %r off the outbox: the oldest item, so FIFO." % v
        out.append(frame(
            [marked(inbox or ["(empty)"],
                    {len(inbox) - 1: "lo"} if inbox else {},
                    label="inbox (push here)"),
             marked(outbox or ["(empty)"],
                    {len(outbox) - 1: "hit"} if outbox else {},
                    label="outbox (pop here)")],
            note, {"moved": moved, "size": len(inbox) + len(outbox)}))
    out.append(frame(
        pairs([("enqueue", "O(1) always"),
               ("dequeue", "O(1) amortised"),
               ("worst single dequeue", "O(n)"),
               ("total moves for n items", "n")],
              {"dequeue": "hit"}, label="the cost"),
        "Each item crosses from inbox to outbox exactly once in its life. So "
        "one dequeue can be O(n), and n dequeues together are still O(n) - "
        "which is what amortised means.",
        {"moved": 0, "size": 0}))
    return viz(out)


_q(
    slug="queue-from-two-stacks",
    kind="coding",
    level="Easy",
    title="Implement a queue using two stacks",
    asked="Implement a FIFO queue using only stacks. What is the cost of each "
          "operation?",
    desc="A queue from two stacks: why pouring only when the outbox is empty "
         "makes dequeue O(1) amortised, and why refilling on every call is "
         "O(n) per operation.",
    lead="Two stacks: push onto the <strong>inbox</strong>, pop from the "
         "<strong>outbox</strong>. When the outbox is empty, pour the whole "
         "inbox into it &mdash; which reverses the order, turning LIFO into "
         "FIFO. Pouring <em>only when empty</em> is what makes dequeue "
         "<strong>O(1) amortised</strong>; pouring every time makes it O(n).",
    say="\"One stack for incoming, one for outgoing. Enqueue pushes onto the "
        "inbox. Dequeue pops the outbox, and if the outbox is empty first it "
        "moves everything across, which reverses the order into FIFO. Enqueue "
        "is O(1); dequeue is O(1) amortised, because each element moves "
        "between the stacks exactly once in its lifetime, even though a single "
        "dequeue can be O(n).\"",
    notice=[
        "Enqueue never reorders anything &mdash; it is always one push.",
        "The pour happens <em>only</em> when the outbox is empty, and it "
        "reverses the order.",
        "While the outbox has items, dequeue does no moving at all.",
    ],
    viz=_twostack_frames(),
    sections=[
        ("Why reversing twice gives FIFO",
         "<p>A stack reverses what you put into it. Pour one stack into "
         "another and you have reversed it again, which restores the original "
         "order &mdash; so the item pushed first ends up on top of the second "
         "stack, which is exactly the front of a queue.</p>"
         "<p>That is the whole trick, and it is worth stating in one sentence "
         "in an interview: <em>the inbox has them newest-first, the outbox has "
         "them oldest-first, and pouring is what converts between the "
         "two</em>.</p>"),
        ("The emptiness check is the entire complexity argument",
         "<p>The naive version pours on every dequeue &mdash; and, to keep "
         "enqueue working, pours back afterwards. That is O(n) per call and "
         "O(n&sup2;) for n dequeues. The editor below measures it: 400 "
         "operations cost 160,000 moves that way, against 400 the right "
         "way.</p>"
         "<p>Pouring only when the outbox is empty means each element crosses "
         "once in its entire life. Total moves for n items is n, so the "
         "average cost per dequeue is constant even though one individual "
         "dequeue can touch every element. That is amortised O(1), and the "
         "distinction between \"amortised O(1)\" and \"O(1) worst case\" is "
         "what the follow-up question is about.</p>"),
        ("When amortised is not good enough",
         "<p>Amortised bounds are about totals, and some systems care about "
         "the worst single call. A real-time audio callback or a request with "
         "a latency budget cannot afford the one dequeue that moves ten "
         "thousand items, even if the average is fine.</p>"
         "<p>The honest answer is that this structure cannot fix that &mdash; "
         "and naming the alternatives is what a strong answer does. Move a "
         "constant number of items per operation instead of all of them "
         "(incremental rebuilding), or use a structure that is O(1) worst case "
         "outright, which in Python is <code>collections.deque</code>. Which "
         "leads to the real-world footnote: nobody builds a queue from two "
         "stacks in production. The question is about reasoning, and it is fair "
         "to say so while still answering it.</p>"),
        ("The mirror question",
         "<p>\"Now implement a stack using two queues.\" It is the same idea and "
         "strictly worse: one of the two operations has to become O(n), because "
         "a queue gives you the wrong end and no amount of shuffling amortises "
         "away. Either push moves everything into the second queue behind the "
         "new item, or pop moves n&minus;1 items across to reach the last "
         "one.</p>"
         "<p>There is no trick that makes both O(1) here, and saying that "
         "directly is the right answer &mdash; the asymmetry between the two "
         "questions is the thing being tested.</p>"),
    ],
    code={
        "file": "two_stacks.py",
        "intro": "FIFO order demonstrated through interleaved operations, then "
                 "the move counts for the amortised and the eager versions at "
                 "400 operations each.",
        "code": '''class Queue:
    """Amortised O(1): pour only when the outbox is empty."""
    def __init__(self):
        self.inbox, self.outbox = [], []
        self.moves = 0

    def enqueue(self, x):
        self.inbox.append(x)

    def dequeue(self):
        if not self.outbox:                  # ONLY when empty
            while self.inbox:
                self.outbox.append(self.inbox.pop())
                self.moves += 1
        if not self.outbox:
            raise IndexError("dequeue from an empty queue")
        return self.outbox.pop()

    def __len__(self):
        return len(self.inbox) + len(self.outbox)


class QueueEager:
    """The version that pours every time: O(n) per dequeue."""
    def __init__(self):
        self.inbox, self.outbox = [], []
        self.moves = 0

    def enqueue(self, x):
        self.inbox.append(x)

    def dequeue(self):
        while self.inbox:
            self.outbox.append(self.inbox.pop()); self.moves += 1
        v = self.outbox.pop()
        while self.outbox:                   # and pour back again
            self.inbox.append(self.outbox.pop()); self.moves += 1
        return v


# FIFO survives interleaving, which is the part worth checking.
q = Queue()
for x in "abc":
    q.enqueue(x)
first, second = q.dequeue(), q.dequeue()
q.enqueue("d")
third, fourth = q.dequeue(), q.dequeue()
print("dequeue order:", first, second, third, fourth, " <- FIFO preserved")
print("enqueued c before d, and c came out first:", third == "c")

# The cost of the emptiness check, measured.
print()
N = 400
for name, cls in (("amortised (pour when empty)", Queue),
                  ("eager (pour every time)   ", QueueEager)):
    inst = cls()
    for i in range(N):
        inst.enqueue(i)
    for i in range(N):
        inst.dequeue()
    print(f"  {name}  {N} enqueues + {N} dequeues -> {inst.moves:,} moves")

print()
print("  each element crosses between the stacks ONCE in its whole life,")
print(f"  so the total is {N} moves for n = {N} - not {N} moves per call.")

# One dequeue can still be O(n) - amortised is about the total.
q = Queue()
for i in range(1_000):
    q.enqueue(i)
before = q.moves
q.dequeue()
print()
print("a single dequeue after 1,000 enqueues moved", q.moves - before, "items")
print("the next one moves", end=" ")
before = q.moves
q.dequeue()
print(q.moves - before, "- which is what amortised means")
''',
        "walk": [
            ("if not self.outbox:",
             "The line the whole question turns on. Pouring unconditionally is "
             "correct and O(n) per call; pouring only when empty is correct "
             "and O(1) amortised."),
            ("self.outbox.append(self.inbox.pop())",
             "Popping from one and pushing to the other is the reversal. After "
             "the pour, the oldest item is on top of the outbox."),
            ("inst.moves",
             "400 against 160,000 for the same workload. The counter is in the "
             "class so the difference is a measurement rather than a claim "
             "about big-O."),
            ("a single dequeue after 1,000 enqueues",
             "1,000 moves on that call and 0 on the next. Amortised O(1) is a "
             "statement about the total, and this is what it looks like from "
             "inside."),
        ],
        "try": [
            "Add <code>peek()</code>. It needs the same emptiness check as "
            "<code>dequeue</code>, and forgetting it is the standard bug in "
            "this extension.",
            "Try implementing a <em>stack</em> from two queues and count the "
            "moves. One of the two operations stays O(n) however you arrange "
            "it, which is the asymmetry worth being able to explain.",
        ],
    },
    check=[
        {"q": "Why does pouring one stack into the other give FIFO order?",
         "options": ["Because stacks are sorted",
                     "A stack reverses; reversing twice restores the original order, so the oldest item ends up on top",
                     "Because the inbox is kept sorted",
                     "It does not; the order is LIFO"],
         "answer": 1,
         "why": "The inbox holds them newest-first and the outbox oldest-first. "
                "Pouring is the conversion."},
        {"q": "What makes dequeue O(1) amortised rather than O(n)?",
         "options": ["The inbox is always small",
                     "Pouring only when the outbox is empty, so each element crosses once in its lifetime",
                     "Python lists are fast",
                     "Nothing; it is O(n)"],
         "answer": 1,
         "why": "Total moves for n items is n. One call can be O(n), and n "
                "calls together are still O(n)."},
        {"q": "What is the cost of a single worst-case dequeue?",
         "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
         "answer": 1,
         "why": "The call that finds an empty outbox moves everything across. "
                "Amortised O(1) does not mean O(1) worst case, and the "
                "difference matters under a latency budget."},
        {"q": "Implementing a stack from two queues instead:",
         "options": ["Works with the same amortised trick",
                     "Forces one of the two operations to be O(n) - the asymmetry is the point",
                     "Is impossible",
                     "Needs three queues"],
         "answer": 1,
         "why": "A queue hands you the wrong end, and no shuffling amortises "
                "that away. Saying so is the right answer."},
    ],
)
