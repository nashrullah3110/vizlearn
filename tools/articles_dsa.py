# -*- coding: utf-8 -*-
"""Written explanations for the algorithms track.

These pages shipped with a short skeleton article - typically 200-300 words
sharing the same headings ("Quick Context", "The Core Idea", "Key Takeaways")
as sixty other pages, with only a couple of sentences under each. The
visualisation carried the page and the prose carried nothing.

Everything here is written for its own page: the actual control names on that
page, complexity derived rather than asserted, and the failure modes that
apply to that algorithm specifically.

Rendered by tools/build_articles.py. Edit here, then `npm run build`.
"""

ARTICLES_DSA = {

# ---------------------------------------------------------------------------
"dsa/linear_search.html": {
 "intro": "Check every element in turn until you find the target or run out of array. It is the only search that works on unsorted data, and that is exactly when you want it.",
 "sections": [
  ("What linear search actually does",
   "<p>Start at index 0. Compare the element there against the target. If it matches, return the index and stop. If it does not, move to index 1 and repeat. If you reach the end without a match, the target is not present.</p>"
   "<p>That is the entire algorithm, and its simplicity is the point: it makes no assumption whatsoever about the data. The array can be sorted, reverse-sorted, or shuffled; it can hold duplicates; it can be a linked list with no random access at all. Linear search does not care, because it never jumps &mdash; it only ever steps forward by one.</p>"),
  ("Counting the comparisons",
   "<p>Take the array <span class=\"mono-font\">[42, 17, 8, 91, 5, 63, 29]</span> and search for <span class=\"mono-font\">91</span>. The algorithm compares 42, then 17, then 8, then 91 &mdash; four comparisons, and it returns index 3.</p>"
   "<p>Now search for <span class=\"mono-font\">29</span>. That sits last, so it takes seven comparisons. Search for <span class=\"mono-font\">100</span>, which is absent, and it also takes seven &mdash; the algorithm cannot know the target is missing until it has ruled out every element.</p>"
   "<p>So the cost splits three ways. Best case is 1 comparison, when the target is first. Worst case is n, when the target is last or absent. The average over all successful searches is:</p>"
   "<p class=\"mono-font\">(1 + 2 + 3 + &hellip; + n) / n = (n + 1) / 2</p>"
   "<p>Roughly half the array. All three cases are O(n) except the best, and it is the worst case that gets quoted, so linear search is an O(n) algorithm with O(1) extra space.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>Watch the worst case.</strong> Set <strong>Array Size</strong> to 25, then set <strong>Search Target</strong> to a value that is not in the array and press <strong>Auto-Run</strong>. Every single cell lights up before the algorithm gives up. That full sweep is what O(n) means.</li>"
   "<li><strong>Watch the best case.</strong> Press <strong>Randomize Array</strong>, read off whatever value landed in the first cell, and set <strong>Search Target</strong> to it. Now the search ends after one comparison, no matter how large the array is.</li>"
   "<li><strong>Prove size drives cost.</strong> Set <strong>Array Size</strong> to 5 and step through a failed search with <strong>Next Step</strong>, counting the comparisons. Now set <strong>Array Size</strong> to 25 and do it again. The count scales with the array, one for one &mdash; there is no shortcut being taken anywhere.</li>"
   "<li><strong>Look for the pattern that is not there.</strong> Press <strong>Randomize Array</strong> several times and watch where the target turns up. Unlike every other search on this track, the position of the value in a <em>sorted</em> sense tells you nothing. Linear search has no notion of “too high” or “too low”.</li>"
   "</ol>"),
  ("When linear search is the right answer",
   "<p>It gets dismissed as the naive option, which is unfair. Reach for it when:</p>"
   "<ul>"
   "<li><strong>The data is unsorted and you will search once.</strong> Sorting costs O(n log n). If you only need one lookup, paying that to enable an O(log n) search is strictly worse than one O(n) scan.</li>"
   "<li><strong>n is small.</strong> Below roughly 30 elements the constant factors dominate and a tight linear scan often beats binary search in real time, because it is branch-predictable and walks memory in order.</li>"
   "<li><strong>The structure has no random access.</strong> On a singly linked list you cannot jump to the middle, so binary search is not available at any price.</li>"
   "<li><strong>The match is not on equality.</strong> Finding the first element satisfying an arbitrary predicate needs a scan; there is nothing to bisect on.</li>"
   "</ul>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Returning a boolean instead of an index.</strong> Callers almost always want to know <em>where</em>, and recovering the position afterwards costs a second scan. Return the index and use &minus;1 (or null) for absent.</li>"
   "<li><strong>Sorting in order to search once.</strong> A single O(n log n) sort to enable one O(log n) lookup is a net loss. Sorting pays off only when it is amortised over many searches.</li>"
   "<li><strong>Nesting it without noticing.</strong> A linear search inside a loop over the same array is O(n&sup2;). This is the most common accidental quadratic in real code &mdash; a hash set turns the inner search into O(1) and the whole thing into O(n).</li>"
   "<li><strong>Forgetting duplicates.</strong> The basic version returns the first match. If you need all of them, keep scanning after the first hit rather than stopping.</li>"
   "</ul>"),
  ("In one line",
   "<p>Linear search trades speed for having no requirements at all. It is O(n) because it may have to look at everything, and it cannot do better because it has no information to exploit &mdash; but for unsorted data, a single lookup, or a small array, that is not a weakness. Every faster search on this track buys its speed with a precondition, and linear search is what you use when you cannot pay it.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/binary_search.html": {
 "intro": "Halve the search space on every comparison. Twenty steps are enough to find one item among a million - provided the array is sorted.",
 "sections": [
  ("The one assumption that makes it work",
   "<p>Binary search requires sorted data, and everything it does follows from that. Look at the middle element. If it equals the target, you are done. If it is <em>smaller</em> than the target, then the target cannot be anywhere in the left half either &mdash; because everything on the left is smaller still. So discard the entire left half in one comparison, and repeat on the right.</p>"
   "<p>Each comparison eliminates half of what remains. That is the whole idea, and it is why the precondition is non-negotiable: on unsorted data, “smaller than the middle” tells you nothing about which side the target is on.</p>"),
  ("Work one through by hand",
   "<p>Search for <span class=\"mono-font\">23</span> in <span class=\"mono-font\">[2, 5, 8, 12, 16, 23, 38, 56, 72, 91]</span>, ten elements, indices 0&ndash;9.</p>"
   "<p class=\"mono-font\">lo=0, hi=9 &rarr; mid=4 &rarr; a[4]=16 &lt; 23 &rarr; go right, lo=5</p>"
   "<p class=\"mono-font\">lo=5, hi=9 &rarr; mid=7 &rarr; a[7]=56 &gt; 23 &rarr; go left, hi=6</p>"
   "<p class=\"mono-font\">lo=5, hi=6 &rarr; mid=5 &rarr; a[5]=23 &rarr; found, index 5</p>"
   "<p>Three comparisons against a linear search’s six. The gap is unremarkable at ten elements and decisive at a million: linear search averages 500,000 comparisons, binary search takes at most 20.</p>"),
  ("Where log n comes from",
   "<p>The search space starts at n and halves every step: n, n/2, n/4, n/8, and so on. The search ends when one element is left, so the question is how many halvings that takes:</p>"
   "<p class=\"mono-font\">n / 2<sup>k</sup> = 1 &nbsp;&rarr;&nbsp; 2<sup>k</sup> = n &nbsp;&rarr;&nbsp; k = log<sub>2</sub>(n)</p>"
   "<p>That is the definition of a logarithm, not an analogy for it. Doubling the array adds exactly one comparison. Going from 1,000 to 1,000,000 elements &mdash; a thousandfold increase &mdash; adds ten.</p>"),
  ("Experiments to try",
   "<ol>"
   "<li><strong>Count the halvings.</strong> Set <strong>Array Size</strong> to 25 and press <strong>Next Step</strong> repeatedly, watching the shaded region shrink. It takes about five steps, because 2<sup>5</sup> = 32 is the first power of two above 25.</li>"
   "<li><strong>Double the array, add one step.</strong> Run a search at <strong>Array Size</strong> 12 and count the steps. Now set it to 24 and count again. One extra step, not twice as many &mdash; that is the logarithm, visible directly.</li>"
   "<li><strong>Search for something absent.</strong> Set <strong>Search Target</strong> to a value not in the array. The window still collapses in log n steps; a failed binary search costs the same as a successful one, unlike linear search where failure is always the worst case.</li>"
   "<li><strong>Find the expensive targets.</strong> Press <strong>Reset Array</strong> and try searching for the very first and very last elements. Both take the full log n steps, while the middle element is found immediately &mdash; the exact inverse of linear search’s cost profile.</li>"
   "</ol>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>Integer overflow in the midpoint.</strong> Writing <span class=\"mono-font\">mid = (lo + hi) / 2</span> overflows when lo and hi are large. Use <span class=\"mono-font\">mid = lo + (hi &minus; lo) / 2</span>. This bug sat in the JDK’s binary search for nine years.</li>"
   "<li><strong>Off-by-one in the bounds.</strong> The two conventions &mdash; inclusive <span class=\"mono-font\">hi = n &minus; 1</span> with <span class=\"mono-font\">while (lo &lt;= hi)</span>, or exclusive <span class=\"mono-font\">hi = n</span> with <span class=\"mono-font\">while (lo &lt; hi)</span> &mdash; are both correct, and mixing them gives an infinite loop or a missed last element. Pick one and keep it.</li>"
   "<li><strong>Assuming the array is sorted.</strong> Binary search on unsorted data does not error; it silently returns wrong answers, which is far worse. If sortedness is an assumption rather than an invariant, it will eventually be violated.</li>"
   "<li><strong>Wanting the first duplicate.</strong> Plain binary search returns <em>some</em> match, not the leftmost. Finding the first occurrence needs the variant that keeps searching left after a hit instead of returning.</li>"
   "</ul>"),
  ("The short version",
   "<p>Binary search converts a sorted array into an O(log n) lookup by throwing away half the remaining candidates with every comparison. The cost is the precondition: something must keep the data sorted, and if that guarantee ever lapses the algorithm fails silently rather than loudly. Sort once and search many times and it is close to unbeatable; sort in order to search once and you have spent O(n log n) to save O(n).</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/fibonacci_search.html": {
 "intro": "Binary search without division. It splits the array at Fibonacci boundaries using only addition and subtraction, which mattered enormously on hardware that could not divide.",
 "sections": [
  ("Why anyone would avoid the midpoint",
   "<p>Binary search computes <span class=\"mono-font\">mid = (lo + hi) / 2</span>. That division &mdash; or at least a bit shift &mdash; was genuinely expensive on early hardware, and on some architectures it still is. Fibonacci search finds a comparable split point using nothing but addition and subtraction of precomputed Fibonacci numbers.</p>"
   "<p>The trick rests on a property of the sequence. Since <span class=\"mono-font\">F(k) = F(k&minus;1) + F(k&minus;2)</span>, any Fibonacci number splits naturally into two smaller Fibonacci numbers. Use that split as the probe point and both resulting subarrays are themselves Fibonacci-sized, so the same trick applies recursively without ever computing a new boundary from scratch.</p>"),
  ("The mechanism, step by step",
   "<p>First find the smallest Fibonacci number that is at least the array length. For an array of 10 elements the sequence runs 1, 1, 2, 3, 5, 8, 13 &mdash; so <span class=\"mono-font\">F(7) = 13</span>, with <span class=\"mono-font\">F(6) = 8</span> and <span class=\"mono-font\">F(5) = 5</span>.</p>"
   "<p>Probe at <span class=\"mono-font\">offset + F(k&minus;2)</span>, clamped to the array bounds. Compare:</p>"
   "<ul>"
   "<li>Target is <strong>larger</strong> &rarr; discard the left part; shift the Fibonacci numbers down two and move the offset up to the probe.</li>"
   "<li>Target is <strong>smaller</strong> &rarr; discard the right part; shift the Fibonacci numbers down one.</li>"
   "<li>Equal &rarr; found.</li>"
   "</ul>"
   "<p>Every update is an index addition or a step down the precomputed sequence. No division, no multiplication.</p>"),
  ("The complexity, and the honest comparison",
   "<p>Because consecutive Fibonacci numbers approach the golden ratio &phi; &asymp; 1.618, each step shrinks the search space by a factor of about 1.618 rather than binary search’s 2. So Fibonacci search is O(log n) too, but with a slightly larger constant:</p>"
   "<p class=\"mono-font\">log<sub>1.618</sub>(n) &asymp; 1.44 &times; log<sub>2</sub>(n)</p>"
   "<p>Roughly 44% more comparisons. In exchange, the probe positions are computed with additions only, and &mdash; the reason it survives in practice &mdash; the two subarrays it examines are unequal in size, with the smaller one probed first. On data read from tape or disk in blocks, that uneven split touches fewer distant locations than binary search’s repeated jumps to the exact middle.</p>"),
  ("Experiments to try",
   "<ol>"
   "<li><strong>Watch the uneven split.</strong> Set <strong>Array Size</strong> to 30 and press <strong>Next Step</strong> through a search. Notice the probe does not land in the middle &mdash; it sits about 38% of the way in, which is 1/&phi;&sup2;. Binary search would split at exactly 50% every time.</li>"
   "<li><strong>Count against binary search.</strong> Run a full search at <strong>Array Size</strong> 30 with <strong>Auto-Run</strong> and count the probes. Compare with the binary search module at the same size: Fibonacci search usually needs one or two more.</li>"
   "<li><strong>Find the boundary Fibonacci number.</strong> Set <strong>Array Size</strong> to 13, then 14. At 13 the array is exactly a Fibonacci number and the splits land cleanly; at 14 the algorithm pads up to 21 and the first probe sits further from the centre.</li>"
   "<li><strong>Search past the end.</strong> Set <strong>Search Target</strong> to a value larger than everything in the array. Watch the clamping keep probes inside the array even though the Fibonacci offsets would run past it &mdash; that clamp is the part implementations most often get wrong.</li>"
   "</ol>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Probing out of bounds.</strong> <span class=\"mono-font\">offset + F(k&minus;2)</span> can exceed the last index whenever n is not exactly a Fibonacci number. It must be clamped with <span class=\"mono-font\">min(offset + F(k&minus;2), n&minus;1)</span>, and omitting that is the classic implementation bug.</li>"
   "<li><strong>Expecting it to beat binary search.</strong> On modern hardware with a cache and a fast divider, binary search wins on almost every workload. Fibonacci search is the right choice for block-access storage or division-free processors, not as a general upgrade.</li>"
   "<li><strong>Recomputing the sequence each call.</strong> The Fibonacci numbers must be precomputed or maintained by subtraction. Regenerating them per search reintroduces the arithmetic you were avoiding.</li>"
   "<li><strong>Forgetting the sorted precondition.</strong> It is exactly as strict as binary search’s. Unsorted input gives silent wrong answers, not an error.</li>"
   "</ul>"),
  ("The short version",
   "<p>Fibonacci search is binary search rebuilt out of additions. It costs about 44% more comparisons because it divides by &phi; rather than by 2, and it earns that back only on hardware where division is expensive or where uneven, locality-friendly splits beat repeated jumps to the middle. Learn it for what it demonstrates: the halving in binary search is not sacred, and any constant-factor shrink per step still gives you a logarithm.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/interpolation_search.html": {
 "intro": "Guess where the value should be rather than always splitting in the middle. On uniformly distributed data it finds a target in about log log n steps - but the wrong distribution turns it back into a linear scan.",
 "sections": [
  ("Searching the way a person uses a phone book",
   "<p>Looking up “Zhang” in a phone book, nobody opens it at the exact middle. You open near the back, because you know where Z falls. Interpolation search formalises that: instead of probing the midpoint, it estimates the target’s position from its <em>value</em> relative to the values at the two ends.</p>"
   "<p>If the low element is 10, the high element is 1000, and you are looking for 100, the target sits about 9% of the way through the range &mdash; so probe about 9% of the way into the array, not 50%.</p>"),
  ("The probe formula",
   "<p>The position estimate is a straight-line interpolation between the endpoints:</p>"
   "<p class=\"mono-font\">pos = lo + ((target &minus; a[lo]) &times; (hi &minus; lo)) / (a[hi] &minus; a[lo])</p>"
   "<p>Take <span class=\"mono-font\">[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]</span> and search for 70. With lo=0, hi=9, a[lo]=10, a[hi]=100:</p>"
   "<p class=\"mono-font\">pos = 0 + ((70 &minus; 10) &times; 9) / (100 &minus; 10) = 540 / 90 = 6</p>"
   "<p>Index 6 holds exactly 70. <strong>One probe.</strong> Binary search would have needed three or four. On perfectly uniform data the first guess is often exact, and that is where the method’s reputation comes from.</p>"),
  ("Why log log n, and when it collapses",
   "<p>On uniformly distributed data each probe does not merely halve the remaining range &mdash; it reduces it to roughly its square root. That gives an average of O(log log n) comparisons, which for a million elements is about 4 rather than binary search’s 20.</p>"
   "<p>But the estimate assumes values grow linearly with index. When they do not, the guess is bad, and consistently bad guesses walk the array one element at a time. On exponentially distributed data such as <span class=\"mono-font\">[1, 2, 4, 8, 16, &hellip;, 2<sup>n</sup>]</span> the interpolation lands near the start every single time and the worst case degrades to <strong>O(n)</strong> &mdash; worse than the binary search it was meant to improve on.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>Watch a one-probe hit.</strong> Set <strong>Array Size</strong> to 30 and press <strong>Reset Array</strong> until the values look evenly spread, then set <strong>Search Target</strong> to a middling value and press <strong>Next Step</strong> once. The first probe often lands on or beside the answer.</li>"
   "<li><strong>Compare against a midpoint split.</strong> Note where the first probe lands for a small target such as the second-smallest value. Interpolation goes straight to the left edge; binary search would still have started dead centre.</li>"
   "<li><strong>Make it work hard.</strong> Set <strong>Search Target</strong> to a value near one extreme and press <strong>Auto-Run</strong>. Watch the probes cluster at that end &mdash; the algorithm homes in from the correct side immediately rather than converging symmetrically.</li>"
   "<li><strong>Scale it up.</strong> Step through a search at <strong>Array Size</strong> 5, then at 30. The probe count barely moves. That flatness is log log n: it grows so slowly that at these sizes it looks like a constant.</li>"
   "</ol>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Dividing by zero.</strong> When <span class=\"mono-font\">a[hi] == a[lo]</span> &mdash; every remaining element is equal &mdash; the denominator is zero. Guard that case explicitly before computing the probe.</li>"
   "<li><strong>Using it on non-uniform data.</strong> This is the real trap. Interpolation search is only a win when values are close to uniformly distributed. On skewed, clustered, or exponential data it is slower than binary search, and the failure is a quiet performance collapse rather than a crash.</li>"
   "<li><strong>Overflow in the numerator.</strong> <span class=\"mono-font\">(target &minus; a[lo]) &times; (hi &minus; lo)</span> multiplies two potentially large numbers. Use a wide enough type, or reorder to divide first.</li>"
   "<li><strong>Skipping the bounds check.</strong> A computed position must still be clamped to <span class=\"mono-font\">[lo, hi]</span>; with unsorted or corrupted input the formula can point outside the array entirely.</li>"
   "</ul>"),
  ("The short version",
   "<p>Interpolation search replaces binary search’s fixed midpoint with an estimate of where the value ought to live, and on uniformly distributed data that estimate is good enough to cut the cost from log n to log log n. The catch is that it is an assumption about the data, not a property of the algorithm: when the distribution is skewed the same formula degrades all the way to O(n). Use it when you know the distribution, and use binary search when you do not.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/insertion_sort.html": {
 "intro": "Build the sorted portion one element at a time, sliding each new value back to where it belongs. Quadratic in general, but genuinely the fastest choice on small or nearly-sorted arrays.",
 "sections": [
  ("How the sorted region grows",
   "<p>Treat the first element as a sorted region of length one. Take the next element, and slide it left past every element larger than it until it sits in the right place. The sorted region is now length two. Repeat until the sorted region is the whole array.</p>"
   "<p>This is how nearly everyone sorts a hand of playing cards, and the correspondence is exact: you hold a sorted fan, pick up a new card, and push it in at the right spot rather than re-sorting the whole hand.</p>"),
  ("Work one through by hand",
   "<p>Sort <span class=\"mono-font\">[5, 2, 9, 1]</span>.</p>"
   "<p class=\"mono-font\">[<u>5</u>, 2, 9, 1] &rarr; take 2, slide past 5 &rarr; [2, 5, 9, 1]</p>"
   "<p class=\"mono-font\">[<u>2, 5</u>, 9, 1] &rarr; take 9, already in place &rarr; [2, 5, 9, 1]</p>"
   "<p class=\"mono-font\">[<u>2, 5, 9</u>, 1] &rarr; take 1, slide past 9, 5, 2 &rarr; [1, 2, 5, 9]</p>"
   "<p>Six comparisons and four shifts. Notice that 9 cost exactly one comparison because it was already larger than everything to its left &mdash; the algorithm does no work when an element is already in position, which is the property everything else about it follows from.</p>"),
  ("Why O(n²) worst and O(n) best",
   "<p>The outer loop runs n&minus;1 times. The inner loop slides the current element back past however many larger elements sit to its left.</p>"
   "<p>On <strong>reverse-sorted</strong> input every element must travel the full width of the sorted region, giving 1 + 2 + 3 + &hellip; + (n&minus;1) = n(n&minus;1)/2 comparisons &mdash; O(n&sup2;).</p>"
   "<p>On <strong>already-sorted</strong> input every element fails its first comparison and stops immediately: n&minus;1 comparisons and zero shifts, so <strong>O(n)</strong>. Almost no other sort has a linear best case, and it is why insertion sort is the tail end of real library sorts.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>See the sorted region grow.</strong> Set <strong>Array Size</strong> to 12 and press <strong>Next Step</strong> repeatedly. The left-hand block is always sorted and always grows by exactly one per outer pass, no matter what the values are.</li>"
   "<li><strong>Find the cheap elements.</strong> Watch for values that stop after a single comparison. Every one of those was already larger than its left neighbour &mdash; the algorithm spent no effort at all on them.</li>"
   "<li><strong>Force the worst case.</strong> Press <strong>Randomize Array</strong> until you get something close to descending order, then <strong>Auto-Run</strong>. Every element crosses the entire sorted region and the shift count balloons toward n&sup2;/2.</li>"
   "<li><strong>Scale the cost.</strong> Run a full sort at <strong>Array Size</strong> 5 and then at 20. Four times the elements takes roughly sixteen times the shifts, not four &mdash; quadratic growth is visible directly in the counter.</li>"
   "</ol>"),
  ("Where it is actually used",
   "<p>Insertion sort is not a toy. It has four properties that keep it in production code:</p>"
   "<ul>"
   "<li><strong>Stable.</strong> Equal elements keep their original relative order, because sliding stops at the first element that is not strictly greater.</li>"
   "<li><strong>In-place.</strong> O(1) extra memory &mdash; no auxiliary array, unlike merge sort.</li>"
   "<li><strong>Adaptive.</strong> Cost is O(n + d) where d is the number of inversions. Nearly-sorted input is nearly linear.</li>"
   "<li><strong>Online.</strong> It can sort a stream, inserting each element as it arrives without seeing the rest.</li>"
   "</ul>"
   "<p>Together these are why virtually every industrial-strength sort &mdash; Timsort in Python and Java, introsort in C++ &mdash; recurses down with quicksort or merge sort and then hands subarrays below roughly 16 elements to insertion sort. At that size its tiny constant factor beats the recursive machinery outright.</p>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Swapping instead of shifting.</strong> Repeated swaps do three assignments where a shift does one. Hold the current value in a temporary, shift larger elements right, then drop it in once.</li>"
   "<li><strong>Using &ge; and destroying stability.</strong> The inner loop must stop on <span class=\"mono-font\">a[j] &gt; key</span>. Using <span class=\"mono-font\">&ge;</span> slides past equal elements and reverses their order, which quietly breaks any multi-key sort built on top.</li>"
   "<li><strong>Running off the front.</strong> The inner loop needs <span class=\"mono-font\">j &ge; 0</span> as well as the comparison; the smallest element in the array will otherwise walk straight past index 0.</li>"
   "<li><strong>Reaching for it on large random arrays.</strong> The adaptivity only helps when the data is nearly sorted. On 100,000 random elements it is thousands of times slower than merge sort.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Insertion sort grows a sorted prefix by sliding each new element back into place, which makes it O(n&sup2;) on random data and O(n) on sorted data. Stable, in-place, adaptive and online, it is the sort that real libraries fall back to once a divide-and-conquer sort has chopped the problem small enough &mdash; not despite being simple, but because being simple is what makes it fast at that scale.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/selection_sort.html": {
 "intro": "Find the smallest remaining element, swap it into place, repeat. Always quadratic - but it performs the fewest writes of any comparison sort, which is the one thing it is genuinely best at.",
 "sections": [
  ("The mechanism",
   "<p>Scan the entire unsorted region to find its minimum. Swap that minimum with the first unsorted position. That position is now finished and never moves again. Shrink the unsorted region by one and repeat.</p>"
   "<p>Where insertion sort takes the <em>next</em> element and finds its place, selection sort takes the <em>next place</em> and finds its element. That inversion is the whole difference, and it explains every performance property below.</p>"),
  ("Work one through by hand",
   "<p>Sort <span class=\"mono-font\">[29, 10, 14, 37, 13]</span>.</p>"
   "<p class=\"mono-font\">Pass 1: min of all five is 10 &rarr; swap with 29 &rarr; [<u>10</u>, 29, 14, 37, 13]</p>"
   "<p class=\"mono-font\">Pass 2: min of last four is 13 &rarr; swap with 29 &rarr; [<u>10, 13</u>, 14, 37, 29]</p>"
   "<p class=\"mono-font\">Pass 3: min of last three is 14 &rarr; already in place &rarr; [<u>10, 13, 14</u>, 37, 29]</p>"
   "<p class=\"mono-font\">Pass 4: min of last two is 29 &rarr; swap with 37 &rarr; [<u>10, 13, 14, 29</u>, 37]</p>"
   "<p>Four passes, 4 + 3 + 2 + 1 = 10 comparisons, and <strong>3 swaps</strong>. The comparison count is fixed by the array size; only the swap count depends on the data.</p>"),
  ("Why it is quadratic no matter what",
   "<p>Pass 1 scans n elements, pass 2 scans n&minus;1, and so on:</p>"
   "<p class=\"mono-font\">(n&minus;1) + (n&minus;2) + &hellip; + 1 = n(n&minus;1)/2 &nbsp;&rarr;&nbsp; O(n&sup2;)</p>"
   "<p>Critically this holds for <em>every</em> input. Finding a minimum requires examining every candidate, and the algorithm has no way to notice that the array is already sorted &mdash; it still scans the whole remaining region to confirm the minimum. Best case, average case and worst case are all &Theta;(n&sup2;), which makes selection sort strictly worse than insertion sort on nearly-sorted data.</p>"
   "<p>The compensation is the write count. Selection sort performs at most <strong>n&minus;1 swaps</strong> &mdash; O(n) writes, one per position. Insertion sort and bubble sort both perform O(n&sup2;) writes.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>Watch the scan, then the single swap.</strong> Set <strong>Array Size</strong> to 15 and press <strong>Next Step</strong>. Each pass sweeps the whole unsorted region looking for a minimum, then makes exactly one swap. The scanning is where all the time goes.</li>"
   "<li><strong>Confirm the sorted region never changes.</strong> Once a cell joins the sorted block on the left it is never touched again. Contrast with bubble sort, where elements keep moving until the very end.</li>"
   "<li><strong>Give it sorted input and watch it not care.</strong> Press <strong>Randomize Array</strong> until the array looks close to ascending, then <strong>Auto-Run</strong>. The comparison count is identical to a shuffled array &mdash; only the swaps drop. No other sort on this track is this indifferent to its input.</li>"
   "<li><strong>Count the swaps.</strong> Run a full sort at <strong>Array Size</strong> 30 and note the swap count stays at or below 29, while the comparison count climbs past 400. That ratio is the entire argument for using it.</li>"
   "</ol>"),
  ("The one situation where it wins",
   "<p>When writes are dramatically more expensive than reads, minimising them matters more than minimising comparisons. That is the case for EEPROM and flash memory, where each cell tolerates a limited number of erase cycles, and for any sort where moving an element means copying a large record rather than an integer.</p>"
   "<p>Selection sort guarantees at most n&minus;1 writes. Cycle sort pushes this to the theoretical minimum and is the specialist choice, but selection sort gets most of the benefit with far simpler code.</p>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Swapping on every comparison.</strong> The minimum’s <em>index</em> should be tracked through the scan and swapped once at the end. Swapping each time a smaller element appears turns the O(n) write advantage &mdash; the only reason to use it &mdash; back into O(n&sup2;).</li>"
   "<li><strong>Assuming it is stable.</strong> It is not. Sorting <span class=\"mono-font\">[2a, 2b, 1]</span> swaps the 1 with the first 2, putting 2b before 2a. Stability requires the shifting variant, which forfeits the low write count.</li>"
   "<li><strong>Expecting sorted input to be fast.</strong> Unlike insertion sort, there is no early exit and no adaptivity. Sorted input costs exactly as many comparisons as random input.</li>"
   "<li><strong>Skipping the self-swap check.</strong> When the minimum is already in position the swap is a no-op; guarding it costs one comparison and saves a write, which matters given that low writes are the point.</li>"
   "</ul>"),
  ("The short version",
   "<p>Selection sort makes n&minus;1 passes, each finding the minimum of what remains, giving &Theta;(n&sup2;) comparisons on every input and no benefit from partially sorted data. What it does offer is at most n&minus;1 swaps &mdash; the fewest writes of any simple comparison sort. On ordinary in-memory data insertion sort beats it on every axis; on write-limited storage that swap count is the reason to choose it anyway.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/merge_sort.html": {
 "intro": "Split the array in half, sort each half, then merge the two sorted halves. Guaranteed O(n log n) on every input, stable, and the reason it costs O(n) extra memory.",
 "sections": [
  ("Divide, conquer, combine",
   "<p>Merge sort is the textbook divide-and-conquer algorithm and it has exactly three steps. <strong>Divide:</strong> split the array at the midpoint. <strong>Conquer:</strong> sort each half by calling merge sort on it. <strong>Combine:</strong> merge the two sorted halves into one sorted array.</p>"
   "<p>The recursion bottoms out at arrays of length one, which are sorted by definition. All the real work happens in the merge, on the way back up.</p>"),
  ("The merge is the whole algorithm",
   "<p>Merging two sorted arrays is linear. Keep a finger on the front of each; repeatedly take the smaller of the two and advance that finger. Merge <span class=\"mono-font\">[2, 5, 9]</span> with <span class=\"mono-font\">[1, 6, 8]</span>:</p>"
   "<p class=\"mono-font\">compare 2 vs 1 &rarr; take 1 &nbsp;&nbsp; [1]</p>"
   "<p class=\"mono-font\">compare 2 vs 6 &rarr; take 2 &nbsp;&nbsp; [1, 2]</p>"
   "<p class=\"mono-font\">compare 5 vs 6 &rarr; take 5 &nbsp;&nbsp; [1, 2, 5]</p>"
   "<p class=\"mono-font\">compare 9 vs 6 &rarr; take 6 &nbsp;&nbsp; [1, 2, 5, 6]</p>"
   "<p class=\"mono-font\">compare 9 vs 8 &rarr; take 8 &nbsp;&nbsp; [1, 2, 5, 8]</p>"
   "<p class=\"mono-font\">left only &rarr; append 9 &nbsp;&nbsp; [1, 2, 5, 6, 8, 9]</p>"
   "<p>Six elements, five comparisons. Each comparison places exactly one element, so merging two runs of total length n costs at most n&minus;1 comparisons and exactly n writes.</p>"),
  ("Where n log n comes from",
   "<p>Halving the array repeatedly gives log&#8322;n levels of recursion &mdash; 32 elements become 16, 8, 4, 2, 1, which is 5 levels. At every level, the merges together touch all n elements exactly once. So:</p>"
   "<p class=\"mono-font\">total work = n per level &times; log<sub>2</sub>(n) levels = O(n log n)</p>"
   "<p>The recurrence is <span class=\"mono-font\">T(n) = 2T(n/2) + O(n)</span>, which is the standard case of the master theorem giving &Theta;(n log n). Crucially this holds for <em>every</em> input &mdash; the split is positional, not value-dependent, so there is no bad pivot and no worst case. Sorted, reversed and random input all cost the same.</p>"),
  ("Experiments to try",
   "<ol>"
   "<li><strong>Watch the recursion bottom out.</strong> Set <strong>Array Size</strong> to 16 and press <strong>Next Step</strong> repeatedly. The array splits until every block holds one element, and only then does anything get compared. All the sorting happens on the way back up.</li>"
   "<li><strong>Count the levels.</strong> At <strong>Array Size</strong> 16 there are 4 levels of merging; at 32 there are 5. Doubling the array adds one level, and each level costs a full pass &mdash; that is n log n, split into its two factors.</li>"
   "<li><strong>Give it sorted input.</strong> Press <strong>Randomize Array</strong> until the array is close to ascending and press <strong>Auto-Run</strong>. The step count barely moves. Unlike quick sort, merge sort has no input that hurts it.</li>"
   "<li><strong>Spot the extra array.</strong> Watch a merge closely: elements are written to a separate buffer and then copied back. That buffer is the O(n) auxiliary memory, and it is not an implementation detail you can optimise away.</li>"
   "</ol>"),
  ("The memory cost, and why it is unavoidable",
   "<p>Merging in place is the hard part. To write the smaller element into position 0 you must first move whatever already occupies position 0, and doing that without a buffer requires shifting &mdash; which turns the linear merge quadratic.</p>"
   "<p>So standard merge sort allocates an auxiliary array of size n, giving <strong>O(n) space</strong>. In-place merge sort algorithms exist, but they trade the clean linear merge for substantially worse constants and considerably more complexity. In practice, if memory is the constraint you use quick sort or heap sort instead.</p>"
   "<p>The exception is linked lists, where merging needs only pointer reassignment and no buffer. Merge sort on a linked list is O(1) extra space, which is why it is the standard list-sorting algorithm.</p>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Allocating a new buffer per recursive call.</strong> This turns O(n) space into O(n log n) and hammers the allocator. Allocate one buffer up front and pass it down.</li>"
   "<li><strong>Breaking stability with &lt; instead of &le;.</strong> When the two fronts are equal the merge must take from the <em>left</em> run. Using a strict comparison that prefers the right run reverses equal elements and silently destroys stability.</li>"
   "<li><strong>Forgetting the leftover tail.</strong> When one run empties, the remainder of the other must be copied across. Dropping that step truncates the output.</li>"
   "<li><strong>Recursing all the way to size 1.</strong> The call overhead dominates on tiny subarrays. Real implementations switch to insertion sort below roughly 16 elements, which typically buys 10&ndash;20%.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Merge sort splits positionally, sorts recursively, and does its real work in a linear merge, giving a guaranteed &Theta;(n log n) on every input with no pathological case. It is stable, it parallelises cleanly, and it is the natural sort for linked lists and for data too large to fit in memory. The price is O(n) auxiliary space for arrays &mdash; which is precisely the trade quick sort makes in the opposite direction.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/quick_sort.html": {
 "intro": "Pick a pivot, push everything smaller to its left and everything larger to its right, then recurse on both sides. Fastest sort in practice, and the only common one whose worst case is quadratic.",
 "sections": [
  ("Partitioning, not merging",
   "<p>Quick sort is divide-and-conquer with the work moved to the front. Choose a pivot element. Rearrange the array so that everything less than the pivot sits to its left and everything greater sits to its right &mdash; the pivot is now in its final sorted position, permanently. Recurse on the left part and the right part.</p>"
   "<p>There is no combine step. Once both sides are sorted, the array is sorted, because partitioning already placed everything on the correct side. That is the mirror image of merge sort, which splits trivially and does all its work merging.</p>"),
  ("Work one through by hand",
   "<p>Sort <span class=\"mono-font\">[7, 2, 9, 4, 1, 8]</span> using the last element, 8, as pivot.</p>"
   "<p class=\"mono-font\">less than 8: [7, 2, 4, 1] &nbsp;|&nbsp; pivot: 8 &nbsp;|&nbsp; greater: [9]</p>"
   "<p>8 is now final at index 4. Recurse left on <span class=\"mono-font\">[7, 2, 4, 1]</span> with pivot 1:</p>"
   "<p class=\"mono-font\">less: [] &nbsp;|&nbsp; pivot: 1 &nbsp;|&nbsp; greater: [7, 2, 4]</p>"
   "<p>Then <span class=\"mono-font\">[7, 2, 4]</span> with pivot 4 gives <span class=\"mono-font\">[2] | 4 | [7]</span>, and everything is placed. Note the second partition was badly unbalanced &mdash; 0 elements against 3 &mdash; which is exactly the behaviour that causes the worst case.</p>"),
  ("Best case, worst case, and why the average holds",
   "<p>When the pivot lands near the median, each partition halves the array, giving log n levels of O(n) partitioning work: <strong>O(n log n)</strong>.</p>"
   "<p>When the pivot is consistently the smallest or largest element, one side gets n&minus;1 elements and the other gets none. That gives n levels of O(n) work: <strong>O(n&sup2;)</strong>. With a fixed first- or last-element pivot this is triggered by <em>already-sorted input</em> &mdash; the most common real-world case, which is why naive quick sort is dangerous.</p>"
   "<p>The saving grace is that the average is robustly O(n log n). Even a split as lopsided as 90/10 at every level still gives logarithmic depth, just with a larger base. You need consistently near-worst pivots to reach quadratic, and randomising the pivot makes that vanishingly unlikely for any fixed input.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Watch a pivot settle permanently.</strong> Set <strong>Array Size</strong> to 15 and press <strong>Next Step</strong> through one partition. When it completes, the pivot is in its final position and is never moved again &mdash; unlike merge sort, elements finish one at a time.</li>"
   "<li><strong>Find a bad split.</strong> Press <strong>Randomize Array</strong> and <strong>Auto-Run</strong> a few times, watching the partition sizes. Occasionally one side gets almost everything; that single unbalanced level is a small dose of the worst case.</li>"
   "<li><strong>Compare the recursion shape with merge sort.</strong> Merge sort’s tree is always perfectly balanced because it splits by position. Quick sort’s depends entirely on the values, so the tree is lopsided and different on every run.</li>"
   "<li><strong>Scale it.</strong> Run a full sort at <strong>Array Size</strong> 5 and then 25. The comparison count grows roughly like n log n, noticeably slower than the n&sup2; growth of insertion sort at the same sizes.</li>"
   "</ol>"),
  ("Why it beats merge sort in practice",
   "<p>Both are O(n log n) on average, yet quick sort is usually faster on arrays. Three reasons:</p>"
   "<ul>"
   "<li><strong>No auxiliary array.</strong> Partitioning is in-place, needing only O(log n) stack space for the recursion. Merge sort needs an O(n) buffer, and allocating and touching it costs real time.</li>"
   "<li><strong>Cache behaviour.</strong> Partitioning sweeps two pointers inward through contiguous memory, which is close to the ideal access pattern for a CPU prefetcher.</li>"
   "<li><strong>Smaller constant factor.</strong> The inner loop is a comparison and a conditional swap, with no writes to a second array and no copy-back.</li>"
   "</ul>"
   "<p>Production implementations defend the worst case rather than accepting it: <strong>median-of-three</strong> or random pivot selection makes sorted input harmless, and <strong>introsort</strong> &mdash; the C++ standard library’s sort &mdash; counts recursion depth and switches to heap sort if it exceeds 2 log n, converting the quadratic worst case into a guaranteed O(n log n).</p>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Always taking the first or last element as pivot.</strong> This makes already-sorted input the worst case, which is the input you are most likely to receive. Use median-of-three or a random pivot.</li>"
   "<li><strong>Mishandling duplicates.</strong> An array of all-equal elements sends every element to one side under naive partitioning, giving O(n&sup2;). Three-way (Dutch national flag) partitioning splits into less / equal / greater and handles it in linear time.</li>"
   "<li><strong>Recursing on the larger side first.</strong> Recursing into the smaller partition and looping on the larger caps stack depth at O(log n). Doing it the other way risks stack overflow on adversarial input.</li>"
   "<li><strong>Expecting stability.</strong> Quick sort is not stable &mdash; partitioning swaps distant elements and reorders equal keys. If you need stability, use merge sort.</li>"
   "</ul>"),
  ("The short version",
   "<p>Quick sort partitions around a pivot, placing that pivot permanently and recursing on both sides with no combine step. In-place, cache-friendly and with a small constant factor, it is the fastest general-purpose array sort in practice &mdash; provided the pivot is chosen so that sorted input is not the worst case. Its O(n&sup2;) ceiling is real but avoidable, and every serious implementation avoids it by randomising the pivot or by falling back to heap sort when the recursion runs too deep.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/counting_sort.html": {
 "intro": "Sort without comparing anything. Tally how many times each value occurs, then rebuild the array from the tallies - linear time, provided the range of values is small.",
 "sections": [
  ("Beating the comparison lower bound",
   "<p>Every comparison-based sort needs &Omega;(n log n) comparisons in the worst case; that is a proven lower bound, not an engineering limit. Counting sort is faster because it never compares two elements. Instead it uses each value <em>as an index</em>, which is a fundamentally different source of information.</p>"
   "<p>The requirement is that values are integers in a known, bounded range. If a value can index an array, counting sort applies.</p>"),
  ("The three passes",
   "<p>Sort <span class=\"mono-font\">[3, 1, 4, 1, 5, 3, 1]</span> with values in 0&ndash;5.</p>"
   "<p><strong>1. Count.</strong> Walk the input, incrementing <span class=\"mono-font\">count[value]</span>:</p>"
   "<p class=\"mono-font\">index: 0 1 2 3 4 5<br>count: 0 3 0 2 1 1</p>"
   "<p><strong>2. Prefix sum.</strong> Replace each entry with the running total, so each slot holds the number of elements less than or equal to that value:</p>"
   "<p class=\"mono-font\">count: 0 3 3 5 6 7</p>"
   "<p><strong>3. Place.</strong> Walk the input <em>backwards</em>, and for each element use <span class=\"mono-font\">count[value] &minus; 1</span> as its output index, then decrement. The result is <span class=\"mono-font\">[1, 1, 1, 3, 3, 4, 5]</span>.</p>"
   "<p>Three linear passes and no comparison anywhere.</p>"),
  ("The complexity, and the k that matters",
   "<p>Counting sort runs in <strong>O(n + k)</strong> time and O(n + k) space, where n is the number of elements and k is the size of the value range.</p>"
   "<p>When k is O(n) this is linear and beats every comparison sort. When k is large it collapses: sorting 1,000 integers spread over the full 32-bit range means allocating a counting array of 4 billion entries to sort 1,000 values. The algorithm is not slow there so much as unusable.</p>"
   "<p>So the honest rule is that counting sort is linear <em>in n and k together</em>, and it is only a good idea when k is comparable to n or smaller.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Watch the tally build.</strong> Set <strong>Array Size</strong> to 20 and <strong>Max Value Limit (K)</strong> to 5, then press <strong>Next Step</strong> through the counting pass. No two input elements are ever compared &mdash; each one simply increments a bucket.</li>"
   "<li><strong>Make k small and see it win.</strong> Keep <strong>Array Size</strong> at 25 and set <strong>Max Value Limit (K)</strong> to 3. The counting array is tiny, buckets fill fast, and the whole sort finishes in three quick sweeps.</li>"
   "<li><strong>Make k large and watch the waste.</strong> Set <strong>Max Value Limit (K)</strong> to 15 with <strong>Array Size</strong> at 5. Now there are more buckets than elements and most sit empty &mdash; you are paying O(k) to sort n = 5. This is the failure mode, in miniature.</li>"
   "<li><strong>See stability in action.</strong> Press <strong>Randomize Array</strong> until duplicates appear, then <strong>Auto-Run</strong>. Equal values are emitted in their original relative order, because the placement pass walks the input backwards.</li>"
   "</ol>"),
  ("Why the last pass runs backwards",
   "<p>This is the detail that looks arbitrary and is not. Walking the input in reverse during the placement pass is what makes counting sort <strong>stable</strong> &mdash; equal elements keep their original relative order.</p>"
   "<p>The prefix-sum array says where the <em>last</em> copy of each value belongs. Consuming the input from the back means the last equal element is placed at the highest available slot, the second-to-last just below it, and so on, preserving input order. Walking forwards places them in reverse.</p>"
   "<p>Stability is not a nicety here: it is the entire reason <strong>radix sort</strong> works. Radix sort runs counting sort once per digit, from least significant to most, and relies on each pass preserving the order established by the previous one. Make counting sort unstable and radix sort produces garbage.</p>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Assuming values start at zero.</strong> With a range like 1000&ndash;1005, allocating 1006 buckets wastes almost all of them. Offset by the minimum: index with <span class=\"mono-font\">value &minus; min</span> and allocate <span class=\"mono-font\">max &minus; min + 1</span>.</li>"
   "<li><strong>Walking forwards in the placement pass.</strong> Silently destroys stability, and therefore silently breaks any radix sort built on top.</li>"
   "<li><strong>Using it on floats or strings.</strong> The value must be usable as an array index. Floats and arbitrary strings need a different approach &mdash; bucket sort or radix sort on their byte representation.</li>"
   "<li><strong>Ignoring k in the complexity.</strong> Calling counting sort “O(n)” without qualification is the most common mistake in exams and interviews. It is O(n + k), and k is what decides whether it is usable.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Counting sort tallies occurrences, converts the tallies to positions with a prefix sum, and writes elements straight to their final slots &mdash; no comparisons, so the &Omega;(n log n) bound does not apply. It runs in O(n + k) and is only worth using when the value range k is comparable to n. Its stability, which comes from that backwards final pass, is what makes radix sort possible.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/breadth_first_search.html": {
 "intro": "Visit a tree level by level rather than branch by branch. A queue is the only thing separating breadth-first search from its depth-first siblings - and that one choice decides everything about the order.",
 "sections": [
  ("Four ways to visit every node",
   "<p>A traversal visits every node exactly once. A tree is not linear, so there is no single obvious order &mdash; and the four standard orders differ only in <em>when</em> a node is processed relative to its children.</p>"
   "<ul>"
   "<li><strong>Inorder</strong> &mdash; left subtree, node, right subtree.</li>"
   "<li><strong>Preorder</strong> &mdash; node, left subtree, right subtree.</li>"
   "<li><strong>Postorder</strong> &mdash; left subtree, right subtree, node.</li>"
   "<li><strong>Level order (BFS)</strong> &mdash; every node at depth 0, then every node at depth 1, and so on.</li>"
   "</ul>"
   "<p>The first three are depth-first: they plunge to the bottom of one branch before considering the next. Only the fourth is breadth-first.</p>"),
  ("Read the four orders off one tree",
   "<p>Take this binary search tree:</p>"
   "<p class=\"mono-font\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8<br>&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;\\<br>&nbsp;&nbsp;&nbsp;3&nbsp;&nbsp;&nbsp;&nbsp;10<br>&nbsp;&nbsp;/ \\&nbsp;&nbsp;&nbsp;&nbsp;\\<br>&nbsp;1&nbsp;&nbsp;&nbsp;6&nbsp;&nbsp;&nbsp;&nbsp;14</p>"
   "<p class=\"mono-font\">Inorder:&nbsp;&nbsp;&nbsp;1, 3, 6, 8, 10, 14</p>"
   "<p class=\"mono-font\">Preorder:&nbsp;&nbsp;8, 3, 1, 6, 10, 14</p>"
   "<p class=\"mono-font\">Postorder: 1, 6, 3, 14, 10, 8</p>"
   "<p class=\"mono-font\">Level:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8, 3, 10, 1, 6, 14</p>"
   "<p>The inorder result is <strong>sorted</strong>. That is not a coincidence and not a property of this particular tree: inorder traversal of any binary search tree emits its keys in ascending order, because the BST invariant says everything left of a node is smaller and everything right is larger. It is the single most useful fact about BSTs.</p>"),
  ("Queue versus stack: the whole difference",
   "<p>Every traversal keeps a collection of nodes it has discovered but not yet processed. The <em>type</em> of collection determines the order:</p>"
   "<ul>"
   "<li>A <strong>stack</strong> (last in, first out) gives depth-first. The most recently discovered node is processed next, so the traversal keeps diving deeper. Recursion uses the call stack implicitly, which is why the three DFS orders are usually written recursively.</li>"
   "<li>A <strong>queue</strong> (first in, first out) gives breadth-first. The <em>oldest</em> undiscovered node goes next, so the traversal finishes an entire level before starting the one below.</li>"
   "</ul>"
   "<p>Swap the stack for a queue in a DFS implementation and you have written BFS. Nothing else changes.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Confirm inorder is sorted.</strong> Press <strong>Random</strong> to build a fresh tree, then press <strong>Inorder</strong>. Whatever shape the tree has, the output sequence comes out in ascending order.</li>"
   "<li><strong>Watch BFS sweep by level.</strong> Press <strong>Level (BFS)</strong> and follow the highlight. It moves strictly left to right across each row before dropping down &mdash; it never descends early, even when a branch is short.</li>"
   "<li><strong>Compare preorder with postorder.</strong> Run <strong>Preorder</strong>, then <strong>Postorder</strong> on the same tree. Preorder starts at the root; postorder ends there. That is why copying a tree uses preorder and deleting one uses postorder &mdash; you must handle the parent first to copy, and last to delete.</li>"
   "<li><strong>Change the shape and re-run.</strong> Use <strong>Node Operations</strong> to insert several increasing values, building a lopsided tree. Now the level-order and inorder outputs converge, because a degenerate tree is really a linked list.</li>"
   "</ol>"),
  ("What each order is actually for",
   "<ul>"
   "<li><strong>Inorder</strong> &mdash; retrieving BST contents in sorted order, and validating that a tree satisfies the BST property (the output must be strictly increasing).</li>"
   "<li><strong>Preorder</strong> &mdash; serialising or copying a tree. The root arrives first, so the structure can be rebuilt as it is read.</li>"
   "<li><strong>Postorder</strong> &mdash; deleting or freeing a tree, and evaluating expression trees. Children are fully handled before the parent, so you never free a node you still need.</li>"
   "<li><strong>Level order</strong> &mdash; finding the <em>shortest</em> path in an unweighted graph, printing a tree by depth, and any problem where nearer nodes must be considered before further ones.</li>"
   "</ul>"
   "<p>All four are O(n) time, since each node is visited once. Space differs: DFS costs O(h) for the stack where h is the height, BFS costs O(w) for the queue where w is the widest level. On a balanced tree the bottom level holds about half of all nodes, so BFS uses O(n) memory where DFS uses O(log n).</p>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Using BFS on a deep, wide tree without thinking about memory.</strong> The queue holds an entire level. For a balanced binary tree of a million nodes that is roughly 500,000 entries at the widest point, against DFS’s 20-frame stack.</li>"
   "<li><strong>Recursing depth-first on a degenerate tree.</strong> A tree built from sorted insertions has height n, and the recursion overflows the stack. Either balance the tree or use an explicit stack.</li>"
   "<li><strong>Forgetting to mark visited nodes on a graph.</strong> Trees have no cycles so traversal terminates naturally. Apply the same code to a general graph without a visited set and it loops forever.</li>"
   "<li><strong>Assuming preorder alone rebuilds a tree.</strong> It does not &mdash; preorder and postorder each lose the structure. You need inorder plus one of the others, or explicit null markers in the serialisation.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>All four traversals visit every node once in O(n); they differ only in when a node is handled relative to its children, and breadth-first differs from the rest only in using a queue instead of a stack. Inorder yields sorted output on a BST, preorder serialises, postorder frees, and level order finds the nearest thing first. Choose by which of those you need, then check whether O(h) or O(w) memory is the one you can afford.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/depth_first_search.html": {
 "intro": "Follow one path as far as it goes, then back up and take the next. Depth-first search is the traversal that answers reachability and structure questions - but it will not give you a shortest path.",
 "sections": [
  ("Go deep first, backtrack second",
   "<p>Start at a node and mark it visited. Pick any unvisited neighbour and move there. Repeat. When a node has no unvisited neighbours left, back up to the previous node and try its next neighbour. The search finishes when it has backed all the way out of the start node.</p>"
   "<p>The behaviour comes entirely from using a <strong>stack</strong>: the most recently discovered node is the next one explored, so the frontier keeps extending forwards rather than fanning out. Recursion gives you that stack for free, which is why DFS is usually four lines of code.</p>"),
  ("Trace it on a small graph",
   "<p>Take the graph with edges <span class=\"mono-font\">A&ndash;B, A&ndash;C, B&ndash;D, C&ndash;D, D&ndash;E</span>, starting at A and preferring alphabetical order:</p>"
   "<p class=\"mono-font\">visit A &rarr; visit B &rarr; visit D &rarr; visit E</p>"
   "<p class=\"mono-font\">E has no unvisited neighbours &rarr; back up to D</p>"
   "<p class=\"mono-font\">D&rsquo;s neighbour C is unvisited &rarr; visit C</p>"
   "<p class=\"mono-font\">order: A, B, D, E, C</p>"
   "<p>Notice that C is adjacent to A and yet is visited <em>last</em>. DFS has no sense of distance from the start &mdash; it went three hops deep before coming back for a direct neighbour. That single observation is why DFS cannot be used for shortest paths.</p>"),
  ("Complexity, and the visited set",
   "<p>DFS is <strong>O(V + E)</strong>: every vertex is pushed and popped once, and every edge is examined once from each endpoint. Space is O(V) for the visited set plus O(h) for the stack, where h is the length of the longest path explored &mdash; which in the worst case is V.</p>"
   "<p>The visited set is not an optimisation, it is a correctness requirement. Without it, any cycle sends the search around forever, and even in an acyclic graph a diamond shape causes exponential re-exploration of shared subgraphs.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>Watch it commit to one branch.</strong> Press <strong>Start Search</strong> and then <strong>Step</strong> repeatedly. The frontier is always a single path running away from the start &mdash; nothing fans out sideways.</li>"
   "<li><strong>Catch a backtrack.</strong> Keep stepping until the search hits a node with no unvisited neighbours. The highlight jumps <em>backwards</em> to the previous node. That jump is the stack popping, and it is the only moment DFS moves toward the start.</li>"
   "<li><strong>Slow it down.</strong> Set <strong>Search Speed</strong> to 1 and press <strong>Auto</strong>. At low speed the dive-and-retreat rhythm is obvious: long runs forward punctuated by sharp jumps back.</li>"
   "<li><strong>Change the shape.</strong> Switch <strong>Structure Type</strong> and press <strong>Reset State</strong>, then run again. On a wide, shallow structure DFS still refuses to explore breadthwise &mdash; it takes the first branch to its end regardless.</li>"
   "</ol>"),
  ("What DFS is good for",
   "<p>DFS answers questions about structure and connectivity rather than distance:</p>"
   "<ul>"
   "<li><strong>Cycle detection.</strong> If the search reaches a node already on the current recursion stack, there is a cycle. (Already <em>visited</em> is not enough &mdash; it must be on the current path.)</li>"
   "<li><strong>Topological sort.</strong> Push each node onto an output stack as its recursion finishes; the reversed finish order is a valid topological ordering of a DAG.</li>"
   "<li><strong>Connected components.</strong> Run DFS from each unvisited node; each run marks exactly one component.</li>"
   "<li><strong>Strongly connected components</strong> via Tarjan’s or Kosaraju’s algorithm, both built directly on DFS finish times.</li>"
   "<li><strong>Maze and puzzle solving</strong> where <em>a</em> solution is wanted rather than the shortest one.</li>"
   "</ul>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Using it for shortest paths.</strong> DFS finds <em>a</em> path, essentially never the shortest. Unweighted shortest paths need BFS; weighted need Dijkstra.</li>"
   "<li><strong>Stack overflow on deep graphs.</strong> Recursive DFS on a graph with a path of 100,000 nodes exhausts the call stack in most languages. Convert to an explicit stack when depth may be large.</li>"
   "<li><strong>Marking visited at the wrong moment.</strong> Mark a node when you <em>push</em> it, not when you pop it. Marking on pop lets the same node enter the stack many times before it is first processed.</li>"
   "<li><strong>Confusing “visited” with “on the current path” for cycle detection.</strong> Distinguishing the two &mdash; often white / grey / black colouring &mdash; is what makes cycle detection correct on a directed graph.</li>"
   "</ul>"),
  ("In one line",
   "<p>Depth-first search uses a stack to follow one path to exhaustion before backtracking, running in O(V + E) with O(h) stack space. It answers structural questions &mdash; cycles, components, topological order &mdash; extremely cheaply, and it is the wrong tool for anything involving distance, because it will happily visit a direct neighbour of the start last.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/dijkstras.html": {
 "intro": "Grow a set of nodes whose shortest distance is already final, always expanding the cheapest one next. It is the standard weighted shortest-path algorithm, and it breaks the moment an edge weight goes negative.",
 "sections": [
  ("Why BFS is not enough",
   "<p>On an unweighted graph, BFS finds shortest paths because every edge costs the same and the queue naturally orders nodes by hop count. Add weights and that collapses: a route of three cheap edges can beat one expensive edge, so the fewest hops is no longer the lowest cost.</p>"
   "<p>Dijkstra’s algorithm fixes this by replacing the queue with a <strong>priority queue</strong> ordered by distance from the source. Instead of expanding the node discovered earliest, it expands the node whose known distance is smallest.</p>"),
  ("The algorithm, and the invariant that makes it correct",
   "<p>Give the source distance 0 and everything else infinity. Then repeat: take the unvisited node with the smallest tentative distance, mark it visited, and for each neighbour check whether going through this node is cheaper than the neighbour’s current best:</p>"
   "<p class=\"mono-font\">if dist[u] + weight(u, v) &lt; dist[v]: dist[v] = dist[u] + weight(u, v)</p>"
   "<p>That check is called <strong>relaxation</strong>. The key claim is that when a node is selected as the minimum, its distance is already final and will never improve.</p>"
   "<p>Why? Any other route to it would have to leave the visited set through some unvisited node w. But w was not chosen, so <span class=\"mono-font\">dist[w] &ge; dist[u]</span>, and the rest of that route only adds more weight. So no cheaper route exists. <strong>This argument depends entirely on weights being non-negative</strong> &mdash; “the rest only adds more” is false if a later edge can subtract.</p>"),
  ("Work one through by hand",
   "<p>Edges: <span class=\"mono-font\">A&rarr;B (4), A&rarr;C (2), C&rarr;B (1), B&rarr;D (5), C&rarr;D (8)</span>, from A.</p>"
   "<p class=\"mono-font\">start:&nbsp; A=0, B=&infin;, C=&infin;, D=&infin;</p>"
   "<p class=\"mono-font\">pick A &rarr; relax: B=4, C=2</p>"
   "<p class=\"mono-font\">pick C (2, smallest) &rarr; relax: B = min(4, 2+1) = 3, D = 2+8 = 10</p>"
   "<p class=\"mono-font\">pick B (3) &rarr; relax: D = min(10, 3+5) = 8</p>"
   "<p class=\"mono-font\">pick D (8) &rarr; done</p>"
   "<p>The shortest route to B is A&rarr;C&rarr;B at cost 3, not the direct edge at cost 4. Two hops beat one, which is exactly the case BFS gets wrong.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Watch it expand by cost, not by distance on screen.</strong> Press <strong>Start Solver</strong> then <strong>Step</strong> repeatedly. The next node chosen is always the cheapest known, which is often not the nearest-looking one.</li>"
   "<li><strong>Catch a relaxation.</strong> Keep stepping and watch a node’s distance <em>drop</em> when a better route is found. Every improvement is one relaxation, and once a node is finalised its number never changes again.</li>"
   "<li><strong>Slow the expansion.</strong> Set <strong>Search Speed</strong> to 1 and press <strong>Auto</strong>. The visited set grows outward in rings of equal cost &mdash; that shape is Dijkstra exploring uniformly in every direction, which is precisely what A* improves on.</li>"
   "<li><strong>Change the graph.</strong> Pick a different <strong>Network Topology</strong>, press <strong>Reset Grid</strong>, and run again. On a denser graph many more relaxations happen per node, because each node has more neighbours to improve.</li>"
   "</ol>"),
  ("Complexity, and why the priority queue matters",
   "<p>With a binary heap the cost is <strong>O((V + E) log V)</strong>: each of V nodes is extracted once at O(log V), and each of E edges may trigger a decrease-key at O(log V).</p>"
   "<p>With a naive array scan for the minimum it is O(V&sup2;), which is actually <em>faster</em> on dense graphs where E approaches V&sup2;. With a Fibonacci heap the theoretical bound improves to O(E + V log V), though the constants are bad enough that binary heaps usually win in practice.</p>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>Using it with negative edge weights.</strong> The correctness argument fails and the algorithm returns wrong answers silently &mdash; a node finalised early may have a cheaper route through an edge considered later. Use Bellman-Ford, which handles negatives in O(VE) and detects negative cycles.</li>"
   "<li><strong>Re-processing stale heap entries.</strong> Most implementations push duplicates instead of doing decrease-key. You must skip a popped node if it is already visited, or you will relax from an out-of-date distance.</li>"
   "<li><strong>Forgetting the predecessor array.</strong> Dijkstra computes distances; reconstructing the actual route needs the parent pointer recorded on every successful relaxation.</li>"
   "<li><strong>Running it to completion when one target is wanted.</strong> You can stop as soon as the target is popped &mdash; its distance is final at that moment. Continuing wastes the rest of the graph.</li>"
   "</ul>"),
  ("In one line",
   "<p>Dijkstra’s algorithm repeatedly finalises the cheapest unvisited node and relaxes its edges, giving single-source shortest paths in O((V + E) log V) with a binary heap. Its correctness rests on non-negative weights, so negative edges call for Bellman-Ford instead. Because it expands uniformly in all directions, it does more work than necessary when you only want one destination &mdash; which is the gap A* fills.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/a_star.html": {
 "intro": "Dijkstra with a sense of direction. Adding an estimate of the remaining distance steers the search toward the goal instead of expanding uniformly - and if that estimate never overestimates, the path is still optimal.",
 "sections": [
  ("The problem with searching in every direction",
   "<p>Dijkstra’s algorithm expands outward from the source in rings of equal cost. If the goal is due east, it still explores just as far north, south and west before reaching it. On a large map that is enormous wasted effort &mdash; the algorithm has no idea where it is going.</p>"
   "<p>A* adds that idea. Alongside the known cost from the start it keeps an <em>estimate</em> of the cost still to come, and expands whichever node looks best on the total.</p>"),
  ("f = g + h",
   "<p>Every node carries three numbers:</p>"
   "<ul>"
   "<li><span class=\"mono-font\">g(n)</span> &mdash; the actual cost of the best known path from the start to n. This is exactly Dijkstra’s distance.</li>"
   "<li><span class=\"mono-font\">h(n)</span> &mdash; the <strong>heuristic</strong>: an estimate of the remaining cost from n to the goal.</li>"
   "<li><span class=\"mono-font\">f(n) = g(n) + h(n)</span> &mdash; the estimated total cost of a route through n.</li>"
   "</ul>"
   "<p>A* is then exactly Dijkstra with the priority queue ordered by f instead of g. Set <span class=\"mono-font\">h(n) = 0</span> everywhere and you get Dijkstra back precisely &mdash; A* is a strict generalisation, not a different algorithm.</p>"),
  ("Admissible, consistent, and why it stays optimal",
   "<p>A heuristic is <strong>admissible</strong> if it never overestimates the true remaining cost. That single property is what guarantees A* finds an optimal path.</p>"
   "<p>The reason: if h never overestimates, then f(n) never overestimates the cost of the best route through n. So when the goal is popped with total cost f, no unexplored node can be hiding a cheaper route &mdash; any such node would have had a smaller f and been popped first.</p>"
   "<p>Overestimate, and that breaks. An inflated h can make the true best route look worse than a bad one, and A* will return the bad one. The common heuristics on a grid are admissible by construction:</p>"
   "<ul>"
   "<li><strong>Manhattan</strong> <span class=\"mono-font\">|dx| + |dy|</span> &mdash; admissible when movement is 4-directional, because that is the exact distance with no obstacles.</li>"
   "<li><strong>Euclidean</strong> <span class=\"mono-font\">&radic;(dx&sup2; + dy&sup2;)</span> &mdash; admissible always, since a straight line is the shortest possible route, but weak (too low) on 4-directional grids.</li>"
   "<li><strong>Zero</strong> &mdash; admissible and useless: this is Dijkstra.</li>"
   "</ul>"
   "<p>Note that Manhattan is <em>not</em> admissible if diagonal movement is allowed, because the diagonal route is shorter than |dx| + |dy|. That mismatch is the most common way people accidentally break optimality.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>See the search become directional.</strong> Press <strong>Run Algorithm</strong> and watch the explored region. It stretches toward the goal rather than spreading in a circle &mdash; that elongation is h doing its job.</li>"
   "<li><strong>Turn the heuristic off.</strong> Set <strong>Heuristic</strong> to the zero or Dijkstra option and press <strong>Reset Grid</strong>, then run again. The explored area balloons into a symmetric blob. The path found is the same length; the work to find it is far greater.</li>"
   "<li><strong>Compare Manhattan against Euclidean.</strong> Run each in turn on the same grid. Manhattan is the larger estimate on a 4-directional grid, so it prunes harder and expands fewer nodes while still finding an optimal route.</li>"
   "<li><strong>Slow it down and watch the frontier choose.</strong> Set <strong>Execution Speed</strong> to 1 and run. Each expansion picks the lowest f, so the frontier repeatedly reaches toward the goal and only falls back sideways when it meets an obstacle.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<ul>"
   "<li><strong>An inadmissible heuristic.</strong> Scaling h up (multiplying by 1.5, say) makes the search much faster and quietly non-optimal. That trade is sometimes worth making &mdash; weighted A* is a real technique &mdash; but it must be a decision, not an accident.</li>"
   "<li><strong>Manhattan distance with diagonal movement.</strong> Overestimates, so paths stop being optimal. Use the octile heuristic when diagonals are allowed.</li>"
   "<li><strong>Forgetting that a node’s g can improve.</strong> With a merely admissible (not consistent) heuristic, a node may be reached again more cheaply after being expanded. Either use a consistent heuristic or re-open such nodes.</li>"
   "<li><strong>An expensive heuristic.</strong> h is evaluated constantly. If computing it costs more than the expansions it saves, A* is slower than Dijkstra despite exploring fewer nodes.</li>"
   "</ul>"),
  ("What to remember",
   "<p>A* orders its priority queue by f = g + h, where g is the cost so far and h estimates the cost remaining, which focuses the search along the direction of the goal instead of expanding uniformly. Provided h never overestimates, the path returned is still optimal &mdash; and the better the estimate, the fewer nodes get expanded. With h = 0 it degenerates exactly to Dijkstra, which is the cleanest way to see what the heuristic is buying.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/backtracking.html": {
 "intro": "Try a choice, follow it as far as it goes, and undo it the moment it fails. Backtracking is brute force with the dead ends pruned away - which is often the difference between impossible and instant.",
 "sections": [
  ("Systematic trial and error",
   "<p>Backtracking builds a solution one decision at a time. At each step it takes a candidate choice and recurses. If that eventually leads to a solution, done. If it leads to a dead end, the algorithm <strong>undoes</strong> the choice and tries the next candidate. If every candidate fails, it returns failure to the previous level, which then undoes <em>its</em> choice.</p>"
   "<p>The undo step is what distinguishes backtracking from plain recursion, and it is where implementations usually go wrong. State that was mutated on the way down must be restored on the way back up, or later branches inherit the corruption.</p>"),
  ("The template",
   "<p>Nearly every backtracking problem fits this shape:</p>"
   "<p class=\"mono-font\">solve(state):<br>"
   "&nbsp;&nbsp;if state is complete: record it, return<br>"
   "&nbsp;&nbsp;for each candidate c:<br>"
   "&nbsp;&nbsp;&nbsp;&nbsp;if c is not valid here: continue&nbsp;&nbsp;&nbsp;&larr; pruning<br>"
   "&nbsp;&nbsp;&nbsp;&nbsp;apply c to state<br>"
   "&nbsp;&nbsp;&nbsp;&nbsp;solve(state)<br>"
   "&nbsp;&nbsp;&nbsp;&nbsp;undo c from state&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&larr; the backtrack</p>"
   "<p>The validity check is the entire performance story. Without it you are enumerating every possibility; with it you discard whole subtrees before exploring them.</p>"),
  ("How much pruning buys you",
   "<p>The eight queens problem asks for eight queens on a chessboard with none attacking another. Placing eight pieces on 64 squares gives about 4.4 billion arrangements. Restricting to one queen per column cuts it to 8<sup>8</sup> = 16.7 million. Checking rows and diagonals as you place each queen &mdash; abandoning a branch the moment two queens conflict &mdash; brings the actual number of positions examined down to roughly <strong>15,000</strong>.</p>"
   "<p>Same search space, same guarantee of finding every solution, five orders of magnitude less work. The algorithm did not get cleverer about queens; it just stopped exploring branches that were already known to fail.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>Watch a path get committed.</strong> Press <strong>Step</strong> repeatedly. The search extends along a single route, taking the first available direction each time &mdash; the same depth-first commitment as DFS.</li>"
   "<li><strong>Catch the undo.</strong> Keep stepping until the path hits a dead end. Watch cells get <em>unmarked</em> as the search retreats. That erasure is the backtrack, and it is what frees those cells for a different attempt.</li>"
   "<li><strong>Watch it re-use a corridor.</strong> After a retreat, notice the search often re-enters territory it just abandoned, this time turning a different way. The state was properly restored, which is exactly why that is possible.</li>"
   "<li><strong>Compare mazes.</strong> Press <strong>New Maze</strong> a few times and <strong>Run</strong> each. Open mazes with many branches cause far more backtracking than corridor-like mazes, where there is rarely a choice to get wrong.</li>"
   "</ol>"),
  ("Where it is used",
   "<p>Backtracking is the standard approach whenever a problem is “find an assignment satisfying these constraints”:</p>"
   "<ul>"
   "<li><strong>Sudoku and N-queens</strong> &mdash; the canonical examples, both solved instantly with constraint checking and hopeless without.</li>"
   "<li><strong>Permutations, combinations and subsets</strong> &mdash; generating all arrangements of a set.</li>"
   "<li><strong>Maze and path finding</strong> when any route will do.</li>"
   "<li><strong>Graph colouring</strong> and general constraint satisfaction, where it is the basis of real CSP solvers.</li>"
   "<li><strong>Regular expression matching</strong> &mdash; and the reason a pathological pattern can hang: catastrophic backtracking is this algorithm failing to prune.</li>"
   "</ul>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Not undoing the state.</strong> The single most common bug. If you mark a cell, recurse, and forget to unmark it on failure, later branches see phantom occupied cells and valid solutions get missed.</li>"
   "<li><strong>Pruning too late.</strong> Checking validity only when the solution is complete turns backtracking back into brute force. Check at every step, as early as the constraint allows.</li>"
   "<li><strong>Passing mutable state by reference and recording it directly.</strong> When a solution is found, store a <em>copy</em>. Storing the live object means the backtracking that follows mutates your recorded answer.</li>"
   "<li><strong>Expecting it to be fast in the worst case.</strong> Pruning improves the typical case, not the bound &mdash; worst-case complexity is still exponential. If pruning is weak, so is the algorithm.</li>"
   "</ul>"),
  ("In one line",
   "<p>Backtracking explores the space of partial solutions depth-first, abandoning a branch as soon as it violates a constraint and undoing its state on the way back out. The undo is what makes it correct and the early constraint check is what makes it fast &mdash; without pruning it is exhaustive search, and with it, problems with billions of arrangements resolve in thousands of steps. The complexity remains exponential in the worst case; the art is in pruning hard enough that the worst case rarely arrives.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/dictionaries_in_python.html": {
 "intro": "Python's dict is a hash table with O(1) average lookup and, since 3.7, a guaranteed insertion order. Knowing which operations are cheap and which quietly are not is most of using it well.",
 "sections": [
  ("What a dict actually is",
   "<p>A dictionary maps keys to values. Internally it is a <strong>hash table</strong>: Python calls <span class=\"mono-font\">hash(key)</span>, reduces the result to an index into an array of slots, and stores the entry there. Looking a key up repeats the computation and goes straight to the slot &mdash; no scanning.</p>"
   "<p>That is why lookup is O(1) on average rather than O(n): the cost does not depend on how many items the dict holds. A dict with ten entries and a dict with ten million take about the same time to answer <span class=\"mono-font\">d[k]</span>.</p>"),
  ("The operations, and what they cost",
   "<p class=\"mono-font\">d[k] = v&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# insert or overwrite &mdash; O(1)</p>"
   "<p class=\"mono-font\">d[k]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# lookup, KeyError if absent &mdash; O(1)</p>"
   "<p class=\"mono-font\">d.get(k, default) # lookup, default if absent &mdash; O(1)</p>"
   "<p class=\"mono-font\">k in d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# membership &mdash; O(1)</p>"
   "<p class=\"mono-font\">d.pop(k)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# remove and return &mdash; O(1)</p>"
   "<p class=\"mono-font\">d.keys() / .values() / .items()&nbsp;# views &mdash; O(1) to create</p>"
   "<p>The last one catches people out. <span class=\"mono-font\">d.keys()</span> does not build a list; it returns a lightweight <strong>view</strong> that stays live as the dict changes. Iterating it is O(n), but creating it is free.</p>"
   "<p>The important contrast is with values. <span class=\"mono-font\">k in d</span> checks keys and is O(1); <span class=\"mono-font\">v in d.values()</span> scans and is O(n). They look symmetric and are not.</p>"),
  ("Try it yourself",
   "<ol>"
   "<li><strong>Compare get with direct indexing.</strong> Choose <strong>Method</strong> for a lookup on a missing key and press <strong>Execute</strong>. Direct indexing raises KeyError; <span class=\"mono-font\">get</span> returns None instead. That difference decides which one belongs in your code.</li>"
   "<li><strong>Overwrite an existing key.</strong> Run an insert with a key that is already present. The dict does not grow &mdash; assignment on an existing key replaces the value in place, which is why dicts cannot hold duplicate keys.</li>"
   "<li><strong>Watch insertion order hold.</strong> Insert several keys in a deliberate order and then iterate. They come back in the order added, not sorted and not hashed &mdash; a language guarantee since Python 3.7.</li>"
   "<li><strong>Delete and re-add.</strong> Remove a key with <strong>Method</strong> set to a pop or delete, then add it back. It reappears at the <em>end</em> of the iteration order, because insertion order means the order of the most recent insertion.</li>"
   "</ol>"),
  ("Why keys must be hashable",
   "<p>A key must be hashable, which in practice means immutable. Strings, numbers and tuples work; lists, dicts and sets do not, and <span class=\"mono-font\">d[[1,2]] = x</span> raises <span class=\"mono-font\">TypeError: unhashable type: 'list'</span>.</p>"
   "<p>The reason is that the hash determines the storage slot. If a key could change after insertion, its hash would change, and the entry would be sitting in a slot the lookup no longer computes &mdash; the value would become unreachable while still occupying memory. Forbidding mutable keys makes that impossible.</p>"
   "<p>A tuple is hashable only if everything inside it is, so <span class=\"mono-font\">(1, 2)</span> works as a key and <span class=\"mono-font\">(1, [2])</span> does not.</p>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Using try/except KeyError where get belongs.</strong> When a missing key is expected rather than exceptional, <span class=\"mono-font\">d.get(k, default)</span> is clearer and faster than catching.</li>"
   "<li><strong>Mutating a dict while iterating it.</strong> Adding or deleting during a <span class=\"mono-font\">for k in d</span> loop raises RuntimeError. Iterate over <span class=\"mono-font\">list(d)</span> if the dict must change inside the loop.</li>"
   "<li><strong>Searching values in a loop.</strong> <span class=\"mono-font\">if v in d.values()</span> inside a loop over n items is O(n&sup2;). If you need lookup by value, build the inverted dict once.</li>"
   "<li><strong>Reinventing defaultdict and Counter.</strong> Checking whether a key exists before appending is what <span class=\"mono-font\">collections.defaultdict</span> is for, and counting occurrences is what <span class=\"mono-font\">collections.Counter</span> is for.</li>"
   "</ul>"),
  ("What to remember",
   "<p>A Python dict is a hash table giving O(1) average insert, lookup, and delete, with keys required to be hashable so their storage slot cannot move. Since 3.7 it also preserves insertion order. The traps are the asymmetries: keys are O(1) but values are O(n), views are live rather than snapshots, and mutating during iteration is an error rather than undefined behaviour.</p>"),
 ]},

# ---------------------------------------------------------------------------
"dsa/lists_in_python.html": {
 "intro": "A Python list is a dynamic array, not a linked list. That single fact explains why appending is fast, inserting at the front is slow, and slicing always costs a copy.",
 "sections": [
  ("A dynamic array, not a linked list",
   "<p>Despite the name, a Python list is a contiguous array of pointers. Elements sit next to each other in memory, so indexing is a single address calculation: <span class=\"mono-font\">lst[i]</span> is O(1) regardless of the list’s length or the value of i.</p>"
   "<p>Everything else follows from that layout. Inserting in the middle means shifting every later element up one slot. Deleting means shifting them down. Only the end of the list can be modified without moving anything &mdash; which is why <span class=\"mono-font\">append</span> and <span class=\"mono-font\">pop()</span> are the fast operations and their front-of-list counterparts are not.</p>"),
  ("Indexing and slicing",
   "<p>Indices count from 0, and negative indices count from the end: <span class=\"mono-font\">lst[-1]</span> is the last element, <span class=\"mono-font\">lst[-2]</span> the second-last.</p>"
   "<p>A slice takes <span class=\"mono-font\">[start:stop:step]</span>, where start is inclusive, stop is exclusive, and any part may be omitted. With <span class=\"mono-font\">lst = [10, 20, 30, 40, 50]</span>:</p>"
   "<p class=\"mono-font\">lst[1:4]&nbsp;&nbsp;&rarr; [20, 30, 40]&nbsp;&nbsp;&nbsp;# stop is excluded</p>"
   "<p class=\"mono-font\">lst[:3]&nbsp;&nbsp;&nbsp;&rarr; [10, 20, 30]</p>"
   "<p class=\"mono-font\">lst[::2]&nbsp;&nbsp;&rarr; [10, 30, 50]&nbsp;&nbsp;&nbsp;# every second element</p>"
   "<p class=\"mono-font\">lst[::-1]&nbsp;&rarr; [50, 40, 30, 20, 10]&nbsp;# reversed</p>"
   "<p>The exclusive stop is deliberate: it makes <span class=\"mono-font\">lst[:k] + lst[k:]</span> reconstruct the original for any k, and it makes the length of a slice simply <span class=\"mono-font\">stop &minus; start</span>. Every slice returns a <strong>new list</strong>, so slicing an n-element list costs O(n) time and O(n) memory &mdash; slicing in a loop is a common accidental quadratic.</p>"),
  ("What each operation costs",
   "<p class=\"mono-font\">lst[i]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# O(1)&nbsp;&nbsp; direct address</p>"
   "<p class=\"mono-font\">lst.append(x)&nbsp;&nbsp;&nbsp;# O(1) amortised</p>"
   "<p class=\"mono-font\">lst.pop()&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# O(1)&nbsp;&nbsp; from the end</p>"
   "<p class=\"mono-font\">lst.insert(0, x)&nbsp;# O(n)&nbsp;&nbsp; shifts everything</p>"
   "<p class=\"mono-font\">lst.pop(0)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# O(n)&nbsp;&nbsp; shifts everything</p>"
   "<p class=\"mono-font\">x in lst&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# O(n)&nbsp;&nbsp; linear scan</p>"
   "<p class=\"mono-font\">lst[a:b]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# O(b&minus;a) copies</p>"
   "<p><strong>Amortised</strong> O(1) for append means individual appends are occasionally expensive. When the underlying array fills, Python allocates a larger one and copies everything across &mdash; O(n) for that one call. Because the array grows by a proportion rather than a fixed amount, those resizes become rarer as the list grows, and the average over many appends is constant.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Watch the exclusive stop.</strong> Set <strong>Start</strong> to 1 and <strong>Stop</strong> to 4, then press <strong>Run Expression</strong>. Three elements come back, not four &mdash; index 4 is the boundary, not a member.</li>"
   "<li><strong>Reverse with a negative step.</strong> Set <strong>Step</strong> to &minus;1 and leave start and stop empty. The whole list comes back reversed, and it is a copy: the original is untouched.</li>"
   "<li><strong>Index from the end.</strong> Set <strong>Index (i)</strong> to &minus;1 and run. You get the last element without needing to know the length &mdash; the idiom that replaces <span class=\"mono-font\">lst[len(lst)&minus;1]</span>.</li>"
   "<li><strong>Compare a front insert with an append.</strong> Use <strong>Select Method</strong> to insert at index 0, then to append. Both look instant here, but only one avoids shifting every element &mdash; the difference shows up at a hundred thousand elements, not five.</li>"
   "</ol>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Using pop(0) as a queue.</strong> Every removal shifts the whole list, so a queue built this way is O(n&sup2;). Use <span class=\"mono-font\">collections.deque</span>, which is O(1) at both ends.</li>"
   "<li><strong>The mutable default argument.</strong> <span class=\"mono-font\">def f(items=[])</span> creates the list <em>once</em>, at definition time, and every call shares it. Use <span class=\"mono-font\">None</span> as the default and build the list inside.</li>"
   "<li><strong>Assuming assignment copies.</strong> <span class=\"mono-font\">b = a</span> binds another name to the same list; mutating b changes a. Use <span class=\"mono-font\">a[:]</span> or <span class=\"mono-font\">list(a)</span> for a shallow copy.</li>"
   "<li><strong>Removing items while iterating.</strong> Deleting during a <span class=\"mono-font\">for</span> loop shifts the remaining elements and the loop skips items. Iterate over a copy, or build a new list with a comprehension.</li>"
   "<li><strong>Multiplying to build a grid.</strong> <span class=\"mono-font\">[[0]*3]*3</span> makes three references to the <em>same</em> row. Use a comprehension: <span class=\"mono-font\">[[0]*3 for _ in range(3)]</span>.</li>"
   "</ul>"),
  ("What to remember",
   "<p>A Python list is a contiguous dynamic array, so indexing is O(1), appending is amortised O(1), and anything touching the front is O(n) because every later element must shift. Slices are always copies, negative indices count from the end, and the stop bound is exclusive. Most list performance bugs are one of two things: treating the front like the back, or slicing inside a loop.</p>"),
 ]},

}
