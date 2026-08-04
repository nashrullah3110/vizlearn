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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A* (pronounced \"A-star\") is a pathfinding and graph traversal algorithm renowned for its performance and accuracy. It's a cornerstone of game development, robotics, and logistics. Unlike simpler algorithms like Breadth-First Search (BFS) or Dijkstra's, A* uses a \"heuristic\" to intelligently guess the best path to explore, making it significantly faster."
   },
   {
    "t": "What does this module say about “Quick Context: What is A*”?",
    "ans": "A* (pronounced \"A-star\") is a pathfinding and graph traversal algorithm renowned for its performance and accuracy. It's a cornerstone of game development, robotics, and logistics. Unlike simpler algorithms like Breadth-First Search (BFS) or Dijkstra's, A* uses a \"heuristic\" to intelligently guess the best path to explore, making it significantly faster."
   }
  ]
 },
 {
  "path": "dsa/backtracking.html",
  "title": "Backtracking Search Method",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Backtracking is a problem-solving technique based on a simple, human idea: try one path, and if it doesn’t work, go back and try another. It systematically explores all possible solutions to a problem by building a solution step-by-step. When it hits a dead end, it \"backtracks\" to the last decision point and makes a different choice."
   },
   {
    "t": "What does this module say about “Quick Context: What is Backtracking”?",
    "ans": "Backtracking is a problem-solving technique based on a simple, human idea: try one path, and if it doesn’t work, go back and try another . It systematically explores all possible solutions to a problem by building a solution step-by-step. When it hits a dead end, it \"backtracks\" to the last decision point and makes a different choice."
   },
   {
    "t": "What does this module say about “The Core Idea: The Three Steps of Backtracking”?",
    "ans": "Every backtracking algorithm, including the maze solver you see above, follows a recursive loop:"
   }
  ]
 },
 {
  "path": "dsa/bellman_ford.html",
  "title": "Bellman-Ford and Negative Weights",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Bellman-Ford relaxes every edge V−1 times instead of committing greedily, so it survives negative weights at O(V·E). One extra pass turns it into a negative-cycle detector. Use Dijkstra when all weights are non-negative; reach for this when they are not."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Bellman-Ford finds shortest paths from one source, like Dijkstra — but it works with negative edge weights, and it can detect when no shortest path exists at all."
   },
   {
    "t": "What does this module say about “Why Dijkstra Fails on Negative Edges”?",
    "ans": "Dijkstra is greedy: once it finalises a vertex's distance, it never revisits it. That relies on an assumption — that adding more edges can only make a path longer."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Imagine finding a word in a physical dictionary. You don't start at \"A\" and read every word. Instead, you open it to the middle, see if your word comes before or after, and instantly eliminate half the dictionary. That is binary search. It's an algorithm that finds a target in a sorted array by repeatedly dividing the search interval in half."
   },
   {
    "t": "What does this module say about “Quick Context: The Dictionary Analogy”?",
    "ans": "Imagine finding a word in a physical dictionary. You don't start at \"A\" and read every word. Instead, you open it to the middle, see if your word comes before or after, and instantly eliminate half the dictionary. That is binary search. It's an algorithm that finds a target in a sorted array by repeatedly dividing the search interval in half."
   },
   {
    "t": "What does this module say about “Key Takeaways”?",
    "ans": "Imagine finding a word in a physical dictionary. You don't start at \"A\" and read every word. Instead, you open it to the middle, see if your word comes before or after, and instantly eliminate half the dictionary. That is binary search. It's an algorithm that finds a target in a sorted array by repeatedly dividing the search interval in half."
   }
  ]
 },
 {
  "path": "dsa/binary_search_trees.html",
  "title": "Binary Search Trees",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A BST turns the binary-search idea into a living structure with O(log n) search, insert and delete — but only while it stays bushy. Sorted input degenerates it to a linked list, which is precisely why self-balancing variants exist and why they, not plain BSTs, are what production libraries ship."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A binary search tree keeps its values in sorted order by position. At every node: the entire left subtree is smaller, the entire right subtree is larger. Searching then works exactly like binary search — compare, discard half, repeat."
   },
   {
    "t": "What does this module say about “Search, Insert, Delete”?",
    "ans": "Searching is a walk: compare with the current node, go left if smaller, right if larger, stop when equal or when you fall off the tree. Insertion follows the same walk and attaches the new node where the search failed."
   }
  ]
 },
 {
  "path": "dsa/breadth_first_search.html",
  "title": "Breadth First Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “Preorder” here?",
    "ans": "Useful for copying trees. The root is always the first element."
   },
   {
    "t": "What is meant by “Postorder” here?",
    "ans": "Useful for deleting trees. The root is always the last element."
   },
   {
    "t": "What is meant by “Level Order (BFS)” here?",
    "ans": "Explores level by level. Finds the shortest path from the root to any other node."
   }
  ]
 },
 {
  "path": "dsa/bubble_sort.html",
  "title": "Bubble Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does this module say about “Quick Context: What is Bubble Sort”?",
    "ans": "Bubble Sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted. The algorithm gets its name because smaller or larger elements \"bubble\" to their proper place."
   },
   {
    "t": "What does this module say about “The Core Idea: Compare and Swap”?",
    "ans": "The entire algorithm is built on one fundamental operation: comparing two adjacent items and swapping them if the first is larger than the second. This process is repeated from the beginning of the array to the end. After the first full pass, the largest element in the array will have \"bubbled up\" to the very last position. The next pass does the same for the second-largest element, and so on."
   },
   {
    "t": "What does this module say about “Pseudocode”?",
    "ans": "The outer loop `i` tracks how many elements are already sorted at the end. The inner loop `j` performs the adjacent comparisons."
   }
  ]
 },
 {
  "path": "dsa/counting_sort.html",
  "title": "Counting Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does this module say about “Quick Context: What is Counting Sort”?",
    "ans": "Counting Sort is a special type of sorting algorithm that doesn't work by comparing elements. Instead, it sorts integers by counting the number of times each distinct value appears in the input array. It's extremely fast, but it only works when the input values are integers within a specific, relatively small range."
   },
   {
    "t": "What does this module say about “Performance & Limitations”?",
    "ans": "Counting Sort is incredibly fast with a time complexity of O(n + k) , where 'n' is the number of elements and 'k' is the range of the input values. This is linear time, much faster than comparison-based sorts like Merge Sort or Quick Sort (O(n log n))."
   }
  ]
 },
 {
  "path": "dsa/cycle_detection.html",
  "title": "Cycle Detection",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Floyd's algorithm detects a loop in O(n) time and O(1) space, because inside a cycle the gap between a one-step and a two-step pointer shrinks by exactly one each iteration and must hit zero. A second phase from the head then locates where the cycle begins."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Floyd's cycle detection — the tortoise and hare — determines whether a linked structure contains a loop, using two pointers moving at different speeds and constant extra memory."
   },
   {
    "t": "What does this module say about “The Obvious Solution and Its Cost”?",
    "ans": "You could store every visited node in a hash set and check each new one. That works and is O(n) time — but it needs O(n) memory ."
   }
  ]
 },
 {
  "path": "dsa/depth_first_search.html",
  "title": "Depth First Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does this module say about “Quick Context: What is Depth-First Search”?",
    "ans": "Depth-First Search (DFS) is an algorithm for traversing or searching tree or graph data structures. The algorithm starts at a selected root node and explores as far as possible along each branch before backtracking. It uses a stack (Last-In, First-Out) to keep track of which node to visit next."
   },
   {
    "t": "What does this module say about “The Core Idea: Go Deep, Then Backtrack”?",
    "ans": "Imagine you're in a maze. Using a DFS strategy, you would pick one path and follow it until you hit a dead end. Only then would you backtrack to the last intersection and try a different, unexplored path. This is the essence of DFS."
   },
   {
    "t": "What does this module say about “Use Cases & Comparison to BFS”?",
    "ans": "DFS is excellent for tasks where you need to explore a path to its conclusion, such as:"
   }
  ]
 },
 {
  "path": "dsa/dijkstras.html",
  "title": "Dijkstra's Algorithm",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “Greedy Choice” here?",
    "ans": "Always explores the most promising path first (the one with the lowest total weight so far)."
   },
   {
    "t": "What is meant by “Priority Queue is Essential” here?",
    "ans": "Efficiently finding the unvisited node with the minimum distance is crucial for performance."
   },
   {
    "t": "What is meant by “Finalized Paths” here?",
    "ans": "Once a node is visited, its shortest path from the source is locked in and will not change."
   },
   {
    "t": "What is meant by “Application” here?",
    "ans": "Perfect for network routing, GPS navigation, and any problem that can be modeled as finding the cheapest path in a graph with non-negative weights."
   }
  ]
 },
 {
  "path": "dsa/divide_and_conquer.html",
  "title": "Divide and Conquer",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Divide and conquer gets its log factor from tree depth: halving repeatedly takes log n levels. Multiply that by the work per level and you have the complexity. Recursing into every branch gives O(n log n); discarding all but one gives O(log n)."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Divide and conquer solves a problem by splitting it into smaller instances of itself, solving those recursively, and combining the results. Three phases: divide, conquer, combine."
   },
   {
    "t": "What does this module say about “Where log n Comes From”?",
    "ans": "The recursion tree makes it obvious. Each level halves the problem size, so it takes log₂n levels to reach size 1 — that is the height of the tree."
   }
  ]
 },
 {
  "path": "dsa/dynamic_programming.html",
  "title": "Dynamic Programming",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Dynamic programming is recursion plus memory. Spot repeated subproblems, define a recurrence, fill a table in dependency order, and exponential work collapses to polynomial. The difficulty is never the code — it is finding the recurrence."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Dynamic programming solves a problem by breaking it into subproblems, solving each once , and storing the answers. It applies when the same subproblems keep reappearing — which is exactly when plain recursion wastes enormous effort."
   },
   {
    "t": "What does this module say about “The Two Conditions”?",
    "ans": "If only the first holds you can still memoise for speed. If neither holds, DP is the wrong tool."
   }
  ]
 },
 {
  "path": "dsa/fibonacci_search.html",
  "title": "Fibonacci Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “Requires Sorted Array” here?",
    "ans": "Just like Binary Search, the data must be sorted for Fibonacci Search to work."
   },
   {
    "t": "What is meant by “Uneven Splitting” here?",
    "ans": "The core mechanism is splitting the array into uneven chunks whose sizes are consecutive Fibonacci numbers."
   },
   {
    "t": "What is meant by “Arithmetic Simplicity” here?",
    "ans": "Its main strength is replacing costly division/multiplication with simple addition and subtraction."
   },
   {
    "t": "What is meant by “Logarithmic Performance” here?",
    "ans": "It's an extremely fast search algorithm for large arrays, with performance comparable to Binary Search."
   }
  ]
 },
 {
  "path": "dsa/graph_representations.html",
  "title": "Graph Representations",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A matrix buys O(1) edge lookup with O(V²) memory; a list buys O(V+E) memory with O(degree) lookup. Because real graphs are sparse, adjacency lists are the default — and that choice is what makes BFS and DFS O(V+E) rather than O(V²)."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A graph is a set of vertices connected by edges . Every graph algorithm on this site — BFS, DFS, Dijkstra, A* — assumes some way of storing those edges, and that choice quietly determines their performance."
   },
   {
    "t": "What does this module say about “It Changes Algorithm Complexity”?",
    "ans": "This is not just a storage detail. BFS and DFS are O(V + E) with an adjacency list but O(V²) with a matrix, because each vertex must scan a whole row. On a sparse graph with a million vertices that is the difference between seconds and hours."
   }
  ]
 },
 {
  "path": "dsa/greedy_algorithms.html",
  "title": "Greedy Algorithms",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Greedy algorithms are fast and elegant when the greedy choice property holds — and silently wrong when it does not. Always ask whether a locally best move can ever block a globally better one. If it can, reach for dynamic programming instead."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A greedy algorithm builds a solution one step at a time, always taking whatever looks best at that moment , and never revisiting a decision. No backtracking, no lookahead."
   },
   {
    "t": "What does this module say about “Activity Selection: Greedy Wins”?",
    "ans": "Given activities with start and finish times, pick the most that do not overlap. The greedy rule is: always take the one that finishes earliest among those still compatible."
   }
  ]
 },
 {
  "path": "dsa/hash_tables.html",
  "title": "Hash Tables and Hashing",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Hashing replaces searching with computing an address. Collisions are unavoidable and must be resolved by chaining or probing; the load factor governs how often they happen. Keep it low and lookups stay effectively constant — let it climb and a hash table quietly becomes a linked list."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A hash table stores key–value pairs in an array. A hash function converts each key into an array index, so finding a key requires no searching at all — you compute where it must be and go straight there."
   },
   {
    "t": "What does this module say about “What Makes a Good Hash Function”?",
    "ans": "The lab uses a simple polynomial rolling hash, shown live above the buckets. Real implementations use stronger functions, but the mechanism is identical."
   }
  ]
 },
 {
  "path": "dsa/heap_sort.html",
  "title": "Heap Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Heap sort is O(n log n) in every case with O(1) extra memory — the only common sort offering both. It loses on speed to quick sort because scattered sift-down accesses wreck cache locality, and it is not stable. Use it when worst-case guarantees matter more than raw throughput."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Heap sort turns the array into a max-heap, then repeatedly moves the largest element to the end. It sorts in place with a guaranteed O(n log n) in every case — best, average and worst."
   },
   {
    "t": "What does this module say about “Phase 1: Heapify in O(n)”?",
    "ans": "Starting from the last non-leaf node and working backwards, sift each element down. Leaves are already valid heaps of size one, so half the array needs no work at all."
   }
  ]
 },
 {
  "path": "dsa/heaps_and_priority_queues.html",
  "title": "Heaps and Priority Queues",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A heap keeps only the extreme value ordered, and that weaker guarantee is what makes it fast: O(1) peek, O(log n) insert and extract, in a pointer-free array. Whenever an algorithm repeatedly asks for the smallest or largest remaining item, a heap is the answer."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A heap is a complete binary tree obeying one rule: every parent is smaller than both its children (a min-heap ) or larger than both (a max-heap ). It says nothing about siblings — the tree is only partially ordered."
   },
   {
    "t": "What does this module say about “Why Partial Ordering Is Better Here”?",
    "ans": "A BST fully sorts its data, which costs effort to maintain. A heap only guarantees the extreme value sits at the root. If all you ever ask is \"what is the smallest item?\", full sorting is wasted work."
   }
  ]
 },
 {
  "path": "dsa/insertion_sort.html",
  "title": "Insertion Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “In-Place” here?",
    "ans": "Sorts the array without needing extra storage."
   },
   {
    "t": "What is meant by “Adaptive” here?",
    "ans": "Performance improves as the array becomes more sorted."
   },
   {
    "t": "What is meant by “Stable” here?",
    "ans": "It does not change the relative order of elements with equal values."
   },
   {
    "t": "What is meant by “Best for Small or Nearly Sorted Data” here?",
    "ans": "Its O(n²) complexity makes it unsuitable for large, unsorted lists."
   }
  ]
 },
 {
  "path": "dsa/interpolation_search.html",
  "title": "Interpolation Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “Smarter Than Binary Search” here?",
    "ans": "It uses the data's values to make a better guess about where the target might be."
   },
   {
    "t": "What is meant by “Data Distribution is Key” here?",
    "ans": "Its incredible speed is only realized when the data is uniformly distributed."
   },
   {
    "t": "What is meant by “No \"Blind\" Probing” here?",
    "ans": "Unlike Binary Search, it doesn't always check the middle, making it feel more human-like in its approach."
   },
   {
    "t": "What is meant by “A Trade-off” here?",
    "ans": "You trade the guaranteed O(log n) performance of Binary Search for a potentially much faster O(log(log n)) average time, at the risk of a slow O(n) worst case."
   }
  ]
 },
 {
  "path": "dsa/kmp_string_matching.html",
  "title": "KMP String Matching",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "KMP precomputes an LPS table describing the pattern's self-overlap, then uses it to shift intelligently after a mismatch. Because the text pointer never moves backwards, matching is O(n+m) with a worst-case guarantee — and it works on streams that can never be rewound."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Knuth–Morris–Pratt finds a pattern inside a text in O(n + m) , where naive search can take O(n·m). The insight: a partial match already tells you something, so there is no need to start over."
   },
   {
    "t": "What does this module say about “What Naive Search Wastes”?",
    "ans": "Naive search compares the pattern at position 0. On a mismatch it shifts by one and restarts from the beginning of the pattern , re-reading text characters it has already examined."
   }
  ]
 },
 {
  "path": "dsa/linear_search.html",
  "title": "Linear Search",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “No Sorting Required” here?",
    "ans": "Works on unsorted data, which is a major advantage."
   },
   {
    "t": "What is meant by “Simple to Implement” here?",
    "ans": "It's often the first search algorithm taught because its logic is so clear."
   },
   {
    "t": "What is meant by “Predictable Performance” here?",
    "ans": "The time it takes is directly proportional to the size of the list."
   },
   {
    "t": "What is meant by “The Brute-Force Method” here?",
    "ans": "It's a reliable but often slow \"brute-force\" approach to finding an item."
   }
  ]
 },
 {
  "path": "dsa/linked_lists.html",
  "title": "Linked Lists",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Linked lists make insertion and deletion cheap and access expensive — the exact opposite of arrays. Use them when you hold a reference to the node you need and are splicing constantly; otherwise an array's cache behaviour usually beats the theory."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A linked list stores each element in its own node , which also holds a pointer to the next node. Unlike an array, the elements need not sit next to each other in memory — the pointers are what impose the order."
   },
   {
    "t": "What does this module say about “The Fundamental Trade-off”?",
    "ans": "An array gives you arr[500] in O(1) because the address is pure arithmetic: start + 500 × itemsize. A linked list has no such shortcut — you must start at the head and follow 500 pointers. That is O(n) ."
   }
  ]
 },
 {
  "path": "dsa/merge_sort.html",
  "title": "Merge Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “Reliable Performance” here?",
    "ans": "With a guaranteed O(n log n) time complexity, Merge Sort is predictable and efficient, regardless of the initial order of the data."
   },
   {
    "t": "What is meant by “Not In-Place” here?",
    "ans": "The need for auxiliary space (O(n)) can be a limiting factor in memory-constrained environments."
   },
   {
    "t": "What is meant by “Stable Sort” here?",
    "ans": "It preserves the relative order of equal elements, which is crucial for certain applications, such as sorting data on multiple criteria."
   },
   {
    "t": "What is meant by “Excellent for External Sorting” here?",
    "ans": "Because it works by processing data in chunks, Merge Sort is well-suited for sorting datasets that are too large to fit into memory."
   }
  ]
 },
 {
  "path": "dsa/minimum_spanning_tree.html",
  "title": "Minimum Spanning Tree",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "An MST connects everything with V−1 edges at minimum cost. Kruskal sorts all edges and uses union-find to reject cycles; Prim grows one tree using a priority queue. The cut property proves both greedy strategies optimal, so neither ever needs to reconsider."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A spanning tree connects every vertex of a graph using exactly V−1 edges and no cycles. The minimum spanning tree is the one with the smallest total edge weight — the cheapest way to keep everything connected."
   },
   {
    "t": "What does this module say about “Kruskal: Sort Globally, Add Safely”?",
    "ans": "The connectivity check is exactly what union-find is for — a near-constant-time \"same group?\" query. Kruskal is the headline application of that structure."
   }
  ]
 },
 {
  "path": "dsa/dictionaries_in_python.html",
  "title": "Python Dictionary Lab",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What does this module say about “Quick Context: What is a Dictionary”?",
    "ans": "A Python dictionary is a collection of key-value pairs . Think of it like a real-world dictionary where you look up a word (the \"key\") to find its definition (the \"value\"). Dictionaries are incredibly fast for retrieving data because they use a technique called hashing . Instead of searching through items one by one, Python can instantly calculate where a value is stored based on its key."
   },
   {
    "t": "What does this module say about “The Core Idea: Hashing and O(1) Access”?",
    "ans": "The magic of dictionaries is their average O(1) , or \"constant time,\" performance for lookups, insertions, and deletions. This means that no matter how large the dictionary grows, the time it takes to perform these operations stays roughly the same."
   },
   {
    "t": "What does this module say about “Practical Use Cases”?",
    "ans": "Dictionaries are one of the most used data structures in Python. They are perfect for:"
   }
  ]
 },
 {
  "path": "dsa/lists_in_python.html",
  "title": "Python List Lab",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “Mutability is Key” here?",
    "ans": "Unlike strings or tuples, lists can be modified in-place, making them ideal for collections of data that need to change over time."
   },
   {
    "t": "What is meant by “Zero-Based Indexing” here?",
    "ans": "Always remember that the first element is at index 0. This is a common source of \"off-by-one\" errors for beginners."
   },
   {
    "t": "What is meant by “Methods vs. Functions” here?",
    "ans": "Methods like my_list.sort() modify the list directly. Functions like sorted(my_list) return a new, sorted list without changing the original."
   },
   {
    "t": "What is meant by “Versatility” here?",
    "ans": "From simple collections of numbers to complex nested structures, lists are the go-to data structure for ordered, mutable data in Python."
   }
  ]
 },
 {
  "path": "dsa/strings_in_python.html",
  "title": "Python String Lab",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “Immutability is Law” here?",
    "ans": "Always remember that string methods do not change the original string. They return a new one. Forgetting this is a common bug, e.g., writing my_string.upper() without assigning the result back to a variable."
   },
   {
    "t": "What is meant by “Slicing is Non-Destructive” here?",
    "ans": "Slicing is a safe way to get parts of a string. It always produces a new string and never modifies the original."
   },
   {
    "t": "What is meant by “Rich Method Library” here?",
    "ans": "Python's string methods are powerful and efficient. Before writing your own function to manipulate a string, always check if a built-in method already does what you need."
   },
   {
    "t": "What is meant by “Strings are Iterable” here?",
    "ans": "You can loop over a string directly, e.g., for char in my_string: print(char) , which is useful for character-by-character processing."
   }
  ]
 },
 {
  "path": "dsa/queues.html",
  "title": "Queues (FIFO)",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A queue preserves arrival order with O(1) work at both ends, provided you move pointers rather than data. Its most important property in algorithms is level-by-level processing — swapping a stack for a queue turns depth-first search into breadth-first search and nothing else changes."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A queue serves items in the order they arrived: FIFO , First In, First Out. You add at the back ( enqueue ) and remove from the front ( dequeue ). It is the queue at a shop, modelled exactly."
   },
   {
    "t": "What does this module say about “Why the Naive Implementation Is Wrong”?",
    "ans": "If you implement a queue as a plain array and dequeue by removing element 0, every dequeue shifts all remaining elements down one position — that is O(n) , not O(1)."
   }
  ]
 },
 {
  "path": "dsa/quick_sort.html",
  "title": "Quick Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “Fast in Practice” here?",
    "ans": "Typically one of the fastest sorting algorithms for RAM-based sorting."
   },
   {
    "t": "What is meant by “In-Place Sorting” here?",
    "ans": "Its low space complexity makes it very memory-efficient compared to Merge Sort."
   },
   {
    "t": "What is meant by “Worst-Case Risk” here?",
    "ans": "Performance degrades significantly on already-sorted or poorly partitioned data. The choice of pivot is critical."
   },
   {
    "t": "What is meant by “Not Stable” here?",
    "ans": "Quick Sort does not preserve the relative order of equal elements, which can be a disadvantage in some applications."
   }
  ]
 },
 {
  "path": "dsa/radix_sort.html",
  "title": "Radix Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Radix sort distributes by digit rather than comparing, achieving O(d·n) — linear when digit count is fixed. It depends entirely on stable bucketing, since each pass must preserve the ordering established by the last. Only usable on digit-decomposable keys, and it costs extra memory."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Radix sort processes numbers one digit at a time, distributing them into buckets by that digit and collecting them back. Repeat for every digit position — least significant first — and the array emerges sorted, with zero comparisons ."
   },
   {
    "t": "What does this module say about “Why Stability Is Non-Negotiable”?",
    "ans": "This is the crux. When sorting by the tens digit, two numbers with the same tens digit must retain the order they got from the units pass — otherwise that earlier work is destroyed."
   }
  ]
 },
 {
  "path": "dsa/recursion_and_call_stack.html",
  "title": "Recursion and the Call Stack",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The confusing part is that a recursive function does not finish before calling itself again. factorial(5) must pause, wait for factorial(4) , and only then multiply."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Recursion is a function calling itself on a smaller version of the same problem. It needs exactly two things: a base case that stops the descent, and a recursive case that moves toward it."
   },
   {
    "t": "What does this module say about “The Call Stack Does the Remembering”?",
    "ans": "The confusing part is that a recursive function does not finish before calling itself again. factorial(5) must pause, wait for factorial(4) , and only then multiply."
   }
  ]
 },
 {
  "path": "dsa/selection_sort.html",
  "title": "Selection Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "What is meant by “Simple to Understand” here?",
    "ans": "Its straightforward logic makes it easy to grasp and implement."
   },
   {
    "t": "What is meant by “Memory Efficient” here?",
    "ans": "The O(1) space complexity is a significant advantage."
   },
   {
    "t": "What is meant by “Inefficient for Large Lists” here?",
    "ans": "The O(n²) time complexity makes it impractical for sorting large datasets compared to algorithms like Merge Sort or Quick Sort."
   },
   {
    "t": "What is meant by “Minimal Swaps” here?",
    "ans": "It performs at most `n-1` swaps, which can be useful if write operations are costly."
   }
  ]
 },
 {
  "path": "dsa/sliding_window.html",
  "title": "Sliding Window",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A sliding window keeps a running summary and updates it at the edges instead of rebuilding it. Fixed windows add-and-remove; variable windows expand and contract. Because both pointers only move forward, the total cost stays linear even when the code looks nested."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The sliding window technique maintains a contiguous range over an array or string and moves it along, updating a running summary incrementally rather than rebuilding it. It turns O(n·k) into O(n)."
   },
   {
    "t": "What does this module say about “Fixed Windows: Add One, Remove One”?",
    "ans": "To find the maximum sum of k consecutive elements, the naive approach sums every window from scratch — k additions per position, O(n·k) overall."
   }
  ]
 },
 {
  "path": "dsa/stacks.html",
  "title": "Stacks (LIFO)",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A stack restricts you to one end, and that restriction buys O(1) push, pop and peek. It models anything where the most recent item must be handled first: nested brackets, function calls, undo history, and depth-first traversal."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A stack is a collection where you may only touch one end — the top . The last thing you put in is the first thing you take out, which is why it is called LIFO : Last In, First Out. Think of a stack of plates."
   },
   {
    "t": "What does this module say about “Three Operations, All O(1)”?",
    "ans": "All three are O(1) because they never touch the rest of the structure. That guarantee is the reason stacks are used in performance-critical places like the call stack."
   }
  ]
 },
 {
  "path": "dsa/topological_sort.html",
  "title": "Topological Sort",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Topological sort orders a DAG so dependencies always precede dependents, in O(V+E) via in-degree counting. When it cannot output every node, the leftovers form a cycle — making it both a scheduler and a circular-dependency detector."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A topological sort orders the vertices of a directed graph so that every edge points forwards: if A must happen before B, A appears earlier. It answers \"in what order can I do these dependent tasks?\""
   },
   {
    "t": "What does this module say about “It Requires a DAG”?",
    "ans": "A valid ordering exists if and only if the graph is a directed acyclic graph — directed edges, no cycles. If A depends on B and B depends on A, no order can satisfy both."
   }
  ]
 },
 {
  "path": "dsa/trie_prefix_tree.html",
  "title": "Trie (Prefix Tree)",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A trie stores strings as paths, sharing common prefixes. Lookup is O(word length) regardless of dictionary size, and prefix queries fall out of the structure for free — which no hash table can match. The price is memory, mitigated by hash-map children or radix compression."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A trie (from re trie val, usually pronounced \"try\") stores strings as paths through a tree. Each edge carries a character, so following a path from the root spells out a prefix. Words sharing a prefix share those nodes."
   },
   {
    "t": "What does this module say about “Lookup Does Not Care How Many Words You Have”?",
    "ans": "Searching for a word of length L costs O(L) — one step per character. Crucially, that is independent of how many words the trie contains. A dictionary of ten words and one of ten million both answer a five-letter query in five steps."
   }
  ]
 },
 {
  "path": "dsa/two_pointers.html",
  "title": "Two Pointers",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Two pointers replaces nested loops with a single coordinated pass, in O(1) extra space. It works only when moving a pointer changes the result predictably — usually because the data is sorted. Recognising that condition is the whole skill."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The two pointers technique uses two indices moving through a sequence in a coordinated way. It typically replaces a nested loop, turning O(n²) into O(n) with no extra memory."
   },
   {
    "t": "What does this module say about “The Classic: Pair Sum”?",
    "ans": "Find two numbers in a sorted array that sum to a target. Brute force checks all pairs: O(n²). Two pointers starts one at each end:"
   }
  ]
 },
 {
  "path": "dsa/union_find.html",
  "title": "Union-Find (Disjoint Set)",
  "cat": "Algorithms",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Union-Find answers \"same group?\" and \"merge groups\" in effectively constant time, using union by rank to keep trees shallow and path compression to flatten them on the way. It is the structure that makes Kruskal's algorithm and fast connected-component queries possible."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Union-Find maintains a collection of non-overlapping sets and supports two operations: find(x) — which set does x belong to? — and union(a, b) — merge the two sets containing a and b."
   },
   {
    "t": "What does this module say about “The Structure”?",
    "ans": "Each set is stored as a tree, with every element pointing to a parent. The root represents the whole set. Two elements are in the same set exactly when they have the same root."
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
    "t": "What does this module say about “The General Formula”?",
    "ans": "How to accurately count the trainable weights and biases inside a Convolutional Layer."
   },
   {
    "t": "What does this module say about “The 3D Nature of Filters”?",
    "ans": "A common misconception is that a filter (kernel) in a CNN is just a 2D grid, like a 3x3 square. While it moves across the image in 2D (up/down, left/right), a filter is actually a 3D block ."
   },
   {
    "t": "What does this module say about “Why does output size not matter”?",
    "ans": "Notice that the size of the input image (e.g., 1000x1000 vs 28x28) and the resulting output feature map are not in the formula . Because of Parameter Sharing, the same filter is slid across the entire image. The number of parameters depends only on the filter configuration , not the image dimensions!"
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
    "t": "What is meant by “Epoch” here?",
    "ans": "One complete pass through the entire dataset."
   },
   {
    "t": "What is meant by “Iteration/Step” here?",
    "ans": "One pass of a single batch through the CNN."
   }
  ]
 },
 {
  "path": "computer_vision/how_dense_layer_works_in_cnn.html",
  "title": "Fully Connected Layer in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Visualize how a flattened 1D array of features connects to every node in the output layer using weights, biases, and Softmax to make final classifications."
   },
   {
    "t": "What does this module say about “The Transition to 1D”?",
    "ans": "Throughout the early stages of a CNN, images are processed as 2D grids (or 3D volumes with color channels). Convolutional and pooling layers extract spatial features like edges, textures, and shapes. However, to make a final classification (e.g., \"Is this a cat or a dog?\"), the network must flatten this 2D/3D data into a single 1D list of numbers. This is the input vector you see on the left."
   },
   {
    "t": "What does this module say about “Why \"Fully Connected\"”?",
    "ans": "It is called a Fully Connected (or Dense) layer because every single node in the input vector is connected to every single node in the output vector. If you have 4 inputs and 3 outputs, there are $4 \\times 3 = 12$ distinct connections (weights), plus 3 biases."
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
  "path": "computer_vision/how_neural_network_process_images.html",
  "title": "How Neural Networks Process Images",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “Flattening” here?",
    "ans": "is the process of stringing rows of pixels together into a line."
   },
   {
    "t": "What does this module say about “Preprocessing Parameters”?",
    "ans": "Neural networks usually compress images to small grids (like 28x28) to manage node count."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "When you look at an image, you see a 2D grid of colors. However, standard Artificial Neural Networks (specifically Dense or Fully-Connected Layers ) are structured to accept only a one-dimensional (1D) array or vector of numbers as input. Before a network can \"look\" at an image, the image must undergo Flattening ."
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
  "path": "computer_vision/padding_in_cnn.html",
  "title": "Padding in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “Valid Padding (P=0)” here?",
    "ans": "No padding. The image shrinks. Only pixels where the kernel fits entirely are computed."
   },
   {
    "t": "What is meant by “Same Padding” here?",
    "ans": "Padding is added so the output size matches the input size. For K=3, P=1. For K=5, P=2."
   }
  ]
 },
 {
  "path": "computer_vision/parameter_sharing_in_cnn.html",
  "title": "Parameter Sharing in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Visualize why Convolutional Neural Networks are so efficient. See how a single set of shared weights is reused across the entire image, drastically reducing the number of parameters compared to a Dense layer."
   },
   {
    "t": "What does this module say about “What is Parameter Sharing”?",
    "ans": "In a traditional Fully Connected (Dense) neural network layer, every output node is connected to every input node with a unique weight (parameter). If you process an image, a specific pixel in the top-left corner has a completely different weight than a pixel in the bottom-right corner."
   },
   {
    "t": "What does this module say about “The Massive Efficiency Gain”?",
    "ans": "Let's look at the math for the simple interactive above. We have a 4x4 input grid (16 pixels) and we are generating a 3x3 output grid (9 pixels)."
   }
  ]
 },
 {
  "path": "computer_vision/downsampling_in_cnn.html",
  "title": "Pooling Layer",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "In Convolutional Neural Networks (CNNs), downsampling (or pooling) is the process of reducing the spatial dimensions (width and height) of a feature map. This is a crucial step that helps to make the network more efficient and robust."
   },
   {
    "t": "What does this module say about “What is Downsampling”?",
    "ans": "In Convolutional Neural Networks (CNNs), downsampling (or pooling) is the process of reducing the spatial dimensions (width and height) of a feature map. This is a crucial step that helps to make the network more efficient and robust."
   },
   {
    "t": "What does this module say about “Max Pooling”?",
    "ans": "Selects the maximum pixel value from the pooling window. It's effective at capturing the most prominent features, like edges or bright spots, and is the most widely used pooling method."
   }
  ]
 },
 {
  "path": "computer_vision/rgb_image_processing.html",
  "title": "RGB Image Processing",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "RGB Image Processing is a fundamental concept in computer vision. It's the basis for how computers \"see\" and manipulate color images. Every colored pixel on your screen is a combination of three values: Red, Green, and Blue."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "RGB Image Processing is a fundamental concept in computer vision. It's the basis for how computers \"see\" and manipulate color images. Every colored pixel on your screen is a combination of three values: Red, Green, and Blue."
   },
   {
    "t": "What does this module say about “The Core Idea: Channels as Layers”?",
    "ans": "Think of a color image not as a single flat picture, but as three separate grayscale images stacked on top of each other. Each of these \"layers\" is a channel , representing the intensity of Red, Green, or Blue light for every pixel."
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
    "ans": "Visualize the Rectified Linear Unit (ReLU). See how it introduces non-linearity by passing positive signals and turning off (clipping) negative signals."
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
  "path": "computer_vision/strides_in_cnn.html",
  "title": "Strides in CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “Stride = 1” here?",
    "ans": "Maximum detail, slow computation, large output map."
   },
   {
    "t": "What is meant by “Stride > 1” here?",
    "ans": "Downsamples the spatial dimensions of the image."
   }
  ]
 },
 {
  "path": "computer_vision/transfer_learning_with_cnn.html",
  "title": "Transfer Learning with CNN",
  "cat": "Computer Vision",
  "q": [
   {
    "t": "What is meant by “Freezing” here?",
    "ans": "a layer means its weights are locked and not updated during backpropagation."
   },
   {
    "t": "What does this module say about “What is Transfer Learning”?",
    "ans": "Training a Deep Convolutional Neural Network from scratch requires millions of images (like the ImageNet dataset), massive amounts of computing power (GPUs), and weeks of training time. Furthermore, early layers in a CNN generally learn the exact same things regardless of the dataset: generic edges, colors, and basic textures."
   },
   {
    "t": "What does this module say about “How it Works: Modifying the Architecture”?",
    "ans": "A standard pre-trained model (like ResNet-50 or VGG-16) is split into two conceptual parts:"
   }
  ]
 },
 {
  "path": "database/case_and_views_in_sql.html",
  "title": "CASE and Views in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "CASE is a per-row branch inside SELECT that returns the first matching value or NULL if nothing matches and there is no ELSE. A view is a saved query, not saved data — it re-runs against live tables on every read, which is what makes it stay correct as the underlying data changes and is exactly the property a materialized view trades away for speed."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "CASE is an if/else that lives inside a SELECT list, evaluated once per row. A VIEW is a query with a name, so you can SELECT from it like a table without repeating the logic every time."
   },
   {
    "t": "What does this module say about “Views: a name for a query, not a copy of it”?",
    "ans": "A plain view stores no data. Every time you query it, the underlying SELECT runs again against the current table — which is the whole point of the raise experiment below. This is different from a materialized view , which does store a snapshot and has to be refreshed explicitly to catch up with changes underneath it."
   }
  ]
 },
 {
  "path": "database/common_table_expressions_in_sql.html",
  "title": "Common Table Expressions in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Use CTEs to turn one unreadable query into several named steps that a colleague can follow. Use WITH RECURSIVE when the data is a hierarchy and you do not know how deep it goes — that is a problem plain SQL simply cannot express."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A Common Table Expression is a named temporary result set defined with WITH , available only to the statement that follows it. Think of it as a variable for a query: compute something once, give it a name, then use that name."
   },
   {
    "t": "What does this module say about “Why Not Just Nest Subqueries”?",
    "ans": "You can — the nested example in this lab returns exactly the same rows. But compare how they read. A nested query is evaluated inside out , so you must find the innermost parenthesis and work outward, holding each layer in your head. A chain of CTEs reads top to bottom , like a recipe."
   }
  ]
 },
 {
  "path": "database/ddl_in_sql.html",
  "title": "DDL in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "DDL defines the contract your data must obey. Time spent choosing sensible types and constraints up front is repaid every day afterwards — and because these statements are usually irreversible, they deserve more care than any query you will write."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Data Definition Language is the subset of SQL that creates and changes structure — tables, columns, types, constraints, indexes. It is distinct from DML, which changes the contents . A useful shorthand: DDL is the blueprint, DML is the furniture."
   },
   {
    "t": "What does this module say about “DDL Usually Cannot Be Rolled Back”?",
    "ans": "In most engines (MySQL and Oracle in particular) DDL statements perform an implicit commit : the moment you run one, any open transaction is committed and the change is permanent. A ROLLBACK afterwards will not save you. PostgreSQL is the notable exception — it supports transactional DDL."
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
    "t": "What does this module say about “Quick Context”?",
    "ans": "Data Manipulation Language covers the statements that read and change rows: INSERT , UPDATE , DELETE and SELECT . Where DDL defines the container, DML fills and reshapes its contents."
   },
   {
    "t": "What does this module say about “The Four Statements”?",
    "ans": "UPDATE employees SET salary = 0; is perfectly valid SQL. Without a WHERE , it applies to every row in the table . The same is true of DELETE FROM employees; ."
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
    "t": "What does this module say about “Integers: Pick the Smallest That Fits”?",
    "ans": "Integer types differ only in width, and width sets the range. TINYINT holds −128 to 127 in one byte; INT covers roughly ±2.1 billion in four; BIGINT uses eight."
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
    "ans": "HAVING works without GROUP BY. With no GROUP BY the whole table is one implicit group, so SELECT SUM (amount) FROM sales HAVING SUM (amount) > 5000 returns either one row or none."
   }
  ]
 },
 {
  "path": "database/indexes_in_sql.html",
  "title": "Indexes and Query Performance",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "An index turns a linear scan into a logarithmic descent of a B-tree, which is why an indexed lookup barely notices a table growing a thousand-fold while a scan grows with it exactly. It works only while the query preserves the index's sort order, so a leading wildcard, a function or arithmetic on the column, or an implicit cast will quietly cost you the index and leave the query text looking innocent."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Without an index, finding the rows that match a condition means reading every row and testing it — a full table scan, and its cost grows in a straight line with the size of the table. That is perfectly fine on ten thousand rows and ruinous on ten million."
   },
   {
    "t": "What does this module say about “Why a B-tree”?",
    "ans": "Almost every relational index is a B-tree: a balanced tree whose nodes are disk pages holding many keys each. Every leaf sits at the same depth, so every lookup costs the same. Because a page holds hundreds of keys, the tree is astonishingly shallow — with a fanout of a few hundred, three or four levels is enough for hundreds of millions of rows."
   }
  ]
 },
 {
  "path": "database/limit_and_offset_in_sql.html",
  "title": "Limit and Offset in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "LIMIT and OFFSET slice a result set, but only after ORDER BY has made that set deterministic. Offset pagination is fine for the first few pages and quietly quadratic beyond them — reach for keyset pagination when the data gets big."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "LIMIT n returns at most n rows. OFFSET m throws away the first m rows before it starts counting. Together they cut a window out of a result set, which is how page 3 of a product listing gets built."
   },
   {
    "t": "What does this module say about “Trap 1: LIMIT Without ORDER BY Is Meaningless”?",
    "ans": "SQL tables are unordered sets . Without an explicit ORDER BY , the database may return rows in any order it finds convenient — and that order can change between runs, after an update, or when the query plan changes."
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
    "t": "What does this module say about “Quick Context”?",
    "ans": "NULL is not zero, not an empty string, and not false. It means the value is unknown, and every comparison that touches it inherits that uncertainty: NULL = NULL is not TRUE, it is UNKNOWN. This is three-valued logic , and COALESCE, NULLIF and IS NULL are the tools for working with it on purpose instead of by accident."
   },
   {
    "t": "What does this module say about “Key Takeaway”?",
    "ans": "NULL means unknown, so comparisons involving it are UNKNOWN rather than TRUE or FALSE, and aggregates skip it by default. COALESCE substitutes a default, NULLIF creates a NULL on purpose, and IS NULL is the only comparison that actually works — everything else is a trap that looks like it should work and quietly does not."
   }
  ]
 },
 {
  "path": "database/normalization_in_sql.html",
  "title": "Normalization (1NF, 2NF, 3NF) in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "1NF removes multi-valued columns, 2NF removes columns that depend on only part of a composite key, and 3NF removes columns that depend on another non-key column rather than the key itself. Each step moves a fact into the one table where it is defined once, which is what makes update anomalies structurally impossible rather than merely unlikely."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A denormalized table stores the same fact in more than one place, which means updating it can leave two copies disagreeing. Normalization is a sequence of rules, each one removing a specific kind of redundancy by moving data into its own table."
   },
   {
    "t": "What does this module say about “What usually goes wrong”?",
    "ans": "Over-normalizing has a cost too: every extra table is another join at query time. Reporting and analytics workloads often deliberately denormalize back down for read speed, accepting the redundancy because the data is written once and read constantly. Normalize for correctness where writes happen; consider denormalizing where reads dominate."
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
    "ans": "Sort the sample table by salary and four pairs of rows tie. Those eight rows appear in some order, but nothing in your query asked for it, so nothing guarantees it will be the same order tomorrow. That is what the \"order is decided\" readout is telling you: a sort is only deterministic once the keys you supplied separate every pair of rows."
   }
  ]
 },
 {
  "path": "database/query_execution_order.html",
  "title": "Query Execution Order in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "SQL executes FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT — not the order you write it in. A clause can only reference what an earlier stage has already produced, which is the single rule behind every \"that name doesn't exist here\" error SQL ever gives you."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "SQL is written in one order and executed in another. You write SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT , top to bottom. The engine runs"
   },
   {
    "t": "What does this module say about “Key Takeaway”?",
    "ans": "SQL executes FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT — not the order you write it in. A clause can only reference what an earlier stage has already produced, which is the single rule behind every \"that name doesn't exist here\" error SQL ever gives you."
   }
  ]
 },
 {
  "path": "database/regular_expressions_in_sql.html",
  "title": "Regular Expressions in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Reach for regex when the shape of the text matters and LIKE cannot describe it — validation, extraction, messy-data cleanup. Reach for LIKE when a prefix will do, because it can use an index and regex usually cannot. This lab runs your pattern through a real regex engine, so what matches here is what will match in your database."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A regular expression describes a shape that text may take, rather than the text itself. SQL's LIKE offers exactly two wildcards; regex offers character classes, quantifiers, anchors, alternation and grouping — enough to validate, extract and clean data directly in the database."
   },
   {
    "t": "What does this module say about “Every Engine Spells It Differently”?",
    "ans": "The dialect differences are mostly in the operator name; the pattern syntax itself is broadly POSIX or PCRE and transfers well."
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
    "ans": "The `GROUP BY` clause in SQL is used with aggregate functions (`COUNT`, `SUM`, `AVG`, etc.) to group rows that have the same values in specified columns into summary rows. It's one of the most powerful tools for data analysis."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The `GROUP BY` clause in SQL is used with aggregate functions (`COUNT`, `SUM`, `AVG`, etc.) to group rows that have the same values in specified columns into summary rows. It's one of the most powerful tools for data analysis."
   },
   {
    "t": "What does this module say about “The Core Idea: Collapse and Calculate”?",
    "ans": "Imagine you have a table of sales data. You don't want to see every single sale; you want to know the total sales for each department. `GROUP BY` is how you do this. It performs two main steps:"
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Go beyond `GROUP BY` to perform calculations across sets of rows while keeping the original rows intact. This guide will make you an expert."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Window functions are a powerful feature in SQL that perform a calculation across a set of table rows that are somehow related to the current row. Unlike aggregate functions (`SUM`, `COUNT`), which collapse rows into a single output row, window functions return a value for every single row ."
   },
   {
    "t": "What does this module say about “The Core Idea: A \"Window\" into Your Data”?",
    "ans": "The magic of window functions is the `OVER()` clause. This clause defines the \"window\" or set of rows the function should consider for its calculation. It has two key components:"
   }
  ]
 },
 {
  "path": "database/subqueries_in_sql.html",
  "title": "Subqueries in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A subquery is just a query whose result another query consumes, and its shape is decided by what it returns: one value (scalar), one column (IN), or a table (derived, which must be aliased). An uncorrelated subquery runs once, before the outer query."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "You cannot write WHERE salary > AVG (salary) — an aggregate over the whole table is not something a row-by-row filter can evaluate. What you can do is compute the average in its own query and use the result: that inner query is a subquery."
   },
   {
    "t": "What does this module say about “The four shapes”?",
    "ans": "Compare the two comparisons in the lab. The scalar version asks \"is this person paid more than the company average?\" — one number, computed once, tested against all eight rows. The correlated version asks \"is this person paid more than their own department's average?\" — a different number per row, so the inner query runs eight times."
   }
  ]
 },
 {
  "path": "database/transactions_and_acid.html",
  "title": "Transactions and ACID in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A transaction makes a group of writes behave as one unit: Atomicity guarantees all-or-nothing, Consistency guarantees the result is valid, Isolation controls what concurrent sessions can see of work in progress, and Durability guarantees a commit survives a crash."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A transfer between two accounts is two separate UPDATE statements. If the database crashes between them, one account has lost money and the other never received it — unless the two are wrapped in a transaction, which guarantees they happen together or not at all."
   },
   {
    "t": "What does this module say about “The four letters”?",
    "ans": "READ UNCOMMITTED lets one session see another's uncommitted changes — a \"dirty read\". READ COMMITTED , the default in most engines, blocks that: a session only ever sees data that has actually been committed. Stricter levels (REPEATABLE READ, SERIALIZABLE) exist to stop other classes of anomaly, at a cost in concurrency."
   }
  ]
 },
 {
  "path": "database/union_intersect_except_in_sql.html",
  "title": "UNION, INTERSECT and EXCEPT in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "UNION, INTERSECT and EXCEPT combine the rows two queries return rather than the tables they read from, and every column has to line up in count and type. UNION removes duplicates and costs a sort or hash to do it; UNION ALL keeps them and is cheaper whenever you already know the two sides do not overlap."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A JOIN combines two tables sideways, matching rows on a key and producing wider rows. A set operator combines two result sets vertically — both SELECTs must return the same number of columns, in compatible types, and the output is one column of rows, not a wider table."
   },
   {
    "t": "What does this module say about “Key Takeaway”?",
    "ans": "UNION, INTERSECT and EXCEPT combine the rows two queries return rather than the tables they read from, and every column has to line up in count and type. UNION removes duplicates and costs a sort or hash to do it; UNION ALL keeps them and is cheaper whenever you already know the two sides do not overlap."
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
    "t": "What does this module say about “Schema Flexibility Cuts Both Ways”?",
    "ans": "Press \"Add field to one record\" in each model. In a document store, one document simply gains a field — no migration, no downtime. In the relational model the same change is an ALTER TABLE affecting every row."
   }
  ]
 },
 {
  "path": "database/what_are_relational_databases.html",
  "title": "What are Relational Databases?",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Store each fact once, identify it with a primary key, and reference it with a foreign key. The database then enforces the relationships for you. Flattening everything looks simpler until the first time you have to change something."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A relational database stores data in tables of rows and columns, where every table describes one kind of thing — customers, orders, products — and tables are connected by shared key values rather than by nesting data inside each other."
   },
   {
    "t": "What does this module say about “Keys Are the Whole Trick”?",
    "ans": "That enforcement is called referential integrity , and it is a guarantee the database makes on your behalf — not something your application code has to remember."
   }
  ]
 },
 {
  "path": "database/where_clause_in_sql.html",
  "title": "Where Clause in SQL",
  "cat": "Database",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "WHERE asks one yes/no question of every row — except the answer can also be \"unknown\", and unknown rows are silently dropped. Most WHERE-clause bugs in production are really NULL bugs."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The WHERE clause is a condition tested against each row independently . If it evaluates to TRUE, the row is kept; anything else and it is dropped. That row-at-a-time model is the key mental picture — the database is not filtering \"the table\", it is asking one question of every row."
   },
   {
    "t": "What does this module say about “The NULL Trap: SQL Has Three Truth Values”?",
    "ans": "NULL does not mean zero or empty string — it means unknown . Comparing anything to an unknown gives an unknown result, so manager = 'Ada Lovelace' is neither TRUE nor FALSE for a row where manager is NULL. It is UNKNOWN , and WHERE only keeps TRUE."
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
  "path": "deep_learning/backpropagation.html",
  "title": "Backpropagation and the Computational Graph",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Backpropagation is the chain rule applied to a computational graph in reverse order: each operation contributes only its own local derivative, and the gradient arriving from downstream is multiplied by it on the way past. An add passes the gradient through untouched, a multiply scales it by the other input, and a saturating activation shrinks it — which is where vanishing gradients come from."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Gradient descent needs a gradient: for every weight in the network, how much the loss would change if that weight moved a little. Backpropagation is how that number is obtained, for millions of weights, at the cost of roughly one extra forward pass."
   },
   {
    "t": "What does this module say about “Everything is a graph”?",
    "ans": "A network is a long expression, and any expression can be drawn as a graph of small operations: multiply, add, apply a function. The graph above is a single neuron with two inputs, which is already enough to show every mechanic that matters."
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
    "ans": "Batch Normalization (BatchNorm) was introduced by Ioffe & Szegedy in 2015 and is now a standard building block in virtually every deep network. It normalizes the inputs to each layer so that training is faster and more stable. This page lets you see what happens with and without it."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Instead of processing one sample at a time (stochastic) or the entire dataset (batch), we process data in mini-batches — fixed-size subsets of the training data. This is the standard approach in modern deep learning, balancing computational efficiency, memory constraints, and gradient quality."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Instead of processing one sample at a time (stochastic) or the entire dataset (batch), we process data in mini-batches — fixed-size subsets of the training data. This is the standard approach in modern deep learning, balancing computational efficiency, memory constraints, and gradient quality."
   },
   {
    "t": "What does this module say about “Key Takeaways”?",
    "ans": "Instead of processing one sample at a time (stochastic) or the entire dataset (batch), we process data in mini-batches — fixed-size subsets of the training data. This is the standard approach in modern deep learning, balancing computational efficiency, memory constraints, and gradient quality."
   }
  ]
 },
 {
  "path": "deep_learning/data_sparsity.html",
  "title": "Data Sparsity",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Observe how \"sparse\" data (inputs composed mostly of zeros) propagates. Because multiplying by zero yields zero, pathways originating from dormant inputs become entirely inactive. Combining this with ReLU activations forces massive sections of the network into a dormant state, drastically reducing the number of required computations!"
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Data sparsity occurs when the majority of values in a feature matrix are zero or missing. This is common in NLP (bag-of-words with 100k+ vocab), recommendation systems (user-item matrices), and one-hot encoded categorical features. Sparse data creates unique challenges for neural networks in terms of memory, computation, and gradient flow."
   },
   {
    "t": "What does this module say about “Key Takeaways”?",
    "ans": "Observe how \"sparse\" data (inputs composed mostly of zeros) propagates. Because multiplying by zero yields zero, pathways originating from dormant inputs become entirely inactive. Combining this with ReLU activations forces massive sections of the network into a dormant state, drastically reducing the number of required computations!"
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
  "path": "deep_learning/feature_scaling_in_neural_networks.html",
  "title": "Feature Scaling & Weight Bias",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Feature scaling transforms input features to a common range or distribution. Without it, features with large magnitudes (e.g., salary in thousands) dominate the gradient updates while small-scale features (e.g., age 18–80) are effectively ignored. This creates lopsided weight updates that slow or prevent convergence."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Feature scaling transforms input features to a common range or distribution. Without it, features with large magnitudes (e.g., salary in thousands) dominate the gradient updates while small-scale features (e.g., age 18–80) are effectively ignored. This creates lopsided weight updates that slow or prevent convergence."
   },
   {
    "t": "What does this module say about “Why Neural Networks Need Scaling”?",
    "ans": "Neural networks compute weighted sums: z = w₁x₁ + w₂x₂ + b. If x₁ (age) ranges 18–80 but x₂ (salary) ranges 20,000–200,000, then w₂ needs to be ~1000x smaller than w₁ to produce similar contributions. This creates an extremely elongated loss landscape where gradient descent oscillates along one axis and crawls along the other."
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
    "t": "What does this module say about “Run Training”?",
    "ans": "Steps 1-2 are ordinary. Step 3 injects a spike 50x the real gradient — an exploding gradient, the kind deep or recurrent nets produce on their own."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Most gradients during training are reasonably sized. Occasionally — a badly scaled batch, a long recurrent chain, a numerically unstable loss — one gradient is enormous. Applied directly, w − lr · g can throw a weight far outside the region the optimiser was making sane progress in, and the next few steps are spent recovering rather than learning."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Batch size trades gradient noise against how many times per epoch you get to move."
   },
   {
    "t": "What does this module say about “What usually goes wrong”?",
    "ans": "Raising batch size without touching the learning rate. You get fewer updates per epoch, each no larger than before, so training slows down and people conclude the larger batch \"trains worse\". The usual remedy is the linear scaling rule: double the batch, double the learning rate, within reason."
   },
   {
    "t": "What does this module say about “In one line”?",
    "ans": "Batch size trades gradient noise against how many times per epoch you get to move."
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
    "ans": "Experiment with automated search strategies. Use Grid Search to systematically scan parameters or Random Search to find high-performance zones efficiently."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Hyperparameters are settings defined before training begins — learning rate, batch size, number of layers, dropout rate, etc. Unlike model parameters (weights), they are not learned via gradient descent. Choosing good hyperparameters can be the difference between a model that converges in 10 minutes and one that never converges at all."
   },
   {
    "t": "What does this module say about “Key Takeaways”?",
    "ans": "Experiment with automated search strategies. Use Grid Search to systematically scan parameters or Random Search to find high-performance zones efficiently."
   }
  ]
 },
 {
  "path": "deep_learning/layer_normalization.html",
  "title": "Layer Normalization",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "BatchNorm and LayerNorm are the same normalization idea applied to different axes: BatchNorm down a column, across the batch; LayerNorm across a row, within one sample. That single difference in axis is why LayerNorm works identically at any batch size, including one, while BatchNorm's statistics depend on the batch it happens to see — which is why transformers and RNNs, which often run with small or variable batches..."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "BatchNorm normalizes each feature — each column — using the mean and standard deviation computed across every sample currently in the batch. That is powerful, and it has one structural weakness: its statistics depend on which other examples happen to be in the batch with you, which becomes a real problem at batch size 1 and in architectures like transformers where \"the batch\" is not a stable, meaningful group."
   },
   {
    "t": "What does this module say about “Key Takeaway”?",
    "ans": "BatchNorm and LayerNorm are the same normalization idea applied to different axes: BatchNorm down a column, across the batch; LayerNorm across a row, within one sample. That single difference in axis is why LayerNorm works identically at any batch size, including one, while BatchNorm's statistics depend on the batch it happens to see — which is why transformers and RNNs, which often run with small or variable batches..."
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
    "t": "What does this module say about “What usually goes wrong”?",
    "ans": "Decaying too early. Shrink the step before the model has reached a good region and it will crawl the rest of the way, converging neatly to somewhere mediocre."
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
  "path": "deep_learning/reproducibility_of_model.html",
  "title": "Model Reproducibility",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "True reproducibility means fixing the Random Seed controls both the initial network weights and the order in which data is shuffled during training. Change the seed to see the data sequence entirely rearrange, then switch back to Seed 42 to verify identical structural recovery!"
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Reproducibility means getting the exact same results when you run the same code with the same data. In deep learning, multiple sources of randomness — weight initialization, data shuffling, dropout masks, GPU floating-point non-determinism — make this surprisingly hard. Ensuring reproducibility is critical for debugging, research, and production deployment."
   },
   {
    "t": "What does this module say about “Sources of Randomness”?",
    "ans": "You must seed all random number generators: Python's built-in, NumPy, and PyTorch (both CPU and CUDA)."
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
    "ans": "Watch a head-to-head race! The CPU has low latency but processes sequentially. The GPU has a memory-transfer delay, but processes massive batches in parallel. Adjust the batch size to see who wins."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Deep learning requires massive amounts of mathematical operations (mostly matrix multiplications). To run these efficiently, we use specialized hardware. The choice between a Central Processing Unit (CPU) and a Graphics Processing Unit (GPU) fundamentally changes how data should be batched and processed."
   },
   {
    "t": "What does this module say about “The GPU (Throughput Optimized)”?",
    "ans": "GPUs were originally designed for rendering graphics but are perfectly suited for deep learning."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Classifier body, linear head, distance-based loss — and scale your targets."
   },
   {
    "t": "What does this module say about “The two differences that matter”?",
    "ans": "Everything else — hidden layers, ReLU, backpropagation, the optimiser — is unchanged from a classifier."
   },
   {
    "t": "What does this module say about “A concrete architecture”?",
    "ans": "Predicting house price from three features: 3 inputs → 16 hidden with ReLU → 1 linear output. That is (3×16 + 16) + (16×1 + 1) = 81 parameters."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The shape of the surface, not the cleverness of the algorithm, decides which optimiser looks good."
   },
   {
    "t": "What does this module say about “What the terrain is made of”?",
    "ans": "The folk explanation of training failure is \"it got stuck in a local minimum\". In high dimensions that is mostly wrong. For a point to be a local minimum, the surface must curve upward in every direction at once — and with millions of parameters that is vanishingly unlikely. Saddle points, where it curves up in some directions and down in others, are enormously more common."
   },
   {
    "t": "What does this module say about “Saddles matter more than local minima”?",
    "ans": "The folk explanation of training failure is \"it got stuck in a local minimum\". In high dimensions that is mostly wrong. For a point to be a local minimum, the surface must curve upward in every direction at once — and with millions of parameters that is vanishingly unlikely. Saddle points, where it curves up in some directions and down in others, are enormously more common."
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
    "ans": "Watch how penalties affect the network parameters! Ridge (L2) smoothly shrinks weights toward zero to prevent overfitting. Lasso (L1) drops useless connections EXACTLY to zero (Sparsity). Select both for Elastic Net."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Regularization is any technique that constrains the model to prevent overfitting — learning the training data too well at the expense of new, unseen data. In neural networks, common regularization methods include L1/L2 weight penalties, dropout, data augmentation, and early stopping."
   },
   {
    "t": "What does this module say about “Why Overfitting Happens”?",
    "ans": "Neural networks are extremely flexible function approximators. A network with millions of parameters can easily memorize every sample in the training set, including noise and outliers. The result: near-zero training loss but poor performance on new data. Regularization adds constraints that favor simpler, generalizable solutions."
   }
  ]
 },
 {
  "path": "deep_learning/residual_connections.html",
  "title": "Residual and Skip Connections",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A residual connection adds the block's input back onto its output, which adds a constant 1 to that layer's local derivative during backpropagation. A chain of derivatives all below 1 shrinks geometrically and vanishes; a chain that includes a guaranteed +1 at every step cannot collapse toward zero regardless of how small the learned part's derivative is."
   },
   {
    "t": "What does this module say about “The Stack”?",
    "ans": "every layer squashes its input by the same factor (local derivative 0.55) — realistic for a deep sigmoid/tanh stack"
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Stack enough layers and, by the chain rule, the gradient reaching an early layer is the product of every local derivative between it and the loss. If each of those derivatives is reliably less than 1 — true of sigmoid and tanh almost everywhere — the product shrinks geometrically."
   }
  ]
 },
 {
  "path": "deep_learning/softmax_and_cross_entropy.html",
  "title": "Softmax and Cross-Entropy",
  "cat": "Deep Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Softmax exponentiates the raw scores and divides by their total, turning any set of logits into a probability distribution — monotonic, so the winner never changes, and shift-invariant, which is what makes it numerically safe. Cross-entropy then reduces to minus the log of the probability given to the true class, so a confident mistake is punished without limit while a hedge is not."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A network's final layer produces one raw number per class. These are called logits , and they can be anything: 8.2, −3.1, 0.0. They are not probabilities — they do not sit between 0 and 1 and they do not add up to anything in particular."
   },
   {
    "t": "What does this module say about “Why they are paired”?",
    "ans": "Take the derivative of cross-entropy with respect to the raw logits and almost everything cancels:"
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
    "ans": "During backpropagation, gradients are multiplied through each layer via the chain rule. If these multiplied factors are consistently < 1, gradients shrink to near-zero (vanishing). If > 1, they blow up (exploding). Both make training impossible for deep architectures."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "During backpropagation, gradients are multiplied through each layer via the chain rule. If these multiplied factors are consistently < 1, gradients shrink to near-zero ( vanishing ). If > 1, they blow up ( exploding ). Both make training impossible for deep architectures."
   },
   {
    "t": "What does this module say about “The Chain Rule Problem”?",
    "ans": "For a network with L layers, the gradient of the loss w.r.t. the first layer's weights involves a product of L partial derivatives:"
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
    "ans": "Watch how initialization impacts training flow! Poor choices cause deep networks to die/vanish (Blue) or explode (Red). Select a method below (like He Normal) or use Batch Normalization to lock gradients into a stable variance (Green) even with bad initial weights."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Neural network weights must be initialized before training begins. The initialization strategy determines the scale and distribution of starting weights, which directly affects whether gradients flow properly through the network or vanish/explode in the first few iterations."
   },
   {
    "t": "What does this module say about “Why Not Initialize to Zero”?",
    "ans": "If all weights are zero (or any constant), every neuron in a layer computes the exact same output . During backpropagation, they all receive the same gradient and update identically. The network never breaks this symmetry — it's equivalent to having a single neuron per layer."
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
  "path": "gen_ai/bm25_and_sparse_retrieval.html",
  "title": "BM25 and Sparse Lexical Retrieval",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "BM25 scores a document by summing, over each query term it contains, that term's rarity across the corpus times a saturating function of how often it appears, normalised by document length. b controls how much long documents are penalised for being long; k1 controls how much repeated terms are rewarded before diminishing returns kick in."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Before dense vector search , and still running alongside it in most real systems, is sparse lexical search: score a document by which query terms it contains, weighted by how informative each term is. BM25 is the version of this idea that actually works well, and it needs no training, no GPU, and no embedding model."
   },
   {
    "t": "What does this module say about “Why it still matters next to embeddings”?",
    "ans": "BM25 gets exact terms right where embeddings can blur them — product codes, error messages, names, acronyms. It is also completely interpretable: every score decomposes into per-term contributions, which is why the breakdown panel above can show exactly where a score came from. This is the sparse half of the hybrid search that most production RAG systems actually run."
   }
  ]
 },
 {
  "path": "gen_ai/byte_pair_encoding_tokenizer.html",
  "title": "Byte Pair Encoding Tokenizer",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "BPE is a compression algorithm repurposed as a vocabulary builder: merge what is frequent, leave the rest in pieces. This lab runs the genuine training loop on whatever corpus you paste in — the merge table you see is the actual product of counting pairs, not a stored example. Real tokenizers add byte-level fallbacks and pre-tokenization rules, but the core loop is exactly this."
   },
   {
    "t": "What does this module say about “The Two Failure Modes It Avoids”?",
    "ans": "BPE lands in between: frequent words become single tokens, rare words split into meaningful pieces, and nothing is ever out-of-vocabulary."
   },
   {
    "t": "What does this module say about “The Algorithm, in Four Lines”?",
    "ans": "That is the entire method. Vocabulary size is simply base characters plus the number of merges — which is why it is an exact dial rather than something you discover after the fact."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Fixed-size chunking is simple and fast but blind to meaning, and will cut sentences in half whenever the count lands mid-sentence. Semantic chunking respects real boundaries at the cost of variable chunk sizes. Overlap recovers some of the context lost at any boundary by duplicating a small window of text between neighbouring chunks."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Every piece of RAG downstream of chunking — embedding, indexing, retrieval, reranking — operates on whatever the chunk boundaries produced. Cut a sentence in half and both halves lose the context that made the original sentence meaningful; the embedding of a fragment is not a fragment of the embedding."
   },
   {
    "t": "What does this module say about “Fixed-size vs semantic”?",
    "ans": "Fixed-size chunking counts a fixed number of words or tokens and cuts there, with no regard for what is at that position — a heading, mid-word, mid-sentence, anywhere. It is simple, predictable, and blind. Semantic chunking respects natural boundaries — sentences, paragraphs, headings — and only splits at those boundaries, accepting some variation in chunk size in exchange for every chunk being a coherent unit."
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
  "path": "gen_ai/dot_product_vs_cosine_similarity.html",
  "title": "Dot Product vs Cosine Similarity for Retrieval",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Cosine similarity divides out vector length and only ever measures direction; dot product does not, so it rewards longer vectors regardless of whether that length means anything. The two metrics agree only when every vector has the same length — true if you normalise your embeddings to unit length, false otherwise."
   },
   {
    "t": "What does this module say about “Stretch Doc B”?",
    "ans": "same direction as before, just longer — like a verbose, repetitive document embedding"
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Cosine similarity asks \"what angle apart are these two vectors\" and ignores length entirely. Dot product asks \"how much do these two vectors agree, weighted by how long they both are\" — length is part of the answer, not discarded."
   }
  ]
 },
 {
  "path": "gen_ai/embeddings_and_vector_search.html",
  "title": "Embeddings and Vector Search",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "An embedding puts meaning somewhere in space, so similarity becomes geometry and retrieval becomes nearest-neighbour search, ranked by cosine because vector length carries length rather than meaning. Exact search costs one comparison per document and does not survive scale, so production indexes partition the space and probe only the nearest few cells — buying a large drop in work for a small, measurable chance of mi..."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "An embedding model maps a piece of text to a point, arranged so that texts about the same thing land near each other. Nothing about the words themselves survives the trip — \"peel a mango\" and \"how to prepare tropical fruit\" share no vocabulary and end up as neighbours anyway."
   },
   {
    "t": "What does this module say about “Cosine, and why it is the default”?",
    "ans": "Retrieval almost always ranks by cosine similarity : the angle between the query vector and the document vector, ignoring how long either one is. Length in an embedding tends to carry things like document length or token count rather than meaning, so ignoring it is the point."
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
    "t": "What does this module say about “What actually helps”?",
    "ans": "What does not help: asking the model whether it is sure. Self-reported confidence is generated by the same process that produced the answer, and is largely uncorrelated with being right."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Hybrid search runs dense and sparse retrieval independently and fuses their rankings rather than their scores, because the two methods' raw numbers are not on comparable scales. Reciprocal Rank Fusion rewards documents both methods rank well, which makes the combined system more robust than either retrieval method alone — a document only one method loves can be outranked by one both methods merely like."
   },
   {
    "t": "What does this module say about “Fusion”?",
    "ans": "small k lets rank-1 dominate; large k (60 is the common default) smooths everything out"
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Dense retrieval and BM25 fail in different, mostly non-overlapping ways. A document phrased differently from the query but on the same topic can score well under a dense method and poorly under exact keyword match; a document with an unusual acronym or exact code can score well under BM25 and be embedded ambiguously."
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
  "path": "gen_ai/quantization_in_llms.html",
  "title": "Quantization in LLMs",
  "cat": "Gen AI",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Quantization buys memory and speed with precision. The surprise is how cheap the trade is: 8-bit is usually indistinguishable from full precision, and modern 4-bit methods come remarkably close. The size numbers here count weights only — real deployments also need memory for activations and the KV cache, which grows with context length."
   },
   {
    "t": "What does this module say about “The Core Idea: A Coarser Ruler”?",
    "ans": "A 32-bit float can express billions of distinct values. An 8-bit integer can express 256, and a 4-bit integer just 16. Quantization finds the range your weights actually occupy and divides it into that many evenly spaced levels:"
   },
   {
    "t": "What does this module say about “Symmetric vs Asymmetric”?",
    "ans": "Toggle between them with the outlier enabled and watch the step size and RMS error change."
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
    "ans": "Precision@k and Recall@k describe a set — how much of what you returned was right, and how much of what was right did you return — and are blind to the order within that set. MRR and nDCG describe a ranking , and reward relevant results for showing up earlier."
   },
   {
    "t": "What does this module say about “Ranking”?",
    "ans": "all three rankings retrieve exactly the same 5 relevant / 5 irrelevant documents"
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Every retrieval method on this site — vector search , BM25 , the two combined — needs a way to say whether it actually worked. That requires a labelled test set: queries with a known correct set of relevant documents, checked against what the system actually returned."
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
    "t": "What is meant by “It's a Measure of Direction, Not Size” here?",
    "ans": "Cosine similarity ignores the magnitude (or length) of the vectors and only considers their orientation in space."
   },
   {
    "t": "What is meant by “The Range is [-1, 1]” here?",
    "ans": "A score of +1 means identical direction, 0 means they are unrelated (orthogonal), and -1 means they are exact opposites."
   },
   {
    "t": "What is meant by “Foundation for NLP” here?",
    "ans": "This is the primary way we measure the similarity between words, sentences, and entire documents after they have been converted into vector embeddings (like Word2Vec or BERT embeddings)."
   },
   {
    "t": "What is meant by “Powers Recommendation Engines” here?",
    "ans": "It's used to find similar users or items. If your vector of movie ratings is similar to someone else's, the engine might recommend movies you haven't seen that they liked."
   }
  ]
 },
 {
  "path": "machine_learning/decision_tree.html",
  "title": "Decision Tree Analysis",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What is meant by “Greedy Algorithm” here?",
    "ans": "ID3 is a \"greedy\" algorithm. At each step, it picks the split that looks best at that moment (the one with the highest Information Gain) without looking ahead to see if a different choice might lead to a better overall tree."
   },
   {
    "t": "What is meant by “Interpretability is a Superpower” here?",
    "ans": "The final tree structure is easy for humans to read and understand. You can trace the path for any new data point to see exactly how the model arrived at its prediction."
   },
   {
    "t": "What is meant by “Foundation for Advanced Models” here?",
    "ans": "While simple, decision trees are the building blocks for more powerful ensemble models like Random Forests and Gradient Boosted Trees (like XGBoost)."
   },
   {
    "t": "What is meant by “Overfitting Risk” here?",
    "ans": "If a decision tree is grown too deep, it can perfectly memorize the training data, including its noise. This leads to overfitting. Techniques like pruning or setting a maximum depth are used to combat this."
   }
  ]
 },
 {
  "path": "machine_learning/evaluation_metrics_for_regression.html",
  "title": "Evaluation Metrics for Regression",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “The Four Key Metrics”?",
    "ans": "Each metric tells a slightly different story about your model's errors. The interactive plot above shows the true data points (green dots), the model's prediction line (orange), and the errors, or residuals (dashed red lines), which are the distances between each true point and the line."
   },
   {
    "t": "What does this module say about “Mean Absolute Error (MAE)”?",
    "ans": "What it is: The average of the absolute differences between the true values and the predicted values. Formula: $ \\frac{1}{n} \\sum_{i=1}^{n} |y_i - \\hat{y}_i| $ Interpretation: It tells you, on average, how far off your predictions are. It's easy to understand because it's in the same units as the target variable. It treats all errors equally, big or small."
   },
   {
    "t": "What does this module say about “Mean Squared Error (MSE)”?",
    "ans": "What it is: The average of the squared differences between the true and predicted values. Formula: $ \\frac{1}{n} \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2 $ Interpretation: By squaring the errors, MSE penalizes larger errors much more heavily than smaller ones. This makes it sensitive to outliers. Its units are squared, which can make it hard to interpret directly."
   }
  ]
 },
 {
  "path": "machine_learning/gradient_boosting.html",
  "title": "Gradient Boosting",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Gradient boosting fits each new small tree to the residuals left by everything built so far, then adds a fraction of it to the running prediction — which is gradient descent performed in function space, with the learning rate as the step size."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A random forest builds many strong trees independently and averages away their variance. Boosting does close to the opposite: it builds many deliberately weak trees in sequence, each one aimed squarely at the mistakes the previous ones left behind."
   },
   {
    "t": "What does this module say about “The loop”?",
    "ans": "The residual panel above is step 2 made visible. Watch it after each tree: the bars shrink, and where they are still tall is exactly where the next tree will spend its capacity."
   }
  ]
 },
 {
  "path": "machine_learning/hard_vs_soft_labelling.html",
  "title": "Hard vs Soft Labelling",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “Defining the Labels”?",
    "ans": "Imagine you're training a model to classify the sentiment of a tweet as 'Negative', 'Neutral', or 'Positive'. How you tell the model the \"correct\" answer for each tweet is where labelling strategy comes in."
   },
   {
    "t": "What does this module say about “Hard Labelling (One-Hot Encoding)”?",
    "ans": "This is the most common approach. You are 100% certain about the class. The correct class gets a value of 1, and all other classes get a 0. It's a \"winner-takes-all\" method. Example Vector: For a 'Positive' tweet, the hard label is [0, 0, 1] . This tells the model, \"This tweet is positive, and nothing else.\""
   },
   {
    "t": "What does this module say about “Soft Labelling (Probabilistic)”?",
    "ans": "This method acknowledges that the world is messy and some data points are ambiguous. Instead of picking one class, you assign a probability distribution across all classes. Example Vector: For a tweet that is mostly positive but has a hint of neutrality, the soft label might be [0.1, 0.2, 0.7] ."
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
    "t": "What is meant by “Sensitivity to Initialization” here?",
    "ans": "Since the initial centroids are placed randomly, you might get different final clusters if you run the algorithm multiple times. This is why in practice, K-Means is often run several times with different random initializations."
   },
   {
    "t": "What is meant by “Speed and Scalability” here?",
    "ans": "K-Means is very fast and computationally efficient, making it an excellent choice for large datasets."
   },
   {
    "t": "What is meant by “Assumptions” here?",
    "ans": "The algorithm assumes that clusters are spherical, of similar size, and have similar density. When these assumptions are violated (like with the moons or circles), it performs poorly."
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
    "t": "What does this module say about “How It Works: Building the Vocabulary”?",
    "ans": "The process is straightforward and consists of two main steps, which you can see in action by clicking the \"Encode Corpus\" button above."
   },
   {
    "t": "What does this module say about “Create a Vocabulary”?",
    "ans": "First, the encoder scans the entire input text (the \"corpus\") to find all unique words (or \"tokens\"). It then sorts these unique words alphabetically to create a consistent vocabulary. This vocabulary acts as a dictionary or a look-up table."
   },
   {
    "t": "What does this module say about “Assign Integer IDs”?",
    "ans": "Once the vocabulary is built, the encoder assigns a unique integer ID to each word, starting from 0. The first word in the sorted vocabulary gets ID 0, the second gets ID 1, and so on. The final output is a sequence of these integer IDs, representing the original text."
   }
  ]
 },
 {
  "path": "machine_learning/label_imbalance_problem.html",
  "title": "Label Imbalance Problem",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “What is the Accuracy Paradox”?",
    "ans": "The Accuracy Paradox occurs when a model achieves a very high accuracy score but is completely useless in practice. This happens because the model learns to simply predict the majority class every single time. In a dataset with 99% normal transactions and 1% fraudulent ones, a model that always guesses \"normal\" will be 99% accurate. It sounds great, but it has failed at its one important job: detecting fraud."
   },
   {
    "t": "What does this module say about “The \"Naive\" Model”?",
    "ans": "This is a deliberately dumb model. Its only rule is: always predict Class 0 (the majority class) . It never predicts an anomaly. As you'll see, its accuracy is deceptively high."
   },
   {
    "t": "What does this module say about “The Standard Trained Model”?",
    "ans": "This is a standard Logistic Regression model. It tries to learn a decision boundary to separate the two classes based on the data. Watch how its behavior and metrics change as the dataset becomes more imbalanced."
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
    "t": "What does this module say about “Types of Drift”?",
    "ans": "This occurs when the fundamental relationship between the input variables and the target variable changes. The \"rules of the game\" have changed. In the visualization, the green dashed line (the true underlying pattern) will slowly change its shape over time, while the data points continue to follow it. The deployed model ( red line ), which learned the original pattern, becomes increasingly wrong."
   },
   {
    "t": "What does this module say about “Concept Drift”?",
    "ans": "This occurs when the fundamental relationship between the input variables and the target variable changes. The \"rules of the game\" have changed. In the visualization, the green dashed line (the true underlying pattern) will slowly change its shape over time, while the data points continue to follow it. The deployed model ( red line ), which learned the original pattern, becomes increasingly wrong."
   },
   {
    "t": "What does this module say about “Data Drift (Covariate Shift)”?",
    "ans": "This occurs when the distribution of the input data changes, even if the underlying concept remains the same. The model starts seeing data it has never encountered before. In the visualization, the green dashed line will remain static, but the blue data points will drift horizontally into a new region."
   }
  ]
 },
 {
  "path": "machine_learning/naive_bayes.html",
  "title": "Naive Bayes Classifier",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “The \"Naive\" Assumption: A Key Simplification”?",
    "ans": "The \"naive\" part of the name comes from a key assumption the algorithm makes: it assumes that all features are independent of each other . In our example, it assumes that the 'Outlook' has no effect on the 'Temperature' or 'Wind'. While this is often not true in the real world (a sunny outlook usually implies hotter temperatures), this simplification makes the calculations much easier and faster."
   },
   {
    "t": "What does this module say about “The Calculation Process: A Walkthrough”?",
    "ans": "The interactive panel walks you through the exact steps the algorithm takes to make a prediction. Let's use the default input: Outlook=Sunny, Temp=Cool, Wind=Strong ."
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
  "path": "machine_learning/roc_curve_and_auc.html",
  "title": "ROC Curve and AUC",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The ROC curve plots true positive rate against false positive rate across every possible threshold, which separates two questions that accuracy tangles together: how well the model ranks, and where you choose to cut. AUC summarises only the first, and equals the probability that a random positive outscores a random negative — so it is unchanged by the threshold and nearly unchanged by class imbalance."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A classifier does not really output a class. It outputs a score — a probability, usually — and something else turns that into a label by comparing it against a threshold. The confusion matrix describes one such threshold. Change the threshold and you get a different matrix from the very same model."
   },
   {
    "t": "What does this module say about “What AUC actually measures”?",
    "ans": "The area under the curve has an interpretation worth memorising, because it is far more intuitive than \"area\":"
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Both methods add a penalty on coefficient size to the loss, trading a little training accuracy for a lot of stability, with lambda controlling how hard that trade is pushed. Ridge squares the weights, so its pressure fades as a coefficient nears zero and everything merely shrinks; Lasso uses absolute values, so its pressure stays constant and weak coefficients are driven to exactly zero, which makes it a feature sele..."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Give a degree-12 polynomial eighteen noisy points and it will pass through nearly all of them. The fit looks superb on the data it has seen, and it is worthless: between the points the curve swings violently, because the only way to hit every point is to use enormous coefficients that cancel each other out."
   },
   {
    "t": "What does this module say about “One extra term”?",
    "ans": "Ordinary least squares minimises the squared error alone. Ridge and Lasso add a penalty on the size of the weights:"
   }
  ]
 },
 {
  "path": "machine_learning/sliding_window_for_timeseries_data.html",
  "title": "Sliding Window for Time Series",
  "cat": "Machine Learning",
  "q": [
   {
    "t": "What does this module say about “What is the Sliding Window Technique”?",
    "ans": "The sliding window method is a fundamental technique for transforming a time series dataset into a format suitable for supervised machine learning. It involves moving a \"window\" of a fixed size over the data, creating input-output pairs. For each window, the data inside becomes the input (features), and the data point(s) immediately following the window becomes the output (target)."
   },
   {
    "t": "What does this module say about “Core Parameters Explained”?",
    "ans": "Two key parameters control how the windows are created. Understanding them is crucial for success:"
   },
   {
    "t": "What does this module say about “Hands-On with the Interactive Panel”?",
    "ans": "Use the visualization above to build a concrete understanding of these parameters:"
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
    "t": "What does this module say about “Quick Context”?",
    "ans": "Training on Label Imbalanced Dataset belongs to machine learning . Build intuition first, then precision."
   },
   {
    "t": "What does this module say about “What This Topic Is Really About”?",
    "ans": "This topic explains why models can appear accurate while still failing on the minority class. With imbalance, the model may learn to favor the majority and miss the rare but important cases."
   },
   {
    "t": "What does this module say about “Why This Matters in Real Work”?",
    "ans": "Fraud detection, disease screening, and safety monitoring all care more about minority detection than raw accuracy. A model with high overall accuracy can still be risky if minority recall is poor."
   }
  ]
 },
 {
  "path": "maths/matrix_as_transformation.html",
  "title": "A Matrix is a Transformation",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A matrix is a record of where the basis vectors land, stored as its columns, and because linear transformations keep grid lines straight and evenly spaced that record determines where every other vector goes. This makes the multiplication rule a derivation rather than a convention: transforming (x, y) means taking x copies of the first column plus y copies of the second."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Most people first meet a matrix as a grid of numbers with rules for multiplying it. The rules work, but they explain nothing, and matrix multiplication in particular looks arbitrary — why rows against columns, and why in that order?"
   },
   {
    "t": "What does this module say about “The columns are the whole story”?",
    "ans": "Start with the two basis vectors: î = (1, 0) pointing along x, and ĵ = (0, 1) pointing along y. Every vector is built from them — (3, 2) means \"3 of î plus 2 of ĵ\"."
   }
  ]
 },
 {
  "path": "maths/bayes_theorem.html",
  "title": "Bayes' Theorem",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Evidence updates a prior; it does not replace it. When a condition is rare, even an excellent test produces mostly false positives, because the healthy majority is so much larger. Always ask how common the thing was before the evidence arrived."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Bayes' theorem takes a prior belief and revises it in light of new evidence. It is the mathematics of changing your mind correctly."
   },
   {
    "t": "What does this module say about “Count People, Not Percentages”?",
    "ans": "The grid shows 10,000 people, one square each. With a 1% base rate and a 99% accurate test:"
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
    "ans": "Probability counts favourable outcomes against all possible outcomes. Conditional probability changes one thing: it shrinks what counts as possible."
   },
   {
    "t": "What does this module say about “P(A|B) is not P(B|A)”?",
    "ans": "This is worth stating in its own section because it causes more real-world damage than any other confusion in probability."
   }
  ]
 },
 {
  "path": "maths/covariance_and_correlation.html",
  "title": "Covariance and Correlation",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Covariance averages the product of each variable's deviation from its own mean, so it is positive when two variables move together and negative when they move oppositely — but it carries the units of both, which makes its magnitude meaningless on its own. Correlation divides by both standard deviations to strip the units out, giving a number always between −1 and 1 that is unchanged by rescaling."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Variance describes how one variable spreads out. Covariance is the same idea for two: when x is above its mean, is y usually above its mean too?"
   },
   {
    "t": "What does this module say about “Why correlation exists”?",
    "ans": "Covariance has a fatal flaw for reporting: it carries the units of both variables multiplied together. Measure height in metres and weight in kilograms and you get one number; switch height to centimetres and the same data gives a number a hundred times larger. Nothing about the relationship changed."
   }
  ]
 },
 {
  "path": "maths/cross_entropy_and_kl_divergence.html",
  "title": "Cross-Entropy and KL Divergence",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Cross-entropy H(p, q) is what your beliefs cost when reality is p, entropy H(p) is the part of that cost no model could avoid, and the KL divergence is the difference — the waste that is genuinely your model's fault. KL is never negative and is zero only when q matches p exactly, so minimising cross-entropy and minimising divergence are the same job."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Entropy is the average surprise of a distribution — the shortest average code length you could achieve if you knew the true probabilities. Cross-entropy asks a harsher question: what does it cost if you build your code for q and the data actually comes from p?"
   },
   {
    "t": "What does this module say about “Why classifiers use it”?",
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
    "t": "What does this module say about “When cosine is the right answer”?",
    "ans": "Cosine dominates text and embedding work, and the reason is specific. In a bag-of-words representation, a long document has larger counts everywhere than a short one on the same subject. Euclidean distance reads that as \"far apart\"; cosine reads the direction of the vector — the mix of words rather than the volume — and correctly calls them similar."
   }
  ]
 },
 {
  "path": "maths/eigenvalues_and_eigenvectors.html",
  "title": "Eigenvalues and Eigenvectors",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "An eigenvector is a direction a transformation does not rotate, and its eigenvalue is the factor it is stretched by, so along an eigenvector the whole matrix collapses into a single multiplication. For a 2×2 matrix they follow from the trace and determinant alone, and always satisfy λ₁+λ₂ = trace and λ₁λ₂ = det; a negative discriminant means no real eigenvectors exist, which is exactly the case for a rotation."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "A matrix moves space . Almost every vector it touches gets both stretched and rotated — it comes out pointing somewhere new."
   },
   {
    "t": "What does this module say about “Finding them”?",
    "ans": "For a 2×2 matrix the eigenvalues come straight out of two numbers you can read off by eye:"
   }
  ]
 },
 {
  "path": "maths/entropy_and_information.html",
  "title": "Entropy and Information",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Entropy is the average surprise of a distribution, −Σp·log(p), and reads as the number of yes/no questions needed to pin down the outcome. It is maximal when every outcome is equally likely and exactly zero when one outcome is certain, which is why it works as a measure of uncertainty."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Suppose I am about to tell you the outcome of an event, and you want to know how much you are about to learn. If the event is a coin flip, you will learn something. If it is \"will the sun rise tomorrow\", you will learn essentially nothing, because you already knew."
   },
   {
    "t": "What does this module say about “Surprise first”?",
    "ans": "Start with a single outcome. How surprising is it? Two things should be true: a certain outcome (p = 1) should carry zero surprise, and rarer outcomes should be more surprising. One function does this cleanly:"
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
  "path": "maths/exponentials.html",
  "title": "Exponentials",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Exponentials multiply rather than add, so they have a constant doubling time and eventually beat any polynomial. Bases above 1 explode, bases below 1 decay toward zero, and base e is the one whose slope equals its value — which is why it underlies softmax, sigmoid and every decay schedule you will configure."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "In y = b^x the variable sits in the exponent . Each step of 1 in x multiplies y by b, rather than adding to it. That single difference is what separates exponential from linear behaviour."
   },
   {
    "t": "What does this module say about “Exponential Always Wins Eventually”?",
    "ans": "Keep the polynomial comparison on and look at the left of the plot: x³ is far ahead. Now slide x rightward. There is a crossover point, and after it 2^x leaves x³ hopelessly behind."
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
    "t": "What does this module say about “Key Takeaway”?",
    "ans": "The identity is the matrix that changes nothing, and the inverse is the one that undoes A — defined by A A⁻¹ = I and computed by dividing through by the determinant, which is precisely why a zero determinant means no inverse exists: the transformation destroyed information and no matrix can recover it."
   }
  ]
 },
 {
  "path": "maths/information_gain.html",
  "title": "Information Gain",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Information gain is the drop in entropy a split buys: the parent's entropy minus the size-weighted average of its children's. The weighting is what stops a tiny lucky child from looking impressive, and the gain is zero exactly when the split leaves the label mix unchanged."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Entropy measures how mixed a set of labels is: 1 bit for an even fifty-fifty split of two classes, 0 bits when every label is the same. Information gain is simply how much that number falls when you split the set in two."
   },
   {
    "t": "What does this module say about “Gini, and why the choice barely matters”?",
    "ans": "Many implementations measure impurity with the Gini index, 1 − Σ pᵢ² , rather than entropy. Both are zero for a pure node and maximal for an even mix; Gini avoids a logarithm and is marginally cheaper. In practice the two pick the same split the overwhelming majority of the time, and scikit-learn's default of Gini is a performance decision, not a statistical one."
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
  "path": "maths/matrix_multiplication.html",
  "title": "Matrix Multiplication",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Row against column, multiply and add, repeat for every output cell. The inner dimensions must agree, the order cannot be swapped, and the cost grows cubically — three facts that explain tensor errors, layer ordering and the entire GPU industry."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Multiplying two matrices produces a new matrix in which every single entry is a dot product — one row of the left matrix against one column of the right. Nothing more complicated is happening."
   },
   {
    "t": "What does this module say about “The Rule for a Single Cell”?",
    "ans": "Click any cell in C and the app highlights the blue row and amber column that feed it, then writes out the arithmetic term by term. Every cell is independent of every other — which is precisely why this operation parallelises so well on a GPU."
   }
  ]
 },
 {
  "path": "maths/maximum_likelihood_estimation.html",
  "title": "Maximum Likelihood Estimation",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Maximum likelihood picks the distribution that makes the observed data least surprising, by holding the data fixed and varying the parameters — the reverse of a probability question. The likelihood is the product of each point's density, and because that product underflows to zero on any real sample, it is always computed as a sum of logarithms instead, which is safe because the logarithm is monotonic."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "You have some data and a family of distributions that might have produced it. Which member of the family should you pick?"
   },
   {
    "t": "What does this module say about “Likelihood is not probability”?",
    "ans": "The two words get used interchangeably in conversation and they are not the same thing."
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
    "t": "What does this module say about “Quick Context”?",
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Hold every other variable still to get a partial derivative; collect the partials to get the gradient. It points uphill, its length measures steepness, and stepping against it is what training a neural network literally means."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Standing on a hillside, \"how steep is it?\" has no single answer — it depends which way you face. A partial derivative answers it for one fixed direction; the gradient bundles those answers into a vector pointing straight up the slope."
   },
   {
    "t": "What does this module say about “Partials: Freeze Everything Else”?",
    "ans": "To compute ∂f/∂x you treat y as a constant and differentiate normally. That is the whole idea — you are asking how f changes if you step east while refusing to move north."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The projection of b onto a is ((a·b)/‖a‖²)a : the point on the line through a that is closest to b, and the only one whose residual is perpendicular to a. Only a's direction matters, so scaling a changes nothing; the scale factor goes negative when the shadow falls behind the origin, zero when the vectors are perpendicular, and equals b exactly when they are parallel."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Projection answers one question: of all the points on the line through a, which is closest to b? The answer is b's shadow, and the line from b down to that shadow is perpendicular. Those two facts — closest point, perpendicular error — are the same fact, and almost every fitting method in machine learning is built on it."
   },
   {
    "t": "What does this module say about “Why this is the root of least squares”?",
    "ans": "Fitting a line to data means solving Xw = y when there is no exact solution: y almost never lies in the space that the columns of X can reach. The best you can do is find the point in that space closest to y — which is the projection of y onto the column space of X."
   }
  ]
 },
 {
  "path": "maths/rank_and_linear_independence.html",
  "title": "Rank and Linear Independence",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Rank counts the independent directions a matrix's columns actually provide, which is the dimension of everything they can reach. Full rank means the span is as large as it could be and the matrix is invertible; a drop in rank means one column was a combination of the others, the determinant is zero, and both the inverse and the unique solution to Ax = b disappear together."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Two columns are linearly independent when neither one can be built out of the other. When they are, the combinations s·c₁ + t·c₂ sweep out the whole plane. When one is a multiple of the other, everything you can build lies on a single line, no matter how hard you pull on s and t."
   },
   {
    "t": "What does this module say about “Key Takeaway”?",
    "ans": "Rank counts the independent directions a matrix's columns actually provide, which is the dimension of everything they can reach. Full rank means the span is as large as it could be and the matrix is invertible; a drop in rank means one column was a combination of the others, the determinant is zero, and both the inverse and the unique solution to Ax = b disappear together."
   }
  ]
 },
 {
  "path": "maths/the_chain_rule.html",
  "title": "The Chain Rule",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Nested functions multiply their slopes. That gives you the derivative of arbitrarily deep compositions — and because multiplication compounds, it also explains why gradients vanish or explode in deep networks."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "When a function feeds into another — y = f(g(x)) — a change in x must travel through both to reach y . The chain rule says the sensitivities simply multiply."
   },
   {
    "t": "What does this module say about “The Gear Analogy”?",
    "ans": "Picture two gears. Turning the first makes the second turn 3× as fast; that second gear drives a third at 2×. Turn the first gear once and the last one spins 6 times — the ratios multiplied."
   }
  ]
 },
 {
  "path": "maths/the_normal_distribution.html",
  "title": "The Normal Distribution",
  "cat": "Maths",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Two parameters describe the entire curve, area equals probability, and 68/95/99.7 holds universally. The central limit theorem is why the shape is so common — but its thin tails mean it is the wrong model whenever extreme events actually matter."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The normal (or Gaussian) distribution is the familiar bell curve: symmetric, single-peaked, thin-tailed. It is completely specified by just two numbers — the mean μ sets where it sits, and the standard deviation σ sets how wide it is."
   },
   {
    "t": "What does this module say about “Two Knobs, Nothing Else”?",
    "ans": "That fixed unit area is what makes it a probability density: area under a stretch of the curve is the probability of landing in that range."
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
    "t": "What does this module say about “Key Takeaway”?",
    "ans": "BPTT = unroll the loop, backpropagate through the chain, sum the shared-weight gradients. It makes RNNs trainable — but it also chains together T multiplications, and a long product of numbers below 1 races toward zero. That arithmetic inevitability is the vanishing gradient problem."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Encoder-only and decoder-only transformers differ by one thing: whether the attention mask deletes the upper triangle. Bidirectional attention lets every token see the whole sequence, which rules out next-token prediction and demands a masked objective instead, and yields strong representations with no ability to generate."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Both families are stacks of the same block: multi-head attention and a feed-forward layer, repeated. The difference is a mask applied inside self-attention — a matrix of minus infinities that deletes some of the attention scores before the softmax."
   },
   {
    "t": "What does this module say about “Why the mask decides the objective”?",
    "ans": "A model that can see the future cannot be trained to predict it. If position 4 can attend to position 5, then \"predict the token at position 5\" is answered by copying it, and nothing is learned. So the two masks admit different training tasks."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "RNNs are designed for sequential data like text. Their core feature is the hidden state , a memory that is passed through time, allowing the network to remember previous inputs and understand context. By using shared weights, they can efficiently process sequences of any length, making them a cornerstone of modern Natural Language Processing."
   },
   {
    "t": "What does this module say about “The Power of Memory in Language”?",
    "ans": "Standard neural networks have a major limitation: they have no memory of the past. They process each input independently. This is a problem for language, where the order of words is crucial. For example, \"dog bites man\" and \"man bites dog\" use the same words but have completely different meanings."
   },
   {
    "t": "What does this module say about “The Unrolled RNN: Step-by-Step Processing”?",
    "ans": "The visualization above \"unrolls\" the RNN loop, showing it as a sequence of identical cells, one for each word (or \"time step\"). Here’s how the information flows:"
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Nobody writes down that \"cat\" is like \"dog\" — the geometry is learned from co-occurrence statistics alone . Random vectors plus a pull-together/push-apart rule over enough text yields a space where distance encodes meaning. Scale the same principle up and you get the embedding layers inside every modern language model."
   },
   {
    "t": "What does this module say about “The Distributional Hypothesis”?",
    "ans": "\"You shall know a word by the company it keeps\" (J.R. Firth, 1957). Words that appear in similar contexts tend to mean similar things — \"cat\" and \"dog\" both follow \"the\", precede \"chased\", appear near \"pet\". Embedding training is simply this idea turned into an optimization: make words with shared contexts have similar vectors."
   },
   {
    "t": "What does this module say about “The Training Loop”?",
    "ans": "Methods like word2vec's skip-gram never see a definition of any word. The loop is:"
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "ANNs don't fail on sequences because they are weak — they fail because their architecture makes three promises (fixed size, unordered input, stateless processing) that sequential data breaks. Recurrent networks are the structural fix: variable-length input consumed one step at a time, with a hidden state that remembers."
   },
   {
    "t": "What does this module say about “The Setup”?",
    "ans": "A classic feed-forward network (ANN / MLP) is a brilliant function approximator — for fixed-size, unordered inputs. Sequential data violates both assumptions at once: sentences have different lengths, and their meaning lives in the ordering. The result is three distinct failure modes."
   },
   {
    "t": "What does this module say about “Limitation 1: The Input Layer is a Fixed-Width Door”?",
    "ans": "The first layer of an ANN has a hard-coded number of neurons. A 6-slot network offers exactly two bad options for real text: truncate longer inputs (information destroyed before learning even starts) or pad shorter ones with dummy values (the network wastes capacity learning to ignore filler). There is no third option — the architecture physically cannot stretch."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "N-grams are a simple but effective method for capturing local context in text by breaking it into small, overlapping chunks. While modern deep learning models use more sophisticated techniques, n-grams remain a foundational concept for understanding how machines begin to process and find patterns in human language."
   },
   {
    "t": "What does this module say about “What are N-grams”?",
    "ans": "An n-gram is a contiguous sequence of 'n' items from a given sample of text or speech. The \"items\" can be characters, syllables, or, most commonly, words. N-grams are a simple yet powerful way for machines to capture the context and statistical properties of a language."
   },
   {
    "t": "What does this module say about “Types of N-grams”?",
    "ans": "The 'n' in n-gram determines the size of the sequence. The most common types are:"
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
    "ans": "Imagine trying to understand a sentence by looking at it as one continuous string of letters. It would be nearly impossible. Tokenization provides the structure that machines need. By converting a sentence like \"NLP is fascinating!\" into tokens such as `[\"NLP\", \"is\", \"fascinating\", \"!\"]`, we create a list of items that a model can count, analyze, and assign meaning to."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Normalize sequential inputs before feeding them to a network: Min-Max when you need a bounded range and trust your extremes, Z-Score when outliers are possible. And always fit the scaler on training data only — for time series, the future must never leak into the past."
   },
   {
    "t": "What does this module say about “Why Networks Care About Scale”?",
    "ans": "Neural networks learn by nudging weights along gradients. When one input ranges over [0, 1] and another over [100, 10000], the loss surface becomes a stretched valley: gradients explode along one axis and vanish along the other, forcing tiny learning rates and slow, unstable training. Normalization reshapes that valley into something closer to a bowl — the same step size works in every direction."
   },
   {
    "t": "What does this module say about “Key Takeaway”?",
    "ans": "Normalize sequential inputs before feeding them to a network: Min-Max when you need a bounded range and trust your extremes, Z-Score when outliers are possible. And always fit the scaler on training data only — for time series, the future must never leak into the past."
   }
  ]
 },
 {
  "path": "natural_language_processing/output_gate_in_lstm.html",
  "title": "Output Gate in LSTM",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The Output Gate separates having information from using it. Together with the Forget Gate (what to erase), the Input Gate (what to write), and the Candidate (what the content is), it completes the four-layer machine that makes an LSTM cell work — and explains why it costs four times a simple RNN's parameters."
   },
   {
    "t": "What does this module say about “Why $\\tanh(C_t)$ First”?",
    "ans": "The cell state is a running sum, so it can drift well outside $[-1, 1]$ after many additions. Feeding that raw value to the next layer would produce unstable activations. Squashing with $\\tanh$ rescales it into a bounded, zero-centred range before the gate scales it further."
   },
   {
    "t": "What does this module say about “It Closes the Loop”?",
    "ans": "$H_t$ is not just the cell's answer — it is also half of the input to the next time step, where it will help compute all four layers again. So the Output Gate does double duty: it decides what the outside world sees, and it decides what the cell tells its own future self. A closed output gate leaves the next step reasoning almost entirely from the incoming token."
   }
  ]
 },
 {
  "path": "natural_language_processing/positional_encoding.html",
  "title": "Positional Encoding",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Self-attention has no notion of order, so position has to be supplied explicitly, and the naive options fail: raw indices grow without bound and normalised ones mean different things in different-length sentences."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "Self-attention computes every position from every other position by dot products and weighted sums. Nowhere in that computation does an index appear. Permute the input and the outputs permute with it, unchanged — the mechanism is permutation-equivariant ."
   },
   {
    "t": "What does this module say about “The obvious ideas, and why they fail”?",
    "ans": "Both are available in the Scheme control above. What is wanted is something bounded, unique per position, consistent across sentence lengths, and — ideally — carrying information about relative distance, since \"the adjective three words back\" is a far more useful notion than \"the word at index 17\"."
   }
  ]
 },
 {
  "path": "natural_language_processing/query_key_value.html",
  "title": "Query, Key and Value",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Attention is a soft dictionary lookup: the query says what a position is looking for, each key says how well that position matches, and each value says what it contributes once matched, with all three being separate learned projections of the same input. Every key matches to some degree, so the output is a weighted blend rather than a single retrieved entry, and the whole mechanism is softmax(QKᵀ/√d_k)V."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The previous module described attention as score, normalise, blend. That description works, but it leaves one thing vague: what exactly is being compared against what?"
   },
   {
    "t": "What does this module say about “A soft dictionary lookup”?",
    "ans": "Think of a Python dictionary. You supply a key, it matches one stored key exactly, and you get back its value. Attention is the same operation with the hard edges removed:"
   }
  ]
 },
 {
  "path": "natural_language_processing/rnn_architecture.html",
  "title": "RNN Architecture",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Internal Flow”?",
    "ans": "The internal architecture of a standard Recurrent Neural Network block is wonderfully simple. It takes its past memory, merges it with the present, and squashes it through a single neural layer to create the future state."
   },
   {
    "t": "What does this module say about “The Core Idea: The Hidden State”?",
    "ans": "Unlike standard feed-forward networks, RNNs pass a single vector of context forward through time. This is the Hidden State ($H_t$) ."
   },
   {
    "t": "What does this module say about “Step-by-Step Flow”?",
    "ans": "When the simulation runs, watch the data flow through these sequential steps inside the cell:"
   }
  ]
 },
 {
  "path": "natural_language_processing/self_attention.html",
  "title": "Self-Attention",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Self-attention is attention with queries, keys and values all drawn from the same sequence, so every word is rewritten as a blend of the words it finds relevant — which is how a pronoun can resolve to a noun six words away in a single step."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "In encoder–decoder attention the queries come from one sequence and the keys and values from another. Self-attention is the same machinery with a single change: all three come from the same sequence . The sentence attends to itself."
   },
   {
    "t": "What does this module say about “What a word is actually doing”?",
    "ans": "Every position emits a query, a key and a value . Each query is scored against every key — including its own — giving an n × n grid of scores. Softmax each row, and you have the matrix above: row i is how word i distributes its attention across the whole sentence."
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The choice between stemming and lemmatization is a trade-off. Stemming is fast and good enough for many applications, but it can be inaccurate. Lemmatization is more accurate and provides meaningful root words, but it comes at a higher computational cost. Choose the tool that best fits the needs of your specific NLP task."
   },
   {
    "t": "What does this module say about “The Goal: Text Normalization”?",
    "ans": "In Natural Language Processing (NLP), we often need to treat different forms of a word as the same. For example, \"run\", \"running\", and \"ran\" all refer to the same basic concept. The process of reducing these variations down to a common base form is called text normalization . Stemming and lemmatization are two popular techniques for achieving this."
   },
   {
    "t": "What does this module say about “Stemming: The Fast and Crude Approach”?",
    "ans": "Stemming is a process that reduces words to their \"stem\" or root form by chopping off prefixes and suffixes. It uses a set of simple, rule-based heuristics and does not care if the resulting stem is a real dictionary word."
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
    "t": "What does this module say about “What is Text Normalization”?",
    "ans": "Text normalization is the process of transforming raw, unstructured text into a clean, standardized format that can be easily understood and analyzed by machines. Think of it as a \"clean-up\" phase for your text data. Computers are literal and see \"Run\", \"run\", and \"running\" as three completely different words."
   },
   {
    "t": "What does this module say about “Why is a Pipeline Necessary”?",
    "ans": "Real-world text is messy. It's filled with inconsistencies like capitalization, punctuation, numbers, and special characters that add little to no semantic value for many NLP tasks. A text normalization pipeline is a series of sequential steps designed to methodically remove this \"noise.\" By applying these steps in a specific order, we can ensure that the final text is clean and ready for more advanced processing, su..."
   },
   {
    "t": "What does this module say about “Exploring the Pipeline Steps”?",
    "ans": "Let's break down the common steps you'll find in a text normalization pipeline, all of which you can toggle in the interactive tool."
   }
  ]
 },
 {
  "path": "natural_language_processing/attention_mechanism.html",
  "title": "The Attention Mechanism",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Attention replaces the single fixed context vector with a fresh weighted average of every encoder state, recomputed at each output step: score the decoder state against each input position, softmax the scores into weights that sum to 1, and blend. Because nothing is compressed, long sentences stop degrading, and because the weights are a proper distribution they can be read as an alignment."
   },
   {
    "t": "What does this module say about “Quick Context”?",
    "ans": "The encoder–decoder models that came before attention worked like this: an RNN read the whole input sentence and squeezed it into a single fixed-length vector, and a second RNN generated the output from that vector alone."
   },
   {
    "t": "What does this module say about “The fix”?",
    "ans": "Attention throws away the assumption that the decoder needs one summary. Instead, keep every encoder state, and at each output step let the decoder build a fresh context vector by weighting them:"
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
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The vanishing gradient problem is not a bug or a tuning issue — it is the inescapable arithmetic of multiplying T numbers that aren't exactly 1. It caps how far back a vanilla RNN can learn, and it is the direct reason LSTMs, GRUs, and ultimately attention-based Transformers exist."
   },
   {
    "t": "What does this module say about “The Arithmetic of Forgetting”?",
    "ans": "BPTT multiplies the gradient by ∂hₜ/∂hₜ₋₁ once per timestep. Call that factor's typical size w . After travelling back T steps the gradient is scaled by w T — a geometric series. At w = 0.7 and T = 30, that's 0.7³⁰ ≈ 0.00002: the beginning of the sentence receives two hundred-thousandths of the learning signal."
   },
   {
    "t": "What does this module say about “Vanishing and Exploding: Two Sides of One Coin”?",
    "ans": "LSTM and GRU cells attack the product itself: they add a cell state with additive updates and learned gates, creating a path where the effective factor stays near 1 for as long as the gates choose. Gradients ride this \"constant error carousel\" across hundreds of steps — which is why LSTMs dominated sequence learning for two decades, until attention offered an even more direct shortcut."
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
    "t": "What does this module say about “The Core Idea: The Cell State”?",
    "ans": "The key to LSTMs is the Cell State ($C_t$) , visualized as the horizontal line running across the top of the diagram. It acts like a conveyor belt."
   },
   {
    "t": "What does this module say about “Step-by-Step Flow”?",
    "ans": "When the simulation runs, watch the data flow through these sequential steps inside the cell:"
   },
   {
    "t": "What does this module say about “The Parameter Cost”?",
    "ans": "Because there are four distinct neural network layers inside this one cell (Forget, Input, Candidate, Output), an LSTM is much more computationally heavy than a standard RNN. Check the Parameters button to see how the matrix dimensions are multiplied by 4."
   }
  ]
 },
 {
  "path": "natural_language_processing/what_is_bi_directional_layer.html",
  "title": "What is a Bidirectional Layer?",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “Step-by-Step Architecture”?",
    "ans": "When you run the simulation, you will see the architecture process the sequence \"The bank of the river\" :"
   },
   {
    "t": "What does this module say about “The Parameter Cost (2x)”?",
    "ans": "It's important to remember that a Bidirectional layer is literally just two standard layers wrapped in a trenchcoat. The forward layer has its own weights ($W^f$), and the backward layer has its own completely separate weights ($W^b$). Because of this, a Bidirectional layer has exactly twice as many parameters as a standard layer of the same size. You can verify this by clicking the Parameters button."
   },
   {
    "t": "What does this module say about “Bidirectional RNN Shared Parameters”?",
    "ans": "Calculates 2x parameters because there are independent Forward and Backward networks."
   }
  ]
 },
 {
  "path": "natural_language_processing/what_is_a_gru.html",
  "title": "What is a GRU?",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "The GRU keeps the essential insight of gating — memory updates as learned, per-dimension decisions — while cutting a gate, a state track, and a quarter of the parameters. Both LSTM and GRU still read strictly left-to-right, though. What if the meaning of a word depends on what comes after it? That is the next module: bidirectional processing."
   },
   {
    "t": "What does this module say about “Simplify Without Breaking”?",
    "ans": "The Gated Recurrent Unit (Cho et al., 2014) asked a sharp question: does an LSTM really need three gates and two separate memory tracks? The GRU's answer: merge the cell state and hidden state into one vector, merge forget+input into a single update gate z , and add a reset gate r for proposing new content. Same gating idea, leaner machine."
   },
   {
    "t": "What does this module say about “How the Two Gates Cooperate”?",
    "ans": "zₜ = σ(W⃂xₜ + U⃂hₜ₋₁) · rₜ = σ(Wᵣxₜ + Uᵣhₜ₋₁) h̃ₜ = tanh(W·xₜ + U·(rₜ⊙hₜ₋₁)) hₜ = zₜ⊙hₜ₋₁ + (1 − zₜ)⊙h̃ₜ"
   }
  ]
 },
 {
  "path": "natural_language_processing/what_is_a_recurrent_cell.html",
  "title": "What is a Recurrent Cell?",
  "cat": "NLP",
  "q": [
   {
    "t": "What is meant by “U·hₜ₋₁” here?",
    "ans": "what the past contributes. This term is the memory."
   },
   {
    "t": "What is meant by “tanh” here?",
    "ans": "squashes the result into [-1, 1], keeping the state bounded step after step."
   },
   {
    "t": "What is meant by “Same W, U, b at every step” here?",
    "ans": "the cell handles a 5-word or a 500-word sentence with the identical parameters. Variable-length input solved."
   }
  ]
 },
 {
  "path": "natural_language_processing/what_is_a_sequence.html",
  "title": "What is a Sequence?",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "A sequence is not just a set of values — it is values plus their order . Any model that throws the order away (like a bag of words) throws information away with it. Everything else in this NLP track — sliding windows, encodings, embeddings, recurrent cells — exists to let neural networks use that ordering information instead of losing it."
   },
   {
    "t": "What does this module say about “The Core Idea”?",
    "ans": "A sequence is an ordered collection of items where the position of each item carries meaning. \"Dog bites man\" and \"man bites dog\" contain exactly the same three words, yet they describe opposite events. That difference lives entirely in the order — and order is precisely what ordinary tabular data doesn't have."
   },
   {
    "t": "What does this module say about “Sequential vs. Tabular Data”?",
    "ans": "In a classic spreadsheet-style dataset, each row is independent: shuffling the rows of a housing-price table changes nothing about what a model can learn. Sequential data breaks this assumption in two ways:"
   }
  ]
 },
 {
  "path": "natural_language_processing/why_text_encoding_is_needed_in_nlp.html",
  "title": "Why Text Encoding is Needed in NLP",
  "cat": "NLP",
  "q": [
   {
    "t": "Without scrolling back — what is the one-line takeaway from this module?",
    "ans": "Text encoding isn't a preprocessing nicety — it is the bridge without which no NLP is possible. A neural network can no more process the raw word \"cat\" than a calculator can. First we turn language into numbers; everything else in NLP is about turning it into good numbers."
   },
   {
    "t": "What does this module say about “The One-Sentence Argument”?",
    "ans": "Every neuron in every network — from a 1958 perceptron to GPT — computes some flavour of w · x + b . Multiplication is only defined for numbers. Therefore, before any text can enter any network, it must be converted into numbers. That conversion is text encoding , and it isn't an optimization — it's a precondition."
   },
   {
    "t": "What does this module say about “What \"Feeding Raw Text\" Actually Does”?",
    "ans": "Try to compute 0.5 × \"cat\" + 0.1 in any language and you get an error or NaN — the arithmetic is simply undefined. In practice a framework like PyTorch refuses at the door: tensors hold floats, not strings. The demo above makes this failure visible instead of hiding it in a stack trace."
   }
  ]
 },
 {
  "path": "natural_language_processing/word_cloud.html",
  "title": "Word Cloud Generator",
  "cat": "NLP",
  "q": [
   {
    "t": "What does this module say about “What is a Word Cloud”?",
    "ans": "A word cloud (or tag cloud) is a visual representation of text data where the size of each word is proportional to its frequency or importance in the source text. In essence, it's a simple yet powerful tool for at-a-glance text analysis . By highlighting the most prominent words, a word cloud allows you to quickly grasp the main themes and key topics within a large body of text without having to read it all."
   },
   {
    "t": "What does this module say about “How Does it Work? The Process Explained”?",
    "ans": "Creating a word cloud involves a few key steps, most of which happen behind the scenes in the interactive generator above."
   },
   {
    "t": "What does this module say about “Why Are Word Clouds Useful”?",
    "ans": "Despite their simplicity, word clouds are widely used in various fields for several reasons:"
   }
  ]
 }
];
