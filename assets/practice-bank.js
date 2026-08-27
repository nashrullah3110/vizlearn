/* GENERATED FILE - do not edit by hand.
 * Source: the same checks tools/build_labs.py writes into each module.
 * Rebuild: python3 tools/build_labs.py
 */
window.VIZLEARN_PRACTICE = [
 {
  "path": "dsa/a_star.html",
  "title": "A* Pathfinding Algorithm",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Setting the heuristic to zero turns A* into:",
    "o": [
     "BFS",
     "Dijkstra",
     "Greedy best-first search",
     "DFS"
    ],
    "a": 1,
    "w": "f = g + h collapses to f = g, which is Dijkstra's priority exactly. The program runs the identical function both ways to show it."
   },
   {
    "t": "An admissible heuristic is one that:",
    "o": [
     "Is fast to compute",
     "Never overestimates the remaining cost",
     "Is always exact",
     "Ignores obstacles"
    ],
    "a": 1,
    "w": "Overestimating lets A* commit to a route before a cheaper one is examined, so the path it returns can be longer than the shortest."
   },
   {
    "t": "Both searches in the program return a path of the same length. What differs?",
    "o": [
     "The path itself",
     "The number of cells expanded",
     "The memory used",
     "Nothing"
    ],
    "a": 1,
    "w": "136 cells against 90 on this grid. A* is not more correct - it is the same answer reached without looking away from the goal."
   }
  ]
 },
 {
  "path": "dsa/backtracking.html",
  "title": "Backtracking Search Method",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is the 'backtrack' in the N-queens program?",
    "o": [
     "The recursive call",
     "queens.pop() - undoing the placement",
     "The safe() check",
     "Returning the solution"
    ],
    "a": 1,
    "w": "Place, explore, undo. Delete the pop and the state leaks into sibling branches, so the search finds nothing while looking like an optimisation."
   },
   {
    "t": "Why is state stored as one column per row rather than as a board?",
    "o": [
     "It is smaller",
     "It makes 'two queens in the same row' impossible by construction",
     "It is faster to print",
     "The board would be too large"
    ],
    "a": 1,
    "w": "Encoding removes an entire class of conflict for free, and the recursion depth becomes the row being filled."
   },
   {
    "t": "Backtracking beats brute force because it:",
    "o": [
     "Is not exponential",
     "Abandons a partial placement before generating any of its completions",
     "Uses less memory",
     "Checks solutions in a better order"
    ],
    "a": 1,
    "w": "It is still exponential in the worst case, just over a far smaller space - the program prints the percentage of positions pruned."
   }
  ]
 },
 {
  "path": "dsa/bellman_ford.html",
  "title": "Bellman-Ford and Negative Weights",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Why exactly V - 1 rounds?",
    "o": [
     "It is a safety margin",
     "A shortest path visits each node once, so it has at most V - 1 edges",
     "It matches the edge count",
     "To detect cycles"
    ],
    "a": 1,
    "w": "Each round settles at least one more edge of any shortest path, so V - 1 rounds is enough and one more would be wasted."
   },
   {
    "t": "How does the algorithm detect a negative cycle?",
    "o": [
     "It counts the edges",
     "It checks for negative weights up front",
     "One extra relaxation round still improves something",
     "The distances go to negative infinity"
    ],
    "a": 2,
    "w": "After V - 1 rounds the distances are final if they exist. A further improvement proves you can keep going round and getting cheaper, so no shortest path exists."
   },
   {
    "t": "Compared with Dijkstra, Bellman-Ford is:",
    "o": [
     "Faster and more general",
     "Slower but handles negative weights",
     "Faster but needs sorted edges",
     "The same algorithm"
    ],
    "a": 1,
    "w": "O(V·E) against O(E log V). You pay for the generality, which is why Dijkstra remains the default when weights are non-negative."
   }
  ]
 },
 {
  "path": "dsa/big_o_notation.html",
  "title": "Big-O Notation and Time Complexity",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Big-O describes:",
    "o": [
     "Exactly how many seconds an algorithm takes",
     "How the cost grows as the input grows",
     "How much memory a language uses",
     "How readable the code is"
    ],
    "a": 1,
    "w": "It is a statement about growth, not about wall-clock time. Hardware changes the constant; it does not change the shape of the curve."
   },
   {
    "t": "Which is O(1)?",
    "o": [
     "Scanning a list for a value",
     "Reading array element 5 by index",
     "Sorting a list",
     "Nested loops over the same list"
    ],
    "a": 1,
    "w": "Indexing computes an address and jumps to it, taking the same time whether the array holds ten items or ten million."
   },
   {
    "t": "For n = 20, an O(n^2) algorithm may well beat an O(n log n) one. Why?",
    "o": [
     "Big-O is wrong",
     "Big-O drops constants, and at small n those constants dominate",
     "O(n log n) is only for sorted data",
     "It cannot happen"
    ],
    "a": 1,
    "w": "Asymptotic notation describes behaviour as n grows large. This is exactly why real sort implementations switch to insertion sort for small partitions."
   }
  ]
 },
 {
  "path": "dsa/binary_search.html",
  "title": "Binary Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Binary search on unsorted data:",
    "o": [
     "Raises an error",
     "Returns the wrong answer without complaining",
     "Falls back to a linear scan",
     "Sorts the data first"
    ],
    "a": 1,
    "w": "Nothing checks the precondition. It compares against the middle, discards a half on the strength of that comparison, and returns something plausible - which is far more dangerous than a crash."
   },
   {
    "t": "Why is the midpoint written mid = lo + (hi - lo) // 2?",
    "o": [
     "It is faster",
     "It avoids overflow when lo + hi is large",
     "It rounds differently",
     "It handles empty lists"
    ],
    "a": 1,
    "w": "Arithmetically identical to (lo + hi) // 2, but that form overflows in fixed-width integers. The bug lived in the JDK's binary search for nine years."
   },
   {
    "t": "Change hi = mid - 1 to hi = mid and run the program. What happens?",
    "o": [
     "It returns the wrong index",
     "It skips the last element",
     "It loops forever and the interpreter kills it",
     "Nothing - both are correct"
    ],
    "a": 2,
    "w": "mid has already been compared and ruled out. Leaving it in the window means a two-item window stops shrinking, so the loop never ends."
   }
  ]
 },
 {
  "path": "dsa/binary_search_trees.html",
  "title": "Binary Search Trees",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Inserting sorted keys into a plain BST produces:",
    "o": [
     "A balanced tree",
     "A tree of height n - effectively a linked list",
     "An error",
     "A heap"
    ],
    "a": 1,
    "w": "Every key goes right, so the tree is one spine and search degrades to O(n). The program prints height 7 for seven sorted keys."
   },
   {
    "t": "An in-order traversal of a BST emits the keys:",
    "o": [
     "In insertion order",
     "In sorted order",
     "Level by level",
     "In reverse"
    ],
    "a": 1,
    "w": "Left, self, right. It comes out sorted for free, without sorting anything - which is the structure's whole selling point over a hash table."
   },
   {
    "t": "Deleting a node with two children works by:",
    "o": [
     "Deleting both subtrees",
     "Copying up the in-order successor and deleting that instead",
     "Rotating the tree",
     "Marking it deleted"
    ],
    "a": 1,
    "w": "The leftmost node of the right subtree has at most one child, so the hard case reduces to an easy one."
   }
  ]
 },
 {
  "path": "dsa/breadth_first_search.html",
  "title": "Breadth First Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Turning BFS into DFS requires changing:",
    "o": [
     "The visited set",
     "popleft() to pop() - the container",
     "The graph representation",
     "The order of the neighbour list"
    ],
    "a": 1,
    "w": "FIFO gives breadth-first, LIFO gives depth-first. The rest of the loop is identical, which is the clearest way to see that the container is the algorithm."
   },
   {
    "t": "Why does the code mark a node visited when it is enqueued rather than when it is dequeued?",
    "o": [
     "It is tidier",
     "Otherwise a node with several neighbours already queued gets added more than once",
     "To keep distances correct",
     "To detect cycles"
    ],
    "a": 1,
    "w": "Marking late lets the same node be queued repeatedly before it is ever processed, which blows up the queue on dense graphs."
   },
   {
    "t": "BFS gives shortest paths on an unweighted graph because:",
    "o": [
     "It uses a priority queue",
     "Nodes are dequeued in order of distance, so the first arrival is by a shortest path",
     "It visits every node",
     "It sorts the neighbours"
    ],
    "a": 1,
    "w": "The frontier expands one full level at a time. On weighted graphs that no longer holds and you need Dijkstra."
   }
  ]
 },
 {
  "path": "dsa/bubble_sort.html",
  "title": "Bubble Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does the swapped flag buy?",
    "o": [
     "Fewer swaps",
     "A best case of O(n) on sorted input",
     "Stability",
     "Less memory"
    ],
    "a": 1,
    "w": "A pass with no swaps proves the list is sorted, so it stops. Without it, sorted input still costs the full n passes."
   },
   {
    "t": "Why does the inner loop run to n - 1 - i rather than n - 1?",
    "o": [
     "To avoid an index error",
     "Because after pass i the last i items are already final",
     "To keep it stable",
     "It makes it O(n)"
    ],
    "a": 1,
    "w": "Each pass carries the largest remaining value to the end, so that tail never needs looking at again. It saves comparisons, not complexity."
   },
   {
    "t": "The program's swap count for a given list equals:",
    "o": [
     "The number of items",
     "The number of passes",
     "The number of inversions in the input",
     "n log n"
    ],
    "a": 2,
    "w": "Each swap fixes exactly one inverted pair, so the totals match exactly. That is why [1,2,3,4,5,0] is so expensive - one item out of place at the wrong end is five inversions."
   }
  ]
 },
 {
  "path": "dsa/counting_sort.html",
  "title": "Counting Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "How does counting sort beat the O(n log n) lower bound?",
    "o": [
     "It is parallel",
     "It never compares two elements",
     "It uses more memory",
     "It only works on small lists"
    ],
    "a": 1,
    "w": "The bound applies to comparison sorts. Counting sort uses the value as an array index, so the proof simply does not cover it."
   },
   {
    "t": "Why does the final loop iterate over reversed(a)?",
    "o": [
     "It is faster",
     "To keep the sort stable",
     "To handle negatives",
     "To avoid an off-by-one"
    ],
    "a": 1,
    "w": "Walking backwards while decrementing before writing keeps equal items in their original order. Radix sort depends on that, so getting it wrong breaks the algorithm built on top."
   },
   {
    "t": "The program sorts [5, 100000, 3]. What is the problem?",
    "o": [
     "The list is too short",
     "The values are too far apart, so k dwarfs n",
     "It is not sorted first",
     "Counting sort cannot handle 100000"
    ],
    "a": 1,
    "w": "O(n + k) is linear only when k is comparable to n. Three items and a hundred thousand counters is the case that makes the cost obvious."
   }
  ]
 },
 {
  "path": "dsa/cycle_detection.html",
  "title": "Cycle Detection",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Floyd's tortoise and hare uses how much extra memory?",
    "o": [
     "O(n) for a visited set",
     "O(log n)",
     "O(1) - two pointers",
     "O(n) for the path"
    ],
    "a": 2,
    "w": "That is the entire point of it. A visited set also works and is easier, but it costs memory proportional to the list."
   },
   {
    "t": "Why does the comparison use 'slow is fast' rather than '==' ?",
    "o": [
     "It is faster",
     "Two different nodes holding equal values would fool ==",
     "== does not work on objects",
     "To avoid a type error"
    ],
    "a": 1,
    "w": "The question is whether the two pointers are on the same node, which is identity, not equality of contents."
   },
   {
    "t": "Why does directed-graph cycle detection need three colours rather than a plain visited set?",
    "o": [
     "To find the cycle's length",
     "Because reaching an already-finished node is fine, while reaching one still on the current path is a cycle",
     "To handle disconnected graphs",
     "To make it iterative"
    ],
    "a": 1,
    "w": "With two states, any diamond shape - two paths meeting at one node - is reported as a cycle. GREY versus BLACK is what distinguishes them."
   }
  ]
 },
 {
  "path": "dsa/depth_first_search.html",
  "title": "Depth First Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without the visited set, DFS on a graph containing a cycle:",
    "o": [
     "Returns the wrong order",
     "Recurses forever",
     "Skips some nodes",
     "Works fine"
    ],
    "a": 1,
    "w": "A graph is not a tree. The visited set is the only thing that terminates the traversal - the program adds a G to A edge to demonstrate exactly this."
   },
   {
    "t": "Why does the iterative version also check 'if node in visited' after popping?",
    "o": [
     "To avoid infinite loops",
     "A node can be pushed by several neighbours before it is popped",
     "To match the recursive order",
     "To count the nodes"
    ],
    "a": 1,
    "w": "Duplicates on the stack are harmless but wasteful; without the check the same node is expanded twice."
   },
   {
    "t": "Work that belongs on the \"leave\" line - after the recursive calls return - includes:",
    "o": [
     "Marking visited",
     "Printing the node",
     "Topological ordering and subtree sizes",
     "Choosing the start"
    ],
    "a": 2,
    "w": "Post-order work needs the whole subtree already processed. Topological sort by DFS is exactly this, reversed."
   }
  ]
 },
 {
  "path": "dsa/dijkstras.html",
  "title": "Dijkstra's Algorithm",
  "cat": "Algorithms",
  "q": [
   {
    "t": "With one negative edge, Dijkstra:",
    "o": [
     "Raises an error",
     "Loops forever",
     "Returns a wrong answer without complaining",
     "Still works"
    ],
    "a": 2,
    "w": "The program finalises C at 2, then discovers a route through B worth -2 and never revisits it. Correctness rests on no edge ever making a finalised node cheaper."
   },
   {
    "t": "Why does the code push a new heap entry instead of updating an existing one?",
    "o": [
     "It is more accurate",
     "heapq cannot decrease a key in place, so stale entries are skipped when popped",
     "To keep the heap sorted",
     "To count relaxations"
    ],
    "a": 1,
    "w": "Lazy deletion: cheaper and far easier to get right than a decrease-key structure, at the cost of a heap larger than the node count."
   },
   {
    "t": "Replacing the heap with a linear scan for the nearest node gives:",
    "o": [
     "Wrong answers",
     "The same answers at O(V²) instead of O(E log V)",
     "A faster algorithm",
     "Bellman-Ford"
    ],
    "a": 1,
    "w": "The heap is an accelerator, not part of the logic. On a dense graph the O(V²) version is actually competitive."
   }
  ]
 },
 {
  "path": "dsa/divide_and_conquer.html",
  "title": "Divide and Conquer",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Why does exponentiation by squaring make ONE recursive call and reuse the result?",
    "o": [
     "It is tidier",
     "Two calls would recompute the same value and lose the entire saving",
     "It avoids overflow",
     "Python requires it"
    ],
    "a": 1,
    "w": "power(b, n//2) * power(b, n//2) looks identical and is exponentially slower. The saving is in reusing the value, not in the halving."
   },
   {
    "t": "Counting inversions during a merge is O(n log n) because, when an item from the right half wins:",
    "o": [
     "It is discarded",
     "Every remaining item on the left is counted in one addition",
     "The halves are swapped",
     "The count is estimated"
    ],
    "a": 1,
    "w": "The left half is sorted, so all of its remainder is greater. Counting in blocks rather than pairs is the whole trick."
   },
   {
    "t": "Divide and conquer proves its answer complete by showing every case falls into:",
    "o": [
     "The base case",
     "Left, right, or across the split",
     "A sorted region",
     "One recursive call"
    ],
    "a": 1,
    "w": "Every inversion is within one half or spans both, and never anything else. That decomposition is the pattern in general, not just here."
   }
  ]
 },
 {
  "path": "dsa/dynamic_programming.html",
  "title": "Dynamic Programming",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Dynamic programming needs subproblems that:",
    "o": [
     "Are independent",
     "Overlap, so an answer is reused many times",
     "Are all the same size",
     "Can be sorted"
    ],
    "a": 1,
    "w": "If each subproblem were needed once, a table would buy nothing over plain recursion. The reuse is what pays for the storage."
   },
   {
    "t": "Top-down memoisation and bottom-up tabulation differ in that tabulation:",
    "o": [
     "Gives different answers",
     "Is always faster",
     "Fills the small cases first and uses no call stack",
     "Needs less memory"
    ],
    "a": 2,
    "w": "Same complexity, no recursion limit, and usually a better constant. Memoisation is normally the easier one to write, because the code still mirrors the recurrence."
   },
   {
    "t": "For coins [1, 3, 4] and target 6, greedy takes 4+1+1. What does the DP table give?",
    "o": [
     "The same 3 coins",
     "2 coins - two 3s",
     "4 coins",
     "It cannot be made"
    ],
    "a": 1,
    "w": "The table computes every amount up to the target, so it finds the combination greedy's one-way choice never considers."
   }
  ]
 },
 {
  "path": "dsa/fibonacci_search.html",
  "title": "Fibonacci Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does Fibonacci search avoid that binary search needs?",
    "o": [
     "Sorted input",
     "Division",
     "Extra memory",
     "Comparisons"
    ],
    "a": 1,
    "w": "The split points come from adding and subtracting Fibonacci numbers, so no division or bit-shift is required. On hardware without cheap division that mattered."
   },
   {
    "t": "Its step count compared with binary search is:",
    "o": [
     "Much better",
     "About the same - both O(log n)",
     "Much worse",
     "Depends on the target"
    ],
    "a": 1,
    "w": "Both are logarithmic and Fibonacci search is slightly worse by a constant. The win was never the step count."
   },
   {
    "t": "Why does the probe use min(offset + f2, n - 1)?",
    "o": [
     "To skip duplicates",
     "Because the covering Fibonacci number overshoots the array",
     "To keep the search stable",
     "To handle negative numbers"
    ],
    "a": 1,
    "w": "The sequence jumps 8, 13, 21 - it rarely equals the array length, so the first probe can point past the end and has to be clamped."
   }
  ]
 },
 {
  "path": "dsa/graph_representations.html",
  "title": "Graph Representations",
  "cat": "Algorithms",
  "q": [
   {
    "t": "For a sparse graph, an adjacency matrix wastes space because it stores:",
    "o": [
     "Every node twice",
     "V² cells regardless of how many edges exist",
     "The edge weights",
     "A copy of each edge list"
    ],
    "a": 1,
    "w": "The grid is allocated up front. A million users with a few hundred million friendships would need 10¹² cells to hold them."
   },
   {
    "t": "\"Is there an edge between A and D?\" is answered fastest by:",
    "o": [
     "An adjacency list",
     "An adjacency matrix",
     "An edge list",
     "All three are the same"
    ],
    "a": 1,
    "w": "One indexed read. The list has to scan A's neighbours and the edge list has to scan everything."
   },
   {
    "t": "BFS, DFS and Dijkstra all assume an adjacency list because they ask:",
    "o": [
     "\"Are these two connected?\"",
     "\"Who does this node reach?\"",
     "\"How many edges are there?\"",
     "\"Is the graph directed?\""
    ],
    "a": 1,
    "w": "Traversals iterate a node's neighbours, which a list returns directly and a matrix only finds by scanning a whole row of V cells."
   }
  ]
 },
 {
  "path": "dsa/greedy_algorithms.html",
  "title": "Greedy Algorithms",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Greedy coin change works for [1, 5, 10, 25] but fails for [1, 3, 4]. What does that show?",
    "o": [
     "Greedy never works",
     "Correctness depends on the denominations, not on the algorithm",
     "The coins must be sorted",
     "It only fails on small targets"
    ],
    "a": 1,
    "w": "Familiarity with real currency is why people assume greedy is generally optimal. Nothing about the code changed - only the input."
   },
   {
    "t": "Activity selection is provably optimal when the meetings are sorted by:",
    "o": [
     "Start time",
     "Finish time",
     "Duration",
     "Number of attendees"
    ],
    "a": 1,
    "w": "Taking the meeting that frees the room earliest can never shut out a better schedule. Sorted by start time, one long early meeting blocks several short ones."
   },
   {
    "t": "The practical way to test a greedy idea is to:",
    "o": [
     "Prove it formally first",
     "Compare it with brute force on small inputs",
     "Try it on the largest case",
     "Check the complexity"
    ],
    "a": 1,
    "w": "The program runs a DP check alongside so the verdict is computed rather than asserted. A counterexample is usually small when it exists at all."
   }
  ]
 },
 {
  "path": "dsa/hash_tables.html",
  "title": "Hash Tables and Hashing",
  "cat": "Algorithms",
  "q": [
   {
    "t": "The program replaces the hash function with 'lambda k: 1'. What happens?",
    "o": [
     "It raises an error",
     "Keys are lost",
     "Everything lands in one bucket and every lookup becomes O(n)",
     "It gets faster"
    ],
    "a": 2,
    "w": "The structure still works perfectly and every guarantee evaporates. O(1) was always conditional on the hash spreading keys out."
   },
   {
    "t": "Why does a resize have to rehash every key?",
    "o": [
     "The hashes change",
     "The index is hash % size, and size just changed",
     "To keep insertion order",
     "To free memory"
    ],
    "a": 1,
    "w": "The hash is stable; the fold into a bucket index is not. Doubling the table moves nearly everything."
   },
   {
    "t": "The load factor threshold exists because:",
    "o": [
     "Memory is limited",
     "Collisions rise sharply as the table fills, so it grows before that happens",
     "Python requires it",
     "It keeps buckets sorted"
    ],
    "a": 1,
    "w": "Past about three-quarters full the chains get long fast. Resizing is O(n), but amortised over the inserts that caused it it is O(1) each."
   }
  ]
 },
 {
  "path": "dsa/heap_sort.html",
  "title": "Heap Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "After the heapify phase, the list is:",
    "o": [
     "Sorted",
     "Reverse sorted",
     "A valid heap, which is a much weaker ordering than sorted",
     "Unchanged"
    ],
    "a": 2,
    "w": "A heap only promises each parent beats its children. Nothing is claimed about siblings - and that weakness is why it can be built in O(n)."
   },
   {
    "t": "Building the heap bottom-up, starting at the last parent, costs:",
    "o": [
     "O(n log n)",
     "O(n)",
     "O(log n)",
     "O(n²)"
    ],
    "a": 1,
    "w": "Most nodes are near the leaves and sift down barely at all. The sum works out linear, which surprises people who expect n sifts of log n each."
   },
   {
    "t": "Why does the extraction phase swap the root with the last item?",
    "o": [
     "To keep the sort stable",
     "It both removes the maximum and puts it in its final position, with no extra memory",
     "To rebalance the tree",
     "To avoid recursion"
    ],
    "a": 1,
    "w": "One swap does both jobs, which is how heap sort sorts in place. The heap then shrinks by one and is repaired with a single sift."
   }
  ]
 },
 {
  "path": "dsa/heaps_and_priority_queues.html",
  "title": "Heaps and Priority Queues",
  "cat": "Algorithms",
  "q": [
   {
    "t": "In an array-backed heap, the children of index i are at:",
    "o": [
     "i-1 and i+1",
     "2i+1 and 2i+2",
     "i/2 and i/2+1",
     "0 and n-1"
    ],
    "a": 1,
    "w": "The tree is arithmetic, not structure. No node objects and no pointers are stored at all."
   },
   {
    "t": "After several pushes, the underlying list is:",
    "o": [
     "Sorted",
     "Sorted except the last item",
     "Only guaranteed to have the smallest item at index 0",
     "In insertion order"
    ],
    "a": 2,
    "w": "A heap promises each parent beats its children and nothing about siblings. Expecting more is the usual misunderstanding."
   },
   {
    "t": "heapq.nlargest(k, data) is O(n log k) rather than O(n log n) because it:",
    "o": [
     "Sorts first",
     "Keeps a heap of only k items",
     "Uses C code",
     "Samples the data"
    ],
    "a": 1,
    "w": "For \"top 10 of a billion\" that is the difference between practical and not."
   }
  ]
 },
 {
  "path": "dsa/insertion_sort.html",
  "title": "Insertion Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Insertion sort's running time is driven by:",
    "o": [
     "The size of the list alone",
     "How many inversions the input has",
     "The largest value",
     "Whether the values are unique"
    ],
    "a": 1,
    "w": "Each shift fixes one inversion, so a nearly sorted list is nearly free. \"Nearly sorted\" is a measurable quantity here, not a vague description."
   },
   {
    "t": "Why does the inner loop shift items rather than swap them?",
    "o": [
     "Swapping would be wrong",
     "A shift is one write instead of three",
     "It keeps the sort stable",
     "It avoids recursion"
    ],
    "a": 1,
    "w": "The item being placed is held in key, so the hole can simply be moved. That constant-factor saving is why insertion sort beats bubble sort in practice."
   },
   {
    "t": "Real sort implementations switch to insertion sort for small partitions because:",
    "o": [
     "It is stable",
     "It uses no extra memory",
     "Its constant factor is small, and big-O ignores constants",
     "It is easier to write"
    ],
    "a": 2,
    "w": "At n around 16 the O(n²) with a tiny constant beats the O(n log n) with a heavier one. CPython's own sort does exactly this."
   }
  ]
 },
 {
  "path": "dsa/interpolation_search.html",
  "title": "Interpolation Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Interpolation search improves on binary search by:",
    "o": [
     "Sorting as it goes",
     "Guessing where the target should be from its value",
     "Checking both ends first",
     "Using a hash of the target"
    ],
    "a": 1,
    "w": "It interpolates a position from the value's distance between the endpoints, instead of always probing the middle. That one line is the whole difference."
   },
   {
    "t": "The program runs it on [1,2,3,4,5,6,7,8,9,5000] looking for 9. Why does it take so many steps?",
    "o": [
     "The list is too short",
     "9 is not in the list",
     "The outlier flattens the estimate, so the probe advances one index at a time",
     "It has to sort first"
    ],
    "a": 2,
    "w": "The computed fraction is nearly zero because 5000 dominates the value range, so each probe lands next to the previous one and the search degenerates to O(n)."
   },
   {
    "t": "Its O(log log n) figure assumes the data is:",
    "o": [
     "Sorted only",
     "Sorted and roughly uniformly distributed",
     "All positive",
     "In a contiguous array"
    ],
    "a": 1,
    "w": "Sortedness alone is not enough - the estimate is a straight-line guess, so it needs the values to rise at a roughly steady rate."
   }
  ]
 },
 {
  "path": "dsa/kmp_string_matching.html",
  "title": "KMP String Matching",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does lps[i] store?",
    "o": [
     "The character at i",
     "The length of the longest proper prefix of pattern[:i+1] that is also its suffix",
     "The number of matches so far",
     "The next index to check"
    ],
    "a": 1,
    "w": "That overlap is the only information needed to know how far the pattern may safely slide after a mismatch."
   },
   {
    "t": "In the search loop, what never happens?",
    "o": [
     "j decreases",
     "i decreases",
     "The pattern slides",
     "A hit"
    ],
    "a": 1,
    "w": "The text index only moves forward, which is the O(n + m) guarantee. Naive matching restarts at i - j + 1 and re-reads characters."
   },
   {
    "t": "After a full match, the code sets j = lps[j - 1] rather than 0. Why?",
    "o": [
     "To reset faster",
     "To find overlapping occurrences",
     "To avoid an index error",
     "To count the matches"
    ],
    "a": 1,
    "w": "Set it to 0 and searching \"aa\" in \"aaaa\" reports fewer matches than there are."
   }
  ]
 },
 {
  "path": "dsa/linear_search.html",
  "title": "Linear Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Linear search needs the data to be:",
    "o": [
     "Sorted",
     "Numeric",
     "Nothing in particular - any sequence",
     "Stored in a hash table"
    ],
    "a": 2,
    "w": "It compares each item in turn, so it has no precondition at all. That is its one real advantage: every faster search buys its speed with an assumption about the data."
   },
   {
    "t": "The program prints an average of comparisons over every value in the list. What does it land on?",
    "o": [
     "n",
     "(n + 1) / 2",
     "log n",
     "n / 4"
    ],
    "a": 1,
    "w": "Finding item i takes i + 1 comparisons, and averaged over all positions that is (n + 1) / 2 - about half the list, which is where the usual rule of thumb comes from."
   },
   {
    "t": "Which case costs the full n comparisons?",
    "o": [
     "Only the last item",
     "Only a missing item",
     "Both the last item and a missing item",
     "Neither"
    ],
    "a": 2,
    "w": "The loop only stops early on a hit. A miss has to rule out every element, so failure always costs the worst case."
   }
  ]
 },
 {
  "path": "dsa/linked_lists.html",
  "title": "Linked Lists",
  "cat": "Algorithms",
  "q": [
   {
    "t": "In reverse(), why is 'nxt = node.next' saved before 'node.next = prev'?",
    "o": [
     "For readability",
     "Otherwise the rest of the list becomes unreachable",
     "To count the nodes",
     "To handle the empty list"
    ],
    "a": 1,
    "w": "Overwriting the only pointer to the remainder loses it - not corrupted, just gone. Delete the line and the list comes back one node long."
   },
   {
    "t": "What is the dummy head in delete() for?",
    "o": [
     "Marking the end",
     "Removing the special case of deleting the first node",
     "Counting nodes",
     "Making it doubly linked"
    ],
    "a": 1,
    "w": "Without a previous node to re-point, deleting the head needs its own branch - and that branch is where the bug always is."
   },
   {
    "t": "Compared with a Python list, a linked list is better at:",
    "o": [
     "Random access",
     "Inserting at the front",
     "Memory use",
     "Cache behaviour"
    ],
    "a": 1,
    "w": "O(1) with no shifting. It loses on everything else, including sequential scans, because the nodes are scattered in memory."
   }
  ]
 },
 {
  "path": "dsa/merge_sort.html",
  "title": "Merge Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Where does the actual sorting happen in merge sort?",
    "o": [
     "In the split",
     "In the merge",
     "In the base case",
     "In the recursion"
    ],
    "a": 1,
    "w": "Splitting a list in half is positional and does no comparing. All the ordering work is in combining two sorted halves."
   },
   {
    "t": "In merge, why is the comparison left[i] <= right[j] rather than < ?",
    "o": [
     "It is faster",
     "It keeps the sort stable",
     "It avoids an index error",
     "It handles empty lists"
    ],
    "a": 1,
    "w": "On a tie the left half wins, and the left half held the earlier items. Changing it to < breaks stability silently, with no other visible symptom."
   },
   {
    "t": "Merge sort's worst case compared with its best case:",
    "o": [
     "Much worse",
     "Slightly worse",
     "The same - O(n log n) either way",
     "Depends on the pivot"
    ],
    "a": 2,
    "w": "It has no pivot to choose badly and no early exit to hit. That predictability is exactly why it is used where worst-case latency matters."
   }
  ]
 },
 {
  "path": "dsa/minimum_spanning_tree.html",
  "title": "Minimum Spanning Tree",
  "cat": "Algorithms",
  "q": [
   {
    "t": "A spanning tree of a graph with V nodes always has:",
    "o": [
     "V edges",
     "V - 1 edges",
     "E - V edges",
     "As few as possible"
    ],
    "a": 1,
    "w": "Exactly enough to connect everything with no cycle. Both Kruskal and Prim stop at that count in the program."
   },
   {
    "t": "The difference between Kruskal and Prim is that Kruskal:",
    "o": [
     "Is faster",
     "Sorts all edges globally, while Prim only considers edges leaving the tree it has grown",
     "Handles negative weights",
     "Needs a starting node"
    ],
    "a": 1,
    "w": "Kruskal works from a global sort and needs union-find to reject cycles; Prim grows locally from one node with a priority queue."
   },
   {
    "t": "Kruskal uses union-find to:",
    "o": [
     "Sort the edges",
     "Track the tree's weight",
     "Check in near-constant time whether an edge would close a cycle",
     "Find the starting node"
    ],
    "a": 2,
    "w": "Both endpoints already in the same component means the edge adds only a cycle. Without union-find that check would need a traversal per edge."
   }
  ]
 },
 {
  "path": "dsa/dictionaries_in_python.html",
  "title": "Python Dictionary Lab",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Why must dictionary keys be hashable?",
    "o": [
     "To keep them sorted",
     "Because a key that changed after insertion would no longer hash to the slot it lives in",
     "To save memory",
     "To allow duplicates"
    ],
    "a": 1,
    "w": "It would become unreachable. In practice this means immutable: tuples work as keys, lists do not."
   },
   {
    "t": "{1: 'a', 1.0: 'b', True: 'c'} produces a dict with how many entries?",
    "o": [
     "3",
     "2",
     "1",
     "It raises an error"
    ],
    "a": 2,
    "w": "1 == 1.0 == True and all three hash identically, so each assignment overwrites the previous value while the first key object stays."
   },
   {
    "t": "Replacing 'x in a_big_list' with 'x in a_big_set' changes the cost from:",
    "o": [
     "O(1) to O(n)",
     "O(n) to roughly O(1)",
     "O(log n) to O(1)",
     "Nothing changes"
    ],
    "a": 1,
    "w": "The list compares against every element; the hash table computes where the answer would be. It is the highest-value one-line optimisation in most beginner Python."
   }
  ]
 },
 {
  "path": "dsa/lists_in_python.html",
  "title": "Python List Lab",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Indexing a Python list is O(1) because the list stores:",
    "o": [
     "A hash of each item",
     "References contiguously, so the address is computed",
     "The items in sorted order",
     "A linked chain of nodes"
    ],
    "a": 1,
    "w": "One multiplication and one read. This is the whole difference between a list and a linked list."
   },
   {
    "t": "What does [[0] * 3] * 3 build?",
    "o": [
     "A 3x3 grid of independent rows",
     "Three references to one row, so writing to one writes to all",
     "A flat list of nine zeros",
     "An error"
    ],
    "a": 1,
    "w": "Multiplying repeats the reference, not the object. This is the most common Python bug in grid and matrix code."
   },
   {
    "t": "sys.getsizeof shows a list's size jumping in steps rather than per item because:",
    "o": [
     "The report is approximate",
     "CPython over-allocates on growth so most appends need no reallocation",
     "Items vary in size",
     "Small lists are cached"
    ],
    "a": 1,
    "w": "That is what \"amortised O(1) append\" means concretely: most appends are free, and occasionally one pays for a copy."
   }
  ]
 },
 {
  "path": "dsa/strings_in_python.html",
  "title": "Python String Lab",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Building a string by += in a loop is O(n²) because each step:",
    "o": [
     "Reallocates the list",
     "Allocates a new string and copies everything so far",
     "Re-encodes to UTF-8",
     "Sorts the characters"
    ],
    "a": 1,
    "w": "Strings are immutable, so there is nothing to append to. \"\".join(parts) does one length calculation, one allocation and one copy."
   },
   {
    "t": "The program accumulates into an object attribute rather than a local variable. Why?",
    "o": [
     "It is more realistic",
     "CPython has an in-place resize special case for locals that would hide the quadratic",
     "Locals are faster",
     "To avoid a NameError"
    ],
    "a": 1,
    "w": "The optimisation only fires under specific conditions and varies by build - which is itself the argument for using join rather than relying on it."
   },
   {
    "t": "Immutability is also what allows strings to be:",
    "o": [
     "Sliced",
     "Used as dictionary keys",
     "Concatenated",
     "Iterated"
    ],
    "a": 1,
    "w": "Hashability requires that the value cannot change underneath the table. A mutable string could not be a key."
   }
  ]
 },
 {
  "path": "dsa/queues.html",
  "title": "Queues (FIFO)",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Why is a queue built on list.pop(0) slow?",
    "o": [
     "Lists cannot grow",
     "Removing the first item shifts every remaining item one place left",
     "It copies the list",
     "It is not slow"
    ],
    "a": 1,
    "w": "O(n) per dequeue, so O(n²) to drain the queue. The program times 30,000 dequeues both ways."
   },
   {
    "t": "collections.deque gives O(1) at both ends because it is:",
    "o": [
     "A sorted array",
     "A doubly linked list of blocks",
     "A hash table",
     "A binary heap"
    ],
    "a": 1,
    "w": "There is no contiguous array to shift, so appending or popping at either end is a pointer update."
   },
   {
    "t": "A circular buffer must track its size separately because:",
    "o": [
     "It grows",
     "Head meeting tail is ambiguous between full and empty",
     "The modulo is expensive",
     "It stores None"
    ],
    "a": 1,
    "w": "Both states have head == tail. Getting this wrong silently overwrites the oldest entry."
   }
  ]
 },
 {
  "path": "dsa/quick_sort.html",
  "title": "Quick Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "With a last-element pivot, which input is quicksort's worst case?",
    "o": [
     "Random data",
     "Already sorted data",
     "Data with duplicates",
     "Very short lists"
    ],
    "a": 1,
    "w": "Each partition peels off one element instead of halving, so the recursion goes n deep. The program prints depth 8 for a sorted 9-item list against 4 for a shuffled one."
   },
   {
    "t": "After partition returns p, why do the recursive calls skip index p?",
    "o": [
     "To save a comparison",
     "The pivot is already in its final sorted position",
     "To keep the sort stable",
     "To avoid infinite recursion"
    ],
    "a": 1,
    "w": "Everything left of p is smaller and everything right is larger, so p cannot move again. That is the one guaranteed piece of progress each partition makes."
   },
   {
    "t": "Quicksort's advantage over merge sort is mainly:",
    "o": [
     "Better worst case",
     "Stability",
     "It sorts in place, needing O(log n) extra space rather than O(n)",
     "Fewer comparisons"
    ],
    "a": 2,
    "w": "Its worst case is worse and it is not stable. The memory profile, plus good cache behaviour, is what keeps it in use."
   }
  ]
 },
 {
  "path": "dsa/radix_sort.html",
  "title": "Radix Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Why must each digit pass be stable?",
    "o": [
     "To keep it fast",
     "Otherwise the previous pass's ordering is destroyed",
     "To handle negative numbers",
     "It does not have to be"
    ],
    "a": 1,
    "w": "Sorting by tens must preserve the ones ordering among items with equal tens digits. An unstable pass silently produces a wrong final answer."
   },
   {
    "t": "Radix sort's cost is O(d · n), where d is:",
    "o": [
     "The number of items",
     "The number of digits in the largest value",
     "The number of distinct values",
     "log n"
    ],
    "a": 1,
    "w": "One pass per digit position, each pass linear in n. Adding a single very wide value adds passes over the entire list."
   },
   {
    "t": "After only the ones-digit pass, the list:",
    "o": [
     "Is sorted",
     "Is sorted by last digit and otherwise scrambled",
     "Is unchanged",
     "Is reverse sorted"
    ],
    "a": 1,
    "w": "Every intermediate state looks broken, which is what makes LSD radix sort hard to debug by eye. Only the final pass makes it correct."
   }
  ]
 },
 {
  "path": "dsa/recursion_and_call_stack.html",
  "title": "Recursion and the Call Stack",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does a stack frame hold?",
    "o": [
     "The function's source",
     "Its arguments, its locals and where to return to",
     "The whole call tree",
     "Only the return value"
    ],
    "a": 1,
    "w": "That is why recursion depth is a memory cost: a thousand pending calls means a thousand of these alive at once."
   },
   {
    "t": "In 'return n * factorial(n - 1)', why can the frame not be discarded at the recursive call?",
    "o": [
     "Python does not support it",
     "The multiplication still has to happen after the call returns",
     "The argument might change",
     "It is discarded"
    ],
    "a": 1,
    "w": "Pending work after the call is exactly what keeps a frame alive. Writing it so the call is the last thing done is tail recursion - which CPython still will not optimise away."
   },
   {
    "t": "The program prints call counts for naive fib. What is the shape?",
    "o": [
     "Linear in n",
     "Roughly doubling for each +1 in n",
     "n log n",
     "Constant"
    ],
    "a": 1,
    "w": "177 calls for fib(10) and 242,785 for fib(25). Recursion is not slow; recursion that recomputes the same subproblems is."
   }
  ]
 },
 {
  "path": "dsa/selection_sort.html",
  "title": "Selection Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "How many comparisons does selection sort make on an already sorted list of n items?",
    "o": [
     "n - 1",
     "About n log n",
     "The same n(n-1)/2 as always",
     "0"
    ],
    "a": 2,
    "w": "There is no early exit available: you cannot know an item is the minimum without checking every remaining one. The count is fixed by n alone."
   },
   {
    "t": "What selection sort is genuinely good at:",
    "o": [
     "Nearly sorted data",
     "Making at most n - 1 swaps",
     "Being stable",
     "Large datasets"
    ],
    "a": 1,
    "w": "One swap per position, whatever the input. Where writes are expensive - flash memory, or records much larger than the key - that is a real advantage."
   },
   {
    "t": "Sorting [2, 2, 1] with this implementation:",
    "o": [
     "Keeps the two 2s in their original order",
     "Swaps their order, so the sort is not stable",
     "Raises an error",
     "Skips the duplicate"
    ],
    "a": 1,
    "w": "The first 2 is swapped with the 1 at the far end, jumping it past the second 2. Selection sort is not stable; insertion sort is."
   }
  ]
 },
 {
  "path": "dsa/sliding_window.html",
  "title": "Sliding Window",
  "cat": "Algorithms",
  "q": [
   {
    "t": "The fixed-size window updates its sum with one line. Which?",
    "o": [
     "total = sum(window)",
     "total += a[i] - a[i - k]",
     "total = max(total, a[i])",
     "total *= 2"
    ],
    "a": 1,
    "w": "Add what entered, subtract what left. Carrying the value forward instead of rebuilding it is what turns O(n·k) into O(n)."
   },
   {
    "t": "In the longest-unique-substring window, why is the check 'ch in seen and seen[ch] >= start' rather than just 'ch in seen'?",
    "o": [
     "To handle the first character",
     "An earlier occurrence may already have fallen off the left edge",
     "To count repeats",
     "To keep it O(n)"
    ],
    "a": 1,
    "w": "Only a repeat inside the current window matters. Drop the second condition and \"abba\" gives the wrong answer."
   },
   {
    "t": "Storing the last index of each character rather than a count lets the left edge:",
    "o": [
     "Move backwards",
     "Jump straight past the previous occurrence",
     "Stay fixed",
     "Be recomputed"
    ],
    "a": 1,
    "w": "Both approaches are correct; jumping keeps the scan clearly linear and the code short."
   }
  ]
 },
 {
  "path": "dsa/stacks.html",
  "title": "Stacks (LIFO)",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Why does the balanced-brackets check test that the stack is empty at the end?",
    "o": [
     "To free memory",
     "To catch openers that were never closed",
     "To reset for the next call",
     "It is not necessary"
    ],
    "a": 1,
    "w": "\"((()\" has every closer matched and is still unbalanced. Without the final check it passes."
   },
   {
    "t": "In the postfix evaluator, why is it 'b, a = stack.pop(), stack.pop()' in that order?",
    "o": [
     "It reads better",
     "The second operand was pushed last, so it comes off first",
     "To avoid an index error",
     "The order does not matter"
    ],
    "a": 1,
    "w": "Swap the names and + and * still look right while - and / silently invert - the worst kind of bug to find."
   },
   {
    "t": "A stack built on a Python list uses append and pop with no index because:",
    "o": [
     "It is more readable",
     "Both act on the end, so both are O(1)",
     "pop(0) is not allowed",
     "It keeps the order correct"
    ],
    "a": 1,
    "w": "insert(0, x) and pop(0) shift every other element. Same stack, every operation turned into O(n)."
   }
  ]
 },
 {
  "path": "dsa/topological_sort.html",
  "title": "Topological Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Kahn's algorithm starts from the nodes whose in-degree is:",
    "o": [
     "Highest",
     "Zero",
     "One",
     "Equal to their out-degree"
    ],
    "a": 1,
    "w": "In-degree zero means nothing has to happen first, so those can be taken immediately - and in any order among themselves."
   },
   {
    "t": "The program detects a cycle by noticing that:",
    "o": [
     "A node repeats",
     "The output is shorter than the node count",
     "The queue empties",
     "An in-degree goes negative"
    ],
    "a": 1,
    "w": "Nodes in a cycle wait on each other forever, so their in-degree never reaches zero and they never enter the queue. The short output is the detection - it costs nothing extra."
   },
   {
    "t": "A directed acyclic graph has:",
    "o": [
     "Exactly one topological order",
     "Usually many valid topological orders",
     "None unless it is a tree",
     "One per starting node"
    ],
    "a": 1,
    "w": "Swapping popleft() for pop() produces a different, equally correct order. Where a specific one is needed, a heap gives the lexicographically smallest."
   }
  ]
 },
 {
  "path": "dsa/trie_prefix_tree.html",
  "title": "Trie (Prefix Tree)",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does the is_word flag distinguish?",
    "o": [
     "Leaves from internal nodes",
     "\"ca\", which is only a prefix, from \"do\", which is a stored word with more beyond it",
     "Uppercase from lowercase",
     "Full from partial branches"
    ],
    "a": 1,
    "w": "Without it a trie can only answer prefix questions - and \"do\" being a word while \"dog\" continues past it has nothing to do with being a leaf."
   },
   {
    "t": "Trie lookup costs O(length of the word) because:",
    "o": [
     "The words are sorted",
     "It walks one node per character, and the number of stored words never enters into it",
     "Hashing is O(1)",
     "It is a balanced tree"
    ],
    "a": 1,
    "w": "A million stored words cost the same as ten. A hash table is also roughly O(length), because it must hash the whole string."
   },
   {
    "t": "The operation a hash table cannot do at all is:",
    "o": [
     "Exact lookup",
     "Insert",
     "List everything starting with \"car\"",
     "Delete"
    ],
    "a": 2,
    "w": "Hashing destroys the relationship between \"car\" and \"card\". Autocomplete is a DFS from the prefix node, which needs the shared structure a trie keeps."
   }
  ]
 },
 {
  "path": "dsa/two_pointers.html",
  "title": "Two Pointers",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Pair-sum with two pointers requires the list to be:",
    "o": [
     "Unique",
     "Sorted",
     "Positive",
     "Even length"
    ],
    "a": 1,
    "w": "Moving a pointer is only justified because sortedness proves the discarded element cannot be part of any solution. Shuffle the input and it returns None for a pair that exists."
   },
   {
    "t": "When the sum is too small, why is it safe to move lo right rather than hi left?",
    "o": [
     "It is arbitrary",
     "a[hi] is the largest available partner, so a[lo] cannot work with anything",
     "It keeps the loop terminating",
     "hi might be negative"
    ],
    "a": 1,
    "w": "Each step eliminates a whole row or column of the pair table, which is how n² candidates are covered in n steps."
   },
   {
    "t": "In the in-place dedupe, why does the function return a length instead of a list?",
    "o": [
     "It is faster",
     "Nothing was reallocated, so the tail still holds stale data",
     "The list is sorted",
     "To avoid copying"
    ],
    "a": 1,
    "w": "The point of the technique is O(1) extra memory. The caller uses a[:n] and ignores whatever is past it."
   }
  ]
 },
 {
  "path": "dsa/union_find.html",
  "title": "Union-Find (Disjoint Set)",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does path compression do?",
    "o": [
     "Removes duplicate elements",
     "Re-points every node touched on the way up straight at the root",
     "Merges the two smallest trees",
     "Sorts the parent array"
    ],
    "a": 1,
    "w": "The walk pays for the next walk. Every node on the path becomes one hop from the root, so repeat queries are effectively free."
   },
   {
    "t": "Union by rank exists to prevent:",
    "o": [
     "Duplicate unions",
     "Trees degenerating into long chains",
     "Cycles",
     "Memory growth"
    ],
    "a": 1,
    "w": "Attaching blindly, as the naive version does, builds a linked list wearing a tree's name - and find degrades to O(n), which the program's hop counts show directly."
   },
   {
    "t": "With both optimisations, the amortised cost per operation is:",
    "o": [
     "O(log n)",
     "O(1) exactly",
     "O(α(n)), which is below 5 for any real n",
     "O(n)"
    ],
    "a": 2,
    "w": "The inverse Ackermann function grows so slowly that it is a constant for practical purposes - but it is not literally O(1)."
   }
  ]
 },
 {
  "path": "computer_vision/one_by_one_convolutions.html",
  "title": "1x1 Convolutions",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does a 1x1 convolution actually combine?",
    "o": [
     "A pixel and its eight neighbours",
     "All the channels at a single spatial position",
     "Every pixel in the feature map",
     "Two adjacent channels"
    ],
    "a": 1,
    "w": "It has no spatial extent, so it never touches neighbours. At each position it takes a weighted sum across the whole channel stack, and repeats that with shared weights everywhere."
   },
   {
    "t": "Why does a ResNet bottleneck put 1x1 convolutions around the 3x3?",
    "o": [
     "To increase the receptive field",
     "So the expensive 3x3 runs on far fewer channels",
     "To normalise the activations",
     "To downsample the spatial dimensions"
    ],
    "a": 1,
    "w": "The 3x3 cost scales with Cin x Cout. Reducing to 64 channels first and expanding after cuts a 590,000-weight block to about 70,000 for the same input and output shape."
   },
   {
    "t": "What happens to two stacked 1x1 convolutions with no activation between them?",
    "o": [
     "They double the receptive field",
     "They collapse into a single linear map",
     "They cannot be trained",
     "They become a 2x2 convolution"
    ],
    "a": 1,
    "w": "Each is a matrix multiplication at every position. Two matrices multiplied together are one matrix, so the pair has exactly the representational power of one layer."
   }
  ]
 },
 {
  "path": "computer_vision/affine_transforms.html",
  "title": "Affine Transforms",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does the determinant ad - bc of an affine transform tell you?",
    "o": [
     "The rotation angle",
     "The factor by which area is scaled",
     "The translation distance",
     "The number of pixels lost"
    ],
    "a": 1,
    "w": "A pure rotation has determinant 1 because area is unchanged. Negative means the image was flipped, and zero means the plane has collapsed onto a line and nothing can invert it."
   },
   {
    "t": "Why do implementations iterate over output pixels and apply the inverse transform?",
    "o": [
     "It is faster",
     "Iterating forwards leaves unwritten holes when the transform enlarges",
     "The forward transform is not defined",
     "It avoids needing interpolation"
    ],
    "a": 1,
    "w": "Forward mapping scatters input pixels to output positions, leaving gaps under enlargement and collisions under shrinking. Backward mapping writes every output pixel exactly once."
   },
   {
    "t": "Which of these is NOT an affine transform?",
    "o": [
     "Rotation",
     "Shear",
     "Perspective correction of a tilted photograph",
     "Uniform scaling"
    ],
    "a": 2,
    "w": "Affine transforms keep parallel lines parallel. Perspective makes parallel lines converge, so it needs a projective transform with eight parameters instead of six."
   }
  ]
 },
 {
  "path": "computer_vision/anchor_boxes.html",
  "title": "Anchor Boxes",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does the network predict for each anchor?",
    "o": [
     "Absolute box coordinates",
     "An offset from that anchor, plus whether an object is present",
     "A segmentation mask",
     "The class only"
    ],
    "a": 1,
    "w": "Regressing a small correction to a known reference box is far easier than producing coordinates from nothing, and it makes the output a fixed-size tensor."
   },
   {
    "t": "Why do anchors with middling IoU get ignored rather than labelled?",
    "o": [
     "To save computation",
     "They are genuinely ambiguous, and forcing them either way teaches the network something untrue",
     "They are duplicates",
     "IoU cannot be computed for them"
    ],
    "a": 1,
    "w": "An anchor at IoU 0.4 neither clearly covers the object nor clearly misses it. The ignore band keeps that ambiguity out of the loss."
   },
   {
    "t": "Why does focal loss exist?",
    "o": [
     "To speed up training",
     "Because tens of thousands of anchors are negative, so easy background dominates the loss",
     "To handle overlapping boxes",
     "To replace IoU"
    ],
    "a": 1,
    "w": "It down-weights examples the model already classifies correctly, which is what let one-stage detectors match two-stage ones."
   }
  ]
 },
 {
  "path": "computer_vision/blur_gaussian_median_bilateral.html",
  "title": "Blur: Gaussian, Median and Bilateral",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Why does a Gaussian blur fail to remove salt-and-pepper noise?",
    "o": [
     "The radius is always too small",
     "A mean includes the outlier, so it is spread rather than removed",
     "It only works on colour images",
     "Gaussian weights are negative"
    ],
    "a": 1,
    "w": "Averaging incorporates every value it is given. A pixel at 255 among neighbours at 40 pulls the mean up, turning one bright dot into a larger dim smudge."
   },
   {
    "t": "Why does the median filter remove an outlier completely?",
    "o": [
     "It clamps values to a range",
     "An extreme value sorts to one end and is never the middle element",
     "It replaces outliers with zero",
     "It detects outliers explicitly"
    ],
    "a": 1,
    "w": "The output is whichever value sits in the middle of the sorted neighbourhood. An extreme value is at an end by definition, so it is simply never selected."
   },
   {
    "t": "What happens to a bilateral filter as its range sigma grows very large?",
    "o": [
     "It becomes an ordinary Gaussian blur",
     "It stops doing anything",
     "It becomes a median filter",
     "It sharpens the image"
    ],
    "a": 0,
    "w": "A large range sigma means the similarity term stops discriminating between neighbours, so only the spatial term is left - which is exactly a Gaussian blur."
   }
  ]
 },
 {
  "path": "computer_vision/cnn.html",
  "title": "CNN Architecture",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “The Convolutional Layer”?",
    "ans": "The core building block of a CNN is the Convolution Operation . Instead of connecting every input pixel to every hidden node (which is computationally impossible for large images), a small matrix called a kernel or filter (e.g., 3x3) slides across the input image."
   },
   {
    "t": "What does this module say about “Activation (ReLU)”?",
    "ans": "After convolution, we introduce non-linearity using an activation function, typically the Rectified Linear Unit (ReLU) . This function simply zeroes out negative values and passes positive values through unchanged:"
   },
   {
    "t": "What does this module say about “Pooling (Downsampling)”?",
    "ans": "Following activation, Max Pooling layers reduce the spatial dimensions of the feature maps. A common strategy is taking the maximum value over a 2x2 window with a stride of 2."
   }
  ]
 },
 {
  "path": "computer_vision/calculating_parameters_in_cnn.html",
  "title": "Calculating Parameters in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “Flatten-then-dense is where parameters explode” here?",
    "ans": "Global average pooling is the standard fix."
   },
   {
    "t": "What is meant by “Doubling the channels roughly quadruples that layer's parameters,” here?",
    "ans": "because both C_in and C_out appear in the formula."
   },
   {
    "t": "What is meant by “Early layers cost compute; late layers cost parameters” here?",
    "ans": "Optimise the right one for your constraint."
   },
   {
    "t": "What is meant by “More parameters is not more capacity in any useful sense” here?",
    "ans": "if they sit in a badly placed dense layer."
   }
  ]
 },
 {
  "path": "computer_vision/colour_spaces_rgb_hsv.html",
  "title": "Colour Spaces: RGB and HSV",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Why is selecting 'anything red' easier in HSV than in RGB?",
    "o": [
     "HSV uses fewer numbers",
     "Hue holds the colour alone, so one range covers dark, pale and vivid reds",
     "RGB cannot represent red",
     "HSV is higher precision"
    ],
    "a": 1,
    "w": "In RGB, brightness and purity change all three channels, so a red range is three coupled conditions. In HSV the colour is one number and lighting mostly moves the other two."
   },
   {
    "t": "Why should a hue mask usually also require a minimum saturation?",
    "o": [
     "To make it faster",
     "Near-grey pixels have an unstable, essentially arbitrary hue",
     "Saturation is more accurate than hue",
     "Hue is undefined above 180"
    ],
    "a": 1,
    "w": "When R, G and B are nearly equal, the hue angle is decided by tiny differences and jumps around. Requiring real saturation means requiring a definite colour."
   },
   {
    "t": "What breaks a naive `10 < hue < 350` test for red?",
    "o": [
     "Hue is circular and red straddles 0",
     "The range is too wide",
     "Hue is stored as a float",
     "Red has no hue"
    ],
    "a": 0,
    "w": "That test selects everything except red. Because the hue axis wraps, red needs two ranges - near 0 and near 360 - or a rotation of the axis first."
   }
  ]
 },
 {
  "path": "computer_vision/convolution_kernels.html",
  "title": "Convolution Kernels by Hand",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "A kernel's nine weights sum to zero. What does its output look like on a flat, uniform region?",
    "o": [
     "White",
     "Black or mid-grey",
     "Unchanged",
     "Inverted"
    ],
    "a": 1,
    "w": "On a flat region every neighbour has the same value, so the weighted sum is that value times zero, which is zero. Displays usually add 128, giving the familiar flat grey."
   },
   {
    "t": "Why does Sobel X find vertical edges rather than horizontal ones?",
    "o": [
     "It scans the image column by column",
     "It subtracts the left column from the right, and only a vertical edge makes those differ",
     "It is applied after a rotation",
     "It uses larger weights"
    ],
    "a": 1,
    "w": "Across a horizontal edge the left and right columns are identical, so the difference is zero. Only a change in the horizontal direction survives."
   },
   {
    "t": "What is the only real difference between this and a CNN's convolutional layer?",
    "o": [
     "The CNN uses a different arithmetic operation",
     "The CNN's kernel weights are learned rather than chosen",
     "The CNN works in colour",
     "The CNN does not slide the kernel"
    ],
    "a": 1,
    "w": "The operation is identical. In a CNN the nine numbers are parameters that gradient descent adjusts, which is why early layers often end up resembling edge detectors nobody designed."
   }
  ]
 },
 {
  "path": "computer_vision/feature_map_in_cnn.html",
  "title": "Convolutional Layer",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "A feature map is:",
    "o": [
     "The filter's weights",
     "The output produced by sliding one filter across the input",
     "A diagram of the architecture",
     "The final classification"
    ],
    "a": 1,
    "w": "The filter is what you slide; the feature map is what comes out - a record of where in the image that filter found what it responds to."
   },
   {
    "t": "Applying a 3x3 filter to a 32x32 image with no padding gives:",
    "o": [
     "32x32",
     "30x30",
     "34x34",
     "16x16"
    ],
    "a": 1,
    "w": "The filter cannot centre on the outermost ring of pixels, so you lose one from each side: 32 - 3 + 1 = 30. Padding exists to hold the size steady."
   },
   {
    "t": "Why do later layers have many more feature maps than early ones?",
    "o": [
     "To use up GPU memory",
     "Early layers detect a few generic patterns; later layers combine them into many specific ones",
     "Because the image gets larger",
     "To speed up training"
    ],
    "a": 1,
    "w": "There are only so many ways to be an edge. There are a great many ways to be a combination of edges, so the count of distinct useful detectors grows with depth as the spatial size shrinks."
   }
  ]
 },
 {
  "path": "computer_vision/data_loaders_in_cnn.html",
  "title": "Data Loaders in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “What is a DataLoader”?",
    "ans": "In deep learning frameworks like PyTorch or TensorFlow, a DataLoader is an utility class that handles the heavy lifting of preparing your data. Instead of writing complex loops to read images from your hard drive one by one, the DataLoader fetches the images, preprocesses them, optionally shuffles them, and groups them into perfectly sized chunks called mini-batches to feed into your CNN."
   },
   {
    "t": "What does this module say about “The Memory Problem (Why use batches?)”?",
    "ans": "Imagine you have a dataset of 1,000,000 high-resolution images. You cannot load all 1 million images into your computer's RAM (or your GPU's VRAM) at the same time—it would instantly crash with an Out-of-Memory (OOM) error."
   },
   {
    "t": "What does this module say about “On-the-fly Data Augmentation”?",
    "ans": "DataLoaders don't just load data; they are also responsible for preprocessing and augmentation . By applying random transformations (like flipping, rotating, or color shifting) to each image as it is loaded , you artificially expand your dataset size. A single image of a cat can be seen by the CNN as dozens of slightly different cats across multiple epochs, making the model highly robust and preventing overfitting."
   }
  ]
 },
 {
  "path": "computer_vision/depthwise_separable_convolution.html",
  "title": "Depthwise Separable Convolution",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does the depthwise step mix?",
    "o": [
     "Channels only",
     "Neighbours only, keeping channels separate",
     "Both",
     "Neither"
    ],
    "a": 1,
    "w": "One k x k filter per input channel, producing one output channel each. The pointwise 1x1 that follows does the channel mixing."
   },
   {
    "t": "Why does the saving approach k squared for wide layers?",
    "o": [
     "The kernel grows",
     "The ratio is 1/(1/Cout + 1/k^2), and the 1/Cout term vanishes as Cout grows",
     "Depthwise convolutions have no weights",
     "Wide layers use fewer channels"
    ],
    "a": 1,
    "w": "With many output channels the pointwise cost becomes small relative to the full convolution, leaving the k^2 factor - nine for a 3x3, 49 for a 7x7."
   },
   {
    "t": "Why is the wall-clock speed-up usually smaller than the parameter saving?",
    "o": [
     "The pointwise step dominates",
     "A depthwise convolution does little arithmetic per byte touched, so it is memory-bound",
     "It needs more layers",
     "The weights are stored differently"
    ],
    "a": 1,
    "w": "Hardware tuned for dense matrix multiplication cannot reach peak throughput on an operation that is starved of arithmetic per memory access."
   }
  ]
 },
 {
  "path": "computer_vision/dilated_convolutions.html",
  "title": "Dilated Convolutions",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "How wide does a 3x3 kernel at dilation 3 reach?",
    "o": [
     "3",
     "7",
     "9",
     "5"
    ],
    "a": 1,
    "w": "k + (k-1)(d-1) = 3 + 2*2 = 7. Nine weights spanning seven positions - the parameter count is unchanged."
   },
   {
    "t": "What causes gridding artefacts?",
    "o": [
     "Too few weights",
     "Several layers at the same dilation rate, so some input positions are never sampled by any of them",
     "Dilation larger than the kernel",
     "Missing padding"
    ],
    "a": 1,
    "w": "The taps land on the same offsets at every level, leaving positions in between unread. Varying the rate so the sampling patterns interlock is the fix."
   },
   {
    "t": "Why is dilation preferred over pooling in segmentation?",
    "o": [
     "It is faster",
     "It grows the receptive field without reducing resolution, and the output must match the input size",
     "It uses fewer weights than pooling",
     "Pooling cannot be backpropagated"
    ],
    "a": 1,
    "w": "Detail destroyed by pooling has to be reconstructed by something. Dilation buys reach while the feature map stays full size - at the cost of memory."
   }
  ]
 },
 {
  "path": "computer_vision/erosion_and_dilation.html",
  "title": "Erosion and Dilation",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Under erosion, when does a foreground pixel survive?",
    "o": [
     "When any pixel under the structuring element is foreground",
     "When every pixel under the structuring element is foreground",
     "When the majority are foreground",
     "When the centre pixel is foreground"
    ],
    "a": 1,
    "w": "Erosion is the 'every' rule. One background pixel anywhere under the element turns the centre off, which is why boundaries retreat and thin features are cut."
   },
   {
    "t": "Why does opening remove small specks without shrinking the larger shapes?",
    "o": [
     "It uses a smaller structuring element for the shapes",
     "The erosion destroys the specks, and the following dilation regrows only what survived",
     "It detects speck size first",
     "It operates on the background instead"
    ],
    "a": 1,
    "w": "Dilation can only grow what is still there. Specks removed by the erosion have nothing left to grow, while larger shapes are restored to roughly their original size."
   },
   {
    "t": "How should the structuring element be sized?",
    "o": [
     "As large as possible",
     "Larger than the artefacts to remove, smaller than the features to keep",
     "Always 3x3",
     "Equal to the image width divided by ten"
    ],
    "a": 1,
    "w": "That gap is what the operation exploits. If the artefacts and the features are close in size, no element separates them and morphology is the wrong tool."
   }
  ]
 },
 {
  "path": "computer_vision/how_dense_layer_works_in_cnn.html",
  "title": "Fully Connected Layer in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “The Transition to 1D”?",
    "ans": "Throughout the early stages of a CNN, images are processed as 2D grids (or 3D volumes with color channels). Convolutional and pooling layers extract spatial features like edges, textures, and shapes. However, to make a final classification (e.g., \"Is this a cat or a dog?\"), the network must flatten this 2D/3D data into a single 1D list of numbers. This is the input vector you see on the left."
   },
   {
    "t": "What does this module say about “Why \"Fully Connected\"”?",
    "ans": "It is called a Fully Connected (or Dense) layer because every single node in the input vector is connected to every single node in the output vector. If you have 4 inputs and 3 outputs, there are $4 \\times 3 = 12$ distinct connections (weights), plus 3 biases."
   },
   {
    "t": "What does this module say about “Where the convolutions stop and the decision starts”?",
    "ans": "Convolutional layers produce feature maps: a stack of grids saying where each learned pattern was found. That is not yet an answer to \"which of these ten classes is it?\""
   }
  ]
 },
 {
  "path": "computer_vision/global_average_pooling.html",
  "title": "Global Average Pooling against Flatten",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "How many times fewer weights does GAP need than flatten, for a 7x7 feature map?",
    "o": [
     "7",
     "49",
     "512",
     "It depends on the number of classes"
    ],
    "a": 1,
    "w": "The ratio is exactly the spatial area of the map. The number of channels and classes appear in both counts and cancel."
   },
   {
    "t": "Why can a GAP network accept any input size?",
    "o": [
     "It resizes the input",
     "The mean of a channel is one number whatever the spatial dimensions were",
     "It uses adaptive convolutions",
     "The dense layer is optional"
    ],
    "a": 1,
    "w": "A flattened network's dense layer expects exactly as many inputs as the flatten produced, which fixes the input size. Pooling removes that constraint."
   },
   {
    "t": "What does global average pooling discard?",
    "o": [
     "The channel identity",
     "Where in the feature map each activation occurred",
     "The magnitude of the activations",
     "Half the channels"
    ],
    "a": 1,
    "w": "It records that a channel fired, not where. For classification that is usually the right trade, since the convolutional layers already encode structure into which channels fire."
   }
  ]
 },
 {
  "path": "computer_vision/grad_cam.html",
  "title": "Grad-CAM",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Where does a feature map's weight come from?",
    "o": [
     "The dense layer's coefficients",
     "The gradient of the class score with respect to that map, averaged over its spatial positions",
     "The map's mean activation",
     "A learned attention head"
    ],
    "a": 1,
    "w": "It answers how much raising that map's activations would raise the class score. Getting it from gradients is what freed Grad-CAM from CAM's architectural requirement."
   },
   {
    "t": "What does the final ReLU do?",
    "o": [
     "Normalises the heatmap",
     "Discards evidence against the class, keeping only what supported it",
     "Removes negative gradients before weighting",
     "Upsamples the result"
    ],
    "a": 1,
    "w": "Drag all the weights negative and the heatmap is empty rather than inverted. Grad-CAM cannot show what argued against a prediction; run it on the competing class instead."
   },
   {
    "t": "Why is a Grad-CAM heatmap coarse?",
    "o": [
     "The gradients are approximated",
     "It has the spatial size of the last convolutional layer, often 7x7, and is interpolated up",
     "The ReLU removes detail",
     "It averages over the batch"
    ],
    "a": 1,
    "w": "The smoothness of the blob is interpolation, not evidence. It can say which seventh of the image mattered, not which pixel."
   }
  ]
 },
 {
  "path": "computer_vision/grayscale_image_processing.html",
  "title": "Grayscale Image Processing",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “Pixel-wise operations” here?",
    "ans": "(like Invert and Threshold) treat each pixel independently."
   },
   {
    "t": "What is meant by “Neighborhood operations” here?",
    "ans": "(like Blur and Edge Detection) calculate a pixel's new value based on its neighbors."
   }
  ]
 },
 {
  "path": "computer_vision/harris_corners.html",
  "title": "Harris Corners and Keypoints",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What distinguishes a corner from an edge in the structure tensor?",
    "o": [
     "A larger determinant only",
     "Both eigenvalues are large, rather than one",
     "The trace is zero",
     "The gradients point the same way"
    ],
    "a": 1,
    "w": "An edge has one large eigenvalue and one small one, so the window can slide along it freely. A corner is pinned in both directions."
   },
   {
    "t": "Why does Harris compute det(M) - k*trace(M)^2 instead of the eigenvalues?",
    "o": [
     "It is more accurate",
     "It behaves the same way - large only when both eigenvalues are large - without the cost of an eigendecomposition per pixel",
     "Eigenvalues can be complex",
     "It handles scale"
    ],
    "a": 1,
    "w": "The determinant is the product of the eigenvalues, so one small one kills it, and the trace term penalises imbalance. k sets how strictly."
   },
   {
    "t": "What is Harris NOT invariant to?",
    "o": [
     "Rotation",
     "Constant brightness offset",
     "Scale",
     "Translation"
    ],
    "a": 2,
    "w": "A corner viewed from twice the distance is a smaller corner, and a fixed window either sees part of it or swamps it. SIFT addressed this by searching over scales."
   }
  ]
 },
 {
  "path": "computer_vision/histograms_and_equalisation.html",
  "title": "Histograms and Equalisation",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does a histogram tell you nothing about?",
    "o": [
     "How many pixels are dark",
     "Where in the image the pixels are",
     "Whether the image is clipped",
     "Whether contrast is low"
    ],
    "a": 1,
    "w": "A histogram is a count per value. An image and a randomly shuffled copy of it have identical histograms, because position is discarded entirely."
   },
   {
    "t": "Which function does histogram equalisation use as its lookup table?",
    "o": [
     "The cumulative distribution function",
     "The probability density function",
     "A Gaussian",
     "The inverse of the histogram"
    ],
    "a": 0,
    "w": "The fraction of pixels at or below each value, scaled to 0-255. Common values make the CDF climb steeply and so get spread apart; rare values collapse together."
   },
   {
    "t": "Why does CLAHE clip the histogram before computing the CDF?",
    "o": [
     "To make it run faster",
     "To cap how steeply the CDF can climb, which limits noise amplification",
     "To remove outlier pixels",
     "To force the histogram to be bimodal"
    ],
    "a": 1,
    "w": "A tall bin means a steep CDF, which pushes nearly-identical neighbouring values far apart. That is exactly what noise amplification is, so limiting bin height limits it."
   }
  ]
 },
 {
  "path": "computer_vision/how_neural_network_process_images.html",
  "title": "How Neural Networks Process Images",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “Flattening” here?",
    "ans": "is the process of stringing rows of pixels together into a line."
   },
   {
    "t": "What does this module say about “The idea in brief”?",
    "ans": "When you look at an image, you see a 2D grid of colors. However, standard Artificial Neural Networks (specifically Dense or Fully-Connected Layers ) are structured to accept only a one-dimensional (1D) array or vector of numbers as input. Before a network can \"look\" at an image, the image must undergo Flattening ."
   },
   {
    "t": "What does this module say about “Preprocessing Parameters”?",
    "ans": "Neural networks usually compress images to small grids (like 28x28) to manage node count."
   }
  ]
 },
 {
  "path": "computer_vision/image_data_augmentation.html",
  "title": "Image Data Augmentation",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Data augmentation is one of the most effective and widely used tools for improving the performance of any computer vision model."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Image Data Augmentation is a critical technique in training deep learning models for computer vision. The core idea is to artificially expand your training dataset by creating modified copies of existing images. By showing a model the same image—but rotated, zoomed, shifted, or with altered brightness—we teach it to recognize the core subject matter regardless of these variations."
   },
   {
    "t": "What does this module say about “The Core Idea: Invariance and Generalization”?",
    "ans": "Imagine you're training a model to recognize cats. If all your training photos show cats perfectly centered and facing forward, the model might fail to recognize a cat that's slightly off-center or tilted. Data augmentation solves this. It teaches the model the concept of \"cat-ness\" is invariant to changes in position, scale, and orientation."
   }
  ]
 },
 {
  "path": "computer_vision/iou_and_non_max_suppression.html",
  "title": "IoU and Non-Max Suppression",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “The problem it solves”?",
    "ans": "A detector's region proposal stage doesn't stop at one box per object — it scores hundreds of candidate boxes and keeps every one above a confidence floor, which for a single real object usually means a cluster of overlapping, near-duplicate boxes. Intersection over Union (IoU) is the standard way to measure how much two boxes overlap: the area they share, divided by the total area either one covers."
   },
   {
    "t": "What does this module say about “NMS Threshold”?",
    "ans": "boxes A-D are four raw proposals from one detector pass, four confidence scores, two actual objects"
   },
   {
    "t": "What does this module say about “Non-Max Suppression”?",
    "ans": "NMS turns that overlap score into a cleanup rule. Sort every proposal by confidence, descending. Take the top one, keep it, and discard every remaining box whose IoU with it exceeds a threshold — those are treated as duplicate detections of the same object. Move to the next surviving box by confidence and repeat, until nothing is left to process."
   }
  ]
 },
 {
  "path": "computer_vision/mean_average_precision.html",
  "title": "Mean Average Precision",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Why must a matched ground-truth box be excluded from later matches?",
    "o": [
     "To save computation",
     "Otherwise several overlapping predictions on one object would each count as a success",
     "IoU cannot be computed twice",
     "The boxes are consumed by NMS"
    ],
    "a": 1,
    "w": "Only the highest-confidence prediction claims a ground-truth box; the rest become false positives. Without that rule a detector could inflate its score by firing repeatedly."
   },
   {
    "t": "Why is a COCO mAP much lower than a VOC mAP on the same predictions?",
    "o": [
     "COCO has more classes",
     "COCO averages over IoU thresholds from 0.50 to 0.95, rewarding precise localisation",
     "COCO uses a different precision formula",
     "COCO images are harder"
    ],
    "a": 1,
    "w": "VOC reported at IoU 0.5 alone. Averaging up to 0.95 demands nearly exact boxes, so the two numbers are different measurements and cannot be compared."
   },
   {
    "t": "What does mAP say about which confidence threshold to deploy?",
    "o": [
     "It gives the optimal threshold",
     "Nothing - it integrates over every threshold",
     "It assumes 0.5",
     "It uses the threshold that maximises F1"
    ],
    "a": 1,
    "w": "AP summarises the whole ranking. Choosing an operating point is a separate decision, made from the costs of the two kinds of error."
   }
  ]
 },
 {
  "path": "computer_vision/object_detection_with_bounding_boxes.html",
  "title": "Object Detection with Bounding Boxes",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “Start here”?",
    "ans": "An object detector's output head does two jobs per candidate region: classify what's there, and regress four numbers describing where it is precisely — typically a box center, width and height, or the offsets needed to nudge a fixed anchor box onto the real object. The classification half is an ordinary softmax problem."
   },
   {
    "t": "What does this module say about “IoU as loss, IoU as grade”?",
    "ans": "A natural localization loss is simply 1 − IoU between the predicted box and the ground truth box: 0 when they coincide exactly, approaching 1 as they stop overlapping at all. At evaluation time, the same IoU number gets a different job — a detection is usually scored as a true positive only if its IoU with the matching ground truth box clears a threshold, conventionally 0.5 under the PASCAL VOC convention."
   },
   {
    "t": "What does this module say about “Classification says what; detection says what and where”?",
    "ans": "A classifier answers one question about a whole image. A detector answers two questions about every object in it: what is it , and where is it — expressed as a rectangle."
   }
  ]
 },
 {
  "path": "computer_vision/padding_in_cnn.html",
  "title": "Padding in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “The Shrinking Problem”?",
    "ans": "In a standard convolutional layer, a kernel (like a 3x3 grid) slides across an image. However, the center of a 3x3 kernel cannot be placed on the absolute edge pixel of the input image without the rest of the kernel \"falling off\" the edge. Therefore, the kernel must start one pixel inward."
   },
   {
    "t": "What does this module say about “The Solution: Zero-Padding”?",
    "ans": "To fix this, we artificially expand the original image by adding a border of zeros around it before applying the convolution. This is called Padding ."
   },
   {
    "t": "What does this module say about “The edges lose out”?",
    "ans": "Slide a 3×3 filter over a 5×5 image and it only fits in 3×3 positions. The output is smaller than the input, and the reason is at the borders: a pixel in the corner has no neighbours on two sides, so the filter cannot be centred there."
   }
  ]
 },
 {
  "path": "computer_vision/parameter_sharing_in_cnn.html",
  "title": "Parameter Sharing in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “What is Parameter Sharing”?",
    "ans": "In a traditional Fully Connected (Dense) neural network layer, every output node is connected to every input node with a unique weight (parameter). If you process an image, a specific pixel in the top-left corner has a completely different weight than a pixel in the bottom-right corner."
   },
   {
    "t": "What does this module say about “The Massive Efficiency Gain”?",
    "ans": "Let's look at the math for the simple interactive above. We have a 4x4 input grid (16 pixels) and we are generating a 3x3 output grid (9 pixels)."
   },
   {
    "t": "What does this module say about “One filter, used everywhere”?",
    "ans": "A dense layer gives every input pixel its own weight to every output unit. A convolutional layer does something quite different: it learns one small filter and applies that same filter at every position in the image."
   }
  ]
 },
 {
  "path": "computer_vision/downsampling_in_cnn.html",
  "title": "Pooling Layer",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “Downsampling too aggressively on small images” here?",
    "ans": "A 32×32 CIFAR image cannot survive five stride-2 stages; it would be down to 1×1 before the network has done anything."
   },
   {
    "t": "What is meant by “Expecting pooling to give real invariance” here?",
    "ans": "It tolerates shifts of a pixel or two, not rotation, scale, or a shifted object. Augmentation is what handles those."
   },
   {
    "t": "What is meant by “Using max pooling right at the end” here?",
    "ans": "Global average pooling is almost always the better final layer."
   },
   {
    "t": "What is meant by “Flattening a large feature map into a dense layer” here?",
    "ans": "That is where the parameter explosion lives; global average pooling removes it."
   }
  ]
 },
 {
  "path": "computer_vision/rgb_image_processing.html",
  "title": "RGB Image Processing",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “Start here”?",
    "ans": "RGB Image Processing is a fundamental concept in computer vision. It's the basis for how computers \"see\" and manipulate color images. Every colored pixel on your screen is a combination of three values: Red, Green, and Blue."
   },
   {
    "t": "What does this module say about “The Core Idea: Channels as Layers”?",
    "ans": "Think of a color image not as a single flat picture, but as three separate grayscale images stacked on top of each other. Each of these \"layers\" is a channel , representing the intensity of Red, Green, or Blue light for every pixel."
   },
   {
    "t": "What does this module say about “Three numbers per pixel”?",
    "ans": "A colour image stores three values per pixel — red, green and blue — each usually 0 to 255. Mixing them additively produces every colour the display can show."
   }
  ]
 },
 {
  "path": "computer_vision/how_relu_works_in_cnn.html",
  "title": "ReLU Activation in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "For convolutional networks, plain ReLU remains the sensible default. Leaky ReLU is the first thing to try if you observe many dead units. GELU and SiLU dominate in transformers and in recent efficient vision architectures, where their smoothness appears to help slightly — at a small computational cost."
   },
   {
    "t": "What does this module say about “What is an Activation Function”?",
    "ans": "When a Convolutional or Dense layer processes data, it computes a series of linear mathematical operations (dot products). If a neural network only consisted of linear operations, stacking multiple layers wouldn't help—the entire network would mathematically collapse into a single linear model. To learn complex, real-world patterns (like recognizing a face or a dog), we must introduce non-linearity ."
   },
   {
    "t": "What does this module say about “Enter ReLU (Rectified Linear Unit)”?",
    "ans": "ReLU is currently the most popular activation function in the world for hidden layers. Its formula is brilliantly simple: if the input is negative, output 0. If the input is positive, output the input unchanged."
   }
  ]
 },
 {
  "path": "computer_vision/edge_detection.html",
  "title": "Real-time Edge Detection",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Edge detection is the first step in helping a computer make sense of the visual world, turning a sea of pixels into structured information."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Edge detection is a fundamental technique in computer vision and image processing. Its purpose is to identify points in a digital image where the brightness changes sharply. These points are typically organized into a set of curved line segments termed edges . This interactive uses the Sobel operator , a classic and efficient algorithm for this task."
   },
   {
    "t": "What does this module say about “The Core Idea: Finding Abrupt Changes”?",
    "ans": "Imagine walking across a flat, grey field that suddenly drops off into a black canyon. Your brain immediately registers that change in elevation. Edge detection algorithms do something similar with pixel values. They \"walk\" across the image and look for sudden jumps in brightness."
   }
  ]
 },
 {
  "path": "computer_vision/receptive_field.html",
  "title": "Receptive Field",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "With stride 1, how does the receptive field grow as layers are added?",
    "o": [
     "Linearly, by k - 1 per layer",
     "Geometrically, doubling each layer",
     "By k per layer",
     "It does not grow"
    ],
    "a": 0,
    "w": "Each layer's window centre already covers the previous field, so only the (k-1)/2 on each side is new. Three 3x3 layers give 1, 3, 5, 7."
   },
   {
    "t": "Why are three stacked 3x3 convolutions usually preferred over one 7x7?",
    "o": [
     "They are more accurate by definition",
     "Same receptive field, fewer weights, and non-linearities in between",
     "7x7 kernels cannot be trained",
     "They use less memory at inference only"
    ],
    "a": 1,
    "w": "27 weights against 49 for the same 7x7 field, plus two ReLUs between the layers - so the stack can represent functions a single linear map cannot."
   },
   {
    "t": "Why is the effective receptive field smaller than the theoretical one?",
    "o": [
     "Padding removes the edges",
     "Edge pixels reach the output through far fewer paths, so their influence falls off",
     "The formula is an approximation",
     "Stride reduces it"
    ],
    "a": 1,
    "w": "The number of paths from an input pixel to the output falls off roughly like a Gaussian away from the centre, so the rim of the theoretical field contributes very little."
   }
  ]
 },
 {
  "path": "computer_vision/resnet_and_identity_shortcuts.html",
  "title": "ResNet and Identity Shortcuts",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “ResNet-50 pretrained on ImageNet is the sensible default backbone” here?",
    "ans": "for a new vision project. It is well-supported everywhere, and fine-tunes reliably."
   },
   {
    "t": "What is meant by “The shortcut must match shapes” here?",
    "ans": "When channels or stride change, use the 1×1 projection; frameworks do this automatically, but hand-written blocks frequently get it wrong."
   },
   {
    "t": "What is meant by “Do not put a ReLU on the identity path” here?",
    "ans": "The whole point is that the path is clean."
   },
   {
    "t": "What is meant by “Batch normalisation and residuals work together” here?",
    "ans": "Removing BN from a deep ResNet usually breaks training unless the initialisation is adjusted to compensate."
   }
  ]
 },
 {
  "path": "computer_vision/resizing_and_interpolation.html",
  "title": "Resizing and Interpolation",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Why must a segmentation mask be resized with nearest neighbour?",
    "o": [
     "It is faster",
     "Class indices are names, and averaging two of them can produce a third unrelated class",
     "Masks are always small",
     "Bilinear does not work on integers"
    ],
    "a": 1,
    "w": "Averaging label 3 and label 5 gives 4, which is a different class entirely. Labels are categorical, so only copying is safe."
   },
   {
    "t": "What causes aliasing when shrinking an image?",
    "o": [
     "Using too many bits per pixel",
     "Sampling without averaging first, so fine detail reappears as a false pattern",
     "The image being too large",
     "Bicubic overshoot"
    ],
    "a": 1,
    "w": "Detail finer than the new sampling grid is not lost gracefully - it beats against the grid and produces a pattern that was never in the scene. Averaging before sampling prevents it."
   },
   {
    "t": "Why can bicubic interpolation produce halos near high-contrast edges?",
    "o": [
     "It reads too few pixels",
     "Its cubic weight function overshoots slightly, adding local contrast",
     "It converts to greyscale",
     "It averages sixteen pixels equally"
    ],
    "a": 1,
    "w": "The overshoot is what makes bicubic look sharper than bilinear. Beside a strong edge the same overshoot shows up as a faint bright or dark fringe."
   }
  ]
 },
 {
  "path": "computer_vision/semantic_segmentation_unet.html",
  "title": "Semantic Segmentation and U-Net",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “It is fully convolutional” here?",
    "ans": ", with no dense layers, so it accepts any input size and has relatively few parameters."
   },
   {
    "t": "What is meant by “Heavy augmentation” here?",
    "ans": "— particularly elastic deformation, which is realistic for tissue — multiplies the effective dataset."
   },
   {
    "t": "What is meant by “Every pixel is a training example” here?",
    "ans": "A single 512×512 image provides 262,144 labelled pixels, which is why so few images can be enough."
   },
   {
    "t": "What is meant by “Patch-based training” here?",
    "ans": "lets large images be processed in tiles, with overlap to avoid edge artefacts."
   }
  ]
 },
 {
  "path": "computer_vision/segmentation_tasks.html",
  "title": "Semantic, Instance and Panoptic Segmentation",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is the difference between semantic and panoptic segmentation?",
    "o": [
     "Panoptic labels the background too",
     "Panoptic also gives countable objects separate instance ids",
     "Semantic uses boxes",
     "Panoptic ignores stuff classes"
    ],
    "a": 1,
    "w": "Both label every pixel with a class. Only panoptic additionally distinguishes two adjacent cars as two objects rather than one 'car' region."
   },
   {
    "t": "Why does instance segmentation not label the background?",
    "o": [
     "It is too expensive",
     "It handles only 'things' - countable objects - and stuff like sky has no instances to assign",
     "The background has no texture",
     "It is left to a separate model"
    ],
    "a": 1,
    "w": "Asking 'how many skies' is not a question. Instance methods need something countable, which is exactly why panoptic segmentation needed a name of its own."
   },
   {
    "t": "What makes panoptic harder than running a semantic and an instance model together?",
    "o": [
     "Two models are slower",
     "Panoptic requires exactly one label per pixel, and instance masks can overlap",
     "The metrics are incompatible",
     "Stuff classes cannot be detected"
    ],
    "a": 1,
    "w": "Mask R-CNN style methods can assign a pixel to two instances. Producing one consistent labelling requires resolving those conflicts, which is what panoptic architectures do directly."
   }
  ]
 },
 {
  "path": "computer_vision/strides_in_cnn.html",
  "title": "Strides in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “What is a Stride”?",
    "ans": "In a Convolutional Layer, a kernel (filter) slides across the input image to produce a feature map. The Stride specifies exactly how many pixels this kernel shifts each time it moves."
   },
   {
    "t": "What does this module say about “Why use larger strides? (Downsampling)”?",
    "ans": "If you process a massive high-resolution image pixel-by-pixel, the resulting feature map will also be massive. This requires enormous amounts of memory and computational power."
   },
   {
    "t": "What does this module say about “How far the filter jumps”?",
    "ans": "Stride is the step size the filter takes as it slides. Stride 1 moves one pixel at a time and looks at every possible position. Stride 2 skips every other position, halving the output in both dimensions."
   }
  ]
 },
 {
  "path": "computer_vision/template_matching.html",
  "title": "Template Matching",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Why is normalised cross-correlation preferred over sum of squared differences?",
    "o": [
     "It is faster",
     "Standardising both sides removes brightness and contrast changes, so it measures pattern rather than pixel values",
     "It handles rotation",
     "It produces integer scores"
    ],
    "a": 1,
    "w": "Brightening the image by a constant grows every squared difference even where the shapes match perfectly. Subtracting means and dividing by standard deviations removes that."
   },
   {
    "t": "Why is the peak in a response map a blob rather than a point?",
    "o": [
     "The image is blurred",
     "A template shifted by one pixel still overlaps almost entirely and still scores well",
     "The correlation is normalised",
     "The template is too large"
    ],
    "a": 1,
    "w": "That is why non-maximum suppression is needed: several nearby positions score highly and would otherwise be returned as separate detections of the same thing."
   },
   {
    "t": "Which of these does template matching handle natively?",
    "o": [
     "Rotation",
     "Scale change",
     "Translation",
     "Deformation"
    ],
    "a": 2,
    "w": "Position is the only unknown it searches over. Rotation and scale require searching those dimensions too, and deformation cannot be represented by a rigid patch at all."
   }
  ]
 },
 {
  "path": "computer_vision/thresholding.html",
  "title": "Thresholding",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does Otsu's method maximise when choosing a threshold?",
    "o": [
     "The number of foreground pixels",
     "The variance between the two groups the threshold creates",
     "The image's overall contrast",
     "The number of edges detected"
    ],
    "a": 1,
    "w": "It tries every candidate threshold and keeps the one whose two resulting groups have the most separated means, weighted by group size."
   },
   {
    "t": "Why does a single global threshold fail on a page photographed under uneven lighting?",
    "o": [
     "The camera resolution is too low",
     "Lit paper can be brighter than ink on the shadowed side, so the values overlap",
     "Otsu is not being used",
     "Paper is not perfectly white"
    ],
    "a": 1,
    "w": "Once background values on one side exceed foreground values on the other, no single cut separates them. Adaptive thresholding computes a local threshold per neighbourhood instead."
   },
   {
    "t": "Why should a median filter usually run before thresholding a noisy image?",
    "o": [
     "It makes the image brighter",
     "Salt-and-pepper pixels sit at extreme values and survive any threshold",
     "It is required by Otsu",
     "It converts the image to greyscale"
    ],
    "a": 1,
    "w": "Impulse noise is at 0 or 255 by definition, so it lands on one side of every threshold. Removing it first is cheap and leaves the mask clean."
   }
  ]
 },
 {
  "path": "computer_vision/transfer_learning_with_cnn.html",
  "title": "Transfer Learning with CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does this module say about “What is Transfer Learning”?",
    "ans": "Training a Deep Convolutional Neural Network from scratch requires millions of images (like the ImageNet dataset), massive amounts of computing power (GPUs), and weeks of training time. Furthermore, early layers in a CNN generally learn the exact same things regardless of the dataset: generic edges, colors, and basic textures."
   },
   {
    "t": "What does this module say about “How it Works: Modifying the Architecture”?",
    "ans": "A standard pre-trained model (like ResNet-50 or VGG-16) is split into two conceptual parts:"
   },
   {
    "t": "What does this module say about “The Three Strategies”?",
    "ans": "We ignore pre-trained weights and initialize the entire network randomly. The network has no prior knowledge. The accuracy climbs very slowly, and on a small dataset, heavy models like VGG-16 will likely overfit and fail to reach high performance."
   }
  ]
 },
 {
  "path": "computer_vision/vision_transformer_patches.html",
  "title": "Vision Transformer Patches",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What does the projection step applied to each patch amount to?",
    "o": [
     "A small CNN",
     "A single linear layer, equivalently a convolution with kernel and stride both equal to the patch size",
     "An attention block",
     "A pooling operation"
    ],
    "a": 1,
    "w": "It is the only learned part of the patching step and it has no non-linearity - which is why it is usually implemented as a strided convolution."
   },
   {
    "t": "Halving the patch size multiplies attention cost by roughly how much?",
    "o": [
     "2",
     "4",
     "16",
     "8"
    ],
    "a": 2,
    "w": "Token count quadruples because the grid doubles in each dimension, and attention is quadratic in token count, so cost rises sixteenfold."
   },
   {
    "t": "Why did the original ViT underperform a ResNet on ImageNet alone?",
    "o": [
     "It had fewer parameters",
     "It has no built-in locality, so relationships convolution assumes must be learned from data",
     "Attention cannot represent edges",
     "The patches were too large"
    ],
    "a": 1,
    "w": "Pre-trained on 300 million images it overtook the ResNet. With enough data it learns the structure convolution assumes, and gains flexibility convolution lacks."
   }
  ]
 },
 {
  "path": "database/aggregate_functions_in_sql.html",
  "title": "Aggregate Functions and the NULL Trap",
  "cat": "Database",
  "q": [
   {
    "t": "What is the difference between COUNT(*) and COUNT(temp_c)?",
    "o": [
     "None, they are aliases",
     "COUNT(*) counts rows; COUNT(temp_c) counts rows where that column is not NULL",
     "COUNT(*) is slower",
     "COUNT(temp_c) counts distinct values"
    ],
    "a": 1,
    "w": "The gap between them is exactly the number of missing values in the column, which makes it a one-line data-quality check."
   },
   {
    "t": "AVG(temp_c) over nine rows, four of them NULL, divides the sum by what?",
    "o": [
     "9",
     "5",
     "4",
     "It returns NULL"
    ],
    "a": 1,
    "w": "AVG skips NULLs entirely - it is SUM(col)/COUNT(col). Whether that is the answer you want depends on what NULL means in your data."
   },
   {
    "t": "What does SUM return over a group containing no non-NULL values?",
    "o": [
     "0",
     "NULL",
     "An error",
     "The row count"
    ],
    "a": 1,
    "w": "Every aggregate except COUNT returns NULL over nothing. That NULL then propagates through any arithmetic it feeds, which is why COALESCE turns up around aggregates so often."
   }
  ]
 },
 {
  "path": "database/case_and_views_in_sql.html",
  "title": "CASE and Views in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What does this module say about “Start here”?",
    "ans": "CASE is an if/else that lives inside a SELECT list, evaluated once per row. A VIEW is a query with a name, so you can SELECT from it like a table without repeating the logic every time."
   },
   {
    "t": "What does this module say about “Views: a name for a query, not a copy of it”?",
    "ans": "A plain view stores no data. Every time you query it, the underlying SELECT runs again against the current table — which is the whole point of the raise experiment below. This is different from a materialized view , which does store a snapshot and has to be refreshed explicitly to catch up with changes underneath it."
   },
   {
    "t": "What does this module say about “CASE: if/else inside a query”?",
    "ans": "CASE is SQL's conditional expression. It returns a value, so it can appear anywhere a value can — in SELECT , in ORDER BY , inside an aggregate, even in WHERE ."
   }
  ]
 },
 {
  "path": "database/common_table_expressions_in_sql.html",
  "title": "Common Table Expressions in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A Common Table Expression is a named temporary result set defined with WITH , available only to the statement that follows it. Think of it as a variable for a query: compute something once, give it a name, then use that name."
   },
   {
    "t": "What does this module say about “Why Not Just Nest Subqueries”?",
    "ans": "You can — the nested example in this lab returns exactly the same rows. But compare how they read. A nested query is evaluated inside out , so you must find the innermost parenthesis and work outward, holding each layer in your head. A chain of CTEs reads top to bottom , like a recipe."
   },
   {
    "t": "What does this module say about “Recursive CTEs: The Real Superpower”?",
    "ans": "This is the thing subqueries genuinely cannot do. A recursive CTE has two halves joined by UNION ALL :"
   }
  ]
 },
 {
  "path": "database/composite_and_covering_indexes.html",
  "title": "Composite and Covering Indexes",
  "cat": "Database",
  "q": [
   {
    "t": "An index on (status, customer_id) exists. Which query can use it for a seek?",
    "o": [
     "WHERE customer_id = 42",
     "WHERE status = 'paid'",
     "Neither",
     "Only queries naming both columns"
    ],
    "a": 1,
    "w": "The index is sorted by status first, so all the 'paid' rows are contiguous. Rows for customer 42 are scattered across every status, so there is no block to find."
   },
   {
    "t": "What does a covering index avoid?",
    "o": [
     "The sort step",
     "Fetching rows from the table, because every column needed is already in the index",
     "Updating on insert",
     "The index search itself"
    ],
    "a": 1,
    "w": "An ordinary lookup searches the index and then fetches each row from the table by random access, which usually dominates. A covering index removes that second stage."
   },
   {
    "t": "Why should equality columns come before range columns in a composite index?",
    "o": [
     "Equality is faster to compare",
     "A range makes everything after it scattered, so only the range column is really used",
     "Ranges cannot be indexed",
     "It reduces index size"
    ],
    "a": 1,
    "w": "An equality narrows to a contiguous block that the next column is sorted within. Once a range opens up, the following columns are no longer in a single ordered run."
   }
  ]
 },
 {
  "path": "database/constraints_in_sql.html",
  "title": "Constraints: UNIQUE, CHECK and NOT NULL",
  "cat": "Database",
  "q": [
   {
    "t": "Why does UNIQUE usually permit several NULLs?",
    "o": [
     "NULLs are stored separately",
     "UNIQUE forbids equal values, and two NULLs are not known to be equal",
     "It is a bug retained for compatibility",
     "NULL is treated as zero"
    ],
    "a": 1,
    "w": "Comparing NULL to NULL yields NULL, not true. The constraint only rejects rows it can prove equal, so unknown values slip through - add NOT NULL if that is not what you meant."
   },
   {
    "t": "What can a CHECK constraint do that NOT NULL and UNIQUE cannot?",
    "o": [
     "Run on delete",
     "Relate two columns of the same row, such as end_date > start_date",
     "Reference another table",
     "Supply a default value"
    ],
    "a": 1,
    "w": "CHECK takes an arbitrary expression over the row, so multi-column rules are enforceable. They are otherwise checked nowhere and violated eventually."
   },
   {
    "t": "Why is a constraint stronger than the same rule in application code?",
    "o": [
     "It runs faster",
     "It holds for every client, including migrations, imports and consoles that were never written yet",
     "It cannot be dropped",
     "It produces better error messages"
    ],
    "a": 1,
    "w": "Application validation holds only for the code paths that run it. The database is the one component every write must pass through."
   }
  ]
 },
 {
  "path": "database/ddl_in_sql.html",
  "title": "DDL in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What is meant by “Adding a column with a default” here?",
    "ans": "historically rewrote every row. PostgreSQL 11+ and MySQL 8+ handle constant defaults without a rewrite; older versions do not."
   },
   {
    "t": "What is meant by “Changing a column type” here?",
    "ans": "generally rewrites the table and holds a strong lock."
   },
   {
    "t": "What is meant by “Adding an index” here?",
    "ans": "locks writes unless you use CREATE INDEX CONCURRENTLY (PostgreSQL) or an online index build."
   },
   {
    "t": "What is meant by “Adding a NOT NULL constraint” here?",
    "ans": "requires scanning the table to verify. Adding it as NOT VALID and validating later avoids the long lock in PostgreSQL."
   }
  ]
 },
 {
  "path": "database/dml_in_sql.html",
  "title": "DML in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "DML is where data actually changes, and the WHERE clause is what stands between a targeted fix and a table-wide accident. Preview with SELECT, wrap risky work in a transaction, and let the constraints you declared in DDL catch what you miss."
   },
   {
    "t": "What does this module say about “The idea in brief”?",
    "ans": "Data Manipulation Language covers the statements that read and change rows: INSERT , UPDATE , DELETE and SELECT . Where DDL defines the container, DML fills and reshapes its contents."
   },
   {
    "t": "What does this module say about “The Four Statements”?",
    "ans": "Both are valid SQL, both run without complaint, and both are the reason database people flinch at typing UPDATE into a production console."
   }
  ]
 },
 {
  "path": "database/datatypes_in_sql.html",
  "title": "Datatypes in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Pick the narrowest type that will hold every legitimate value, use DECIMAL for anything monetary, use real date types for dates, and add NOT NULL wherever a missing value would be meaningless. These choices are hard to change later and quietly govern correctness forever."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A datatype declares what a column may contain. The database uses it to reject invalid data, to decide how many bytes each value occupies, and to choose how comparisons and arithmetic behave. Get it wrong and you pay in storage, in speed, or — worst — in silently incorrect numbers."
   },
   {
    "t": "What does this module say about “Integers: pick the smallest that fits”?",
    "ans": "SMALLINT holds ±32,767 in 2 bytes. INT holds about ±2.1 billion in 4. BIGINT holds roughly ±9.2 quintillion in 8."
   }
  ]
 },
 {
  "path": "database/deadlocks_in_sql.html",
  "title": "Deadlocks",
  "cat": "Database",
  "q": [
   {
    "t": "What distinguishes a deadlock from ordinary lock waiting?",
    "o": [
     "The number of rows involved",
     "A cycle - each transaction waits for another that is itself waiting",
     "The isolation level",
     "How long the wait lasts"
    ],
    "a": 1,
    "w": "Ordinary waiting resolves itself when the holder commits. A cycle cannot, because every participant is blocked on another participant that will never move."
   },
   {
    "t": "What is the reliable way to prevent deadlocks?",
    "o": [
     "Raise the lock timeout",
     "Acquire locks in a consistent order everywhere in the application",
     "Use a lower isolation level",
     "Add more indexes"
    ],
    "a": 1,
    "w": "A cycle requires two transactions to disagree about the order. Ordering by primary key is the usual choice because it is total and can be applied mechanically."
   },
   {
    "t": "After a deadlock error, what must the application retry?",
    "o": [
     "The failed statement",
     "The whole transaction from the beginning",
     "Nothing, the engine retries it",
     "The connection"
    ],
    "a": 1,
    "w": "The victim's transaction was rolled back entirely, so re-running one statement starts from a state that no longer exists."
   }
  ]
 },
 {
  "path": "database/exists_vs_in_vs_join.html",
  "title": "EXISTS, IN and JOIN",
  "cat": "Database",
  "q": [
   {
    "t": "Why does NOT IN return no rows when the subquery contains a NULL?",
    "o": [
     "NULL is treated as zero",
     "The comparison against NULL is unknown rather than false, and WHERE keeps only definitely-true rows",
     "NOT IN does not support subqueries",
     "The subquery fails silently"
    ],
    "a": 1,
    "w": "NOT IN expands to a chain of <> comparisons joined by AND. One unknown makes the whole chain unknown for every row, so nothing survives the WHERE."
   },
   {
    "t": "Why does a JOIN sometimes return a customer twice when EXISTS does not?",
    "o": [
     "JOIN ignores the primary key",
     "A join pairs each left row with every match, so two orders give two rows",
     "EXISTS deduplicates automatically",
     "The join is missing a condition"
    ],
    "a": 1,
    "w": "That multiplication is what a join is for when you want the other table's columns. EXISTS asks only whether a match is there, so it never produces the extra rows."
   },
   {
    "t": "Why is `SELECT 1` conventional inside EXISTS?",
    "o": [
     "It is faster than SELECT *",
     "The select list is never read, so naming a column would be misleading",
     "EXISTS requires a literal",
     "It avoids a NULL check"
    ],
    "a": 1,
    "w": "EXISTS tests only whether a row was returned. Writing SELECT * suggests the columns matter, and they do not."
   }
  ]
 },
 {
  "path": "database/explain_and_query_plans.html",
  "title": "EXPLAIN and Query Plans",
  "cat": "Database",
  "q": [
   {
    "t": "In a plan, what does SCAN tell you?",
    "o": [
     "The query failed",
     "Every row will be read and tested",
     "An index is being used",
     "The table is sorted"
    ],
    "a": 1,
    "w": "SEARCH ... USING INDEX means it can jump straight to the matches. SCAN on a large table where you expected a lookup is the thing to look for."
   },
   {
    "t": "Why does `WHERE customer_id + 0 = 42` stop using an index on customer_id?",
    "o": [
     "Adding zero changes the value",
     "The index stores column values, not values of expressions over the column",
     "Arithmetic is not allowed in WHERE",
     "The index needs rebuilding"
    ],
    "a": 1,
    "w": "The index's ordering is on the bare column. Wrap it in anything - a function, arithmetic, a cast - and that ordering no longer corresponds to what is being asked."
   },
   {
    "t": "When is a full scan the better plan?",
    "o": [
     "Never",
     "On a small table, or when the query matches a large fraction of the rows",
     "Only when no index exists",
     "When the table is sorted"
    ],
    "a": 1,
    "w": "An index yields row locations that must then be fetched individually. Fetching most of a table one row at a time costs more than reading it in order."
   }
  ]
 },
 {
  "path": "database/having_in_sql.html",
  "title": "HAVING in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "WHERE filters rows before grouping and HAVING filters groups after, which is why WHERE cannot mention an aggregate and why HAVING is the only place a condition on SUM or COUNT can live. The consequence people miss is that WHERE does not merely remove rows from the output — it changes what every aggregate downstream is computed from, so moving one condition between the two clauses changes the numbers, not just the row..."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A grouped query runs in stages. Rows are read, WHERE discards the ones that fail a per-row test, what is left is collected into groups, each group is boiled down to its aggregates, and only then does HAVING get a look — at the groups, not the rows."
   },
   {
    "t": "What does this module say about “Two things people are surprised by”?",
    "ans": "HAVING works without GROUP BY. With no GROUP BY the whole table is one implicit group, so SELECT SUM (amount) FROM sales HAVING SUM (amount) > 5000 returns either one row or none. An aggregate in HAVING need not appear in SELECT. You can filter on COUNT (*) while selecting only the region. The aggregate is computed either way; SELECT just decides what is shown."
   }
  ]
 },
 {
  "path": "database/indexes_in_sql.html",
  "title": "Indexes and Query Performance",
  "cat": "Database",
  "q": [
   {
    "t": "What is meant by “Storage” here?",
    "ans": "Typically 10–20% of the table size per index, sometimes far more for wide composite indexes."
   },
   {
    "t": "What is meant by “Insert, update and delete speed” here?",
    "ans": "Every index must be updated whenever the indexed data changes. A table with eight indexes does nine writes for every logical write."
   },
   {
    "t": "What is meant by “Planning time and instability” here?",
    "ans": "More indexes means more options for the planner to consider, and more chances for it to choose a bad one on a mis-estimated query."
   },
   {
    "t": "What is meant by “Maintenance” here?",
    "ans": "Indexes fragment as data changes and occasionally need rebuilding."
   }
  ]
 },
 {
  "path": "database/isolation_levels.html",
  "title": "Isolation Levels",
  "cat": "Database",
  "q": [
   {
    "t": "What is a non-repeatable read?",
    "o": [
     "Reading uncommitted data",
     "Reading the same row twice in one transaction and getting different values",
     "A new row appearing between two queries",
     "A transaction being rolled back"
    ],
    "a": 1,
    "w": "It is permitted at READ COMMITTED, where each statement sees the latest committed data - so a report reading a table twice can produce internally inconsistent totals."
   },
   {
    "t": "How does SERIALIZABLE typically deliver its guarantee in a modern engine?",
    "o": [
     "By running transactions one at a time",
     "By detecting conflicts and aborting a transaction, which the application must retry",
     "By locking every table it touches",
     "By disabling concurrent writes"
    ],
    "a": 1,
    "w": "It lets transactions proceed optimistically and rejects one when no serial order explains the outcome. Code that assumes commit always succeeds fails intermittently under load."
   },
   {
    "t": "Why is 'we use REPEATABLE READ' an incomplete description of behaviour?",
    "o": [
     "The level does not exist in all engines",
     "The standard permits phantoms there, but PostgreSQL and MySQL each prevent them by different mechanisms",
     "It is the same as SERIALIZABLE",
     "It only applies to reads"
    ],
    "a": 1,
    "w": "The standard says which anomalies are permitted, not which are prevented, and engines prevent more than required in different ways. The engine matters as much as the level."
   }
  ]
 },
 {
  "path": "database/key_value_and_graph_models.html",
  "title": "Key-Value and Graph Models",
  "cat": "Database",
  "q": [
   {
    "t": "Why is a key-value store fast?",
    "o": [
     "It keeps everything in memory",
     "It has no query planner, joins or secondary indexes to maintain, so a lookup is a hash and a read",
     "It compresses values",
     "It skips durability"
    ],
    "a": 1,
    "w": "The narrow interface is the feature. The cost is that every access path must be designed in advance and encoded in the key."
   },
   {
    "t": "How does a graph edge differ from a SQL foreign key?",
    "o": [
     "It is faster to write",
     "It is a stored object followed like a pointer, rather than a value matched at query time",
     "It can only connect two node types",
     "It cannot carry properties"
    ],
    "a": 1,
    "w": "This is why traversal cost scales with edges visited rather than table size, and why the gap against joins widens with depth."
   },
   {
    "t": "What is a graph database usually worse at than a relational one?",
    "o": [
     "Variable-depth traversal",
     "Aggregating over millions of rows, such as total revenue by month",
     "Storing properties on relationships",
     "Finding shortest paths"
    ],
    "a": 1,
    "w": "The test for reaching for a graph model is whether your interesting questions are about connections rather than about attributes."
   }
  ]
 },
 {
  "path": "database/limit_and_offset_in_sql.html",
  "title": "Limit and Offset in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What is meant by “Do not show an exact total” here?",
    "ans": "\"Showing 21–40\" with a next button is usually enough, and it is what most large sites do."
   },
   {
    "t": "What is meant by “Use an approximate count” here?",
    "ans": "PostgreSQL's reltuples in pg_class , or EXPLAIN 's row estimate, is instant and close enough for \"about 1,200 results\"."
   },
   {
    "t": "What is meant by “Cache it” here?",
    "ans": "Store the count and refresh it periodically, or maintain it with a trigger if it must be exact."
   }
  ]
 },
 {
  "path": "database/mvcc_in_databases.html",
  "title": "MVCC: How Readers Avoid Blocking Writers",
  "cat": "Database",
  "q": [
   {
    "t": "What does a write do under MVCC?",
    "o": [
     "Overwrites the row in place and takes a lock",
     "Creates a new version, leaving the old one for transactions still reading it",
     "Blocks all readers until it commits",
     "Copies the whole table"
    ],
    "a": 1,
    "w": "Nothing is destroyed while a live snapshot might still need it, which is exactly why a reader that began earlier never has to wait."
   },
   {
    "t": "Which conflict does MVCC NOT remove?",
    "o": [
     "Reader against writer",
     "Writer against reader",
     "Two writers updating the same row",
     "Two readers"
    ],
    "a": 2,
    "w": "Both would produce a new version from the same old one and one update would be lost. The second waits, or fails at commit with a serialisation error."
   },
   {
    "t": "Why does an idle-in-transaction connection cause table bloat?",
    "o": [
     "It holds an exclusive lock",
     "Its snapshot pins every version created since it began, so cleanup cannot reclaim them",
     "It writes new versions continuously",
     "It disables autovacuum"
    ],
    "a": 1,
    "w": "Vacuum can only reclaim a version no live snapshot can still see. One old open transaction holds back cleanup for the whole database."
   }
  ]
 },
 {
  "path": "database/null_handling_in_sql.html",
  "title": "NULL Handling and COALESCE in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "NULL means unknown, so comparisons involving it are UNKNOWN rather than TRUE or FALSE, and aggregates skip it by default. COALESCE substitutes a default, NULLIF creates a NULL on purpose, and IS NULL is the only comparison that actually works — everything else is a trap that looks like it should work and quietly does not."
   },
   {
    "t": "What does this module say about “Context first”?",
    "ans": "NULL is not zero, not an empty string, and not false. It means the value is unknown, and every comparison that touches it inherits that uncertainty: NULL = NULL is not TRUE, it is UNKNOWN. This is three-valued logic , and COALESCE, NULLIF and IS NULL are the tools for working with it on purpose instead of by accident."
   },
   {
    "t": "What does this module say about “The three tools”?",
    "ans": "The single idea that unlocks this topic: NULL does not mean zero, and it does not mean an empty string. It means no value was recorded ."
   }
  ]
 },
 {
  "path": "database/normalization_in_sql.html",
  "title": "Normalization (1NF, 2NF, 3NF) in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What does this module say about “Start here”?",
    "ans": "A denormalized table stores the same fact in more than one place, which means updating it can leave two copies disagreeing. Normalization is a sequence of rules, each one removing a specific kind of redundancy by moving data into its own table."
   },
   {
    "t": "What does this module say about “The three rules”?",
    "ans": "Put everything in one wide table and three specific problems appear. They have names, and recognising them is most of the skill."
   },
   {
    "t": "What does this module say about “The problem normalisation solves”?",
    "ans": "Put everything in one wide table and three specific problems appear. They have names, and recognising them is most of the skill."
   }
  ]
 },
 {
  "path": "database/oltp_vs_olap_columnar.html",
  "title": "OLTP, OLAP and Columnar Storage",
  "cat": "Database",
  "q": [
   {
    "t": "Why is a row store slow at averaging one column over ten million rows?",
    "o": [
     "It cannot use indexes",
     "The values are scattered one per row, so every page must be read to collect a small fraction of each",
     "Averages require a full sort",
     "Row stores do not compress"
    ],
    "a": 1,
    "w": "To read 8 bytes of interest you read the whole 200-byte row. A column store reads only the region holding that column."
   },
   {
    "t": "Why do column stores compress so much better?",
    "o": [
     "They use a stronger algorithm",
     "A column holds one type and often few distinct values, so dictionary and run-length encoding work extremely well",
     "They discard nulls",
     "They store less data"
    ],
    "a": 1,
    "w": "Ten-times ratios are ordinary, and since the bottleneck is I/O, less data read is most of the speed-up."
   },
   {
    "t": "What goes wrong when reports run against the production OLTP database?",
    "o": [
     "The reports return stale data",
     "A large scan evicts the working set from the buffer cache, so application queries afterwards go to disk",
     "The reports lock the tables",
     "Transactions fail"
    ],
    "a": 1,
    "w": "The dashboard is slow and the checkout is slow, and the cause is not visible in the application's own metrics."
   }
  ]
 },
 {
  "path": "database/order_by_in_sql.html",
  "title": "ORDER BY in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A result set has no order unless ORDER BY gives it one, and the order is only deterministic once your keys separate every pair of rows — which is why a unique tie-breaker belongs on anything paginated. Keys apply left to right, each one consulted only for the ties the previous keys left behind. NULL placement is engine-specific, so write NULLS FIRST or NULLS LAST rather than trusting a default."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A table is a set of rows, and a set has no order. Without an ORDER BY the database is free to return rows in whatever order came out of its plan — insertion order, index order, or whatever the parallel workers finished in. It often looks stable for months and then changes the day the table grows an index or the optimiser picks a different plan."
   },
   {
    "t": "What does this module say about “Ties, and why a second key is not optional”?",
    "ans": "Sorting by a column with duplicate values leaves the tied rows in an undefined order relative to each other. Combined with LIMIT , this produces one of the most confusing bugs in SQL:"
   }
  ]
 },
 {
  "path": "database/partitioning_in_databases.html",
  "title": "Partitioning by Range and Hash",
  "cat": "Database",
  "q": [
   {
    "t": "What is partition pruning?",
    "o": [
     "Deleting old partitions automatically",
     "The planner proving a query cannot match certain partitions and skipping them",
     "Compressing partitions that are rarely read",
     "Merging small partitions"
    ],
    "a": 1,
    "w": "It requires the partition key in the WHERE clause. Without it every partition is read, and the scheme costs more than it saves."
   },
   {
    "t": "Why can hash partitioning not prune a range query?",
    "o": [
     "Hashes are too slow",
     "Hashing destroys order, so adjacent key values land in unrelated partitions",
     "Ranges are not supported",
     "It has too few partitions"
    ],
    "a": 1,
    "w": "That is the trade for even distribution. Range partitioning prunes ranges well but can leave one partition hot when recent data gets all the traffic."
   },
   {
    "t": "Why is time-series data almost always range-partitioned?",
    "o": [
     "Timestamps hash badly",
     "Dropping an old partition is instant, while deleting the equivalent rows writes a version each and bloats the table",
     "Range partitions compress better",
     "Hash partitioning cannot use timestamps"
    ],
    "a": 1,
    "w": "Retention is usually the bigger win over pruning. DROP TABLE unlinks a file; DELETE generates enormous WAL traffic and leaves bloat behind."
   }
  ]
 },
 {
  "path": "database/primary_and_foreign_keys.html",
  "title": "Primary and Foreign Keys",
  "cat": "Database",
  "q": [
   {
    "t": "What two guarantees does declaring a primary key give you?",
    "o": [
     "Uniqueness and an index",
     "Uniqueness and NOT NULL",
     "NOT NULL and a default",
     "Uniqueness and sort order"
    ],
    "a": 1,
    "w": "No two rows may share the value, and no row may leave it NULL. A row whose identity is unknown cannot be referred to at all."
   },
   {
    "t": "Why is a surrogate integer usually preferred over an email address as a primary key?",
    "o": [
     "Integers sort faster",
     "Nothing in the world can force it to change, so referencing rows never need updating",
     "Emails cannot be indexed",
     "It uses less disk"
    ],
    "a": 1,
    "w": "A natural key carries meaning and meaning changes. A person changing their email would mean updating every referencing row; a meaningless integer is stable by construction."
   },
   {
    "t": "Why does SQLite in particular need `PRAGMA foreign_keys = ON`?",
    "o": [
     "It has no foreign keys",
     "Enforcement is off by default for backwards compatibility, so REFERENCES clauses are accepted but ignored",
     "It only enforces them on DELETE",
     "The pragma creates the index"
    ],
    "a": 1,
    "w": "The schema parses and looks correct while guaranteeing nothing, which is worse than having no constraint at all because it invites trust."
   }
  ]
 },
 {
  "path": "database/query_execution_order.html",
  "title": "Query Execution Order in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What is meant by “DISTINCT” here?",
    "ans": "runs after SELECT and before ORDER BY . That is why SELECT DISTINCT x FROM t ORDER BY y fails in strict engines — y was removed before the sort could use it."
   },
   {
    "t": "What is meant by “Window functions” here?",
    "ans": "are computed after HAVING and before DISTINCT . They can see the grouped rows, and WHERE / HAVING cannot see them. Filtering on a window function always needs an outer query."
   },
   {
    "t": "What is meant by “CTEs ( WITH )” here?",
    "ans": "are conceptually evaluated first, as named inputs to the main query, though modern planners inline them and optimise across the boundary."
   },
   {
    "t": "What is meant by “OFFSET” here?",
    "ans": "runs with LIMIT , at the very end, after everything has been produced and sorted — which is exactly why deep offsets are slow."
   }
  ]
 },
 {
  "path": "database/recursive_ctes_in_sql.html",
  "title": "Recursive CTEs",
  "cat": "Database",
  "q": [
   {
    "t": "What stops a recursive CTE?",
    "o": [
     "A fixed iteration limit",
     "The recursive step returning no rows",
     "The anchor running out",
     "A depth column reaching zero"
    ],
    "a": 1,
    "w": "Nothing else halts it. With cyclic data the step keeps producing rows forever, which is why a depth cap or a path check is worth adding."
   },
   {
    "t": "What does the recursive step read on each round?",
    "o": [
     "The whole accumulated result so far",
     "Only the rows produced by the previous round",
     "Only the anchor's rows",
     "The base table only"
    ],
    "a": 1,
    "w": "That is exactly what makes it a level-by-level walk. Aggregating across all levels has to happen in the outer query instead."
   },
   {
    "t": "How do you turn a descendants query into an ancestors query?",
    "o": [
     "Add ORDER BY DESC",
     "Swap which side of the join condition the CTE is on, and start from a different anchor",
     "Use UNION instead of UNION ALL",
     "It cannot be done"
    ],
    "a": 1,
    "w": "Ancestors and descendants are the same walk with the arrow reversed. The construct is unchanged; only the anchor and the join condition move."
   }
  ]
 },
 {
  "path": "database/regular_expressions_in_sql.html",
  "title": "Regular Expressions in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What is meant by “Anchor them” here?",
    "ans": "Without ^ and $ , a pattern matches anywhere in the string, which is usually not what a validation rule means."
   },
   {
    "t": "What is meant by “Escape properly” here?",
    "ans": "A literal dot is \\. ; unescaped it matches any character, so '^[0-9]+.[0-9]+$' accepts \"12x34\"."
   },
   {
    "t": "What is meant by “Watch case sensitivity” here?",
    "ans": "PostgreSQL's ~ is case-sensitive, ~* is not; MySQL's REGEXP follows the column collation."
   },
   {
    "t": "What is meant by “Prefer explicit classes” here?",
    "ans": "[0-9] is unambiguous across engines; \\d is not always available and may include non-ASCII digits under Unicode rules."
   }
  ]
 },
 {
  "path": "database/replication_and_lag.html",
  "title": "Replication, Read Replicas and Lag",
  "cat": "Database",
  "q": [
   {
    "t": "Why does a user sometimes not see their own change after saving?",
    "o": [
     "The write failed silently",
     "The read went to a replica that has not yet applied the change",
     "The cache was stale",
     "The transaction rolled back"
    ],
    "a": 1,
    "w": "Nothing errored. Read-your-writes routing - sending that user's reads to the primary briefly after a write - is the usual fix."
   },
   {
    "t": "What does synchronous replication cost?",
    "o": [
     "Extra disk on the replica",
     "A network round trip on every commit, so writes get slower and stall if the replica is unreachable",
     "The ability to add more replicas",
     "Read capacity"
    ],
    "a": 1,
    "w": "It is a direct instance of the CAP trade: consistency across replicas costs availability and latency, and no configuration escapes it."
   },
   {
    "t": "What happens if a primary fails while a replica is 200ms behind?",
    "o": [
     "The replica catches up first",
     "Promoting it loses 200ms of writes that were already acknowledged to clients",
     "Writes are replayed from the client",
     "The failover is rejected"
    ],
    "a": 1,
    "w": "Those writes were confirmed and are gone. Durability requirements and replication mode are therefore the same decision."
   }
  ]
 },
 {
  "path": "database/groupby_in_sql.html",
  "title": "SQL GroupBy Visualizer",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The clauses run in a fixed order, and knowing it removes almost all confusion about which filter goes where:"
   },
   {
    "t": "What does this module say about “The idea in brief”?",
    "ans": "The GROUP BY clause in SQL is used with aggregate functions ( COUNT , SUM , AVG , etc.) to group rows that have the same values in specified columns into summary rows. It's one of the most powerful tools for data analysis."
   },
   {
    "t": "What does this module say about “The Core Idea: Collapse and Calculate”?",
    "ans": "Imagine you have a table of sales data. You don't want to see every single sale; you want to know the total sales for each department. GROUP BY is how you do this. It performs two main steps:"
   }
  ]
 },
 {
  "path": "database/sql_injection_and_parameters.html",
  "title": "SQL Injection and Parameterised Queries",
  "cat": "Database",
  "q": [
   {
    "t": "Why does a parameterised query prevent injection?",
    "o": [
     "It escapes dangerous characters",
     "The statement is parsed before the value arrives, so the value can never become syntax",
     "It validates input types",
     "It runs with fewer privileges"
    ],
    "a": 1,
    "w": "It is a structural guarantee rather than a filter: there is no input for which a bound parameter turns into query structure."
   },
   {
    "t": "Why is escaping an inadequate defence?",
    "o": [
     "It is slow",
     "Numeric contexts have no quotes to escape, character sets can defeat it, and it is a per-engine blacklist",
     "It breaks Unicode",
     "It only works on SELECT"
    ],
    "a": 1,
    "w": "WHERE id = 1 OR 1=1 contains no special characters at all. Parameterisation avoids the whole class by never putting the value in the query text."
   },
   {
    "t": "How should a user-supplied ORDER BY column be handled?",
    "o": [
     "Parameterise it with a placeholder",
     "Map it through an allowlist of known-good identifiers and reject anything else",
     "Escape it",
     "Wrap it in quotes"
    ],
    "a": 1,
    "w": "Placeholders stand for values, not identifiers. Identifiers must be chosen from a fixed set rather than sanitised."
   }
  ]
 },
 {
  "path": "database/joins_in_sql.html",
  "title": "SQL Joins Visualizer",
  "cat": "Database",
  "q": [
   {
    "t": "A LEFT JOIN returns:",
    "o": [
     "Only rows matching in both tables",
     "Every row from the left table, with NULLs where the right has no match",
     "Every row from both tables",
     "Only rows with no match"
    ],
    "a": 1,
    "w": "The left table is preserved whole. That is what makes LEFT JOIN the tool for 'show me all customers, including the ones with no orders'."
   },
   {
    "t": "You LEFT JOIN, then filter the right table in the WHERE clause. What usually happens?",
    "o": [
     "Nothing changes",
     "The unmatched rows have NULLs, fail the filter, and vanish - turning it into an INNER JOIN",
     "The query errors",
     "Duplicate rows appear"
    ],
    "a": 1,
    "w": "NULL fails almost every comparison. Putting that condition in the ON clause instead keeps the unmatched rows, and this is one of the most common SQL bugs there is."
   },
   {
    "t": "Joining on a column with duplicate values on both sides produces:",
    "o": [
     "An error",
     "More rows than either table - every matching pair is returned",
     "The rows are deduplicated automatically",
     "Only the first match"
    ],
    "a": 1,
    "w": "Three matching rows on each side give nine output rows. Unexpected row multiplication after a join is nearly always a duplicate key on one side."
   }
  ]
 },
 {
  "path": "database/window_functions_in_sql.html",
  "title": "SQL Window Functions",
  "cat": "Database",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Window functions are a powerful feature in SQL that perform a calculation across a set of table rows that are somehow related to the current row. Unlike aggregate functions ( SUM , COUNT ), which collapse rows into a single output row, window functions return a value for every single row ."
   },
   {
    "t": "What does this module say about “The Core Idea: A \"Window\" into Your Data”?",
    "ans": "The magic of window functions is the OVER() clause. This clause defines the \"window\" or set of rows the function should consider for its calculation. It has two key components:"
   },
   {
    "t": "What does this module say about “Aggregate without collapsing”?",
    "ans": "GROUP BY answers \"what is the total per region?\" and destroys the individual rows in the process. A window function answers \"what is the total for this row's region, shown next to this row?\" and keeps everything."
   }
  ]
 },
 {
  "path": "database/self_joins_in_sql.html",
  "title": "Self-Joins",
  "cat": "Database",
  "q": [
   {
    "t": "Why does an inner self-join drop the top of a hierarchy?",
    "o": [
     "The root has no id",
     "The root's parent reference is NULL and NULL matches nothing",
     "Inner joins skip the first row",
     "The alias is missing"
    ],
    "a": 1,
    "w": "An inner join needs a match on both sides. The root's manager_id is NULL, so no row matches and it is dropped silently - LEFT JOIN keeps it with a NULL manager."
   },
   {
    "t": "Why is `a.id < b.id` preferred over `a.id <> b.id` when pairing rows?",
    "o": [
     "It is faster",
     "It stops self-pairing and also returns each unordered pair once instead of twice",
     "<> does not work on integers",
     "It handles NULLs"
    ],
    "a": 1,
    "w": "<> removes self-pairs but still returns both (A, B) and (B, A). For two distinct rows exactly one ordering satisfies <, so each pair appears once."
   },
   {
    "t": "When does a self-join stop being the right tool?",
    "o": [
     "When the table is large",
     "When the depth of the hierarchy is not known in advance",
     "When the parent column is nullable",
     "When more than two columns are selected"
    ],
    "a": 1,
    "w": "Each level costs one written join, so an unknown depth cannot be expressed. That is exactly what a recursive CTE is for."
   }
  ]
 },
 {
  "path": "database/sharding_in_databases.html",
  "title": "Sharding",
  "cat": "Database",
  "q": [
   {
    "t": "What is the difference between partitioning and sharding?",
    "o": [
     "Sharding uses hashing, partitioning uses ranges",
     "Partitions live in one database; shards live on separate servers that share no planner, lock table or transaction manager",
     "Sharding is for reads only",
     "Partitioning requires a shard key"
    ],
    "a": 1,
    "w": "The machine boundary is the whole difficulty. Anything that needed a global view - joins, unique constraints, transactions - has to be rebuilt or given up."
   },
   {
    "t": "What happens to a query that does not name the shard key?",
    "o": [
     "It fails",
     "It is sent to every shard and the results merged, with latency set by the slowest one",
     "It is routed to shard 0",
     "It runs on a replica"
    ],
    "a": 1,
    "w": "Scatter-gather. This is why the shard key is a decision about which queries stay cheap forever, not a schema detail."
   },
   {
    "t": "Why do virtual buckets make rebalancing easier?",
    "o": [
     "They compress the data",
     "Keys hash to a fixed large number of buckets, so adding a shard moves a few buckets rather than changing the hash rule for every row",
     "They remove the need for a shard key",
     "They allow cross-shard joins"
    ],
    "a": 1,
    "w": "With a plain hash(key) % N rule, adding a shard changes almost every row's destination. Consistent hashing solves the same problem by moving only one arc of the ring."
   }
  ]
 },
 {
  "path": "database/star_schema.html",
  "title": "Star Schema: Facts and Dimensions",
  "cat": "Database",
  "q": [
   {
    "t": "What does a fact table contain?",
    "o": [
     "Descriptive attributes like product names and categories",
     "One row per event: numeric measures plus foreign keys to the dimensions",
     "One row per customer",
     "Aggregated totals"
    ],
    "a": 1,
    "w": "Long and narrow. The descriptive text lives in the dimensions, which are short and wide - putting it in the fact table widens the largest table for nothing."
   },
   {
    "t": "Why is mixing grain in a fact table so dangerous?",
    "o": [
     "It breaks foreign keys",
     "Summing a per-order total across order lines multiplies revenue by the number of lines, and nothing errors",
     "It prevents indexing",
     "It makes joins ambiguous"
    ],
    "a": 1,
    "w": "It is the most common defect in real warehouses precisely because it is silent. State the grain in one sentence before creating the table."
   },
   {
    "t": "Why do star schemas usually beat snowflake schemas in a warehouse?",
    "o": [
     "They use less storage",
     "Dimensions are small enough that the redundancy costs little, while the extra joins cost real query time",
     "Snowflake schemas cannot be indexed",
     "BI tools cannot read snowflakes"
    ],
    "a": 1,
    "w": "The exception is a genuinely large dimension - tens of millions of customers - where duplication starts to matter more than the joins."
   }
  ]
 },
 {
  "path": "database/subqueries_in_sql.html",
  "title": "Subqueries in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What is meant by “A scalar subquery returning more than one row” here?",
    "ans": "The engine raises an error at runtime, and only when the data grows enough to produce a second row — so this bug ships. Guard with LIMIT 1 and an explicit ORDER BY , or use MIN / MAX ."
   },
   {
    "t": "What is meant by “NOT IN with NULLs” here?",
    "ans": "Covered above, and worth repeating because it fails silently rather than loudly."
   },
   {
    "t": "What is meant by “Forgetting the alias on a derived table” here?",
    "ans": "Most engines require one; the error message is clear but the cause is not obvious the first time."
   },
   {
    "t": "What is meant by “Correlated subqueries in SELECT” here?",
    "ans": "SELECT name, (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) FROM customers c runs one count per customer. A LEFT JOIN with GROUP BY , or a window function, does it in one pass."
   }
  ]
 },
 {
  "path": "database/cap_theorem.html",
  "title": "The CAP Theorem",
  "cat": "Database",
  "q": [
   {
    "t": "What is wrong with 'pick two of three'?",
    "o": [
     "There are actually four properties",
     "Partitions are not optional, so the real choice is between C and A when one occurs",
     "Consistency and availability are the same thing",
     "It only applies to SQL databases"
    ],
    "a": 1,
    "w": "Networks fail eventually, so P must be tolerated. The theorem constrains behaviour during that specific temporary failure, not design in general."
   },
   {
    "t": "A CP system during a partition will:",
    "o": [
     "Answer from local state and reconcile later",
     "Return an error rather than risk two different answers to the same question",
     "Elect a new primary",
     "Queue writes indefinitely"
    ],
    "a": 1,
    "w": "Correct, and temporarily unavailable to anyone who cannot reach a quorum. The right choice when a wrong answer is worse than no answer."
   },
   {
    "t": "What does the 'ELC' half of PACELC describe?",
    "o": [
     "Error handling during partitions",
     "The latency-against-consistency trade when the network is healthy, which is live on every request",
     "Eventual consistency guarantees",
     "Leader election"
    ],
    "a": 1,
    "w": "Confirm every write with remote replicas and be slower, or acknowledge locally and be briefly stale. It is the synchronous-versus-asynchronous replication choice."
   }
  ]
 },
 {
  "path": "database/document_model_vs_rows.html",
  "title": "The Document Model against Rows",
  "cat": "Database",
  "q": [
   {
    "t": "When does the document model genuinely beat normalised rows?",
    "o": [
     "Always, for reads",
     "When the access pattern is fetching one whole object, since it is a single read with no joins",
     "When data must be strongly consistent",
     "When the same fact appears in many places"
    ],
    "a": 1,
    "w": "The data is contiguous and deserialises straight into an object. The gap widens as the object gains parts - and closes when queries come from other directions."
   },
   {
    "t": "What is the real cost of copying a customer's address into every order document?",
    "o": [
     "Disk space",
     "Every change means finding and rewriting every copy, and any missed copy diverges",
     "Slower reads",
     "It breaks JSON indexing"
    ],
    "a": 1,
    "w": "The question is whether the copies must agree. On an invoice the address arguably should be a historical fact, in which case it is not duplication at all."
   },
   {
    "t": "Why has the relational/document distinction largely dissolved?",
    "o": [
     "Document stores added SQL",
     "PostgreSQL, MySQL and SQLite all have indexable, queryable, transactional JSON columns, so the choice is per-column",
     "Documents turned out to be slower",
     "Normalisation was abandoned"
    ],
    "a": 1,
    "w": "Tables for entities queried from several directions, a JSON column for genuinely variable parts read only alongside their parent - in one database, in one transaction."
   }
  ]
 },
 {
  "path": "database/transactions_and_acid.html",
  "title": "Transactions and ACID in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What is meant by “Always touch rows in a consistent order” here?",
    "ans": "— sort account IDs before updating them, and the cycle above cannot form."
   },
   {
    "t": "What is meant by “Keep transactions short” here?",
    "ans": "Never hold a transaction open across a network call, a user's think time, or an external API. The most common cause of lock contention is a transaction that started before it needed to."
   },
   {
    "t": "What is meant by “Retry on deadlock” here?",
    "ans": "Deadlock errors are expected under load, not exceptional. Application code that touches contended rows should catch the error and retry with a short random delay."
   }
  ]
 },
 {
  "path": "database/union_intersect_except_in_sql.html",
  "title": "UNION, INTERSECT and EXCEPT in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What is meant by “Combining partitioned or archived tables” here?",
    "ans": "into one result, which is the classic UNION ALL case."
   },
   {
    "t": "What is meant by “Comparing two datasets during a migration” here?",
    "ans": "Run A EXCEPT B and B EXCEPT A ; if both return nothing, the datasets are identical. This is the fastest reconciliation check there is."
   },
   {
    "t": "What is meant by “Adding a total row” here?",
    "ans": "to a report by unioning the detail with an aggregate."
   },
   {
    "t": "What is meant by “Merging results from different sources” here?",
    "ans": "that happen to share a shape — internal customers and external ones, current staff and alumni."
   }
  ]
 },
 {
  "path": "database/what_are_non_relational_databases.html",
  "title": "What are Non Relational Databases?",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "There is no \"better\" model, only different bargains. Relational gives you enforced consistency and flexible ad-hoc queries; non-relational gives you speed, scale and schema freedom in exchange for moving integrity into your application. Most real systems today use both."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A non-relational database stores data in a shape other than fixed tables of rows and columns. The name \"NoSQL\" is a historical accident — it is best read as \"not only SQL\" , since many of these systems now support SQL-like query languages."
   },
   {
    "t": "What does this module say about “The Four Families”?",
    "ans": "The headline benefit of a document store is that you can add a field to one document without altering anything else. For rapidly changing data, or genuinely heterogeneous records, that removes real friction: no migration, no downtime, no coordination."
   }
  ]
 },
 {
  "path": "database/what_are_relational_databases.html",
  "title": "What are Relational Databases?",
  "cat": "Database",
  "q": [
   {
    "t": "What does this module say about “The problem it solves”?",
    "ans": "A relational database stores data in tables of rows and columns, where every table describes one kind of thing — customers, orders, products — and tables are connected by shared key values rather than by nesting data inside each other."
   },
   {
    "t": "What does this module say about “Keys are the whole trick”?",
    "ans": "The foreign key is what turns a pile of tables into a database. Declared properly, it makes an order pointing at a non-existent customer impossible — not unlikely, not caught by a validation function somewhere, but rejected by the engine for every client that ever connects."
   },
   {
    "t": "What does this module say about “Why Split the Data at All”?",
    "ans": "Switch this lab to one flat table and look at the red cells. The customer's name and city now repeat on every order they ever placed. That redundancy causes three classic problems:"
   }
  ]
 },
 {
  "path": "database/where_clause_in_sql.html",
  "title": "Where Clause in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "What is meant by “BETWEEN a AND b” here?",
    "ans": "is inclusive at both ends. For dates this is a common source of off-by-one bugs, because BETWEEN '2026-01-01' AND '2026-01-31' excludes anything timestamped later on the 31st. Prefer >= start AND < next_start ."
   },
   {
    "t": "What is meant by “IN (...)” here?",
    "ans": "is shorthand for a chain of ORs, and works with a subquery as well as a literal list."
   },
   {
    "t": "What is meant by “LIKE” here?",
    "ans": "uses % for any run of characters and _ for exactly one. Escape literal percent signs with an ESCAPE clause."
   },
   {
    "t": "What is meant by “IS DISTINCT FROM” here?",
    "ans": "compares two values treating NULLs as comparable — NULL IS DISTINCT FROM 5 is TRUE. It is the operator you want when comparing nullable columns, and it is supported by PostgreSQL and several others."
   }
  ]
 },
 {
  "path": "deep_learning/activation_functions.html",
  "title": "Activation Functions in DL",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Stack 100 linear layers with no activation between them. What can the result represent?",
    "o": [
     "Any function at all",
     "Exactly what a single linear layer can - nothing more",
     "Only step functions",
     "Curves, but not corners"
    ],
    "a": 1,
    "w": "A chain of matrix multiplies collapses into one matrix. Without a non-linearity, depth buys literally nothing."
   },
   {
    "t": "A ReLU unit outputs zero for every input in your dataset and its gradient never recovers. This is called:",
    "o": [
     "Vanishing gradient",
     "A dead ReLU",
     "Exploding gradient",
     "Saturation"
    ],
    "a": 1,
    "w": "ReLU's gradient is exactly zero on the negative side, so a unit pushed fully negative can never be updated back. Leaky ReLU exists to keep a small gradient alive there."
   },
   {
    "t": "Why do deep sigmoid networks train so badly?",
    "o": [
     "Sigmoid is slow to compute",
     "Its gradient is tiny at both ends, and multiplying many tiny gradients vanishes the signal",
     "Sigmoid cannot output negative values",
     "It requires normalised inputs"
    ],
    "a": 1,
    "w": "Sigmoid's derivative peaks at 0.25 and falls toward zero at the tails. Chain a dozen of those together and the gradient reaching the early layers is effectively zero."
   }
  ]
 },
 {
  "path": "deep_learning/autoencoders.html",
  "title": "Autoencoders",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Why is training a network to copy its input not a null task?",
    "o": [
     "The network is too small to copy",
     "The representation in the middle is smaller than the input, so information must be discarded - and the loss decides what",
     "The output has a different shape",
     "Noise is always added"
    ],
    "a": 1,
    "w": "What survives the bottleneck is what the data was mostly made of. The copying is the mechanism; the constraint is the point."
   },
   {
    "t": "What does a linear autoencoder with squared error find?",
    "o": [
     "An arbitrary subspace",
     "The same subspace as PCA",
     "The identity function",
     "A sparse code"
    ],
    "a": 1,
    "w": "Provably the same span, though not necessarily the principal components in order. Non-linearity is what makes an autoencoder more than PCA with extra steps."
   },
   {
    "t": "Why does a bottleneck remove noise?",
    "o": [
     "Noise is filtered before encoding",
     "Noise has no structure to compress, so a narrow code cannot afford to store it",
     "The decoder smooths the output",
     "The loss ignores noise"
    ],
    "a": 1,
    "w": "Denoising autoencoders make this the training procedure - corrupt the input, ask for the clean version - which also prevents a wide code from learning the identity."
   }
  ]
 },
 {
  "path": "deep_learning/backpropagation.html",
  "title": "Backpropagation and the Computational Graph",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What is meant by “Start from the loss” here?",
    "ans": "The page opens with the forward pass already done: values left to right, ending on a single number. Press Reset and Step if you want to watch that part happen too — but it holds no surprises, it is just the network making a prediction."
   },
   {
    "t": "What is meant by “Keep stepping” here?",
    "ans": "The gradient starts at the loss as 1, then flows right to left. Each node prints the multiplication it performed, so you can read the chain rule rather than take it on faith."
   },
   {
    "t": "What is meant by “Compare the two weight gradients” here?",
    "ans": "They differ only by their input: ∂L/∂w₁ carries x₁ and ∂L/∂w₂ carries x₂. Set Input x1 to 0 and its weight's gradient goes to exactly zero — that weight cannot learn from this example at all."
   },
   {
    "t": "What is meant by “Check the answer” here?",
    "ans": "The gradient-check panel recomputes ∂L/∂w₁ numerically, by nudging w₁ and dividing the change in loss by the change in weight. It agrees with the chain rule to several decimal places, which is the test to reach for whenever a hand-written backward pass looks suspicious."
   }
  ]
 },
 {
  "path": "deep_learning/batch_normalization.html",
  "title": "Batch Normalization in Deep Networks",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The conventional order is Conv → BatchNorm → ReLU . Normalising before the activation keeps the pre-activations centred, so roughly half the ReLU units are active — which is what the initialisation assumed."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Batch Normalization (BatchNorm) was introduced by Ioffe & Szegedy in 2015 and is now a standard building block in virtually every deep network. It normalizes the inputs to each layer so that training is faster and more stable. This page lets you see what happens with and without it."
   },
   {
    "t": "What does this module say about “The Problem BatchNorm Solves”?",
    "ans": "When you feed raw features with different scales (e.g., Age 18–80 vs. Salary 20k–200k) into a network, the first-layer weights that receive the large feature grow disproportionately. During backpropagation those large weights amplify gradients in early layers ( exploding ), while deeper layers receive progressively smaller updates ( vanishing ). The result: unstable training or very slow convergence."
   }
  ]
 },
 {
  "path": "deep_learning/batch_processing_in_neural_networks.html",
  "title": "Batch Processing in Networks",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What is meant by “Mixed precision” here?",
    "ans": "stores activations in 16-bit, roughly halving the requirement and speeding up the arithmetic."
   },
   {
    "t": "What is meant by “Gradient checkpointing” here?",
    "ans": "keeps only some activations and recomputes the rest, trading about 30% more compute for a large memory saving."
   },
   {
    "t": "What is meant by “Gradient accumulation” here?",
    "ans": ", above, which keeps the memory small and the effective batch large."
   }
  ]
 },
 {
  "path": "deep_learning/contrastive_learning.html",
  "title": "Contrastive and Self-Supervised Learning",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What is a positive pair in contrastive learning?",
    "o": [
     "Two images of the same class",
     "Two augmented views of the same image",
     "An image and its label",
     "Two images that score highly"
    ],
    "a": 1,
    "w": "No labels are involved, which is the point. Two images of the same class are treated as negatives - a real cost that supervised contrastive learning fixes when labels exist."
   },
   {
    "t": "What does a low temperature do to InfoNCE?",
    "o": [
     "Flattens the comparison",
     "Sharpens the softmax so the hardest negative dominates the gradient",
     "Reduces the number of negatives needed",
     "Prevents collapse"
    ],
    "a": 1,
    "w": "It learns fine distinctions quickly and is unstable. High temperature flattens everything until the loss stops discriminating at all."
   },
   {
    "t": "How do BYOL and SimSiam avoid collapse without negatives?",
    "o": [
     "They use very large batches",
     "An asymmetry - a predictor head on one branch and a stop-gradient on the other",
     "They add noise to the representations",
     "They keep a queue of past representations"
    ],
    "a": 1,
    "w": "The large-batch and queue approaches are SimCLR and MoCo, which do use negatives. That negatives turned out to be optional was a genuine surprise."
   }
  ]
 },
 {
  "path": "deep_learning/data_sparsity.html",
  "title": "Data Sparsity",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What is meant by “Transfer learning” here?",
    "ans": "— start from a pretrained model, so a few hundred labels suffice."
   },
   {
    "t": "What is meant by “Self-supervised pretraining” here?",
    "ans": "on your unlabelled data, then fine-tune on the labelled subset."
   },
   {
    "t": "What is meant by “Active learning” here?",
    "ans": "— let the model choose which examples to send for labelling, prioritising the ones it is least sure about."
   },
   {
    "t": "What is meant by “Pseudo-labelling” here?",
    "ans": "— label the confident predictions on unlabelled data and train on them, carefully, since errors compound."
   }
  ]
 },
 {
  "path": "deep_learning/diffusion_models.html",
  "title": "Diffusion Models",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What does the network in a diffusion model predict?",
    "o": [
     "The clean image",
     "The noise that was added",
     "The next step's schedule",
     "A latent code"
    ],
    "a": 1,
    "w": "Given the noise, recovering the original is just rearranging the forward equation. That makes the loss a plain squared error rather than anything adversarial."
   },
   {
    "t": "Why can training sample a random step t rather than simulating up to it?",
    "o": [
     "The steps are independent",
     "The forward process has a closed form, so you can jump to any t in one shot",
     "The schedule is linear",
     "Early steps do not matter"
    ],
    "a": 1,
    "w": "x_t = sqrt(abar)x0 + sqrt(1-abar)eps needs no simulation, which is what makes training cheap."
   },
   {
    "t": "What is the main disadvantage against a GAN?",
    "o": [
     "Blurrier samples",
     "Mode collapse",
     "Sampling needs many sequential passes where a GAN needs one",
     "No stable objective"
    ],
    "a": 2,
    "w": "The stable objective and full coverage are diffusion's advantages. DDIM and distillation have shortened sampling considerably, but it remains the trade."
   }
  ]
 },
 {
  "path": "deep_learning/dropout_in_neural_networks.html",
  "title": "Dropout Regularization",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What does dropout do during training?",
    "o": [
     "Removes layers permanently",
     "Randomly zeroes a fraction of unit outputs on each forward pass",
     "Reduces the learning rate over time",
     "Discards the worst training examples"
    ],
    "a": 1,
    "w": "A different random subset is silenced every pass, so no unit can rely on any particular other unit being present. That forced redundancy is what regularises the network."
   },
   {
    "t": "Is dropout active at inference time?",
    "o": [
     "Yes, always",
     "No - it is disabled, and activations are scaled to compensate",
     "Only for the last layer",
     "Only if the model overfits"
    ],
    "a": 1,
    "w": "You want deterministic predictions when serving. Leaving dropout on at inference is a classic bug: it makes the same input return different answers on each call."
   },
   {
    "t": "A dropout rate of 0.9 on a small network is likely to cause:",
    "o": [
     "Faster convergence",
     "Severe underfitting - too little signal survives each pass",
     "Perfect generalisation",
     "No change"
    ],
    "a": 1,
    "w": "Regularisation is a dial, not a switch. Drop nine units in ten and there is barely a network left to learn anything."
   }
  ]
 },
 {
  "path": "deep_learning/early_stopping_in_neural_networks.html",
  "title": "Early Stopping",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Early stopping monitors which quantity?",
    "o": [
     "Training loss",
     "Validation loss",
     "The learning rate",
     "Gradient magnitude"
    ],
    "a": 1,
    "w": "Training loss almost always keeps falling, so it can never signal when to stop. Validation loss is the one that turns around when generalisation starts degrading."
   },
   {
    "t": "What does the 'patience' setting control?",
    "o": [
     "How many epochs to train in total",
     "How many epochs without improvement to tolerate before stopping",
     "The size of the validation set",
     "How much the loss must fall by"
    ],
    "a": 1,
    "w": "Validation loss is noisy and can tick up for an epoch or two before improving again. Patience stops you from quitting on a wobble."
   },
   {
    "t": "Patience is set to 0. What is the risk?",
    "o": [
     "Training never stops",
     "Stopping on the first noisy uptick, well before the real minimum",
     "The model overfits badly",
     "The learning rate decays too fast"
    ],
    "a": 1,
    "w": "With no tolerance at all, one bad epoch ends the run. You get an undertrained model and a validation curve that had plenty left in it."
   }
  ]
 },
 {
  "path": "deep_learning/embedding_layers.html",
  "title": "Embedding Layers",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Why is an embedding layer implemented as a lookup rather than a matmul?",
    "o": [
     "Lookups are more accurate",
     "The one-hot product touches every weight in the table to retrieve a single row",
     "Matmuls cannot be differentiated",
     "The table is too large to store"
    ],
    "a": 1,
    "w": "At 50,000 tokens and 512 dimensions that is 25.6 million numbers touched to get 512. The definitions are identical; only the implementation differs."
   },
   {
    "t": "Which rows of an embedding table receive a gradient on a given step?",
    "o": [
     "All of them",
     "Only the rows for tokens that appeared in the batch",
     "The most frequent rows",
     "None - they are frozen"
    ],
    "a": 1,
    "w": "The backward pass scatters gradients to the rows that were used, which means a very large parameter tensor sits almost entirely idle on any step."
   },
   {
    "t": "What does weight tying do?",
    "o": [
     "Freezes the embedding table",
     "Shares the input embedding with the output layer, halving the cost and usually improving quality",
     "Reduces the embedding dimension",
     "Ties embeddings to positions"
    ],
    "a": 1,
    "w": "Both layers have one row per token and both are learning what tokens mean, so sharing them is natural as well as cheaper."
   }
  ]
 },
 {
  "path": "deep_learning/feature_scaling_in_neural_networks.html",
  "title": "Feature Scaling & Weight Bias",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Gradients scale with input magnitude, so unscaled features give some weights enormous gradients and others negligible ones, and no single learning rate serves both. Standardisation is the default for neural networks; min-max suits bounded inputs and breaks on outliers. Fit the scaler on the training split only, keep those statistics for validation, test and production, and leave one-hot columns alone."
   },
   {
    "t": "What does this module say about “Why scale breaks gradient descent”?",
    "ans": "The gradient of the loss with respect to a weight is proportional to that weight’s input . So a feature measured in hundreds of thousands produces gradients roughly four orders of magnitude larger than a feature measured in tens."
   },
   {
    "t": "What does this module say about “Work the numbers”?",
    "ans": "Take age 30 and salary 60,000 with weights of 0.5 each. The salary term contributes 30,000 to the weighted sum and the age term contributes 15 — the age feature is invisible, and it would take a weight around 1000× larger to compete."
   }
  ]
 },
 {
  "path": "deep_learning/generative_adversarial_networks.html",
  "title": "Generative Adversarial Networks",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Why does a very good discriminator stop the generator learning?",
    "o": [
     "It overfits the real data",
     "Where the distributions barely overlap its output is flat, and a flat function has no gradient to follow",
     "It slows training down",
     "It causes mode collapse"
    ],
    "a": 1,
    "w": "The generator improves by following the slope of the discriminator's opinion. Wasserstein GAN replaces the classifier with a critic whose distance stays informative even for disjoint distributions."
   },
   {
    "t": "What is mode collapse?",
    "o": [
     "The discriminator stops improving",
     "The generator finds a narrow region that fools the discriminator and stays there, representing little of the data",
     "Training diverges",
     "The latent space collapses to a point"
    ],
    "a": 1,
    "w": "Nothing in the objective punishes it directly, because the discriminator judges samples one at a time and never sees the lack of variety."
   },
   {
    "t": "Why are GAN samples sharper than a VAE's?",
    "o": [
     "GANs use larger networks",
     "Nothing rewards averaging - a hedged sample is exactly what the discriminator catches",
     "GANs have no latent space",
     "The discriminator sharpens them"
    ],
    "a": 1,
    "w": "A VAE's pixel-wise reconstruction term rewards hedging: when uncertain, the average of the possibilities scores better than any single one."
   }
  ]
 },
 {
  "path": "deep_learning/gradient_accumulation.html",
  "title": "Gradient Accumulation",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Why is the accumulated update identical to a large-batch update?",
    "o": [
     "It is an approximation that converges",
     "The gradient of a mean loss is the mean of the per-example gradients, and differentiation is linear",
     "The optimiser corrects for it",
     "The learning rate is adjusted"
    ],
    "a": 1,
    "w": "Identical up to floating-point ordering, not merely similar. That linearity is the whole justification."
   },
   {
    "t": "Which part of training memory does accumulation reduce?",
    "o": [
     "The optimiser state",
     "The activations kept for the backward pass",
     "The weights",
     "The gradients"
    ],
    "a": 1,
    "w": "Activations scale with batch size; weights, gradients and optimiser state do not. When the weights alone do not fit, accumulation is not the answer."
   },
   {
    "t": "Which layer type does gradient accumulation genuinely change?",
    "o": [
     "Layer normalisation",
     "Batch normalisation",
     "Dropout",
     "Convolution"
    ],
    "a": 1,
    "w": "Its statistics come from whatever is in the forward pass - the micro-batch. Layer norm normalises per example and is indifferent to the batch, which is one reason transformers use it."
   }
  ]
 },
 {
  "path": "deep_learning/gradient_clipping.html",
  "title": "Gradient Clipping",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Gradient clipping rescales an oversized gradient down to a maximum norm before the optimiser applies it, preserving direction while bounding step size. It is cheap insurance against the rare exploding gradient that would otherwise throw training off course, and it is standard practice in RNNs and very deep networks, where long chains of multiplication make the occasional huge gradient close to inevitable."
   },
   {
    "t": "What does this module say about “Context first”?",
    "ans": "Most gradients during training are reasonably sized. Occasionally — a badly scaled batch, a long recurrent chain, a numerically unstable loss — one gradient is enormous. Applied directly, w − lr · g can throw a weight far outside the region the optimiser was making sane progress in, and the next few steps are spent recovering rather than learning."
   },
   {
    "t": "What does this module say about “Run Training”?",
    "ans": "Steps 1-2 are ordinary. Step 3 injects a spike 50x the real gradient — an exploding gradient, the kind deep or recurrent nets produce on their own."
   }
  ]
 },
 {
  "path": "deep_learning/gradient_descent_training.html",
  "title": "Gradient Descent",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Your loss oscillates wildly and sometimes increases. The most likely cause is:",
    "o": [
     "The learning rate is too high",
     "The learning rate is too low",
     "Not enough training data",
     "Too many layers"
    ],
    "a": 0,
    "w": "Steps large enough to overshoot the minimum bounce from one wall of the valley to the other. Cutting the learning rate is the first thing to try."
   },
   {
    "t": "The loss decreases, but almost imperceptibly, over thousands of steps. This suggests:",
    "o": [
     "The learning rate is too high",
     "The learning rate is too low",
     "The model has converged",
     "The data needs shuffling"
    ],
    "a": 1,
    "w": "Tiny steps make real but glacial progress. It is the mirror image of the previous failure, and the reason schedules start high and decay rather than picking one value forever."
   },
   {
    "t": "Why subtract the gradient instead of adding it?",
    "o": [
     "To keep weights positive",
     "The gradient points uphill, and the aim is to reduce the loss",
     "To prevent overfitting",
     "Because the loss is negative"
    ],
    "a": 1,
    "w": "The gradient is the direction of steepest increase. Moving against it is what makes the algorithm gradient *descent*."
   }
  ]
 },
 {
  "path": "deep_learning/gradient_descent_batch_processing.html",
  "title": "Gradient Descent Batch Processing",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What is meant by “Batch normalisation” here?",
    "ans": "needs at least about 8 examples per batch for usable statistics. Below that, use GroupNorm."
   },
   {
    "t": "What is meant by “Very large inputs” here?",
    "ans": "— high-resolution images, long sequences — may force a batch of 1 or 2. Gradient accumulation recovers the effective batch size."
   },
   {
    "t": "What is meant by “Small datasets” here?",
    "ans": "give few updates per epoch at a large batch size, so a smaller batch and more updates often trains better."
   }
  ]
 },
 {
  "path": "deep_learning/how_loss_is_calculated.html",
  "title": "How Loss is Calculated",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What is a loss function for?",
    "o": [
     "Measuring how fast the model trains",
     "Turning 'how wrong is this prediction' into one number that can be minimised",
     "Choosing the architecture",
     "Preventing overfitting"
    ],
    "a": 1,
    "w": "Optimisation needs a single scalar to push downhill. The loss is that scalar, and its choice defines what the model treats as an error in the first place."
   },
   {
    "t": "Why use cross-entropy rather than squared error for classification?",
    "o": [
     "It is faster",
     "It punishes confident wrong answers far more sharply, giving usable gradients",
     "It works without probabilities",
     "It cannot overfit"
    ],
    "a": 1,
    "w": "Cross-entropy goes to infinity as a confident prediction turns out wrong. Squared error caps out, so a badly wrong classifier gets only a weak nudge to fix itself."
   },
   {
    "t": "Training loss is falling but validation loss has started to rise. This means:",
    "o": [
     "The learning rate is too low",
     "The model has started overfitting",
     "The data is corrupted",
     "Training has converged"
    ],
    "a": 1,
    "w": "The model is still improving on data it has seen while getting worse on data it has not. That gap opening up is the definition of overfitting, and the point early stopping watches for."
   }
  ]
 },
 {
  "path": "deep_learning/hyper-paramter_tuning.html",
  "title": "Hyperparameter Tuning",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Hyperparameters sit outside gradient descent, so the only way to evaluate them is to train and measure — which makes the search strategy itself worth thinking about. Random search beats grid search at equal budget because it spends its samples on more distinct values of whichever hyperparameter actually matters, and anything spanning orders of magnitude should be sampled on a log scale."
   },
   {
    "t": "What does this module say about “Two kinds of number”?",
    "ans": "A parameter is learned: weights and biases move during training because gradient descent moves them. A hyperparameter is fixed before training and never updated by the optimiser — learning rate, number of layers, neurons per layer, batch size, dropout rate, regularisation strength."
   },
   {
    "t": "What does this module say about “Grid search, random search, and why random usually wins”?",
    "ans": "Grid search tries every combination on a predefined grid. With 5 learning rates and 5 layer widths that is 25 runs, and adding a third hyperparameter with 5 values makes it 125. The cost is exponential in the number of hyperparameters. Random search samples combinations at random from ranges you specify."
   }
  ]
 },
 {
  "path": "deep_learning/label_smoothing.html",
  "title": "Label Smoothing",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Why does a one-hot target make a model overconfident?",
    "o": [
     "It has too few classes",
     "Softmax reaches probability 1 only in the limit, so the optimal logit gap is infinite and training never stops pushing",
     "The gradient is too large",
     "It has no regularisation"
    ],
    "a": 1,
    "w": "The target is unattainable, so widening logits is always an available way to reduce the loss. Smoothing makes the optimal gap finite and reachable."
   },
   {
    "t": "Why does the training loss no longer approach zero?",
    "o": [
     "The model is underfitting",
     "The minimum achievable loss is the entropy of the smoothed target, which is not zero",
     "The learning rate is too low",
     "Label smoothing adds noise"
    ],
    "a": 1,
    "w": "You changed what perfect means. It also means losses are no longer comparable with runs that did not use smoothing."
   },
   {
    "t": "Why should a distillation teacher be trained without label smoothing?",
    "o": [
     "It makes the teacher less accurate",
     "The student learns from the relative sizes of the wrong-class probabilities, and smoothing flattens exactly that",
     "The student cannot handle smoothed targets",
     "It slows distillation down"
    ],
    "a": 1,
    "w": "The informative part is that this dog was slightly cat and not at all lorry. Smoothing erases the dark knowledge distillation depends on."
   }
  ]
 },
 {
  "path": "deep_learning/layer_normalization.html",
  "title": "Layer Normalization",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What does this module say about “Start here”?",
    "ans": "BatchNorm normalizes each feature — each column — using the mean and standard deviation computed across every sample currently in the batch. That is powerful, and it has one structural weakness: its statistics depend on which other examples happen to be in the batch with you, which becomes a real problem at batch size 1 and in architectures like transformers where \"the batch\" is not a stable, meaningful group."
   },
   {
    "t": "What does this module say about “Normalising across features, not across the batch”?",
    "ans": "Batch normalisation standardises each feature using statistics computed across the examples in a batch. Layer normalisation does the opposite: it standardises each example using statistics computed across its own features."
   },
   {
    "t": "What does this module say about “Pre-norm versus post-norm”?",
    "ans": "Where the normalisation sits relative to the residual connection turns out to matter a great deal."
   }
  ]
 },
 {
  "path": "deep_learning/learning_rate_scheduling.html",
  "title": "Learning Rate Scheduling",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Big steps to travel, small steps to arrive — and get the starting size right before tuning the decay."
   },
   {
    "t": "What does this module say about “Why one value cannot serve both phases”?",
    "ans": "Early in training you are far from any good solution and want large steps. Late in training you are close, and large steps make you bounce around the minimum without ever landing in it. A fixed rate forces a compromise that is wrong at both ends."
   },
   {
    "t": "What does this module say about “One rate does not fit the whole run”?",
    "ans": "Early in training the weights are far from anything useful, and large steps make rapid progress. Late in training the model is close to a good solution, and large steps overshoot it repeatedly — the loss plateaus and bounces rather than settling."
   }
  ]
 },
 {
  "path": "deep_learning/linear_regression_with_gradient_descent.html",
  "title": "Linear Regression with Gradient Descent",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Two parameters, the same optimiser as a deep network, and slow enough to watch every step."
   },
   {
    "t": "What does this module say about “The two gradients”?",
    "ans": "You are fitting y = mx + c by minimising mean squared error. The partial derivatives are:"
   },
   {
    "t": "What does this module say about “One step, worked out”?",
    "ans": "Three points: (1, 2), (2, 4), (3, 6). The answer is obviously m = 2, c = 0, but start from m = 0, c = 0 and let the maths find it."
   }
  ]
 },
 {
  "path": "deep_learning/mixed_precision_training.html",
  "title": "Mixed Precision and Loss Scaling",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What does loss scaling change about the parameter update?",
    "o": [
     "It makes updates larger",
     "Nothing - the optimiser unscales first; the scaling only keeps the numbers inside fp16's range",
     "It clips large gradients",
     "It skips small gradients"
    ],
    "a": 1,
    "w": "It is a change of units, not a change of algorithm. Multiply the loss, every gradient scales by the chain rule, divide before stepping."
   },
   {
    "t": "What does dynamic loss scaling do when a gradient overflows?",
    "o": [
     "Clips it to the maximum",
     "Halves the scale and skips the step entirely",
     "Falls back to fp32 for that step",
     "Raises the scale"
    ],
    "a": 1,
    "w": "There is no way to recover what an overflowed gradient should have been, so it is discarded rather than repaired. A few skipped steps early cost nothing."
   },
   {
    "t": "Why does bfloat16 not need loss scaling?",
    "o": [
     "It has more mantissa bits",
     "It has the same exponent range as fp32, and range was the problem",
     "It is computed in software",
     "It rounds differently"
    ],
    "a": 1,
    "w": "bfloat16 trades mantissa bits for exponent bits - less precision, same range. For gradients, precision mostly was not the issue."
   }
  ]
 },
 {
  "path": "deep_learning/reproducibility_of_model.html",
  "title": "Model Reproducibility",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Training draws randomness from initialisation, shuffling, dropout and augmentation, each from its own generator, so reproducibility means seeding all of them rather than one. Even then GPU reductions are non-deterministic at the level of floating-point rounding, and training amplifies those differences over thousands of steps."
   },
   {
    "t": "What does this module say about “Where the randomness comes from”?",
    "ans": "Neural network training is randomised in at least four independent places, and every one of them changes the final weights:"
   },
   {
    "t": "What does this module say about “Seeding, and what a seed actually fixes”?",
    "ans": "These are all pseudo -random: a deterministic sequence generated from a starting value called the seed. Fix the seed and the sequence is identical every run."
   }
  ]
 },
 {
  "path": "deep_learning/model_training_curve.html",
  "title": "Model Training Curves",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Training loss keeps falling while validation loss rises. The right reading is:",
    "o": [
     "Train longer",
     "Stop around where they diverged",
     "Raise the learning rate",
     "Add more layers"
    ],
    "a": 1,
    "w": "The divergence point is where the model stopped learning the pattern and started learning the training set. Everything after it is overfitting."
   },
   {
    "t": "Both curves are flat and high from the very first epoch. Most likely:",
    "o": [
     "The model has converged",
     "The model is not learning at all - bad learning rate, bad initialisation, or a wiring bug",
     "The dataset is too large",
     "Dropout is too low"
    ],
    "a": 1,
    "w": "A model that never improves has not converged, it has failed to start. Check the learning rate first, then whether the labels and the loss are actually connected."
   },
   {
    "t": "Validation loss sits consistently *below* training loss. The usual explanation is:",
    "o": [
     "A bug - this is impossible",
     "Regularisation like dropout penalises the training pass but not the validation pass",
     "The model is overfitting",
     "The validation set is too large"
    ],
    "a": 1,
    "w": "Dropout is on during training and off during validation, so the training number is measured under harder conditions. It is normal early on and not a cause for alarm."
   }
  ]
 },
 {
  "path": "deep_learning/model_training_on_cpu_vs_gpu.html",
  "title": "Model Training on CPU vs GPU",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A GPU trades per-core speed for thousands of cores, which suits neural networks because matrix multiplication is embarrassingly parallel. The speedup is real only when there is enough work in flight to occupy the device, so batch size and layer width matter more than anything else, and the separate memory space means transfers and synchronisations can quietly become the bottleneck."
   },
   {
    "t": "What does this module say about “Latency versus throughput”?",
    "ans": "A CPU has a handful of cores optimised to finish one instruction stream as fast as possible: high clock speeds, deep pipelines, large caches, aggressive branch prediction. It is built for latency."
   },
   {
    "t": "What does this module say about “Why batch size is the variable that matters”?",
    "ans": "Multiplying a 1×512 input by a 512×512 weight matrix uses a tiny fraction of a GPU’s cores; the rest sit idle. Multiply a 256×512 batch by the same weights and the work grows 256-fold while the time barely moves, because that work fills capacity that was already there and already paid for."
   }
  ]
 },
 {
  "path": "deep_learning/neural_network.html",
  "title": "Neural Network Visualizer",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What do the hidden layers of a network actually do?",
    "o": [
     "Store the training data",
     "Build progressively more useful representations of the input",
     "Reduce the number of parameters",
     "Shuffle the inputs"
    ],
    "a": 1,
    "w": "Each layer re-describes its input in terms the next layer finds easier. That learned re-description is the thing deep learning buys you over hand-engineered features."
   },
   {
    "t": "Widening a layer from 64 to 512 units mainly increases:",
    "o": [
     "Training speed",
     "Capacity - and with it the risk of overfitting",
     "The learning rate",
     "The number of layers"
    ],
    "a": 1,
    "w": "More parameters means more that can be memorised. Extra capacity with no extra data or regularisation is the standard route into overfitting."
   },
   {
    "t": "All weights are initialised to exactly zero. What happens?",
    "o": [
     "Training proceeds normally",
     "Every unit in a layer computes the same thing and stays identical forever",
     "The loss becomes negative",
     "The network trains faster"
    ],
    "a": 1,
    "w": "Identical weights get identical gradients, so the units never differentiate. Random initialisation exists to break exactly this symmetry."
   }
  ]
 },
 {
  "path": "deep_learning/neural_network_for_regression.html",
  "title": "Neural Network for Regression",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What is meant by “Check the input range at prediction time” here?",
    "ans": "and flag or refuse inputs outside it. This is a production concern that is easy to overlook."
   },
   {
    "t": "What is meant by “Model the right quantity” here?",
    "ans": "Predicting price-per-square-metre, or a change rather than a level, often extrapolates far better than predicting the raw level."
   }
  ]
 },
 {
  "path": "deep_learning/neural_network_for_unsupervised_learning.html",
  "title": "Neural Network for Unsupervised Learning",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "No labels needed — make the input the target and let a narrow layer decide what was worth keeping."
   },
   {
    "t": "What does this module say about “The autoencoder trick”?",
    "ans": "An autoencoder is trained to reproduce its own input. On its own that is trivial — copy the input to the output and the loss is zero. The trick is the bottleneck: a hidden layer narrower than the input, which the data must pass through."
   },
   {
    "t": "What does this module say about “A worked shape”?",
    "ans": "8 input features → 3-unit bottleneck → 8 reconstruction outputs. The encoder must express 8 numbers using 3, and the decoder must rebuild all 8 from those 3."
   }
  ]
 },
 {
  "path": "deep_learning/optimizers_in_3d.html",
  "title": "Optimizers in 3D",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What is meant by “Small batches generalise slightly better” here?",
    "ans": "because their gradient noise makes it hard to settle into a narrow crevice."
   },
   {
    "t": "What is meant by “Very large batches sometimes generalise worse” here?",
    "ans": ", and techniques like LARS and longer warm-up exist to counter it."
   },
   {
    "t": "What is meant by “Weight averaging” here?",
    "ans": "(SWA) averages weights from several late-training points, landing nearer the centre of a basin than any individual point."
   },
   {
    "t": "What is meant by “Sharpness-aware minimisation” here?",
    "ans": "(SAM) explicitly penalises sharpness by taking a step towards the worst nearby point before updating."
   }
  ]
 },
 {
  "path": "deep_learning/optimizers_in_neural_networks.html",
  "title": "Optimizers in Neural Networks",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Same downhill direction, different memory — and memory is what stops you bouncing off the walls."
   },
   {
    "t": "What does this module say about “What each one adds”?",
    "ans": "Picture a long narrow valley where the gradient across the valley is 10 and along it is 0.1. With η = 0.01, SGD steps 0.1 across and 0.001 along — a hundred to one. It bounces off the steep walls while creeping toward the actual minimum."
   },
   {
    "t": "What does this module say about “Why plain SGD zig-zags”?",
    "ans": "Picture a long narrow valley where the gradient across the valley is 10 and along it is 0.1. With η = 0.01, SGD steps 0.1 across and 0.001 along — a hundred to one. It bounces off the steep walls while creeping toward the actual minimum."
   }
  ]
 },
 {
  "path": "deep_learning/overfitting_vs_underfitting.html",
  "title": "Overfitting vs Underfitting",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Training accuracy 99%, validation accuracy 62%. This is:",
    "o": [
     "Underfitting",
     "Overfitting",
     "A good model",
     "Data leakage"
    ],
    "a": 1,
    "w": "The model has learned the training set specifically, including its noise, and cannot generalise. A large gap between the two scores is the tell."
   },
   {
    "t": "Training accuracy 61%, validation accuracy 60%. This is:",
    "o": [
     "Underfitting - the model is too simple for the problem",
     "Overfitting",
     "Ideal",
     "Impossible"
    ],
    "a": 0,
    "w": "Both scores are poor and close together, so nothing is being memorised - there simply is not enough capacity, or enough training, to capture the pattern."
   },
   {
    "t": "Which change would you expect to reduce overfitting?",
    "o": [
     "Adding more layers",
     "Adding more training data",
     "Training for more epochs",
     "Raising the learning rate"
    ],
    "a": 1,
    "w": "More data makes memorisation harder and generalisation easier. The other three all push capacity or fitting further in the direction that caused the problem."
   }
  ]
 },
 {
  "path": "deep_learning/perceptron.html",
  "title": "Perceptron Classifier",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "A single perceptron cannot learn XOR. Why not?",
    "o": [
     "XOR needs more training data",
     "XOR is not linearly separable, and one perceptron draws one straight boundary",
     "XOR requires a sigmoid activation",
     "The learning rate is always too high"
    ],
    "a": 1,
    "w": "No single straight line separates XOR's two classes. No choice of weights and bias fixes that - it is a limit of the shape the model can express, which is what stacking layers solves."
   },
   {
    "t": "What does the bias term let a neuron do?",
    "o": [
     "Learn faster",
     "Shift its decision boundary away from the origin",
     "Rotate its decision boundary",
     "Handle more inputs"
    ],
    "a": 1,
    "w": "Weights rotate the boundary; the bias translates it. Without a bias every boundary is nailed to the origin, which is a severe and usually pointless restriction."
   },
   {
    "t": "Why can a step activation not be trained by backpropagation?",
    "o": [
     "It is too slow",
     "Its gradient is zero everywhere it is defined, so there is nothing to descend",
     "It only outputs integers",
     "It needs too much memory"
    ],
    "a": 1,
    "w": "Backpropagation moves weights along the gradient. A flat function gives a gradient of zero everywhere, so no weight ever updates. This is precisely why sigmoid and then ReLU replaced it."
   }
  ]
 },
 {
  "path": "deep_learning/regularization_in_neural_networks.html",
  "title": "Regularization Techniques",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Regularisation adds a weight-size penalty to the loss so the optimiser trades fit against simplicity, with λ setting the rate. L2 shrinks all weights proportionally and keeps every feature; L1 applies constant pressure and drives weights to exactly zero, producing a sparse, self-selecting model. Use it when the model overfits, scale the features first, and reach for AdamW if the optimiser is Adam."
   },
   {
    "t": "What does this module say about “Penalising complexity”?",
    "ans": "An overfitting model has found a way to fit noise, and doing that almost always requires large weights — sharp, wiggly functions need big coefficients. Regularisation exploits that by adding the size of the weights to the loss:"
   },
   {
    "t": "What does this module say about “L1 and L2, and why one is sparse”?",
    "ans": "L2 (ridge, weight decay) penalises the sum of squared weights: penalty = Σ w i ² → gradient = 2w i"
   }
  ]
 },
 {
  "path": "deep_learning/residual_connections.html",
  "title": "Residual and Skip Connections",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What does this module say about “What this is”?",
    "ans": "Stack enough layers and, by the chain rule, the gradient reaching an early layer is the product of every local derivative between it and the loss. If each of those derivatives is reliably less than 1 — true of sigmoid and tanh almost everywhere — the product shrinks geometrically."
   },
   {
    "t": "What does this module say about “The Stack”?",
    "ans": "every layer squashes its input by the same factor (local derivative 0.55) — realistic for a deep sigmoid/tanh stack"
   },
   {
    "t": "What does this module say about “The two reasons it works”?",
    "ans": "Identity becomes easy to represent. Ask a block to produce the output directly and it must learn a mapping. Ask it to produce the difference and it can output nothing — drive the weights towards zero — and the block passes its input through unchanged."
   }
  ]
 },
 {
  "path": "deep_learning/seq2seq_and_beam_search.html",
  "title": "Seq2seq and Beam Search",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Why can greedy decoding produce a worse sequence than beam search?",
    "o": [
     "It is faster",
     "It maximises the next token, not the whole sequence, and cannot reconsider an early commitment",
     "It ignores the encoder",
     "It has no length normalisation"
    ],
    "a": 1,
    "w": "The highest-probability first token can lead into a region where everything that follows is bad, and greedy decoding has no way back."
   },
   {
    "t": "Why does beam search need length normalisation?",
    "o": [
     "To speed it up",
     "Sequence probability is a product, so every extra token lowers it and short sequences win by default",
     "To handle the beam width",
     "To avoid repeated tokens"
    ],
    "a": 1,
    "w": "Unnormalised beam search has a systematic bias toward stopping early. The fix has no principled derivation and every production decoder has one."
   },
   {
    "t": "Why does a very wide beam often make translation worse?",
    "o": [
     "It overfits",
     "It searches the model's objective more faithfully, and very high-probability text is bland",
     "It runs out of memory",
     "It discards the correct path"
    ],
    "a": 1,
    "w": "The beam search curse. It is also why open-ended generation uses sampling instead - for creative text the most probable path is the boring one."
   }
  ]
 },
 {
  "path": "deep_learning/softmax_and_cross_entropy.html",
  "title": "Softmax and Cross-Entropy",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A network's final layer produces one raw number per class. These are called logits , and they can be anything: 8.2, −3.1, 0.0. They are not probabilities — they do not sit between 0 and 1 and they do not add up to anything in particular."
   },
   {
    "t": "What does this module say about “From scores to probabilities”?",
    "ans": "A classifier's final layer outputs one unbounded number per class — a logit. Softmax turns those into probabilities:"
   },
   {
    "t": "What does this module say about “The loss that goes with it”?",
    "ans": "Cross-entropy measures how far the predicted distribution is from the truth. With a one-hot target the sum collapses to a single term:"
   }
  ]
 },
 {
  "path": "deep_learning/vanishing_vs_exploding_gradient.html",
  "title": "Vanishing & Exploding Gradients",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Backpropagation multiplies per-layer derivatives together, so anything consistently below 1 shrinks the gradient exponentially with depth and anything above 1 amplifies it. Sigmoid’s maximum derivative of 0.25 made deep networks untrainable; ReLU’s derivative of 1 fixed it, and initialisation, normalisation and residual connections keep the product near 1 by design."
   },
   {
    "t": "What does this module say about “Where both problems come from”?",
    "ans": "Backpropagation computes the gradient at an early layer by multiplying together the local derivatives of every layer above it. For a network of depth L that is a product of L terms."
   },
   {
    "t": "What does this module say about “Why sigmoid made it worse”?",
    "ans": "The derivative of the sigmoid is σ(x)(1 − σ(x)) , which peaks at 0.25 when x = 0 and falls toward zero for inputs of large magnitude."
   }
  ]
 },
 {
  "path": "deep_learning/variational_autoencoders.html",
  "title": "Variational Autoencoders",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "What does the encoder of a VAE output?",
    "o": [
     "A single point",
     "A mean and a standard deviation",
     "A probability per class",
     "A reconstruction"
    ],
    "a": 1,
    "w": "The code is sampled from that distribution, so the same input gives different codes on different passes and the decoder must handle a neighbourhood rather than a point."
   },
   {
    "t": "What problem does the reparameterisation trick solve?",
    "o": [
     "The latent space is too large",
     "You cannot backpropagate through a sampling operation, so the randomness is moved into an input instead",
     "The KL term is intractable",
     "The decoder is too weak"
    ],
    "a": 1,
    "w": "z = mu + sigma*epsilon makes the expression an ordinary differentiable function of mu and sigma with epsilon fixed. VAEs were not trainable without it."
   },
   {
    "t": "What is posterior collapse?",
    "o": [
     "The decoder stops training",
     "The KL term wins, the encoder outputs the prior regardless of input, and the decoder ignores the latent",
     "The latent space develops gaps",
     "The reconstruction error diverges"
    ],
    "a": 1,
    "w": "The opposite failure - reconstruction winning - gives tight clusters with empty space between them, where sampling lands in the gaps."
   }
  ]
 },
 {
  "path": "deep_learning/weight_initialization.html",
  "title": "Weight Initialization Methods",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Initialisation must be random to break symmetry, and scaled to layer width so activation and gradient variance stay roughly constant with depth. He initialisation is the default for ReLU networks because ReLU halves the variance and He’s factor of 2 restores it; Xavier suits tanh and sigmoid. Get this wrong and a deep network either learns nothing or diverges — before the optimiser has had any say in the matter."
   },
   {
    "t": "What does this module say about “Why not zero, and why not all-equal”?",
    "ans": "Initialising every weight to zero seems harmless and completely breaks the network. If all weights in a layer are identical, every neuron in that layer computes the same output, receives the same gradient, and applies the same update — so they stay identical forever. A layer of 512 such neurons has the expressive power of one."
   },
   {
    "t": "What does this module say about “The variance is what actually matters”?",
    "ans": "Randomness alone is not enough; the scale of the random values decides whether signal survives depth. Each layer multiplies its input by a weight matrix, so the variance of the activations is multiplied layer by layer."
   }
  ]
 },
 {
  "path": "deep_learning/weights_and_biases.html",
  "title": "Weights & Biases",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Weights decide direction and strength; the bias decides where the threshold sits."
   },
   {
    "t": "What does this module say about “What each one does geometrically”?",
    "ans": "A neuron computes z = w · x + b . Those two terms do different jobs, and it is worth separating them:"
   },
   {
    "t": "What does this module say about “A concrete example”?",
    "ans": "One input, weight w = 2.0 , bias b = 0 . At x = 0.5 you get z = 1.0 — the neuron fires."
   }
  ]
 },
 {
  "path": "fastapi/apirouter.html",
  "title": "APIRouter",
  "cat": "FastAPI",
  "q": [
   {
    "t": "What does `prefix` on an APIRouter do?",
    "o": [
     "Renames the router",
     "Prepends to every path in it",
     "Sets a tag",
     "Adds a dependency"
    ],
    "a": 1,
    "w": "It applies to every route in the router, so `@router.get(\"\")` with `prefix=\"/modules\"` becomes `/modules`. Tags, set the same way, group the routes in the docs."
   },
   {
    "t": "Why can a fixed route in one router be unreachable?",
    "o": [
     "A bug",
     "Inclusion order sets match order, so an earlier router's variable route shadows it",
     "Routers are unordered",
     "Prefixes conflict"
    ],
    "a": 1,
    "w": "Across routers, inclusion order is match order - and the mistake is harder to spot because the two routes live in different files."
   },
   {
    "t": "What does `dependencies=[...]` on a router do?",
    "o": [
     "Nothing",
     "Applies to every route in it, running for its effect",
     "Passes the value to each handler",
     "Only documents them"
    ],
    "a": 1,
    "w": "It runs for every route in the section. The return value is not injected; a handler that needs it declares its own Depends, and the result is cached within the request."
   },
   {
    "t": "When should you create a routers/ directory?",
    "o": [
     "After 50 endpoints",
     "On day one, even with two",
     "Never",
     "Only for large teams"
    ],
    "a": 1,
    "w": "Moving three routes is trivial and moving eighty is a weekend - and by then something depends on the import layout."
   }
  ]
 },
 {
  "path": "fastapi/class_dependencies.html",
  "title": "Class Dependencies",
  "cat": "FastAPI",
  "q": [
   {
    "t": "Why is a class a valid dependency?",
    "o": [
     "FastAPI special-cases classes",
     "Depends takes any callable, and calling a class constructs an instance",
     "Only Pydantic models work",
     "It is not"
    ],
    "a": 1,
    "w": "FastAPI reads `__init__`'s signature the way it reads a function's, so its parameters become request parameters and the handler receives the instance."
   },
   {
    "t": "What does `Depends()` with no argument use?",
    "o": [
     "The first dependency",
     "The parameter's type annotation as the callable",
     "Nothing",
     "The handler name"
    ],
    "a": 1,
    "w": "For a class dependency the annotation and the callable are the same thing, so the argument is redundant."
   },
   {
    "t": "When does `RequireRole(\"admin\")` run?",
    "o": [
     "Per request",
     "Once at import; only `__call__` runs per request",
     "Never",
     "Once per worker per request"
    ],
    "a": 1,
    "w": "Configuration belongs in `__init__` and per-request work in `__call__`. The instance is shared across requests, so mutable state on `self` is shared too."
   },
   {
    "t": "When is a plain function the better choice?",
    "o": [
     "Always",
     "When the dependency holds no configuration, state or methods",
     "Never",
     "Only for headers"
    ],
    "a": 1,
    "w": "Most dependencies just read parameters and hand them over. A class without configuration or behaviour is the same thing with more ceremony."
   }
  ]
 },
 {
  "path": "fastapi/dependencies_with_yield.html",
  "title": "Dependencies with yield",
  "cat": "FastAPI",
  "q": [
   {
    "t": "When does the code after `yield` run?",
    "o": [
     "Immediately",
     "After the response has been produced",
     "Only on success",
     "Never"
    ],
    "a": 1,
    "w": "Setup, then handler, then teardown - which is why it works for anything with a request-scoped lifetime."
   },
   {
    "t": "A handler raises a 404. Does the teardown run?",
    "o": [
     "No",
     "Yes, if the yield is inside a try/finally",
     "Only for 500s",
     "Only for async dependencies"
    ],
    "a": 1,
    "w": "That is the reason to use yield rather than a plain return. Without `try/finally` a failing handler skips the close and leaks the connection."
   },
   {
    "t": "Where does `db.commit()` belong in the transaction pattern?",
    "o": [
     "Before the yield",
     "Immediately after the yield",
     "In finally",
     "In the handler"
    ],
    "a": 1,
    "w": "It is only reached when the handler completed without raising. An `except` clause rolls back and re-raises; `finally` closes either way."
   },
   {
    "t": "Cleanup itself fails. What should the teardown do?",
    "o": [
     "Raise",
     "Catch and log it",
     "Return a 500",
     "Retry forever"
    ],
    "a": 1,
    "w": "The response is already decided and being sent, so an exception there cannot become a clean error - and may truncate the response instead."
   }
  ]
 },
 {
  "path": "fastapi/dependency_injection.html",
  "title": "Dependency Injection",
  "cat": "FastAPI",
  "q": [
   {
    "t": "What is a FastAPI dependency?",
    "o": [
     "A registered class",
     "An ordinary function called by Depends",
     "A middleware",
     "A Pydantic model"
    ],
    "a": 1,
    "w": "No registry, no container, no base class. `Depends(fn)` calls the function and passes the result, and the function's own parameters are request parameters."
   },
   {
    "t": "Two parameters depend on the same function. How many times is it called?",
    "o": [
     "Twice",
     "Once - the result is cached for the request",
     "Once globally",
     "Depends on the type"
    ],
    "a": 1,
    "w": "Caching is per request, which matters because dependencies compose - a handler and a sub-dependency both needing `current_user` decode the token once, not twice."
   },
   {
    "t": "Why is a dependency the right place for authentication?",
    "o": [
     "It is faster",
     "Raising there stops the request before the handler runs, and the rule is stated once",
     "It is required",
     "It hides the header from the docs"
    ],
    "a": 1,
    "w": "No endpoint can forget the check and no two can check differently - and the header still appears in the schema, because the dependency declares it."
   },
   {
    "t": "Do a dependency's parameters appear in the API documentation?",
    "o": [
     "No, they are internal",
     "Yes - as the endpoint's own parameters",
     "Only headers do",
     "Only with a flag"
    ],
    "a": 1,
    "w": "As far as a caller is concerned they are the endpoint's parameters, so the abstraction hides nothing from the contract."
   }
  ]
 },
 {
  "path": "fastapi/dependency_overrides.html",
  "title": "Dependency Overrides",
  "cat": "FastAPI",
  "q": [
   {
    "t": "What is `app.dependency_overrides` keyed by?",
    "o": [
     "The dependency's name",
     "The function object itself",
     "The route path",
     "A string id"
    ],
    "a": 1,
    "w": "It is keyed by identity, so importing the same function by two different paths gives two objects and the override silently targets the wrong one."
   },
   {
    "t": "You override a dependency at the bottom of a tree. What happens above it?",
    "o": [
     "Nothing",
     "Everything built on it uses the replacement",
     "It raises",
     "Only direct users change"
    ],
    "a": 1,
    "w": "That is why you should fake as low as possible - overriding the top skips the logic you wanted to test, while overriding the edge lets it run."
   },
   {
    "t": "Why clear overrides between tests?",
    "o": [
     "Performance",
     "They live on the app, so one test silently changes every later one",
     "They leak memory",
     "They are read-only"
    ],
    "a": 1,
    "w": "The failure appears in an unrelated test with no obvious cause. A fixture that sets, yields and clears is the standard shape."
   },
   {
    "t": "Can a router-level dependency be overridden?",
    "o": [
     "No",
     "Yes - overrides replace the function wherever it is declared",
     "Only with middleware",
     "Only at app level"
    ],
    "a": 1,
    "w": "Which is what makes a router-wide auth requirement testable; otherwise every test of every route in that section would need a valid credential."
   }
  ]
 },
 {
  "path": "fastapi/error_handling.html",
  "title": "Error Handling",
  "cat": "FastAPI",
  "q": [
   {
    "t": "Where can `HTTPException` be raised?",
    "o": [
     "Only in the handler",
     "Anywhere in the call stack",
     "Only in dependencies",
     "Only in middleware"
    ],
    "a": 1,
    "w": "It is an exception, so it unwinds. A function five levels deep can refuse the request without every caller checking a return value."
   },
   {
    "t": "Why raise `ModuleNotFound` in a service rather than `HTTPException(404)`?",
    "o": [
     "It is faster",
     "The service may also be called from a job, a CLI or a test, none of which have a request to answer",
     "HTTPException is deprecated",
     "No reason"
    ],
    "a": 1,
    "w": "Business logic that imports fastapi can only be used from a request. Mapping the domain error to a status at the edge keeps the service reusable and testable."
   },
   {
    "t": "What should an `Exception` handler return to the client?",
    "o": [
     "The traceback",
     "A generic message plus a correlation id",
     "The exception type",
     "Nothing"
    ],
    "a": 1,
    "w": "A traceback names files, versions and sometimes values - an information leak. Log it, and give the caller an id they can quote."
   },
   {
    "t": "You override the `HTTPException` handler. What is easy to forget?",
    "o": [
     "The status code and `exc.headers`",
     "The detail",
     "The path",
     "Async"
    ],
    "a": 0,
    "w": "Hard-coding a status breaks every non-404, and dropping `exc.headers` silently discards things like `Retry-After` and `WWW-Authenticate`."
   }
  ]
 },
 {
  "path": "fastapi/form_data_and_files.html",
  "title": "Form Data and File Uploads",
  "cat": "FastAPI",
  "q": [
   {
    "t": "You declare `username: str` with no marker on a POST endpoint. Where does FastAPI look?",
    "o": [
     "The form body",
     "The query string",
     "A header",
     "The JSON body"
    ],
    "a": 1,
    "w": "A plain parameter defaults to a query parameter. `Form()` is what tells FastAPI the value is in a form-encoded body."
   },
   {
    "t": "Why is `UploadFile` preferable to a `bytes` parameter?",
    "o": [
     "It is faster",
     "Large uploads are spooled to disk instead of held in memory",
     "It validates the content",
     "It is required"
    ],
    "a": 1,
    "w": "Reading a whole upload into RAM is fine for an avatar and a denial-of-service vector for anything larger."
   },
   {
    "t": "Can you safely use `file.filename` to build a save path?",
    "o": [
     "Yes",
     "No - it is attacker-controlled and can contain `..` or absolute paths",
     "Only for images",
     "Only if it is short"
    ],
    "a": 1,
    "w": "It comes from the client and can say anything. Generate your own name and keep the original only as display metadata."
   },
   {
    "t": "What does FastAPI do about upload size by default?",
    "o": [
     "Caps it at 1MB",
     "Nothing - it is unlimited",
     "Rejects over 10MB",
     "Streams it away"
    ],
    "a": 1,
    "w": "Nothing caps it. Read with a limit in the handler, and set one in whatever sits in front of the app, since the bytes arrive before your code runs."
   }
  ]
 },
 {
  "path": "fastapi/http_methods_and_routing.html",
  "title": "HTTP Methods and Routing",
  "cat": "FastAPI",
  "q": [
   {
    "t": "A GET request is prefetched by a browser and your handler deletes something. Whose bug is it?",
    "o": [
     "The browser's",
     "Yours - GET must be safe",
     "Nobody's",
     "The proxy's"
    ],
    "a": 1,
    "w": "Browsers prefetch, proxies cache and monitoring replays, all on the assumption that GET changes nothing. A destructive GET will eventually be called by something that was not a person."
   },
   {
    "t": "What does a 405 tell you that a 404 does not?",
    "o": [
     "Nothing",
     "The path matched a route, but not for that method",
     "The server is down",
     "The body was invalid"
    ],
    "a": 1,
    "w": "405 means the URL is right and the verb is wrong - usually a typo in the decorator or a client using the wrong method. A 404 means nothing matched at all."
   },
   {
    "t": "Why can a client safely retry a failed PUT but not a failed POST?",
    "o": [
     "PUT is faster",
     "PUT is idempotent - repeating it leaves the same state",
     "POST has no body",
     "It cannot"
    ],
    "a": 1,
    "w": "A repeated PUT replaces the same resource with the same content. A repeated POST creates a second record, which is why a timed-out POST leaves a client genuinely uncertain."
   },
   {
    "t": "Where do routes registered on an APIRouter sit in match order?",
    "o": [
     "Always first",
     "In the order the routers were included",
     "Alphabetically",
     "Always last"
    ],
    "a": 1,
    "w": "Inclusion order determines match order, so a catch-all in an early router can shadow a more specific route in a later one."
   }
  ]
 },
 {
  "path": "fastapi/headers_and_cookies.html",
  "title": "Headers and Cookies",
  "cat": "FastAPI",
  "q": [
   {
    "t": "Why does `x_token: str = Header()` read the `x-token` header?",
    "o": [
     "Coincidence",
     "Underscores are converted to hyphens, since header names are not valid identifiers",
     "It reads `x_token` literally",
     "Only with a config flag"
    ],
    "a": 1,
    "w": "Most header names contain hyphens and none are valid Python identifiers, so the conversion is automatic. `convert_underscores=False` turns it off."
   },
   {
    "t": "What belongs in a header rather than a query parameter?",
    "o": [
     "A search term",
     "A filter",
     "Metadata about the request, like auth or content negotiation",
     "An identifier"
    ],
    "a": 2,
    "w": "Headers carry metadata about the request. Data belongs where it can be seen, bookmarked and linked - the URL or the body."
   },
   {
    "t": "Why set `httponly=True` on a session cookie?",
    "o": [
     "It is faster",
     "Page JavaScript cannot read it, so an injected script cannot steal the session",
     "It encrypts the value",
     "It stops CSRF"
    ],
    "a": 1,
    "w": "It keeps the value out of reach of scripts. CSRF is a different problem, addressed by `samesite`."
   },
   {
    "t": "Where should reading an `Authorization` header live?",
    "o": [
     "In every handler",
     "In a dependency",
     "In middleware only",
     "In the model"
    ],
    "a": 1,
    "w": "Doing it per handler means the same four lines in thirty functions and the thirty-first forgetting. A dependency does it once and each endpoint declares one parameter."
   }
  ]
 },
 {
  "path": "fastapi/path_parameters.html",
  "title": "Path Parameters",
  "cat": "FastAPI",
  "q": [
   {
    "t": "Can a path parameter be optional?",
    "o": [
     "Yes, with a default",
     "No - it is part of the URL, so omitting it is a different URL",
     "Only with Path()",
     "Only if it is a string"
    ],
    "a": 1,
    "w": "A request without the segment is a request to a different path. If you want both shapes, declare two routes."
   },
   {
    "t": "What is `loc` for a failed path parameter?",
    "o": [
     "('body', 'module_id')",
     "('path', 'module_id')",
     "('module_id',)",
     "()"
    ],
    "a": 1,
    "w": "The first element names which part of the request failed - path, query, header or body - which is what lets a client point the user at the right thing."
   },
   {
    "t": "Why annotate a path parameter as `Enum` rather than `str`?",
    "o": [
     "It is faster",
     "Clear error listing the options, an enumeration in the schema, and checked comparisons in your handler",
     "It is required",
     "To allow slashes"
    ],
    "a": 1,
    "w": "A `str` accepts anything and documents nothing. The enum gives the caller the permitted values and gives a generated client a real type."
   },
   {
    "t": "What does `{full_path:path}` do that a plain parameter does not?",
    "o": [
     "Makes it optional",
     "Matches across slashes",
     "Validates it as a file",
     "Makes it required"
    ],
    "a": 1,
    "w": "A plain parameter stops at the next slash. Note that a `:path` value can contain `..`, so building a filesystem path from one without checking is a traversal vulnerability."
   }
  ]
 },
 {
  "path": "fastapi/query_parameters.html",
  "title": "Query Parameters",
  "cat": "FastAPI",
  "q": [
   {
    "t": "How does FastAPI decide a parameter is a query parameter?",
    "o": [
     "It must be declared with Query()",
     "By elimination - not in the path, not a model, not a dependency",
     "By its type",
     "It must have a default"
    ],
    "a": 1,
    "w": "Query is the fallback classification, which is why `limit: int = 10` works with no ceremony. `Query()` is only needed to add constraints or to disambiguate a list."
   },
   {
    "t": "Why does a list query parameter need `Query(default=[])` rather than `= []`?",
    "o": [
     "Style",
     "Without the marker a list annotation is read as a request body",
     "Lists are not supported otherwise",
     "To make it required"
    ],
    "a": 1,
    "w": "The explicit marker tells FastAPI where the value comes from. Without it, the list annotation is classified as a body."
   },
   {
    "t": "What does `?on=false` give a `bool` parameter?",
    "o": [
     "True, because the string is non-empty",
     "False",
     "A 422",
     "None"
    ],
    "a": 1,
    "w": "Pydantic reads the word's meaning, not the container's emptiness - unlike `bool(\"false\")` in plain Python, which is True. That is what makes query flags work."
   },
   {
    "t": "Why use `Literal` for a `sort` parameter instead of `str`?",
    "o": [
     "It is faster",
     "An unrecognised value fails loudly instead of silently falling back to a default",
     "It is required",
     "To allow lists"
    ],
    "a": 1,
    "w": "A plain `str` accepts `?sort=colour`, falls through to whatever your code does with an unknown key, and nobody is told. That is how results end up subtly wrong for weeks."
   }
  ]
 },
 {
  "path": "fastapi/reading_a_422.html",
  "title": "Reading a 422",
  "cat": "FastAPI",
  "q": [
   {
    "t": "What is the first element of `loc` in a FastAPI validation error?",
    "o": [
     "The field name",
     "The part of the request - path, query, header, cookie or body",
     "The model name",
     "The status code"
    ],
    "a": 1,
    "w": "It tells the caller where to look. Code that reads `loc[0]` as a field name is wrong here in a way it was not in plain Pydantic."
   },
   {
    "t": "A request for `/modules/99` is well-formed but no module 99 exists. What should it return?",
    "o": [
     "422",
     "404",
     "400",
     "409"
    ],
    "a": 1,
    "w": "The request fitted the declared shape perfectly. Nothing with that id exists, which is a fact about the world - so your code raises HTTPException(404)."
   },
   {
    "t": "Why assert on `type` rather than `msg` in a test?",
    "o": [
     "type is shorter",
     "Messages are prose and get reworded between releases",
     "msg is always empty",
     "No difference"
    ],
    "a": 1,
    "w": "Type codes are stable identifiers. Matching on prose makes the suite fail on a wording change, which teaches a team to distrust it."
   },
   {
    "t": "How do you return a different error envelope for validation failures?",
    "o": [
     "Change the model",
     "An `@app.exception_handler(RequestValidationError)`",
     "A middleware",
     "You cannot"
    ],
    "a": 1,
    "w": "The handler receives the exception and returns whatever JSON shape your clients expect - keeping the 422 status, and logging the original errors for diagnosis."
   }
  ]
 },
 {
  "path": "fastapi/request_bodies.html",
  "title": "Request Bodies",
  "cat": "FastAPI",
  "q": [
   {
    "t": "How does FastAPI know a parameter is the request body?",
    "o": [
     "It must be called `body`",
     "It is annotated with a Pydantic model",
     "It uses Body()",
     "It is the last parameter"
    ],
    "a": 1,
    "w": "A model annotation is the signal. Path names come from the route, and anything else defaults to a query parameter."
   },
   {
    "t": "What is `loc` for a bad field inside the second item of a list in the body?",
    "o": [
     "('minutes',)",
     "('body', 'minutes')",
     "('body', 'lessons', 1, 'minutes')",
     "()"
    ],
    "a": 2,
    "w": "The path names the source, the field, the index and the inner field - which for a large payload is the entire diagnosis."
   },
   {
    "t": "A client sends `minuets` instead of `minutes`. What happens by default?",
    "o": [
     "422",
     "The key is ignored and `minutes` takes its default",
     "The value is stored anyway",
     "A warning"
    ],
    "a": 1,
    "w": "Pydantic ignores unknown keys unless told otherwise. `extra=\"forbid\"` makes it a 422 - usually right for an internal API, weighed against forward compatibility for a public one."
   },
   {
    "t": "What distinguishes PUT from PATCH?",
    "o": [
     "Nothing",
     "PUT replaces the whole resource; PATCH updates part of it",
     "PUT is for creation",
     "PATCH cannot take a body"
    ],
    "a": 1,
    "w": "A PUT body should be complete, and an omitted field means clearing it. PATCH updates only what was sent, which is what `model_dump(exclude_unset=True)` is for."
   }
  ]
 },
 {
  "path": "fastapi/response_models.html",
  "title": "Response Models",
  "cat": "FastAPI",
  "q": [
   {
    "t": "What happens without a `response_model`?",
    "o": [
     "Nothing is returned",
     "Whatever the handler returns is serialised, including internal fields",
     "A 500",
     "Only declared fields are sent"
    ],
    "a": 1,
    "w": "The framework sends what you gave it. That is how a column added to a table later silently starts appearing in an API response."
   },
   {
    "t": "A handler returns `{\"id\": \"abc\"}` where the response model declares `id: int`. What does the caller get?",
    "o": [
     "The string",
     "A 422",
     "A 500",
     "None"
    ],
    "a": 2,
    "w": "The caller sent nothing wrong; your code broke its own contract, so it is a server error. Without a response model that malformed value would have shipped."
   },
   {
    "t": "Why use separate Create and Out models?",
    "o": [
     "Performance",
     "What a caller may send and what they may see are different questions",
     "It is required",
     "To avoid validation"
    ],
    "a": 1,
    "w": "A single model with everything optional documents nothing - no client can tell what is guaranteed in either direction."
   },
   {
    "t": "Your handler returns an ORM row and the response model raises. What is usually missing?",
    "o": [
     "response_model_exclude_none",
     "`from_attributes=True` on the output model",
     "A status code",
     "An alias"
    ],
    "a": 1,
    "w": "By default a model validates from a mapping. `from_attributes=True` - `orm_mode` in Pydantic v1 - lets it read attributes off an object instead."
   }
  ]
 },
 {
  "path": "fastapi/router_and_global_dependencies.html",
  "title": "Router and Global Dependencies",
  "cat": "FastAPI",
  "q": [
   {
    "t": "What happens to the return value of a router-level dependency?",
    "o": [
     "It is injected into every handler",
     "It is discarded - the dependency runs for its effect",
     "It becomes a header",
     "It is cached globally"
    ],
    "a": 1,
    "w": "There is no parameter to receive it. A handler needing the value declares its own Depends, and per-request caching means the function still runs once."
   },
   {
    "t": "What is the main argument for a router-level dependency over per-route?",
    "o": [
     "Performance",
     "A route added later is protected without anyone remembering",
     "Better docs",
     "It is required"
    ],
    "a": 1,
    "w": "Per-route protection works until somebody adds one and does not know the convention. Nothing fails, no test covers it, and the gap is found by someone looking."
   },
   {
    "t": "In what order do app, router and route dependencies run?",
    "o": [
     "Route first",
     "Outermost first - app, then router, then route",
     "Alphabetically",
     "Undefined"
    ],
    "a": 1,
    "w": "They stack rather than replace, so each layer adds a rule and can rely on the ones outside it having passed."
   },
   {
    "t": "Authentication across a section: dependency or middleware?",
    "o": [
     "Middleware - it is cross-cutting",
     "A dependency - it is about the endpoints, appears in the schema, and can be overridden in tests",
     "Either is equal",
     "Neither"
    ],
    "a": 1,
    "w": "Middleware runs before routing, cannot declare parameters, is invisible to the docs and is awkward to exempt or override. Reserve it for things that apply to every request regardless of route."
   }
  ]
 },
 {
  "path": "fastapi/status_codes.html",
  "title": "Status Codes",
  "cat": "FastAPI",
  "q": [
   {
    "t": "Why is returning 200 with an error body a problem?",
    "o": [
     "It is slower",
     "Retries, caches, monitoring and client error handling all branch on the status class",
     "It is invalid HTTP",
     "It breaks JSON"
    ],
    "a": 1,
    "w": "The first digit drives behaviour in code you did not write. A 200 means every caller must parse your body to learn something the protocol had a field for, and your error rate reads as zero."
   },
   {
    "t": "What must a 204 response contain?",
    "o": [
     "An empty object",
     "Nothing at all",
     "A message",
     "The deleted id"
    ],
    "a": 1,
    "w": "Declare `status_code=204` and return None. A body makes the response malformed - some clients error, others silently ignore it, which is worse."
   },
   {
    "t": "A signed-in reader tries an admin-only delete. Which code?",
    "o": [
     "401",
     "403",
     "422",
     "404"
    ],
    "a": 1,
    "w": "401 means unauthenticated - I do not know who you are. Here we do, and they are not allowed, which is 403. Collapsing the two makes clients loop on re-authentication."
   },
   {
    "t": "A create request is valid but the slug already exists. Which code?",
    "o": [
     "422",
     "400",
     "409",
     "404"
    ],
    "a": 2,
    "w": "Nothing about the payload was malformed - the same body would have worked a minute earlier. That is a conflict with current state, which is 409."
   }
  ]
 },
 {
  "path": "fastapi/sub_dependencies.html",
  "title": "Sub-dependencies",
  "cat": "FastAPI",
  "q": [
   {
    "t": "A sub-dependency is reached by three different paths in one request. How many times does it run?",
    "o": [
     "Three",
     "Once - the cache covers the whole tree",
     "Depends on order",
     "Once per path"
    ],
    "a": 1,
    "w": "In a real application `current_user` is reached several ways, and without the cache the token would be decoded repeatedly. This is where caching stops being an optimisation."
   },
   {
    "t": "A dependency in the middle of the tree raises. What runs after it?",
    "o": [
     "Everything else",
     "Nothing below or after it, including the handler",
     "Only the handler",
     "Only siblings"
    ],
    "a": 1,
    "w": "That short-circuit is what lets a later level assume an earlier one succeeded - and why declaring a check in the signature is safer than remembering it in a handler."
   },
   {
    "t": "A dependency three levels down declares a `limit` query parameter. Does it appear in the docs?",
    "o": [
     "No, it is internal",
     "Yes - as the endpoint's own parameter",
     "Only if re-declared",
     "Only headers appear"
    ],
    "a": 1,
    "w": "Parameters gather upward, so the indirection hides nothing from the contract - and adding a required one is a breaking change for every endpoint using that dependency."
   },
   {
    "t": "What is the problem with a five-level dependency chain?",
    "o": [
     "It is slow",
     "The endpoint's signature stops telling a reader what it needs",
     "It breaks caching",
     "It is not allowed"
    ],
    "a": 1,
    "w": "It works correctly. But one parameter standing for five functions, their parameters and their possible errors is no longer informative."
   }
  ]
 },
 {
  "path": "fastapi/what_is_fastapi.html",
  "title": "What FastAPI Is",
  "cat": "FastAPI",
  "q": [
   {
    "t": "Which library does FastAPI use for validation?",
    "o": [
     "Its own",
     "Pydantic",
     "Starlette",
     "marshmallow"
    ],
    "a": 1,
    "w": "FastAPI has no validation code of its own. It hands data to Pydantic and converts the resulting ValidationError into a 422, which is why everything you know about Pydantic applies directly."
   },
   {
    "t": "What is an ASGI application?",
    "o": [
     "A web server",
     "An async callable taking (scope, receive, send)",
     "A Pydantic model",
     "A router"
    ],
    "a": 1,
    "w": "That is the entire interface. uvicorn translates sockets into those three arguments, which is also why an app can be called directly, with no network, for tests."
   },
   {
    "t": "A request fails validation. Does your handler run?",
    "o": [
     "Yes, with None values",
     "No - validation happens before it",
     "Only for GET",
     "It depends on the model"
    ],
    "a": 1,
    "w": "The 422 is produced before the function is called. That is why handlers need no defensive type checking at the top."
   },
   {
    "t": "Where does the interactive documentation come from?",
    "o": [
     "A separate file you write",
     "The JSON Schema generated from your annotations",
     "uvicorn",
     "A decorator argument"
    ],
    "a": 1,
    "w": "Your models generate schemas, FastAPI assembles them into an OpenAPI document, and the docs page renders it. Writing a field description is writing documentation."
   }
  ]
 },
 {
  "path": "fastapi/your_first_endpoint.html",
  "title": "Your First Endpoint",
  "cat": "FastAPI",
  "q": [
   {
    "t": "What does `@app.get(\"/x\")` do to the function?",
    "o": [
     "Wraps it in a handler",
     "Registers it as a route and returns it unchanged",
     "Makes it async",
     "Adds validation code to it"
    ],
    "a": 1,
    "w": "The decorator records the path, method and signature in the routing table. The function itself is untouched and still callable directly."
   },
   {
    "t": "Why is `/modules/latest` unreachable when declared after `/modules/{module_id}`?",
    "o": [
     "A bug",
     "Routes match in registration order, first match wins",
     "Fixed paths are lower priority",
     "It needs a tag"
    ],
    "a": 1,
    "w": "The variable route matches first, with module_id=\"latest\". Declare fixed paths before variable ones - and annotating the parameter `int` makes the failure loud rather than silent."
   },
   {
    "t": "What must a 204 response contain?",
    "o": [
     "An empty dict",
     "Nothing - no body at all",
     "A message",
     "The created object"
    ],
    "a": 1,
    "w": "204 means success with nothing to say. Returning a value with status_code=204 produces a malformed response; return an explicit `Response(status_code=204)`."
   },
   {
    "t": "Where does an endpoint's description in the docs come from?",
    "o": [
     "A separate file",
     "The function's docstring, unless you pass `description`",
     "The route path",
     "The response model"
    ],
    "a": 1,
    "w": "The docstring becomes the description and Markdown is rendered - so documentation written where a Python developer naturally writes it also reaches the API docs."
   }
  ]
 },
 {
  "path": "gen_ai/ann_indexing_hnsw_and_ivf.html",
  "title": "ANN indexing: HNSW and IVF",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "HNSW stacks proximity graphs: sparse upper layers with long edges to cross the space, a dense bottom layer to refine. Search is greedy with a candidate list of width efSearch, which is the runtime recall/latency knob. M and efConstruction are fixed at build time. IVF is the simpler alternative — cluster then probe — cheaper to build and update, and it misses neighbours across cluster boundaries."
   },
   {
    "t": "What does this module say about “HNSW: skip lists, in vector space”?",
    "ans": "Take a proximity graph — each vector linked to its nearest neighbours — and stack several, each a random sample of the one below. Search enters at the sparse top layer and greedily moves to whichever neighbour is closer to the query, until no neighbour improves. Then it drops a layer and repeats."
   },
   {
    "t": "What does this module say about “The parameters worth naming”?",
    "ans": "M — edges per node, fixed at build time. Higher means a better-connected graph, better recall, more memory. The graph itself is a real memory cost on top of the vectors, which is HNSW's main drawback."
   }
  ]
 },
 {
  "path": "gen_ai/bm25_and_sparse_retrieval.html",
  "title": "BM25 and Sparse Lexical Retrieval",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "BM25 scores a document by summing, over each query term it contains, that term's rarity across the corpus times a saturating function of how often it appears, normalised by document length. b controls how much long documents are penalised for being long; k1 controls how much repeated terms are rewarded before diminishing returns kick in."
   },
   {
    "t": "What does this module say about “What this is”?",
    "ans": "Before dense vector search , and still running alongside it in most real systems, is sparse lexical search: score a document by which query terms it contains, weighted by how informative each term is. BM25 is the version of this idea that actually works well, and it needs no training, no GPU, and no embedding model."
   },
   {
    "t": "What does this module say about “Scoring by term overlap, carefully”?",
    "ans": "BM25 is the keyword retrieval function that most search engines are built on. It scores a document against a query by adding up a contribution per matching term:"
   }
  ]
 },
 {
  "path": "gen_ai/byte_pair_encoding_tokenizer.html",
  "title": "Byte Pair Encoding Tokenizer",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What does this module say about “The Two Failure Modes It Avoids”?",
    "ans": "BPE lands in between: frequent words become single tokens, rare words split into meaningful pieces, and nothing is ever out-of-vocabulary."
   },
   {
    "t": "What does this module say about “The Algorithm, in Four Lines”?",
    "ans": "That is the entire method. Vocabulary size is simply base characters plus the number of merges — which is why it is an exact dial rather than something you discover after the fact."
   },
   {
    "t": "What does this module say about “Merge Order Is the Model”?",
    "ans": "The merge list is ordered , and that order matters at encoding time: to tokenize a new word you replay the merges from rank 1 downward, applying each wherever it fits. The \"How it got there\" panel shows this replay step by step — the word starts as loose characters and progressively fuses."
   }
  ]
 },
 {
  "path": "gen_ai/casual_language_modeling.html",
  "title": "Causal Language Modeling",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What is meant by “Models are Statistical Parrots” here?",
    "ans": "They learn patterns, not meaning. Their output is based on the probability of what token should come next based on the data they were trained on."
   },
   {
    "t": "What is meant by “Generation is One Token at a Time” here?",
    "ans": "Text is generated sequentially. The model predicts the next token, adds it to the sequence, and then uses that new, longer sequence to predict the token after that."
   },
   {
    "t": "What is meant by “Temperature Controls Creativity” here?",
    "ans": "Temperature is a key parameter for controlling the randomness and \"creativity\" of the generated output."
   },
   {
    "t": "What is meant by “Context is King” here?",
    "ans": "The model's predictions are entirely dependent on the preceding tokens (the context). Changing even one word in the prompt can drastically alter the probability distribution for the next token."
   }
  ]
 },
 {
  "path": "gen_ai/chunking_strategies_for_rag.html",
  "title": "Chunking Strategies for RAG",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What does this module say about “Before the details”?",
    "ans": "Every piece of RAG downstream of chunking — embedding, indexing, retrieval, reranking — operates on whatever the chunk boundaries produced. Cut a sentence in half and both halves lose the context that made the original sentence meaningful; the embedding of a fragment is not a fragment of the embedding."
   },
   {
    "t": "What does this module say about “Fixed-size vs semantic”?",
    "ans": "Fixed-size chunking counts a fixed number of words or tokens and cuts there, with no regard for what is at that position — a heading, mid-word, mid-sentence, anywhere. It is simple, predictable, and blind. Semantic chunking respects natural boundaries — sentences, paragraphs, headings — and only splits at those boundaries, accepting some variation in chunk size in exchange for every chunk being a coherent unit."
   },
   {
    "t": "What does this module say about “Why overlap exists”?",
    "ans": "Even a well-placed boundary loses something: whatever came just before a chunk starts is not in it, even though it might be exactly the context needed to make the chunk's first sentence make sense. Overlap re-includes the last few words of the previous chunk at the start of the next one, at the direct cost of storing and embedding the same words twice."
   }
  ]
 },
 {
  "path": "gen_ai/completeness_in_llm_evaluation.html",
  "title": "Completeness in LLM evaluation",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Completeness is the proportion of required points an answer actually states, and it needs a key-points reference to be defined at all. It is the one dimension that penalises omission rather than error, which makes it the failure users notice last and act on first. Low completeness is usually a retrieval or chunking problem rather than a generation one."
   },
   {
    "t": "What does this module say about “Complete relative to what”?",
    "ans": "Completeness is undefined without a statement of what the answer needed to contain, so the reference is not optional. In practice that means a key-points list per evaluation query: the facts a good answer must include, written by whoever understands the domain."
   },
   {
    "t": "What does this module say about “Why the other dimensions cannot see it”?",
    "ans": "Consider an answer that states only \"Refunds are issued within 14 days.\" when the question was about the full refund policy. It is correct. It is grounded. It is entirely relevant. It scores 1.0 on three dimensions and leaves out the condition that makes it actionable."
   }
  ]
 },
 {
  "path": "gen_ai/context_window_and_kv_cache.html",
  "title": "Context Windows and the KV Cache",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The context window is the model's entire working memory, re-sent on every request, and it is shared between the system prompt, retrieved context, the conversation and the reply being written into it. The KV cache turns generation from quadratic work into linear by storing each token's key and value once, and it is paid for in memory that scales with layers, KV heads and sequence length — half a megabyte per token on..."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A language model holds no state between requests. Everything it appears to remember — your name, the file you pasted, what it said three turns ago — is re-sent on every call, inside the context window. The window is a hard limit on how much can be sent, and everything competes for it: the system prompt, retrieved documents, the conversation so far, and the space the reply needs to be written into."
   },
   {
    "t": "What does this module say about “What the KV cache is”?",
    "ans": "Generation is one token at a time, and each new token attends to every token before it. Attention needs a key and a value vector for each earlier position — and those never change once computed, because a token's key and value depend only on the tokens up to it."
   }
  ]
 },
 {
  "path": "gen_ai/context_aware_chunking.html",
  "title": "Context-aware chunking",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Context-aware chunking changes what is stored rather than where the cut falls. A chunk full of pronouns and back-references is unusable by the generator and invisible to retrieval, so title, heading path and resolved references are added back. Keep the enrichment short relative to the chunk, or shared context dominates the embedding and chunks stop being distinguishable."
   },
   {
    "t": "What does this module say about “The problem is coreference, not boundaries”?",
    "ans": "Prose is written to be read in order, so it leans on everything before it: \"it\", \"this policy\", \"as described above\", \"the latter\". Cut one paragraph out and those references dangle."
   },
   {
    "t": "What does this module say about “What gets added”?",
    "ans": "Cheap and free: document title and heading path, prepended. Deterministic, no model call, and usually the largest single improvement."
   }
  ]
 },
 {
  "path": "gen_ai/corrective_rag.html",
  "title": "Corrective RAG (CRAG)",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Corrective RAG grades retrieved documents before generating, and takes a different path when they are poor: rewrite the query, fall back to another source, or decline. Retrieval never fails loudly — it always returns its nearest k — so without a grader a query with no answer still produces a confident, sourced-looking one."
   },
   {
    "t": "What does this module say about “The failure it fixes”?",
    "ans": "A vector search returns the k nearest chunks whether or not any of them is relevant. There is no null result: ask about something absent from the corpus and you still get five chunks, at low similarity, and the generator dutifully writes an answer from them."
   },
   {
    "t": "What does this module say about “The three verdicts”?",
    "ans": "A grader — a small model, a cross-encoder, or a similarity threshold — labels the retrieved set:"
   }
  ]
 },
 {
  "path": "gen_ai/correctness_in_llm_evaluation.html",
  "title": "Correctness in LLM evaluation",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Correctness compares the answer against a reference or verifiable fact, which makes it the only one of the four dimensions that requires ground truth someone has to write. Exact match and n-gram overlap fail on paraphrase; claim-level judging against a key-facts reference is what works."
   },
   {
    "t": "What does this module say about “Correct against what, exactly”?",
    "ans": "Correctness is only defined relative to a reference, and choosing that reference is most of the work:"
   },
   {
    "t": "What does this module say about “Why exact match fails, and what replaces it”?",
    "ans": "The obvious automation — string comparison against the reference — fails immediately on natural language. \"14 days\", \"fourteen days\" and \"two weeks\" are the same answer and share no characters. Exact match systematically punishes fluent phrasing."
   }
  ]
 },
 {
  "path": "gen_ai/distributed_retrieval_and_sharding.html",
  "title": "Distributed retrieval and sharding",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Scatter-gather sends the query to every shard, takes a local top-k from each and merges. Shard randomly rather than by topic, or the relevant documents concentrate in one shard and its local k throws most of them away. Latency becomes the slowest shard's, not the average, so p99 gets worse with every shard added. Shards solve data that will not fit; replicas solve query volume."
   },
   {
    "t": "What does this module say about “Shards and replicas are different things”?",
    "ans": "A shard holds a slice of the corpus. Sharding handles data that will not fit — memory or index build time — and every query must visit every shard."
   },
   {
    "t": "What does this module say about “Shard randomly”?",
    "ans": "The instinct is to shard by topic or tenant so a query only touches one shard. For a multi-tenant system where every query is scoped to one tenant, that is right — it is really many small indexes."
   }
  ]
 },
 {
  "path": "gen_ai/dot_product_vs_cosine_similarity.html",
  "title": "Dot Product vs Cosine Similarity for Retrieval",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Cosine similarity divides out vector length and only ever measures direction; dot product does not, so it rewards longer vectors regardless of whether that length means anything. The two metrics agree only when every vector has the same length — true if you normalise your embeddings to unit length, false otherwise."
   },
   {
    "t": "What does this module say about “What this is”?",
    "ans": "Cosine similarity asks \"what angle apart are these two vectors\" and ignores length entirely. Dot product asks \"how much do these two vectors agree, weighted by how long they both are\" — length is part of the answer, not discarded."
   },
   {
    "t": "What does this module say about “Stretch Doc B”?",
    "ans": "same direction as before, just longer — like a verbose, repetitive document embedding"
   }
  ]
 },
 {
  "path": "gen_ai/embeddings_and_vector_search.html",
  "title": "Embeddings and Vector Search",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "An embedding model maps a piece of text to a point, arranged so that texts about the same thing land near each other. Nothing about the words themselves survives the trip — \"peel a mango\" and \"how to prepare tropical fruit\" share no vocabulary and end up as neighbours anyway."
   },
   {
    "t": "What does this module say about “Cosine, and why it is the default”?",
    "ans": "Retrieval almost always ranks by cosine similarity : the angle between the query vector and the document vector, ignoring how long either one is. Length in an embedding tends to carry things like document length or token count rather than meaning, so ignoring it is the point."
   },
   {
    "t": "What does this module say about “Exact search does not scale”?",
    "ans": "An exact search compares the query against every vector in the index. That is 18 comparisons here and 18 million in a real corpus, per query, and it is why nobody runs exact search at scale."
   }
  ]
 },
 {
  "path": "gen_ai/fine_tuning_vs_rlhf.html",
  "title": "Fine-Tuning vs RLHF and DPO",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Pretraining supplies knowledge and fluency, supervised fine-tuning supplies behaviour by imitation, and preference optimisation supplies judgement between answers that are all plausible. RLHF and DPO reach the same optimum — a policy proportional to the reference times the exponentiated reward — with DPO skipping the reward model that RLHF has to train and then defend."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A pretrained model is a text predictor. Ask it a question and it produces something a document containing that question might plausibly continue with — which is not the same as an answer, and certainly not a helpful one."
   },
   {
    "t": "What does this module say about “The maths both preference methods share”?",
    "ans": "Every preference method optimises the same objective: get more reward without drifting far from the model you started with. That constraint has a closed form,"
   }
  ]
 },
 {
  "path": "gen_ai/groundedness_in_llm_evaluation.html",
  "title": "Groundedness in LLM evaluation",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Groundedness is the proportion of an answer's claims that the retrieved context actually supports. It is the direct measure of hallucination, it needs no reference answer, and it is independent of truth — a claim can be grounded and wrong, or true and ungrounded. Measure it per claim rather than per answer so it tells you which span to look at."
   },
   {
    "t": "What does this module say about “What it measures, claim by claim”?",
    "ans": "The answer is decomposed into atomic claims — individual assertions that could each be checked independently — and each is tested against the retrieved context. Groundedness is the proportion that are supported."
   },
   {
    "t": "What does this module say about “Why it is independent of correctness”?",
    "ans": "This is the distinction people collapse, and the four combinations are all real:"
   }
  ]
 },
 {
  "path": "gen_ai/hallucination_and_grounding.html",
  "title": "Hallucination and Grounding",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A model hallucinates because it answers by sampling a distribution that has no state for \"I do not know\" — the mass has to go somewhere, and when the true fact is thinly represented it goes onto whatever is most plausible instead."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Ask a model something it has barely seen and it does not go quiet. Next-token prediction produces a distribution over the whole vocabulary, that distribution sums to one, and decoding picks from it. There is no branch in the architecture where \"insufficient evidence\" lives."
   },
   {
    "t": "What does this module say about “Where hallucinations come from”?",
    "ans": "A language model is trained to produce text that looks like its training data. It is not trained to be true, and it has no mechanism for checking."
   }
  ]
 },
 {
  "path": "gen_ai/how_llms_predict_next_word.html",
  "title": "How LLMs Predict the Next Word?",
  "cat": "Gen AI",
  "q": [
   {
    "t": "At each step, a language model produces:",
    "o": [
     "A single word",
     "A probability distribution over the whole vocabulary",
     "A sentence",
     "A yes/no decision"
    ],
    "a": 1,
    "w": "The model scores every token it knows. Which one actually gets emitted is a separate sampling decision made on top of that distribution."
   },
   {
    "t": "Raising the sampling temperature does what?",
    "o": [
     "Makes output more deterministic",
     "Flattens the distribution, so less likely tokens get picked more often",
     "Speeds up generation",
     "Increases the context length"
    ],
    "a": 1,
    "w": "Low temperature sharpens toward the top token and reads as safe and repetitive. High temperature flattens the odds and reads as creative, or as incoherent once pushed too far."
   },
   {
    "t": "Why does a model produce fluent text that is confidently wrong?",
    "o": [
     "It has a bug",
     "It is optimised for plausible continuations, not for truth",
     "Its training data was too small",
     "The temperature is always too high"
    ],
    "a": 1,
    "w": "Next-token prediction rewards text that looks like its training data. A fluent falsehood satisfies that objective just as well as a fluent fact - there is no separate check for truth."
   }
  ]
 },
 {
  "path": "gen_ai/how_llms_process_text.html",
  "title": "How LLMs Process Text?",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Text in, integers, vectors, mixed vectors, logits, text out. The embeddings and attention weights in this lab are deterministic stand-ins for learned parameters, but the operations — sinusoidal positions, scaled dot-product attention, softmax — are the real ones. Understanding this pipeline makes context windows, tokenizer quirks and attention costs stop feeling arbitrary."
   },
   {
    "t": "What does this module say about “Stages 1–3: Text Becomes Integers”?",
    "ans": "Tokenization splits the string into subword pieces, and each piece is looked up in the vocabulary to get an integer ID. That is the model's entire input: a list of integers. Nothing about the meaning of a word has entered yet — ID 4021 is no closer to ID 4022 than to ID 9. The IDs are arbitrary addresses, not measurements."
   },
   {
    "t": "What does this module say about “Stage 4: Embeddings Give IDs Meaning”?",
    "ans": "Each ID indexes into a giant lookup table, pulling out a learned vector of d numbers. These vectors are where meaning lives. Words used in similar contexts end up with similar vectors, and this table is trained along with everything else."
   }
  ]
 },
 {
  "path": "gen_ai/hybrid_search_reciprocal_rank_fusion.html",
  "title": "Hybrid Search: Dense + Sparse (Reciprocal Rank Fusion)",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What does this module say about “The idea in brief”?",
    "ans": "Dense retrieval and BM25 fail in different, mostly non-overlapping ways. A document phrased differently from the query but on the same topic can score well under a dense method and poorly under exact keyword match; a document with an unusual acronym or exact code can score well under BM25 and be embedded ambiguously."
   },
   {
    "t": "What does this module say about “Fusion”?",
    "ans": "small k lets rank-1 dominate; large k (60 is the common default) smooths everything out"
   },
   {
    "t": "What does this module say about “Why fuse ranks, not raw scores”?",
    "ans": "A cosine similarity lives between -1 and 1. A BM25 score is an unbounded sum that depends on corpus size and term rarity. Averaging the two numbers directly is meaningless — a BM25 score of 8 is not \"worth\" anything in particular next to a cosine of 0.6. Reciprocal Rank Fusion sidesteps this by throwing the scores away and using only each document's position in each list."
   }
  ]
 },
 {
  "path": "gen_ai/indexing_in_vector_databases.html",
  "title": "Indexing in vector databases",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Without an index, finding the nearest vector means comparing against every stored vector. An index prunes most of them and pays for it in recall, so the metric is recall@k measured against an exact search. Recall, latency and memory are the three knobs, and every index type exposes them under different names."
   },
   {
    "t": "What does this module say about “Why exact search stops working”?",
    "ans": "A flat index stores the vectors and compares the query with every one. It is exact, trivially correct, and the right answer for small collections — and the cost is O(n·d) per query, so a million 768-dimensional vectors is around 768 million multiply-adds for a single search."
   },
   {
    "t": "What does this module say about “What an index buys and what it costs”?",
    "ans": "Every approximate index prunes: it organises vectors so that most can be skipped without being compared. That turns a linear scan into something closer to logarithmic, and introduces the possibility of missing a genuine neighbour because the structure routed the search elsewhere."
   }
  ]
 },
 {
  "path": "gen_ai/knowledge_distillation_in_llms.html",
  "title": "Knowledge Distillation in LLMs",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A hard label answers one question. A teacher's full distribution answers every question at once — how likely each alternative is, and therefore how the classes relate. Temperature is the tool that makes that hidden structure large enough to learn from. The student in this lab performs real gradient descent on the combined loss, so the convergence you watch is genuine optimisation, just at a much smaller scale."
   },
   {
    "t": "What does this module say about “Dark Knowledge: The Central Idea”?",
    "ans": "A training label says \"this is a dog\" and nothing else. But a trained teacher, shown that same photo, might output dog 0.90, wolf 0.07, cat 0.02, car 0.001 ."
   },
   {
    "t": "What does this module say about “Why Temperature Is Essential”?",
    "ans": "There is a catch: a confident teacher's non-target probabilities are so tiny that they contribute almost nothing to the gradient. At T = 1 the distribution is nearly one-hot, so the student learns roughly what the plain label already told it."
   }
  ]
 },
 {
  "path": "gen_ai/lora_in_llms.html",
  "title": "LoRA in LLMs",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "LoRA does not make the model smaller — it makes the update smaller. By constraining the change to a low-rank subspace, it converts fine-tuning from an infrastructure project into something that runs on one GPU and ships as a few-megabyte file, with no inference penalty once merged."
   },
   {
    "t": "What does this module say about “The Insight: Updates Are Low-Rank”?",
    "ans": "Fine-tuning changes a weight matrix from W to W + ΔW . The observation behind LoRA is that although W is enormously expressive, the change needed to specialise a model for one task has very low intrinsic rank — it does not need the full space."
   },
   {
    "t": "What does this module say about “Why the Savings Are So Extreme”?",
    "ans": "A full update on a 4096×4096 layer is 16.7 million parameters. The LoRA version at rank 8 is 8 × (4096 + 4096) = 65,536 — about 0.4% . The saving comes from replacing a product of dimensions with a sum of them."
   }
  ]
 },
 {
  "path": "gen_ai/maximal_marginal_relevance.html",
  "title": "Maximal Marginal Relevance (MMR)",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "MMR selects documents one at a time, and after the first pick, every subsequent choice is weighed against how similar it is to what has already been selected — trading some relevance for coverage. λ controls the trade directly: 1.0 is ordinary top-k relevance ranking, 0.0 ignores relevance and maximises spread, and everything between balances the two."
   },
   {
    "t": "What does this module say about “Context first”?",
    "ans": "Plain top-k retrieval picks the k highest-scoring documents independently. If a document collection has several near-identical passages about the same popular sub-topic, all of them can legitimately score near the top — and a naive top-k fills the context with repetition instead of coverage, wasting the retrieval budget on saying the same thing three times."
   },
   {
    "t": "What does this module say about “Selection”?",
    "ans": "1.0 = pure relevance (same as MMR off). 0.0 = pure diversity, ignores relevance entirely."
   }
  ]
 },
 {
  "path": "gen_ai/multi_query_retriever.html",
  "title": "Multi-Query Retriever",
  "cat": "Gen AI",
  "q": [
   {
    "t": "How are the results of the separate queries combined?",
    "o": [
     "Union, deduplicated",
     "Intersection",
     "Only the best query's results are kept",
     "Averaged scores"
    ],
    "a": 0,
    "w": "Every document any phrasing found is kept. A document is missed only if EVERY phrasing misses it, which is the whole point."
   },
   {
    "t": "Multi-query retrieval mainly improves:",
    "o": [
     "Precision",
     "Recall",
     "Latency",
     "Index size"
    ],
    "a": 1,
    "w": "It trades a longer and noisier candidate list for a much lower chance of missing the right document - recall up, precision down, deliberately."
   },
   {
    "t": "Why is multi-query usually followed by reranking or MMR?",
    "o": [
     "To translate the query",
     "To clean up the larger, noisier list",
     "To compress the documents",
     "To generate more queries"
    ],
    "a": 1,
    "w": "Raising recall pulls in irrelevant documents too. Something downstream has to reorder or diversify before the list reaches the model."
   }
  ]
 },
 {
  "path": "gen_ai/parent_document_retriever.html",
  "title": "Parent Document Retriever",
  "cat": "Gen AI",
  "q": [
   {
    "t": "In a parent document retriever, what is actually indexed and scored?",
    "o": [
     "The whole parent documents",
     "The small child chunks",
     "Both, separately",
     "Only the document titles"
    ],
    "a": 1,
    "w": "Children are indexed so the match is precise. The parent is what gets returned - the score decides WHICH document, the parent decides how much text the model sees."
   },
   {
    "t": "Two retrieved child chunks belong to the same parent. How many passages go to the model?",
    "o": [
     "One",
     "Two",
     "Three",
     "It depends on the scores"
    ],
    "a": 0,
    "w": "Parents are deduplicated. Without that, a document with three good chunks would be sent three times and burn the context window."
   },
   {
    "t": "Why not simply index large chunks instead?",
    "o": [
     "They are slower to embed",
     "The query terms get diluted",
     "They cannot be embedded",
     "They break the tokenizer"
    ],
    "a": 1,
    "w": "A large chunk spreads the query's terms among hundreds of unrelated words, so its similarity score drops and it may not be retrieved at all - even though it holds the answer."
   }
  ]
 },
 {
  "path": "gen_ai/permission_filtering_in_rag.html",
  "title": "Permission filtering in RAG retrieval",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What is meant by “A user with no groups” here?",
    "ans": "should retrieve nothing, not everything. A missing or empty filter that matches all documents is the classic catastrophic bug."
   },
   {
    "t": "What is meant by “A filter on a field that does not exist” here?",
    "ans": "should fail closed, not open. Some stores silently ignore unknown fields."
   },
   {
    "t": "What is meant by “Documents with no ACL recorded” here?",
    "ans": "— decide whether the default is deny (correct) or allow (dangerous), and make it explicit."
   },
   {
    "t": "What is meant by “Cached results” here?",
    "ans": "A cache keyed only on the query text will serve one user's authorised results to another. Cache keys must include the permission context."
   }
  ]
 },
 {
  "path": "gen_ai/quantization_in_llms.html",
  "title": "Quantization in LLMs",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What does this module say about “The Core Idea: A Coarser Ruler”?",
    "ans": "A 32-bit float can express billions of distinct values. An 8-bit integer can express 256, and a 4-bit integer just 16. Quantization finds the range your weights actually occupy and divides it into that many evenly spaced levels:"
   },
   {
    "t": "What does this module say about “Symmetric vs Asymmetric”?",
    "ans": "Toggle between them with the outlier enabled and watch the step size and RMS error change."
   },
   {
    "t": "What does this module say about “Outliers Are the Real Enemy”?",
    "ans": "Quantization error does not grow smoothly with bit-width — it is dominated by range . A single weight far from the others stretches the min-max span, and since the step size is that span divided by a fixed number of levels, every other weight gets a coarser grid."
   }
  ]
 },
 {
  "path": "gen_ai/query_rewriting_and_hyde.html",
  "title": "Query Rewriting and HyDE",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What does this module say about “Before the details”?",
    "ans": "A user's question and the passage that answers it are usually written in different registers: short and colloquial versus long-form and technical. Every similarity metric in this batch — cosine , BM25 — depends on shared vocabulary between what is embedded and what is stored."
   },
   {
    "t": "What does this module say about “What Gets Embedded”?",
    "ans": "the HyDE passage below is written by hand as a labelled example of what an LLM would draft — no model runs in this page"
   },
   {
    "t": "What does this module say about “Two ways to close the gap”?",
    "ans": "Query expansion adds related terms to the original query — synonyms, likely technical vocabulary — widening what it can match against. HyDE (Hypothetical Document Embeddings) goes further: ask a language model to draft a plausible answer to the question, without ever checking whether that answer is true, and embed that hypothetical answer instead of the question."
   }
  ]
 },
 {
  "path": "gen_ai/caching_in_rag_pipelines.html",
  "title": "Query, embedding and prompt caching",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Three different caches share the name. The query cache stores a finished answer keyed on the question and saves the most per hit, at the risk of serving a stale one. The embedding cache stores a vector keyed on the text and is permanently valid until the model changes. Prompt caching lives in the provider and only helps when the shared text comes first in the prompt."
   },
   {
    "t": "What does this module say about “Embedding cache: the easy one”?",
    "ans": "Keyed on a hash of the text and the model name. Embedding is deterministic, so the same text always gives the same vector — which makes this cache both trivially correct and permanently valid, until you change models."
   },
   {
    "t": "What does this module say about “Query cache: the highest saving, and the highest risk”?",
    "ans": "Keyed on the question, storing the final answer. A hit skips retrieval, reranking and generation — often seconds and most of the cost. Real traffic is heavily repetitive, so hit rates can be high."
   }
  ]
 },
 {
  "path": "gen_ai/reranking_bi_encoders_vs_cross_encoders.html",
  "title": "Re-ranking: Bi-Encoders vs Cross-Encoders",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A bi-encoder scores query and document independently, which is what makes it fast enough to search a whole corpus but blind to interactions between them — a lexical coincidence can outrank a genuine match. A cross-encoder reads both together and catches that, at a cost that only scales with the shortlist, not the corpus."
   },
   {
    "t": "What does this module say about “The idea in brief”?",
    "ans": "A bi-encoder embeds the query and every document separately , ahead of time — that is what makes the embeddings precomputable and search fast, but it also means the model never looks at a query and a document together. A cross-encoder takes both as one input and lets the model attend across them jointly, at the cost of running a full forward pass per query-document pair, at query time, with nothing precomputable."
   },
   {
    "t": "What does this module say about “The two-stage pattern”?",
    "ans": "Cross-encoders are far more accurate but cost too much to run over an entire corpus — a million documents means a million forward passes per query. The standard fix is two stages: a cheap bi-encoder (or BM25, or both) retrieves a shortlist of maybe 20-100 candidates, and only that shortlist is re-scored by the expensive cross-encoder, which then decides the final order."
   }
  ]
 },
 {
  "path": "gen_ai/recursive_chunking.html",
  "title": "Recursive chunking",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What is meant by “Confusing characters with tokens,” here?",
    "ans": "so chunks are four times smaller than intended."
   },
   {
    "t": "What is meant by “No overlap,” here?",
    "ans": "so a sentence spanning a boundary is lost from both chunks."
   },
   {
    "t": "What is meant by “Too much overlap” here?",
    "ans": "(50%+), which duplicates storage and fills results with near-identical chunks."
   },
   {
    "t": "What is meant by “Splitting tables,” here?",
    "ans": "which destroys them. Extract tables separately and keep each whole."
   }
  ]
 },
 {
  "path": "gen_ai/relevance_in_llm_evaluation.html",
  "title": "Relevance in LLM evaluation",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Answer relevance measures how much of the answer addresses the question asked. Distinguish it from context relevance, which scores retrieved chunks and is a retrieval metric. It is the only dimension that penalises padding, hedging and confidently answering a nearby question — all of which score perfectly on correctness and groundedness."
   },
   {
    "t": "What does this module say about “Two different things are called relevance”?",
    "ans": "The word is used for two distinct measurements and conflating them makes evaluation results incomparable."
   },
   {
    "t": "What does this module say about “The failures it exists to catch”?",
    "ans": "Padding. The answer contains the requested information plus three paragraphs of adjacent context nobody asked for. Every claim is true and grounded, and the user has to hunt for the answer. Models trained to be helpful pad heavily, and no other dimension penalises it."
   }
  ]
 },
 {
  "path": "gen_ai/retrieval_evaluation_metrics.html",
  "title": "Retrieval Evaluation Metrics",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Retrieval returns a ranking, so metrics are computed at a cutoff k and differ mainly in whether they care about position. Precision@k and recall@k ignore order within the cutoff; MRR looks only at the first relevant result; NDCG discounts by position and handles graded relevance. For RAG, recall@k at your actual context size is the number to optimise, because the model can survive a bad chunk but not a missing one."
   },
   {
    "t": "What does this module say about “Why classification metrics are not enough”?",
    "ans": "A retriever does not return a yes or no; it returns an ordered list of candidates. Two systems can retrieve exactly the same documents and be very different in quality if one puts the relevant ones first and the other buries them at position 10."
   },
   {
    "t": "What does this module say about “Ranking”?",
    "ans": "all three rankings retrieve exactly the same 5 relevant / 5 irrelevant documents"
   }
  ]
 },
 {
  "path": "gen_ai/rag.html",
  "title": "Retrieval-Augmented Generation (RAG)",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "RAG answers questions a model was never trained on by finding relevant passages and putting them in the prompt, so generation becomes reading rather than recall. The retrieval step is ordinary similarity search and it always returns something, which makes the quality of your chunking, your ranking and your \"I could not find it\" path the whole ballgame."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A language model knows what was in its training data, frozen at some cutoff date. It does not know your company's handbook, last week's incident report, or a product invented for a teaching page. Asked anyway, it will answer — fluently, and wrongly."
   },
   {
    "t": "What does this module say about “The pipeline”?",
    "ans": "Only steps 3 to 5 happen per question. Steps 1 and 2 happen once, when the documents change — which is why RAG updates in the time it takes to re-index rather than the time it takes to retrain."
   }
  ]
 },
 {
  "path": "gen_ai/self_query_retriever.html",
  "title": "Self-Query Retriever",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Why can plain similarity search not honour \"published after 2020\"?",
    "o": [
     "Dates are not embeddable",
     "A cosine score has no notion of a constraint",
     "The index is too small",
     "Years are stopwords"
    ],
    "a": 1,
    "w": "Embeddings compare meaning. The phrase is treated as more subject matter to match, not as a rule, so a 2017 paper about attention can still win."
   },
   {
    "t": "A self-query retriever splits the question into:",
    "o": [
     "Two semantic queries",
     "A semantic query and a metadata filter",
     "Keywords and embeddings",
     "A question and an answer"
    ],
    "a": 1,
    "w": "One half is embedded and compared; the other becomes a structured predicate like year > 2020 that is executed against the metadata."
   },
   {
    "t": "In what order do the two halves run?",
    "o": [
     "Filter first, then rank the survivors",
     "Rank first, then filter the top results",
     "Both at once, scores averaged",
     "Whichever is faster"
    ],
    "a": 0,
    "w": "The filter removes documents that break the constraint, and similarity only ranks what survived. Filtering after ranking would let a top-k full of excluded documents leave nothing behind."
   }
  ]
 },
 {
  "path": "gen_ai/semantic_chunking.html",
  "title": "Semantic chunking",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Semantic chunking embeds each sentence and cuts where the similarity between neighbours drops, so boundaries land at topic changes rather than at character counts. It costs one embedding per sentence at index time, and it is usually not worth it on documents that already carry headings."
   },
   {
    "t": "What does this module say about “How the boundary is chosen”?",
    "ans": "Split into sentences, embed each one, and compute the similarity between each consecutive pair. Where the text stays on topic the similarity is high; where the subject changes it dips. Cut at the dips."
   },
   {
    "t": "What does this module say about “What it costs”?",
    "ans": "The cost is real and worth stating plainly: one embedding call per sentence at indexing time ."
   }
  ]
 },
 {
  "path": "gen_ai/structure_aware_chunking.html",
  "title": "Structure-aware chunking",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Structure-aware chunking splits along the document's own markup — headings, list items, table rows — because those boundaries were placed by the author and cost nothing to find. Carrying the heading path into each chunk is the half people miss: it makes a fragment self-describing and puts the section's vocabulary into the embedded text."
   },
   {
    "t": "What does this module say about “Boundaries you do not have to guess”?",
    "ans": "A Markdown heading, an HTML <section> , a PDF outline entry, a slide break: each is a statement by the author that the subject changes here. Semantic chunking spends an embedding per sentence to infer what the markup already says."
   },
   {
    "t": "What does this module say about “What it needs from you”?",
    "ans": "A parser per format. Markdown is easy, HTML is manageable, PDF is genuinely hard — a PDF has no structure, only positioned glyphs, so headings must be inferred from font size and spacing. Most RAG quality problems on PDFs are really extraction problems."
   }
  ]
 },
 {
  "path": "gen_ai/tf_idf.html",
  "title": "TF-IDF",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "TF-IDF weights a term by how often it appears here times how rare it is everywhere. A term in every document has an idf of zero and drops out by arithmetic rather than by a list. It knows nothing about meaning, which is why a synonym scores zero and why dense retrieval runs alongside it."
   },
   {
    "t": "What does this module say about “The two halves”?",
    "ans": "Term frequency is how often a term occurs in a document, usually damped — a word appearing twenty times is not twenty times as relevant, so implementations take a logarithm or normalise by document length."
   },
   {
    "t": "What does this module say about “Where it falls short”?",
    "ans": "No length normalisation by default. A long document contains more of everything, so raw TF favours it. Dividing by length overcorrects and favours very short ones. BM25's b parameter exists to tune between the two."
   }
  ]
 },
 {
  "path": "gen_ai/queries_keys_and_values.html",
  "title": "What are Queries, Keys and Values in an LLM?",
  "cat": "Gen AI",
  "q": [
   {
    "t": "What is meant by “Value” here?",
    "ans": "— what each position contributes when selected."
   },
   {
    "t": "What does this module say about “Why three and not one”?",
    "ans": "If a token used the same vector to search with and to be found by, attention would collapse into plain similarity: tokens would attend to tokens like themselves. Separating query from key lets a token look for something different from itself — a verb seeking its subject, a pronoun seeking its referent."
   },
   {
    "t": "What does this module say about “The mechanism in one line”?",
    "ans": "softmax(QK T / √d) V . The dot products score every query against every key; the division keeps the softmax out of its saturated region, where gradients vanish; softmax turns scores into weights summing to one; and those weights are applied to the values."
   }
  ]
 },
 {
  "path": "gen_ai/hit_rate_at_k.html",
  "title": "What is Hit Rate@k?",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Hit Rate@k is the proportion of queries with at least one relevant result in the top k. It is binary per query, ignores position and quantity, and measures the ceiling on your pipeline — if the evidence never reaches the model, nothing downstream can fix it."
   },
   {
    "t": "What does this module say about “The definition, and the averaging that hides in it”?",
    "ans": "For a single query, Hit Rate@k is binary: 1 if any of the top k results is relevant, 0 if none is. There is no partial credit. A query whose top 3 contains five relevant documents and a query whose top 3 contains exactly one both score 1."
   },
   {
    "t": "What does this module say about “Why it is the right first metric for RAG”?",
    "ans": "A RAG generator does not need every relevant document. It needs enough grounding to answer, and for most factual questions one good chunk is enough. If the answer is in the context, the model can use it; if it is not, no amount of prompt engineering will recover it."
   }
  ]
 },
 {
  "path": "gen_ai/mean_reciprocal_rank.html",
  "title": "What is MRR (Mean Reciprocal Rank)?",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "MRR averages 1/rank of the first relevant result. It is the metric for systems where the consumer stops at the first good answer, and it is far more sensitive to the top of the ranking than recall or precision. It ignores every relevant result after the first, so it is the wrong choice for questions needing several sources."
   },
   {
    "t": "What does this module say about “The definition, and the shape of the curve”?",
    "ans": "Reciprocal rank for a query is 1/(rank of the first relevant result). MRR is the mean of that over an evaluation set. The name is worth reading literally: it is a mean of reciprocal ranks , and each word matters."
   },
   {
    "t": "What does this module say about “When position is the whole question”?",
    "ans": "MRR is the right metric when the consumer stops at the first good result. Question answering with a single correct answer, \"I'm feeling lucky\" search, entity lookup, a code assistant jumping to a definition — in all of these the second correct result is worth nothing."
   }
  ]
 },
 {
  "path": "gen_ai/masked_language_modeling.html",
  "title": "What is Masked Language Modeling?",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "MLM turns any raw text into supervised training data by deleting parts of it. Because the blank is surrounded rather than trailing, the model learns deep bidirectional understanding — ideal for classification, retrieval and question answering, and unsuitable for generation. That generative job belongs to causal models, which predict strictly forward."
   },
   {
    "t": "What does this module say about “Why It Must Be Bidirectional”?",
    "ans": "A causal model reads left to right and predicts what comes next, so it can never look ahead. MLM has no such restriction: the blank sits in the middle , and the model is free to use every token on both sides at once."
   },
   {
    "t": "What does this module say about “The Curious 80 / 10 / 10 Split”?",
    "ans": "BERT masks about 15% of tokens, but does not always insert a literal [MASK] . Of the chosen positions:"
   }
  ]
 },
 {
  "path": "gen_ai/precision_at_k.html",
  "title": "What is Precision@k?",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Precision@k is the fraction of the returned k that was relevant, with k always as the denominator. It is the cheap metric to label, because it needs judgements only for what you returned. In a RAG pipeline it is not just about efficiency: irrelevant context costs tokens, pushes good evidence into the least-attended part of the prompt, and gives the model plausible material to be wrong with."
   },
   {
    "t": "What does this module say about “The definition, and the denominator that never moves”?",
    "ans": "Precision@k is the number of relevant documents in the top k divided by k. Not by the number of relevant documents in the corpus, and not by the number retrieved — by k, always."
   },
   {
    "t": "What does this module say about “Why noise is not free in a RAG pipeline”?",
    "ans": "The old intuition — \"the model can just ignore irrelevant chunks\" — is not quite true, and the ways it fails are worth naming."
   }
  ]
 },
 {
  "path": "gen_ai/recall_at_k.html",
  "title": "What is Recall@k?",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Recall@k is the fraction of all relevant documents that reached the top k. It is the metric that bounds a RAG pipeline, because a document that was never retrieved cannot be used, while an irrelevant one can be ignored. It rises monotonically with k, so it is meaningless without its k and must be read against a cost — usually your context budget."
   },
   {
    "t": "What does this module say about “The definition, and the denominator people forget”?",
    "ans": "Recall@k is the number of relevant documents in the top k divided by the total number of relevant documents that exist . The numerator is easy; the denominator is where the difficulty lives."
   },
   {
    "t": "What does this module say about “Why it is the retrieval metric for RAG”?",
    "ans": "The generator can ignore an irrelevant chunk. It cannot invent a relevant one that was never retrieved. That asymmetry is the whole argument: recall failures are unrecoverable, precision failures are merely expensive ."
   }
  ]
 },
 {
  "path": "interview/three-sum.html",
  "title": "3Sum",
  "cat": "Interview",
  "q": [
   {
    "t": "Fixing one element reduces 3Sum from O(n³) to O(n²) because the inner search becomes:",
    "o": [
     "A binary search",
     "Two Sum, which is O(n) on sorted input",
     "A hash lookup",
     "A sort"
    ],
    "a": 1,
    "w": "n iterations of a linear inner scan is O(n²). The sort is O(n log n) and disappears into that."
   },
   {
    "t": "Why sort rather than use a hash map for the inner search?",
    "o": [
     "It is faster",
     "Sorting makes duplicates adjacent, so deduplication is a skip rather than a set of tuples",
     "Hash maps do not work here",
     "It uses less memory"
    ],
    "a": 1,
    "w": "Both are O(n²). Deduplication is the real difficulty of this problem, and adjacency is what makes it cheap."
   },
   {
    "t": "How many places need a duplicate skip?",
    "o": [
     "One - the fixed element",
     "Two - the fixed element and both pointers after a hit",
     "Three",
     "None, if you use a set"
    ],
    "a": 1,
    "w": "Skipping only the fixed value still finds the same triple twice within one inner scan."
   }
  ]
 },
 {
  "path": "interview/valid-anagram.html",
  "title": "Are two strings anagrams?",
  "cat": "Interview",
  "q": [
   {
    "t": "Counting beats sorting for anagram checks because it is:",
    "o": [
     "O(1) instead of O(n)",
     "O(n) instead of O(n log n)",
     "More readable",
     "Stable"
    ],
    "a": 1,
    "w": "One pass over each string versus a comparison sort of both. Space goes from O(1) to O(k) in the alphabet size."
   },
   {
    "t": "Why delete a key when its count reaches zero?",
    "o": [
     "To save memory",
     "So the final check is simply 'is the dictionary empty?'",
     "To avoid negatives",
     "Counter requires it"
    ],
    "a": 1,
    "w": "Leaving zeros in means comparing against a dict of zeros. Deleting makes the terminal condition trivial."
   },
   {
    "t": "A fixed 26-element array version breaks on:",
    "o": [
     "Long strings",
     "Any character outside a-z, such as an accented letter",
     "Empty strings",
     "Repeated letters"
    ],
    "a": 1,
    "w": "ord(ch) - ord('a') indexes out of range. Say the alphabet assumption out loud when you offer that optimisation."
   }
  ]
 },
 {
  "path": "interview/valid-palindrome.html",
  "title": "Check whether a string is a palindrome",
  "cat": "Interview",
  "q": [
   {
    "t": "The main advantage of the two-pointer palindrome check over s == s[::-1] is:",
    "o": [
     "It is shorter",
     "O(1) extra space, and it stops at the first mismatch",
     "It handles Unicode",
     "It is the only correct one"
    ],
    "a": 1,
    "w": "The slice builds a full reversed copy and always compares everything. Both are O(n) time in the worst case."
   },
   {
    "t": "Why do the inner skip loops need `lo < hi` in their condition?",
    "o": [
     "To count comparisons",
     "Otherwise a string of pure punctuation runs a pointer off the end",
     "To handle uppercase",
     "To make it stable"
    ],
    "a": 1,
    "w": "Nothing else stops the skip. It is the bug the question is really probing."
   },
   {
    "t": "In the 'allow one deletion' variant, why is it still O(n)?",
    "o": [
     "The string is short",
     "The branch happens at most once, so the two sub-checks never nest",
     "It uses a set",
     "It is O(n²)"
    ],
    "a": 1,
    "w": "You get exactly one chance to delete, so it is one linear scan plus at most two more - not a recursive explosion."
   }
  ]
 },
 {
  "path": "interview/counting-with-dictionaries.html",
  "title": "Count things with a dictionary",
  "cat": "Interview",
  "q": [
   {
    "t": "Reading a missing key from a defaultdict:",
    "o": [
     "Returns None",
     "Creates it with the default value",
     "Raises KeyError",
     "Returns 0 without inserting"
    ],
    "a": 1,
    "w": "A read can grow the dictionary. Counter returns 0 without inserting, which is why it is safer for inspection."
   },
   {
    "t": "Finding the k most common items is best done with:",
    "o": [
     "Sorting all counts, O(m log m)",
     "A heap of size k, O(m log k)",
     "A linear scan, O(m²)",
     "Binary search"
    ],
    "a": 1,
    "w": "heapq.nlargest and Counter.most_common(k) both do this. For 'top 10 of a billion' it is the whole question."
   },
   {
    "t": "Counting n items with a dictionary costs:",
    "o": [
     "O(n log n)",
     "O(n)",
     "O(n²)",
     "O(k) in the distinct count"
    ],
    "a": 1,
    "w": "One lookup and one write per item, each O(1) on average. Space is O(k) in the number of distinct items."
   }
  ]
 },
 {
  "path": "interview/design-an-lru-cache.html",
  "title": "Design an LRU cache",
  "cat": "Interview",
  "q": [
   {
    "t": "Why does an LRU cache need a doubly linked list rather than a singly linked one?",
    "o": [
     "To iterate backwards",
     "Removing an arbitrary node in O(1) requires knowing its predecessor",
     "To store more data",
     "It does not"
    ],
    "a": 1,
    "w": "With only forward pointers you would have to scan to find the node before, which is O(n) and defeats the requirement."
   },
   {
    "t": "What does the hash map store as its value?",
    "o": [
     "The cached value",
     "The list node holding that value",
     "The insertion time",
     "The key again"
    ],
    "a": 1,
    "w": "Storing the node is what lets you go from a key straight to its position in the order and unlink it without walking."
   },
   {
    "t": "Does a successful get change the cache?",
    "o": [
     "No, reads are free",
     "Yes - it makes that entry the most recently used",
     "Only if the cache is full",
     "Only for the first read"
    ],
    "a": 1,
    "w": "That is what distinguishes LRU from FIFO. A cache where reads did not count would evict on insertion order instead."
   }
  ]
 },
 {
  "path": "interview/does-len-count-characters-or-bytes.html",
  "title": "Does len() count characters or bytes?",
  "cat": "Interview",
  "q": [
   {
    "t": "len(s) on a Python 3 string counts:",
    "o": [
     "Bytes",
     "Code points",
     "Grapheme clusters",
     "UTF-16 units"
    ],
    "a": 1,
    "w": "A str is a sequence of code points. Bytes depend on an encoding, and graphemes need a library the standard library does not ship."
   },
   {
    "t": "Two strings render identically but compare unequal. The most likely cause is:",
    "o": [
     "A trailing space",
     "One uses a combining accent and the other a precomposed character",
     "Different encodings",
     "One is bytes"
    ],
    "a": 1,
    "w": "é can be one code point or 'e' plus a combining mark. unicodedata.normalize('NFC', s) collapses them before comparison."
   },
   {
    "t": "You need to enforce a 100-character database limit. You should measure:",
    "o": [
     "len(s)",
     "len(s.encode('utf-8')) if the column is measured in bytes",
     "The number of words",
     "sys.getsizeof(s)"
    ],
    "a": 1,
    "w": "Storage and transport limits are byte limits. A 100-code-point string can be 400 bytes in UTF-8."
   }
  ]
 },
 {
  "path": "interview/edit-distance.html",
  "title": "Edit distance (Levenshtein)",
  "cat": "Interview",
  "q": [
   {
    "t": "In the DP table, the cell above dp[i][j] corresponds to which edit?",
    "o": [
     "Insert",
     "Delete a character from the first string",
     "Substitute",
     "No edit"
    ],
    "a": 1,
    "w": "Up is delete, left is insert, diagonal is substitute. Naming them is what shows the recurrence is understood rather than memorised."
   },
   {
    "t": "Filling row 0 and column 0 with zeros instead of 0..n gives:",
    "o": [
     "The same answer",
     "Answers that are too small",
     "An IndexError",
     "Answers that are too large"
    ],
    "a": 1,
    "w": "The edges encode the cost of reaching the empty string. Zeroing them makes those conversions free."
   },
   {
    "t": "The space can be reduced to O(min(m, n)) because:",
    "o": [
     "The strings are short",
     "Each cell depends only on the previous row and the cell to its left",
     "The table is symmetric",
     "Most cells are zero"
    ],
    "a": 1,
    "w": "Two rows suffice. The cost is that you can no longer walk the table back to recover which edits were made."
   }
  ]
 },
 {
  "path": "interview/find-the-duplicate-number.html",
  "title": "Find the duplicate number",
  "cat": "Interview",
  "q": [
   {
    "t": "Why can the array be treated as a linked list?",
    "o": [
     "It is sorted",
     "Every value is a valid index, so each slot points to another slot",
     "It contains no zeros",
     "It is the same length as its values"
    ],
    "a": 1,
    "w": "Values are in 1..n, so no jump leaves the array and index 0 is never re-entered - making it a chain with a guaranteed cycle."
   },
   {
    "t": "The meeting point of the two pointers is:",
    "o": [
     "The duplicate",
     "Somewhere inside the cycle, not necessarily its entrance",
     "Always index 0",
     "The array length"
    ],
    "a": 1,
    "w": "Phase one only proves a cycle exists. Phase two walks from the head to find the entrance, which is the duplicate."
   },
   {
    "t": "Which constraint rules out using a set?",
    "o": [
     "Do not modify the array",
     "O(1) space",
     "O(n) time",
     "Values are 1..n"
    ],
    "a": 1,
    "w": "A set is O(n) memory. 'Do not modify' is what rules out sorting and index-negation instead."
   }
  ]
 },
 {
  "path": "interview/first-non-repeating-character.html",
  "title": "First non-repeating character",
  "cat": "Interview",
  "q": [
   {
    "t": "Why can this not be solved in a single pass?",
    "o": [
     "Strings are immutable",
     "A character's uniqueness is not decidable until the whole string has been read",
     "Counters are slow",
     "It can be"
    ],
    "a": 1,
    "w": "The first character might repeat at the very end. A pass can record enough to answer afterwards, which is what the counter is."
   },
   {
    "t": "The second pass walks the string rather than the counter because:",
    "o": [
     "It is faster",
     "'First' is a property of the string's order",
     "Counters are unordered",
     "It uses less memory"
    ],
    "a": 1,
    "w": "Walking the dict also works since 3.7, when insertion order became a guarantee - but you should say which you are relying on."
   },
   {
    "t": "In the streaming version, what makes each add O(1) amortised?",
    "o": [
     "The counter is O(1)",
     "Every character is pushed once and popped at most once",
     "The queue is sorted",
     "It only stores unique characters"
    ],
    "a": 1,
    "w": "The while loop can run several times on one call, but across the whole stream it does at most n pops in total."
   }
  ]
 },
 {
  "path": "interview/group-anagrams.html",
  "title": "Group anagrams together",
  "cat": "Interview",
  "q": [
   {
    "t": "The key idea in grouping anagrams efficiently is:",
    "o": [
     "Sorting the whole list first",
     "Giving each word a canonical key that all its anagrams share",
     "Comparing each word to the first",
     "Using a set"
    ],
    "a": 1,
    "w": "Being anagrams is an equivalence relation, so you group by label rather than testing pairs. That removes the n² entirely."
   },
   {
    "t": "Why must the count key be a tuple rather than a list?",
    "o": [
     "Tuples are faster",
     "Lists are unhashable, so they cannot be dictionary keys",
     "Tuples are shorter",
     "It does not matter"
    ],
    "a": 1,
    "w": "A key's hash must stay valid for the life of the entry, so only immutable types are allowed."
   },
   {
    "t": "For n words of length m, grouping by sorted key costs:",
    "o": [
     "O(n²·m)",
     "O(n·m log m)",
     "O(n log n)",
     "O(m²)"
    ],
    "a": 1,
    "w": "One sort per word, then O(1) to place it. The count-tuple key drops it to O(n·m)."
   }
  ]
 },
 {
  "path": "interview/grouping-and-inverting-dictionaries.html",
  "title": "Group records and invert a dictionary",
  "cat": "Interview",
  "q": [
   {
    "t": "itertools.groupby differs from SQL's GROUP BY in that it:",
    "o": [
     "Is faster",
     "Only groups consecutive equal keys, so the input must be sorted first",
     "Returns a dict",
     "Cannot take a key function"
    ],
    "a": 1,
    "w": "On unsorted input you get one group per run, and later runs overwrite earlier ones when collected into a dict."
   },
   {
    "t": "Inverting a dict with a comprehension when two keys share a value:",
    "o": [
     "Raises ValueError",
     "Silently keeps only the last key",
     "Keeps both in a list",
     "Skips the duplicates"
    ],
    "a": 1,
    "w": "No error is raised and an entry disappears. If duplicates are possible, invert to lists - which is grouping by value."
   },
   {
    "t": "A dict mapping names to lists of scores cannot be inverted directly because:",
    "o": [
     "It is too large",
     "Lists are unhashable and so cannot be keys",
     "The names repeat",
     "Comprehensions do not allow it"
    ],
    "a": 1,
    "w": "Converting each value to a tuple makes it hashable and the inversion legal."
   }
  ]
 },
 {
  "path": "interview/how-does-a-python-dict-work.html",
  "title": "How does a Python dict work?",
  "cat": "Interview",
  "q": [
   {
    "t": "Dictionary lookup is O(1) because:",
    "o": [
     "Dictionaries are sorted",
     "The slot is computed from the key's hash rather than searched for",
     "Keys are unique",
     "It uses binary search"
    ],
    "a": 1,
    "w": "Neither hashing nor indexing depends on the number of entries. The key comparison at the slot is what makes it correct."
   },
   {
    "t": "Why does a resize have to rehash every key?",
    "o": [
     "Hashes change over time",
     "The index is hash % size, and size just changed",
     "To sort them",
     "To free memory"
    ],
    "a": 1,
    "w": "The hash is stable; the fold into a slot is not. Doubling the table moves nearly everything."
   },
   {
    "t": "Python randomises string hashes per process in order to:",
    "o": [
     "Improve distribution",
     "Stop an attacker crafting keys that all collide",
     "Save memory",
     "Preserve insertion order"
    ],
    "a": 1,
    "w": "Deliberately collided input turns every operation into a linear scan - a real denial-of-service attack. It is also why hash() differs between runs."
   }
  ]
 },
 {
  "path": "interview/design-a-hashmap.html",
  "title": "Implement a hash map from scratch",
  "cat": "Interview",
  "q": [
   {
    "t": "In separate chaining, a collision means:",
    "o": [
     "An error",
     "Both entries live in the same bucket's list",
     "The table resizes",
     "One key is overwritten"
    ],
    "a": 1,
    "w": "Collisions are expected. The lookup then compares keys along the chain, which is why the key comparison is not optional."
   },
   {
    "t": "Why does a resize have to rehash every key?",
    "o": [
     "Hashes expire",
     "The bucket index is hash % size, and the size just changed",
     "To sort the keys",
     "It does not"
    ],
    "a": 1,
    "w": "The hash is stable; the fold into a bucket is not. That single resize is O(n), amortised to O(1) per insert."
   },
   {
    "t": "Why is deletion harder in open addressing than in chaining?",
    "o": [
     "It needs more memory",
     "Blanking a slot breaks probe chains that ran through it, so tombstones are needed",
     "Keys become unhashable",
     "It is not harder"
    ],
    "a": 1,
    "w": "A later entry reached by probing past the deleted slot becomes unreachable. Tombstones let probes continue while allowing reuse."
   }
  ]
 },
 {
  "path": "interview/implement-substring-search.html",
  "title": "Implement substring search (strStr)",
  "cat": "Interview",
  "q": [
   {
    "t": "In KMP's search loop, which index never moves backwards?",
    "o": [
     "j, the pattern index",
     "i, the text index",
     "Both",
     "Neither"
    ],
    "a": 1,
    "w": "That is the O(n + m) guarantee. Naive search restarts at start + 1 and re-reads characters it has already seen."
   },
   {
    "t": "lps[i] stores:",
    "o": [
     "The character at i",
     "The length of the longest proper prefix of pattern[:i+1] that is also its suffix",
     "How many matches so far",
     "The next index to check"
    ],
    "a": 1,
    "w": "That overlap is exactly what tells the algorithm how far the pattern may slide without re-reading text."
   },
   {
    "t": "Naive substring search is genuinely quadratic on:",
    "o": [
     "Random text",
     "Highly repetitive text such as 'aaaa...ab' searched for 'aaab'",
     "Short patterns",
     "Unicode text"
    ],
    "a": 1,
    "w": "Nearly every alignment matches a long way before failing, so the same characters are read again and again."
   }
  ]
 },
 {
  "path": "interview/isomorphic-strings.html",
  "title": "Isomorphic strings",
  "cat": "Interview",
  "q": [
   {
    "t": "Why are two maps needed rather than one?",
    "o": [
     "For speed",
     "A single map allows two characters to map onto the same target",
     "To handle the empty string",
     "To keep it O(n)"
    ],
    "a": 1,
    "w": "'badc' against 'baba' passes every forward rule and is not isomorphic. The mapping has to be a bijection."
   },
   {
    "t": "The canonical-form approach compares:",
    "o": [
     "Sorted characters",
     "The order in which distinct characters first appear",
     "Character counts",
     "String lengths"
    ],
    "a": 1,
    "w": "'paper' and 'title' both become (0,1,2,0,3). It is the same 'canonicalise then compare' move as grouping anagrams."
   },
   {
    "t": "Why must the length check come before zip?",
    "o": [
     "zip is slow",
     "zip stops at the shorter string, so unequal lengths would compare only the overlap",
     "zip needs equal lengths",
     "It does not"
    ],
    "a": 1,
    "w": "'ab' and 'a' would otherwise be reported isomorphic on the basis of their first character alone."
   }
  ]
 },
 {
  "path": "interview/kth-largest-element.html",
  "title": "Kth largest element",
  "cat": "Interview",
  "q": [
   {
    "t": "Why a MIN-heap when you want the k LARGEST elements?",
    "o": [
     "It is faster to build",
     "Its root is the weakest kept value, which is the one to evict",
     "Max-heaps do not exist in Python",
     "It sorts as it goes"
    ],
    "a": 1,
    "w": "You need O(1) access to the smallest of the ones you are keeping, so a new larger value can replace it immediately."
   },
   {
    "t": "The heap approach uses how much memory?",
    "o": [
     "O(n)",
     "O(k)",
     "O(log n)",
     "O(n log k)"
    ],
    "a": 1,
    "w": "The heap never exceeds k entries. That is the whole reason to prefer it when n is huge or arrives as a stream."
   },
   {
    "t": "Quickselect's worst case is:",
    "o": [
     "O(n)",
     "O(n²), which a random pivot makes very unlikely",
     "O(n log n)",
     "O(log n)"
    ],
    "a": 1,
    "w": "A consistently bad pivot peels off one element at a time. Saying 'quickselect with a random pivot' pre-empts the follow-up."
   }
  ]
 },
 {
  "path": "interview/longest-common-prefix.html",
  "title": "Longest common prefix",
  "cat": "Interview",
  "q": [
   {
    "t": "Why does one pass suffice?",
    "o": [
     "The list is sorted",
     "The candidate prefix can only shrink, never grow",
     "Strings are immutable",
     "It does not"
    ],
    "a": 1,
    "w": "No word can lengthen a prefix that an earlier word already trimmed, so there is nothing to backtrack over."
   },
   {
    "t": "The longest possible answer is bounded by:",
    "o": [
     "The first string",
     "The shortest string in the list",
     "The number of strings",
     "The longest string"
    ],
    "a": 1,
    "w": "The prefix must be a prefix of every string, including the shortest one."
   },
   {
    "t": "Sorting the list and comparing only the first and last works because:",
    "o": [
     "Sorting groups similar strings",
     "In lexicographic order those two are the most different, so their shared prefix bounds every other pair",
     "It removes duplicates",
     "It is faster"
    ],
    "a": 1,
    "w": "Neat, and asymptotically worse - O(n log n · m). Offer it as an alternative, not as the main answer."
   }
  ]
 },
 {
  "path": "interview/longest-consecutive-sequence.html",
  "title": "Longest consecutive sequence",
  "cat": "Interview",
  "q": [
   {
    "t": "What makes the solution O(n) despite a loop inside a loop?",
    "o": [
     "The set is sorted",
     "Only the start of each run walks forward, so the inner loop does n steps in total",
     "The inner loop is capped",
     "It is actually O(n²)"
    ],
    "a": 1,
    "w": "Runs do not overlap, so total inner work is bounded by n. Each element is touched at most twice."
   },
   {
    "t": "How do you know a value starts a run?",
    "o": [
     "It is the smallest",
     "value - 1 is not in the set",
     "It appears first in the array",
     "It is even"
    ],
    "a": 1,
    "w": "If the predecessor exists, some other value will walk this run from its true start, so this one can be skipped entirely."
   },
   {
    "t": "Why is sorting not the accepted answer?",
    "o": [
     "It gives the wrong result",
     "It is O(n log n), and the question asks for O(n)",
     "It cannot handle duplicates",
     "It uses too much memory"
    ],
    "a": 1,
    "w": "Sorting is correct and simpler - give it first, name its cost, then improve to the set-based version."
   }
  ]
 },
 {
  "path": "interview/longest-palindromic-substring.html",
  "title": "Longest palindromic substring",
  "cat": "Interview",
  "q": [
   {
    "t": "How many centres does the expansion approach try?",
    "o": [
     "n",
     "2n - 1",
     "n²",
     "log n"
    ],
    "a": 1,
    "w": "n character centres for odd-length palindromes plus n-1 gap centres for even-length ones. Forgetting the gaps is the classic bug."
   },
   {
    "t": "Compared with the DP table, expanding around centres is:",
    "o": [
     "Faster asymptotically",
     "The same time, but O(1) space instead of O(n²)",
     "Slower",
     "Only correct for odd lengths"
    ],
    "a": 1,
    "w": "Both are O(n²) time. The space difference is the reason to prefer expansion, and noticing that is the point of the question."
   },
   {
    "t": "The O(n) algorithm for this problem is:",
    "o": [
     "Binary search",
     "Manacher's algorithm",
     "KMP",
     "Kadane's"
    ],
    "a": 1,
    "w": "It reuses already-found palindromes to skip work, in the same spirit as KMP's prefix table. Naming it is usually enough."
   }
  ]
 },
 {
  "path": "interview/longest-substring-without-repeating-characters.html",
  "title": "Longest substring without repeating characters",
  "cat": "Interview",
  "q": [
   {
    "t": "Why is `seen[ch] >= start` needed as well as `ch in seen`?",
    "o": [
     "To handle the first character",
     "A character last seen before the window must not drag the left edge backwards",
     "To count repeats",
     "To keep it O(n)"
    ],
    "a": 1,
    "w": "Only repeats inside the current window matter. 'abba' is the shortest input that gets the wrong answer without it."
   },
   {
    "t": "The time complexity is O(n) because:",
    "o": [
     "The string is short",
     "Both pointers only ever move forwards, for at most 2n moves total",
     "The dictionary is O(1)",
     "It uses recursion"
    ],
    "a": 1,
    "w": "The right edge advances n times and the left edge never retreats, so the total work is linear despite the nested feel."
   },
   {
    "t": "The space complexity is:",
    "o": [
     "O(n)",
     "O(k), one entry per distinct character",
     "O(1)",
     "O(n²)"
    ],
    "a": 1,
    "w": "The map holds distinct characters, so it is bounded by the alphabet - the answer most candidates get wrong."
   }
  ]
 },
 {
  "path": "interview/maximum-subarray-kadane.html",
  "title": "Maximum subarray sum (Kadane)",
  "cat": "Interview",
  "q": [
   {
    "t": "At each element, Kadane chooses between:",
    "o": [
     "Sorting or not",
     "Extending the current run or starting fresh from this element",
     "Left half or right half",
     "Adding or multiplying"
    ],
    "a": 1,
    "w": "Only those two can be the best subarray ending here. It is dynamic programming with the table reduced to one variable."
   },
   {
    "t": "Initialising best to 0 rather than values[0] breaks:",
    "o": [
     "Long arrays",
     "An all-negative array, which returns 0 - the empty subarray",
     "Arrays with duplicates",
     "Nothing"
    ],
    "a": 1,
    "w": "Zero is only reachable by choosing nothing at all. Ask whether the empty subarray is allowed before you commit."
   },
   {
    "t": "The space complexity of Kadane is:",
    "o": [
     "O(n)",
     "O(1)",
     "O(log n)",
     "O(n²)"
    ],
    "a": 1,
    "w": "Two running values and nothing else. The DP table collapses because each step depends only on the previous one."
   }
  ]
 },
 {
  "path": "interview/memoisation-with-a-dictionary.html",
  "title": "Memoisation: caching with a dictionary",
  "cat": "Interview",
  "q": [
   {
    "t": "Memoisation speeds up recursion by:",
    "o": [
     "Making each call faster",
     "Removing repeated calls for subproblems already solved",
     "Using less memory",
     "Avoiding recursion"
    ],
    "a": 1,
    "w": "The work drops to the number of distinct subproblems. The recurrence itself is unchanged."
   },
   {
    "t": "Caching a function that reads the current time gives you:",
    "o": [
     "A TypeError",
     "A stale answer returned forever",
     "A slower function",
     "Correct behaviour"
    ],
    "a": 1,
    "w": "The cache assumes purity. The bug then looks like wrong data rather than a wrong cache, which is what makes it nasty."
   },
   {
    "t": "Why must a cached function's arguments be hashable?",
    "o": [
     "For speed",
     "They are used as dictionary keys",
     "To allow recursion",
     "They need not be"
    ],
    "a": 1,
    "w": "That is why such functions often take tuples where you would expect lists - the constraint comes from the cache."
   }
  ]
 },
 {
  "path": "interview/merge-intervals.html",
  "title": "Merge overlapping intervals",
  "cat": "Interview",
  "q": [
   {
    "t": "Why does sorting by start make one pass sufficient?",
    "o": [
     "It removes duplicates",
     "An interval can then only overlap the merged block immediately before it",
     "It makes the list shorter",
     "Sorting merges them"
    ],
    "a": 1,
    "w": "Everything earlier starts earlier and has already been absorbed, so there is only ever one candidate to compare against."
   },
   {
    "t": "Why must the extend use max(last_end, this_end)?",
    "o": [
     "For speed",
     "A fully contained interval would otherwise shrink the merged block",
     "To handle negatives",
     "It does not matter"
    ],
    "a": 1,
    "w": "[1,10] then [2,3] would set the end to 3 and silently lose everything from 3 to 10."
   },
   {
    "t": "The overall complexity is:",
    "o": [
     "O(n)",
     "O(n log n), dominated by the sort",
     "O(n²)",
     "O(log n)"
    ],
    "a": 1,
    "w": "The sweep itself is linear. If the input arrives already sorted, the whole thing is O(n)."
   }
  ]
 },
 {
  "path": "interview/minimum-window-substring.html",
  "title": "Minimum window substring",
  "cat": "Interview",
  "q": [
   {
    "t": "Why is the shrink step a while loop rather than an if?",
    "o": [
     "To avoid an index error",
     "The window must keep shrinking while it stays valid, to find the minimum",
     "To count characters",
     "It could be an if"
    ],
    "a": 1,
    "w": "Stopping after one contraction records a valid window but not the smallest one ending at that right edge."
   },
   {
    "t": "Why update the missing counter on == rather than >=?",
    "o": [
     "It is faster",
     "With >= a surplus copy decrements it again, declaring the window valid too early",
     "== handles duplicates",
     "There is no difference"
    ],
    "a": 1,
    "w": "The counter tracks how many requirements are unmet, so it must change only when one crosses its threshold."
   },
   {
    "t": "The overall complexity is O(n) because:",
    "o": [
     "The window is small",
     "Each pointer only moves forward, so the total moves are bounded by 2n",
     "The counter is O(1)",
     "It is actually O(n²)"
    ],
    "a": 1,
    "w": "Same amortised argument as the other sliding-window problems - a nested loop is not automatically quadratic."
   }
  ]
 },
 {
  "path": "interview/product-of-array-except-self.html",
  "title": "Product of array except self",
  "cat": "Interview",
  "q": [
   {
    "t": "Why is division ruled out?",
    "o": [
     "It is slow",
     "A single zero makes every other answer a division by zero",
     "It loses precision",
     "It needs an extra array"
    ],
    "a": 1,
    "w": "Two zeros is worse still. You can special-case the zero count, but the question is really about the prefix/suffix decomposition."
   },
   {
    "t": "The extra space beyond the output array is:",
    "o": [
     "O(n) for the suffix array",
     "O(1) - the running product is a single variable",
     "O(log n)",
     "O(n²)"
    ],
    "a": 1,
    "w": "The left products are stored in the output array itself and the right product is carried in one variable."
   },
   {
    "t": "Why is the running product initialised to 1?",
    "o": [
     "To avoid zeros",
     "It is the identity for multiplication, so the first prefix contributes nothing",
     "To count elements",
     "It could be anything"
    ],
    "a": 1,
    "w": "A sum-based version of the same pattern would initialise to 0. Getting the identity wrong is the standard bug."
   }
  ]
 },
 {
  "path": "interview/remove-duplicates-in-place.html",
  "title": "Remove duplicates from a sorted array in place",
  "cat": "Interview",
  "q": [
   {
    "t": "Why does the function return a length rather than a list?",
    "o": [
     "Lists are slow",
     "Nothing was reallocated, so the tail still holds stale data",
     "To save memory",
     "It returns both"
    ],
    "a": 1,
    "w": "The point of the question is O(1) extra space. Building a new list would defeat it."
   },
   {
    "t": "The current element is compared against:",
    "o": [
     "values[read - 1]",
     "values[write - 1], the last element kept",
     "values[0]",
     "The next element"
    ],
    "a": 1,
    "w": "The last kept value is the invariant. The other comparison agrees on sorted input and is the wrong idea to carry forward."
   },
   {
    "t": "Writing into the array while reading it is safe because:",
    "o": [
     "The array is copied",
     "write never overtakes read, so only already-consumed slots are overwritten",
     "The array is sorted",
     "Python protects it"
    ],
    "a": 1,
    "w": "write lags behind by exactly the number of duplicates skipped, so it can never clobber unread input."
   }
  ]
 },
 {
  "path": "interview/reverse-a-string.html",
  "title": "Reverse a string",
  "cat": "Interview",
  "q": [
   {
    "t": "Why can't you reverse a Python string in place?",
    "o": [
     "It is too slow",
     "Strings are immutable - there is no in-place operation at all",
     "Slicing is required",
     "You can, with s.reverse()"
    ],
    "a": 1,
    "w": "In-place means working on a character list. str has no reverse() method for exactly this reason."
   },
   {
    "t": "The two-pointer reversal loop uses `while lo < hi` rather than `<=` because:",
    "o": [
     "It is faster",
     "With <= an odd-length string swaps its middle character with itself",
     "<= causes an index error",
     "The pointers never meet"
    ],
    "a": 1,
    "w": "Harmless but pointless. The condition is precisely what the question is testing."
   },
   {
    "t": "How many swaps does the in-place reversal make for n characters?",
    "o": [
     "n",
     "n/2",
     "n log n",
     "n - 1"
    ],
    "a": 1,
    "w": "Each swap places two characters, and the pointers meet in the middle. Memory is O(1) regardless of n."
   }
  ]
 },
 {
  "path": "interview/rotate-an-array.html",
  "title": "Rotate an array by k",
  "cat": "Interview",
  "q": [
   {
    "t": "The three-reversal rotation uses how much extra space?",
    "o": [
     "O(n)",
     "O(1)",
     "O(k)",
     "O(log n)"
    ],
    "a": 1,
    "w": "Only a couple of index variables. The slice version allocates a whole second array."
   },
   {
    "t": "Why is `k %= n` needed before the reversals?",
    "o": [
     "To handle negatives only",
     "A k larger than the array puts the block boundary out of range",
     "To make it faster",
     "It is not needed"
    ],
    "a": 1,
    "w": "Rotating by k and by k % n are the same operation, and without the modulo the second reversal is given invalid bounds."
   },
   {
    "t": "After reversing the whole array, why reverse each block again?",
    "o": [
     "To undo the rotation",
     "The blocks are in the right places but internally backwards",
     "To sort them",
     "To save memory"
    ],
    "a": 1,
    "w": "One reversal gets the two groups to the correct sides; the other two restore the order inside each group."
   }
  ]
 },
 {
  "path": "interview/string-compression.html",
  "title": "Run-length string compression",
  "cat": "Interview",
  "q": [
   {
    "t": "Why append to a list rather than build the result with +=?",
    "o": [
     "Lists are shorter",
     "+= allocates a new string per run, making the output building quadratic",
     "Strings cannot be concatenated",
     "join is required"
    ],
    "a": 1,
    "w": "The scan is linear either way; the difference is entirely in how the output is assembled."
   },
   {
    "t": "compress('abc') should return:",
    "o": [
     "'a1b1c1'",
     "'abc'",
     "''",
     "'abc3'"
    ],
    "a": 1,
    "w": "The compressed form is longer, so the original is returned. That final comparison is the most commonly forgotten line."
   },
   {
    "t": "The in-place variant is safe because:",
    "o": [
     "The array is copied first",
     "The write pointer can never overtake the read pointer when compression wins",
     "Runs are always long",
     "It uses recursion"
    ],
    "a": 1,
    "w": "Each run of length k is written as at most k characters, so written output stays behind consumed input."
   }
  ]
 },
 {
  "path": "interview/search-in-rotated-sorted-array.html",
  "title": "Search in a rotated sorted array",
  "cat": "Interview",
  "q": [
   {
    "t": "Why does binary search still apply after rotation?",
    "o": [
     "The array is still sorted",
     "At least one half of the window is always in order",
     "Rotation preserves indices",
     "It does not - you must sort first"
    ],
    "a": 1,
    "w": "A rotation makes two sorted runs, so mid always falls inside one of them. Identifying which is the whole trick."
   },
   {
    "t": "Having identified the sorted half, you decide where to search by:",
    "o": [
     "Comparing the target with mid",
     "Checking whether the target lies within that half's endpoint range",
     "Searching both halves",
     "Comparing with a[0]"
    ],
    "a": 1,
    "w": "In a sorted range, membership is a range check. If it is not in there, it can only be in the other half."
   },
   {
    "t": "With duplicates allowed, the worst case becomes:",
    "o": [
     "Still O(log n)",
     "O(n), because a[lo] == a[mid] == a[hi] reveals nothing",
     "O(n log n)",
     "Impossible"
    ],
    "a": 1,
    "w": "The only safe move is to shrink the window by one. This is a genuine lower bound and the standard follow-up question."
   }
  ]
 },
 {
  "path": "interview/sliding-window-maximum.html",
  "title": "Sliding window maximum",
  "cat": "Interview",
  "q": [
   {
    "t": "Why can a smaller value behind a larger one be discarded?",
    "o": [
     "To save memory",
     "Every future window containing it also contains the larger, later value",
     "It is already counted",
     "It cannot be"
    ],
    "a": 1,
    "w": "It can never be a maximum again, so keeping it is pure waste. That observation is the whole algorithm."
   },
   {
    "t": "Why store indices in the deque rather than values?",
    "o": [
     "Indices are smaller",
     "The front must be expired once it falls outside the window, which needs its position",
     "Values are not hashable",
     "It makes no difference"
    ],
    "a": 1,
    "w": "Without positions there is no way to distinguish a stale maximum from a current one."
   },
   {
    "t": "The algorithm is O(n) rather than O(n·k) because:",
    "o": [
     "k is small",
     "Each index is pushed once and popped at most once across the whole run",
     "The deque is sorted",
     "max() is O(1)"
    ],
    "a": 1,
    "w": "The inner while loop can pop several entries at once, but the total pops are bounded by n."
   }
  ]
 },
 {
  "path": "interview/sort-colors-dutch-national-flag.html",
  "title": "Sort an array of 0s, 1s and 2s",
  "cat": "Interview",
  "q": [
   {
    "t": "After swapping a 2 from mid to the high region, why must mid stay?",
    "o": [
     "To recount",
     "The value swapped back is from the unexamined region and has not been looked at",
     "To keep it stable",
     "It should advance"
    ],
    "a": 1,
    "w": "After a 0 swap the incoming value is a known 1, so mid can pass it. After a 2 swap it is unexamined - advancing leaves stray 2s."
   },
   {
    "t": "The regions maintained by the invariant are:",
    "o": [
     "Two",
     "Four: settled 0s, settled 1s, unexamined, settled 2s",
     "Three, all settled",
     "One"
    ],
    "a": 1,
    "w": "The unexamined region between mid and hi is the one people forget, and it is why the loop condition is mid <= hi."
   },
   {
    "t": "Why is the counting approach not the accepted answer?",
    "o": [
     "It is wrong",
     "It takes two passes, and does not generalise to sorting objects by a key",
     "It uses too much memory",
     "It is slower"
    ],
    "a": 1,
    "w": "It is correct and simple - give it first. The partition is asked for because it works on real records, not just on integers."
   }
  ]
 },
 {
  "path": "interview/subarray-sum-equals-k.html",
  "title": "Subarray sum equals k",
  "cat": "Interview",
  "q": [
   {
    "t": "Why is the prefix map seeded with {0: 1}?",
    "o": [
     "To avoid a KeyError",
     "So subarrays starting at index 0 are counted",
     "To count the empty subarray",
     "It is not needed"
    ],
    "a": 1,
    "w": "The empty prefix has sum 0. Without it, [7] with k=7 returns 0 - the simplest possible input fails."
   },
   {
    "t": "The map stores, for each prefix sum:",
    "o": [
     "Its index",
     "How many times it has occurred",
     "True or False",
     "The subarray"
    ],
    "a": 1,
    "w": "Several earlier positions can share a running sum, and each is a distinct qualifying subarray, so counts are needed rather than positions."
   },
   {
    "t": "Why can't a sliding window be used here?",
    "o": [
     "The array is unsorted",
     "Negative values mean extending the window can decrease the sum",
     "k might be zero",
     "It is too slow"
    ],
    "a": 1,
    "w": "A window relies on the sum growing monotonically as it grows. If everything is positive, the window works and uses O(1) space."
   }
  ]
 },
 {
  "path": "interview/trapping-rain-water.html",
  "title": "Trapping rain water",
  "cat": "Interview",
  "q": [
   {
    "t": "The water above a single bar equals:",
    "o": [
     "The tallest bar minus its height",
     "min(tallest to the left, tallest to the right) minus its height",
     "Its height",
     "The average of its neighbours"
    ],
    "a": 1,
    "w": "Water is held by the lower of the two containing walls. Anything above that level runs off."
   },
   {
    "t": "Why is it safe to settle the shorter side's water immediately?",
    "o": [
     "It is an approximation",
     "The shorter side is necessarily the smaller of the two maxima, so it alone decides",
     "Water flows left",
     "It is not safe"
    ],
    "a": 1,
    "w": "A bar at least as tall already exists on the other side, so the min is on this side and nothing further can change it."
   },
   {
    "t": "The two-pointer version improves on the precomputed-arrays version in:",
    "o": [
     "Time",
     "Space - O(1) instead of O(n)",
     "Correctness",
     "Both time and space"
    ],
    "a": 1,
    "w": "Both are O(n) time. Two running maxima replace two full arrays."
   }
  ]
 },
 {
  "path": "interview/two-sum.html",
  "title": "Two Sum",
  "cat": "Interview",
  "q": [
   {
    "t": "The one-pass solution works by:",
    "o": [
     "Sorting first",
     "Looking up the complement target - value in a dictionary",
     "Comparing every pair",
     "Using binary search"
    ],
    "a": 1,
    "w": "You know exactly which number you need, so it becomes a lookup rather than a search. That removes the inner loop."
   },
   {
    "t": "Why must you check before storing the current value?",
    "o": [
     "For speed",
     "Otherwise an element can pair with itself when the target is double it",
     "Dictionaries reject duplicates",
     "It does not matter"
    ],
    "a": 1,
    "w": "[3] with target 6 returns (0, 0) if you store first - a pair that does not exist."
   },
   {
    "t": "When is the two-pointer version preferable to the dictionary?",
    "o": [
     "Always",
     "When the input is already sorted and O(1) space matters",
     "When there are duplicates",
     "When the list is short"
    ],
    "a": 1,
    "w": "It needs no extra memory, but sorting just to enable it costs O(n log n) and destroys the original indices the question wants."
   }
  ]
 },
 {
  "path": "interview/valid-parentheses.html",
  "title": "Valid parentheses",
  "cat": "Interview",
  "q": [
   {
    "t": "Why is a counter not enough for multiple bracket types?",
    "o": [
     "Counters overflow",
     "'([)]' has balanced counts but the wrong nesting order",
     "Counters cannot go negative",
     "It is enough"
    ],
    "a": 1,
    "w": "A counter records how many are open, not which ones. Nesting is last-in-first-out, so it needs a stack."
   },
   {
    "t": "Which input passes every in-loop check and is still unbalanced?",
    "o": [
     "'(]'",
     "')('",
     "'((('",
     "'()'"
    ],
    "a": 2,
    "w": "Nothing inside the loop rejects unclosed openers. The final 'is the stack empty?' test is what catches it."
   },
   {
    "t": "Forgetting the empty-stack check before popping gives you:",
    "o": [
     "A wrong answer",
     "An IndexError",
     "An infinite loop",
     "The correct answer"
    ],
    "a": 1,
    "w": "Popping an empty list raises. It is the failure mode most likely to appear live in an interview."
   }
  ]
 },
 {
  "path": "interview/what-does-string-slicing-cost.html",
  "title": "What does slicing a string cost?",
  "cat": "Interview",
  "q": [
   {
    "t": "s[2:6] returns:",
    "o": [
     "A view into s",
     "A new string holding a copy of four characters",
     "A list of characters",
     "A generator"
    ],
    "a": 1,
    "w": "Python string slices always copy. The cost is O(k) in the length of the slice, in both time and memory."
   },
   {
    "t": "Why does peeling characters off the front with s = s[1:] go quadratic?",
    "o": [
     "The loop runs twice",
     "Each iteration copies the whole remaining string",
     "Strings are re-encoded",
     "len() is O(n)"
    ],
    "a": 1,
    "w": "n iterations copying an average of n/2 characters each is O(n²). Carrying an index copies nothing."
   },
   {
    "t": "Which type gives you a genuine zero-copy slice?",
    "o": [
     "str",
     "memoryview over bytes",
     "list",
     "tuple"
    ],
    "a": 1,
    "w": "memoryview shares the underlying buffer, so slicing it is O(1). It works on bytes-like objects, not on str."
   }
  ]
 },
 {
  "path": "interview/modifying-a-collection-while-iterating.html",
  "title": "What happens if you modify a collection while looping over it?",
  "cat": "Interview",
  "q": [
   {
    "t": "Deleting from a list while iterating over it:",
    "o": [
     "Raises RuntimeError",
     "Silently skips elements",
     "Works correctly",
     "Raises IndexError"
    ],
    "a": 1,
    "w": "Removing an element shifts the rest left while the loop index advances, so the shifted-in element is never visited. No error is raised, which makes it worse than the dict's behaviour."
   },
   {
    "t": "Which dict operation during iteration is legal?",
    "o": [
     "Deleting a key",
     "Adding a key",
     "Assigning to a key that already exists",
     "None of them"
    ],
    "a": 2,
    "w": "Only a size change trips the check. Reassigning an existing key leaves the size alone, so it is allowed."
   },
   {
    "t": "The preferred fix is:",
    "o": [
     "Iterate backwards",
     "Build a new collection with a comprehension",
     "Use a while loop",
     "Catch the RuntimeError"
    ],
    "a": 1,
    "w": "It mutates nothing, states the intent, and avoids the repeated O(n) removals. Iterating a copy is for when in-place mutation is genuinely required."
   }
  ]
 },
 {
  "path": "interview/what-is-a-python-list-underneath.html",
  "title": "What is a Python list underneath?",
  "cat": "Interview",
  "q": [
   {
    "t": "A Python list is implemented as:",
    "o": [
     "A linked list of nodes",
     "A dynamic array of references",
     "A hash table",
     "A balanced tree"
    ],
    "a": 1,
    "w": "Contiguous, equally sized references, over-allocated. That is why indexing is O(1) and why the references can point at objects of any type."
   },
   {
    "t": "Why is append 'amortised' O(1) rather than simply O(1)?",
    "o": [
     "It is always O(1)",
     "Occasionally it reallocates and copies everything, which is O(n)",
     "It depends on the item",
     "Because lists are sorted"
    ],
    "a": 1,
    "w": "Growth is geometric, so the copies are rare enough to average out - but any individual append can be the expensive one."
   },
   {
    "t": "insert(0, x) is O(n) because:",
    "o": [
     "The list is copied",
     "Every existing element shifts one slot right",
     "Python checks the type",
     "It reallocates every time"
    ],
    "a": 1,
    "w": "Contiguous storage means making room at the front costs a move of everything after it. deque avoids this entirely."
   }
  ]
 },
 {
  "path": "interview/accidental-quadratic-complexity.html",
  "title": "What is the complexity of this code?",
  "cat": "Interview",
  "q": [
   {
    "t": "for x in items: if x in a_list: ... has complexity:",
    "o": [
     "O(n)",
     "O(n²)",
     "O(n log n)",
     "O(1)"
    ],
    "a": 1,
    "w": "n iterations times an O(n) membership scan. Building a set before the loop makes it O(n)."
   },
   {
    "t": "Which fixes a queue built on list.pop(0)?",
    "o": [
     "Sorting the list",
     "collections.deque",
     "A set",
     "A tuple"
    ],
    "a": 1,
    "w": "pop(0) shifts every remaining element, so it is O(n) each and O(n²) overall. deque is O(1) at both ends."
   },
   {
    "t": "How do you demonstrate a quadratic without arguing about it?",
    "o": [
     "Read the source",
     "Double the input and show the time going up about fourfold",
     "Count the lines",
     "Profile one call"
    ],
    "a": 1,
    "w": "Growth is the observable property. Linear roughly doubles; quadratic roughly quadruples."
   }
  ]
 },
 {
  "path": "interview/str-versus-bytes-in-python.html",
  "title": "What is the difference between str and bytes?",
  "cat": "Interview",
  "q": [
   {
    "t": "b[0] where b is a bytes object gives you:",
    "o": [
     "A one-character bytes",
     "An int",
     "A str",
     "A TypeError"
    ],
    "a": 1,
    "w": "Indexing bytes yields the numeric value of that byte. Slicing gives bytes back; indexing does not."
   },
   {
    "t": "Decoding UTF-8 data as latin-1 produces:",
    "o": [
     "A UnicodeDecodeError",
     "Wrong text, with no error at all",
     "The same text",
     "An empty string"
    ],
    "a": 1,
    "w": "latin-1 maps every possible byte to some character, so it never fails. That silence is what makes mojibake hard to trace."
   },
   {
    "t": "Where should encode and decode happen in a well-structured program?",
    "o": [
     "Everywhere, as needed",
     "Only at the I/O boundaries, with str used throughout the middle",
     "Only on user input",
     "Never - Python handles it"
    ],
    "a": 1,
    "w": "The sandwich rule: decode on the way in, encode on the way out, and let every internal layer work in text."
   }
  ]
 },
 {
  "path": "interview/sets-versus-lists-and-deduplication.html",
  "title": "When should you use a set instead of a list?",
  "cat": "Interview",
  "q": [
   {
    "t": "Which deduplicates a list while preserving the original order?",
    "o": [
     "set(items)",
     "list(dict.fromkeys(items))",
     "sorted(set(items))",
     "items.unique()"
    ],
    "a": 1,
    "w": "Dicts have preserved insertion order since 3.7. sorted(set(...)) deduplicates and reorders, which is often shipped by accident."
   },
   {
    "t": "What can a list hold that a set cannot?",
    "o": [
     "Strings",
     "Unhashable elements such as lists",
     "Integers",
     "None"
    ],
    "a": 1,
    "w": "Set elements must be hashable, for the same reason dictionary keys must be. A tuple works where a list does not."
   },
   {
    "t": "'Which items are in A but not in B' is best written as:",
    "o": [
     "A loop with `if x not in b`",
     "set_a - set_b",
     "sorted(a) != sorted(b)",
     "a.remove(b)"
    ],
    "a": 1,
    "w": "The loop is O(n·m) when b is a list. The difference operator is O(n + m) and says what it means."
   }
  ]
 },
 {
  "path": "interview/why-are-python-strings-immutable.html",
  "title": "Why are Python strings immutable?",
  "cat": "Interview",
  "q": [
   {
    "t": "Why can a string be a dictionary key when a list cannot?",
    "o": [
     "Strings are shorter",
     "A string's value cannot change, so its hash cannot go stale",
     "Lists are not comparable",
     "Dictionaries only accept text"
    ],
    "a": 1,
    "w": "A key is stored in a slot chosen from its hash. If the value could change afterwards the entry would sit in the wrong slot and become unreachable, so only immutable types are allowed."
   },
   {
    "t": "What does s.upper() do to s?",
    "o": [
     "Uppercases it in place",
     "Nothing - it returns a new string",
     "Raises unless you assign it",
     "Depends on the encoding"
    ],
    "a": 1,
    "w": "Every string method returns a new object. Forgetting to assign the result is one of the most common beginner bugs in Python."
   },
   {
    "t": "Building a string with += in a loop is O(n²) because each step:",
    "o": [
     "Re-encodes to UTF-8",
     "Allocates a new string and copies everything so far",
     "Sorts the characters",
     "Grows the underlying list"
    ],
    "a": 1,
    "w": "There is nothing to append to, so the accumulated text is copied every time. \"\".join(parts) does one allocation and one copy instead."
   }
  ]
 },
 {
  "path": "interview/the-nested-list-multiplication-bug.html",
  "title": "Why does [[0]*3]*3 break?",
  "cat": "Interview",
  "q": [
   {
    "t": "[[0] * 3] * 3 creates:",
    "o": [
     "Three independent rows",
     "One row, referenced three times",
     "A 3x3 tuple",
     "An error"
    ],
    "a": 1,
    "w": "Multiplication repeats the reference. Writing through any of the three names is writing to the one object."
   },
   {
    "t": "a[:] on a list of lists gives you:",
    "o": [
     "A full independent copy",
     "A new outer list holding the same inner lists",
     "The same object",
     "A tuple"
    ],
    "a": 1,
    "w": "That is a shallow copy. Nested mutation is still shared; only copy.deepcopy duplicates all the way down."
   },
   {
    "t": "def f(x, acc=[]) misbehaves because the default is evaluated:",
    "o": [
     "On every call",
     "Once, when the function is defined",
     "Only on the first call that omits it",
     "Never"
    ],
    "a": 1,
    "w": "One list is created at definition time and shared by every call that omits the argument. Use None and build inside the function."
   }
  ]
 },
 {
  "path": "interview/string-interning-and-the-is-operator.html",
  "title": "Why does `is` sometimes work on strings?",
  "cat": "Interview",
  "q": [
   {
    "t": "Why is 'hello' is 'hello' often True?",
    "o": [
     "Strings are compared by value",
     "CPython interns identical short literals into one object",
     "is and == are the same",
     "Both are empty"
    ],
    "a": 1,
    "w": "Interning reuses one object. It is an optimisation immutability makes legal, not a language guarantee."
   },
   {
    "t": "'hello world' is ('hello' + ' world') is usually False because:",
    "o": [
     "The strings differ",
     "The second is built at runtime, so it is not interned",
     "Spaces are not allowed",
     "+ returns a list"
    ],
    "a": 1,
    "w": "The interner sees literals in compiled code. A string assembled while the program runs is a fresh object."
   },
   {
    "t": "The only safe use of `is` is with:",
    "o": [
     "Short strings",
     "None, True and False",
     "Numbers below 257",
     "Anything immutable"
    ],
    "a": 1,
    "w": "Those are singletons, so identity is genuinely the test you want. Everything else should use ==."
   }
  ]
 },
 {
  "path": "interview/why-is-in-slow-on-a-list.html",
  "title": "Why is `in` slow on a list but fast on a set?",
  "cat": "Interview",
  "q": [
   {
    "t": "x in my_list has complexity:",
    "o": [
     "O(1)",
     "O(n)",
     "O(log n)",
     "O(n log n)"
    ],
    "a": 1,
    "w": "A list has no index of its contents, so membership is a linear scan. A miss always costs the full length."
   },
   {
    "t": "Testing membership repeatedly against a large list is best fixed by:",
    "o": [
     "Sorting the list first",
     "Building a set once, before the loop",
     "Using a tuple",
     "Using enumerate"
    ],
    "a": 1,
    "w": "O(n) once plus O(1) per lookup, instead of O(n) per lookup. Building it inside the loop would be worse than not bothering."
   },
   {
    "t": "Which deduplicates a list while preserving order?",
    "o": [
     "set(items)",
     "list(dict.fromkeys(items))",
     "sorted(set(items))",
     "items.unique()"
    ],
    "a": 1,
    "w": "Dicts have preserved insertion order since 3.7, so their keys act as an ordered set. A set makes no ordering promise."
   }
  ]
 },
 {
  "path": "interview/why-must-dict-keys-be-hashable.html",
  "title": "Why must dictionary keys be hashable?",
  "cat": "Interview",
  "q": [
   {
    "t": "A list cannot be a dictionary key because:",
    "o": [
     "Lists are too large",
     "Mutating it would change its hash and orphan the entry",
     "Lists are not comparable",
     "Lists have no order"
    ],
    "a": 1,
    "w": "The hash is the address. A moving hash means a moving address, and the entry becomes unreachable."
   },
   {
    "t": "Is (1, [2]) hashable?",
    "o": [
     "Yes, tuples are always hashable",
     "No - a tuple's hash comes from its contents, and a list is mutable",
     "Only if the list is empty",
     "Yes, but slowly"
    ],
    "a": 1,
    "w": "Immutability has to hold all the way down. frozenset exists so that set-like values can be keys."
   },
   {
    "t": "Defining __eq__ on a class without __hash__ makes instances:",
    "o": [
     "Hash by identity",
     "Unhashable - Python sets __hash__ to None",
     "Hash by value automatically",
     "Immutable"
    ],
    "a": 1,
    "w": "You redefined equality, so the identity-based default hash no longer agrees with it. @dataclass(frozen=True) does both correctly."
   }
  ]
 },
 {
  "path": "interview/find-versus-index-on-strings.html",
  "title": "find() vs index() vs `in` — which one?",
  "cat": "Interview",
  "q": [
   {
    "t": "s.index('zzz') when 'zzz' is absent:",
    "o": [
     "Returns -1",
     "Raises ValueError",
     "Returns None",
     "Returns 0"
    ],
    "a": 1,
    "w": "That is the only difference from find. Use index when a miss means something upstream is broken and you want it to fail loudly."
   },
   {
    "t": "Why is `if s.find(x):` a bug?",
    "o": [
     "find is slow",
     "A match at index 0 is falsy, so it reads as not found",
     "find returns None",
     "It only works on lists"
    ],
    "a": 1,
    "w": "0 is a legitimate result and a falsy value. The test must be != -1, which is why `in` is preferred when you only need a bool."
   },
   {
    "t": "To find the second occurrence of a substring, the cheapest approach is:",
    "o": [
     "Slice the string and search again",
     "Pass a start index: s.find(x, first + 1)",
     "Reverse the string",
     "Use a regex"
    ],
    "a": 1,
    "w": "The start bound avoids copying the remainder, which slicing in a loop would do on every iteration."
   }
  ]
 },
 {
  "path": "interview/list-versus-tuple-versus-deque.html",
  "title": "list vs tuple vs deque vs array — which and why?",
  "cat": "Interview",
  "q": [
   {
    "t": "The most practical difference between a tuple and a list is that a tuple:",
    "o": [
     "Is faster",
     "Is hashable, so it can be a dict key or set member",
     "Uses less memory",
     "Cannot hold mixed types"
    ],
    "a": 1,
    "w": "Immutability is the mechanism; hashability is the consequence you actually reach for. It is why coordinates and cache keys are tuples."
   },
   {
    "t": "You need a queue. Which container?",
    "o": [
     "list, using pop(0)",
     "deque, using popleft()",
     "tuple",
     "set"
    ],
    "a": 1,
    "w": "pop(0) shifts every remaining element, so it is O(n) each and O(n²) overall. deque is O(1) at both ends."
   },
   {
    "t": "array.array uses less memory than a list of the same integers because it:",
    "o": [
     "Compresses them",
     "Stores the values inline rather than references to objects",
     "Uses fewer bits per number",
     "Shares objects"
    ],
    "a": 1,
    "w": "A list of a million numbers is a million pointers plus a million objects. The trade is that an array holds one type only."
   }
  ]
 },
 {
  "path": "machine_learning/bias_vs_variance.html",
  "title": "Bias vs Variance",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What is meant by “The Goal is Generalization” here?",
    "ans": "A low training error is meaningless if the validation error is high. The goal is always to build a model that performs well on data it has never seen before."
   },
   {
    "t": "What is meant by “Underfitting (High Bias)” here?",
    "ans": "Your model is too simple. Symptoms: High training error and high validation error."
   },
   {
    "t": "What is meant by “Overfitting (High Variance)” here?",
    "ans": "Your model is too complex. Symptoms: Very low training error but high validation error. The gap between them is large."
   },
   {
    "t": "What is meant by “The Tradeoff is Real” here?",
    "ans": "As you decrease bias by making your model more complex (e.g., adding more features or layers), you almost always increase its variance. The art of machine learning is finding the right level of complexity for the given data."
   }
  ]
 },
 {
  "path": "machine_learning/choosing_k.html",
  "title": "Choosing k: Elbow and Silhouette",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why can inertia alone never choose k?",
    "o": [
     "It is too slow to compute",
     "It falls at every increase in k and reaches zero when every point is its own cluster",
     "It requires spherical clusters",
     "It ignores cluster separation"
    ],
    "a": 1,
    "w": "Minimising it always answers 'as many clusters as possible'. It measures tightness around centres, not whether the grouping is good."
   },
   {
    "t": "What does a negative silhouette score for a point mean?",
    "o": [
     "The point is an outlier",
     "It is closer on average to a different cluster than to its own, so it is probably misassigned",
     "The clusters overlap",
     "k is too small"
    ],
    "a": 1,
    "w": "s = (b - a) / max(a, b), so s goes negative when the mean distance to the nearest other cluster is smaller than the mean distance within its own."
   },
   {
    "t": "Why does the silhouette have a genuine maximum while inertia does not?",
    "o": [
     "It is normalised between -1 and 1",
     "Adding clusters eventually pushes points close to a neighbouring cluster, which lowers the score",
     "It uses squared distances",
     "It is computed per cluster"
    ],
    "a": 1,
    "w": "It measures separation relative to tightness. Splitting a coherent group hurts the separation term, so the score falls rather than improving automatically."
   }
  ]
 },
 {
  "path": "machine_learning/confusion_matrix.html",
  "title": "Confusion Matrix Analysis",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "A disease affects 1% of people. A model that always predicts 'healthy' scores 99% accuracy. What does the confusion matrix show?",
    "o": [
     "A strong model",
     "Zero true positives - it never catches a single case",
     "Balanced precision and recall",
     "A high false positive rate"
    ],
    "a": 1,
    "w": "The whole top row of the matrix is empty. Accuracy hides this completely, which is exactly why the matrix is worth reading on any imbalanced problem."
   },
   {
    "t": "For a spam filter, which error is usually more costly?",
    "o": [
     "A false negative - spam reaching the inbox",
     "A false positive - a real email sent to the spam folder",
     "They are equally costly",
     "Neither matters if accuracy is high"
    ],
    "a": 1,
    "w": "A missed spam is an annoyance; a lost job offer is a disaster. This asymmetry is why you tune the threshold toward precision here, and toward recall for something like cancer screening."
   },
   {
    "t": "Recall answers which question?",
    "o": [
     "Of the cases I flagged, how many were real?",
     "Of the real cases, how many did I catch?",
     "How many predictions were correct overall?",
     "How balanced are the classes?"
    ],
    "a": 1,
    "w": "Recall divides by the actual positives, so it measures coverage of the true cases. Precision divides by your predicted positives and measures how trustworthy a flag is."
   }
  ]
 },
 {
  "path": "machine_learning/cosine_similarity.html",
  "title": "Cosine Similarity Metric",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Overview”?",
    "ans": "How do we measure how \"similar\" two things are, especially when they are represented as lists of numbers (vectors)? While we could measure the distance between their endpoints (Euclidean distance), Cosine Similarity offers a different perspective: it measures the angle between two vectors. This simple but powerful idea is fundamental to modern AI, from search engines to recommendation systems."
   },
   {
    "t": "What does this module say about “The Core Idea: It's All About Direction”?",
    "ans": "Imagine two arrows starting from the same point (the origin). Cosine similarity doesn't care about the length of these arrows (their \"magnitude\"); it only cares about the direction they are pointing."
   },
   {
    "t": "What does this module say about “Why angle rather than distance”?",
    "ans": "Here is the situation cosine similarity was invented for. Take two documents about football. One is a 200-word match report; the other is a 4,000-word essay on the same match. Count the words in each and you get two vectors: the essay's numbers are all roughly twenty times bigger."
   }
  ]
 },
 {
  "path": "machine_learning/dbscan_clustering.html",
  "title": "DBSCAN: Density-Based Clustering",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why can DBSCAN separate two interleaved crescents when k-means cannot?",
    "o": [
     "It uses more iterations",
     "Clusters spread through connected dense regions, so they can be any shape, while k-means draws straight boundaries between centres",
     "It scales the features first",
     "It knows the number of clusters"
    ],
    "a": 1,
    "w": "K-means assigns each point to the nearest centroid, so the boundary is always a straight line. DBSCAN never asks how far anything is from a centre."
   },
   {
    "t": "What is a border point?",
    "o": [
     "A point at the edge of the dataset",
     "A point within eps of a core point but without enough neighbours to be core itself",
     "A point equidistant from two clusters",
     "A point labelled noise"
    ],
    "a": 1,
    "w": "Core points have at least minPts neighbours within eps and drive the expansion; border points get swept in by them; everything else is noise."
   },
   {
    "t": "What is DBSCAN's main structural weakness?",
    "o": [
     "It needs k in advance",
     "One eps applies everywhere, so clusters of differing density cannot both be found",
     "It cannot label outliers",
     "It only works in two dimensions"
    ],
    "a": 1,
    "w": "The eps that finds a sparse cluster merges a dense one into its surroundings. HDBSCAN builds a hierarchy over eps values to handle exactly this."
   }
  ]
 },
 {
  "path": "machine_learning/data_leakage.html",
  "title": "Data Leakage",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why does fitting a StandardScaler before the train/test split count as leakage?",
    "o": [
     "It slows training down",
     "The mean and standard deviation are learned parameters, so test rows influence what the model sees",
     "It changes the test labels",
     "It only matters for k-NN"
    ],
    "a": 1,
    "w": "Anything that learns parameters from data must learn them from training data only. Otherwise the reported score stops being an estimate of performance on unseen data."
   },
   {
    "t": "What is the right question to ask about a suspicious feature?",
    "o": [
     "Is it correlated with the target?",
     "Would this value be present and correct at the moment a prediction is needed?",
     "Is it numeric or categorical?",
     "Does removing it hurt the score?"
    ],
    "a": 1,
    "w": "A cancellation reason correlates beautifully with churn and does not exist before the customer churns. Correlation is exactly what makes leaked features look valuable."
   },
   {
    "t": "Why does a random split leak on time-series data?",
    "o": [
     "The rows are correlated",
     "Future rows land in training and past rows in test, so the model predicts backwards after seeing what happened",
     "Time cannot be a feature",
     "The test set becomes too small"
    ],
    "a": 1,
    "w": "Production always predicts forward from the past. A random split evaluates a situation that can never occur, so the score does not describe the deployed system."
   }
  ]
 },
 {
  "path": "machine_learning/decision_tree.html",
  "title": "Decision Tree Analysis",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Overview”?",
    "ans": "A Decision Tree is one of the most intuitive and interpretable models in machine learning. It makes predictions by learning a series of simple \"if-then-else\" rules from the data, forming a tree-like structure. This lab visualizes the ID3 (Iterative Dichotomiser 3) algorithm, which builds the tree by asking one simple question at each step: \"Which feature gives me the most information to help classify my data?\""
   },
   {
    "t": "What does this module say about “The Core Idea: Maximizing Information Gain”?",
    "ans": "The goal of the ID3 algorithm is to build a tree that separates the data into pure groups (i.e., groups containing only a single class) as efficiently as possible. It does this by choosing the best feature to split on at each node. The \"best\" feature is the one that results in the most significant reduction in uncertainty, a concept measured by Information Gain ."
   },
   {
    "t": "What does this module say about “Entropy: A Measure of Impurity”?",
    "ans": "First, we measure the \"impurity\" or \"randomness\" of a set of data using a metric called Entropy . A dataset with a perfect mix of all classes (e.g., 50% 'Yes', 50% 'No') has the highest entropy (maximum uncertainty). A dataset with only one class (e.g., 100% 'Yes') has zero entropy (perfect certainty). Information Gain: The Reduction in Entropy"
   }
  ]
 },
 {
  "path": "machine_learning/evaluation_metrics_for_regression.html",
  "title": "Evaluation Metrics for Regression",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Overview”?",
    "ans": "In regression, our goal is to predict a continuous value, like a price or a temperature. But how do we know if our model's predictions are any good? Evaluation metrics are the tools we use to measure a model's performance and quantify its error. This lab visualizes four of the most common regression metrics, allowing you to see how they respond to changes in data and model fit in real-time."
   },
   {
    "t": "What does this module say about “The Four Key Metrics”?",
    "ans": "Each metric tells a slightly different story about your model's errors. The interactive plot above shows the true data points (green dots), the model's prediction line (orange), and the errors, or residuals (dashed red lines), which are the distances between each true point and the line."
   },
   {
    "t": "What does this module say about “Mean Squared Error (MSE)”?",
    "ans": "Definitions blur together until you put numbers through them. Here are five predicted and actual house prices, in thousands of pounds:"
   }
  ]
 },
 {
  "path": "machine_learning/feature_scaling.html",
  "title": "Feature Scaling",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why is k-NN affected by feature scaling but a decision tree is not?",
    "o": [
     "Trees ignore numeric columns",
     "k-NN sums squared differences, so the larger-scaled column dominates; a tree's splits are unchanged by any monotonic rescaling",
     "Trees scale internally",
     "k-NN requires normalised inputs to run"
    ],
    "a": 1,
    "w": "Rescaling changes `income > 45000` into `income' > 0.53`, which partitions exactly the same rows. Distance, by contrast, is dominated by whichever column has the biggest numbers."
   },
   {
    "t": "What is MinMaxScaler's main weakness compared with StandardScaler?",
    "o": [
     "It is slower",
     "It uses the minimum and maximum, so one extreme value compresses all the real data",
     "It cannot handle negative numbers",
     "It changes the shape of the distribution"
    ],
    "a": 1,
    "w": "Min and max are the two most outlier-sensitive statistics there are. One salary of ten million maps to 1.0 and pushes every real salary into a sliver at the bottom."
   },
   {
    "t": "Where must a scaler's mean and standard deviation come from?",
    "o": [
     "The whole dataset",
     "The training data only",
     "The test data",
     "A standard reference table"
    ],
    "a": 1,
    "w": "They are learned parameters. Computing them across everything lets test-set information reach the model before evaluation, and the reported score stops estimating anything."
   }
  ]
 },
 {
  "path": "machine_learning/permutation_importance.html",
  "title": "Feature and Permutation Importance",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why shuffle a column rather than delete it?",
    "o": [
     "Deleting is slower",
     "Deleting requires retraining, which gives a different model and answers a different question",
     "Shuffling preserves the correlation with other features",
     "Deleting breaks the input shape"
    ],
    "a": 1,
    "w": "Shuffling keeps the same fitted model and the same distribution, so the only thing that changed is whether that column still carries signal."
   },
   {
    "t": "Two near-identical informative features both show low importance. Why?",
    "o": [
     "They cancel each other out",
     "Shuffling one leaves the other intact, so the model uses the twin and loses almost no accuracy",
     "The model ignored both",
     "Their importance was divided between them"
    ],
    "a": 1,
    "w": "The metric is measured one column at a time. The honest reading is 'either one suffices', which this method cannot express - permute correlated groups together instead."
   },
   {
    "t": "What bias does a tree's built-in impurity importance have?",
    "o": [
     "It favours features used early in the tree",
     "It favours high-cardinality features, because more distinct values mean more split points to be chosen at",
     "It favours binary features",
     "It ignores correlated features"
    ],
    "a": 1,
    "w": "A random ID column can score above a useful binary flag. Permutation importance does not have this bias, at the cost of a re-scoring pass per feature."
   }
  ]
 },
 {
  "path": "machine_learning/gaussian_mixture_models.html",
  "title": "Gaussian Mixture Models",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does a GMM report for each point?",
    "o": [
     "A single cluster label",
     "A probability of belonging to each component",
     "A distance to the nearest centroid",
     "An outlier score"
    ],
    "a": 1,
    "w": "That is the point: a point in the overlap between two groups records its doubt, where k-means would label it without hesitation."
   },
   {
    "t": "What do the two steps of EM do?",
    "o": [
     "Split and merge clusters",
     "E computes responsibilities from the current parameters; M re-estimates parameters from those responsibilities",
     "Estimate then maximise the number of components",
     "Initialise then converge"
    ],
    "a": 1,
    "w": "It resolves a chicken-and-egg problem by alternating, and each iteration provably does not decrease the likelihood - though only to a local maximum."
   },
   {
    "t": "K-means is the special case of a GMM where:",
    "o": [
     "There is only one component",
     "Components are spherical and equally weighted, and responsibilities are forced to 0 or 1",
     "The covariance is full",
     "EM is run once"
    ],
    "a": 1,
    "w": "Which is why a GMM handles elliptical and unequally sized clusters that k-means cuts in half or splits evenly."
   }
  ]
 },
 {
  "path": "machine_learning/gradient_boosting.html",
  "title": "Gradient Boosting",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What is meant by “XGBoost” here?",
    "ans": "— the one that made boosting famous by winning competitions. Adds explicit L1 and L2 regularisation on leaf weights and a well-engineered handling of missing values, where each split learns a default direction for absent values."
   },
   {
    "t": "What is meant by “LightGBM” here?",
    "ans": "— the fastest on large data. It grows trees leaf-wise (always splitting the leaf that reduces loss most) rather than level by level, and bins continuous features into histograms. Usually the best choice above a few hundred thousand rows, but leaf-wise growth overfits small datasets unless you cap num_leaves ."
   },
   {
    "t": "What is meant by “CatBoost” here?",
    "ans": "— the one to reach for with many categorical columns. It encodes them with target statistics computed in a way that avoids leaking the target, and its defaults are unusually good, so it often wins with no tuning at all."
   }
  ]
 },
 {
  "path": "machine_learning/grid_vs_random_search.html",
  "title": "Grid Search against Random Search",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why does a 4x4 grid of 16 trials explore an important hyperparameter poorly?",
    "o": [
     "Grids are slower",
     "All four points in a column share the same value, so 16 trials give only 4 distinct values of that parameter",
     "It cannot sample the edges",
     "The lattice is biased toward the centre"
    ],
    "a": 1,
    "w": "The other trials in a column vary only the axis that does not matter. Random search of the same 16 trials gives 16 distinct values of every parameter."
   },
   {
    "t": "How should a learning rate be sampled in a random search?",
    "o": [
     "Uniformly between the bounds",
     "Log-uniformly",
     "Normally around the default",
     "In equal steps"
    ],
    "a": 1,
    "w": "Uniform sampling between 0.0001 and 0.1 puts about 90% of the draws above 0.01, which leaves the small-value region essentially unexplored."
   },
   {
    "t": "What should you check if the best value found sits at the edge of the search range?",
    "o": [
     "Nothing, edges are common",
     "Widen the range - no search finds what lies outside its bounds",
     "Reduce the number of trials",
     "Switch to grid search"
    ],
    "a": 1,
    "w": "A best value at the boundary is evidence the optimum is beyond it. The search reported the best point it was allowed to consider, not the best point."
   }
  ]
 },
 {
  "path": "machine_learning/handling_missing_values.html",
  "title": "Handling Missing Values",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does 'missing not at random' mean?",
    "o": [
     "The values were lost by a bug",
     "Whether a value is absent depends on the value itself, such as high earners declining to state income",
     "The missing rows are scattered evenly",
     "The column has no default"
    ],
    "a": 1,
    "w": "It is the hard case and the common one: dropping such rows removes a biased sample, and imputing a central value pulls every statistic toward the middle."
   },
   {
    "t": "Why does mean imputation weaken a column's correlations?",
    "o": [
     "It changes the units",
     "The imputed rows all carry the same value and no relationship to other columns, diluting the real relationship",
     "It introduces outliers",
     "It removes the column's variance entirely"
    ],
    "a": 1,
    "w": "A pile of identical values has no variance and no covariance with anything, so it drags every measured relationship toward zero."
   },
   {
    "t": "Why add a missing-value indicator column?",
    "o": [
     "To make the imputation reversible",
     "Because the fact that a value was absent is often predictive in itself",
     "It is required by scikit-learn",
     "It speeds up training"
    ],
    "a": 1,
    "w": "When absence depends on the value - high earners declining to answer - 'declined to answer' predicts the answer. Plain imputation throws that away for free."
   }
  ]
 },
 {
  "path": "machine_learning/hard_vs_soft_labelling.html",
  "title": "Hard vs Soft Labelling",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Overview”?",
    "ans": "When we train a classification model, we need to provide it with labeled data. The way we represent these labels can have a significant impact on how the model learns. This lab explores two common approaches: Hard Labelling and Soft Labelling . By comparing them side-by-side, you can build a strong intuition for why representing uncertainty can lead to more robust and nuanced models."
   },
   {
    "t": "What does this module say about “Defining the Labels”?",
    "ans": "Imagine you're training a model to classify the sentiment of a tweet as 'Negative', 'Neutral', or 'Positive'. How you tell the model the \"correct\" answer for each tweet is where labelling strategy comes in."
   },
   {
    "t": "What does this module say about “Hard Labelling (One-Hot Encoding)”?",
    "ans": "This is the most common approach. You are 100% certain about the class. The correct class gets a value of 1, and all other classes get a 0. It's a \"winner-takes-all\" method. Example Vector: For a 'Positive' tweet, the hard label is [0, 0, 1] . This tells the model, \"This tweet is positive, and nothing else.\" Soft Labelling (Probabilistic)"
   }
  ]
 },
 {
  "path": "machine_learning/hierarchical_clustering.html",
  "title": "Hierarchical Clustering and Dendrograms",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What is the advantage of building the whole tree?",
    "o": [
     "It is faster than k-means",
     "k is chosen after seeing the merge distances, rather than decided in advance",
     "It handles more data",
     "It labels outliers"
    ],
    "a": 1,
    "w": "One tree, and a horizontal cut at any height gives a clustering. Cutting just below a large jump in merge distance is the dendrogram's version of the elbow."
   },
   {
    "t": "What is chaining, and which linkage causes it?",
    "o": [
     "Complete linkage merging outliers",
     "Single linkage joining two separate blobs through a thin bridge of points, because any short hop is enough",
     "Average linkage producing equal-sized clusters",
     "Ward linkage minimising variance"
    ],
    "a": 1,
    "w": "Single linkage uses the nearest pair, so a bridge provides a cheap merge at every step. Complete linkage has the opposite failure: it breaks up genuinely elongated clusters."
   },
   {
    "t": "Why is hierarchical clustering impractical for large datasets?",
    "o": [
     "It needs too many iterations",
     "It requires an n-by-n distance matrix, so memory grows with the square of the point count",
     "Linkage cannot be computed at scale",
     "The dendrogram cannot be drawn"
    ],
    "a": 1,
    "w": "100,000 points is ten billion distances. Time is O(n^2 log n) at best, but memory is usually what stops you first."
   }
  ]
 },
 {
  "path": "machine_learning/isolation_forest.html",
  "title": "Isolation Forest",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why does a short average path length mean a point is anomalous?",
    "o": [
     "It is close to the root of the tree by chance",
     "A point far from the rest is separated by a random split quickly, while a point in a dense region needs many splits",
     "Short paths indicate low variance",
     "The tree is pruned around outliers"
    ],
    "a": 1,
    "w": "Path length is the effort required to isolate the point. No model of normality is ever built - the score falls out of how easy separation is."
   },
   {
    "t": "Why is each tree built from a small subsample?",
    "o": [
     "Only for speed",
     "It also reduces masking - in the full data a cluster of anomalies can shield its own members and look normal",
     "To avoid overfitting the threshold",
     "Because trees cannot handle large inputs"
    ],
    "a": 1,
    "w": "In a small sample those anomalies are usually alone and isolated immediately. It reduces swamping too - normal points looking anomalous because the data is crowded."
   },
   {
    "t": "Which anomaly does Isolation Forest tend to miss?",
    "o": [
     "A point far outside the whole dataset",
     "A point in a low-density gap between two dense clusters, which is normal globally but anomalous locally",
     "A duplicate row",
     "A point with an extreme value in one feature"
    ],
    "a": 1,
    "w": "It finds points that are globally easy to separate. Local Outlier Factor compares each point's density with its neighbours' and catches these instead."
   }
  ]
 },
 {
  "path": "machine_learning/cross_validation.html",
  "title": "K-Fold Cross Validation",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What problem does k-fold cross-validation solve?",
    "o": [
     "Slow training",
     "A single train/test split gives one noisy estimate that depends on which rows landed where",
     "Class imbalance",
     "Missing values"
    ],
    "a": 1,
    "w": "Every row gets to be in the test set exactly once, so the score is averaged over k splits instead of resting on one lucky or unlucky partition."
   },
   {
    "t": "For an imbalanced dataset, which variant should you reach for?",
    "o": [
     "Leave-one-out",
     "Stratified k-fold",
     "A single 50/50 split",
     "More folds"
    ],
    "a": 1,
    "w": "Stratification preserves the class ratio in every fold. Without it a rare class can be absent from a fold entirely, making that fold's score meaningless."
   },
   {
    "t": "What is the main cost of cross-validation?",
    "o": [
     "It needs more data",
     "You train k models instead of one",
     "It biases the estimate upward",
     "It cannot be used with neural networks"
    ],
    "a": 1,
    "w": "10-fold means ten training runs. That is usually fine for classical models and often prohibitive for large deep networks, which is why they typically use a single held-out set."
   }
  ]
 },
 {
  "path": "machine_learning/k_means.html",
  "title": "K-Means Clustering",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “What clustering is for, in plain words”?",
    "ans": "Most machine learning you meet first is supervised : someone hands you examples that are already labelled — this email is spam, that house sold for £320,000 — and the model learns to copy those labels on new data."
   },
   {
    "t": "What does this module say about “The tidying-up analogy”?",
    "ans": "Imagine a room with hundreds of books on the floor and you want them in five piles."
   },
   {
    "t": "What does this module say about “Initialisation decides the answer”?",
    "ans": "Place two initial centroids inside the same true cluster and k-means will happily split that cluster in half while merging two others. The result is stable, self-consistent and wrong."
   }
  ]
 },
 {
  "path": "machine_learning/knn.html",
  "title": "K-Nearest Neighbors",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "You set K = 1 and the decision boundary becomes jagged and unstable. That is a symptom of:",
    "o": [
     "Underfitting - the model is too simple",
     "Overfitting - the model is chasing individual points, noise included",
     "A bug in the distance calculation",
     "Too little training data"
    ],
    "a": 1,
    "w": "With K = 1 every single point, including mislabelled ones, gets its own territory. High variance and a jagged boundary are the classic signature of overfitting."
   },
   {
    "t": "Why does KNN need its features scaled?",
    "o": [
     "To speed up the distance computation",
     "Because a feature with a larger numeric range dominates the distance, regardless of its importance",
     "Because KNN assumes normally distributed data",
     "It does not need scaling"
    ],
    "a": 1,
    "w": "Distance sums squared differences. A salary in the tens of thousands swamps an age in the tens, so the model quietly becomes 'nearest by salary' no matter what you intended."
   },
   {
    "t": "KNN is called a lazy learner because:",
    "o": [
     "It is inaccurate",
     "It does no work at training time and defers everything to prediction time",
     "It only uses a subset of the data",
     "It converges slowly"
    ],
    "a": 1,
    "w": "Training is just storing the dataset. All the cost lands on prediction, when it must measure the new point against every stored one - which is why KNN is expensive to serve at scale."
   }
  ]
 },
 {
  "path": "machine_learning/label_encoding.html",
  "title": "Label Encoding Process",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Overview”?",
    "ans": "Machine learning models are mathematical functions; they understand numbers, not text. Before we can train a model on categorical data (like city names, product types, or sentiments), we must convert that text into a numerical format. Label Encoding is one of the simplest techniques to achieve this. It works by assigning a unique integer to each unique category or \"label\" in your dataset."
   },
   {
    "t": "What does this module say about “How It Works: Building the Vocabulary”?",
    "ans": "The process is straightforward and consists of two main steps, which you can see in action by clicking the \"Encode Corpus\" button above."
   },
   {
    "t": "What does this module say about “Create a Vocabulary”?",
    "ans": "First, the encoder scans the entire input text (the \"corpus\") to find all unique words (or \"tokens\"). It then sorts these unique words alphabetically to create a consistent vocabulary. This vocabulary acts as a dictionary or a look-up table. 2. Assign Integer IDs"
   }
  ]
 },
 {
  "path": "machine_learning/label_imbalance_problem.html",
  "title": "Label Imbalance Problem",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Overview”?",
    "ans": "In many real-world scenarios, the data we care about is rare. Think of credit card fraud, rare disease detection, or critical system failures. In these datasets, the \"normal\" class vastly outnumbers the \"anomaly\" class. This is called Label Imbalance , and it creates a dangerous trap for machine learning models: The Accuracy Paradox ."
   },
   {
    "t": "What does this module say about “What is the Accuracy Paradox”?",
    "ans": "The Accuracy Paradox occurs when a model achieves a very high accuracy score but is completely useless in practice. This happens because the model learns to simply predict the majority class every single time. In a dataset with 99% normal transactions and 1% fraudulent ones, a model that always guesses \"normal\" will be 99% accurate. It sounds great, but it has failed at its one important job: detecting fraud."
   },
   {
    "t": "What does this module say about “The \"Naive\" Model”?",
    "ans": "This is a deliberately dumb model. Its only rule is: always predict Class 0 (the majority class) . It never predicts an anomaly. As you'll see, its accuracy is deceptively high. 2. The Standard Trained Model"
   }
  ]
 },
 {
  "path": "machine_learning/learning_curves.html",
  "title": "Learning Curves",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Training error is high and the two curves have converged. What does that mean?",
    "o": [
     "Variance - collect more data",
     "Bias - the model is too simple, and more data will not help",
     "The split is wrong",
     "The model is well fitted"
    ],
    "a": 1,
    "w": "The model cannot fit data it has already seen, so unseen data is not the problem. The curves have already converged, so adding examples moves neither."
   },
   {
    "t": "What tells you whether collecting more data will help?",
    "o": [
     "The size of the gap",
     "Whether the validation curve is still falling at your current dataset size",
     "The training error alone",
     "The number of features"
    ],
    "a": 1,
    "w": "A still-descending validation curve means more examples will improve the model, and its slope suggests by how much. A flat one means the effort belongs elsewhere."
   },
   {
    "t": "High training error AND a large gap suggests what?",
    "o": [
     "Severe overfitting",
     "A bug - check the split, the labels, and whether validation comes from a different distribution",
     "Ideal capacity",
     "Too much regularisation"
    ],
    "a": 1,
    "w": "Bias and variance alone do not produce that combination. It usually means mislabelled data or a validation set drawn from somewhere else."
   }
  ]
 },
 {
  "path": "machine_learning/linear_regression_with_ols.html",
  "title": "Linear Regression with OLS",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Ordinary least squares minimises the sum of:",
    "o": [
     "The residuals",
     "The squared residuals",
     "The absolute residuals",
     "The predicted values"
    ],
    "a": 1,
    "w": "Squaring makes every error positive so they cannot cancel, and it gives a smooth function with a closed-form solution. It also punishes large errors disproportionately."
   },
   {
    "t": "Why does OLS react so strongly to a single far-off point?",
    "o": [
     "Because it uses the mean",
     "Because squaring makes a distant point dominate the total error",
     "Because the data must be normal",
     "It does not - OLS is robust"
    ],
    "a": 1,
    "w": "An error of 10 contributes 100; an error of 1 contributes 1. One outlier can outweigh a hundred well-fitted points, which is why absolute-error methods are preferred when outliers are expected."
   },
   {
    "t": "R-squared of 0.0 means:",
    "o": [
     "The model is perfect",
     "The model explains no more variance than predicting the mean",
     "The data has no variance",
     "The model is broken"
    ],
    "a": 1,
    "w": "R-squared compares your model against the trivial always-predict-the-mean baseline. Zero means you have matched that baseline and no more. It can even go negative if you do worse."
   }
  ]
 },
 {
  "path": "machine_learning/logistic_regression.html",
  "title": "Logistic Regression",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Logistic regression computes a linear score and squashes it through a sigmoid to get a probability, which makes the decision boundary a straight line and the output something you can actually reason about. It is trained with log loss because that surface is convex and punishes confident mistakes properly."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Linear regression predicts a number. If you need a yes or no, you cannot use it directly: it happily predicts −4 or 17, and neither is a probability. Logistic regression fixes this with one extra step. It computes the same weighted sum, then passes the result through a function that squashes any real number into the range 0 to 1."
   },
   {
    "t": "What does this module say about “Work one through by hand”?",
    "ans": "Take weights w = [1.0, 1.0] and bias b = −10 , the values this page starts on. Feed it the point (4, 4) :"
   }
  ]
 },
 {
  "path": "machine_learning/model_and_data_drift.html",
  "title": "Model and Data Drift",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Overview”?",
    "ans": "A machine learning model is a snapshot of the world at the moment it was trained. But the world is not static. Customer preferences change, economic conditions shift, and new patterns emerge. Model Drift is the degradation of a model's predictive power over time because the real-world environment has changed since the model was deployed."
   },
   {
    "t": "What does this module say about “Types of Drift”?",
    "ans": "This occurs when the fundamental relationship between the input variables and the target variable changes. The \"rules of the game\" have changed. In the visualization, the green dashed line (the true underlying pattern) will slowly change its shape over time, while the data points continue to follow it. The deployed model ( red line ), which learned the original pattern, becomes increasingly wrong. 2."
   },
   {
    "t": "What does this module say about “Concept Drift”?",
    "ans": "This occurs when the fundamental relationship between the input variables and the target variable changes. The \"rules of the game\" have changed. In the visualization, the green dashed line (the true underlying pattern) will slowly change its shape over time, while the data points continue to follow it. The deployed model ( red line ), which learned the original pattern, becomes increasingly wrong. 2."
   }
  ]
 },
 {
  "path": "machine_learning/naive_bayes.html",
  "title": "Naive Bayes Classifier",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Overview”?",
    "ans": "The Naive Bayes Classifier is a simple yet powerful algorithm for predictive modeling. It's based on Bayes' Theorem and is particularly useful for text classification, like spam filtering. Its core idea is to calculate the probability of a certain outcome (e.g., \"Should I play tennis?\") based on the evidence provided by a set of features (e.g., the weather outlook, temperature, and wind)."
   },
   {
    "t": "What does this module say about “The \"Naive\" Assumption: A Key Simplification”?",
    "ans": "The \"naive\" part of the name comes from a key assumption the algorithm makes: it assumes that all features are independent of each other . In our example, it assumes that the 'Outlook' has no effect on the 'Temperature' or 'Wind'. While this is often not true in the real world (a sunny outlook usually implies hotter temperatures), this simplification makes the calculations much easier and faster."
   },
   {
    "t": "What does this module say about “Bayes' theorem without the fear”?",
    "ans": "Everything here rests on one line, and the line is less intimidating written as a sentence."
   }
  ]
 },
 {
  "path": "machine_learning/one_hot_encoding.html",
  "title": "One-Hot Encoding",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why not just number categories 1, 2, 3 and feed them in directly?",
    "o": [
     "Numbers are slower to process",
     "It invents an order and a distance that the categories do not have",
     "Models cannot accept integers",
     "It uses more memory"
    ],
    "a": 1,
    "w": "Labelling red=1, green=2, blue=3 tells the model green sits between red and blue, and that blue is three times red. Both are nonsense, and a linear model will act on them."
   },
   {
    "t": "A column has 50,000 distinct values. One-hot encoding it will:",
    "o": [
     "Work fine",
     "Create 50,000 mostly-zero columns, which is usually unusable",
     "Fail with an error",
     "Automatically group rare values"
    ],
    "a": 1,
    "w": "High-cardinality columns explode under one-hot encoding. This is where target encoding, hashing or learned embeddings earn their keep instead."
   },
   {
    "t": "When does label encoding become the right choice?",
    "o": [
     "Never",
     "When the categories genuinely have an order, like small/medium/large",
     "Whenever there are more than 10 categories",
     "Only for the target variable"
    ],
    "a": 1,
    "w": "Ordinal data has a real ordering, so encoding it as 1/2/3 preserves information rather than fabricating it. Tree-based models are also far more tolerant of integer codes than linear ones."
   }
  ]
 },
 {
  "path": "machine_learning/outliers_and_influence.html",
  "title": "Outliers and Influence",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why does least squares react so strongly to a single distant point?",
    "o": [
     "It weights recent points more",
     "It minimises squared error, so a point twice as far off pulls four times as hard",
     "It ignores points near the mean",
     "It fits the maximum rather than the average"
    ],
    "a": 1,
    "w": "The objective is willing to move a long way to reduce one large residual, even at a small cost to every other point. That is what the loss function asks for."
   },
   {
    "t": "What makes a point 'influential' rather than merely an outlier?",
    "o": [
     "It has a large residual",
     "It is unusual in x as well as y, so removing it changes the model",
     "It is the newest observation",
     "It has a missing value"
    ],
    "a": 1,
    "w": "The line pivots about the mean of x, so a point far along x sits at the end of a long lever. Extreme in y near the pivot is harmless; the combination is not."
   },
   {
    "t": "What is wrong with removing anything beyond three standard deviations?",
    "o": [
     "Three is too strict",
     "The outlier has already inflated the standard deviation being used to judge it",
     "It requires a normal distribution",
     "It removes too few points"
    ],
    "a": 1,
    "w": "The rule uses a statistic the outlier corrupts, so a large enough outlier widens the threshold enough to protect itself. Robust measures like the median absolute deviation avoid this."
   }
  ]
 },
 {
  "path": "machine_learning/partial_dependence_and_shap.html",
  "title": "Partial Dependence, ICE and SHAP",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "A partial dependence curve is flat. What can you conclude?",
    "o": [
     "The feature does not matter",
     "Only that the average effect is near zero - it may matter enormously in opposite directions by subgroup",
     "The model is underfitted",
     "The feature is correlated with another"
    ],
    "a": 1,
    "w": "Plotting ICE curves settles it: if they are parallel the average is a fair summary; if they fan out or cross, there is an interaction the average cancels."
   },
   {
    "t": "What does the additivity of SHAP values give you?",
    "o": [
     "Faster computation",
     "The values sum exactly to the gap between the base value and this prediction, so nothing is unattributed",
     "Independence from the model type",
     "Causal interpretation"
    ],
    "a": 1,
    "w": "That is what makes it usable as an explanation of a single prediction. Exact computation is exponential, so TreeSHAP and KernelSHAP approximate it."
   },
   {
    "t": "Why can part of a partial dependence curve be untrustworthy when features are correlated?",
    "o": [
     "The averaging is biased",
     "It sets the feature to values that never co-occur with the other columns, so the model is extrapolating",
     "The curve becomes non-monotonic",
     "ICE curves cannot be computed"
    ],
    "a": 1,
    "w": "Sweeping age across every row creates people aged 18 with forty years of experience. ALE plots avoid this by varying a feature only within ranges that actually occur."
   }
  ]
 },
 {
  "path": "machine_learning/ml_pipelines.html",
  "title": "Pipelines",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does cross-validating a pipeline do that cross-validating a model does not?",
    "o": [
     "It runs faster",
     "It refits every preprocessing step on each fold's training portion",
     "It uses more folds",
     "It tunes hyperparameters automatically"
    ],
    "a": 1,
    "w": "Preprocessing fitted by hand beforehand has already seen every validation row. Inside a pipeline the correct order is the only thing the object can do."
   },
   {
    "t": "Why does a pipeline remove the train/serve gap?",
    "o": [
     "It compresses the model",
     "The fitted object contains the preprocessing, so there is no second implementation to drift out of step",
     "It logs predictions",
     "It validates input types"
    ],
    "a": 1,
    "w": "Reimplementing preprocessing in the serving code is a common production failure and a silent one - the model receives differently-prepared inputs and quietly degrades."
   },
   {
    "t": "What does a pipeline NOT protect you from?",
    "o": [
     "Fitting a scaler on test data",
     "Splits that were wrong to begin with, such as one patient appearing on both sides",
     "Imputing before scaling",
     "Feature selection leakage"
    ],
    "a": 1,
    "w": "It fits each fold correctly but cannot know your folds are badly formed. Grouped data needs GroupKFold and time series need TimeSeriesSplit."
   }
  ]
 },
 {
  "path": "machine_learning/precision_recall_and_f1.html",
  "title": "Precision, Recall and F1",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What happens to precision and recall as the threshold falls?",
    "o": [
     "Both rise",
     "Both fall",
     "Recall rises and precision falls",
     "They are unaffected by the threshold"
    ],
    "a": 2,
    "w": "A lower threshold flags more cases, so more real positives are caught (recall up) but the flagged set fills with negatives (precision down). The threshold picks a point on the trade-off, it does not improve the model."
   },
   {
    "t": "Why is F1 a harmonic rather than arithmetic mean?",
    "o": [
     "It is faster to compute",
     "The harmonic mean is pulled toward the smaller value, so it stays low unless both are high",
     "It bounds the result to [0, 1]",
     "It handles zero denominators"
    ],
    "a": 1,
    "w": "Precision 1.0 with recall 0.01 averages arithmetically to a respectable 0.505 and gives an F1 of 0.0198. The harmonic mean refuses to be gamed by a degenerate model."
   },
   {
    "t": "Why is accuracy misleading when 1% of cases are positive?",
    "o": [
     "It ignores true negatives",
     "Predicting 'never positive' scores 99% while catching nothing",
     "It cannot be computed",
     "It depends on the threshold"
    ],
    "a": 1,
    "w": "Accuracy measures the class balance more than the model. Precision and recall would both be zero, which is the honest description of that model."
   }
  ]
 },
 {
  "path": "machine_learning/precision_recall_vs_roc.html",
  "title": "Precision-Recall against ROC",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why does ROC stay flattering as positives become rare?",
    "o": [
     "It uses accuracy",
     "TPR and FPR are each computed within one class, so neither depends on the balance between them",
     "It ignores false positives",
     "It is computed at a single threshold"
    ],
    "a": 1,
    "w": "Adding a million negatives leaves TPR untouched and changes FPR only through its own proportionally larger denominator. Precision's denominator mixes both classes, so it falls."
   },
   {
    "t": "10,000 rows, 100 positive, 90% recall and 5% false positive rate. What is precision?",
    "o": [
     "90%",
     "About 15%",
     "About 50%",
     "5%"
    ],
    "a": 1,
    "w": "90 true positives against 495 false positives from the 9,900 negatives gives 90/585, about 15%. A 5% FPR sounds excellent and produces five wrong flags for every right one."
   },
   {
    "t": "What is the no-skill baseline on a PR curve?",
    "o": [
     "The diagonal",
     "A horizontal line at the positive rate",
     "Always 0.5",
     "There is none"
    ],
    "a": 1,
    "w": "It moves with the base rate, which is why a PR AUC must never be quoted without it. 0.4 is poor on balanced data and outstanding at a 2% positive rate."
   }
  ]
 },
 {
  "path": "machine_learning/pca.html",
  "title": "Principal Component Analysis",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does the first principal component point along?",
    "o": [
     "The direction that best separates the classes",
     "The direction the data varies along most",
     "The column with the largest values",
     "The line minimising vertical distance to the target"
    ],
    "a": 1,
    "w": "PC1 maximises uᵀΣu - the variance measured along the direction u. It has never seen your labels, which is why it is unsupervised and why it can happily discard the direction that separates the classes."
   },
   {
    "t": "Two features are almost perfectly correlated. What happens to the second eigenvalue?",
    "o": [
     "It grows",
     "It stays the same",
     "It collapses towards zero",
     "It becomes negative"
    ],
    "a": 2,
    "w": "Perfect correlation means the cloud lies on a line: there is no spread in the perpendicular direction, so λ₂ is zero and PC1 explains 100%. Two columns, one dimension of information."
   },
   {
    "t": "Why must you usually standardise the columns before running PCA?",
    "o": [
     "Otherwise the maths is undefined",
     "Because variance carries units, so a column measured in large numbers dominates the first component",
     "To make the components interpretable",
     "To speed up the eigen-decomposition"
    ],
    "a": 1,
    "w": "PCA maximises variance, and variance is in squared units. Income in rupees next to age in years makes income the first component no matter what the data means."
   }
  ]
 },
 {
  "path": "machine_learning/probability_calibration.html",
  "title": "Probability Calibration",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why is AUC unchanged as the temperature slider moves?",
    "o": [
     "AUC is insensitive to class imbalance",
     "Temperature scaling is monotonic, so it never changes the order of any two predictions",
     "The model is retrained each time",
     "AUC uses only the top predictions"
    ],
    "a": 1,
    "w": "Every ranking metric is identical at every setting, while calibration swings from badly over-confident to badly under-confident. Looking only at AUC tells you nothing about calibration."
   },
   {
    "t": "A reliability curve sits below the diagonal. The model is:",
    "o": [
     "Under-confident",
     "Over-confident",
     "Well calibrated",
     "Poorly ranked"
    ],
    "a": 1,
    "w": "It says 0.9 and is right 70% of the time. This is the common failure mode for modern neural networks, and the damaging one when probabilities feed decisions."
   },
   {
    "t": "When does calibration not matter?",
    "o": [
     "When the model is a neural network",
     "When the output is only used to rank - showing the top 100 results, say",
     "When the classes are balanced",
     "When AUC is high"
    ],
    "a": 1,
    "w": "It matters whenever a probability feeds a decision with costs, because expected value is probability times payoff, so a wrong probability is a wrong decision."
   }
  ]
 },
 {
  "path": "machine_learning/roc_curve_and_auc.html",
  "title": "ROC Curve and AUC",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A classifier does not really output a class. It outputs a score — a probability, usually — and something else turns that into a label by comparing it against a threshold. The confusion matrix describes one such threshold. Change the threshold and you get a different matrix from the very same model."
   },
   {
    "t": "What does this module say about “What AUC actually measures”?",
    "ans": "The area under that curve compresses the whole picture into one number between 0 and 1."
   },
   {
    "t": "What does this module say about “One model, every threshold”?",
    "ans": "A classifier that outputs probabilities is not one classifier — it is a family of them, one for every threshold you might pick. Threshold at 0.9 and you get a cautious model; threshold at 0.1 and you get an eager one. Accuracy, precision and recall all describe a single member of that family."
   }
  ]
 },
 {
  "path": "machine_learning/random_forest.html",
  "title": "Random Forest and Bagging",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A random forest trains many deep, deliberately different trees and lets them vote, which cancels the variance that makes any single deep tree unreliable. The diversity comes from two places — a bootstrap sample of the rows and a random subset of the features at every split — and without that diversity extra trees buy nothing."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A decision tree grown to full depth will classify every training point correctly. It does this by carving the space into ever smaller rectangles until each one is pure — including rectangles that exist only to accommodate a single mislabelled point. The result has near-perfect training accuracy and a boundary that looks like a staircase drawn during an earthquake."
   },
   {
    "t": "What does this module say about “What makes a forest more than bagging”?",
    "ans": "Bagged trees have a weakness: if one feature is strongly predictive, nearly every tree splits on it first, and the trees end up highly correlated. Averaging correlated models buys much less than averaging independent ones."
   }
  ]
 },
 {
  "path": "machine_learning/ridge_and_lasso_regression.html",
  "title": "Ridge and Lasso Regression",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Give a degree-12 polynomial eighteen noisy points and it will pass through nearly all of them. The fit looks superb on the data it has seen, and it is worthless: between the points the curve swings violently, because the only way to hit every point is to use enormous coefficients that cancel each other out."
   },
   {
    "t": "What does this module say about “One extra term”?",
    "ans": "Ordinary least squares minimises the squared error alone. Ridge and Lasso add a penalty on the size of the weights:"
   },
   {
    "t": "What does this module say about “Why Lasso zeroes and Ridge does not”?",
    "ans": "Look at how each penalty behaves as a coefficient approaches zero. The derivative of w 2 is 2w , which itself goes to zero — so the closer a Ridge coefficient gets to zero, the weaker the force pushing it further. It approaches zero and never arrives."
   }
  ]
 },
 {
  "path": "machine_learning/sliding_window_for_timeseries_data.html",
  "title": "Sliding Window for Time Series",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A sliding window converts a time series into supervised (input, target) pairs, with the window size encoding how much history you claim is relevant and the stride controlling how much consecutive examples overlap. The modelling choice is straightforward; the discipline is in the split — chronological, with a gap of at least one window between segments, and every scaler fitted on the training period alone."
   },
   {
    "t": "What does this module say about “Turning a sequence into a supervised problem”?",
    "ans": "A model needs examples with features and a label. A time series is a single ordered run of values, so you build examples by sliding a fixed-length window along it: the values inside the window are the input, and the value immediately after it is the target."
   },
   {
    "t": "What does this module say about “Window size and stride”?",
    "ans": "Window size (W) is how much history the model sees per prediction, and it is a real modelling assumption: it asserts that nothing older than W steps matters. Too small and the model cannot see the pattern — a weekly cycle needs at least seven daily steps. Too large and each example carries mostly irrelevant history, the input dimension grows, and the number of examples shrinks."
   }
  ]
 },
 {
  "path": "machine_learning/stacking_and_voting.html",
  "title": "Stacking and Voting Ensembles",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why can a majority vote score worse than its best member?",
    "o": [
     "The vote discards probabilities",
     "Every member counts equally, so two weak learners can outvote a strong one whenever they agree",
     "Voting requires an odd number of models",
     "The members were not calibrated"
    ],
    "a": 1,
    "w": "It is what happens whenever an ensemble is assembled without checking the members are comparable in quality - which is why 'just ensemble it' is bad advice."
   },
   {
    "t": "Why must the meta-learner be trained on cross-validated predictions?",
    "o": [
     "To save computation",
     "In-sample predictions look suspiciously good for an overfitted base model, so the meta-learner learns to trust it",
     "To balance the classes",
     "Because base models need to be retrained anyway"
    ],
    "a": 1,
    "w": "Every prediction the meta-learner sees has to be out-of-sample. It is why stacking costs roughly k times the training of its members."
   },
   {
    "t": "What condition must hold for an ensemble to help at all?",
    "o": [
     "The members must be the same type of model",
     "The members must make different mistakes",
     "There must be an odd number of members",
     "The members must be calibrated"
    ],
    "a": 1,
    "w": "Three models that fail on the same rows combine into one model that fails on those rows. Checking the correlation of their errors is the diagnostic to run first."
   }
  ]
 },
 {
  "path": "machine_learning/svm.html",
  "title": "Support Vector Machines",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “The Core Idea of SVM”?",
    "ans": "A Support Vector Machine (SVM) is a powerful supervised learning algorithm used for classification and regression. For classification, its primary goal is to find the optimal hyperplane that best separates data points of different classes in a high-dimensional space. The \"best\" hyperplane is the one that has the largest possible margin —the distance between the hyperplane and the nearest data point from either class."
   },
   {
    "t": "What does this module say about “Maximizing the Margin”?",
    "ans": "Why is a large margin so important? A larger margin implies a more confident and robust classification model. It means the decision boundary is as far as possible from the data points of both classes, making it less sensitive to small variations in the data and more likely to generalize well to new, unseen data."
   },
   {
    "t": "What does this module say about “What are Support Vectors”?",
    "ans": "The data points that lie exactly on the margin boundaries are called Support Vectors . These are the most critical data points in the dataset because they alone \"support\" or define the position and orientation of the optimal hyperplane."
   }
  ]
 },
 {
  "path": "machine_learning/threshold_tuning.html",
  "title": "Threshold Tuning",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Where does the 0.5 default threshold come from?",
    "o": [
     "It is derived from the training data",
     "It is the library's default, optimal only when classes are balanced and both errors cost the same",
     "It maximises accuracy on any dataset",
     "It is the median predicted probability"
    ],
    "a": 1,
    "w": "A default has to be something. Change the balance or the relative cost of the two mistakes and 0.5 stops being the right cut."
   },
   {
    "t": "If a miss costs ten times a false alarm, roughly what threshold does the cost formula give?",
    "o": [
     "0.5",
     "About 0.09",
     "0.9",
     "It depends only on the model"
    ],
    "a": 1,
    "w": "cost_FP / (cost_FP + cost_FN) = 1/11, about 0.09. The default of 0.5 would be about five times too strict for that problem."
   },
   {
    "t": "How does threshold tuning differ from calibration?",
    "o": [
     "They are the same thing",
     "Tuning picks a cut on the scores as given; calibration changes the scores so 0.8 really means 80%",
     "Calibration only applies to trees",
     "Tuning requires the test set"
    ],
    "a": 1,
    "w": "They are independent. A badly calibrated model can rank perfectly and a tuned threshold still works - but deriving the threshold from the cost formula needs p to be a real probability."
   }
  ]
 },
 {
  "path": "machine_learning/train_test_split.html",
  "title": "Train-Test Split Method",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why hold back a test set at all?",
    "o": [
     "To speed up training",
     "To estimate how the model does on data it has never seen",
     "Because algorithms require it",
     "To reduce the size of the training data"
    ],
    "a": 1,
    "w": "Training accuracy measures memorisation as much as learning. The only honest estimate of future performance comes from data the model has never been fitted on."
   },
   {
    "t": "You scale your features using statistics from the whole dataset, then split. What have you done?",
    "o": [
     "Nothing wrong - scaling is not learning",
     "Leaked information from the test set into training",
     "Made the model train more slowly",
     "Guaranteed overfitting"
    ],
    "a": 1,
    "w": "The scaler saw the test set's mean and range, so the test score is no longer clean. Fit the scaler on the training split only, then apply it to the test split."
   },
   {
    "t": "Your test set is tiny - say 20 rows. What is the main problem?",
    "o": [
     "Training will be slow",
     "The score is so noisy that it barely constrains anything",
     "The model cannot converge",
     "There is no problem"
    ],
    "a": 1,
    "w": "With 20 rows, one extra mistake moves accuracy by five whole percentage points. The estimate has such wide error bars that it cannot distinguish a good model from a mediocre one."
   }
  ]
 },
 {
  "path": "machine_learning/training_on_label_imbalanced_dataset.html",
  "title": "Training on Imbalanced Dataset",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Why imbalance breaks training”?",
    "ans": "Standard training minimises average loss over the dataset. When one class holds 99% of the rows, that average is dominated by it: predicting the majority everywhere already achieves very low loss, so there is little gradient pressure to learn the minority class at all."
   },
   {
    "t": "What does this module say about “The three families of fix”?",
    "ans": "Resample the data. Oversampling duplicates minority rows — simple, and risks overfitting to the few examples you have. SMOTE improves on it by synthesising new minority points along the lines between existing neighbours rather than copying. Undersampling discards majority rows, which balances the classes and throws away real information; it is reasonable when the majority class is genuinely enormous."
   },
   {
    "t": "What does this module say about “Start by changing nothing about the data”?",
    "ans": "The instinct on seeing an imbalanced dataset is to resample it immediately. That is usually the third-best move. Two cheaper things come first, and often one of them is enough."
   }
  ]
 },
 {
  "path": "machine_learning/tsne_and_umap.html",
  "title": "t-SNE and UMAP beside PCA",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Why can you not read the distance between two clusters in a t-SNE plot?",
    "o": [
     "The axes are unlabelled",
     "The layout only optimises for keeping near neighbours near; nothing constrains the gaps between groups",
     "The plot is rotated arbitrarily",
     "Distances are logarithmic"
    ],
    "a": 1,
    "w": "Two clusters at opposite ends of the plot may be more similar than two adjacent ones. PCA, being a linear projection, does preserve global distances."
   },
   {
    "t": "What can UMAP do that t-SNE cannot?",
    "o": [
     "Preserve local structure",
     "Transform data it did not see during fitting",
     "Run deterministically",
     "Handle more than three dimensions"
    ],
    "a": 1,
    "w": "t-SNE has no mapping from the original space to the layout, so adding a point means re-running everything. This matters when the embedding is part of a pipeline."
   },
   {
    "t": "Why is PCA the safer choice for dimensionality reduction inside a pipeline?",
    "o": [
     "It separates clusters better",
     "It is a stable, invertible linear mapping that applies to new data, whereas t-SNE coordinates have no meaning outside the plot",
     "It is stochastic",
     "It preserves cluster density"
    ],
    "a": 1,
    "w": "t-SNE and UMAP are visualisation tools. They answer 'does my data separate at all' well, and make poor preprocessing steps."
   }
  ]
 },
 {
  "path": "maths/matrix_as_transformation.html",
  "title": "A Matrix is a Transformation",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Most people first meet a matrix as a grid of numbers with rules for multiplying it. The rules work, but they explain nothing, and matrix multiplication in particular looks arbitrary — why rows against columns, and why in that order?"
   },
   {
    "t": "What does this module say about “The columns are the whole story”?",
    "ans": "Start with the two basis vectors: î = (1, 0) pointing along x, and ĵ = (0, 1) pointing along y. Every vector is built from them — (3, 2) means \"3 of î plus 2 of ĵ\"."
   },
   {
    "t": "What does this module say about “Why matrix-vector multiplication looks like that”?",
    "ans": "Now the formula stops being arbitrary. To transform (x, y), take x copies of where î went and y copies of where ĵ went, and add:"
   }
  ]
 },
 {
  "path": "maths/basis_span_and_orthogonality.html",
  "title": "Basis, Span and Orthogonality",
  "cat": "Maths",
  "q": [
   {
    "t": "Two vectors in the plane have determinant zero. What do they span?",
    "o": [
     "The whole plane",
     "A line through the origin",
     "A single point",
     "Nothing"
    ],
    "a": 1,
    "w": "The parallelogram has collapsed, so one vector is a multiple of the other and adds no new direction. Every combination lands on one line."
   },
   {
    "t": "What does an orthonormal basis buy you?",
    "o": [
     "A larger span",
     "The matrix of those vectors has its transpose as its inverse",
     "A non-zero determinant",
     "Fewer vectors are needed"
    ],
    "a": 1,
    "w": "Undoing the transformation becomes free, which is why orthonormal bases turn up wherever numerical stability matters."
   },
   {
    "t": "Why is a determinant of 0.001 a problem even though it is not zero?",
    "o": [
     "It makes the span smaller",
     "The basis is nearly dependent, so anything computed in it is numerically unstable",
     "It cannot be inverted",
     "It means the vectors are orthogonal"
    ],
    "a": 1,
    "w": "Exact zero is easy to catch. Nearly zero is the same problem in disguise, and the condition number is how it is measured."
   }
  ]
 },
 {
  "path": "maths/bayes_theorem.html",
  "title": "Bayes' Theorem",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “What this is”?",
    "ans": "Bayes' theorem takes a prior belief and revises it in light of new evidence. It is the mathematics of changing your mind correctly."
   },
   {
    "t": "What does this module say about “Count People, Not Percentages”?",
    "ans": "The grid shows 10,000 people, one square each. With a 1% base rate and a 99% accurate test:"
   },
   {
    "t": "What does this module say about “The Base Rate Dominates”?",
    "ans": "Drag the base rate slider from 0.1% upward and watch the answer climb. The test never changed — only how common the condition is. This is why:"
   }
  ]
 },
 {
  "path": "maths/bernoulli_binomial_poisson.html",
  "title": "Bernoulli, Binomial and Poisson",
  "cat": "Maths",
  "q": [
   {
    "t": "Why is a Bernoulli variance largest at p = 0.5?",
    "o": [
     "Because the mean is largest there",
     "An event that always or never happens is not random, so spread must fall to zero at either end",
     "Because the distribution is symmetric there",
     "It is not - variance is constant"
    ],
    "a": 1,
    "w": "p(1-p) peaks at 0.5 and collapses at both extremes, which is the arithmetic saying something obvious about certainty."
   },
   {
    "t": "What survives when a binomial becomes a Poisson?",
    "o": [
     "n only",
     "p only",
     "Their product np",
     "Neither"
    ],
    "a": 2,
    "w": "n grows and p shrinks with np fixed, and only lambda = np appears in the result. That is what makes Poisson usable when you know the rate but not the number of opportunities."
   },
   {
    "t": "Your count data has mean 4 and variance 12. What does that suggest?",
    "o": [
     "A Poisson fits well",
     "Overdispersion - events are clustering, violating the constant-rate assumption",
     "The mean is miscalculated",
     "The window is too small"
    ],
    "a": 1,
    "w": "A Poisson forces mean and variance to be equal. Variance well above the mean is a finding: something is varying that the model treats as fixed. A negative binomial adds that second parameter."
   }
  ]
 },
 {
  "path": "maths/cholesky_and_positive_definiteness.html",
  "title": "Cholesky and Positive-Definiteness",
  "cat": "Maths",
  "q": [
   {
    "t": "When does a Cholesky factorisation exist?",
    "o": [
     "For every square matrix",
     "For a symmetric matrix with every eigenvalue strictly positive",
     "For every symmetric matrix",
     "For every invertible matrix"
    ],
    "a": 1,
    "w": "Positive definite means x'Cx > 0 for all non-zero x. For a covariance matrix that quantity is a variance, so a matrix failing the test describes no distribution that exists."
   },
   {
    "t": "How do you generate samples with a given covariance C?",
    "o": [
     "Multiply independent standard normals by L, where C = LL'",
     "Multiply them by C",
     "Add C to independent normals",
     "Take the eigenvalues of C"
    ],
    "a": 0,
    "w": "Cov(Lz) = L I L' = LL' = C. It underlies Monte Carlo simulation of correlated risk, multivariate normal sampling, and the VAE reparameterisation trick."
   },
   {
    "t": "Why is attempting a Cholesky the standard positive-definiteness test?",
    "o": [
     "It is the only test",
     "It costs about a third of n^3 - far cheaper than computing eigenvalues - and fails exactly when the property does not hold",
     "It works on non-symmetric matrices",
     "It never fails"
    ],
    "a": 1,
    "w": "About half of an LU and roughly a tenth of an eigendecomposition. Routines that need the answer attempt the factorisation and watch for the negative square root."
   }
  ]
 },
 {
  "path": "maths/combinatorics.html",
  "title": "Combinatorics: Permutations and Combinations",
  "cat": "Maths",
  "q": [
   {
    "t": "What separates a permutation count from a combination count?",
    "o": [
     "A factor of n",
     "A factor of k! - the number of orders each selection could arrive in",
     "A factor of (n-k)!",
     "Nothing; they are the same"
    ],
    "a": 1,
    "w": "At n = 12, k = 5 the ordered count is 95,040 and the unordered is 792, and the ratio is exactly 120 = 5!."
   },
   {
    "t": "Why is C(n, k) symmetric in k?",
    "o": [
     "Because factorials are symmetric",
     "Choosing which k to keep is the same act as choosing which n-k to leave",
     "Because the distribution is normal",
     "It is not symmetric"
    ],
    "a": 1,
    "w": "The same partition of the set, described from either side - which is why the bars mirror around the middle."
   },
   {
    "t": "Why should you not compute C(n, k) from factorials directly?",
    "o": [
     "The formula is wrong",
     "21! overflows a 64-bit integer, while C(n, k) is usually far smaller than the factorials defining it",
     "It is slower",
     "It only works for small k"
    ],
    "a": 1,
    "w": "Work in logarithms or use the multiplicative recurrence. Pascal's identity C(n,k) = C(n-1,k-1) + C(n-1,k) is the standard dynamic-programming route."
   }
  ]
 },
 {
  "path": "maths/conditional_probability.html",
  "title": "Conditional Probability",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Conditioning on B does not change the outcomes, it discards the ones where B did not happen, so P(A | B) is simply the count of outcomes in both events divided by the count in B. Independence is the special case where that shrinking leaves A's share unchanged, which is exactly when P(A and B) = P(A)P(B) is valid and not before."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Probability counts favourable outcomes against all possible outcomes. Conditional probability changes one thing: it shrinks what counts as possible. P(A | B) is read \"the probability of A given B\". The bar does not mean division and it does not mean \"and\". It means: assume B happened, throw away every outcome where it did not, and ask about A within what remains."
   },
   {
    "t": "What does this module say about “Probability, once you know something”?",
    "ans": "Conditional probability is the probability of one event given that another has happened."
   }
  ]
 },
 {
  "path": "maths/confidence_intervals.html",
  "title": "Confidence Intervals",
  "cat": "Maths",
  "q": [
   {
    "t": "What does the 95% in a 95% confidence interval describe?",
    "o": [
     "The probability the parameter is in your interval",
     "How often the procedure produces intervals that contain the parameter",
     "The proportion of data inside the interval",
     "The confidence of the analyst"
    ],
    "a": 1,
    "w": "The parameter is fixed - it is inside or it is not. What is random is the interval, because it is computed from a random sample."
   },
   {
    "t": "Why does a nominal 95% interval cover only about 89% at n = 5 here?",
    "o": [
     "The random number generator is biased",
     "It uses a z value with an estimated SD, which is unreliable at small n - the problem the t-distribution fixes",
     "The population is not normal",
     "1000 draws is not enough"
    ],
    "a": 1,
    "w": "The correction is large at small n and negligible past about 30. Dragging n upward closes the gap on its own."
   },
   {
    "t": "Two 95% intervals overlap. What follows?",
    "o": [
     "The difference is not significant",
     "Nothing directly - a test of the difference can still be significant",
     "The samples are the same size",
     "Both contain the true mean"
    ],
    "a": 1,
    "w": "Overlap of separate intervals is not a test of their difference. Test the difference directly rather than eyeballing the bars."
   }
  ]
 },
 {
  "path": "maths/convexity_and_optimisation.html",
  "title": "Convexity and Optimisation Landscapes",
  "cat": "Maths",
  "q": [
   {
    "t": "What is the defining consequence of convexity for optimisation?",
    "o": [
     "The gradient is always positive",
     "Every local minimum is the global minimum",
     "The function has one input",
     "Gradient descent converges in one step"
    ],
    "a": 1,
    "w": "Find a stationary point with positive curvature and you are done, with a proof. That is why linear and logistic regression are so well behaved."
   },
   {
    "t": "Why are saddle points more common than local minima in high dimensions?",
    "o": [
     "Gradients are larger there",
     "A local minimum needs every Hessian eigenvalue positive, which is vanishingly unlikely across millions of dimensions",
     "Saddle points attract gradient descent",
     "Local minima require convexity"
    ],
    "a": 1,
    "w": "Almost every stationary point has some negative direction, making it escapable - and mini-batch noise helps find that direction."
   },
   {
    "t": "Descent diverges on a perfectly convex bowl. What is the likely cause?",
    "o": [
     "The function is secretly non-convex",
     "The learning rate is too large for the curvature",
     "The starting point is wrong",
     "There are several minima"
    ],
    "a": 1,
    "w": "Convexity guarantees a unique minimum exists; it says nothing about whether your step size will find it. The safe step depends on curvature."
   }
  ]
 },
 {
  "path": "maths/covariance_and_correlation.html",
  "title": "Covariance and Correlation",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Variance describes how one variable spreads out. Covariance is the same idea for two: when x is above its mean, is y usually above its mean too? Correlation is covariance with the units removed. That single change is what makes it comparable across datasets — and, as we will see, still leaves it blind to anything that is not a straight line."
   },
   {
    "t": "What does this module say about “Why correlation exists”?",
    "ans": "Covariance has a fatal flaw for reporting: it carries the units of both variables multiplied together. Measure height in metres and weight in kilograms and you get one number; switch height to centimetres and the same data gives a number a hundred times larger. Nothing about the relationship changed."
   },
   {
    "t": "What does this module say about “Correlation matrices, and multicollinearity”?",
    "ans": "With several features, the correlation matrix shows every pair at once, and it is one of the first things worth plotting on a new dataset."
   }
  ]
 },
 {
  "path": "maths/cross_entropy_and_kl_divergence.html",
  "title": "Cross-Entropy and KL Divergence",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Entropy is the average surprise of a distribution — the shortest average code length you could achieve if you knew the true probabilities. Cross-entropy asks a harsher question: what does it cost if you build your code for q and the data actually comes from p? The answer is always at least H(p), and the excess is the KL divergence."
   },
   {
    "t": "What does this module say about “Entropy, cross-entropy and KL, in one relationship”?",
    "ans": "Three quantities that are constantly confused, and one equation that separates them:"
   },
   {
    "t": "What does this module say about “Things to try”?",
    "ans": "For a single labelled example, p is one-hot: probability 1 on the true class and 0 elsewhere. Every term of the cross-entropy sum vanishes except one, leaving"
   }
  ]
 },
 {
  "path": "maths/derivatives_and_slope.html",
  "title": "Derivatives and Slope",
  "cat": "Maths",
  "q": [
   {
    "t": "The derivative of a function at a point tells you:",
    "o": [
     "The value of the function there",
     "The slope of the tangent line there",
     "The area under the curve up to there",
     "Whether the function is positive"
    ],
    "a": 1,
    "w": "A derivative is an instantaneous rate of change - the slope of the curve at that exact point, which is the tangent line's slope."
   },
   {
    "t": "At a minimum of a smooth curve, the derivative is:",
    "o": [
     "As large as possible",
     "Zero",
     "Negative",
     "Undefined"
    ],
    "a": 1,
    "w": "The curve is momentarily flat at the bottom. This is exactly what gradient descent chases: it keeps stepping until the gradient is near zero and there is no downhill direction left."
   },
   {
    "t": "Gradient descent subtracts the gradient rather than adding it. Why?",
    "o": [
     "To keep the numbers small",
     "Because the gradient points uphill, and the goal is to go down",
     "Because loss is always negative",
     "To avoid dividing by zero"
    ],
    "a": 1,
    "w": "The gradient points in the direction of steepest increase. To reduce the loss you move against it - which is the minus sign in every update rule you will ever see."
   }
  ]
 },
 {
  "path": "maths/determinant.html",
  "title": "Determinant",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The determinant is the signed area factor of a transformation: ad − bc is the area of the parallelogram the unit square becomes, its magnitude says how much every region is scaled, and its sign says whether the plane was flipped over."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A matrix is a transformation of space, and the determinant measures one thing about it: how much it scales area. A determinant of 3 means every region comes out three times as large; 0.5 means everything shrinks by half; 1 means area is untouched, however much the shape has been rotated or sheared."
   },
   {
    "t": "What does this module say about “What zero means”?",
    "ans": "If the determinant is zero, the parallelogram has no area: the two columns lie on the same line, and the whole plane has been squashed onto that line. Everything that goes wrong with a singular matrix follows from this one picture."
   }
  ]
 },
 {
  "path": "maths/distance_metrics.html",
  "title": "Distance Metrics",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Euclidean, Manhattan and Chebyshev are the L2, L1 and L∞ norms of the difference between two points, always ordered Chebyshev ≤ Euclidean ≤ Manhattan and agreeing only when a single coordinate differs; their equal-distance rings are a circle, a diamond and a square, which is what makes them disagree."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A surprising number of algorithms do nothing but compare distances. KNN finds the nearest points, k-means assigns each point to the nearest centre, hierarchical clustering merges the closest pair, and a vector database retrieves the closest embeddings."
   },
   {
    "t": "What does this module say about “Several ways to measure \"far apart\"”?",
    "ans": "Distance is the foundation of clustering, nearest-neighbour methods, anomaly detection and most retrieval systems — and there is more than one sensible definition."
   }
  ]
 },
 {
  "path": "maths/eigenvalues_and_eigenvectors.html",
  "title": "Eigenvalues and Eigenvectors",
  "cat": "Maths",
  "q": [
   {
    "t": "What is meant by “Scale before decomposing” here?",
    "ans": "Eigenvalues of a covariance matrix depend on units, so an unscaled column with a large range dominates the first component."
   },
   {
    "t": "What is meant by “Signs are arbitrary” here?",
    "ans": "An eigenvector and its negation describe the same direction; do not read meaning into which one a library returns."
   },
   {
    "t": "What is meant by “Order is not guaranteed” here?",
    "ans": "by np.linalg.eig . Sort explicitly, or use eigh for symmetric matrices."
   },
   {
    "t": "What is meant by “Repeated eigenvalues” here?",
    "ans": "mean the corresponding eigenvectors are not unique — any rotation within that subspace works, so individual component directions become meaningless."
   }
  ]
 },
 {
  "path": "maths/entropy_and_information.html",
  "title": "Entropy and Information",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Suppose I am about to tell you the outcome of an event, and you want to know how much you are about to learn. If the event is a coin flip, you will learn something. If it is \"will the sun rise tomorrow\", you will learn essentially nothing, because you already knew."
   },
   {
    "t": "What does this module say about “Surprise first”?",
    "ans": "Start with a single outcome. How surprising is it? Two things should be true: a certain outcome (p = 1) should carry zero surprise, and rarer outcomes should be more surprising. One function does this cleanly:"
   },
   {
    "t": "What does this module say about “Entropy is average surprise”?",
    "ans": "Now take the whole distribution and average the surprise, weighting each outcome by how often it actually occurs:"
   }
  ]
 },
 {
  "path": "maths/equation_of_line.html",
  "title": "Equation of a Line (y = mx + c)",
  "cat": "Maths",
  "q": [
   {
    "t": "In y = mx + c, what does c control?",
    "o": [
     "How steep the line is",
     "Where the line crosses the y-axis",
     "How long the line is",
     "Whether the line is straight"
    ],
    "a": 1,
    "w": "c is the intercept: it slides the whole line up and down without rotating it. m is the slope, and it is the only term that changes the steepness."
   },
   {
    "t": "A line has slope m = 0. What does it look like?",
    "o": [
     "Vertical",
     "Horizontal",
     "At 45 degrees",
     "It does not exist"
    ],
    "a": 1,
    "w": "Slope is rise over run. A zero rise for any run is a flat, horizontal line. A vertical line is the case with no defined slope at all, because the run is zero and you cannot divide by it."
   },
   {
    "t": "Why does this one equation matter so much later on?",
    "o": [
     "It is the simplest thing to plot",
     "A neuron computes exactly this shape - weights are slopes and the bias is an intercept",
     "Every dataset is a straight line",
     "It is required for calculus"
    ],
    "a": 1,
    "w": "w·x + b is y = mx + c with more inputs. Weights play the role of slopes and the bias plays the role of the intercept, which is why a perceptron can only ever draw a straight boundary."
   }
  ]
 },
 {
  "path": "maths/expectation_and_variance.html",
  "title": "Expectation and Variance",
  "cat": "Maths",
  "q": [
   {
    "t": "A fair die has E[X] = 3.5. What does that tell you?",
    "o": [
     "3.5 is the most likely roll",
     "It is the balance point of the distribution, and need not be attainable",
     "Half the rolls are below 3.5",
     "The variance is 3.5"
    ],
    "a": 1,
    "w": "No die has ever rolled a 3.5. The expectation is where the distribution would balance on a pin, not a prediction of any single outcome."
   },
   {
    "t": "When does Var(X + Y) = Var(X) + Var(Y)?",
    "o": [
     "Always",
     "Only when X and Y are independent",
     "Only when both are normal",
     "Only when the means are equal"
    ],
    "a": 1,
    "w": "Expectation adds unconditionally; variance does not. Otherwise a covariance term appears - which is why diversification and bagging both depend on decorrelation."
   },
   {
    "t": "Why is Var(X) = E[X^2] - (E[X])^2 numerically dangerous?",
    "o": [
     "It needs two passes over the data",
     "With large values and small variance the two terms nearly cancel, destroying precision",
     "It can return a negative number in exact arithmetic",
     "It assumes independence"
    ],
    "a": 1,
    "w": "It is the one-pass formula, and the subtraction of two nearly equal large numbers is what Welford's algorithm exists to avoid."
   }
  ]
 },
 {
  "path": "maths/exponentials.html",
  "title": "Exponentials",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Before the details”?",
    "ans": "In y = b^x the variable sits in the exponent . Each step of 1 in x multiplies y by b, rather than adding to it. That single difference is what separates exponential from linear behaviour."
   },
   {
    "t": "What does this module say about “Exponential Always Wins Eventually”?",
    "ans": "Keep the polynomial comparison on and look at the left of the plot: x³ is far ahead. Now slide x rightward. There is a crossover point, and after it 2^x leaves x³ hopelessly behind."
   },
   {
    "t": "What does this module say about “Doubling Time and Half-Life”?",
    "ans": "A defining feature of exponentials: the time to double is constant . It takes just as long to go from 1 to 2 as from a million to two million. The panel computes this live — at base 2 it is exactly 1 step, at base 1.1 about 7.3 steps."
   }
  ]
 },
 {
  "path": "maths/hypothesis_testing_and_p_values.html",
  "title": "Hypothesis Testing and p-values",
  "cat": "Maths",
  "q": [
   {
    "t": "A p-value is the probability of:",
    "o": [
     "The null hypothesis being true",
     "A result at least this extreme, assuming the null is true",
     "The alternative hypothesis being true",
     "Making a Type I error"
    ],
    "a": 1,
    "w": "It is computed assuming the null, so it cannot tell you how likely that assumption was. Going the other way needs Bayes' theorem and a prior."
   },
   {
    "t": "A study reports p = 0.4. What can you conclude?",
    "o": [
     "The null hypothesis is true",
     "The data is consistent with the null - which is also what an underpowered study looks like",
     "There is no effect",
     "The sample was too large"
    ],
    "a": 1,
    "w": "A large p-value is produced both by a real absence of effect and by a study too small to detect one. Distinguishing them requires power."
   },
   {
    "t": "Why must the choice of one or two tails be made before seeing the data?",
    "o": [
     "It changes the test statistic",
     "Choosing afterwards halves the p-value for free, which is cheating rather than a modelling choice",
     "Two-tailed tests need more data",
     "The null hypothesis changes"
    ],
    "a": 1,
    "w": "The two-tailed p-value is exactly double the one-tailed one for the same statistic, so the decision has to precede the observation."
   }
  ]
 },
 {
  "path": "maths/identity_inverse_transpose.html",
  "title": "Identity, Inverse and Transpose",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The identity is the matrix that changes nothing, and the inverse is the one that undoes A — defined by A A⁻¹ = I and computed by dividing through by the determinant, which is precisely why a zero determinant means no inverse exists: the transformation destroyed information and no matrix can recover it."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A matrix is a transformation . Once you can do something to space, three questions follow immediately: what does nothing, what puts it back, and what happens if you read the matrix sideways."
   },
   {
    "t": "What does this module say about “Three operations that keep appearing”?",
    "ans": "The identity matrix I has ones on the diagonal and zeros elsewhere. Multiplying by it changes nothing:"
   }
  ]
 },
 {
  "path": "maths/information_gain.html",
  "title": "Information Gain",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Entropy measures how mixed a set of labels is: 1 bit for an even fifty-fifty split of two classes, 0 bits when every label is the same. Information gain is simply how much that number falls when you split the set in two. A decision tree does nothing cleverer than this. At every node it tries every feature and every threshold, computes the gain for each, and keeps the winner."
   },
   {
    "t": "What does this module say about “How much did that question help”?",
    "ans": "Information gain measures how much a split reduces uncertainty. It is the difference between the entropy before a question is asked and the average entropy afterwards."
   },
   {
    "t": "What does this module say about “How a tree uses it”?",
    "ans": "At every node the algorithm loops over every feature and, for numeric features, every candidate threshold. For each candidate it computes the information gain, and it keeps the best. Then it repeats on each child."
   }
  ]
 },
 {
  "path": "maths/jensens_inequality.html",
  "title": "Jensen's Inequality",
  "cat": "Maths",
  "q": [
   {
    "t": "For a convex f, which is larger?",
    "o": [
     "f(E[X])",
     "E[f(X)]",
     "They are equal",
     "It depends on the distribution"
    ],
    "a": 1,
    "w": "Convex means the chord lies above the curve, so the average of the heights sits above the height at the average. Concave reverses it."
   },
   {
    "t": "When is the gap exactly zero?",
    "o": [
     "When X is normal",
     "When f is linear, or X is constant",
     "When the variance is small",
     "Never"
    ],
    "a": 1,
    "w": "Flatten the curve to a line and the chord lies on it; shrink the distribution to a point and the two dots merge. Nothing else gives equality."
   },
   {
    "t": "How does Jensen make variational inference possible?",
    "o": [
     "It bounds the variance",
     "It turns log of an expectation into a tractable lower bound - the ELBO - that decomposes and can be maximised",
     "It proves convergence of EM",
     "It removes the latent variables"
    ],
    "a": 1,
    "w": "log sum_z p(x,z) cannot be optimised directly. Jensen on the concave log gives a bound that does decompose, and maximising it cannot decrease the true objective."
   }
  ]
 },
 {
  "path": "maths/lagrange_multipliers.html",
  "title": "Lagrange Multipliers",
  "cat": "Maths",
  "q": [
   {
    "t": "At a constrained optimum, what is true of the level line and the constraint?",
    "o": [
     "They cross at right angles",
     "They are tangent",
     "The level line is horizontal",
     "The gradient is zero"
    ],
    "a": 1,
    "w": "If they crossed you could slide along the constraint onto a better level line. Tangency means the gradients are parallel, which is the condition."
   },
   {
    "t": "What does the multiplier lambda measure?",
    "o": [
     "The size of the constraint",
     "How much the optimal value improves per unit of loosened constraint",
     "The distance to the optimum",
     "The curvature of the objective"
    ],
    "a": 1,
    "w": "The shadow price. In economics it is literally what an extra unit of capacity is worth; in ridge regression it is the regularisation strength."
   },
   {
    "t": "Why are SVMs sparse?",
    "o": [
     "The kernel is sparse",
     "Complementary slackness makes the multiplier zero for every point whose constraint is slack",
     "Only a few points are stored",
     "The objective is convex"
    ],
    "a": 1,
    "w": "Points comfortably on the correct side contribute nothing to the solution. Only the ones pressed against the margin have non-zero multipliers - those are the support vectors."
   }
  ]
 },
 {
  "path": "maths/logarithms.html",
  "title": "Logarithms",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A log is an exponent in disguise. It converts products into sums, compresses vast ranges into readable ones, and is undefined at zero — three facts that between them explain log-likelihood, cross-entropy loss, entropy in bits, and most NaN bugs in training code."
   },
   {
    "t": "What does this module say about “The Property That Matters Most”?",
    "ans": "A logarithm converts multiplication into addition . Change the two numbers in the product demo and watch both sides stay equal. This is not a curiosity — it is why logs are everywhere in machine learning."
   },
   {
    "t": "What does this module say about “The Three Bases You Will Meet”?",
    "ans": "The base only rescales the curve — every log is a constant multiple of every other. Watch the three readouts stay in fixed proportion as you slide x."
   }
  ]
 },
 {
  "path": "maths/markov_chains.html",
  "title": "Markov Chains",
  "cat": "Maths",
  "q": [
   {
    "t": "What does the Markov property say?",
    "o": [
     "Every state is equally likely",
     "The next state depends only on the current one, not on the path that led there",
     "The chain always converges",
     "Transitions are symmetric"
    ],
    "a": 1,
    "w": "The present screens off the past, so you carry one thing - where you are - instead of a history of arbitrary length."
   },
   {
    "t": "What is the stationary distribution?",
    "o": [
     "The starting distribution",
     "The pi satisfying pi P = pi - the left eigenvector of P with eigenvalue 1",
     "The most likely state",
     "The uniform distribution"
    ],
    "a": 1,
    "w": "It is where the chain settles regardless of where it started, provided the chain is irreducible and aperiodic."
   },
   {
    "t": "What does MCMC do with this idea?",
    "o": [
     "Runs it forwards to predict states",
     "Constructs a chain whose stationary distribution is the posterior it wants, then treats the visited states as samples",
     "Estimates the transition matrix from data",
     "Finds the second-largest eigenvalue"
    ],
    "a": 1,
    "w": "Nearly all Bayesian computation is this, which is also why burn-in and convergence diagnostics matter: early samples reflect the starting point, not the target."
   }
  ]
 },
 {
  "path": "maths/matrix_calculus.html",
  "title": "Matrix Calculus",
  "cat": "Maths",
  "q": [
   {
    "t": "What shape is the gradient of a scalar loss with respect to a 784x128 weight matrix?",
    "o": [
     "128x784",
     "784x128",
     "A scalar",
     "784x1"
    ],
    "a": 1,
    "w": "The same shape as the thing differentiated by - which is why W -= lr * dW type-checks, and the fastest way to catch a wrong derivation."
   },
   {
    "t": "What is d(x'Ax)/dx?",
    "o": [
     "Ax",
     "(A + A')x",
     "2A",
     "A'x"
    ],
    "a": 1,
    "w": "Both copies of x contribute. The familiar 2Ax is the special case where A is symmetric, which is why it works for A'A in least squares."
   },
   {
    "t": "For a linear layer y = Wx, what is dL/dW?",
    "o": [
     "W' times dL/dy",
     "The outer product (dL/dy) x'",
     "dL/dy",
     "x times dL/dy"
    ],
    "a": 1,
    "w": "An m-long upstream gradient times an n-long input gives an m-by-n outer product - exactly W's shape. The shape rule confirms it immediately."
   }
  ]
 },
 {
  "path": "maths/matrix_multiplication.html",
  "title": "Matrix Multiplication",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “The problem it solves”?",
    "ans": "Multiplying two matrices produces a new matrix in which every single entry is a dot product — one row of the left matrix against one column of the right. Nothing more complicated is happening."
   },
   {
    "t": "What does this module say about “The Rule for a Single Cell”?",
    "ans": "Click any cell in C and the app highlights the blue row and amber column that feed it, then writes out the arithmetic term by term. Every cell is independent of every other — which is precisely why this operation parallelises so well on a GPU."
   },
   {
    "t": "What does this module say about “Order Matters”?",
    "ans": "Matrix multiplication is not commutative : AB ≠ BA in general. Often BA is not even a legal operation — a (2×3) times a (3×4) works, but (3×4) times (2×3) does not. When people say the order of layers matters, this is the literal reason."
   }
  ]
 },
 {
  "path": "maths/maximum_likelihood_estimation.html",
  "title": "Maximum Likelihood Estimation",
  "cat": "Maths",
  "q": [
   {
    "t": "What is meant by “Consistent” here?",
    "ans": "With enough data, the estimate converges to the true parameter value."
   },
   {
    "t": "What is meant by “Asymptotically efficient” here?",
    "ans": "No other consistent estimator has smaller variance in the large-sample limit."
   },
   {
    "t": "What is meant by “Invariant” here?",
    "ans": "If θ-hat is the MLE of θ, then g(θ-hat) is the MLE of g(θ) — so you can estimate on whichever scale is convenient."
   }
  ]
 },
 {
  "path": "maths/mean_mode_and_median.html",
  "title": "Mean, Mode and Median",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The mean is the balance point and uses every value — which makes it precise but fragile. The median is the middle and shrugs off outliers. The mode is the most common and is the only option for categories. Skewed data pulls them apart, and \"average\" without qualification is an ambiguous word."
   },
   {
    "t": "What does this module say about “What this is”?",
    "ans": "All three are measures of central tendency — attempts to summarise a whole dataset with one number. They answer subtly different questions, and on skewed data they can be wildly far apart."
   },
   {
    "t": "What does this module say about “The Three Definitions”?",
    "ans": "On a perfectly symmetric distribution all three land in the same place. Load Symmetric and see the three markers stack up."
   }
  ]
 },
 {
  "path": "maths/mean_variance_standard_deviation.html",
  "title": "Mean, Variance and Standard Deviation",
  "cat": "Maths",
  "q": [
   {
    "t": "Every value in a dataset is increased by 10. What happens?",
    "o": [
     "The mean and the standard deviation both rise by 10",
     "The mean rises by 10, the standard deviation is unchanged",
     "Neither changes",
     "The standard deviation rises, the mean does not"
    ],
    "a": 1,
    "w": "Shifting everything moves the centre but not the spread. The distances between points are identical, and spread is all the standard deviation measures."
   },
   {
    "t": "Why is standard deviation usually quoted rather than variance?",
    "o": [
     "It is easier to compute",
     "It is in the same units as the data, so it is directly readable",
     "Variance can be negative",
     "Variance only works for large samples"
    ],
    "a": 1,
    "w": "Variance is in squared units - 'seconds squared' means nothing to a reader. Taking the square root returns it to the original units so it can be compared against the mean."
   },
   {
    "t": "A single extreme outlier is added to a dataset. Which is affected more?",
    "o": [
     "The mean",
     "The variance",
     "Both equally",
     "Neither"
    ],
    "a": 1,
    "w": "Variance squares each distance from the mean, so a far-away point contributes enormously. The mean moves too, but only linearly - this squaring is why variance-based methods are fragile to outliers."
   }
  ]
 },
 {
  "path": "maths/partial_derivatives_and_gradient.html",
  "title": "Partial Derivatives and the Gradient",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Start here”?",
    "ans": "Standing on a hillside, \"how steep is it?\" has no single answer — it depends which way you face. A partial derivative answers it for one fixed direction; the gradient bundles those answers into a vector pointing straight up the slope."
   },
   {
    "t": "What does this module say about “Partials: Freeze Everything Else”?",
    "ans": "To compute ∂f/∂x you treat y as a constant and differentiate normally. That is the whole idea — you are asking how f changes if you step east while refusing to move north."
   },
   {
    "t": "What does this module say about “Gradient Descent: Just Walk Backwards”?",
    "ans": "Training a model means finding the lowest point of a loss surface. The gradient points uphill, so you step the other way:"
   }
  ]
 },
 {
  "path": "maths/probability_basics.html",
  "title": "Probability Basics",
  "cat": "Maths",
  "q": [
   {
    "t": "Two fair coin flips. What is the probability of two heads?",
    "o": [
     "1/2",
     "1/4",
     "1/3",
     "3/4"
    ],
    "a": 1,
    "w": "Independent events multiply: 1/2 x 1/2 = 1/4. The four equally likely outcomes are HH, HT, TH, TT, and only one of them qualifies."
   },
   {
    "t": "P(A|B) means:",
    "o": [
     "The probability of A and B both happening",
     "The probability of A, given that B has happened",
     "The probability of A or B",
     "The probability of B, given A"
    ],
    "a": 1,
    "w": "The bar is 'given'. Conditioning narrows the world to the cases where B is true and asks how often A holds within that smaller set. Swapping the two sides gives a different number - assuming otherwise is the base-rate fallacy."
   },
   {
    "t": "A test is 99% accurate for a disease affecting 1 in 10,000 people. You test positive. Roughly how worried should you be?",
    "o": [
     "99% likely to have it",
     "About 1% likely to have it",
     "50/50",
     "Certain to have it"
    ],
    "a": 1,
    "w": "Among 10,000 people there is about 1 true case and about 100 false positives, so a positive result is right roughly 1 time in 100. The base rate dominates, which is exactly what Bayes' rule formalises."
   }
  ]
 },
 {
  "path": "maths/projections.html",
  "title": "Projections",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Projection answers one question: of all the points on the line through a, which is closest to b? The answer is b's shadow, and the line from b down to that shadow is perpendicular. Those two facts — closest point, perpendicular error — are the same fact, and almost every fitting method in machine learning is built on it."
   },
   {
    "t": "What does this module say about “Casting a shadow onto a direction”?",
    "ans": "A projection answers: how much of vector a lies along the direction of vector b ? Picture the sun directly overhead of b and a casting a shadow onto it."
   },
   {
    "t": "What does this module say about “Least squares is a projection”?",
    "ans": "Linear regression fits a line by minimising squared residuals. Geometrically it is projecting."
   }
  ]
 },
 {
  "path": "maths/qr_decomposition.html",
  "title": "QR Decomposition and Gram-Schmidt",
  "cat": "Maths",
  "q": [
   {
    "t": "Why is R upper triangular?",
    "o": [
     "By convention",
     "The k-th original vector is built only from the first k orthonormal vectors, never a later one",
     "Because Q is orthogonal",
     "To make back-substitution possible"
    ],
    "a": 1,
    "w": "Nothing is ever built from a q that comes later, so everything below the diagonal is zero - which then makes back-substitution possible as a consequence."
   },
   {
    "t": "Why do least-squares solvers avoid the normal equations?",
    "o": [
     "They are slower",
     "Forming A'A squares the condition number, consuming most of the available precision",
     "They require a square matrix",
     "They cannot handle collinearity"
    ],
    "a": 1,
    "w": "A condition number of 10^6 becomes 10^12. QR gives Rx = Q'b, solved by back-substitution, with the conditioning never squared."
   },
   {
    "t": "What does modified Gram-Schmidt change?",
    "o": [
     "The resulting Q and R",
     "Nothing algebraically - it subtracts each projection immediately, which is far more stable in floating point",
     "The order of the input vectors",
     "It produces a square Q"
    ],
    "a": 1,
    "w": "Algebraically identical, numerically much better. Serious implementations use Householder reflections instead, which are stable regardless of input."
   }
  ]
 },
 {
  "path": "maths/quantiles_and_percentiles.html",
  "title": "Quantiles and Percentiles",
  "cat": "Maths",
  "q": [
   {
    "t": "Why is the median unaffected by adding one enormous value?",
    "o": [
     "It is recomputed from the mean",
     "It depends only on order, so a new extreme value is just 'one more above the middle'",
     "Outliers are removed first",
     "It uses the IQR"
    ],
    "a": 1,
    "w": "A mean is a balance point and moves when anything moves. That robustness is why median income is reported rather than mean income."
   },
   {
    "t": "What do the whiskers on a box plot reach?",
    "o": [
     "The minimum and maximum",
     "The furthest points within 1.5 times the IQR of the box",
     "Two standard deviations",
     "The 5th and 95th percentiles"
    ],
    "a": 1,
    "w": "The 1.5 is a Tukey convention, not a test. For a normal distribution it flags about 0.7% of points, and a skewed distribution produces them by construction."
   },
   {
    "t": "Why can you not average the p99 of two servers?",
    "o": [
     "The samples are different sizes",
     "Percentiles are not linear - aggregating them needs the underlying distributions",
     "p99 is not a percentile",
     "The servers are not independent"
    ],
    "a": 1,
    "w": "It is the commonest error in latency reporting and it always understates the tail. Structures like t-digest exist to aggregate quantiles properly."
   }
  ]
 },
 {
  "path": "maths/rank_and_linear_independence.html",
  "title": "Rank and Linear Independence",
  "cat": "Maths",
  "q": [
   {
    "t": "What is meant by “Image compression” here?",
    "ans": "A 1000×1000 image kept at rank 50 stores 5% of the numbers and often looks nearly identical, because natural images are dominated by a few strong directions."
   },
   {
    "t": "What is meant by “Recommender systems” here?",
    "ans": "A user-item ratings matrix is assumed to be approximately low rank — a few latent taste factors explain most preferences — and the missing entries are filled by reconstructing from those factors."
   },
   {
    "t": "What is meant by “Noise reduction” here?",
    "ans": "Signal usually lives in the strong directions and noise is spread across the weak ones, so truncating the small singular values cleans the data."
   },
   {
    "t": "What is meant by “LoRA fine-tuning” here?",
    "ans": "Large language models are adapted by learning a low-rank update to the weight matrices, training a tiny fraction of the parameters. The whole method is named after this property."
   }
  ]
 },
 {
  "path": "maths/sampling_distributions.html",
  "title": "Sampling Distributions and Standard Error",
  "cat": "Maths",
  "q": [
   {
    "t": "What is a sampling distribution?",
    "o": [
     "The distribution of the data in one sample",
     "The distribution of a statistic across all the samples you could have drawn",
     "The distribution of the population",
     "The distribution of the residuals"
    ],
    "a": 1,
    "w": "You only ever draw one sample, so you reason about what would happen across the samples you did not take. It is the object a confidence interval describes."
   },
   {
    "t": "Which shrinks as you collect more data?",
    "o": [
     "The standard deviation of the population",
     "The standard error of the estimate",
     "Both",
     "Neither"
    ],
    "a": 1,
    "w": "SD describes the data and is a property of the population. SE describes an estimate. If the number would change when you collect more data of the same kind, it is a standard error."
   },
   {
    "t": "Why do national polls settle around 1,000 respondents?",
    "o": [
     "It is a legal requirement",
     "The sqrt(n) curve flattens, so further precision costs four times the data and bias dominates anyway",
     "Larger samples become biased",
     "The central limit theorem requires it"
    ],
    "a": 1,
    "w": "Every halving of uncertainty costs four times the data. Past that point the remaining error is dominated by sampling bias, which more data cannot fix."
   }
  ]
 },
 {
  "path": "maths/singular_value_decomposition.html",
  "title": "Singular Value Decomposition",
  "cat": "Maths",
  "q": [
   {
    "t": "What shape does the unit circle become under any 2x2 matrix?",
    "o": [
     "Another circle",
     "An ellipse",
     "A parallelogram",
     "It depends on the matrix"
    ],
    "a": 1,
    "w": "Always an ellipse - that is what the SVD asserts. Rotate, stretch along the axes, rotate again, and stage 3 is an axis-aligned ellipse for every matrix."
   },
   {
    "t": "What does a large condition number tell you?",
    "o": [
     "The matrix is large",
     "The matrix nearly flattens some direction, so solving with it amplifies error",
     "The determinant is negative",
     "The singular values are complex"
    ],
    "a": 1,
    "w": "It is the largest singular value over the smallest. Near 1 means all directions are treated alike; large means the ellipse is a sliver."
   },
   {
    "t": "Why is the SVD preferred over an eigendecomposition?",
    "o": [
     "It is faster",
     "It exists for every matrix of every shape, and its bases are orthonormal",
     "Its values can be complex",
     "It does not require centring"
    ],
    "a": 1,
    "w": "Eigendecomposition needs a square matrix and does not always exist even then; eigenvectors need not be perpendicular. Singular values are always real and non-negative."
   }
  ]
 },
 {
  "path": "maths/taylor_series.html",
  "title": "Taylor Series",
  "cat": "Maths",
  "q": [
   {
    "t": "What does the second term of a Taylor series give you?",
    "o": [
     "The value at the point",
     "The tangent line",
     "The curvature",
     "The radius of convergence"
    ],
    "a": 1,
    "w": "One term is a constant at the right height; two is the tangent; three is the quadratic that also has the right bend - which is what Newton's method optimises."
   },
   {
    "t": "Why does the series for 1/(1+x^2) stop improving beyond x = 1?",
    "o": [
     "The function is not smooth there",
     "It has complex poles at distance 1 from the origin, which sets the radius of convergence",
     "Floating point runs out of precision",
     "The derivatives become zero"
    ],
    "a": 1,
    "w": "The function is perfectly smooth on the real line. The radius is the distance to the nearest singularity wherever it sits, including off the real line."
   },
   {
    "t": "A Taylor series is a statement about:",
    "o": [
     "The whole function",
     "A neighbourhood of the expansion point",
     "The function's maximum",
     "Its integral"
    ],
    "a": 1,
    "w": "It is built entirely from derivatives at one point, so it cannot know anything about elsewhere. Move the expansion point and the region of agreement moves with it."
   }
  ]
 },
 {
  "path": "maths/central_limit_theorem.html",
  "title": "The Central Limit Theorem",
  "cat": "Maths",
  "q": [
   {
    "t": "What exactly becomes normal?",
    "o": [
     "The population",
     "The sample",
     "The distribution of the sample mean across repeated samples",
     "The variance"
    ],
    "a": 2,
    "w": "The sample looks like the population, because that is what it is drawn from. It is the mean that goes normal, and the population's shape does not appear in the statement."
   },
   {
    "t": "You want to halve your uncertainty about a mean. What must you do?",
    "o": [
     "Double the sample",
     "Quadruple the sample",
     "Halve the sample",
     "Nothing - it is fixed by the population"
    ],
    "a": 1,
    "w": "The standard error is sigma over root n. That square root is why precision gets expensive and why polls stubbornly report margins of about three percent."
   },
   {
    "t": "For which population does the theorem fail entirely?",
    "o": [
     "A bimodal one",
     "A skewed one",
     "A Cauchy distribution, which has no finite variance",
     "A discrete one"
    ],
    "a": 2,
    "w": "Average n Cauchy draws and you get another Cauchy with the same spread as one draw. Bimodal and skewed populations converge - just more slowly."
   }
  ]
 },
 {
  "path": "maths/the_chain_rule.html",
  "title": "The Chain Rule",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Before the details”?",
    "ans": "When a function feeds into another — y = f(g(x)) — a change in x must travel through both to reach y . The chain rule says the sensitivities simply multiply."
   },
   {
    "t": "What does this module say about “The Gear Analogy”?",
    "ans": "Picture two gears. Turning the first makes the second turn 3× as fast; that second gear drives a third at 2×. Turn the first gear once and the last one spins 6 times — the ratios multiplied."
   },
   {
    "t": "What does this module say about “Reading the Diagram”?",
    "ans": "The chain strip shows x → u → y with each link's local derivative underneath. The app also computes a numeric check — the slope measured by actually nudging x by a tiny amount — and it always matches the product. The rule is not an approximation."
   }
  ]
 },
 {
  "path": "maths/jacobian_and_hessian.html",
  "title": "The Jacobian and the Hessian",
  "cat": "Maths",
  "q": [
   {
    "t": "What does the Hessian tell you that the gradient does not?",
    "o": [
     "Which direction is downhill",
     "How quickly the gradient changes, and therefore how far a step can safely go",
     "The value of the function",
     "Whether the function is continuous"
    ],
    "a": 1,
    "w": "The tangent says which way and how steeply; it says nothing about how long that remains true. Curvature is exactly what a step size wants to know."
   },
   {
    "t": "Why is Newton's method not used to train large neural networks?",
    "o": [
     "It converges too slowly",
     "The Hessian has n^2 entries and costs about n^3 to invert, which is impossible at a million parameters",
     "It requires a convex loss",
     "It cannot handle mini-batches"
    ],
    "a": 1,
    "w": "Near a minimum it converges quadratically, which is far better than gradient descent - it is purely the arithmetic that rules it out. Adam keeps a diagonal approximation instead."
   },
   {
    "t": "Why does backpropagation multiply Jacobians right to left?",
    "o": [
     "It is more numerically stable",
     "Starting from the scalar loss keeps every intermediate a vector rather than a full matrix",
     "The chain rule requires that order",
     "It allows parallelism"
    ],
    "a": 1,
    "w": "Left to right would carry a full matrix at every step. Reverse mode is why a backward pass costs a small multiple of a forward pass at any parameter count."
   }
  ]
 },
 {
  "path": "maths/the_normal_distribution.html",
  "title": "The Normal Distribution",
  "cat": "Maths",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The normal (or Gaussian) distribution is the familiar bell curve: symmetric, single-peaked, thin-tailed. It is completely specified by just two numbers — the mean μ sets where it sits, and the standard deviation σ sets how wide it is."
   },
   {
    "t": "What does this module say about “Two Knobs, Nothing Else”?",
    "ans": "That fixed unit area is what makes it a probability density: area under a stretch of the curve is the probability of landing in that range."
   },
   {
    "t": "What does this module say about “The 68–95–99.7 Rule”?",
    "ans": "These percentages hold for every normal distribution, whatever μ and σ are. Cycle the region selector and watch the shaded area match — the app integrates the curve numerically rather than quoting the constants."
   }
  ]
 },
 {
  "path": "maths/type_i_and_type_ii_errors.html",
  "title": "Type I and Type II Errors",
  "cat": "Maths",
  "q": [
   {
    "t": "You tighten alpha from 0.05 to 0.01. What happens to power?",
    "o": [
     "It rises",
     "It falls",
     "It is unchanged",
     "It depends on the sample size"
    ],
    "a": 1,
    "w": "The threshold moves right, shrinking the false-positive tail and growing the false-negative one. Moving the line always trades one error for the other."
   },
   {
    "t": "What improves both error rates at once?",
    "o": [
     "Moving the threshold",
     "A larger sample, because both curves narrow",
     "A smaller alpha",
     "A one-tailed test"
    ],
    "a": 1,
    "w": "Their spread is the standard error, which falls like root n, so the overlap shrinks. A larger true effect also works, but you rarely control that."
   },
   {
    "t": "Why are effects from underpowered studies often inflated?",
    "o": [
     "The analysis is biased",
     "Only an unusually large sample fluctuation could cross the threshold at that sample size",
     "Small samples have larger true effects",
     "The alpha was too strict"
    ],
    "a": 1,
    "w": "The winner's curse - and a substantial part of why published effects shrink on replication."
   }
  ]
 },
 {
  "path": "maths/vector_norms.html",
  "title": "Vector Norms",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A norm answers \"how big is this vector\", and L1, L2 and L∞ give three different answers — the sum of absolute values, the straight-line length, and the largest component — always ordered L∞ ≤ L2 ≤ L1, agreeing only on the axes."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "\"How big is this vector?\" sounds like it has one answer. It has several, and machine learning uses at least three of them routinely — often in the same model."
   },
   {
    "t": "What does this module say about “The shapes are the point”?",
    "ans": "Draw every vector whose norm equals exactly 1 and you get that norm's unit ball . This is where the three stop being interchangeable:"
   }
  ]
 },
 {
  "path": "maths/vectors_and_dot_product.html",
  "title": "Vectors and the Dot Product",
  "cat": "Maths",
  "q": [
   {
    "t": "Two vectors point in exactly opposite directions. Their dot product is:",
    "o": [
     "Zero",
     "Positive",
     "Negative",
     "Undefined"
    ],
    "a": 2,
    "w": "The dot product carries the cosine of the angle between them. At 180 degrees the cosine is -1, so the product is negative. It is zero only when they are perpendicular."
   },
   {
    "t": "What does a dot product of zero tell you?",
    "o": [
     "The vectors are identical",
     "The vectors are at right angles",
     "One vector has zero length",
     "Both b and c are possible"
    ],
    "a": 3,
    "w": "Perpendicular vectors give zero, and so does any vector dotted with the zero vector. Both cases are worth remembering - the second is a common source of silent bugs."
   },
   {
    "t": "Where does the dot product show up in a neural network?",
    "o": [
     "Only in the loss function",
     "In every neuron - the weighted sum is a dot product of weights and inputs",
     "Only during backpropagation",
     "Only in convolutional layers"
    ],
    "a": 1,
    "w": "w·x is literally a dot product. A layer of neurons is a stack of them, which is why a layer is implemented as a matrix multiply."
   }
  ]
 },
 {
  "path": "natural_language_processing/ascii_codes.html",
  "title": "ASCII Character Codes",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "ASCII is the essential bridge between human language and computer processing. It standardizes the representation of text as numbers, a fundamental step for all digital communication and computation. By interacting with the explorer, you can build a solid intuition for this cornerstone of computer science and NLP."
   },
   {
    "t": "What does this module say about “What is ASCII”?",
    "ans": "ASCII, which stands for American Standard Code for Information Interchange , is a character encoding standard. In simple terms, it's a universal dictionary that assigns a unique number to every letter, digit, and symbol you can type. Computers don't understand letters like 'A' or 'b'; they only understand numbers. ASCII translates our human-readable characters into a numerical format."
   },
   {
    "t": "What does this module say about “How It Works: From Character to Code”?",
    "ans": "The standard ASCII table contains 128 unique codes, numbered from 0 to 127. Each code represents a specific character. For example:"
   }
  ]
 },
 {
  "path": "natural_language_processing/backpropagation_through_time.html",
  "title": "Backpropagation Through Time",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "BPTT = unroll the loop, backpropagate through the chain, sum the shared-weight gradients. It makes RNNs trainable — but it also chains together T multiplications, and a long product of numbers below 1 races toward zero. That arithmetic inevitability is the vanishing gradient problem."
   },
   {
    "t": "What does this module say about “The Problem With a Loop”?",
    "ans": "Backpropagation works on feed-forward graphs — signals flow one way, gradients flow back the same way. An RNN's feedback loop breaks that picture. The fix, Backpropagation Through Time (BPTT) , is beautifully blunt: unroll the loop into T copies of the cell, one per timestep, and the loop becomes an ordinary (deep) feed-forward chain that standard backprop can handle."
   },
   {
    "t": "What does this module say about “Forward, Then Backward”?",
    "ans": "A recurrent network is a loop, and gradients cannot flow through a loop directly. So training unrolls it: a 50-step sequence becomes a 50-layer feed-forward network in which every layer shares the same weight matrix."
   }
  ]
 },
 {
  "path": "natural_language_processing/candidate_memory_in_lstm.html",
  "title": "Candidate Memory in LSTM",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The candidate layer is the LSTM's content generator: bounded, signed, and completely powerless on its own. Content and control are deliberately separated — $\\tanh$ proposes, sigmoid disposes. The last piece of the cell decides what the outside world gets to see: the Output Gate ."
   },
   {
    "t": "What does this module say about “A Proposal, Not a Decision”?",
    "ans": "The candidate layer — written $\\tilde{C}_t$ and read \"C-tilde\" — takes the same merged vector as every other layer and produces a fresh piece of content:"
   },
   {
    "t": "What does this module say about “Why $\\tanh$ and Not a Sigmoid”?",
    "ans": "This is the question that separates people who have memorised the diagram from people who understand it. The answer is sign ."
   }
  ]
 },
 {
  "path": "natural_language_processing/bert_vs_gpt.html",
  "title": "Encoder-only vs Decoder-only (BERT vs GPT)",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Both families are stacks of the same block: multi-head attention and a feed-forward layer, repeated. The difference is a mask applied inside self-attention — a matrix of minus infinities that deletes some of the attention scores before the softmax."
   },
   {
    "t": "What does this module say about “Why the mask decides the objective”?",
    "ans": "A model that can see the future cannot be trained to predict it. If position 4 can attend to position 5, then \"predict the token at position 5\" is answered by copying it, and nothing is learned. So the two masks admit different training tasks."
   },
   {
    "t": "What does this module say about “Two ways to train on the same architecture”?",
    "ans": "BERT and GPT are both transformers. What separates them is which direction they can look and what they are trained to predict — and everything else follows from that one choice."
   }
  ]
 },
 {
  "path": "natural_language_processing/forget_gate_in_lstm.html",
  "title": "Forget Gate in LSTM",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The Forget Gate is the only component that can remove information from an LSTM's long-term memory, and it does so multiplicatively and permanently. Keeping it near 1 turns the cell state into a protected highway across time; letting it drift toward 0 collapses the LSTM back into a forgetful RNN. Next, see how new information gets written in: the Input Gate ."
   },
   {
    "t": "What does this module say about “What the Gate Actually Is”?",
    "ans": "The Forget Gate is a small neural layer with a sigmoid output. It reads the merged vector $[H_{t-1}, X_t]$ and produces one number between 0 and 1 for every slot in the cell state :"
   },
   {
    "t": "What does this module say about “It Is a Dimmer, Not a Switch”?",
    "ans": "The word \"gate\" suggests open or closed, but the sigmoid makes it a dimmer per dimension . In a real trained LSTM the forget vector might look like $[0.98, 0.03, 0.71, 0.99, \\dots]$ — the cell holds on to some facts with near-perfect fidelity while dumping others in the same time step."
   }
  ]
 },
 {
  "path": "natural_language_processing/how_lstm_processes_text.html",
  "title": "How LSTM Processes Text",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “The Vanishing Gradient Problem”?",
    "ans": "Standard Recurrent Neural Networks (RNNs) pass a single \"hidden state\" forward through time. While great in theory, standard RNNs suffer from the vanishing gradient problem . During training, as the network looks back across many time steps (long sentences), the signals necessary to update the weights become microscopically small."
   },
   {
    "t": "What does this module say about “The Dual State Solution: Cell and Hidden States”?",
    "ans": "LSTMs solve this amnesia by introducing a more complex internal structure that passes two distinct states forward at every time step (as seen in the visualization):"
   },
   {
    "t": "What does this module say about “The Four Gates (Why so many parameters?)”?",
    "ans": "To control what gets added to or removed from the Cell State conveyor belt, the LSTM uses neural network layers called gates . Inside every single LSTM cell block shown in the visual, there are actually four separate fully-connected layers operating simultaneously:"
   }
  ]
 },
 {
  "path": "natural_language_processing/how_neural_network_text.html",
  "title": "How Neural Networks Process Text",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Neural networks process text by first converting words into meaningful numerical vectors (embeddings). These numbers are then passed through a series of hidden layers that extract increasingly complex features. Finally, an output layer makes a prediction based on these learned features."
   },
   {
    "t": "What does this module say about “The Core Challenge: Computers Don't Read Words”?",
    "ans": "Neural networks are powerful mathematical machines, but they only operate on numbers. They can't directly understand text like \"hello\" or \"world\". The first and most crucial step in Natural Language Processing (NLP) is to convert text into a numerical format that a network can process. This process is called text vectorization or word embedding ."
   },
   {
    "t": "What does this module say about “The Three Main Stages of Processing Text”?",
    "ans": "Our interactive visualization demonstrates the key stages a neural network follows to process text data:"
   }
  ]
 },
 {
  "path": "natural_language_processing/how_rnn_process_text.html",
  "title": "How RNN Processes Text",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “The Power of Memory in Language”?",
    "ans": "Standard neural networks have a major limitation: they have no memory of the past. They process each input independently. This is a problem for language, where the order of words is crucial. For example, \"dog bites man\" and \"man bites dog\" use the same words but have completely different meanings."
   },
   {
    "t": "What does this module say about “The Unrolled RNN: Step-by-Step Processing”?",
    "ans": "The visualization above \"unrolls\" the RNN loop, showing it as a sequence of identical cells, one for each word (or \"time step\"). Here’s how the information flows:"
   },
   {
    "t": "What does this module say about “Shared Weights: The Key to Learning”?",
    "ans": "A crucial concept in RNNs is shared weights . The same set of calculations (the same \"brain\") is used at every single time step. This is incredibly efficient. Instead of learning a new set of rules for the first word, second word, etc., the RNN learns a single set of rules for how to update its memory based on a new word and its previous memory."
   }
  ]
 },
 {
  "path": "natural_language_processing/how_words_are_represented_in_neural_networks.html",
  "title": "How Words are Represented in Neural Networks",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Word representation is a ladder: IDs are compact but lie about order, one-hot is honest but huge and similarity-blind, and dense embeddings are small, learned, and encode meaning as geometry. Modern NLP starts at the top of that ladder."
   },
   {
    "t": "What does this module say about “The Chain of Translations”?",
    "ans": "A neural network is a pile of multiplications and additions — it can only consume numbers. So every word goes through a chain of translations: word → token ID → one-hot vector → dense embedding . Each stage exists to fix a shortcoming of the previous one."
   },
   {
    "t": "What does this module say about “Token IDs and Their Trap”?",
    "ans": "The dictionary lookup (\"cat\" → 1, \"dog\" → 3) is compact, but the raw integers smuggle in a false claim: that \"dog\" (3) is somehow three times \"cat\" (1), or that words with adjacent IDs are related. The IDs are arbitrary labels, and arithmetic on labels is meaningless — a network fed raw IDs will happily learn those fake relationships."
   }
  ]
 },
 {
  "path": "natural_language_processing/how_are_embeddings_generated.html",
  "title": "How are Embeddings Generated?",
  "cat": "NLP",
  "q": [
   {
    "t": "What is meant by “Masked language modelling” here?",
    "ans": "(BERT) hides 15% of tokens and predicts them from both directions."
   },
   {
    "t": "What is meant by “Next-token prediction” here?",
    "ans": "(GPT) predicts each token from those before it."
   }
  ]
 },
 {
  "path": "natural_language_processing/input_gate_in_lstm.html",
  "title": "Input Gate in LSTM",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The Input Gate is the LSTM's write-enable line. It converts a proposal into an actual memory change, one dimension at a time, and it does so by adding rather than overwriting. To see where that proposal comes from, study the Candidate Memory layer next."
   },
   {
    "t": "What does this module say about “What the Gate Actually Is”?",
    "ans": "Like the Forget Gate, the Input Gate is a sigmoid layer emitting one value per memory slot:"
   },
   {
    "t": "What does this module say about “Why Addition, Not Replacement”?",
    "ans": "The written term is added to what the Forget Gate let through. This matters enormously. Replacement would destroy old memory every time something new arrived; addition lets the cell accumulate — keeping the subject of a sentence while layering on new adjectives."
   }
  ]
 },
 {
  "path": "natural_language_processing/rnn.html",
  "title": "Interactive 3D RNN Visualizer",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Network Inspector”?",
    "ans": "Hover over the unrolled 3D network to inspect states and trace data flow. Click a node to focus camera."
   },
   {
    "t": "What does this module say about “The Temporal Dimension (Unrolling)”?",
    "ans": "In the 3D visualization above, the network is \"unrolled\" across time along the Z-axis. While it looks like a massive network, it is actually the exact same set of weights being applied repeatedly at each time step $t$. The $Z$-axis visually represents the passage of time."
   },
   {
    "t": "What does this module say about “Deep RNNs (Multiple Layers)”?",
    "ans": "Just like standard neural networks benefit from depth, RNNs can be stacked into Deep RNNs . By setting the \"Hidden Layers\" dropdown to 2 or 3, you create a hierarchy. The first hidden layer extracts basic temporal features from the raw input sequence, while higher layers piece together those basic features to understand more complex, long-term abstractions."
   }
  ]
 },
 {
  "path": "natural_language_processing/limitations_of_ann_with_sequential_data.html",
  "title": "Limitations of ANN with Sequential Data",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “The Setup”?",
    "ans": "A classic feed-forward network (ANN / MLP) is a brilliant function approximator — for fixed-size, unordered inputs. Sequential data violates both assumptions at once: sentences have different lengths, and their meaning lives in the ordering. The result is three distinct failure modes."
   },
   {
    "t": "What does this module say about “Limitation 1: The Input Layer is a Fixed-Width Door”?",
    "ans": "The first layer of an ANN has a hard-coded number of neurons. A 6-slot network offers exactly two bad options for real text: truncate longer inputs (information destroyed before learning even starts) or pad shorter ones with dummy values (the network wastes capacity learning to ignore filler). There is no third option — the architecture physically cannot stretch."
   },
   {
    "t": "What does this module say about “Limitation 2: Order Blindness”?",
    "ans": "The standard fixed-size representation for text — bag of words — counts word occurrences and discards positions. \"Dog bites man\" and \"man bites dog\" produce bit-for-bit identical vectors , so the network is mathematically incapable of distinguishing them, no matter how long you train. Whatever information lives in the ordering is gone before the first neuron fires."
   }
  ]
 },
 {
  "path": "natural_language_processing/multi_head_attention.html",
  "title": "Multi-Head Attention",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Multi-head attention runs several attention operations in parallel, each with its own projections, so a layer can represent several relationships at once instead of compromising between them in a single distribution that must sum to 1."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A single self-attention layer produces one set of weights per word, and those weights must sum to 1. That is a hard constraint: attention spent on one word is attention taken from another."
   },
   {
    "t": "What does this module say about “The idea”?",
    "ans": "Run several attention operations in parallel. Each gets its own query, key and value projections, so each is free to compare words along a different axis and produce a completely different weighting. Then concatenate their outputs and pass the result through one more linear layer to mix them back together."
   }
  ]
 },
 {
  "path": "natural_language_processing/n_gram.html",
  "title": "N-gram Explainer",
  "cat": "NLP",
  "q": [
   {
    "t": "What is meant by “Features for classical classifiers” here?",
    "ans": "TF-IDF over unigrams and bigrams, plus logistic regression, remains a strong baseline for text classification — and it trains in seconds."
   },
   {
    "t": "What is meant by “Character n-grams” here?",
    "ans": "for language identification, authorship attribution and handling misspellings. Character 3-grams are remarkably effective at identifying a language from a short string."
   },
   {
    "t": "What is meant by “Autocomplete and query suggestion,” here?",
    "ans": "where a count-based model over query logs is fast and adequate."
   },
   {
    "t": "What is meant by “Spelling correction” here?",
    "ans": "and fuzzy matching, using character n-gram overlap."
   }
  ]
 },
 {
  "path": "natural_language_processing/tokenization.html",
  "title": "NLP Tokenizer",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “What is Tokenization”?",
    "ans": "Tokenization is the fundamental first step in any Natural Language Processing (NLP) pipeline. It's the process of breaking down a stream of raw text into smaller, meaningful units called tokens . These tokens can be words, characters, or sub-word units, depending on the chosen strategy."
   },
   {
    "t": "What does this module say about “Why is Tokenization So Important”?",
    "ans": "Imagine trying to understand a sentence by looking at it as one continuous string of letters. It would be nearly impossible. Tokenization provides the structure that machines need. By converting a sentence like \"NLP is fascinating!\" into tokens such as [\"NLP\", \"is\", \"fascinating\", \"!\"] , we create a list of items that a model can count, analyze, and assign meaning to."
   },
   {
    "t": "What does this module say about “Exploring Different Tokenization Methods”?",
    "ans": "There's no single \"best\" way to tokenize text; the right method depends on the task and the language. The interactive visualizer above lets you experiment with the most common strategies. Let's explore them:"
   }
  ]
 },
 {
  "path": "natural_language_processing/normalization_techniques_for_sequential_data.html",
  "title": "Normalization Techniques for Sequential Data",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Normalising over the wrong axis”?",
    "ans": "Every normalisation layer does the same arithmetic — subtract a mean, divide by a standard deviation, then apply a learned scale and shift. What differs is which values are pooled to compute that mean and deviation."
   },
   {
    "t": "What does this module say about “Why batch norm fails on sequences”?",
    "ans": "Variable length. Sequences in a batch have different lengths, so timestep 50 might have 32 real values in one batch and 3 in another, with the rest padding. Statistics computed over that are unstable, and computed over padding they are simply wrong. Per-timestep statistics."
   },
   {
    "t": "What does this module say about “Two different meanings of \"normalisation\"”?",
    "ans": "The word covers two unrelated operations in sequence work, and conflating them causes confusion."
   }
  ]
 },
 {
  "path": "natural_language_processing/output_gate_in_lstm.html",
  "title": "Output Gate in LSTM",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Why $\\tanh(C_t)$ First”?",
    "ans": "The cell state is a running sum, so it can drift well outside $[-1, 1]$ after many additions. Feeding that raw value to the next layer would produce unstable activations. Squashing with $\\tanh$ rescales it into a bounded, zero-centred range before the gate scales it further."
   },
   {
    "t": "What does this module say about “It Closes the Loop”?",
    "ans": "$H_t$ is not just the cell's answer — it is also half of the input to the next time step, where it will help compute all four layers again. So the Output Gate does double duty: it decides what the outside world sees, and it decides what the cell tells its own future self. A closed output gate leaves the next step reasoning almost entirely from the incoming token."
   },
   {
    "t": "What does this module say about “Deciding what to expose”?",
    "ans": "The cell state holds everything the LSTM is carrying. The output gate decides how much of it to reveal as this step's output."
   }
  ]
 },
 {
  "path": "natural_language_processing/positional_encoding.html",
  "title": "Positional Encoding",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Self-attention computes every position from every other position by dot products and weighted sums. Nowhere in that computation does an index appear. Permute the input and the outputs permute with it, unchanged — the mechanism is permutation-equivariant . For a bag of words that would be a feature."
   },
   {
    "t": "What does this module say about “The obvious ideas, and why they fail”?",
    "ans": "Both are available in the Scheme control above. What is wanted is something bounded, unique per position, consistent across sentence lengths, and — ideally — carrying information about relative distance, since \"the adjective three words back\" is a far more useful notion than \"the word at index 17\"."
   },
   {
    "t": "What does this module say about “The sinusoidal answer”?",
    "ans": "The original transformer used a fixed function of position, with a different frequency in every pair of dimensions:"
   }
  ]
 },
 {
  "path": "natural_language_processing/query_key_value.html",
  "title": "Query, Key and Value",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The previous module described attention as score, normalise, blend. That description works, but it leaves one thing vague: what exactly is being compared against what?"
   },
   {
    "t": "What does this module say about “A soft dictionary lookup”?",
    "ans": "Attention is easiest to read as a lookup that returns a blend rather than one entry."
   },
   {
    "t": "What does this module say about “Why keys and values are separate”?",
    "ans": "It is reasonable to ask why we need both — why not match against the values directly and save a matrix?"
   }
  ]
 },
 {
  "path": "natural_language_processing/rnn_architecture.html",
  "title": "RNN Architecture",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "An RNN is one cell unrolled across time, sharing weights at every step, so its parameter count is fixed at dh + h² + h regardless of sequence length. Training backpropagates through the whole unrolled graph, which makes the effective depth equal to the sequence length — hence vanishing gradients, mandatory gradient clipping, and truncated BPTT."
   },
   {
    "t": "What does this module say about “Unrolling”?",
    "ans": "An RNN is usually drawn as a cell with an arrow looping back to itself. That is compact and slightly misleading. To understand training, unroll it: draw one copy of the cell per timestep, with the hidden state flowing left to right between copies."
   },
   {
    "t": "What does this module say about “Internal Flow”?",
    "ans": "Unrolling a recurrent cell across time gives a network as deep as the sequence is long - sharing one set of weights the whole way. That is what makes RNNs efficient, and what makes them hard to train."
   }
  ]
 },
 {
  "path": "natural_language_processing/self_attention.html",
  "title": "Self-Attention",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "In encoder–decoder attention the queries come from one sequence and the keys and values from another. Self-attention is the same machinery with a single change: all three come from the same sequence . The sentence attends to itself."
   },
   {
    "t": "What does this module say about “What a word is actually doing”?",
    "ans": "Every position emits a query, a key and a value . Each query is scored against every key — including its own — giving an n × n grid of scores. Softmax each row, and you have the matrix above: row i is how word i distributes its attention across the whole sentence."
   },
   {
    "t": "What does this module say about “The example worth staring at”?",
    "ans": "\"The animal didn't cross the street because it was too tired.\" What does \"it\" refer to?"
   }
  ]
 },
 {
  "path": "natural_language_processing/sequential_data_preparation_with_sliding_window.html",
  "title": "Sequential Data Preparation with Sliding Window",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The sliding window is the simplest bridge between sequential data and supervised learning: it manufactures labeled examples from an unlabeled stream. Its fixed width is both its strength (simplicity) and its weakness — the model can never look further back than w steps, which is exactly the limitation that motivates recurrent architectures."
   },
   {
    "t": "What does this module say about “The Problem It Solves”?",
    "ans": "Supervised learning needs pairs: an input X and the correct answer y . But a time series or a sentence arrives as one long, unlabeled stream. The sliding window converts that stream into training data by declaring: \"the last w values are the input, and the very next value is the target.\""
   },
   {
    "t": "What does this module say about “How It Works”?",
    "ans": "Given a sequence of length N and a window of size w, slide the window one position at a time:"
   }
  ]
 },
 {
  "path": "natural_language_processing/stemming_vs_lemmatization.html",
  "title": "Stemming vs Lemmatization",
  "cat": "NLP",
  "q": [
   {
    "t": "What is meant by “Lemmatising without a part of speech,” here?",
    "ans": "so verbs and adjectives are treated as nouns and left unchanged."
   },
   {
    "t": "What is meant by “Using an English stemmer on other languages” here?",
    "ans": "Suffix rules are language-specific, and applying English ones to German or Turkish produces nonsense."
   },
   {
    "t": "What is meant by “Stemming before a transformer” here?",
    "ans": "Destroys information and creates out-of-vocabulary fragments."
   },
   {
    "t": "What is meant by “Stemming the query but not the index” here?",
    "ans": "(or vice versa) in a search system, so nothing matches."
   }
  ]
 },
 {
  "path": "natural_language_processing/text_encoding_techniques_in_nlp.html",
  "title": "Text Encoding Techniques in NLP",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Sparse encodings are a progression of fixes: one-hot removes label encoding's fake ordering, bag-of-words adds document structure, TF-IDF suppresses noise words. What none of them can do is say that \"cat\" and \"kitten\" are related — for that you need embeddings , the subject of the next module."
   },
   {
    "t": "What does this module say about “A Ladder of Encodings”?",
    "ans": "Once you accept that text must become numbers, the question is which numbers. The four classic answers form a ladder — each rung keeps more information or removes more distortion than the one below it."
   },
   {
    "t": "What does this module say about “Label Encoding & One-Hot”?",
    "ans": "Label encoding assigns each vocabulary word an integer. It's maximally compact, but the integers imply a fake ordering — the model may conclude that word #7 is \"more\" than word #3. One-hot encoding removes that lie by giving each word its own dimension: a vector of zeros with a single 1."
   }
  ]
 },
 {
  "path": "natural_language_processing/text_normalization_pipeline.html",
  "title": "Text Normalization Pipeline",
  "cat": "NLP",
  "q": [
   {
    "t": "What is meant by “Observe the Order” here?",
    "ans": "Try changing the order of operations (though the visualizer has a fixed order, imagine swapping them). What happens if you remove stopwords *before* converting to lowercase? The word \"The\" would not be removed because it doesn't match the lowercase \"the\" in the stopword list. This highlights why the pipeline's sequence is important."
   },
   {
    "t": "What is meant by “Toggle Steps On and Off” here?",
    "ans": "Run the pipeline with only \"Lowercase\" and \"Remove Punctuation\" enabled. Then, progressively add more steps. Notice how the character count and the text itself change with each addition. This demonstrates the impact of each normalization technique."
   },
   {
    "t": "What is meant by “Use Different Inputs” here?",
    "ans": "Try pasting in different kinds of text. Use a formal sentence, a casual tweet with hashtags and mentions, and a line of code. See how the pipeline handles each one. This will build your intuition for where and why text normalization is so crucial in the world of NLP."
   }
  ]
 },
 {
  "path": "natural_language_processing/attention_mechanism.html",
  "title": "The Attention Mechanism",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The encoder–decoder models that came before attention worked like this: an RNN read the whole input sentence and squeezed it into a single fixed-length vector, and a second RNN generated the output from that vector alone."
   },
   {
    "t": "What does this module say about “The fix”?",
    "ans": "Attention throws away the assumption that the decoder needs one summary. Instead, keep every encoder state, and at each output step let the decoder build a fresh context vector by weighting them:"
   },
   {
    "t": "What does this module say about “Why the weights are interpretable”?",
    "ans": "Because they sum to 1 and are all positive, the weights read as a distribution of interest: \"to produce this word, I looked 70% at cat and 20% at the \". Plotting them for every output word against every input word gives the alignment matrix in the second panel, and on a translation task it recovers word alignment without ever having been told what alignment is."
   }
  ]
 },
 {
  "path": "natural_language_processing/transformer_architecture.html",
  "title": "The Transformer Architecture",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A transformer block is two sublayers, each wrapped in the same add-and-normalise pattern: attention moves information between positions, and a position-wise feed-forward network processes each token on its own. The residual connection is what makes depth possible, giving the gradient a path that skips each sublayer — remove it and a deep stack stops training entirely — while layer normalisation holds the activation s..."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The previous modules built the parts: query, key and value , self-attention , multiple heads , positional encoding . This module assembles them."
   },
   {
    "t": "What does this module say about “What each piece is for”?",
    "ans": "The division of labour between the first two is worth holding on to: attention mixes across tokens, the FFN thinks about each token. A transformer alternates between the two, over and over."
   }
  ]
 },
 {
  "path": "natural_language_processing/vanishing_gradient_problem_in_rnn.html",
  "title": "Vanishing Gradient Problem in RNN",
  "cat": "NLP",
  "q": [
   {
    "t": "What is meant by “Use an LSTM or GRU” here?",
    "ans": "rather than a plain RNN. This is the main fix, and it is free."
   },
   {
    "t": "What is meant by “Orthogonal initialisation” here?",
    "ans": "of the recurrent matrix keeps its singular values at 1, so the product neither grows nor shrinks initially."
   },
   {
    "t": "What is meant by “Shorter sequences,” here?",
    "ans": "or truncated backpropagation through time, which bounds how far gradients must travel."
   },
   {
    "t": "What is meant by “Attention,” here?",
    "ans": "which removes the distance dependence entirely."
   }
  ]
 },
 {
  "path": "natural_language_processing/what_are_embeddings.html",
  "title": "What are Embeddings?",
  "cat": "NLP",
  "q": [
   {
    "t": "What is an embedding?",
    "o": [
     "A compressed copy of the text",
     "A dense vector whose position encodes meaning, learned from usage",
     "A dictionary of definitions",
     "The tokenizer's vocabulary"
    ],
    "a": 1,
    "w": "Embeddings place words in a space where distance means something. Nothing about the meaning is written down - it is inferred entirely from which contexts a word turns up in."
   },
   {
    "t": "Why are embeddings better than one-hot vectors for words?",
    "o": [
     "They use less memory only",
     "One-hot makes every pair of words equally distant, so no similarity can be expressed",
     "One-hot vectors cannot be used in networks",
     "They are easier to compute"
    ],
    "a": 1,
    "w": "Under one-hot, 'cat' is exactly as far from 'dog' as from 'parliament'. Embeddings can put related words near each other, which is the whole point."
   },
   {
    "t": "Embeddings trained on ordinary web text reliably reproduce:",
    "o": [
     "Perfect definitions",
     "The social biases present in that text",
     "Grammatical rules only",
     "Nothing beyond word frequency"
    ],
    "a": 1,
    "w": "The vectors encode how words are actually used, including every stereotype in the corpus. This is measurable, well documented, and a real problem in deployed systems."
   }
  ]
 },
 {
  "path": "natural_language_processing/what_is_lstm.html",
  "title": "What is LSTM?",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "An LSTM separates long-term memory (the cell state) from working output (the hidden state) and controls the flow between them with three learned sigmoid gates. Because the cell state is updated by addition and gated multiplication rather than a matrix multiply, the gradient travels back through it multiplied only by the forget gate — so when the model chooses to remember, it genuinely can, for hundreds of steps."
   },
   {
    "t": "What does this module say about “Two states, not one”?",
    "ans": "A simple recurrent cell has one hidden state, and it is completely rewritten at every timestep. An LSTM has two:"
   },
   {
    "t": "What does this module say about “The three gates”?",
    "ans": "Each gate is a small sigmoid layer producing values in [0, 1], which then multiply a vector elementwise — 0 blocks completely, 1 passes completely, and everything between is a partial pass."
   }
  ]
 },
 {
  "path": "natural_language_processing/what_is_bi_directional_layer.html",
  "title": "What is a Bidirectional Layer?",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Why one direction is not enough”?",
    "ans": "A forward RNN at position t has seen tokens 1 to t and nothing after. That is a real handicap, because disambiguation frequently depends on what comes next."
   },
   {
    "t": "What does this module say about “How the two passes combine”?",
    "ans": "A bidirectional layer runs two entirely separate recurrent cells with their own weights. The forward cell reads left to right; the backward cell reads the same sequence right to left. At each position their hidden states are concatenated:"
   },
   {
    "t": "What does this module say about “Reading the sequence twice”?",
    "ans": "A forward LSTM at word 5 knows words 1 to 5. A bidirectional layer runs a second, independent LSTM backwards — from the end to the beginning — and concatenates the two hidden states at each position."
   }
  ]
 },
 {
  "path": "natural_language_processing/what_is_a_gru.html",
  "title": "What is a GRU?",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Simplify Without Breaking”?",
    "ans": "The Gated Recurrent Unit (Cho et al., 2014) asked a sharp question: does an LSTM really need three gates and two separate memory tracks? The GRU's answer: merge the cell state and hidden state into one vector, merge forget+input into a single update gate z , and add a reset gate r for proposing new content. Same gating idea, leaner machine."
   },
   {
    "t": "What does this module say about “How the Two Gates Cooperate”?",
    "ans": "zₜ = σ(W⃂xₜ + U⃂hₜ₋₁) · rₜ = σ(Wᵣxₜ + Uᵣhₜ₋₁) h̃ₜ = tanh(W·xₜ + U·(rₜ⊙hₜ₋₁)) hₜ = zₜ⊙hₜ₋₁ + (1 − zₜ)⊙h̃ₜ"
   },
   {
    "t": "What does this module say about “LSTM vs GRU at a Glance”?",
    "ans": "A GRU is an LSTM with the design simplified. It merges the forget and input gates into a single update gate , and it drops the separate cell state — there is only the hidden state."
   }
  ]
 },
 {
  "path": "natural_language_processing/what_is_a_recurrent_cell.html",
  "title": "What is a Recurrent Cell?",
  "cat": "NLP",
  "q": [
   {
    "t": "What is meant by “Streaming with bounded memory” here?",
    "ans": "One fixed-size state regardless of how much has been processed, where a transformer's KV cache grows with every token."
   },
   {
    "t": "What is meant by “On-device inference” here?",
    "ans": "Small, fast, no attention kernels required."
   },
   {
    "t": "What is meant by “Small datasets” here?",
    "ans": "The inductive bias helps where a transformer trained from scratch overfits."
   },
   {
    "t": "What is meant by “Classical time series” here?",
    "ans": "Numeric sequences of moderate length, where windowing plus a GRU is a strong baseline."
   }
  ]
 },
 {
  "path": "natural_language_processing/what_is_a_sequence.html",
  "title": "What is a Sequence?",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “The Core Idea”?",
    "ans": "A sequence is an ordered collection of items where the position of each item carries meaning. \"Dog bites man\" and \"man bites dog\" contain exactly the same three words, yet they describe opposite events. That difference lives entirely in the order — and order is precisely what ordinary tabular data doesn't have."
   },
   {
    "t": "What does this module say about “Sequential vs. Tabular Data”?",
    "ans": "In a classic spreadsheet-style dataset, each row is independent: shuffling the rows of a housing-price table changes nothing about what a model can learn. Sequential data breaks this assumption in two ways:"
   },
   {
    "t": "What does this module say about “Order is part of the data”?",
    "ans": "A sequence is data where the order carries meaning. Shuffle it and you have destroyed information, not merely rearranged it."
   }
  ]
 },
 {
  "path": "natural_language_processing/why_text_encoding_is_needed_in_nlp.html",
  "title": "Why Text Encoding is Needed in NLP",
  "cat": "NLP",
  "q": [
   {
    "t": "What is meant by “Normalise” here?",
    "ans": "— Unicode form, whitespace, markup. Not case or punctuation."
   },
   {
    "t": "What is meant by “Tokenise” here?",
    "ans": "into subwords with the model's own tokeniser."
   }
  ]
 },
 {
  "path": "natural_language_processing/word_cloud.html",
  "title": "Word Cloud Generator",
  "cat": "NLP",
  "q": [
   {
    "t": "What is meant by “Stop words are language-specific” here?",
    "ans": "An English list applied to French text leaves \"le\", \"de\" and \"et\" dominating."
   },
   {
    "t": "What is meant by “Domain stop words matter too” here?",
    "ans": "In product reviews, \"product\", \"item\" and the brand name are noise; add them to the list."
   },
   {
    "t": "What is meant by “Lemmatise or accept duplicates” here?",
    "ans": "\"Run\", \"runs\" and \"running\" appear as three words otherwise."
   },
   {
    "t": "What is meant by “Watch for a dominating single term” here?",
    "ans": "that compresses everything else to illegibility. A log scale on the weights helps."
   }
  ]
 },
 {
  "path": "pydantic/aliases.html",
  "title": "Aliases",
  "cat": "Pydantic",
  "q": [
   {
    "t": "You set `alias=\"publishedAt\"`. Why does `Module(published_at=...)` now fail?",
    "o": [
     "A bug",
     "By default the alias replaces the Python name as input",
     "Aliases are output-only",
     "It needs by_alias"
    ],
    "a": 1,
    "w": "The alias becomes the input name. `populate_by_name=True` restores the Python name as an accepted alternative, which is almost always what you want."
   },
   {
    "t": "Your API accepts camelCase but returns snake_case. What is missing?",
    "o": [
     "populate_by_name",
     "by_alias=True on the dump",
     "validation_alias",
     "An alias_generator"
    ],
    "a": 1,
    "w": "Aliases are not used for output unless requested. FastAPI does this for you on response models, which is why a manual dump elsewhere can behave differently."
   },
   {
    "t": "What is `AliasChoices` for?",
    "o": [
     "Choosing between models",
     "Accepting several input spellings, first one present wins",
     "Output formatting",
     "Nested paths"
    ],
    "a": 1,
    "w": "It is the clean way to run a rename: add the new name, keep the old, and clients migrate at their own pace with no branching in your code."
   },
   {
    "t": "What does `AliasPath(\"author\", \"name\")` do?",
    "o": [
     "Renames the field",
     "Pulls a value from a nested payload into a flat field",
     "Creates a nested model",
     "Sets a serialisation alias"
    ],
    "a": 1,
    "w": "Strings are keys and integers are indices, so a nested response flattens into your model. It is validation-only - there is no serialisation equivalent."
   }
  ]
 },
 {
  "path": "pydantic/annotated_and_custom_types.html",
  "title": "Annotated and Custom Types",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What is `Annotated[str, Field(pattern=...)]`?",
    "o": [
     "A Pydantic-only construct",
     "A real type you can name and reuse anywhere",
     "A validator",
     "A default value"
    ],
    "a": 1,
    "w": "`Annotated` is standard typing. Bound to a name it becomes a reusable type, so a rule is defined once and every use site stays consistent."
   },
   {
    "t": "In `Annotated[str, BeforeValidator(f), Field(pattern=p)]`, what runs first?",
    "o": [
     "The pattern",
     "The before-validator, then coercion, then the pattern",
     "They run in parallel",
     "Undefined order"
    ],
    "a": 1,
    "w": "Before-validators see raw input, then coercion happens, then constraints, then after-validators. Written the other way the pattern would reject values the normaliser was meant to fix."
   },
   {
    "t": "Why is `Annotated[int, Field(gt=0)] = 10` preferable to `Field(default=10, gt=0)`?",
    "o": [
     "It is faster",
     "It separates what the type is from what it defaults to, and the type can be named and reused",
     "The second is invalid",
     "No difference at all"
    ],
    "a": 1,
    "w": "Behaviour is identical; the Annotated form keeps the constraint with the type and the default where defaults normally sit, and lets the constrained type be reused."
   },
   {
    "t": "What does `SecretStr` protect against?",
    "o": [
     "Weak passwords",
     "The value appearing in repr, logs and tracebacks",
     "SQL injection",
     "Short strings"
    ],
    "a": 1,
    "w": "It hides the value in representations so a token cannot leak into a log by accident, and requires `.get_secret_value()` to read it - making every access deliberate."
   }
  ]
 },
 {
  "path": "pydantic/collections_of_models.html",
  "title": "Collections of Models",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Item 1 of a 4-item list is invalid. What happens to items 2 and 3?",
    "o": [
     "They are skipped",
     "They are still validated and their failures reported too",
     "The whole list is rejected untested",
     "Only item 1 is reported"
    ],
    "a": 1,
    "w": "Validation covers the whole collection and reports every failure in one exception, which is what makes bulk imports fixable in a single pass."
   },
   {
    "t": "What does `Set[float]` do with `[1.0, 2.0, 1.0]`?",
    "o": [
     "Raises on the duplicate",
     "Gives a set of two items",
     "Gives three items",
     "Gives a list"
    ],
    "a": 1,
    "w": "Sets deduplicate silently. That is right for tags and wrong for measurements - if repeats are meaningful, use a list."
   },
   {
    "t": "You need to validate a bare JSON array of models. What is the right tool?",
    "o": [
     "A wrapper model with one list field",
     "TypeAdapter(List[Model])",
     "A loop calling model_validate",
     "It cannot be validated"
    ],
    "a": 1,
    "w": "`TypeAdapter` validates any annotation directly. The wrapper model is the workaround people reach for before discovering it."
   },
   {
    "t": "Why is `TypeAdapter(List[X]).validate_python(rows)` better than a list comprehension of `X.model_validate`?",
    "o": [
     "No difference",
     "It loops inside the compiled core rather than crossing into Python per item",
     "It skips validation",
     "It is only for JSON"
    ],
    "a": 1,
    "w": "One call into Rust validates the whole list. The comprehension does the same checks with one Python-to-Rust round trip per item."
   }
  ]
 },
 {
  "path": "pydantic/computed_fields.html",
  "title": "Computed Fields",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Why does a plain `@property` not appear in `model_dump()`?",
    "o": [
     "It is a bug",
     "Properties are not fields; only `@computed_field` adds one to the output",
     "It needs an annotation",
     "It does appear"
    ],
    "a": 1,
    "w": "A property is ordinary Python and Pydantic does not serialise it. `@computed_field` is the opt-in that makes a derived value part of the model's output."
   },
   {
    "t": "What happens if you pass a computed field to the constructor?",
    "o": [
     "It overrides the calculation",
     "It is ignored, or rejected with extra=forbid",
     "It raises always",
     "It is stored"
    ],
    "a": 1,
    "w": "Computed fields are output-only. Allowing them as input would create a second source of truth for a value that is a function of the model."
   },
   {
    "t": "A computed field divides by another field that can be zero. When does this fail?",
    "o": [
     "At validation, as a ValidationError",
     "At serialisation, as a ZeroDivisionError",
     "Never",
     "At class definition"
    ],
    "a": 1,
    "w": "The model validates fine - every field is the right type. The failure arrives at `model_dump()` and is not a ValidationError, so validation error handling does not catch it."
   },
   {
    "t": "Which schema mode shows computed fields?",
    "o": [
     "validation",
     "serialization",
     "Both",
     "Neither"
    ],
    "a": 1,
    "w": "They describe what the model emits, never what it accepts, so they appear in `model_json_schema(mode=\"serialization\")` - which is what a FastAPI response model uses."
   }
  ]
 },
 {
  "path": "pydantic/custom_serializers.html",
  "title": "Custom Serializers",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Does a `@field_serializer` change what the field holds in memory?",
    "o": [
     "Yes",
     "No - only the output; validation and the stored type are unaffected",
     "Only in JSON mode",
     "It replaces the validator"
    ],
    "a": 1,
    "w": "It runs on the way out. The attribute is still the validated type, so arithmetic and comparisons keep working - which is what makes the feature safe."
   },
   {
    "t": "A Decimal field is serialised as \"£12.50\". What does the schema say?",
    "o": [
     "string",
     "Still a decimal, unless you set return_type",
     "It errors",
     "Nothing"
    ],
    "a": 1,
    "w": "Serialisers change output but not the schema, so docs and generated clients describe a type the endpoint no longer returns. `return_type` keeps them honest."
   },
   {
    "t": "Why prefer `@model_serializer(mode=\"wrap\")` over the plain form?",
    "o": [
     "It is faster",
     "The handler produces the default output, so newly added fields still flow through",
     "It is required",
     "It supports JSON only"
    ],
    "a": 1,
    "w": "The plain form makes every field your responsibility, so a field added later silently never appears. Wrapping augments the default rather than replacing it."
   },
   {
    "t": "What is the argument against serialising a date as \"26 August 2026\"?",
    "o": [
     "It is slower",
     "It is display formatting: a client cannot sort, filter or localise it",
     "Dates cannot be formatted",
     "It breaks validation"
    ],
    "a": 1,
    "w": "ISO output is data every client can work with. Formatting assumes a language and a reader, and belongs in the layer that knows who the audience is."
   }
  ]
 },
 {
  "path": "pydantic/dates_uuids_and_decimals.html",
  "title": "Dates, UUIDs and Decimals",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Why does `Decimal(\"0.1\")` differ from `Decimal(0.1)`?",
    "o": [
     "They are the same",
     "The float is already inexact before Decimal sees it",
     "Decimal cannot take strings",
     "The string is rounded"
    ],
    "a": 1,
    "w": "0.1 has no exact binary representation, so the float is already wrong when it is handed over. Decimal faithfully preserves the wrong value - which is why money travels as a string."
   },
   {
    "t": "What happens when you compare a naive datetime with an aware one?",
    "o": [
     "It works",
     "Python raises TypeError",
     "The naive one is assumed UTC",
     "Pydantic converts it"
    ],
    "a": 1,
    "w": "They are not comparable. A model accepting plain `datetime` takes both kinds happily, so the failure appears far from the model - which is what `AwareDatetime` prevents."
   },
   {
    "t": "Why does `json.dumps(m.model_dump())` fail on a model with a date field?",
    "o": [
     "model_dump is broken",
     "model_dump returns Python objects, and json.dumps cannot serialise a date",
     "Dates are unsupported",
     "It needs mode='python'"
    ],
    "a": 1,
    "w": "`model_dump()` deliberately keeps Python types. Use `model_dump_json()`, or `model_dump(mode=\"json\")` when you need the dict first."
   },
   {
    "t": "Which constraint expresses 'a currency amount in whole pence'?",
    "o": [
     "gt=0",
     "decimal_places=2",
     "max_length=2",
     "multiple_of=0.01"
    ],
    "a": 1,
    "w": "`decimal_places=2` rejects values with more precision than the system handles, and records that decision in the schema where it can be read."
   }
  ]
 },
 {
  "path": "pydantic/enums_and_literals.html",
  "title": "Enums and Literals",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Why prefer `Literal[\"a\", \"b\"]` over `Field(pattern=r\"^(a|b)$\")`?",
    "o": [
     "It is faster",
     "Better error, appears as an enum in the schema, and mypy understands it",
     "Patterns do not work",
     "No real difference"
    ],
    "a": 1,
    "w": "The Literal error lists the allowed values, the schema becomes a renderable choice for clients and docs, and static checkers can verify your own comparisons against it."
   },
   {
    "t": "Why write `class Track(str, Enum)` rather than `class Track(Enum)`?",
    "o": [
     "It is required by Pydantic",
     "So members compare equal to their strings and serialise as plain text",
     "It is faster",
     "To allow methods"
    ],
    "a": 1,
    "w": "Without the mixin, `Track.MATHS == \"maths\"` is False and json.dumps refuses the member, which breaks any code that does not know the enum exists."
   },
   {
    "t": "What does `model_dump()` return for an enum field, versus `model_dump_json()`?",
    "o": [
     "Both give the value",
     "The member, and the value respectively",
     "Both give the member",
     "It raises"
    ],
    "a": 1,
    "w": "`model_dump()` keeps Python objects, so you get the member. JSON has no enums, so the JSON forms convert to the underlying value."
   },
   {
    "t": "Where is `Literal` not just a preference but the required mechanism?",
    "o": [
     "Any string field",
     "As the tag of a discriminated union",
     "Optional fields",
     "Nested models"
    ],
    "a": 1,
    "w": "The discriminator lookup is built at class-definition time, so the tag value must be known then - which is what Literal provides and a plain str does not."
   }
  ]
 },
 {
  "path": "pydantic/field_constraints.html",
  "title": "Field Constraints",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What does `pattern=r\"[a-z]+\"` accept?",
    "o": [
     "Only all-lowercase strings",
     "Also 'abc123!!!' - it matches from the start but need not reach the end",
     "Nothing",
     "Any string"
    ],
    "a": 1,
    "w": "`pattern` matches from the start rather than requiring the whole string. Without `^...$` anchors it fails permissively, which is how this bug survives longest."
   },
   {
    "t": "A field is `int = Field(gt=0)` and receives `\"5\"`. What happens?",
    "o": [
     "Rejected - it is a string",
     "Coerced to 5, then compared against 0, and accepted",
     "Compared as text",
     "Rejected - gt needs a float"
    ],
    "a": 1,
    "w": "Constraints run after coercion. That is also why the two failure modes have different error types: `int_parsing` versus `greater_than`."
   },
   {
    "t": "Does `Field(gt=0)` with no default make a field optional?",
    "o": [
     "Yes",
     "No - it is still required",
     "Only for ints",
     "It defaults to 0"
    ],
    "a": 1,
    "w": "Requiredness is decided by the presence of a default. `Field` with only constraints supplies no default, so the field stays required."
   },
   {
    "t": "Why write `description=` on a field?",
    "o": [
     "It makes validation stricter",
     "It appears in the generated JSON Schema and therefore in API docs",
     "It is required",
     "It speeds up validation"
    ],
    "a": 1,
    "w": "Metadata changes no behaviour but flows into `model_json_schema()`, which FastAPI renders as documentation. It is the cheapest documentation available."
   }
  ]
 },
 {
  "path": "pydantic/generic_models.html",
  "title": "Generic Models",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Does `Page[Module]` validate its `items`?",
    "o": [
     "No - generics skip validation",
     "Yes, fully, with Module's own rules and normal error paths",
     "Only the length",
     "Only in strict mode"
    ],
    "a": 1,
    "w": "A generic gives reuse, not an escape from checking. Coercion, constraints and error paths all behave exactly as in a non-generic model."
   },
   {
    "t": "Why alias `ModulePage = Page[Module]` at module level?",
    "o": [
     "Required syntax",
     "Each parameterisation builds a real class; the alias names it once and avoids repeating the lookup",
     "It changes validation",
     "For mypy only"
    ],
    "a": 1,
    "w": "`Page[Module]` creates and caches a distinct class. Naming it once is both clearer at every use site and avoids doing the lookup in a hot path."
   },
   {
    "t": "What does `TypeVar(\"T\", bound=Resource)` let you do?",
    "o": [
     "Nothing extra",
     "Write methods on the generic that rely on what Resource guarantees",
     "Skip validation",
     "Allow any type"
    ],
    "a": 1,
    "w": "The bound means every parameterisation is a Resource, so a method can safely use `item.id`. It also documents what the envelope is for."
   },
   {
    "t": "When is a generic the wrong tool?",
    "o": [
     "Always",
     "At two use sites, or when the payload is one of a fixed small set",
     "For paginated responses",
     "With models"
    ],
    "a": 1,
    "w": "Two near-identical classes read better than a generic; the pattern earns its keep around the third. And a fixed small set of payloads is a discriminated union, which says more."
   }
  ]
 },
 {
  "path": "pydantic/json_schema.html",
  "title": "JSON Schema",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What does a `field_validator` contribute to the generated schema?",
    "o": [
     "The rule as a keyword",
     "Nothing - it is invisible to consumers",
     "A description",
     "An example"
    ],
    "a": 1,
    "w": "Arbitrary logic has no schema equivalent. The rule is still enforced, but documentation, generated clients and browser forms know nothing about it - which is why constraints are preferred where they can express the rule."
   },
   {
    "t": "Where do computed fields appear?",
    "o": [
     "The validation schema",
     "The serialization schema only",
     "Both",
     "Neither"
    ],
    "a": 1,
    "w": "They are output-only, so advertising them in an input schema would tell callers to send something that cannot be sent."
   },
   {
    "t": "Why does a nested model appear in `$defs` rather than inline?",
    "o": [
     "To save bytes only",
     "So it is referenced once and becomes a named type in generated clients",
     "It is a bug",
     "Because of recursion limits"
    ],
    "a": 1,
    "w": "A referenced definition becomes one named type used in several places, rather than several anonymous objects that happen to match. It is also what makes recursive models expressible."
   },
   {
    "t": "What do `examples` on a field do?",
    "o": [
     "Change validation",
     "Populate the interactive docs' request form with a working request",
     "Set the default",
     "Nothing"
    ],
    "a": 1,
    "w": "They change no behaviour and flow into the schema, where documentation tools use them to give a first-time caller something that works rather than an empty box."
   }
  ]
 },
 {
  "path": "pydantic/migrating_v1_to_v2.html",
  "title": "Migrating v1 to v2",
  "cat": "Pydantic",
  "q": [
   {
    "t": "In v2, what does `summary: Optional[str]` with no default mean?",
    "o": [
     "Optional, defaults to None as in v1",
     "Required, and may be None",
     "Forbidden",
     "It warns"
    ],
    "a": 1,
    "w": "v1 added the default implicitly; v2 does not. Nothing warns, so code that worked starts raising `missing` at runtime - the largest source of failures in a real migration."
   },
   {
    "t": "What replaced `@root_validator`?",
    "o": [
     "@field_validator",
     "@model_validator with an explicit mode",
     "@validator",
     "Nothing"
    ],
    "a": 1,
    "w": "The mode is now explicit, and an after-validator receives the finished model as `self` rather than a dict of values - so fields are already converted."
   },
   {
    "t": "Which of these dates a tutorial as v1?",
    "o": [
     "model_config",
     "class Config and .dict()",
     "field_validator",
     "TypeAdapter"
    ],
    "a": 1,
    "w": "An inner `class Config`, `.dict()`, `@validator`, `orm_mode` and `min_items` are all v1 vocabulary. Treat the behaviour such a page describes as historical too."
   },
   {
    "t": "Why review error-handling code carefully during a migration?",
    "o": [
     "It is slower in v2",
     "Error type codes were renamed wholesale, and a branch that never matches fails silently",
     "Errors were removed",
     "It is unchanged"
    ],
    "a": 1,
    "w": "Code matching v1 codes or message strings stops matching with no exception raised. This is precisely why the advice throughout is to match on `type` rather than `msg`."
   }
  ]
 },
 {
  "path": "pydantic/nested_models.html",
  "title": "Nested Models",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What is the `loc` for a bad `email` inside a nested `author` field?",
    "o": [
     "('email',)",
     "('author',)",
     "('author', 'email')",
     "It has no loc"
    ],
    "a": 2,
    "w": "`loc` is the full path to the failing value. That is what makes a deeply nested payload debuggable rather than merely rejected."
   },
   {
    "t": "You pass `author=\"Ada\"` where a nested `Author` model is expected. Where does the error point?",
    "o": [
     "At author.name",
     "At the author field itself",
     "At the whole model",
     "Nowhere - it is accepted"
    ],
    "a": 1,
    "w": "A string cannot be read as an Author at all, so the failure is on the field rather than inside it - a different problem from one of Author's own fields being wrong."
   },
   {
    "t": "Why use `Field(default_factory=Author)` rather than `= Author()` for a nested default?",
    "o": [
     "It is faster",
     "`= Author()` is evaluated once at class definition, so every parent would share one instance",
     "They are identical",
     "`= Author()` is a syntax error"
    ],
    "a": 1,
    "w": "The expression runs when the class body runs. A factory is called per instance, which is what a per-parent default needs."
   },
   {
    "t": "How do you exclude one field of a nested model from `model_dump`?",
    "o": [
     "Not possible",
     "exclude={\"author\": {\"email\"}}",
     "exclude=\"author.email\"",
     "Only with a separate model"
    ],
    "a": 1,
    "w": "`include` and `exclude` accept nested dicts to reach inside. For anything more structural than a field or two, a separate output model reads better and appears correctly in the schema."
   }
  ]
 },
 {
  "path": "pydantic/parsing_json.html",
  "title": "Parsing JSON",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What does `model_validate_json` do with malformed JSON?",
    "o": [
     "Raises JSONDecodeError",
     "Raises ValidationError with type json_invalid, including a position",
     "Returns None",
     "Silently ignores it"
    ],
    "a": 1,
    "w": "Syntax failures arrive through the same channel as validation failures, so one handler covers both - and the context names where in the document the problem is."
   },
   {
    "t": "Why is `model_validate_json` more faithful for a `Decimal` field?",
    "o": [
     "It rounds better",
     "json.loads makes a float first, losing precision before validation runs",
     "Decimals are unsupported otherwise",
     "It is not"
    ],
    "a": 1,
    "w": "The direct parser reads the digits as written and can build the Decimal from exact text. Going via Python, the value is already an inexact float when Pydantic sees it."
   },
   {
    "t": "You already have a dict from a database driver. Which method?",
    "o": [
     "model_validate_json",
     "model_validate",
     "Either",
     "TypeAdapter"
    ],
    "a": 1,
    "w": "There is no JSON text to parse. The rule is: text or bytes go to `model_validate_json`, Python objects go to `model_validate`."
   },
   {
    "t": "Where should a `TypeAdapter` be constructed?",
    "o": [
     "Inside the function that uses it",
     "Once at module level",
     "Per request",
     "It does not matter"
    ],
    "a": 1,
    "w": "Constructing one compiles a schema. Doing that inside a loop or per call is a real performance mistake that is easy to miss."
   }
  ]
 },
 {
  "path": "pydantic/performance_and_pydantic_core.html",
  "title": "Performance and pydantic-core",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What are the two pieces of Pydantic v2?",
    "o": [
     "A parser and a serialiser",
     "A Python layer that builds schemas and a Rust core that executes them",
     "Two Python packages",
     "A validator and a model class"
    ],
    "a": 1,
    "w": "Schema building happens once per class in Python; validation runs compiled Rust against that schema. That split is why v2 is fast and why v1 needed a rewrite rather than tuning."
   },
   {
    "t": "Which is faster for validating 4,000 rows?",
    "o": [
     "A comprehension of model_validate",
     "TypeAdapter(List[Model]).validate_python(rows)",
     "Identical",
     "Depends on the model"
    ],
    "a": 1,
    "w": "One call lets the loop happen inside the core. The comprehension crosses between Python and Rust once per row - the most effective one-line change for bulk work."
   },
   {
    "t": "Why is a `field_validator` more expensive than an equivalent `Field` constraint?",
    "o": [
     "It is not",
     "It calls out of the Rust core into Python for every value",
     "It validates twice",
     "It rebuilds the schema"
    ],
    "a": 1,
    "w": "Constraints run inside the compiled core; a validator suspends it to call the interpreter. The constraint also reaches the schema, which is the more important reason to prefer it."
   },
   {
    "t": "How should the timings on this page be read?",
    "o": [
     "As figures for a production server",
     "As ratios only - WebAssembly is several times slower than a native interpreter",
     "As worst cases",
     "They are exact"
    ],
    "a": 1,
    "w": "Relative comparisons under identical conditions transfer; absolute seconds are a property of the machine. That is true of any benchmark, including ones you run yourself."
   }
  ]
 },
 {
  "path": "pydantic/pydantic_vs_dataclasses.html",
  "title": "Pydantic vs Dataclasses",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What does `@dataclass` do with the annotation `minutes: int`?",
    "o": [
     "Checks the value is an int",
     "Converts the value",
     "Uses it only to decide the field exists",
     "Raises if it is wrong"
    ],
    "a": 2,
    "w": "A dataclass reads annotations to discover the fields and generate an `__init__` that assigns them. The types are never checked at runtime."
   },
   {
    "t": "Where does validation genuinely earn its cost?",
    "o": [
     "Everywhere, always",
     "At the boundary where untrusted data arrives",
     "Only in tests",
     "Nowhere - it is too slow"
    ],
    "a": 1,
    "w": "Data crossing into your code is a guess until checked. Past that line it has already been proven, and re-checking the same values buys nothing."
   },
   {
    "t": "You need to validate a bare `List[int]` with no model around it. What do you use?",
    "o": [
     "A one-field wrapper model",
     "TypeAdapter",
     "A dataclass",
     "It cannot be done"
    ],
    "a": 1,
    "w": "`TypeAdapter(List[int])` applies the full machinery to any annotation. The wrapper model is the workaround people use before they discover it."
   },
   {
    "t": "What does `pydantic.dataclasses.dataclass` give you?",
    "o": [
     "Nothing different",
     "The dataclass API with validation added",
     "A faster dataclass",
     "A BaseModel"
    ],
    "a": 1,
    "w": "It is a drop-in that keeps dataclass introspection while validating on construction - useful for adding checks to existing dataclasses without rewriting them as models."
   }
  ]
 },
 {
  "path": "pydantic/pydantic_with_fastapi.html",
  "title": "Pydantic with FastAPI",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What does `response_model` do besides validating the output?",
    "o": [
     "Nothing",
     "Filters it to the declared fields, so undeclared keys cannot leak",
     "Caches it",
     "Sets the status code"
    ],
    "a": 1,
    "w": "A handler returning a dict with `password_hash` produces a response without one. It is a real security property, and more reliable than trusting every future edit of the handler."
   },
   {
    "t": "What is in a FastAPI 422 response body?",
    "o": [
     "A plain string",
     "Essentially `e.errors()` - loc, type, msg and input per failure",
     "Only the first error",
     "Nothing useful"
    ],
    "a": 1,
    "w": "Everything from the errors module applies directly, with `loc` starting at `body`, `path`, `query` or `header` to say which part of the request was wrong."
   },
   {
    "t": "Why separate Create, Update and Out models?",
    "o": [
     "FastAPI requires it",
     "Each says what that endpoint actually accepts or returns; one all-optional model guarantees nothing",
     "It is faster",
     "For nesting"
    ],
    "a": 1,
    "w": "Create excludes server-assigned fields, Update is all-optional for `exclude_unset`, Out declares exactly what may be seen. Collapsing them produces documentation that promises nothing."
   },
   {
    "t": "Where does 'does this track exist?' belong?",
    "o": [
     "A field validator",
     "A model validator",
     "The handler or service layer",
     "response_model"
    ],
    "a": 2,
    "w": "It is a fact about the world, not the shape of the payload - and the right answer is a 404 or 409 rather than a 422. Keeping it out also keeps models testable without a database."
   }
  ]
 },
 {
  "path": "pydantic/reading_a_validation_error.html",
  "title": "Reading a ValidationError",
  "cat": "Pydantic",
  "q": [
   {
    "t": "A payload has four invalid fields. How many exceptions does Pydantic raise?",
    "o": [
     "Four",
     "One, carrying all four",
     "One per model",
     "It stops at the first"
    ],
    "a": 1,
    "w": "Every field is checked and a single `ValidationError` carries the complete list, so a caller can fix everything in one pass."
   },
   {
    "t": "What does `loc` of `('lessons', 1, 'minutes')` mean?",
    "o": [
     "Three separate errors",
     "The minutes field of the item at index 1 in lessons",
     "A field literally named lessons.1.minutes",
     "Line 1 of the file"
    ],
    "a": 1,
    "w": "`loc` is a path. Integers are sequence indices and strings are field names, so this locates one value inside a nested structure."
   },
   {
    "t": "Why match on `type` rather than `msg`?",
    "o": [
     "type is shorter",
     "msg is prose and gets reworded between releases",
     "msg is always empty",
     "There is no difference"
    ],
    "a": 1,
    "w": "Types are stable identifiers; messages are human sentences that may be clarified or translated. Matching on prose breaks quietly on upgrade."
   },
   {
    "t": "What should a custom validator raise to join the same error report?",
    "o": [
     "ValidationError",
     "ValueError",
     "TypeError",
     "Exception"
    ],
    "a": 1,
    "w": "Pydantic catches `ValueError`, wraps it with the field's location and gives it the type `value_error`. Building a `ValidationError` by hand is unnecessary."
   }
  ]
 },
 {
  "path": "pydantic/required_optional_and_defaults.html",
  "title": "Required, Optional and Defaults",
  "cat": "Pydantic",
  "q": [
   {
    "t": "A field is declared `note: Optional[str]` with no default. Is it required?",
    "o": [
     "No - Optional makes it optional",
     "Yes - it is nullable but still required",
     "Only in strict mode",
     "It defaults to None"
    ],
    "a": 1,
    "w": "`Optional[str]` means `str or None`, which is about allowed values. Requiredness is decided by whether a default exists. Pydantic v1 added the default implicitly; v2 deliberately does not."
   },
   {
    "t": "Which tells you whether a caller actually supplied a field?",
    "o": [
     "model_dump()",
     "model_fields_set",
     "model_json_schema()",
     "The field being None"
    ],
    "a": 1,
    "w": "After validation an omitted field and an explicitly null one both read as `None`. `model_fields_set` is the only record of what was actually sent."
   },
   {
    "t": "What does `model_dump(exclude_unset=True)` produce, and why does it matter?",
    "o": [
     "Everything except None",
     "Only fields the caller supplied - the right shape for PATCH",
     "Only required fields",
     "An empty dict"
    ],
    "a": 1,
    "w": "An update that dumps every field will overwrite untouched columns with defaults or None. Excluding unset fields keeps 'not mentioned' meaning 'leave alone'."
   },
   {
    "t": "Why use `default_factory=datetime.now` instead of `= datetime.now()`?",
    "o": [
     "It is faster",
     "The second freezes the time the class was defined",
     "Both are identical",
     "The second is a syntax error"
    ],
    "a": 1,
    "w": "`datetime.now()` is evaluated once, when the class body runs, so every instance would claim the same creation time. A factory is called per instance."
   }
  ]
 },
 {
  "path": "pydantic/settings_management.html",
  "title": "Settings Management",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Why does a required setting with no default matter?",
    "o": [
     "It is faster",
     "The process fails at boot naming the variable, instead of producing a None that fails hours later",
     "It saves memory",
     "It enables caching"
    ],
    "a": 1,
    "w": "Failing before the process claims to be ready is the whole point. A missing variable that becomes None surfaces far from its cause, whenever that code path is first taken."
   },
   {
    "t": "`APP_DEBUG=false` with a `bool` field gives what?",
    "o": [
     "True, because the string is non-empty",
     "False",
     "A ValidationError",
     "None"
    ],
    "a": 1,
    "w": "Pydantic reads the meaning of the word, unlike `bool(os.environ.get(...))` where any non-empty string is truthy. That difference is a classic configuration bug."
   },
   {
    "t": "Why is `env: Literal[\"dev\", \"test\", \"prod\"]` better than `env: str`?",
    "o": [
     "It is faster",
     "ENV=staging fails at boot with the permitted values named, instead of silently taking every else-branch",
     "It uses less memory",
     "No difference"
    ],
    "a": 1,
    "w": "Typos and out-of-range values cause most configuration incidents. A closed set catches them at start-up rather than letting them alter behaviour silently."
   },
   {
    "t": "Why use `SecretStr` in a settings model specifically?",
    "o": [
     "It encrypts the value",
     "A settings object is the thing most likely to be logged or printed at start-up",
     "It is required",
     "It speeds up reading"
    ],
    "a": 1,
    "w": "It is not encryption - it hides the value from repr, logs and tracebacks, and requires `.get_secret_value()` so every real access is deliberate."
   }
  ]
 },
 {
  "path": "pydantic/strict_vs_lax_mode.html",
  "title": "Strict vs Lax Mode",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Why is lax mode the default?",
    "o": [
     "It is faster",
     "Because data at a boundary arrives as text and would otherwise need manual conversion everywhere",
     "For backwards compatibility",
     "It is not - strict is"
    ],
    "a": 1,
    "w": "Query strings, form posts and CSVs contain no integers. Refusing text would put an `int()` call in a try block in front of every model, which is the code the library removes."
   },
   {
    "t": "Does strict mode refuse an `int` for a `float` field?",
    "o": [
     "Yes",
     "No - widening loses nothing, so it is allowed",
     "Only in JSON mode",
     "Only for negatives"
    ],
    "a": 1,
    "w": "Strict removes parsing, not lossless widening. `bool` for an `int` is also still accepted, because bool genuinely is a subclass of int in Python."
   },
   {
    "t": "A strict model validates a `date` field from a JSON string. What happens?",
    "o": [
     "Refused - it is a string",
     "Accepted, because JSON has no date type",
     "Converted silently in all modes",
     "It raises a config error"
    ],
    "a": 1,
    "w": "Strict refuses *unnecessary* conversion. From Python a real date object was available so a string is refused; from JSON the string is the only representation there is."
   },
   {
    "t": "Which field is the classic candidate for `strict=True` in an otherwise lax model?",
    "o": [
     "A description",
     "An identifier or a money amount",
     "An optional note",
     "A title"
    ],
    "a": 1,
    "w": "An id arriving as text usually means something upstream lost a type, and a Decimal accepting a float accepts an already-inexact value. Both are cases where silence hides a real problem."
   }
  ]
 },
 {
  "path": "pydantic/type_adapter.html",
  "title": "TypeAdapter",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Why is `TypeAdapter(List[Lesson])` better than a wrapper model with one list field?",
    "o": [
     "It is the only way",
     "Same validation with no artificial object, and the schema describes an array rather than an object",
     "It is stricter",
     "No real difference"
    ],
    "a": 1,
    "w": "The wrapper exists only to hold the list, forces callers through `.items`, and makes the API document an object where the data is an array."
   },
   {
    "t": "Where should a TypeAdapter be constructed?",
    "o": [
     "Inside the loop",
     "Once at module level",
     "Per request",
     "It makes no difference"
    ],
    "a": 1,
    "w": "Constructing one compiles a schema. Rebuilding it per call is real repeated work and does not look like a performance bug in review."
   },
   {
    "t": "Which validates a thousand rows faster?",
    "o": [
     "A comprehension of model_validate",
     "TypeAdapter(List[Model]).validate_python(rows)",
     "They are identical",
     "Neither validates"
    ],
    "a": 1,
    "w": "One call lets the Rust core do the looping; the comprehension crosses between Python and Rust once per item. It is the most effective single-line optimisation here."
   },
   {
    "t": "When is a model still the better choice than an adapter?",
    "o": [
     "Never",
     "When the thing deserves a name, needs validators or config, or benefits from attribute access",
     "Only for JSON",
     "Only for nested data"
    ],
    "a": 1,
    "w": "Adapters have no class body and hand back plain objects. Models name domain concepts and give validators, config and methods somewhere to live."
   }
  ]
 },
 {
  "path": "pydantic/types_and_coercion.html",
  "title": "Types and Coercion",
  "cat": "Pydantic",
  "q": [
   {
    "t": "A field is `n: int`. What does Pydantic do with the float `9.5`?",
    "o": [
     "Gives 9",
     "Gives 10",
     "Raises a ValidationError",
     "Gives 9.5"
    ],
    "a": 2,
    "w": "Conversion happens only when nothing is lost. `9.0` becomes `9`, but rounding `9.5` would discard information, so it refuses rather than guessing."
   },
   {
    "t": "A field is `s: str`. What happens with the integer `9`?",
    "o": [
     "Gives \"9\"",
     "Raises a ValidationError",
     "Gives 9",
     "Gives None"
    ],
    "a": 1,
    "w": "This is the asymmetry to remember. Text arriving where a number is wanted is normal; a number arriving where text is wanted is usually a real bug in the caller, so it is not hidden."
   },
   {
    "t": "What does a `bool` field do with the string `\"false\"`?",
    "o": [
     "True, because the string is non-empty",
     "False",
     "Raises",
     "None"
    ],
    "a": 1,
    "w": "Pydantic reads the meaning of the word, not the emptiness of the container. Plain Python's `bool(\"false\")` is `True`, which is why query-string parsing needs this behaviour."
   },
   {
    "t": "When is strict mode the right choice?",
    "o": [
     "Always",
     "At the boundary where text arrives",
     "Deep inside a system where types should already be correct",
     "Never"
    ],
    "a": 2,
    "w": "At the boundary, coercion removes conversion code you would otherwise write. Inside, a wrong type is a bug of your own, and silently fixing it hides the bug."
   }
  ]
 },
 {
  "path": "pydantic/unions_and_discriminated_unions.html",
  "title": "Unions and Discriminated Unions",
  "cat": "Pydantic",
  "q": [
   {
    "t": "In smart mode, what does Pydantic try first for a union?",
    "o": [
     "Left to right conversion",
     "An exact type match across all members",
     "The narrowest type",
     "Random order"
    ],
    "a": 1,
    "w": "An exact match wins without any conversion. Only when nothing matches exactly does it fall back to converting left to right, which is where order starts to matter."
   },
   {
    "t": "Two models in a union can both accept `{\"title\": \"x\"}`. What happens?",
    "o": [
     "A ValidationError",
     "The first one that validates wins, by position",
     "Both are returned",
     "The one with more fields wins"
    ],
    "a": 1,
    "w": "This is the dangerous case: no error, just the wrong object. Defaults make it much more likely, since they let a member accept payloads it was never meant for."
   },
   {
    "t": "What does `Field(discriminator=\"kind\")` require of each member?",
    "o": [
     "A str field named kind",
     "A Literal field named kind with a distinct value",
     "Nothing",
     "An Enum"
    ],
    "a": 1,
    "w": "The value must be known at class-definition time so Pydantic can build the tag-to-model lookup, which is what `Literal` provides and a plain `str` does not."
   },
   {
    "t": "Why do discriminated unions produce better errors?",
    "o": [
     "They have shorter messages",
     "Only one branch is attempted, so only its errors are reported",
     "They suppress errors",
     "They validate less"
    ],
    "a": 1,
    "w": "Without a tag, every member is tried and every member's failures are reported. With one, exactly one branch runs, so the report is about the shape the data actually claimed to be."
   }
  ]
 },
 {
  "path": "pydantic/validator_modes.html",
  "title": "Validator Modes",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Your validator turns a CSV string into a list, but it never runs. Why?",
    "o": [
     "A Pydantic bug",
     "It is in after mode, and a string already failed list coercion before it",
     "It needs @classmethod",
     "The field is optional"
    ],
    "a": 1,
    "w": "After validators run at step 4, and coercion failed at step 2. Shape-fixing logic must be in before mode, where the raw value is still available."
   },
   {
    "t": "What does a `plain` validator skip?",
    "o": [
     "Nothing",
     "Coercion and constraints - it replaces validation entirely",
     "Only constraints",
     "Only coercion"
    ],
    "a": 1,
    "w": "It takes over completely. Whatever it returns becomes the field unvalidated, so producing the right type and raising on bad input are both your responsibility."
   },
   {
    "t": "What does a `wrap` validator receive besides the value?",
    "o": [
     "The model",
     "A handler that performs the normal validation",
     "The field name",
     "Nothing"
    ],
    "a": 1,
    "w": "Calling the handler runs standard validation, so a wrap validator can catch its failure and substitute a value, or add context and re-raise."
   },
   {
    "t": "In `Annotated[str, BeforeValidator(to_slug), Field(pattern=p)]`, what is the order?",
    "o": [
     "Pattern, then normaliser",
     "Normaliser, then coercion, then pattern",
     "Both at once",
     "Pattern only"
    ],
    "a": 1,
    "w": "The pipeline is before, coerce, constrain, after. Written the other way the pattern would reject the messy input the normaliser existed to clean."
   }
  ]
 },
 {
  "path": "pydantic/what_is_pydantic.html",
  "title": "What Pydantic Is For",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What does a plain Python type annotation do at runtime?",
    "o": [
     "Rejects wrong types",
     "Converts the value",
     "Nothing",
     "Logs a warning"
    ],
    "a": 2,
    "w": "Annotations are stored and ignored while the program runs. They serve readers, editors and static checkers. Pydantic is one of the tools that chooses to act on them."
   },
   {
    "t": "A model field is annotated `minutes: int` and receives the string `\"9\"`. What happens by default?",
    "o": [
     "ValidationError",
     "It becomes the integer 9",
     "It stays the string \"9\"",
     "It becomes None"
    ],
    "a": 1,
    "w": "Default lax mode converts anything with an unambiguous reading, because data crossing a boundary usually arrives as text. `\"nine\"` would raise, because there is no unambiguous reading."
   },
   {
    "t": "Why does Pydantic report every invalid field rather than stopping at the first?",
    "o": [
     "It is faster",
     "So a caller can fix everything in one pass",
     "To make errors longer",
     "It stops at the first by default"
    ],
    "a": 1,
    "w": "One raise carrying the full list means a form can highlight all its broken inputs at once, instead of revealing them one resubmission at a time."
   },
   {
    "t": "Where does a Pydantic model earn its place?",
    "o": [
     "At the boundary where outside data enters",
     "In every function",
     "Only in tests",
     "In the database layer"
    ],
    "a": 0,
    "w": "Validate once where untrusted data arrives, and everything downstream can assume the shape is correct. Re-checking at every layer costs time and adds no safety."
   }
  ]
 },
 {
  "path": "pydantic/your_first_basemodel.html",
  "title": "Your First BaseModel",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Why does a model refuse positional arguments?",
    "o": [
     "To save memory",
     "Because adding a field would silently change what positional calls mean",
     "Because dicts are unordered",
     "It does not - they work"
    ],
    "a": 1,
    "w": "Models gain fields over time. If position mattered, inserting a field would reassign every existing positional call's values without raising anything."
   },
   {
    "t": "What is the difference between `model_dump()` and `model_dump_json()`?",
    "o": [
     "None",
     "dump gives Python objects, dump_json gives a JSON-safe string",
     "dump_json is deprecated",
     "dump only works on nested models"
    ],
    "a": 1,
    "w": "`model_dump()` keeps Python types like `datetime` intact for use inside your program. `model_dump_json()` converts everything to something JSON can carry, for data that is leaving the process."
   },
   {
    "t": "Two separately created `Module` objects have identical field values. What does `==` return?",
    "o": [
     "False - different objects",
     "True - models compare by value",
     "It raises",
     "Only if you define __eq__"
    ],
    "a": 1,
    "w": "Pydantic generates an `__eq__` that compares field values, which is what makes assertions in tests short."
   },
   {
    "t": "You have a dict from `json.loads`. Which is the better way to build a model from it?",
    "o": [
     "Module(**data)",
     "Module.model_validate(data)",
     "Module.parse(data)",
     "Module.from_dict(data)"
    ],
    "a": 1,
    "w": "Both `Module(**data)` and `model_validate(data)` work, but `model_validate` states that validation is happening and survives keys that are not valid Python identifiers."
   }
  ]
 },
 {
  "path": "pydantic/field_validator.html",
  "title": "field_validator",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What happens if a validator checks a value but forgets to return it?",
    "o": [
     "The original value is kept",
     "The field becomes None",
     "It raises",
     "Validation is skipped"
    ],
    "a": 1,
    "w": "Whatever the validator returns becomes the field, and a function with no return returns None. This fails silently, which is what makes it the most costly mistake with this API."
   },
   {
    "t": "Why must `@classmethod` sit below `@field_validator`?",
    "o": [
     "Style only",
     "Decorators apply bottom-up, so field_validator needs a classmethod to register",
     "It does not matter",
     "classmethod is optional"
    ],
    "a": 1,
    "w": "The inner decorator runs first. Reversed, field_validator receives a plain function and the resulting error does not obviously explain the cause."
   },
   {
    "t": "When is `mode=\"before\"` the right choice?",
    "o": [
     "Always",
     "When fixing the shape of raw input, such as a CSV string that should be a list",
     "For performance",
     "When raising errors"
    ],
    "a": 1,
    "w": "In after mode the value has already been coerced, so a string where a list was expected has already failed. Before mode is the only place to repair the shape."
   },
   {
    "t": "Why prefer `Field(gt=0)` over a validator that checks `v > 0`?",
    "o": [
     "It is faster",
     "The constraint appears in the JSON Schema; the validator is invisible to docs and clients",
     "Validators cannot raise",
     "No difference"
    ],
    "a": 1,
    "w": "Both reject the same values, but only the constraint reaches documentation, generated clients and form builders that read the schema."
   }
  ]
 },
 {
  "path": "pydantic/model_config.html",
  "title": "model_config",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What does a model do by default with a key it did not declare?",
    "o": [
     "Raises",
     "Silently ignores it",
     "Stores it",
     "Warns"
    ],
    "a": 1,
    "w": "The default is `extra=\"ignore\"`. A typo in a key produces no error and no field, so the bug appears later as a value that is inexplicably a default."
   },
   {
    "t": "Is `m.minutes = \"not a number\"` validated by default?",
    "o": [
     "Yes",
     "No - validation happens at construction only",
     "Only for ints",
     "It raises AttributeError"
    ],
    "a": 1,
    "w": "Assignment is plain Python unless `validate_assignment=True` is set. Without it, a model's declared types can quietly stop being true."
   },
   {
    "t": "What does `frozen=True` give you besides blocking assignment?",
    "o": [
     "Faster validation",
     "Hashability, so the model can be a dict key or set member",
     "Automatic caching",
     "Stricter types"
    ],
    "a": 1,
    "w": "Immutability makes the model hashable, which unlocks ordinary Python that mutable models cannot do - and `model_copy(update=...)` still produces modified versions."
   },
   {
    "t": "What is the risk of `from_attributes=True` on an output model?",
    "o": [
     "None",
     "It reads any matching attribute, so undeclared-but-named fields like password_hash can reach the response, and lazy relations get loaded",
     "It is slow",
     "It breaks nesting"
    ],
    "a": 1,
    "w": "It faithfully reads whatever attribute matches a field name, and touching a lazy ORM relationship triggers queries. Output models should list only what may be seen."
   }
  ]
 },
 {
  "path": "pydantic/model_dump_and_model_dump_json.html",
  "title": "model_dump and model_dump_json",
  "cat": "Pydantic",
  "q": [
   {
    "t": "Why does `json.dumps(m.model_dump())` raise TypeError on a date field?",
    "o": [
     "model_dump is broken",
     "model_dump returns real Python objects, which json.dumps cannot encode",
     "Dates are unsupported",
     "It needs an argument"
    ],
    "a": 1,
    "w": "`model_dump()` deliberately preserves Python types. Use `model_dump_json()`, or `model_dump(mode=\"json\")` when something else does the encoding."
   },
   {
    "t": "A PATCH client sends `{\"summary\": null}` to clear a field. Which filter preserves that?",
    "o": [
     "exclude_none",
     "exclude_unset",
     "exclude_defaults",
     "Any of them"
    ],
    "a": 1,
    "w": "`exclude_unset` keeps fields that were supplied, including explicit nulls. `exclude_none` would drop it, silently discarding the instruction to clear the value."
   },
   {
    "t": "What does `Field(exclude=True)` do?",
    "o": [
     "Rejects the field on input",
     "Keeps it out of every serialisation while remaining on the object",
     "Hides it from repr only",
     "Makes it optional"
    ],
    "a": 1,
    "w": "The value is still there and still accessible; it just never appears in a dump. `SecretStr` covers the different risk of the value appearing in logs and tracebacks."
   },
   {
    "t": "Is `model_dump(exclude={\"minutes\"})` valid input to the same model?",
    "o": [
     "Always",
     "Not if minutes is required - the field is now missing",
     "Only in JSON mode",
     "Yes, defaults fill it"
    ],
    "a": 1,
    "w": "An unfiltered dump round-trips, but filtering removes fields the model requires. This matters when a filtered dump is stored and later read back."
   }
  ]
 },
 {
  "path": "pydantic/model_validator.html",
  "title": "model_validator",
  "cat": "Pydantic",
  "q": [
   {
    "t": "What must an `after` model validator return?",
    "o": [
     "Nothing",
     "self",
     "A dict",
     "True"
    ],
    "a": 1,
    "w": "It receives the finished model and must return it. Forgetting is the same silent failure as forgetting to return from a field validator."
   },
   {
    "t": "What is the `loc` of an error raised by a model validator?",
    "o": [
     "The first field",
     "An empty tuple",
     "The model name",
     "It has none"
    ],
    "a": 1,
    "w": "The failure belongs to the object rather than any one field. Handling code that does `loc[0]` will raise IndexError the first time such a rule is added."
   },
   {
    "t": "Why not use `info.data` in a field validator for a cross-field rule?",
    "o": [
     "It is slower",
     "It only exposes fields declared earlier, so reordering the class breaks the rule",
     "It is deprecated",
     "It cannot raise"
    ],
    "a": 1,
    "w": "Fields validate in declaration order. A rule depending on that order is invisible to whoever later reorders the class for readability."
   },
   {
    "t": "Where does 'does this track exist in the database?' belong?",
    "o": [
     "A model validator",
     "A field validator",
     "The service layer, not the model",
     "A constraint"
    ],
    "a": 2,
    "w": "Models check shape and internal consistency using only the data. A validator doing I/O makes the model untestable, turns validation into a network call, and hides a query where nobody expects one."
   }
  ]
 },
 {
  "path": "python/args_and_kwargs.html",
  "title": "*args and **kwargs",
  "cat": "Python",
  "q": [
   {
    "t": "Inside `def f(*args)`, what type is `args`?",
    "o": [
     "A list",
     "A tuple",
     "A dict",
     "A set"
    ],
    "a": 1,
    "w": "A tuple. **kwargs gives a dict; *args gives a tuple, which is immutable and reflects that the arguments are fixed once passed."
   },
   {
    "t": "`volume(*[2, 3, 4])` is the same as what?",
    "o": [
     "volume([2, 3, 4])",
     "volume(2, 3, 4)",
     "volume(24)",
     "A TypeError"
    ],
    "a": 1,
    "w": "At a call site the star spreads the list across the parameters. Without it you would pass one argument - the list itself."
   },
   {
    "t": "Why does the wrapper pattern use both `*args` and `**kwargs`?",
    "o": [
     "To be faster",
     "So it can forward any call without knowing the signature",
     "Because Python requires both",
     "To sort the arguments"
    ],
    "a": 1,
    "w": "Together they capture every positional and keyword argument, so the wrapper forwards whatever it was given to a function whose parameters it does not need to know."
   }
  ]
 },
 {
  "path": "python/booleans_and_comparisons.html",
  "title": "Booleans and Comparisons",
  "cat": "Python",
  "q": [
   {
    "t": "What does bool(\"\") return?",
    "o": [
     "True",
     "False",
     "\"\"",
     "An error"
    ],
    "a": 1,
    "w": "Empty things are falsy: \"\", 0, [], {} and None. Everything else is truthy, which is why `if name:` reads as \"if name is not empty\"."
   },
   {
    "t": "age = 20. What is the value of `age > 18`?",
    "o": [
     "A bool",
     "A string",
     "An int",
     "Nothing - it is a statement"
    ],
    "a": 0,
    "w": "A comparison is an expression that produces a real bool value. You can print it, store it, or pass it around - not only put it in an if."
   },
   {
    "t": "Which operator asks whether two values are equal?",
    "o": [
     "=",
     "==",
     ":=",
     "==="
    ],
    "a": 1,
    "w": "= assigns, == compares. Python raises a SyntaxError if you use = inside an if, which catches the typo early."
   }
  ]
 },
 {
  "path": "python/classes_and_objects.html",
  "title": "Classes and Objects",
  "cat": "Python",
  "q": [
   {
    "t": "What is `self`?",
    "o": [
     "A reserved keyword",
     "The instance the method was called on",
     "The class itself",
     "A copy of the object"
    ],
    "a": 1,
    "w": "It is the instance, passed as the first argument. `a.speak()` is exactly `Dog.speak(a)` - the name self is convention, not syntax."
   },
   {
    "t": "`total = 0` written directly in the class body is:",
    "o": [
     "A separate value per instance",
     "One value shared by every instance",
     "A syntax error",
     "A local variable"
    ],
    "a": 1,
    "w": "It is a class attribute - one object shared by all instances. Per-instance data is assigned to self inside __init__."
   },
   {
    "t": "You print an object and get `<__main__.Point object at 0x...>`. The fix?",
    "o": [
     "Define __init__",
     "Define __repr__",
     "Use str() instead",
     "Rename the class"
    ],
    "a": 1,
    "w": "__repr__ decides how the object shows up when printed or shown in a list. Two lines, and every debug print afterwards is readable."
   }
  ]
 },
 {
  "path": "python/conditional_comprehensions.html",
  "title": "Conditional Comprehensions",
  "cat": "Python",
  "q": [
   {
    "t": "Which position takes an `else`?",
    "o": [
     "The trailing if",
     "The if/else in the expression at the front",
     "Both",
     "Neither"
    ],
    "a": 1,
    "w": "The expression must produce a value for every item, so its else is mandatory. The trailing if is a filter and takes none."
   },
   {
    "t": "`[x for x in xs if c]` and `[a if c else b for x in xs]` differ how?",
    "o": [
     "No difference",
     "The first can drop items; the second always returns one value per item",
     "The second is faster",
     "The first requires a list"
    ],
    "a": 1,
    "w": "Filtering changes how many items come out. Choosing changes what each item becomes, and the count is unchanged."
   },
   {
    "t": "In a comprehension with both, which runs first?",
    "o": [
     "The expression",
     "The filter",
     "They run in parallel",
     "Undefined"
    ],
    "a": 1,
    "w": "The filter runs first, so the expression only ever sees items that passed it - which is what makes filtering out None before comparing safe."
   }
  ]
 },
 {
  "path": "python/conditional_expressions.html",
  "title": "Conditional Expressions",
  "cat": "Python",
  "q": [
   {
    "t": "What does `x = 5 if False` do?",
    "o": [
     "Sets x to None",
     "Sets x to False",
     "Raises SyntaxError",
     "Leaves x unchanged"
    ],
    "a": 2,
    "w": "An expression must produce a value on every path, so the else is mandatory. There is no one-armed conditional expression."
   },
   {
    "t": "`value or 'default'` differs from a conditional expression how?",
    "o": [
     "It is faster",
     "It also replaces 0, '' and other falsy values",
     "It only works on strings",
     "There is no difference"
    ],
    "a": 1,
    "w": "`or` tests truthiness, not presence. If 0 or an empty string is a real value in your data, `or` throws it away silently."
   },
   {
    "t": "Why can a conditional expression go inside an f-string?",
    "o": [
     "f-strings allow statements",
     "Because it is an expression, and f-strings interpolate expressions",
     "It cannot",
     "Only if bracketed"
    ],
    "a": 1,
    "w": "f-strings evaluate expressions in their braces. A four-line if statement is not an expression and cannot appear there."
   }
  ]
 },
 {
  "path": "python/dict_and_set_comprehensions.html",
  "title": "Dict and Set Comprehensions",
  "cat": "Python",
  "q": [
   {
    "t": "What does `{n for n in [1, 2, 2]}` build?",
    "o": [
     "A list",
     "A dict",
     "A set with two items",
     "A set with three items"
    ],
    "a": 2,
    "w": "Braces with no colon build a set, and a set deduplicates: {1, 2}."
   },
   {
    "t": "`{k: v for k, v in [('a', 1), ('a', 2)]}` gives what?",
    "o": [
     "{'a': 1}",
     "{'a': 2}",
     "An error",
     "{'a': [1, 2]}"
    ],
    "a": 1,
    "w": "The later duplicate key silently overwrites the earlier value. Nothing warns you, which matters when the input might have duplicates."
   },
   {
    "t": "How do you write an empty set comprehension result's type literal?",
    "o": [
     "{}",
     "set()",
     "{,}",
     "[]"
    ],
    "a": 1,
    "w": "{} is an empty dict. There is no empty-set literal, so set() is the only way to write one."
   }
  ]
 },
 {
  "path": "python/dictionaries.html",
  "title": "Dictionaries",
  "cat": "Python",
  "q": [
   {
    "t": "person = {\"name\": \"Ada\"}. What does person[\"age\"] do?",
    "o": [
     "Returns None",
     "Returns \"\"",
     "Raises KeyError",
     "Creates the key"
    ],
    "a": 2,
    "w": "Square brackets on a missing key raise KeyError. Assigning to a missing key creates it, but reading one does not."
   },
   {
    "t": "What does person.get(\"age\", 0) return when there is no age key?",
    "o": [
     "0",
     "None",
     "KeyError",
     "\"age\""
    ],
    "a": 0,
    "w": "get() takes an optional fallback and returns it instead of raising. With no fallback given it returns None."
   },
   {
    "t": "Looping with `for x in person:` gives you:",
    "o": [
     "The keys",
     "The values",
     "Key-value pairs",
     "Nothing"
    ],
    "a": 0,
    "w": "Iterating a dictionary yields its keys. Use .items() when you want both halves, or .values() for just the values."
   }
  ]
 },
 {
  "path": "python/dictionary_methods.html",
  "title": "Dictionary Methods",
  "cat": "Python",
  "q": [
   {
    "t": "What does `d.get('missing')` return?",
    "o": [
     "KeyError",
     "None",
     "An empty string",
     "0"
    ],
    "a": 1,
    "w": "get returns None for a missing key, or whatever default you pass as the second argument. Square brackets raise instead."
   },
   {
    "t": "`teams.setdefault(k, []).append(x)` does what?",
    "o": [
     "Only works if k exists",
     "Gets the list at k, creating an empty one first if absent, then appends",
     "Replaces the value at k",
     "Raises if k is missing"
    ],
    "a": 1,
    "w": "setdefault returns the existing value, inserting the default first when the key is absent - which is the grouping idiom."
   },
   {
    "t": "`for k in d` iterates over what?",
    "o": [
     "Keys",
     "Values",
     "Key-value pairs",
     "Nothing"
    ],
    "a": 0,
    "w": "Plain iteration gives keys. Use d.items() for pairs and d.values() for values."
   }
  ]
 },
 {
  "path": "python/files_and_with.html",
  "title": "Files and with",
  "cat": "Python",
  "q": [
   {
    "t": "What does `with` do for a file?",
    "o": [
     "Makes reading faster",
     "Closes it when the block ends, even on an exception",
     "Locks it",
     "Creates it if missing"
    ],
    "a": 1,
    "w": "Guaranteed cleanup is the point. Without it you need a try/finally, and a forgotten close leaves buffered writes unflushed."
   },
   {
    "t": "Opening an existing file with mode \"w\" does what?",
    "o": [
     "Appends to it",
     "Truncates it immediately",
     "Raises an error",
     "Reads it"
    ],
    "a": 1,
    "w": "\"w\" empties the file the moment it opens, before any write. Use \"a\" to add to a file."
   },
   {
    "t": "Why iterate `for line in f` rather than use readlines()?",
    "o": [
     "It is the only way",
     "It holds one line in memory instead of the whole file",
     "readlines is deprecated",
     "It strips newlines"
    ],
    "a": 1,
    "w": "Iterating streams the file a line at a time, so it works on files larger than memory."
   }
  ]
 },
 {
  "path": "python/for_loops_and_range.html",
  "title": "For Loops and range()",
  "cat": "Python",
  "q": [
   {
    "t": "What does range(5) produce?",
    "o": [
     "1,2,3,4,5",
     "0,1,2,3,4",
     "0,1,2,3,4,5",
     "5"
    ],
    "a": 1,
    "w": "range stops BEFORE its endpoint, giving five numbers starting at 0. That lines up with zero-based indexing."
   },
   {
    "t": "You want a running total. Where does `total = 0` belong?",
    "o": [
     "Before the loop",
     "Inside the loop body",
     "After the loop",
     "It does not matter"
    ],
    "a": 0,
    "w": "Inside the body it resets on every pass, so the final answer is just the last item. The loop runs, no error appears, and the number is quietly wrong."
   },
   {
    "t": "Can you loop over a string with a for loop?",
    "o": [
     "Yes - it yields characters",
     "No - only lists work",
     "Only with range()",
     "Only if you call list() first"
    ],
    "a": 0,
    "w": "Strings are iterable, so a for loop walks them one character at a time."
   }
  ]
 },
 {
  "path": "python/function_arguments.html",
  "title": "Function Arguments",
  "cat": "Python",
  "q": [
   {
    "t": "When is a default argument value evaluated?",
    "o": [
     "On every call",
     "Once, when the function is defined",
     "The first time the function is called",
     "When the module is imported and again per call"
    ],
    "a": 1,
    "w": "Once, at definition time. That single fact is what makes a mutable default accumulate across calls."
   },
   {
    "t": "What is the fix for `def f(items=[])`?",
    "o": [
     "Use a tuple instead",
     "Default to None and build the list inside",
     "Copy the list at the end",
     "Nothing - it is fine"
    ],
    "a": 1,
    "w": "None is immutable so nothing accumulates, and the fresh list is created inside the call where it belongs."
   },
   {
    "t": "Which call is a syntax error?",
    "o": [
     "f('a', b=2)",
     "f(a='a', b=2)",
     "f(b=2, 'a')",
     "f('a', 2)"
    ],
    "a": 2,
    "w": "Positional arguments must come before keyword ones; otherwise Python cannot work out which parameter the positional value was meant for."
   }
  ]
 },
 {
  "path": "python/functions_and_return.html",
  "title": "Functions and Return Values",
  "cat": "Python",
  "q": [
   {
    "t": "A function that prints but never returns gives its caller:",
    "o": [
     "The printed value",
     "None",
     "An empty string",
     "An error"
    ],
    "a": 1,
    "w": "Printing puts characters on the screen; returning hands a value back. Without a return the call evaluates to None, which is why adding to the result raises TypeError."
   },
   {
    "t": "In `def area(width, height):`, width and height are:",
    "o": [
     "Arguments",
     "Parameters",
     "Return values",
     "Globals"
    ],
    "a": 1,
    "w": "The names in the def line are parameters. The values you pass when calling are the arguments."
   },
   {
    "t": "What does `def greet(name, greeting=\"Hello\")` let you do?",
    "o": [
     "Call greet with one argument",
     "Call greet with none",
     "Return two values",
     "Skip the return"
    ],
    "a": 0,
    "w": "A default makes that parameter optional, so greet(\"Ada\") works and greet(\"Ada\", \"Hi\") overrides it."
   }
  ]
 },
 {
  "path": "python/generators_and_yield.html",
  "title": "Generators and yield",
  "cat": "Python",
  "q": [
   {
    "t": "What does calling a generator function do?",
    "o": [
     "Runs the body and returns a list",
     "Returns a generator without running the body",
     "Raises unless you use next()",
     "Runs the body up to the first yield"
    ],
    "a": 1,
    "w": "It builds a generator object. Nothing inside runs until a value is requested."
   },
   {
    "t": "`list(g)` twice on the same generator gives what the second time?",
    "o": [
     "The same values",
     "An empty list",
     "An error",
     "Half the values"
    ],
    "a": 1,
    "w": "A generator walks forward once and is then exhausted. Call the function again for a fresh one."
   },
   {
    "t": "How does `(x*x for x in nums)` differ from `[x*x for x in nums]`?",
    "o": [
     "No difference",
     "It produces values on demand instead of building a list",
     "It is a tuple",
     "It sorts the result"
    ],
    "a": 1,
    "w": "Round brackets make a generator expression: nothing is built, and values are produced as they are asked for."
   }
  ]
 },
 {
  "path": "python/hello_python.html",
  "title": "Hello, Python!",
  "cat": "Python",
  "q": [
   {
    "t": "What does print(\"Hello\") send to the screen?",
    "o": [
     "Hello",
     "\"Hello\" with quotes",
     "Hello\\n",
     "Nothing"
    ],
    "a": 0,
    "w": "print() writes the value, not its source text. The quotes are part of the code that made the string; they are not part of the string."
   },
   {
    "t": "print(2 + 3) prints:",
    "o": [
     "2 + 3",
     "\"2 + 3\"",
     "5",
     "23"
    ],
    "a": 2,
    "w": "Python evaluates the expression before printing, so print(2 + 3) is exactly print(5)."
   },
   {
    "t": "A program is just:",
    "o": [
     "A text file of instructions the interpreter reads top to bottom",
     "A compiled binary",
     "A list of files",
     "A single function"
    ],
    "a": 0,
    "w": "Python reads your .py file from top to bottom and runs each statement in turn. That ordering matters - a line can use a name only after the line that defined it."
   }
  ]
 },
 {
  "path": "python/if_elif_else.html",
  "title": "If, Elif and Else",
  "cat": "Python",
  "q": [
   {
    "t": "score = 95, and the branches check >= 70, then >= 80, then >= 90 in that order. What prints?",
    "o": [
     "The >= 90 branch",
     "The >= 70 branch",
     "All three",
     "Nothing"
    ],
    "a": 1,
    "w": "Only the FIRST true branch runs. 95 satisfies >= 70, so that one wins and the rest are skipped - which is why specific conditions must come before general ones."
   },
   {
    "t": "What decides which lines belong to an if branch?",
    "o": [
     "Curly braces",
     "The indentation",
     "A blank line",
     "The end keyword"
    ],
    "a": 1,
    "w": "Python uses indentation as real syntax. Moving a line in or out by four spaces genuinely changes which branch it belongs to."
   },
   {
    "t": "How many else clauses can one if statement have?",
    "o": [
     "As many as you like",
     "Exactly one",
     "At most one",
     "None"
    ],
    "a": 2,
    "w": "else is optional, and there can be at most one. elif is the clause you can repeat."
   }
  ]
 },
 {
  "path": "python/inheritance.html",
  "title": "Inheritance",
  "cat": "Python",
  "q": [
   {
    "t": "What happens if a subclass __init__ does not call super().__init__()?",
    "o": [
     "Python calls it automatically",
     "The parent's setup never runs",
     "It raises immediately",
     "The subclass cannot be instantiated"
    ],
    "a": 1,
    "w": "The subclass __init__ replaces the parent's entirely. Attributes the parent would have set are simply missing, and you find out later via AttributeError."
   },
   {
    "t": "Why can `describe()` on the parent call the child's `speak()`?",
    "o": [
     "It cannot",
     "Method lookup starts on the actual object's class",
     "describe is copied into each child",
     "Only with super()"
    ],
    "a": 1,
    "w": "Lookup starts at the instance's own class, so the override is found first. That is what lets a parent method work for every subclass."
   },
   {
    "t": "A Car has an Engine. Should Car inherit from Engine?",
    "o": [
     "Yes",
     "No - that is a has-a relationship, so hold one as an attribute",
     "Only if Engine has no __init__",
     "Yes, for speed"
    ],
    "a": 1,
    "w": "Inheritance is for is-a. Composition - holding the object as an attribute - is easier to change and does not tie the two classes together."
   }
  ]
 },
 {
  "path": "python/list_comprehensions.html",
  "title": "List Comprehensions",
  "cat": "Python",
  "q": [
   {
    "t": "Where does the filtering `if` go in a comprehension?",
    "o": [
     "Before the expression",
     "At the end, after the for clause",
     "Anywhere",
     "Comprehensions cannot filter"
    ],
    "a": 1,
    "w": "The trailing `if` filters. An `if/else` that chooses between two values goes in the expression at the front instead - a different job in a different place."
   },
   {
    "t": "What does `(n * n for n in nums)` create?",
    "o": [
     "A list",
     "A tuple",
     "A generator",
     "A set"
    ],
    "a": 2,
    "w": "Round brackets make a generator expression, which produces values one at a time instead of building the whole result in memory."
   },
   {
    "t": "In `[n for row in grid for n in row]`, which loop is the outer one?",
    "o": [
     "`for n in row`",
     "`for row in grid`",
     "They run in parallel",
     "Neither - it is not a nested loop"
    ],
    "a": 1,
    "w": "The clauses appear in the same order as the nested loops: the first for is the outer one."
   }
  ]
 },
 {
  "path": "python/lists_and_indexing.html",
  "title": "Lists and Indexing",
  "cat": "Python",
  "q": [
   {
    "t": "colours = [\"red\", \"green\", \"blue\"]. What is colours[1]?",
    "o": [
     "\"red\"",
     "\"green\"",
     "\"blue\"",
     "An error"
    ],
    "a": 1,
    "w": "Indexes count from 0, so index 1 is the SECOND item. Read an index as \"how far from the start\" and this stops being a trap."
   },
   {
    "t": "That same three-item list. What does colours[3] do?",
    "o": [
     "Returns \"blue\"",
     "Returns None",
     "Raises IndexError",
     "Adds a fourth item"
    ],
    "a": 2,
    "w": "Three items occupy indexes 0, 1 and 2. Asking for 3 is out of range, and Python raises rather than inventing a value."
   },
   {
    "t": "After nums = [3, 1, 2] and sorted(nums), what is nums?",
    "o": [
     "[1, 2, 3]",
     "[3, 1, 2]",
     "None",
     "An error"
    ],
    "a": 1,
    "w": "sorted() returns a NEW sorted list and leaves the original alone. nums.sort() is the one that reorders in place - and it returns None, which is where the confusion usually starts."
   }
  ]
 },
 {
  "path": "python/modules_and_import.html",
  "title": "Modules and import",
  "cat": "Python",
  "q": [
   {
    "t": "What is the main problem with `from module import *`?",
    "o": [
     "It is slow",
     "It hides where names came from and can silently overwrite yours",
     "It only works once",
     "It cannot import functions"
    ],
    "a": 1,
    "w": "Names appear from nowhere, and a clash replaces your own definition with no warning at all."
   },
   {
    "t": "What does `import math` put in your namespace?",
    "o": [
     "Every function in math",
     "The name math only",
     "sqrt and pi",
     "Nothing"
    ],
    "a": 1,
    "w": "Just the module object. Its contents stay behind the math. prefix, which is what makes the origin of a call obvious."
   },
   {
    "t": "Importing the same module twice does what?",
    "o": [
     "Runs it twice",
     "Uses the cached module - it runs once",
     "Raises an error",
     "Doubles memory"
    ],
    "a": 1,
    "w": "Python caches modules in sys.modules, so top-level code runs exactly once per program."
   }
  ]
 },
 {
  "path": "python/mutability_and_aliasing.html",
  "title": "Mutability and Aliasing",
  "cat": "Python",
  "q": [
   {
    "t": "After `a = [1]; b = a; b.append(2)`, what is `a`?",
    "o": [
     "[1]",
     "[1, 2]",
     "[2]",
     "An error"
    ],
    "a": 1,
    "w": "b = a creates a second name for one list, not a copy. The append is visible through both names."
   },
   {
    "t": "A function does `items = [9]`. What does the caller see?",
    "o": [
     "Its list becomes [9]",
     "No change - only the local name was rebound",
     "An error",
     "Its list is emptied"
    ],
    "a": 1,
    "w": "Rebinding points the local name at a new object. Only mutating the original object is visible to the caller."
   },
   {
    "t": "Why does `[[0]*3]*3` misbehave?",
    "o": [
     "It creates 9 separate zeros",
     "The outer multiplication repeats one inner list by reference",
     "It is a syntax error",
     "It does not - it works fine"
    ],
    "a": 1,
    "w": "There is one inner list with three references to it, so writing to one row appears to write to all three."
   }
  ]
 },
 {
  "path": "python/nested_conditionals.html",
  "title": "Nested Conditionals",
  "cat": "Python",
  "q": [
   {
    "t": "`if a:` containing only `if b:` with no else is the same as what?",
    "o": [
     "if a or b:",
     "if a and b:",
     "if not a:",
     "Nothing - it cannot be flattened"
    ],
    "a": 1,
    "w": "Both conditions must hold and nothing else happens, so `and` says it in one line at one indentation level."
   },
   {
    "t": "What is a guard clause?",
    "o": [
     "A try/except around the function",
     "An early return that handles one case and leaves",
     "A nested if",
     "A type check"
    ],
    "a": 1,
    "w": "It handles a refusal immediately and returns, so the remainder of the function is not indented inside an else."
   },
   {
    "t": "How does an `elif` chain differ from nested ifs?",
    "o": [
     "It is faster",
     "It is one decision at one indentation level, not a tree",
     "It cannot have an else",
     "It only works on numbers"
    ],
    "a": 1,
    "w": "elif expresses several mutually exclusive outcomes of a single decision. Nesting expresses decisions that live inside other decisions."
   }
  ]
 },
 {
  "path": "python/nested_data_structures.html",
  "title": "Nested Data Structures",
  "cat": "Python",
  "q": [
   {
    "t": "`people[0]['langs'][1]` reads as:",
    "o": [
     "key, index, key",
     "index, key, index",
     "three indexes",
     "three keys"
    ],
    "a": 1,
    "w": "Left to right: index the list of people, look up the langs key, then index that list."
   },
   {
    "t": "Why use `.get('user', {})` rather than `.get('user')` in a chain?",
    "o": [
     "It is faster",
     "So the next .get has a dict to call rather than None",
     "It avoids typing",
     "There is no difference"
    ],
    "a": 1,
    "w": "None has no .get method, so the chain would raise AttributeError. An empty dict keeps the chain valid."
   },
   {
    "t": "What does `[x for row in rows for x in row]` do?",
    "o": [
     "Filters rows",
     "Flattens a list of lists",
     "Sorts the rows",
     "Counts items"
    ],
    "a": 1,
    "w": "The clauses are in the same order as nested loops: take each row, then each item in it, producing one flat list."
   }
  ]
 },
 {
  "path": "python/nested_for_loops.html",
  "title": "Nested For Loops",
  "cat": "Python",
  "q": [
   {
    "t": "Two loops nested over the same 500-item list. How many inner bodies run?",
    "o": [
     "500",
     "1,000",
     "250,000",
     "It depends on the data"
    ],
    "a": 2,
    "w": "500 outer passes, each running 500 inner passes: 500 x 500 = 250,000. Nesting multiplies."
   },
   {
    "t": "A `break` in the inner loop of a nested pair does what?",
    "o": [
     "Leaves both loops",
     "Leaves the inner loop only",
     "Skips to the next inner item",
     "Raises an error"
    ],
    "a": 1,
    "w": "break leaves the loop containing it. The outer loop carries on with its next pass, which surprises people expecting to be out of both."
   },
   {
    "t": "You double the size of the input to a doubly-nested loop. The work:",
    "o": [
     "Doubles",
     "Quadruples",
     "Stays the same",
     "Grows by 2 bodies"
    ],
    "a": 1,
    "w": "n squared: doubling n gives (2n) squared = 4 n squared. That is why nested loops are the first thing to look at when something is slow."
   }
  ]
 },
 {
  "path": "python/none_and_truthiness.html",
  "title": "None and Truthiness",
  "cat": "Python",
  "q": [
   {
    "t": "Which of these is truthy?",
    "o": [
     "0",
     "''",
     "'0'",
     "[]"
    ],
    "a": 2,
    "w": "'0' is a non-empty string, so it is True. Only the empty string is falsy - which bites when reading text input."
   },
   {
    "t": "A function returns an index or None. Why is `if not result` a bug?",
    "o": [
     "It is slower",
     "Index 0 is falsy, so a real result is treated as missing",
     "not cannot be used on integers",
     "It raises on None"
    ],
    "a": 1,
    "w": "0 and None both take the false branch, so finding something at the first position reports as not found. Nothing raises; the answer is just wrong."
   },
   {
    "t": "Why `is None` rather than `== None`?",
    "o": [
     "They are identical",
     "There is one None object, so identity is exact and cannot be overridden",
     "`==` is deprecated",
     "`is` works on more types"
    ],
    "a": 1,
    "w": "None is a singleton, so identity is the precise test. A class can define __eq__ to make == None true for something that is not None."
   }
  ]
 },
 {
  "path": "python/numbers_and_operators.html",
  "title": "Numbers and Operators",
  "cat": "Python",
  "q": [
   {
    "t": "7 / 2 in Python 3 gives:",
    "o": [
     "3",
     "3.5",
     "3 remainder 1",
     "An error"
    ],
    "a": 1,
    "w": "Python 3's / is true division and always returns a float when the division is not exact. The old integer-truncating behaviour lives on as //."
   },
   {
    "t": "7 % 3 evaluates to:",
    "o": [
     "2",
     "1",
     "2.33",
     "7"
    ],
    "a": 1,
    "w": "The modulo operator returns the remainder after division: 7 = 2×3 + 1, so 7 % 3 is 1. It is the operator behind 'is n even?' checks and clock arithmetic."
   },
   {
    "t": "2 ** 10 evaluates to:",
    "o": [
     "20",
     "1024",
     "12",
     "200"
    ],
    "a": 1,
    "w": "** is exponentiation, not multiplication. 2 ** 10 means 2 raised to the power 10, which is 1024."
   }
  ]
 },
 {
  "path": "python/reading_errors.html",
  "title": "Reading Errors and Tracebacks",
  "cat": "Python",
  "q": [
   {
    "t": "Which line of a traceback names the actual problem?",
    "o": [
     "The first",
     "The last",
     "The middle",
     "It varies"
    ],
    "a": 1,
    "w": "Read bottom-up. The last line is the error type and a plain-English description; the line above it points at your code."
   },
   {
    "t": "print(totl) when you meant total raises:",
    "o": [
     "TypeError",
     "ValueError",
     "NameError",
     "SyntaxError"
    ],
    "a": 2,
    "w": "NameError means Python has never seen that name. It is almost always a typo or a variable used before it was assigned."
   },
   {
    "t": "int(\"twelve\") raises ValueError rather than TypeError because:",
    "o": [
     "The type is wrong",
     "The type is right but the value is not",
     "int takes no arguments",
     "Strings cannot be converted"
    ],
    "a": 1,
    "w": "int() accepts strings, so the type is fine - but \"twelve\" is not a string that represents a number. Right type, impossible value."
   }
  ]
 },
 {
  "path": "python/sets_and_set_operations.html",
  "title": "Sets and Set Operations",
  "cat": "Python",
  "q": [
   {
    "t": "What does `{}` create?",
    "o": [
     "An empty set",
     "An empty dictionary",
     "An empty tuple",
     "A syntax error"
    ],
    "a": 1,
    "w": "Dictionaries claimed the braces first. An empty set is written `set()`."
   },
   {
    "t": "Why is `x in big_set` so much faster than `x in big_list`?",
    "o": [
     "Sets are stored sorted",
     "A set jumps straight to a slot from the hash; a list must scan",
     "Sets are held in memory, lists on disk",
     "It is not faster"
    ],
    "a": 1,
    "w": "The hash tells the set roughly where the item would live, so it checks one place. A list has no such shortcut and compares elements one by one."
   },
   {
    "t": "`{\"a\", \"b\"} ^ {\"b\", \"c\"}` gives what?",
    "o": [
     "{'b'}",
     "{'a', 'c'}",
     "{'a', 'b', 'c'}",
     "set()"
    ],
    "a": 1,
    "w": "`^` is symmetric difference: everything in exactly one of the two sets. 'b' is in both, so it is excluded."
   }
  ]
 },
 {
  "path": "python/shallow_and_deep_copy.html",
  "title": "Shallow vs Deep Copying",
  "cat": "Python",
  "q": [
   {
    "t": "After a shallow copy of `[[1, 2]]`, changing `copy[0][0]`:",
    "o": [
     "Changes only the copy",
     "Changes the original too",
     "Raises an error",
     "Creates a new inner list"
    ],
    "a": 1,
    "w": "The outer list is new but the inner list is shared, so a change one level down is visible through both."
   },
   {
    "t": "When is a shallow copy sufficient?",
    "o": [
     "Always",
     "When everything inside is immutable",
     "Never",
     "Only for dicts"
    ],
    "a": 1,
    "w": "With immutable contents there is nothing shared that can change, so the shallow copy behaves like a complete one."
   },
   {
    "t": "Which of these is NOT a shallow copy of a list?",
    "o": [
     "nums[:]",
     "list(nums)",
     "nums.copy()",
     "copy.deepcopy(nums)"
    ],
    "a": 3,
    "w": "deepcopy rebuilds every mutable object inside as well. The other three duplicate only the outer list."
   }
  ]
 },
 {
  "path": "python/slicing_step_negatives.html",
  "title": "Slicing with Step",
  "cat": "Python",
  "q": [
   {
    "t": "What is `'abcdef'[1:4]`?",
    "o": [
     "'abcd'",
     "'bcd'",
     "'bcde'",
     "'bc'"
    ],
    "a": 1,
    "w": "Start at index 1, stop before index 4: characters 1, 2 and 3."
   },
   {
    "t": "What does `s[::-1]` do?",
    "o": [
     "Removes the last item",
     "Reverses the sequence",
     "Takes every second item",
     "Raises an error"
    ],
    "a": 1,
    "w": "A step of -1 walks the whole sequence backwards. It is the standard reverse idiom."
   },
   {
    "t": "`s[99]` raises IndexError but `s[2:99]` does not. Why?",
    "o": [
     "Slices clamp to what exists",
     "s[2:99] also raises",
     "Slices are cached",
     "99 is special"
    ],
    "a": 0,
    "w": "A slice returns whatever part of the range exists, possibly nothing. Indexing demands that exact position, so it raises."
   }
  ]
 },
 {
  "path": "python/string_methods.html",
  "title": "String Methods",
  "cat": "Python",
  "q": [
   {
    "t": "After `name = 'ana'` then `name.upper()`, what is name?",
    "o": [
     "'ANA'",
     "'ana'",
     "None",
     "An error"
    ],
    "a": 1,
    "w": "Strings are immutable. The method returned a new string that was discarded; the original is untouched. You have to rebind."
   },
   {
    "t": "What does `'banana'.strip('ab')` remove?",
    "o": [
     "The substring 'ab'",
     "Any leading or trailing a or b characters",
     "All a and b anywhere",
     "Nothing"
    ],
    "a": 1,
    "w": "The argument is a set of characters trimmed from both ends, not a substring. removesuffix is the method for removing an ending."
   },
   {
    "t": "`', '.join([1, 2])` does what?",
    "o": [
     "Returns '1, 2'",
     "Raises TypeError",
     "Returns [1, 2]",
     "Returns '12'"
    ],
    "a": 1,
    "w": "join works on strings only. Convert first: ', '.join(str(n) for n in nums)."
   }
  ]
 },
 {
  "path": "python/strings_and_slicing.html",
  "title": "Strings and Slicing",
  "cat": "Python",
  "q": [
   {
    "t": "len(\"hello\") returns:",
    "o": [
     "4",
     "5",
     "6",
     "An error"
    ],
    "a": 1,
    "w": "len() counts characters. \"hello\" has five of them. It counts spaces too - len(\"a b\") is 3."
   },
   {
    "t": "s = \"python\"; s[0] is:",
    "o": [
     "\"p\"",
     "\"y\"",
     "\"t\"",
     "\"n\""
    ],
    "a": 0,
    "w": "Indexing starts at 0 in Python, not 1. s[0] is the first character, and s[-1] is a convenient way to reach the last one."
   },
   {
    "t": "\"hello\".upper() returns:",
    "o": [
     "\"HELLO\"",
     "\"hello\"",
     "5",
     "An error"
    ],
    "a": 0,
    "w": "Strings are objects with methods, and most return a NEW string rather than editing the one in place - \"hello\" is unchanged after the call."
   }
  ]
 },
 {
  "path": "python/tuples_and_unpacking.html",
  "title": "Tuples and Unpacking",
  "cat": "Python",
  "q": [
   {
    "t": "Why can a tuple be a dictionary key when a list cannot?",
    "o": [
     "Tuples are smaller",
     "Tuples are hashable because they cannot change",
     "Lists are too slow",
     "Dictionaries only accept brackets"
    ],
    "a": 1,
    "w": "A key must hash to the same value forever. A list can change after insertion, so the dictionary would look in the wrong place; Python prevents that by making lists unhashable."
   },
   {
    "t": "What is `type((5))`?",
    "o": [
     "tuple",
     "int",
     "list",
     "SyntaxError"
    ],
    "a": 1,
    "w": "The comma makes a tuple, not the brackets. `(5)` is just 5 in brackets; `(5,)` is a one-element tuple."
   },
   {
    "t": "In `a, b = b, a`, why is no temporary variable needed?",
    "o": [
     "Python swaps in place",
     "The right side becomes a tuple first, then is unpacked",
     "Assignment happens left to right",
     "It only works for numbers"
    ],
    "a": 1,
    "w": "Python evaluates the whole right-hand side into a tuple before assigning anything, so both old values are safely captured."
   }
  ]
 },
 {
  "path": "python/type_conversion.html",
  "title": "Type Conversion",
  "cat": "Python",
  "q": [
   {
    "t": "What does `int(\"3.9\")` do?",
    "o": [
     "Returns 3",
     "Returns 4",
     "Raises ValueError",
     "Returns 3.9"
    ],
    "a": 2,
    "w": "From a string, int refuses anything that is not a whole number. From a float, int(3.9) truncates to 3 - the two behave differently on purpose."
   },
   {
    "t": "`round(2.5)` returns what?",
    "o": [
     "3",
     "2",
     "2.5",
     "An error"
    ],
    "a": 1,
    "w": "Python rounds a tie to the nearest even number, which avoids biasing a long run of values upward. round(3.5) is 4."
   },
   {
    "t": "`bool(\"0\")` is:",
    "o": [
     "False",
     "True",
     "An error",
     "0"
    ],
    "a": 1,
    "w": "Only an empty string is falsy. \"0\" has a character in it, so it is True - a classic bug when reading text input."
   }
  ]
 },
 {
  "path": "python/variable_scope.html",
  "title": "Variable Scope",
  "cat": "Python",
  "q": [
   {
    "t": "What order does Python search for a name?",
    "o": [
     "Global, Local, Builtin, Enclosing",
     "Local, Enclosing, Global, Builtin",
     "Builtin, Global, Enclosing, Local",
     "Local, Global only"
    ],
    "a": 1,
    "w": "LEGB. The first match wins, which is why shadowing a builtin like `list` quietly changes what that name means for the rest of the scope."
   },
   {
    "t": "Why does reading `x` before `x = 1` inside a function raise?",
    "o": [
     "x was never defined anywhere",
     "The assignment makes x local for the whole function",
     "print runs before assignment",
     "It does not raise"
    ],
    "a": 1,
    "w": "Python decides at compile time that an assigned name is local for the entire function, so the earlier read refers to a local that has no value yet."
   },
   {
    "t": "`items.append(1)` inside a function affects the outer list. Why no `global`?",
    "o": [
     "append is special",
     "It mutates the object rather than rebinding the name",
     "Lists are always global",
     "It does not actually affect it"
    ],
    "a": 1,
    "w": "Only assignment creates a local name. Mutating the object the name already points at needs no declaration."
   }
  ]
 },
 {
  "path": "python/variables_and_types.html",
  "title": "Variables and Types",
  "cat": "Python",
  "q": [
   {
    "t": "x = \"10\" makes x:",
    "o": [
     "The number 10",
     "The string \"10\"",
     "An error",
     "A list"
    ],
    "a": 1,
    "w": "Python guesses the type from the value. 10 with quotes is a string; without them it is an integer, and the two behave completely differently even though they look alike."
   },
   {
    "t": "Which of these is NOT a built-in Python type?",
    "o": [
     "int",
     "str",
     "list",
     "integer"
    ],
    "a": 3,
    "w": "The type is spelled int, not integer. Being able to ask type(x) and read the answer is a core skill on this track."
   },
   {
    "t": "You reuse a variable name for a new value. The old value:",
    "o": [
     "Still exists under that name",
     "Is gone from that name (unless something else still references it)",
     "Moves to another variable automatically",
     "Causes an error"
    ],
    "a": 1,
    "w": "A name is a label pointing at a value. Rebinding it points the label at something else; the old value is discarded once nothing references it. Names do not hold values, they label them."
   }
  ]
 },
 {
  "path": "python/while_loops_and_control.html",
  "title": "While Loops, break and continue",
  "cat": "Python",
  "q": [
   {
    "t": "A while loop whose condition never becomes false will:",
    "o": [
     "Stop after 100 passes",
     "Run forever",
     "Raise an error immediately",
     "Skip its body"
    ],
    "a": 1,
    "w": "Nothing stops it but you. On this site the interpreter runs in a Web Worker and is killed after ten seconds, so the page survives the mistake."
   },
   {
    "t": "What does break do?",
    "o": [
     "Skips to the next pass",
     "Leaves the loop entirely",
     "Restarts the loop",
     "Pauses execution"
    ],
    "a": 1,
    "w": "break exits the whole loop immediately. continue is the one that skips only the current pass."
   },
   {
    "t": "When is a while loop's condition checked?",
    "o": [
     "Before every pass",
     "After every pass",
     "Only once",
     "Halfway through the body"
    ],
    "a": 0,
    "w": "It is tested before each pass, so a while loop whose condition starts false never runs its body at all."
   }
  ]
 },
 {
  "path": "python/enumerate_function.html",
  "title": "enumerate()",
  "cat": "Python",
  "q": [
   {
    "t": "What does `enumerate(['a', 'b'])` yield?",
    "o": [
     "'a', 'b'",
     "0, 1",
     "(0, 'a') then (1, 'b')",
     "A dictionary"
    ],
    "a": 2,
    "w": "It yields tuples of index and item. The `for i, x` form unpacks them, which is why the tuples are usually invisible."
   },
   {
    "t": "With `enumerate(names, start=1)`, which item does n=1 refer to?",
    "o": [
     "names[1]",
     "names[0]",
     "The last item",
     "It raises"
    ],
    "a": 1,
    "w": "start= changes the label only. The first item is still index 0, so using n to index back into the list is off by one."
   },
   {
    "t": "Why prefer enumerate over `for i in range(len(items))`?",
    "o": [
     "It is the only way to get an index",
     "It gives the item directly instead of indexing back in",
     "It sorts the list",
     "range does not work on lists"
    ],
    "a": 1,
    "w": "You get both the position and the value without a second lookup, and without an index you could get wrong."
   }
  ]
 },
 {
  "path": "python/f_strings_and_formatting.html",
  "title": "f-strings and Formatting",
  "cat": "Python",
  "q": [
   {
    "t": "What does `f\"{2/3:.2f}\"` produce?",
    "o": [
     "'0.67'",
     "'0.666666'",
     "0.67 as a float",
     "A syntax error"
    ],
    "a": 0,
    "w": "It produces the string '0.67'. Formatting affects the text produced, not the underlying value, which still has all its digits."
   },
   {
    "t": "What is `{price:>10.2f}` doing?",
    "o": [
     "Rounding price to 10 decimals",
     "Right-aligning in 10 columns with 2 decimals",
     "Multiplying by 10",
     "Left-aligning in 2 columns"
    ],
    "a": 1,
    "w": "`>` right-aligns, 10 is the field width, .2f is two decimal places. Combining them is how columns line up."
   },
   {
    "t": "You write `\"{name} scored\"` with no f prefix. What prints?",
    "o": [
     "The value of name",
     "The literal text {name} scored",
     "An error",
     "An empty string"
    ],
    "a": 1,
    "w": "Without the f prefix the braces are ordinary characters. This is a quiet bug: nothing raises, the output is just wrong."
   }
  ]
 },
 {
  "path": "python/loop_else.html",
  "title": "for/else and while/else",
  "cat": "Python",
  "q": [
   {
    "t": "When does a for/else's else block run?",
    "o": [
     "When the loop body never ran",
     "When the loop finished without a break",
     "Always",
     "Only when an exception occurred"
    ],
    "a": 1,
    "w": "It means nobreak. A loop over an empty sequence never breaks, so the else still runs - which is why the 'did not run' reading is wrong."
   },
   {
    "t": "What does for/else replace in ordinary code?",
    "o": [
     "The break statement",
     "A found = False flag checked after the loop",
     "The range function",
     "try/except"
    ],
    "a": 1,
    "w": "The flag exists only to carry 'we never found it' past the loop. The else block is that branch, without the extra variable."
   },
   {
    "t": "`for x in []: pass` followed by `else: print('hi')` prints what?",
    "o": [
     "Nothing",
     "hi",
     "An error",
     "Depends on Python version"
    ],
    "a": 1,
    "w": "Zero iterations means zero breaks, so the loop completed normally and the else runs."
   }
  ]
 },
 {
  "path": "python/input_and_output.html",
  "title": "input() and Output",
  "cat": "Python",
  "q": [
   {
    "t": "The user types 42. What does `input()` return?",
    "o": [
     "The integer 42",
     "The string '42'",
     "42.0",
     "It depends"
    ],
    "a": 1,
    "w": "Always a string. input cannot know what the digits are meant to be, so it does not guess - which is why '42' + '42' is '4242'."
   },
   {
    "t": "What does `print(i, end=' ')` do?",
    "o": [
     "Prints a space before i",
     "Prints i followed by a space instead of a newline",
     "Skips the print",
     "Adds a space to i"
    ],
    "a": 1,
    "w": "end replaces the trailing newline, which is how you print several values on one line. A bare print() then closes the line."
   },
   {
    "t": "Why does `int(input())` need a try/except in real programs?",
    "o": [
     "input is slow",
     "The user can type something that is not a number",
     "int is deprecated",
     "It does not"
    ],
    "a": 1,
    "w": "Any non-numeric text raises ValueError, and an empty line does too. Anything a person types needs handling."
   }
  ]
 },
 {
  "path": "python/lambda_map_filter.html",
  "title": "lambda, map and filter",
  "cat": "Python",
  "q": [
   {
    "t": "What can a lambda body contain?",
    "o": [
     "Any statements",
     "A single expression",
     "Up to three lines",
     "Only arithmetic"
    ],
    "a": 1,
    "w": "One expression, whose value is returned automatically. No return statement, no assignments, no loops."
   },
   {
    "t": "`list(m)` twice on a map object gives what the second time?",
    "o": [
     "The same list",
     "An empty list",
     "An error",
     "Half the list"
    ],
    "a": 1,
    "w": "map is a lazy iterator and is exhausted after one pass. Store the list if you need it more than once."
   },
   {
    "t": "Which is preferred: `map(lambda w: int(w), ws)` or `map(int, ws)`?",
    "o": [
     "The lambda version",
     "map(int, ws)",
     "They differ in result",
     "Neither - always use a loop"
    ],
    "a": 1,
    "w": "The function already exists, so wrapping it in a lambda adds nothing but noise."
   }
  ]
 },
 {
  "path": "python/match_and_case.html",
  "title": "match and case",
  "cat": "Python",
  "q": [
   {
    "t": "What does a bare `case status:` do?",
    "o": [
     "Compares against the variable status",
     "Matches anything and binds the name status",
     "Raises an error",
     "Matches only strings"
    ],
    "a": 1,
    "w": "A bare name is a capture pattern - it matches everything. This is the classic match bug, because the first such case swallows every value and nothing complains."
   },
   {
    "t": "What happens when no case matches and there is no `case _`?",
    "o": [
     "An error is raised",
     "Nothing happens - it falls through",
     "The first case runs",
     "The program exits"
    ],
    "a": 1,
    "w": "match is not exhaustive by default. With no matching case and no wildcard, the block simply does nothing."
   },
   {
    "t": "`case {\"type\": \"click\", \"x\": x}` does what beyond matching?",
    "o": [
     "Nothing else",
     "Binds x to the value found at that key",
     "Deletes the key",
     "Converts the dict to a list"
    ],
    "a": 1,
    "w": "Patterns destructure as they match, which is the main reason match exists - it replaces a check followed by a separate lookup."
   }
  ]
 },
 {
  "path": "python/range_step.html",
  "title": "range() with step",
  "cat": "Python",
  "q": [
   {
    "t": "What does `list(range(5, 0))` give?",
    "o": [
     "[5, 4, 3, 2, 1]",
     "[]",
     "[0, 1, 2, 3, 4]",
     "An error"
    ],
    "a": 1,
    "w": "With no step it counts up, and 5 is already past the stop of 0, so the range is empty. Counting down needs an explicit negative step."
   },
   {
    "t": "To walk indices of a 4-item list backwards including 0, you need:",
    "o": [
     "range(3, 0, -1)",
     "range(3, -1, -1)",
     "range(4, 0, -1)",
     "range(0, 4, -1)"
    ],
    "a": 1,
    "w": "The stop is excluded, so stopping at -1 is what makes 0 the last value produced."
   },
   {
    "t": "Why is `999_999 in range(1_000_000)` fast?",
    "o": [
     "The range is cached",
     "It computes the answer arithmetically rather than scanning",
     "Ranges are sorted",
     "It is not fast"
    ],
    "a": 1,
    "w": "A range knows its start, stop and step, so membership is a calculation. It is the one sequence where `in` does not scan."
   }
  ]
 },
 {
  "path": "python/sorted_with_key.html",
  "title": "sorted() with key=",
  "cat": "Python",
  "q": [
   {
    "t": "What does `nums = nums.sort()` leave in nums?",
    "o": [
     "The sorted list",
     "None",
     "The original list",
     "An error"
    ],
    "a": 1,
    "w": ".sort() sorts in place and returns None, so the assignment replaces the list with None. Use sorted() if you want a value back."
   },
   {
    "t": "How do you sort by count descending, then name ascending?",
    "o": [
     "reverse=True",
     "key=lambda x: (-x.count, x.name)",
     "Two separate sorts with reverse",
     "It is not possible"
    ],
    "a": 1,
    "w": "reverse=True flips every field. Negating just the numeric part of a tuple key reverses that field alone."
   },
   {
    "t": "What does a stable sort guarantee?",
    "o": [
     "It never crashes",
     "Items comparing equal keep their original order",
     "It is always fastest",
     "The list is copied"
    ],
    "a": 1,
    "w": "Stability is what makes sorting in several passes work: a later sort does not scramble the order established by an earlier one."
   }
  ]
 },
 {
  "path": "python/try_and_except.html",
  "title": "try and except",
  "cat": "Python",
  "q": [
   {
    "t": "Why is a bare `except:` discouraged?",
    "o": [
     "It is slower",
     "It catches your own bugs too, hiding them",
     "It only works in functions",
     "It cannot be combined with finally"
    ],
    "a": 1,
    "w": "It swallows NameError, AttributeError and everything else, so a typo becomes a wrong answer rather than a crash that tells you where to look."
   },
   {
    "t": "When does an `else` block on a try run?",
    "o": [
     "Always",
     "Only when an exception was raised",
     "Only when no exception was raised",
     "Never - try has no else"
    ],
    "a": 2,
    "w": "else runs when the try block completed without raising. It keeps follow-up code out of the try, so the handler cannot catch errors from it by accident."
   },
   {
    "t": "What does `as e` give you?",
    "o": [
     "A copy of the try block",
     "The exception object, with its detail",
     "The line number only",
     "A retry counter"
    ],
    "a": 1,
    "w": "The exception object carries the specifics - which key, which value - which is the part worth logging."
   }
  ]
 },
 {
  "path": "python/zip_function.html",
  "title": "zip()",
  "cat": "Python",
  "q": [
   {
    "t": "`zip(['a','b','c'], [1,2])` produces how many pairs?",
    "o": [
     "3",
     "2",
     "An error",
     "5"
    ],
    "a": 1,
    "w": "zip stops at the shortest input, silently. 'c' is dropped with no warning at all, which is why strict=True exists."
   },
   {
    "t": "How do you make a length mismatch an error?",
    "o": [
     "zip_longest",
     "zip(a, b, strict=True)",
     "len(a) == len(b)",
     "You cannot"
    ],
    "a": 1,
    "w": "strict=True raises ValueError when the inputs differ in length (Python 3.10+), turning a silent truncation into a visible bug."
   },
   {
    "t": "What does `zip(*pairs)` do?",
    "o": [
     "Sorts the pairs",
     "Unzips them back into separate sequences",
     "Removes duplicates",
     "Nothing useful"
    ],
    "a": 1,
    "w": "The star spreads the pairs into separate arguments, so zip re-groups them by position - the inverse of zipping."
   }
  ]
 }
];
