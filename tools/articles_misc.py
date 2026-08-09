# -*- coding: utf-8 -*-
"""Written explanations for the remaining thin pages.

The last seventeen pages under 400 words of prose, across the Python, machine
learning, computer vision, generative AI and database tracks. Grouped in one
file because none of these tracks had more than a handful.

Note the python/ pages are code-runner pages (data-vz-py), so build_labs.py
suppresses run buttons on them - their "try this" sections describe edits to
make in the editor rather than controls to move.

Rendered by tools/build_articles.py. Edit here, then `npm run build`.
"""

ARTICLES_MISC = {

# =========================================================== python ==========
"python/if_elif_else.html": {
 "intro": "A condition is checked, one branch runs, and the rest are skipped entirely. The order you write the branches in is part of the logic, not a matter of style.",
 "sections": [
  ("Only the first match runs",
   "<p>Python evaluates each condition in turn from the top. The moment one is true, that block runs and <em>every remaining branch is skipped</em> &mdash; including ones that would also have been true. The <span class=\"mono-font\">else</span> runs only if nothing matched.</p>"
   "<p class=\"mono-font\">if score &gt;= 90:<br>&nbsp;&nbsp;&nbsp;&nbsp;grade = \"A\"<br>elif score &gt;= 70:<br>&nbsp;&nbsp;&nbsp;&nbsp;grade = \"C\"<br>else:<br>&nbsp;&nbsp;&nbsp;&nbsp;grade = \"F\"</p>"
   "<p>A score of 95 matches the first condition and stops. It never reaches the second, even though 95 is also &ge; 70. This exclusivity is what makes the chain a decision rather than a list of checks.</p>"),
  ("Why order is logic",
   "<p>Reverse those first two branches and the code breaks. If <span class=\"mono-font\">score &gt;= 70</span> came first, a score of 95 would match it and print C &mdash; the 90 branch would be unreachable for every value that could satisfy it.</p>"
   "<p>The rule is <strong>specific first, general last</strong>. A broad condition placed early shadows every narrower one after it, and the failure is silent: the code runs, produces a plausible answer, and is wrong.</p>"
   "<p>This is also why separate <span class=\"mono-font\">if</span> statements are not the same as <span class=\"mono-font\">elif</span>. Three consecutive <span class=\"mono-font\">if</span>s are three independent checks and all three can run; an if/elif/elif chain runs at most one.</p>"),
  ("Truthiness",
   "<p>The condition does not have to be a comparison. Python treats several values as false in a boolean context: <span class=\"mono-font\">False</span>, <span class=\"mono-font\">None</span>, <span class=\"mono-font\">0</span>, <span class=\"mono-font\">0.0</span>, and every empty container &mdash; <span class=\"mono-font\">\"\"</span>, <span class=\"mono-font\">[]</span>, <span class=\"mono-font\">{}</span>, <span class=\"mono-font\">()</span>. Everything else is true.</p>"
   "<p>So <span class=\"mono-font\">if items:</span> is the idiomatic way to ask “is this list non-empty?”, and it reads better than <span class=\"mono-font\">if len(items) &gt; 0:</span>.</p>"
   "<p>The trap is that <span class=\"mono-font\">0</span> and <span class=\"mono-font\">None</span> are both falsy but mean different things. If a variable can legitimately be 0, test <span class=\"mono-font\">if x is not None:</span> explicitly &mdash; otherwise a real value of 0 is treated as missing.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Watch the skip.</strong> Run the example with a value that satisfies the first condition, then add a print inside the second branch. It never appears &mdash; the branch is not merely false, it is never evaluated.</li>"
   "<li><strong>Break it by reordering.</strong> Swap the first two conditions and run again with the same input. You get a different, wrong answer from identical logic in a different order.</li>"
   "<li><strong>Drop the else.</strong> Remove the final branch and pass a value matching nothing. Nothing happens and no error is raised, which is the usual source of an unset variable further down.</li>"
   "<li><strong>Test truthiness directly.</strong> Try an empty string, an empty list and <span class=\"mono-font\">0</span> as the condition. All three take the else branch.</li>"
   "</ol>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Using <span class=\"mono-font\">=</span> instead of <span class=\"mono-font\">==</span>.</strong> Python raises a SyntaxError here rather than silently assigning, which is one of the friendlier language decisions.</li>"
   "<li><strong>Chaining separate ifs when you meant elif.</strong> Several branches run and the last one wins.</li>"
   "<li><strong><span class=\"mono-font\">if x == True:</span></strong> &mdash; redundant and subtly different from <span class=\"mono-font\">if x:</span>. Write the plain condition.</li>"
   "<li><strong>Mixing tabs and spaces.</strong> Indentation defines the block, so inconsistent whitespace changes which statements belong to the branch. Use four spaces throughout.</li>"
   "<li><strong>Testing a falsy-but-valid value.</strong> <span class=\"mono-font\">if count:</span> treats a genuine count of zero as absent.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>An if/elif/else chain evaluates conditions top to bottom and runs exactly one branch, so ordering is part of the logic &mdash; put specific conditions before general ones or the general one will shadow them. Conditions need not be comparisons, since empty containers, zero and None are all falsy; the exception worth remembering is that a meaningful zero must be tested against None explicitly rather than by truthiness.</p>"),
 ]},

"python/booleans_and_comparisons.html": {
 "intro": "Comparisons produce True or False, and combining them with and, or and not is how a program makes decisions. The details that catch people are short-circuiting and the difference between == and is.",
 "sections": [
  ("The comparison operators",
   "<p class=\"mono-font\">==&nbsp;&nbsp;equal to&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;!=&nbsp;&nbsp;not equal to<br>"
   "&lt;&nbsp;&nbsp;&nbsp;less than&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&gt;&nbsp;&nbsp;&nbsp;greater than<br>"
   "&lt;=&nbsp;&nbsp;less or equal&nbsp;&nbsp;&gt;=&nbsp;&nbsp;greater or equal</p>"
   "<p>Each returns a genuine boolean. Python also allows chained comparisons, which read exactly as they do in mathematics:</p>"
   "<p class=\"mono-font\">if 0 &lt;= age &lt; 130:</p>"
   "<p>This is not two separate comparisons glued together &mdash; Python evaluates <span class=\"mono-font\">age</span> once and checks both bounds, which is both faster and clearer than <span class=\"mono-font\">age &gt;= 0 and age &lt; 130</span>.</p>"),
  ("and, or, not - and short-circuiting",
   "<p><span class=\"mono-font\">and</span> is true only if both sides are; <span class=\"mono-font\">or</span> is true if either is; <span class=\"mono-font\">not</span> inverts.</p>"
   "<p>The important behaviour is <strong>short-circuiting</strong>: Python stops as soon as the answer is determined. In <span class=\"mono-font\">A and B</span>, if A is false then B is <em>never evaluated</em>. In <span class=\"mono-font\">A or B</span>, if A is true then B is never evaluated.</p>"
   "<p>That is not an optimisation detail, it is something you rely on constantly:</p>"
   "<p class=\"mono-font\">if items and items[0] == \"x\":</p>"
   "<p>If <span class=\"mono-font\">items</span> is empty the first operand is falsy, so the indexing never runs and there is no IndexError. Reverse the order and it crashes. Guard conditions belong on the left.</p>"),
  ("== compares value, is compares identity",
   "<p>This is the single most common source of confusion. <span class=\"mono-font\">==</span> asks whether two objects have the same <em>value</em>; <span class=\"mono-font\">is</span> asks whether they are the <em>same object</em> in memory.</p>"
   "<p class=\"mono-font\">a = [1, 2, 3]<br>b = [1, 2, 3]<br>a == b&nbsp;&nbsp;&rarr; True&nbsp;&nbsp;&nbsp;same contents<br>a is b&nbsp;&nbsp;&rarr; False&nbsp;&nbsp;different objects</p>"
   "<p>Almost always you want <span class=\"mono-font\">==</span>. The exception is comparing against the singletons <span class=\"mono-font\">None</span>, <span class=\"mono-font\">True</span> and <span class=\"mono-font\">False</span>, where <span class=\"mono-font\">x is None</span> is the correct idiom because there is exactly one None object.</p>"
   "<p>Small integers and short strings sometimes appear to work with <span class=\"mono-font\">is</span> because Python caches them &mdash; which makes the bug intermittent and therefore worse.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>See short-circuiting.</strong> Write <span class=\"mono-font\">False and print(\"ran\")</span> and run it. Nothing prints. Change the first operand to True and the print executes.</li>"
   "<li><strong>Guard an index.</strong> Try <span class=\"mono-font\">items and items[0]</span> with an empty list, then flip the operands and watch it raise IndexError.</li>"
   "<li><strong>Compare identity and value.</strong> Build two lists with the same contents and test both <span class=\"mono-font\">==</span> and <span class=\"mono-font\">is</span>. Same value, different objects.</li>"
   "<li><strong>Chain a comparison.</strong> Run <span class=\"mono-font\">1 &lt; 5 &lt; 10</span> and then <span class=\"mono-font\">10 &lt; 5 &lt; 1</span> to confirm both bounds are actually being checked.</li>"
   "</ol>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Using <span class=\"mono-font\">is</span> to compare values.</strong> Works by accident for small integers and cached strings, then fails on the first value outside the cache.</li>"
   "<li><strong>Putting the guard on the wrong side.</strong> Short-circuiting only protects what comes after it.</li>"
   "<li><strong>Comparing floats with <span class=\"mono-font\">==</span>.</strong> <span class=\"mono-font\">0.1 + 0.2 == 0.3</span> is False, because binary floating point cannot represent those values exactly. Use <span class=\"mono-font\">math.isclose</span>.</li>"
   "<li><strong>Writing <span class=\"mono-font\">if x == True</span>.</strong> Verbose and breaks for truthy-but-not-True values such as <span class=\"mono-font\">1</span> or a non-empty list.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Comparisons return booleans and can be chained the way they are written in mathematics. <span class=\"mono-font\">and</span> and <span class=\"mono-font\">or</span> short-circuit, which is what lets a guard on the left protect an expression on the right &mdash; so operand order matters. Use <span class=\"mono-font\">==</span> for value and reserve <span class=\"mono-font\">is</span> for None, True and False, and never compare floats for exact equality.</p>"),
 ]},

"python/for_loops_and_range.html": {
 "intro": "A for loop walks through a sequence, taking one item at a time. range() manufactures a sequence of numbers to walk through, without ever building the list.",
 "sections": [
  ("Iterating over items, not indices",
   "<p>Python’s for loop takes each element of a collection in turn:</p>"
   "<p class=\"mono-font\">for name in [\"ana\", \"bo\", \"cy\"]:<br>&nbsp;&nbsp;&nbsp;&nbsp;print(name)</p>"
   "<p>Note what is absent: no counter, no length, no indexing. The loop variable holds the <em>element</em>, not its position. Coming from C or Java the instinct is <span class=\"mono-font\">for i in range(len(items))</span> followed by <span class=\"mono-font\">items[i]</span>, and that is almost always the wrong shape in Python &mdash; it is longer, slower to read, and introduces an index you can get wrong.</p>"
   "<p>When you genuinely need the position as well, <span class=\"mono-font\">enumerate</span> gives you both:</p>"
   "<p class=\"mono-font\">for i, name in enumerate(items):</p>"),
  ("What range actually produces",
   "<p><span class=\"mono-font\">range</span> takes up to three arguments, matching slice syntax: start (inclusive, default 0), stop (exclusive), and step (default 1).</p>"
   "<p class=\"mono-font\">range(5)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; 0 1 2 3 4<br>"
   "range(2, 6)&nbsp;&nbsp;&nbsp;&rarr; 2 3 4 5<br>"
   "range(0, 10, 3) &rarr; 0 3 6 9<br>"
   "range(5, 0, -1) &rarr; 5 4 3 2 1</p>"
   "<p>The stop value is excluded, which is why <span class=\"mono-font\">range(5)</span> gives five numbers starting at zero and why <span class=\"mono-font\">range(len(items))</span> covers exactly the valid indices.</p>"
   "<p>Crucially, range does not build a list. It is a lazy object that computes each value as it is asked for, so <span class=\"mono-font\">range(10_000_000)</span> uses a constant few dozen bytes rather than hundreds of megabytes. Wrapping it in <span class=\"mono-font\">list()</span> throws that advantage away.</p>"),
  ("break, continue, else",
   "<p><span class=\"mono-font\">break</span> exits the loop immediately. <span class=\"mono-font\">continue</span> skips to the next iteration. Both apply to the innermost loop only.</p>"
   "<p>Python also allows an <span class=\"mono-font\">else</span> on a loop, which is genuinely useful and almost universally misread. The else block runs when the loop finishes <strong>without</strong> hitting a break:</p>"
   "<p class=\"mono-font\">for item in items:<br>&nbsp;&nbsp;&nbsp;&nbsp;if item == target:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;break<br>else:<br>&nbsp;&nbsp;&nbsp;&nbsp;print(\"not found\")</p>"
   "<p>Read it as “no break” rather than “else” and it makes sense: it is the natural place for the not-found case, without needing a flag variable.</p>"),
  ("Experiments to try",
   "<ol>"
   "<li><strong>Check the exclusive stop.</strong> Run <span class=\"mono-font\">range(5)</span> and count the values. Five numbers, ending at 4 &mdash; the stop is a boundary, not a member.</li>"
   "<li><strong>Count backwards.</strong> Try <span class=\"mono-font\">range(5, 0, -1)</span>, then <span class=\"mono-font\">range(5, 0)</span> with no step. The second produces nothing at all, because the default step of +1 can never reach a smaller stop.</li>"
   "<li><strong>Use enumerate.</strong> Loop over a list with and without enumerate and compare. The index comes for free rather than being maintained by hand.</li>"
   "<li><strong>Try the loop else.</strong> Search for a value that exists, then one that does not, and watch when the else block fires.</li>"
   "</ol>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Looping over indices out of habit.</strong> <span class=\"mono-font\">for i in range(len(items))</span> when you only use <span class=\"mono-font\">items[i]</span> is a C idiom transplanted into Python.</li>"
   "<li><strong>Off-by-one from the exclusive stop.</strong> To count 1 to 10 you need <span class=\"mono-font\">range(1, 11)</span>.</li>"
   "<li><strong>Modifying a list while looping over it.</strong> Removing items shifts everything after them, so the loop silently skips elements. Iterate over a copy, or build a new list.</li>"
   "<li><strong>Expecting the loop variable to be scoped to the loop.</strong> It leaks into the surrounding scope and keeps its final value after the loop ends.</li>"
   "<li><strong>Forgetting range is lazy.</strong> Printing it shows <span class=\"mono-font\">range(0, 5)</span> rather than the numbers; wrap it in <span class=\"mono-font\">list()</span> only to inspect it, not in real code.</li>"
   "</ul>"),
  ("The short version",
   "<p>A for loop iterates over elements directly, and <span class=\"mono-font\">enumerate</span> is how you get the index when you actually need it. <span class=\"mono-font\">range</span> generates numbers lazily with an exclusive stop, so it costs nothing regardless of size. The loop <span class=\"mono-font\">else</span> runs only when no break occurred, which makes it the clean way to handle a search that found nothing.</p>"),
 ]},

"python/strings_and_slicing.html": {
 "intro": "Strings are immutable sequences of characters. Slicing pulls out any part of one, and immutability means every operation that looks like a change is really building a new string.",
 "sections": [
  ("Immutable, and why that matters",
   "<p>A string cannot be modified in place. <span class=\"mono-font\">s[0] = \"H\"</span> raises a TypeError, and every method that appears to change a string &mdash; <span class=\"mono-font\">upper</span>, <span class=\"mono-font\">replace</span>, <span class=\"mono-font\">strip</span> &mdash; returns a <em>new</em> string and leaves the original untouched.</p>"
   "<p class=\"mono-font\">s = \"hello\"<br>s.upper()&nbsp;&nbsp;&nbsp;&rarr; \"HELLO\"<br>print(s)&nbsp;&nbsp;&nbsp;&nbsp;&rarr; \"hello\"&nbsp;&nbsp;unchanged</p>"
   "<p>Forgetting to assign the result is the most common string bug there is. The performance consequence matters too: building a string by repeated concatenation in a loop copies everything each time, which is quadratic. Collect the pieces in a list and <span class=\"mono-font\">\"\".join(parts)</span> at the end.</p>"),
  ("Slicing",
   "<p>Slices take <span class=\"mono-font\">[start:stop:step]</span>, with start inclusive, stop exclusive, and any part omittable. With <span class=\"mono-font\">s = \"Python\"</span>:</p>"
   "<p class=\"mono-font\">s[0]&nbsp;&nbsp;&nbsp;&nbsp;&rarr; \"P\"<br>"
   "s[-1]&nbsp;&nbsp;&nbsp;&rarr; \"n\"&nbsp;&nbsp;&nbsp;&nbsp;negative counts from the end<br>"
   "s[0:3]&nbsp;&nbsp;&rarr; \"Pyt\"<br>"
   "s[2:]&nbsp;&nbsp;&nbsp;&rarr; \"thon\"<br>"
   "s[:3]&nbsp;&nbsp;&nbsp;&rarr; \"Pyt\"<br>"
   "s[::2]&nbsp;&nbsp;&rarr; \"Pto\"<br>"
   "s[::-1]&nbsp;&rarr; \"nohtyP\"&nbsp;reversed</p>"
   "<p>The exclusive stop makes <span class=\"mono-font\">s[:k] + s[k:]</span> reconstruct the original for any k, and the length of <span class=\"mono-font\">s[a:b]</span> is simply <span class=\"mono-font\">b &minus; a</span>. Slices also never raise an IndexError &mdash; <span class=\"mono-font\">\"abc\"[10:20]</span> returns an empty string rather than crashing, unlike indexing a single position.</p>"),
  ("The methods worth knowing",
   "<p class=\"mono-font\">.strip()&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;remove surrounding whitespace<br>"
   ".split(\",\")&nbsp;&nbsp;&nbsp;split into a list on a separator<br>"
   "\",\".join(xs)&nbsp;&nbsp;join a list into one string<br>"
   ".replace(a, b)&nbsp;substitute every occurrence<br>"
   ".startswith(x)&nbsp;prefix test<br>"
   ".find(x)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;index or &minus;1 if absent</p>"
   "<p><span class=\"mono-font\">split</span> and <span class=\"mono-font\">join</span> are inverses and do most of the real work in text processing. Note that <span class=\"mono-font\">join</span> is called on the <em>separator</em>, not on the list &mdash; <span class=\"mono-font\">\", \".join(items)</span> &mdash; which surprises nearly everyone once.</p>"
   "<p>For building strings from values, f-strings are the modern form: <span class=\"mono-font\">f\"{name} is {age}\"</span>, with expressions and formatting allowed inside the braces.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Confirm immutability.</strong> Call <span class=\"mono-font\">.upper()</span> without assigning, then print the original. Unchanged &mdash; the result was discarded.</li>"
   "<li><strong>Reverse with a slice.</strong> Run <span class=\"mono-font\">s[::-1]</span> and check the original is untouched. Every slice is a new string.</li>"
   "<li><strong>Slice past the end.</strong> Try <span class=\"mono-font\">s[10:20]</span> on a short string. Empty result, no error &mdash; then try <span class=\"mono-font\">s[10]</span> and get IndexError.</li>"
   "<li><strong>Split and rejoin.</strong> Split on a comma, then join with a different separator, and watch the round trip.</li>"
   "</ol>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>Not assigning the result.</strong> <span class=\"mono-font\">s.replace(\"a\", \"b\")</span> alone does nothing observable.</li>"
   "<li><strong>Concatenating in a loop.</strong> Quadratic. Use a list and <span class=\"mono-font\">join</span>.</li>"
   "<li><strong>Calling join on the list.</strong> It is a method of the separator string.</li>"
   "<li><strong>Confusing <span class=\"mono-font\">find</span> and <span class=\"mono-font\">index</span>.</strong> <span class=\"mono-font\">find</span> returns &minus;1 when absent; <span class=\"mono-font\">index</span> raises.</li>"
   "<li><strong>Assuming one character is one byte.</strong> Python strings are Unicode, so a character may be several bytes when encoded &mdash; <span class=\"mono-font\">len()</span> counts characters, not bytes.</li>"
   "</ul>"),
  ("The short version",
   "<p>Strings are immutable sequences, so every transforming method returns a new string and the original never changes &mdash; assign the result, and never build strings by concatenation in a loop. Slicing uses an exclusive stop, accepts negative indices, and returns an empty string rather than raising when the range is out of bounds. <span class=\"mono-font\">split</span> and <span class=\"mono-font\">join</span> are the two methods most text processing is actually made of.</p>"),
 ]},

"python/functions_and_return.html": {
 "intro": "A function packages a piece of work behind a name. return sends a value back to the caller - and a function without one still returns something, which is the source of a great many confusing bugs.",
 "sections": [
  ("Defining and calling",
   "<p class=\"mono-font\">def area(width, height):<br>&nbsp;&nbsp;&nbsp;&nbsp;return width * height</p>"
   "<p><span class=\"mono-font\">width</span> and <span class=\"mono-font\">height</span> are <strong>parameters</strong> &mdash; names the function uses internally. The values supplied at the call site are <strong>arguments</strong>. Calling <span class=\"mono-font\">area(3, 4)</span> binds 3 to width and 4 to height, runs the body, and evaluates to 12.</p>"
   "<p>Arguments can be passed by position or by name, and keyword arguments are worth using whenever the meaning is not obvious: <span class=\"mono-font\">area(width=3, height=4)</span> cannot be got the wrong way round.</p>"),
  ("return, and the None you did not ask for",
   "<p><span class=\"mono-font\">return</span> does two things at once: it sends a value back and it <em>exits the function immediately</em>. Any code after it in the same path never runs, which is what makes early returns a clean way to handle edge cases.</p>"
   "<p>A function with no return statement still returns <span class=\"mono-font\">None</span>. So does one that reaches the end without hitting a return. That is why this is such a common bug:</p>"
   "<p class=\"mono-font\">def double(x):<br>&nbsp;&nbsp;&nbsp;&nbsp;x * 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# computed, then thrown away<br><br>result = double(5)&nbsp;&nbsp;&rarr; None</p>"
   "<p>The multiplication happens; nothing is sent back. There is no error, and the None surfaces later as a TypeError somewhere unrelated.</p>"
   "<p>Distinguish <span class=\"mono-font\">return</span> from <span class=\"mono-font\">print</span>: printing shows a value to a human, returning gives it to the calling code. A function that prints its answer instead of returning it cannot be used in a calculation.</p>"),
  ("Scope and default arguments",
   "<p>Names created inside a function are <strong>local</strong> to it and disappear when it ends. The function can read names from the enclosing scope but assigning to one creates a new local rather than modifying the outer variable, unless declared <span class=\"mono-font\">global</span> &mdash; which is nearly always the wrong solution.</p>"
   "<p>Default values let a parameter be optional: <span class=\"mono-font\">def greet(name, greeting=\"Hello\")</span>. Defaults must come after all non-default parameters.</p>"
   "<p>The famous trap is a <strong>mutable default</strong>. The default is evaluated <em>once</em>, when the function is defined, not on each call:</p>"
   "<p class=\"mono-font\">def add(item, target=[]):&nbsp;&nbsp;# wrong<br>&nbsp;&nbsp;&nbsp;&nbsp;target.append(item)<br>&nbsp;&nbsp;&nbsp;&nbsp;return target</p>"
   "<p>Every call that omits <span class=\"mono-font\">target</span> shares the same list, so results accumulate across calls. Use <span class=\"mono-font\">None</span> as the default and create the list inside the body.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Forget the return.</strong> Write a function that computes a value without returning it, then print the call. You get None, and no error to explain why.</li>"
   "<li><strong>Return early.</strong> Put a return before other statements and confirm the later ones never run.</li>"
   "<li><strong>Compare print and return.</strong> Write one function that prints and one that returns, then try to use each result in an arithmetic expression. Only the returning one works.</li>"
   "<li><strong>Trigger the mutable default.</strong> Define the buggy version above and call it three times. The list grows across calls, because there is only ever one of it.</li>"
   "</ol>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>Printing instead of returning.</strong> The value is displayed and then lost.</li>"
   "<li><strong>Falling off the end.</strong> A branch with no return silently yields None.</li>"
   "<li><strong>Mutable default arguments.</strong> Shared state between calls; use None.</li>"
   "<li><strong>Reaching for <span class=\"mono-font\">global</span>.</strong> Almost always better solved by returning a value and assigning it at the call site.</li>"
   "<li><strong>Calling without parentheses.</strong> <span class=\"mono-font\">f</span> is the function object; <span class=\"mono-font\">f()</span> calls it.</li>"
   "</ul>"),
  ("The short version",
   "<p>A function takes parameters, runs a body, and returns a value; without an explicit return it returns None, which is why a missing return shows up as a confusing error far from its cause. Return exits immediately, local names vanish when the call ends, and default arguments are evaluated once at definition time &mdash; so a mutable default is shared by every call that relies on it.</p>"),
 ]},

"python/dictionaries.html": {
 "intro": "A dictionary stores key-value pairs and finds any of them in constant time. It is the data structure Python itself is built out of, and the one that turns most quadratic loops into linear ones.",
 "sections": [
  ("Keys and values",
   "<p>A dict maps keys to values, written with braces:</p>"
   "<p class=\"mono-font\">ages = {\"ana\": 31, \"bo\": 27}<br>ages[\"ana\"]&nbsp;&nbsp;&rarr; 31<br>ages[\"cy\"] = 45&nbsp;&nbsp;# add<br>ages[\"bo\"] = 28&nbsp;&nbsp;# overwrite</p>"
   "<p>Keys are unique: assigning to an existing key replaces its value rather than adding a second entry. Values have no such constraint and can repeat freely.</p>"
   "<p>Lookup is <strong>O(1)</strong> &mdash; the cost does not grow with the size of the dict &mdash; because Python hashes the key to compute where the value is stored rather than searching for it. A list, by contrast, must scan.</p>"),
  ("Getting values without crashing",
   "<p>Indexing a missing key raises <span class=\"mono-font\">KeyError</span>. When a key may legitimately be absent, that is the wrong tool:</p>"
   "<p class=\"mono-font\">ages[\"zoe\"]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; KeyError<br>"
   "ages.get(\"zoe\")&nbsp;&nbsp;&nbsp;&rarr; None<br>"
   "ages.get(\"zoe\", 0)&nbsp;&rarr; 0&nbsp;&nbsp;&nbsp;custom default<br>"
   "\"zoe\" in ages&nbsp;&nbsp;&nbsp;&nbsp;&rarr; False</p>"
   "<p>Use <span class=\"mono-font\">get</span> when absence is expected and normal; let the KeyError happen when absence means something has genuinely gone wrong. Both are correct in the right place, and choosing between them is a statement about your assumptions.</p>"),
  ("Iterating",
   "<p class=\"mono-font\">for key in ages:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# keys<br>"
   "for v in ages.values():&nbsp;&nbsp;&nbsp;# values<br>"
   "for k, v in ages.items():&nbsp;# both</p>"
   "<p>Iterating a dict directly gives keys, which is why <span class=\"mono-font\">for key in ages</span> needs no method call. <span class=\"mono-font\">items()</span> is what you want most of the time.</p>"
   "<p>Since Python 3.7 dictionaries preserve <strong>insertion order</strong> as a language guarantee, so iteration returns keys in the order they were first added. Deleting a key and re-adding it moves it to the end.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Trigger a KeyError.</strong> Index a key that does not exist, then do the same with <span class=\"mono-font\">get</span>. One raises, the other returns None.</li>"
   "<li><strong>Overwrite a key.</strong> Assign to a key that is already present and check the length. It does not grow &mdash; keys are unique.</li>"
   "<li><strong>Check insertion order.</strong> Add several keys in a deliberate order and iterate. They come back in that order, not sorted.</li>"
   "<li><strong>Try an unhashable key.</strong> Use a list as a key and read the TypeError. Keys must be immutable, because their hash decides where the value lives.</li>"
   "</ol>"),
  ("Why dicts turn quadratic loops linear",
   "<p>This is the practical reason dictionaries matter so much. Checking membership in a list is O(n) because it scans; checking membership in a dict or set is O(1).</p>"
   "<p>So a loop over n items that checks each against a list of n items is O(n&sup2;) &mdash; a million operations for a thousand items. Convert the inner list to a set or dict first and the same loop is O(n): a thousand operations. That single substitution is the most common large speedup in everyday Python, and it is why building a lookup dict before a loop is such a reliable habit.</p>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Indexing where <span class=\"mono-font\">get</span> belongs.</strong> Turns an expected absence into a crash.</li>"
   "<li><strong>Mutating while iterating.</strong> Adding or removing keys inside a <span class=\"mono-font\">for</span> loop over the dict raises RuntimeError. Iterate over <span class=\"mono-font\">list(d)</span> instead.</li>"
   "<li><strong>Using a mutable object as a key.</strong> Lists and dicts are unhashable; tuples of immutables work.</li>"
   "<li><strong>Searching values in a loop.</strong> <span class=\"mono-font\">v in d.values()</span> is O(n) and undoes the whole benefit.</li>"
   "<li><strong>Hand-rolling counting.</strong> <span class=\"mono-font\">collections.Counter</span> and <span class=\"mono-font\">defaultdict</span> already do it.</li>"
   "</ul>"),
  ("What to remember",
   "<p>A dictionary maps unique, immutable keys to values with O(1) lookup, insertion and deletion, and preserves insertion order. Use <span class=\"mono-font\">get</span> when a key may reasonably be missing and indexing when it may not. Its biggest practical use is replacing repeated list scans: swapping an <span class=\"mono-font\">in list</span> check for an <span class=\"mono-font\">in dict</span> check is what turns an accidental O(n&sup2;) into O(n).</p>"),
 ]},

# ================================================= machine learning ==========
"machine_learning/cross_validation.html": {
 "intro": "One train-test split gives you one number, and that number depends on which rows happened to land in the test set. K-fold cross-validation uses every row for testing exactly once and reports the spread as well as the average.",
 "sections": [
  ("What a single split cannot tell you",
   "<p>Hold out 20% of the data, train on the rest, and you get an accuracy figure. Change the random seed and you get a different one &mdash; sometimes several points different on a small dataset.</p>"
   "<p>Neither number is wrong; both are estimates from a sample of test rows, and a sample of 200 rows carries real sampling error. With one split you have no way to tell whether a two-point difference between two models is a genuine improvement or the luck of the partition.</p>"),
  ("How k-fold works",
   "<p>Split the data into k equally sized folds. Then run k separate experiments: hold out fold 1 and train on folds 2&hellip;k, hold out fold 2 and train on the rest, and so on. Each fold serves as the test set exactly once, and each row is predicted exactly once by a model that never saw it.</p>"
   "<p>You end up with k scores. Report the <strong>mean</strong> as the performance estimate and the <strong>standard deviation</strong> as a measure of how stable it is. The standard deviation is the part a single split cannot give you, and it is often the more informative number: a model scoring 0.82 &plusmn; 0.01 is a very different proposition from one scoring 0.82 &plusmn; 0.09.</p>"
   "<p>k = 5 or k = 10 are the standard choices. Larger k means more training data per fold (less pessimistic bias) but k model fits and more correlated training sets. The extreme, k = n, is leave-one-out: nearly unbiased, high variance, and usually far too expensive.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>Watch each fold take its turn.</strong> Set <strong>Folds (k)</strong> to 5 and press <strong>Run Next Fold</strong> repeatedly. A different block becomes the test set each time, and the remaining blocks train.</li>"
   "<li><strong>Compare the fold scores.</strong> Press <strong>Auto-Run All</strong> and look at the individual results, not just the average. The spread between the best and worst fold is exactly the uncertainty a single split would have hidden.</li>"
   "<li><strong>Increase k.</strong> Set <strong>Folds (k)</strong> to 10 and run again. Each model trains on 90% of the data instead of 80%, and there are twice as many fits to pay for.</li>"
   "<li><strong>Shuffle first.</strong> Press <strong>Shuffle</strong> and re-run. If the data arrived sorted by class, unshuffled folds can be wildly unrepresentative &mdash; which is why stratification exists.</li>"
   "</ol>"),
  ("Stratified, grouped, and time series",
   "<p>Plain k-fold splits at random, which is wrong in three common situations:</p>"
   "<ul>"
   "<li><strong>Imbalanced classes</strong> &mdash; a random fold might contain almost none of the minority class. <strong>Stratified k-fold</strong> preserves the class proportions in every fold, and should be the default for classification.</li>"
   "<li><strong>Grouped data</strong> &mdash; multiple rows per patient, user or session. If rows from the same group land in both train and test, the model has effectively seen the answer. <strong>GroupKFold</strong> keeps each group entirely on one side.</li>"
   "<li><strong>Time series</strong> &mdash; random folds train on the future to predict the past, which is leakage in its purest form. Use a forward-chaining split where each fold trains only on data preceding its test window.</li>"
   "</ul>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Preprocessing before splitting.</strong> Fitting a scaler, imputer or feature selector on the whole dataset leaks test information into training and inflates every fold. Put the preprocessing inside a Pipeline so it is refitted within each fold.</li>"
   "<li><strong>Random folds on time series.</strong> Produces excellent scores and a model that fails in production.</li>"
   "<li><strong>Reporting only the mean.</strong> The standard deviation is what tells you whether a difference between two models is meaningful.</li>"
   "<li><strong>Tuning hyperparameters on the same CV used to report the score.</strong> Selecting on those folds means the reported number is optimistic; nested cross-validation is the correct fix.</li>"
   "<li><strong>Forgetting to shuffle sorted data.</strong> Folds become unrepresentative before stratification can help.</li>"
   "</ul>"),
  ("What to remember",
   "<p>K-fold cross-validation trains k models, each holding out a different fold, so every row is tested once and you get a mean <em>and</em> a spread rather than one seed-dependent number. Use stratified folds for classification, grouped folds when rows share a subject, and forward-chaining for time series. Whatever the variant, fit every preprocessing step inside the fold &mdash; doing it beforehand leaks the test set and quietly invalidates the whole exercise.</p>"),
 ]},

"machine_learning/confusion_matrix.html": {
 "intro": "Four numbers - TP, FP, FN, TN - and every classification metric is a ratio of them. Knowing which ratio to care about is the actual skill; accuracy is usually the wrong one.",
 "sections": [
  ("The four cells",
   "<p>For a binary classifier each prediction falls into one of four boxes:</p>"
   "<ul>"
   "<li><strong>True Positive (TP)</strong> &mdash; predicted positive, actually positive. Correct.</li>"
   "<li><strong>False Positive (FP)</strong> &mdash; predicted positive, actually negative. A false alarm; a Type I error.</li>"
   "<li><strong>False Negative (FN)</strong> &mdash; predicted negative, actually positive. A miss; a Type II error.</li>"
   "<li><strong>True Negative (TN)</strong> &mdash; predicted negative, actually negative. Correct.</li>"
   "</ul>"
   "<p>The two errors are not interchangeable, and which one hurts more is a property of the problem rather than the model. A cancer screen missing a tumour (FN) is far worse than flagging a healthy patient for a follow-up (FP). A spam filter deleting a real email (FP) is far worse than letting spam through (FN).</p>"),
  ("The metrics, and what each asks",
   "<p class=\"mono-font\">accuracy&nbsp; = (TP + TN) / (TP + FP + FN + TN)</p>"
   "<p class=\"mono-font\">precision = TP / (TP + FP)</p>"
   "<p class=\"mono-font\">recall&nbsp;&nbsp;&nbsp; = TP / (TP + FN)</p>"
   "<p class=\"mono-font\">F1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 2 &middot; (precision &middot; recall) / (precision + recall)</p>"
   "<p>Read them as questions. <strong>Precision</strong>: of everything I flagged, how much was real? <strong>Recall</strong>: of everything real, how much did I catch? Precision is about the cost of false alarms; recall is about the cost of misses.</p>"
   "<p><strong>F1</strong> is their harmonic mean, which &mdash; unlike an ordinary average &mdash; is dragged down hard by the smaller of the two. Precision 1.0 with recall 0.0 gives F1 = 0, not 0.5, which is the behaviour you want from a summary that should not reward ignoring one side entirely.</p>"),
  ("Why accuracy misleads",
   "<p>Take a dataset that is 99% negative &mdash; fraud detection, rare disease, defect inspection. A model that predicts “negative” for every single input scores <strong>99% accuracy</strong> and has no value whatsoever: TP = 0, so precision and recall are both zero.</p>"
   "<p>This is the accuracy paradox, and it is why accuracy is a poor default on any imbalanced problem. Precision, recall and F1 all ignore TN, which is exactly the cell that inflates accuracy when negatives dominate.</p>"),
  ("Experiments to try",
   "<ol>"
   "<li><strong>Build the paradox.</strong> Set <strong>True Positives (TP)</strong> to 0, <strong>False Negatives (FN)</strong> to 10, <strong>False Positives (FP)</strong> to 0 and <strong>True Negatives (TN)</strong> to 990. Accuracy reads 99% while precision and recall are zero.</li>"
   "<li><strong>Trade one for the other.</strong> Raise <strong>False Positives (FP)</strong> while lowering <strong>False Negatives (FN)</strong>. Recall climbs and precision falls &mdash; the trade-off you make by lowering a decision threshold.</li>"
   "<li><strong>Find where F1 peaks.</strong> Adjust until precision and recall are close. F1 is highest when they are balanced, and collapses when either is small.</li>"
   "<li><strong>Randomize and read.</strong> Press <strong>Randomize</strong> and predict which metric will look best before checking. Whichever cell is largest drives it.</li>"
   "</ol>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>Reporting accuracy on imbalanced data.</strong> The single most common evaluation error.</li>"
   "<li><strong>Optimising precision or recall alone.</strong> Either can be made perfect trivially &mdash; predict positive for nothing, or for everything. They are only meaningful together.</li>"
   "<li><strong>Leaving the threshold at 0.5.</strong> The confusion matrix describes one threshold. Moving it moves every metric, and the right threshold comes from the relative cost of FP and FN.</li>"
   "<li><strong>Transposing the matrix.</strong> Libraries differ on whether rows are true or predicted labels. Check the axis before reading off FP and FN.</li>"
   "<li><strong>Using F1 when the errors have very different costs.</strong> F1 weights precision and recall equally; when they are not equally important, use F&beta; or state the costs directly.</li>"
   "</ul>"),
  ("What to remember",
   "<p>The confusion matrix holds the four counts every classification metric is built from, and the choice of metric is a statement about which error costs more. Precision asks how many flagged items were real, recall asks how many real items were caught, and F1 balances them harmonically so neither can be ignored. Accuracy includes true negatives, which is why it looks excellent on imbalanced data where the model has learned nothing.</p>"),
 ]},

"machine_learning/training_on_label_imbalanced_dataset.html": {
 "intro": "When 99% of your rows share one label, a model that always predicts that label scores 99%. Fixing imbalance means changing the data, the loss, or the threshold - and being honest about which metric you are reading.",
 "sections": [
  ("Why imbalance breaks training",
   "<p>Standard training minimises average loss over the dataset. When one class holds 99% of the rows, that average is dominated by it: predicting the majority everywhere already achieves very low loss, so there is little gradient pressure to learn the minority class at all.</p>"
   "<p>The model is not malfunctioning. It is optimising exactly what you asked it to, and what you asked for was the wrong thing &mdash; you wanted the rare class detected, and you told it to minimise overall error, which are different objectives whenever the classes are unequal.</p>"),
  ("The three families of fix",
   "<p><strong>Resample the data.</strong> <em>Oversampling</em> duplicates minority rows &mdash; simple, and risks overfitting to the few examples you have. <strong>SMOTE</strong> improves on it by synthesising new minority points along the lines between existing neighbours rather than copying. <em>Undersampling</em> discards majority rows, which balances the classes and throws away real information; it is reasonable when the majority class is genuinely enormous.</p>"
   "<p><strong>Reweight the loss.</strong> Give minority errors a larger weight, typically inversely proportional to class frequency, so one minority mistake costs as much as ninety-nine majority ones. This changes nothing about the data and is usually the first thing to try &mdash; <span class=\"mono-font\">class_weight=\"balanced\"</span> in scikit-learn, or <span class=\"mono-font\">pos_weight</span> in a PyTorch loss. <strong>Focal loss</strong> goes further by down-weighting examples the model already classifies confidently, concentrating training on the hard cases.</p>"
   "<p><strong>Move the threshold.</strong> Often the model’s probabilities are fine and only the 0.5 cutoff is wrong. Lowering it trades precision for recall without retraining anything, and choosing it from a precision-recall curve is frequently the cheapest real improvement available.</p>"),
  ("Experiments to try",
   "<ol>"
   "<li><strong>Start balanced.</strong> Set <strong>Class 0 Ratio</strong> to 50 and press <strong>Retrain Both Models</strong>. Both classes are learned and the boundary sits sensibly between them.</li>"
   "<li><strong>Make it severe.</strong> Raise <strong>Class 0 Ratio</strong> to 95 and retrain. The boundary shifts toward the minority class and swallows it &mdash; accuracy stays high while the minority class is barely detected.</li>"
   "<li><strong>Apply a fix.</strong> With the ratio still at 95, choose a strategy from <strong>Fix Strategy</strong> and retrain. The boundary moves back and minority recall recovers, at some cost in precision.</li>"
   "<li><strong>Push to the extreme.</strong> Set <strong>Class 0 Ratio</strong> to 99 and compare with and without a fix. At this level the unmitigated model is close to a constant predictor.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<ul>"
   "<li><strong>Resampling before splitting.</strong> The most damaging mistake here. Oversample first and duplicated (or SMOTE-interpolated) rows appear in both train and test, so the test set contains near-copies of training rows and the score is meaningless. Resample <em>inside</em> the training fold only.</li>"
   "<li><strong>Still reporting accuracy.</strong> If you fixed the training and kept the metric, you cannot see whether it worked. Use precision, recall, F1, or PR-AUC.</li>"
   "<li><strong>Using ROC-AUC on severe imbalance.</strong> It is computed over the whole threshold range and stays optimistic because true negatives are plentiful. Precision-recall AUC is the more honest curve when positives are rare.</li>"
   "<li><strong>SMOTE on high-dimensional or categorical data.</strong> Interpolating between neighbours assumes a meaningful metric space; on one-hot features it synthesises rows that could not exist.</li>"
   "<li><strong>Treating imbalance as always a problem.</strong> If the class ratio in training matches the real world and the metric reflects the actual costs, no correction may be needed.</li>"
   "</ul>"),
  ("The short version",
   "<p>Imbalance is a mismatch between the average loss you are minimising and the rare-class detection you actually want. Fix it by reweighting the loss (usually first), resampling the training data (inside the fold, never before the split), or simply moving the decision threshold. Then change the metric too &mdash; accuracy cannot show you whether any of it worked.</p>"),
 ]},

"machine_learning/k_means.html": {
 "intro": "Guess k centres, assign every point to its nearest one, move each centre to the mean of its points, repeat. It converges quickly, and it converges to whatever the initial guess led it toward.",
 "sections": [
  ("Two steps, repeated",
   "<p>K-means alternates between two operations until nothing changes:</p>"
   "<ol>"
   "<li><strong>Assign.</strong> Each point joins the cluster whose centroid is nearest, by Euclidean distance.</li>"
   "<li><strong>Update.</strong> Each centroid moves to the mean position of the points assigned to it.</li>"
   "</ol>"
   "<p>Each step can only reduce the total within-cluster sum of squares &mdash; reassigning a point to a nearer centroid reduces its contribution, and moving a centroid to the mean minimises the sum of squared distances by definition. Since the objective decreases monotonically and there are finitely many assignments, the algorithm always terminates.</p>"
   "<p>What it does <em>not</em> guarantee is arriving at the best solution. It converges to a local minimum, and which one depends entirely on where the centroids started.</p>"),
  ("Initialisation decides the answer",
   "<p>Place two initial centroids inside the same true cluster and k-means will happily split that cluster in half while merging two others. The result is stable, self-consistent and wrong.</p>"
   "<p><strong>k-means++</strong> is the standard fix and the default in most libraries. It chooses the first centroid at random, then chooses each subsequent one with probability proportional to its squared distance from the nearest existing centroid &mdash; so new centroids tend to land far from the ones already placed. This costs one extra pass and dramatically improves both the quality and the consistency of the result.</p>"
   "<p>The complementary defence is to run the whole algorithm several times from different seeds and keep the best (<span class=\"mono-font\">n_init</span> in scikit-learn).</p>"),
  ("Choosing k",
   "<p>K-means cannot tell you how many clusters there are; k is an input. Two standard ways to choose it:</p>"
   "<p>The <strong>elbow method</strong> plots within-cluster sum of squares against k. It always decreases &mdash; more centroids always fit better, and at k = n it reaches zero &mdash; so you look for the bend where the improvement flattens. It is subjective, and frequently there is no clear elbow.</p>"
   "<p>The <strong>silhouette score</strong> measures, for each point, how much closer it is to its own cluster than to the next nearest, on a scale from &minus;1 to 1. Averaged over all points it gives a single number per k, and picking the maximum is less arbitrary than eyeballing a bend.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>Watch the two steps alternate.</strong> Press <strong>Step Algorithm</strong> repeatedly. Assignments change, then centroids move, then assignments change again &mdash; and the movements shrink each round.</li>"
   "<li><strong>Get a different answer from the same data.</strong> Press <strong>Reset Positions</strong> and run again several times. Different starts sometimes give visibly different clusterings, which is the local-minimum problem directly.</li>"
   "<li><strong>Ask for the wrong k.</strong> Set <strong>Clusters (K)</strong> to 8 on data with three obvious groups. K-means splits real clusters to reach the number requested &mdash; it never declines to use a centroid.</li>"
   "<li><strong>Try a shape it cannot handle.</strong> Choose a non-spherical arrangement from <strong>Initial Layout</strong> and run. Because assignment is by distance to a centre, the clusters come out as convex blobs regardless of the true structure.</li>"
   "</ol>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Not scaling the features.</strong> K-means uses Euclidean distance, so a feature measured in thousands dominates one measured in decimals and effectively becomes the only feature. Standardise first &mdash; this is the most common mistake.</li>"
   "<li><strong>Expecting non-spherical clusters.</strong> The algorithm assumes roughly round, similarly sized groups. For elongated, nested or density-based shapes use DBSCAN or Gaussian mixtures.</li>"
   "<li><strong>Running it once.</strong> A single run from a single initialisation is a coin flip. Use k-means++ and multiple restarts.</li>"
   "<li><strong>Reading the elbow as objective.</strong> The curve always decreases; the bend is a judgement call. Cross-check with silhouette.</li>"
   "<li><strong>Ignoring outliers.</strong> Centroids are means, so a single extreme point drags its centroid noticeably. Consider k-medoids when outliers are present.</li>"
   "</ul>"),
  ("The short version",
   "<p>K-means alternates assigning points to the nearest centroid and moving each centroid to its points’ mean, which always converges but only to a local optimum determined by the initialisation &mdash; so use k-means++ and several restarts. It requires you to choose k, assumes roughly spherical clusters of similar size, and relies on Euclidean distance, which makes feature scaling mandatory rather than advisable.</p>"),
 ]},

"machine_learning/sliding_window_for_timeseries_data.html": {
 "intro": "Supervised learning needs (input, target) pairs and a time series is just one long sequence. A sliding window manufactures the pairs - and the way you split them afterwards is where most time-series projects go wrong.",
 "sections": [
  ("Turning a sequence into a supervised problem",
   "<p>A model needs examples with features and a label. A time series is a single ordered run of values, so you build examples by sliding a fixed-length window along it: the values inside the window are the input, and the value immediately after it is the target.</p>"
   "<p>With the series <span class=\"mono-font\">[10, 12, 15, 13, 18, 20, 19]</span> and a window of 3:</p>"
   "<p class=\"mono-font\">[10, 12, 15] &rarr; 13<br>[12, 15, 13] &rarr; 18<br>[15, 13, 18] &rarr; 20<br>[13, 18, 20] &rarr; 19</p>"
   "<p>Seven observations become four training examples. In general a series of length n with window W and stride S yields <span class=\"mono-font\">&lfloor;(n &minus; W) / S&rfloor; + 1</span> examples &mdash; so the window costs you W observations’ worth of data before you get anything at all.</p>"),
  ("Window size and stride",
   "<p><strong>Window size (W)</strong> is how much history the model sees per prediction, and it is a real modelling assumption: it asserts that nothing older than W steps matters. Too small and the model cannot see the pattern &mdash; a weekly cycle needs at least seven daily steps. Too large and each example carries mostly irrelevant history, the input dimension grows, and the number of examples shrinks.</p>"
   "<p><strong>Stride (S)</strong> is how far the window jumps between examples. A stride of 1 gives the maximum number of examples, heavily overlapping and therefore highly correlated. A larger stride gives fewer, more independent examples. Stride 1 is the usual choice for training; larger strides are used to cut redundancy on very long series.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Watch the window slide.</strong> Set <strong>Window Size (W)</strong> to 3 and <strong>Stride (S)</strong> to 1, then scroll along the series. Each position produces one training example, and consecutive examples share almost all their values.</li>"
   "<li><strong>Widen the window.</strong> Raise <strong>Window Size (W)</strong> to 10. Each example carries more history, and there are fewer of them &mdash; the trade is visible directly in the count.</li>"
   "<li><strong>Increase the stride.</strong> Set <strong>Stride (S)</strong> to 5. The windows stop overlapping heavily and the example count drops sharply, but each one is far more independent of the last.</li>"
   "<li><strong>Change the data.</strong> Press <strong>Random Series</strong> and try a window shorter than the visible cycle, then longer. A window that cannot span one period of the pattern cannot represent it.</li>"
   "</ol>"),
  ("Splitting without leaking",
   "<p>This is the part that matters most and is most often got wrong. Random train-test splitting is <em>invalid</em> for time series: it puts future windows in the training set and past windows in the test set, so the model is trained on the future to predict the past.</p>"
   "<p>Scores from that setup look excellent and mean nothing. Split <strong>chronologically</strong> &mdash; train on the earliest portion, validate on the middle, test on the most recent &mdash; so the evaluation mirrors how the model will actually be used.</p>"
   "<p>Overlapping windows add a second leak at the boundary: the last training window and the first test window share observations. Leave a gap of at least W steps between the splits.</p>"
   "<p>The same applies to scaling. Fit the scaler on the training period only; computing a mean over the whole series leaks future information into every training example.</p>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>Random shuffling before the split.</strong> Guarantees leakage and a score that will not survive deployment.</li>"
   "<li><strong>No gap between train and test.</strong> Overlapping windows straddle the boundary and share data.</li>"
   "<li><strong>Scaling on the full series.</strong> The training data learns statistics that include the test period.</li>"
   "<li><strong>Ignoring non-stationarity.</strong> If the mean or variance drifts over time, a model fitted on early data may not transfer. Difference the series or model the trend explicitly.</li>"
   "<li><strong>Predicting one step and reporting it as multi-step.</strong> Errors compound when a model’s own predictions are fed back as inputs; evaluate the horizon you actually need.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>A sliding window converts a time series into supervised (input, target) pairs, with the window size encoding how much history you claim is relevant and the stride controlling how much consecutive examples overlap. The modelling choice is straightforward; the discipline is in the split &mdash; chronological, with a gap of at least one window between segments, and every scaler fitted on the training period alone.</p>"),
 ]},

# ================================================= computer vision ===========
"computer_vision/downsampling_in_cnn.html": {
 "intro": "Pooling shrinks a feature map by summarising each small neighbourhood into one value. It cuts computation, widens what later layers can see, and buys a small amount of tolerance to things moving.",
 "sections": [
  ("What pooling does",
   "<p>A pooling layer slides a window over the feature map and replaces the values inside it with a single summary. With a 2&times;2 window and stride 2 &mdash; by far the most common setting &mdash; the windows do not overlap, and the output is half the height and half the width, so <strong>a quarter of the values</strong>.</p>"
   "<p><strong>Max pooling</strong> keeps the largest value in the window. Since a feature map records how strongly a filter responded at each position, the maximum says “this feature was detected somewhere in this neighbourhood”, which is usually the useful part.</p>"
   "<p><strong>Average pooling</strong> takes the mean, preserving overall intensity rather than peak response. It is smoother and less common in hidden layers, but <em>global</em> average pooling &mdash; averaging each channel down to a single number &mdash; is now standard at the end of a network, replacing the large fully connected layer that used to sit there.</p>"
   "<p>Pooling has <strong>no parameters</strong>. It is a fixed operation, so it adds nothing to the model size and nothing to train.</p>"),
  ("The three reasons it is there",
   "<p><strong>Computation.</strong> Quartering the spatial dimensions quarters the work of every subsequent layer. In a deep network that compounds enormously.</p>"
   "<p><strong>Receptive field.</strong> This is the one people miss. After pooling, each position in the smaller map summarises a larger region of the original image, so a 3&times;3 filter applied afterwards covers twice the input area it would have before. Stacking convolution and pooling is what lets a network built from small filters eventually see the whole image &mdash; without it, a network of 3&times;3 filters would need to be impractically deep.</p>"
   "<p><strong>Translation invariance.</strong> If a feature shifts by one pixel within a pooling window, the maximum is unchanged. This is a genuine but modest benefit &mdash; it tolerates small shifts, not large ones, and it is often overstated.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Halve the map.</strong> Draw a pattern, set <strong>Window Size</strong> to 2&times;2 and <strong>Stride</strong> to 2, then press <strong>Animate Pooling</strong>. The output is half the width and height, and the windows tile without overlapping.</li>"
   "<li><strong>Compare max with average.</strong> Switch <strong>Operation Type</strong> between them on the same drawing. Max keeps sharp peaks and discards everything else; average blurs, preserving overall intensity.</li>"
   "<li><strong>Test the invariance claim.</strong> Draw a small mark, pool it, then <strong>Clear</strong> and redraw it shifted by one cell within the same window. The max-pooled output is identical. Shift it into the next window and the output changes &mdash; the invariance is strictly local.</li>"
   "<li><strong>Overlap the windows.</strong> Set <strong>Stride</strong> to 1 with a 2&times;2 window. The output barely shrinks, because overlapping windows downsample far less.</li>"
   "</ol>"),
  ("Why some architectures drop it",
   "<p>Pooling is a fixed rule, and a strided convolution achieves the same downsampling while <em>learning</em> how to summarise. Many modern architectures use stride-2 convolutions instead, and all-convolutional networks remove pooling entirely.</p>"
   "<p>It is also destructive in a way that matters for some tasks. Max pooling discards the position of the maximum within the window, which is fine for classification and harmful for segmentation, where the output must be pixel-accurate. U-Net’s skip connections exist largely to restore the spatial detail pooling threw away.</p>"),
  ("What usually goes wrong",
   "<ul>"
   "<li><strong>Pooling too aggressively.</strong> Several 2&times;2 pools in quick succession reduce a 224&times;224 image to a handful of pixels, destroying the spatial information later layers need.</li>"
   "<li><strong>Expecting real translation invariance.</strong> It handles a shift of a pixel or two. Larger shifts need data augmentation.</li>"
   "<li><strong>Using max pooling for segmentation without skip connections.</strong> The precise locations are gone and cannot be recovered from the pooled map alone.</li>"
   "<li><strong>Forgetting it has no parameters.</strong> A pooling layer cannot learn or adapt; if you want a learned reduction, use a strided convolution.</li>"
   "<li><strong>Odd input sizes.</strong> A 2&times;2 pool on a 7&times;7 map leaves a remainder, and different frameworks handle the edge differently. Check whether yours floors or pads.</li>"
   "</ul>"),
  ("What to remember",
   "<p>Pooling summarises each neighbourhood into one value, most often taking the maximum of a 2&times;2 window at stride 2, which quarters the feature map for free &mdash; it has no parameters. Its real value is enlarging the receptive field so small filters can eventually see large structures, with computational saving second and a modest, purely local translation tolerance third. Strided convolutions do the same job with learned weights, which is why newer architectures often skip it.</p>"),
 ]},

"computer_vision/calculating_parameters_in_cnn.html": {
 "intro": "A convolutional layer's parameter count depends on the filter size, the input channels and the number of filters - and not at all on the size of the image. That independence is the whole reason CNNs are practical.",
 "sections": [
  ("The formula",
   "<p>For a convolutional layer with kernel size k&times;k, C<sub>in</sub> input channels and F filters:</p>"
   "<p class=\"mono-font\">parameters = (k &times; k &times; C<sub>in</sub> &times; F) + F</p>"
   "<p>Each filter is a small 3-D volume of size k&times;k&times;C<sub>in</sub>, and there are F of them. The trailing <span class=\"mono-font\">+ F</span> is one bias per filter.</p>"
   "<p>The part worth pausing on is what is <em>absent</em>: the height and width of the input never appear. A layer applied to a 32&times;32 image and the same layer applied to a 4096&times;4096 image have exactly the same number of parameters.</p>"),
  ("Filters are three-dimensional",
   "<p>A “3&times;3 filter” on an RGB input is not 9 weights, it is 3&times;3&times;3 = 27. A filter always spans <em>every</em> input channel, because it looks for a pattern across all of them at once &mdash; an edge detector on colour images must consider red, green and blue together.</p>"
   "<p>Work one through. First conv layer, 3&times;3 kernel, RGB input, 64 filters:</p>"
   "<p class=\"mono-font\">(3 &times; 3 &times; 3 &times; 64) + 64 = 1728 + 64 = <strong>1792</strong></p>"
   "<p>Second layer, 3&times;3 kernel, taking those 64 channels, producing 128:</p>"
   "<p class=\"mono-font\">(3 &times; 3 &times; 64 &times; 128) + 128 = 73728 + 128 = <strong>73,856</strong></p>"
   "<p>Forty times more, from the same kernel size &mdash; because C<sub>in</sub> and F both grew. The product of those two dominates, which is why deep layers with many channels hold most of a CNN’s weights.</p>"),
  ("Weight sharing, and the comparison that makes the point",
   "<p>A fully connected layer on a 224&times;224&times;3 image with 64 outputs would need 224 &times; 224 &times; 3 &times; 64 &asymp; <strong>9.6 million</strong> parameters. The convolutional layer above does a comparable job with <strong>1,792</strong>.</p>"
   "<p>The saving comes from <strong>weight sharing</strong>: the same filter slides across every position rather than each position having its own weights. That encodes a real assumption &mdash; a vertical edge is a vertical edge wherever it appears &mdash; and it buys two things at once. Far fewer parameters, and translation equivariance, since a feature is detected the same way regardless of where it sits.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Grow the kernel.</strong> Raise <strong>3x3</strong> from 3 to 7 and watch the count. It grows with the <em>square</em> of the kernel size, so 7&times;7 costs more than five times a 3&times;3 &mdash; which is why modern networks stack small kernels instead.</li>"
   "<li><strong>Grow the channels.</strong> Raise <strong>Input Channels</strong> and then <strong>Number of Filters</strong>. Each scales the count linearly, and together they scale it multiplicatively.</li>"
   "<li><strong>Toggle the bias.</strong> Switch the bias checkbox and note the change is exactly F &mdash; a rounding error next to the weights, which is why layers followed by batch normalisation usually drop it entirely.</li>"
   "<li><strong>Confirm the image size is irrelevant.</strong> Nothing in the calculation refers to input height or width. That is the property that makes a CNN usable on large images at all.</li>"
   "</ol>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Forgetting the depth dimension.</strong> Counting a 3&times;3 filter as 9 weights instead of 9 &times; C<sub>in</sub> is the most common error, and it understates the layer by a large factor.</li>"
   "<li><strong>Confusing parameters with activations.</strong> Parameters are fixed and independent of image size; activation memory scales with height &times; width &times; channels &times; batch. Out-of-memory errors during training are almost always activations, not weights.</li>"
   "<li><strong>Using large kernels.</strong> Two stacked 3&times;3 layers cover the same receptive field as one 5&times;5 with fewer parameters and an extra non-linearity. VGG made this the standard.</li>"
   "<li><strong>Keeping the bias before batch norm.</strong> The normalisation subtracts the mean and cancels it exactly, so those parameters do nothing.</li>"
   "</ul>"),
  ("In one line",
   "<p>A convolutional layer holds (k &times; k &times; C<sub>in</sub> &times; F) + F parameters, with filters spanning every input channel and the image dimensions appearing nowhere. Weight sharing is what buys the enormous reduction against a fully connected layer, along with translation equivariance. Cost grows with the square of the kernel and the product of input and output channels &mdash; which is why small kernels and staged channel growth are the standard design.</p>"),
 ]},

# ======================================================== gen_ai =============
"gen_ai/retrieval_evaluation_metrics.html": {
 "intro": "Retrieval returns a ranked list, so the metric has to care about order. Precision@k, recall@k, MRR and NDCG each answer a different question about that list.",
 "sections": [
  ("Why classification metrics are not enough",
   "<p>A retriever does not return a yes or no; it returns an ordered list of candidates. Two systems can retrieve exactly the same documents and be very different in quality if one puts the relevant ones first and the other buries them at position 10.</p>"
   "<p>So retrieval metrics are evaluated <strong>at a cutoff k</strong> &mdash; the number of results a user or a downstream model will actually see &mdash; and the better ones are sensitive to position within that cutoff.</p>"),
  ("Precision@k and Recall@k",
   "<p class=\"mono-font\">precision@k = (relevant in top k) / k</p>"
   "<p class=\"mono-font\">recall@k&nbsp;&nbsp;&nbsp; = (relevant in top k) / (total relevant)</p>"
   "<p>Precision@k asks how much of what you returned was useful. Recall@k asks how much of what exists you managed to find.</p>"
   "<p>With 3 relevant documents in the collection and a top-5 list containing 2 of them: precision@5 = 2/5 = 0.4, recall@5 = 2/3 = 0.67.</p>"
   "<p>Both ignore order entirely &mdash; a relevant document at position 1 and at position 5 count identically. For a RAG pipeline feeding a fixed number of chunks to a model that may be the right simplification; for a search results page it is not.</p>"),
  ("MRR and NDCG",
   "<p><strong>MRR</strong> (mean reciprocal rank) uses only the position of the <em>first</em> relevant result, averaged over queries:</p>"
   "<p class=\"mono-font\">MRR = mean(1 / rank of first relevant)</p>"
   "<p>First position scores 1.0, second 0.5, third 0.33. It is the right metric when the user needs one good answer and will stop reading once they have it &mdash; question answering, navigational search &mdash; and it deliberately ignores everything after the first hit.</p>"
   "<p><strong>NDCG</strong> (normalised discounted cumulative gain) is the most complete of the four. It handles <em>graded</em> relevance rather than a binary label, applies a logarithmic discount so later positions contribute less, and normalises by the score of the ideal ranking so the result lands in [0, 1] and is comparable across queries.</p>"
   "<p>Use NDCG when relevance comes in degrees and the whole ordering matters; use MRR when only the first hit does.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Move the cutoff.</strong> Slide <strong>k</strong> from 1 to 10 and watch precision@k and recall@k move in opposite directions. A larger k almost always raises recall and lowers precision.</li>"
   "<li><strong>Change the ranking.</strong> Switch <strong>Ranking</strong> so the relevant documents sit lower. Precision@k and recall@k at a large k barely move, while MRR and NDCG drop sharply &mdash; that difference is exactly what order-aware metrics measure.</li>"
   "<li><strong>Put one relevant result first.</strong> Choose a ranking with a relevant document at position 1. MRR jumps to 1.0 regardless of what follows, which shows how much it ignores.</li>"
   "<li><strong>Set k = 1.</strong> Precision@1 and recall@1 become extremely blunt. At small k the choice of metric matters far more than at large k.</li>"
   "</ol>"),
  ("Choosing one for a RAG pipeline",
   "<p>For retrieval feeding a language model, <strong>recall@k</strong> is usually the metric that matters most. The model can ignore an irrelevant chunk among the k it receives, but it cannot use a relevant chunk that was never retrieved &mdash; a missed document is unrecoverable, whereas a spurious one is merely noise.</p>"
   "<p>Set k to the number of chunks you actually pass to the model and measure recall at that value. Then use precision or NDCG as a secondary check, since packing the context with irrelevant material does cost tokens and can distract the model.</p>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Reporting a metric without its k.</strong> “Precision 0.4” is meaningless; precision@5 is a number.</li>"
   "<li><strong>Using accuracy.</strong> It has no meaning over a ranked list of a large corpus, where almost everything is irrelevant.</li>"
   "<li><strong>Ignoring order when order matters.</strong> Precision@k cannot distinguish a system that ranks well from one that merely retrieves the same set in a worse order.</li>"
   "<li><strong>Assuming complete relevance labels.</strong> Most evaluation sets label only judged documents, so an unjudged-but-relevant result counts against you and recall is systematically understated.</li>"
   "<li><strong>Averaging over too few queries.</strong> These metrics are noisy per query; differences need many queries to be meaningful.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Retrieval returns a ranking, so metrics are computed at a cutoff k and differ mainly in whether they care about position. Precision@k and recall@k ignore order within the cutoff; MRR looks only at the first relevant result; NDCG discounts by position and handles graded relevance. For RAG, recall@k at your actual context size is the number to optimise, because the model can survive a bad chunk but not a missing one.</p>"),
 ]},

"gen_ai/multi_query_retriever.html": {
 "intro": "One question can be asked many ways, and vector search only finds what is phrased like the query it was given. A multi-query retriever generates several rewordings, searches with each, and merges the results.",
 "sections": [
  ("The vocabulary mismatch problem",
   "<p>Embedding-based retrieval finds documents whose vectors are near the query’s vector. That works well when the question and the document use similar language, and fails when they do not.</p>"
   "<p>Ask “how do I speed up my model?” of a corpus that discusses “reducing inference latency”, “quantisation” and “batch throughput” and the embedding may simply not land near any of them. The information is present and the phrasing is wrong, and a single query gets a single shot at matching it.</p>"
   "<p>The failure is silent. The retriever returns its nearest neighbours regardless, so you get plausible-looking, unhelpful chunks with no signal that anything was missed.</p>"),
  ("Generating several queries and merging",
   "<p>A multi-query retriever asks a language model to produce N alternative phrasings of the question &mdash; typically 3 to 5 &mdash; each approaching it from a different angle. The original question above might become:</p>"
   "<ul>"
   "<li>“What techniques reduce model inference latency?”</li>"
   "<li>“How can I improve throughput at serving time?”</li>"
   "<li>“What makes a neural network run faster in production?”</li>"
   "</ul>"
   "<p>Each is embedded and searched independently, giving N result sets which are then combined and deduplicated. Because the rewordings cover different vocabulary, their nearest neighbours differ, and the union covers substantially more of the relevant material than any one query would.</p>"
   "<p>Merging is usually done with <strong>reciprocal rank fusion</strong> rather than raw scores. RRF assigns each document a score of <span class=\"mono-font\">&Sigma; 1/(60 + rank)</span> across the lists it appears in, which rewards documents that several rewordings agree on and avoids the problem that similarity scores from different queries are not directly comparable.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>Compare a single query with the set.</strong> Look at what one phrasing retrieves against the union of all of them. The union is broader, and usually includes at least one document no single query found.</li>"
   "<li><strong>Find the documents only one variant retrieves.</strong> These are exactly the recall the technique is buying &mdash; material the original phrasing would have missed entirely.</li>"
   "<li><strong>Look for agreement.</strong> Documents retrieved by several variants are the strongest candidates, and that consensus is what rank fusion promotes to the top.</li>"
   "<li><strong>Watch the precision cost.</strong> The merged list is longer and contains more marginal results. Multi-query improves recall and dilutes precision, which is why a reranker usually follows it.</li>"
   "</ol>"),
  ("What it costs, and what to use instead",
   "<p>Multi-query is not free. Generating the variants is an extra LLM call on the critical path, adding latency and cost to every request, and it runs N searches instead of one. For an interactive application that overhead is real.</p>"
   "<p>Related approaches make different trades. <strong>HyDE</strong> generates a hypothetical <em>answer</em> and embeds that, on the argument that an answer is textually closer to the passage containing it than a question is. <strong>Query decomposition</strong> splits a multi-part question into separate sub-questions, which multi-query does not do &mdash; it rephrases rather than divides. And <strong>hybrid search</strong>, combining dense retrieval with BM25 keyword matching, addresses much of the same vocabulary problem for a fraction of the cost, because exact term matching catches precisely the rare words embeddings handle worst.</p>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Generating variants that all say the same thing.</strong> If the rewordings are near-identical, they retrieve the same documents and you have paid for nothing. The prompt must push for genuinely different angles and vocabulary.</li>"
   "<li><strong>Merging by raw similarity score.</strong> Scores from different query embeddings are not comparable. Use rank-based fusion.</li>"
   "<li><strong>Skipping deduplication.</strong> The same chunk retrieved by four variants will otherwise occupy four slots of context.</li>"
   "<li><strong>Not reranking afterwards.</strong> The merged list is broader and noisier; a cross-encoder reranker recovers the precision.</li>"
   "<li><strong>Using it where the problem is chunking.</strong> If the relevant text is split badly across chunks, no amount of query rewriting will retrieve it intact.</li>"
   "</ul>"),
  ("What to remember",
   "<p>A multi-query retriever compensates for the fact that a single embedding gets one attempt at matching the corpus vocabulary: it generates several rewordings, retrieves with each, and fuses the ranked lists. It buys recall at the cost of an extra LLM call, N searches, and some precision &mdash; so it pairs naturally with a reranker. Where the mismatch is about rare or exact terms, hybrid search with BM25 gets much of the same benefit far more cheaply.</p>"),
 ]},

# ====================================================== database =============
"database/query_execution_order.html": {
 "intro": "SQL is written SELECT first and executed SELECT almost last. Nearly every confusing SQL error - unknown alias, aggregate in WHERE - is explained by that gap.",
 "sections": [
  ("Written order versus execution order",
   "<p>A query is written in this order:</p>"
   "<p class=\"mono-font\">SELECT &rarr; FROM &rarr; WHERE &rarr; GROUP BY &rarr; HAVING &rarr; ORDER BY &rarr; LIMIT</p>"
   "<p>It is executed in this one:</p>"
   "<p class=\"mono-font\">FROM &rarr; JOIN &rarr; WHERE &rarr; GROUP BY &rarr; HAVING &rarr; SELECT &rarr; DISTINCT &rarr; ORDER BY &rarr; LIMIT</p>"
   "<p>The database first works out which rows it is dealing with (FROM and JOIN), filters them (WHERE), groups what survives (GROUP BY), filters the groups (HAVING), and only then computes the output columns (SELECT). Sorting and limiting happen last, on the finished result.</p>"),
  ("The two errors this explains",
   "<p><strong>An alias defined in SELECT cannot be used in WHERE.</strong></p>"
   "<p class=\"mono-font\">SELECT price * qty AS total<br>FROM orders<br>WHERE total &gt; 100&nbsp;&nbsp;&nbsp;&nbsp;&minus;&minus; error</p>"
   "<p>WHERE runs before SELECT, so at that moment <span class=\"mono-font\">total</span> does not exist yet. Repeat the expression instead: <span class=\"mono-font\">WHERE price * qty &gt; 100</span>.</p>"
   "<p>ORDER BY, however, runs <em>after</em> SELECT &mdash; so <span class=\"mono-font\">ORDER BY total</span> works perfectly well. That is why the same alias is legal in one clause and not the other, which looks arbitrary until you know the order.</p>"
   "<p><strong>An aggregate cannot appear in WHERE.</strong></p>"
   "<p class=\"mono-font\">WHERE COUNT(*) &gt; 5&nbsp;&nbsp;&nbsp;&minus;&minus; error<br>HAVING COUNT(*) &gt; 5&nbsp;&nbsp;&minus;&minus; correct</p>"
   "<p>WHERE runs before GROUP BY, when no groups exist and there is nothing to count. HAVING runs after, which is precisely what it is for.</p>"),
  ("WHERE and HAVING are not interchangeable",
   "<p>Both filter, at different stages, and the distinction matters for correctness as well as speed:</p>"
   "<ul>"
   "<li><strong>WHERE</strong> filters individual <em>rows</em>, before grouping. Excluded rows never reach the aggregate.</li>"
   "<li><strong>HAVING</strong> filters <em>groups</em>, after aggregation. All rows contribute to the aggregate; whole groups are then discarded.</li>"
   "</ul>"
   "<p><span class=\"mono-font\">WHERE status = 'paid'</span> computes totals from paid orders only. <span class=\"mono-font\">HAVING SUM(amount) &gt; 1000</span> computes totals from every order and keeps the customers whose total exceeds 1000. Moving a condition between them changes the answer.</p>"
   "<p>When a condition <em>could</em> go in either &mdash; a plain column filter &mdash; put it in WHERE. Filtering earlier means fewer rows to group, which is almost always faster.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Step through a query.</strong> Press <strong>Step</strong> repeatedly and watch which clause runs at each stage. FROM produces the rows, WHERE removes some, GROUP BY collapses the rest, and SELECT is near the end.</li>"
   "<li><strong>Break it deliberately.</strong> Enable the option that uses a SELECT alias in WHERE. It fails, because at that point the alias has not been created.</li>"
   "<li><strong>Then use the same alias in ORDER BY.</strong> Enable that option instead. It works &mdash; same alias, different clause, and the execution order is the only reason.</li>"
   "<li><strong>Reset and compare.</strong> Press <strong>Reset</strong> and run a working query, watching how many rows survive each stage. Filtering early leaves far less work for everything downstream.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<ul>"
   "<li><strong>Using a SELECT alias in WHERE or GROUP BY.</strong> Repeat the expression, or wrap the query in a subquery or CTE where the alias already exists.</li>"
   "<li><strong>Putting an aggregate in WHERE.</strong> Use HAVING.</li>"
   "<li><strong>Using HAVING for row filters.</strong> Correct results, more work &mdash; the rows are grouped before being discarded.</li>"
   "<li><strong>Expecting LIMIT to speed up an aggregate.</strong> LIMIT runs last, so the database has already grouped and sorted everything before it truncates.</li>"
   "<li><strong>Filtering an outer join in WHERE.</strong> A condition on the right-hand table in WHERE discards the NULL rows and silently turns the LEFT JOIN into an INNER JOIN. Put it in the ON clause instead.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>SQL executes FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT &mdash; not the order it is written in. That single fact explains why SELECT aliases work in ORDER BY but not WHERE, why aggregates belong in HAVING rather than WHERE, and why filtering early is faster. When a query does something surprising, walking it through the execution order usually answers it in one step.</p>"),
 ]},

"database/union_intersect_except_in_sql.html": {
 "intro": "Set operators combine whole result sets vertically, stacking rows rather than widening them. That is the difference from a JOIN, and it is the point people miss most often.",
 "sections": [
  ("Stacking, not joining",
   "<p>A JOIN combines tables <strong>horizontally</strong>: matching rows are linked and the result has the columns of both. A set operator combines result sets <strong>vertically</strong>: rows from the second query are stacked under rows from the first, and the column count does not change.</p>"
   "<p>So the question a set operator answers is “which rows appear in these two result sets?”, not “what belongs together?”. If you want columns from two tables, you need a JOIN; if you want the rows from two similar queries treated as one collection, you need these.</p>"),
  ("The three operators",
   "<p>Take two result sets, A = {1, 2, 3} and B = {2, 3, 4}:</p>"
   "<p class=\"mono-font\">A UNION B&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; 1, 2, 3, 4&nbsp;&nbsp;&nbsp;in either, duplicates removed<br>"
   "A UNION ALL B&nbsp;&rarr; 1,2,3,2,3,4&nbsp;&nbsp;everything, duplicates kept<br>"
   "A INTERSECT B &rarr; 2, 3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;in both<br>"
   "A EXCEPT B&nbsp;&nbsp;&nbsp;&nbsp;&rarr; 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;in A but not B</p>"
   "<p>Two things are worth noting. <strong>EXCEPT is not symmetric</strong> &mdash; <span class=\"mono-font\">B EXCEPT A</span> gives 4, a different answer. And UNION, INTERSECT and EXCEPT all remove duplicates by default, which is a genuine cost: the database must sort or hash the entire result to find them.</p>"
   "<p>Some databases spell EXCEPT as MINUS (Oracle), and the semantics are the same.</p>"),
  ("The rules every set operator enforces",
   "<ul>"
   "<li><strong>Same number of columns</strong> in both queries.</li>"
   "<li><strong>Compatible types</strong>, position by position &mdash; the first column of one must be comparable with the first column of the other.</li>"
   "<li><strong>Column names come from the first query.</strong> The second query’s aliases are ignored entirely.</li>"
   "<li><strong>ORDER BY applies to the whole result</strong> and may appear only once, at the very end. It cannot be attached to an individual branch.</li>"
   "</ul>"
   "<p>Note that matching is <em>positional</em>, not by name. If the first query selects (id, name) and the second selects (name, id), and both are text-compatible, the query runs and silently returns nonsense.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Compare UNION with UNION ALL.</strong> Switch <strong>Operator</strong> between them and count the rows. The difference is exactly the duplicates &mdash; and UNION paid to find them.</li>"
   "<li><strong>Look at INTERSECT.</strong> Only rows present in both sides survive. This is the set equivalent of an inner join on every column at once.</li>"
   "<li><strong>Reverse EXCEPT.</strong> Note which rows survive, then imagine swapping the two queries. The answer changes completely &mdash; order matters here and nowhere else among the three.</li>"
   "<li><strong>Watch the duplicate handling.</strong> With duplicates present in the source, see which operators collapse them and which do not.</li>"
   "</ol>"),
  ("UNION ALL is usually the one you want",
   "<p>UNION performs a deduplication pass over the combined result, which means a sort or a hash of every row. When you know the two sets cannot overlap &mdash; last month’s orders and this month’s orders, or partitioned tables split by region &mdash; that work finds nothing and you have paid for it anyway.</p>"
   "<p>UNION ALL simply concatenates and is frequently several times faster on large result sets. Use UNION only when duplicates are genuinely possible <em>and</em> you want them removed; reach for UNION ALL by default and add the deduplication deliberately.</p>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Using UNION out of habit.</strong> The unnecessary deduplication is one of the more common avoidable costs in reporting queries.</li>"
   "<li><strong>Mismatched column order.</strong> Positional matching means compatible-but-wrong orderings run happily and return garbage.</li>"
   "<li><strong>Expecting EXCEPT to be symmetric.</strong> Swapping the operands gives a different result.</li>"
   "<li><strong>Putting ORDER BY on a branch.</strong> It belongs once, at the end, and applies to the whole combined set.</li>"
   "<li><strong>Reaching for a set operator when a JOIN is needed.</strong> If you want columns from both tables, no set operator will do it &mdash; they only ever stack rows.</li>"
   "</ul>"),
  ("What to remember",
   "<p>UNION, INTERSECT and EXCEPT combine result sets vertically, requiring the same column count and compatible types matched by position rather than name. All three deduplicate by default, which costs a full sort or hash &mdash; so prefer UNION ALL unless you specifically need duplicates removed. EXCEPT is the only one where operand order changes the answer, and none of them is a substitute for a JOIN.</p>"),
 ]},

}
