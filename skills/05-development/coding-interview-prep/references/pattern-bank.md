# Pattern Bank — The Core DSA Patterns

> Deep reference for `coding-interview-prep`. Master the *pattern*, not the solution: each
> entry gives what it is, when to reach for it, canonical problems, complexity, and the
> variations that expose memorizers. Solve with the 6-step framework, log every problem,
> and re-solve misses at day 3 and 7.

## How to use this bank

1. Pick the pattern for the problem type (see the quick map at the bottom).
2. Solve the canonical problem with the 6-step framework before reading solutions.
3. Solve 2-3 variations without help; log each (date, pattern, diff, hint-needed, one fix).
4. Re-solve anything you missed at day 3 and day 7 — spaced repetition is the whole game.

---

## 1. Hash Map / Set
- **What:** O(1) average lookup/insert keyed by value.
- **When:** existence checks, counting, pairing (two-sum), dedupe.
- **Canonical:** Two Sum · Contains Duplicate · Valid Anagram · Group Anagrams.
- **Complexity:** O(n) time, O(n) space.
- **Variations:** subarray sum equals K (prefix map), longest consecutive sequence, top-K frequent (with heap).

## 2. Two Pointers
- **What:** Two indices moving toward each other or together over a sorted sequence.
- **When:** sorted arrays, "find a pair that satisfies a condition", palindrome checks.
- **Canonical:** Two Sum II · Valid Palindrome · Container With Most Water · 3Sum.
- **Complexity:** O(n) time, O(1) space.
- **Variations:** 4Sum, trapping rain water, move zeroes, remove duplicates in place.

## 3. Sliding Window
- **What:** A window over a subarray/substring; expand and shrink while maintaining a condition.
- **When:** "longest/shortest subarray/substring with condition X", fixed-size window sums.
- **Canonical:** Longest Substring Without Repeating Characters · Minimum Window Substring · Max Sum Subarray of Size K.
- **Complexity:** O(n) time — each element enters and leaves once.
- **Variations:** longest repeating character replacement, permutation in string, fruit into baskets.

## 4. Prefix Sum
- **What:** Precompute cumulative sums for O(1) range queries.
- **When:** range-sum queries, "subarray sum equals K", contiguous subarray conditions.
- **Canonical:** Range Sum Query - Immutable · Subarray Sum Equals K · Product of Array Except Self.
- **Complexity:** O(n) precompute, O(1) query.
- **Variations:** 2D prefix sums, contiguous array (0/1 → +1/-1), minimum size subarray sum.

## 5. Binary Search
- **What:** Halve the search space on a monotonic predicate. Includes rotated-array and first/last-position variants.
- **When:** sorted input, "find a boundary where a predicate flips", search the answer space.
- **Canonical:** Binary Search · Search in Rotated Sorted Array · First and Last Position · Koko Eating Bananas.
- **Complexity:** O(log n) time, O(1) space.
- **Variations:** find peak element, search a 2D matrix, time-based key-value store, split array largest sum.

## 6. Stack
- **What:** LIFO; matching, monotonic trends, reversal.
- **When:** balanced parentheses, next-greater-element, expression evaluation, undo.
- **Canonical:** Valid Parentheses · Min Stack · Next Greater Element · Daily Temperatures.
- **Complexity:** O(n) time, O(n) space worst.
- **Variations:** monotonic stack (largest rectangle in histogram), evaluate RPN, decode string, online stock span.

## 7. Queue & Deque
- **What:** FIFO; deque for window min/max.
- **When:** BFS ordering, task scheduling, sliding-window maximum.
- **Canonical:** Implement Queue with Stacks · Sliding Window Maximum · Number of Recent Calls.
- **Complexity:** O(n) amortized.
- **Variations:** design circular queue, task scheduler, reveal cards in increasing order.

## 8. Linked List
- **What:** Node-based linear structure; reversal, cycle detection, fast/slow pointers, merging.
- **When:** reversing, cycle detection, "kth from end", merging sorted lists, LRU cache.
- **Canonical:** Reverse Linked List · Linked List Cycle · Merge Two Sorted Lists · Remove Nth Node From End.
- **Complexity:** O(n) time, O(1) space (iterative).
- **Variations:** LRU cache, reorder list, palindrome linked list, copy list with random pointer.

## 9. Recursion & Backtracking
- **What:** Explore a decision tree; undo choices on dead ends; generate all combinations.
- **When:** "all subsets/permutations/combinations", constraint satisfaction (N-Queens), word search.
- **Canonical:** Subsets · Permutations · Combination Sum · Word Search · N-Queens.
- **Complexity:** exponential (O(2^n) subsets, O(n!) permutations) — pruning matters.
- **Variations:** generate parentheses, palindrome partitioning, letter combinations, sudoku solver.

## 10. Greedy
- **What:** Locally optimal choice at each step, argued globally optimal.
- **When:** interval scheduling, jump-game reachability, canonical-coin change, task scheduling.
- **Canonical:** Jump Game · Gas Station · Non-overlapping Intervals · Candy.
- **Complexity:** often O(n log n) due to sorting.
- **Variations:** minimum arrows to burst balloons, partition labels, meeting rooms II, queue reconstruction by height.

## 11. Binary Tree Traversal
- **What:** DFS (pre/in/post) and BFS (level order) over trees.
- **When:** any tree problem: depth, symmetry, path sums, serialization, LCA.
- **Canonical:** Binary Tree Inorder Traversal · Maximum Depth · Level Order Traversal · Lowest Common Ancestor · Validate BST.
- **Complexity:** O(n) time, O(h) space (h = height).
- **Variations:** diameter of a binary tree, right-side view, path sum II/III, construct from traversals, flatten to linked list.

## 12. Graph Traversal (BFS/DFS)
- **What:** Explore nodes/edges; BFS for shortest path in unweighted graphs, DFS for connectivity.
- **When:** islands/connected components, shortest path (unweighted), clone graph, word ladder.
- **Canonical:** Number of Islands · Clone Graph · Word Ladder · Rotting Oranges.
- **Complexity:** O(V + E).
- **Variations:** Pacific Atlantic water flow, walls and gates, surrounded regions, 01 matrix (multi-source BFS).

## 13. Heap / Priority Queue
- **What:** Efficient min/max extraction; top-K patterns.
- **When:** "K largest/smallest", merge K sorted lists, median stream, task scheduling.
- **Canonical:** Kth Largest Element in an Array · Top K Frequent Elements · Merge K Sorted Lists · Find Median from Data Stream.
- **Complexity:** O(log k) per op (k = heap size).
- **Variations:** K closest points to origin, smallest range covering K lists, meeting rooms II (min-heap by end), reorganize string.

## 14. Trie (Prefix Tree)
- **What:** Tree keyed by character prefixes.
- **When:** prefix search/autocomplete, wildcard word dictionary, word search II.
- **Canonical:** Implement Trie · Add and Search Word · Word Search II.
- **Complexity:** O(L) per op (L = word length); O(total chars) space.
- **Variations:** longest word in dictionary, replace words, autocomplete system, maximum XOR of two numbers.

## 15. Union-Find (Disjoint Set)
- **What:** Track connected components with near-O(1) find/union (path compression + rank).
- **When:** connectivity, undirected cycle detection, dynamic grouping.
- **Canonical:** Number of Provinces · Redundant Connection · Accounts Merge · Graph Valid Tree.
- **Complexity:** O(α(n)) amortized.
- **Variations:** operations to make network connected, evaluate division, smallest string with swaps.

## 16. Topological Sort
- **What:** Order a DAG so every edge u→v has u before v.
- **When:** prerequisites, task ordering, dependency resolution, directed cycle detection.
- **Canonical:** Course Schedule · Course Schedule II · Alien Dictionary.
- **Complexity:** O(V + E).
- **Variations:** minimum height trees, sequence reconstruction, all possible recipes.

## 17. Shortest Path (Dijkstra / BFS)
- **What:** Dijkstra for non-negative weighted graphs (min-heap); BFS for unweighted.
- **When:** cheapest/shortest path with costs, network delay, minimum effort paths.
- **Canonical:** Network Delay Time · Cheapest Flights Within K Stops · Path With Minimum Effort.
- **Complexity:** O((V + E) log V).
- **Variations:** swim in rising water, find the city with the smallest number of neighbors at threshold.

## 18. Dynamic Programming — 1D
- **What:** Overlapping subproblems solved bottom-up/top-down where state depends on earlier states.
- **When:** house robber, climbing stairs, coin change, word break, decode ways, LIS.
- **Canonical:** Climbing Stairs · House Robber · Coin Change · Longest Increasing Subsequence · Word Break.
- **Complexity:** O(n) or O(n²) depending on transitions.
- **Variations:** partition equal subset sum, maximum product subarray, unique BSTs, paint house.

## 19. Dynamic Programming — 2D (grids & strings)
- **What:** DP over (i, j) states — grid paths, LCS, edit distance, knapsack, interval DP.
- **When:** unique paths, longest common subsequence, edit distance, 0/1 knapsack.
- **Canonical:** Unique Paths · Longest Common Subsequence · Edit Distance · 0/1 Knapsack.
- **Complexity:** O(n·m) time and space (space can be compressed).
- **Variations:** minimum path sum, distinct subsequences, interleaving string, burst balloons (interval DP), wildcard matching.

## 20. Bit Manipulation
- **What:** XOR, shifts, masks for set operations and tricks.
- **When:** single-number (XOR), power-of-two, counting bits, subset enumeration.
- **Canonical:** Single Number · Number of 1 Bits · Counting Bits · Power of Two.
- **Complexity:** O(n) or O(1) per op.
- **Variations:** missing number (XOR), reverse bits, sum of two integers, maximum XOR (with trie).

## 21. Math & Number Theory
- **What:** Primes, GCD/LCM, modular arithmetic, fast exponentiation.
- **When:** is-prime, gcd, pow mod, roman numerals, happy number.
- **Canonical:** Pow(x, n) · Count Primes · Roman to Integer · Happy Number.
- **Complexity:** fast exponentiation O(log n).
- **Variations:** fraction to recurring decimal, integer to English words, divide two integers, sqrt without a library.

## 22. Matrix / Grid (2D array)
- **What:** Row/column/diagonal manipulation; spiral/simulation; in-place transforms.
- **When:** spiral order, rotate image, set matrix zeroes, game of life, matrix BFS.
- **Canonical:** Spiral Matrix · Rotate Image · Set Matrix Zeroes · Search a 2D Matrix II.
- **Complexity:** O(n·m).
- **Variations:** diagonal traverse, matrix block sum, shift 2D grid, toeplitz matrix.

## 23. Intervals
- **What:** Sort by start; merge/overlap; sweep line.
- **When:** merge intervals, meeting rooms, insert interval, min arrows.
- **Canonical:** Merge Intervals · Meeting Rooms II · Insert Interval.
- **Complexity:** O(n log n) for sort, O(n) sweep.
- **Variations:** employee free time, interval list intersections, non-overlapping intervals.

## 24. Monotonic Queue / Stack
- **What:** Deque/stack keeping candidates in monotonic order.
- **When:** sliding-window max/min, next-greater boundaries.
- **Canonical:** Sliding Window Maximum · Shortest Subarray With Sum at Least K.
- **Complexity:** O(n) amortized.
- **Variations:** max value of equation, largest rectangle in histogram (monotonic stack), sum of subarray minimums.

## 25. Design / OOP (Data-Structure Design)
- **What:** Combine structures (hash + list, two heaps) to meet per-operation targets.
- **When:** LRU cache, insert-delete-getRandom, min stack, median finder.
- **Canonical:** LRU Cache · Insert Delete GetRandom O(1) · Min Stack · Find Median from Data Stream.
- **Complexity:** O(1)-O(log n) per op by design.
- **Variations:** max frequency stack, all-one data structure, design twitter.

---

## Quick map — problem phrase → pattern

| If the problem says… | Reach for |
|---|---|
| find a pair / count / frequency / existence | Hash map/set |
| sorted array + two elements | Two pointers |
| longest/shortest subarray or substring with a condition | Sliding window |
| range sum / subarray sum equals K | Prefix sum |
| search in sorted / find the boundary | Binary search |
| matching / next greater / balanced | Stack |
| level order / BFS / shortest (unweighted) | Queue / BFS |
| reverse / cycle / kth from end | Linked list (fast/slow) |
| all subsets / permutations / combinations | Backtracking |
| max/min with greedy choice each step | Greedy |
| K largest/smallest / top K | Heap |
| prefix / autocomplete / wildcard dictionary | Trie |
| connected components / undirected cycle | Union-Find |
| prerequisites / ordering / directed cycle | Topological sort |
| weighted shortest path / cheapest | Dijkstra |
| overlapping subproblems, maximize/minimize | DP (1D/2D) |
| XOR tricks / count bits / single number | Bit manipulation |
| prime / gcd / pow / roman | Math |
| spiral / rotate matrix | Matrix traversal |
| merge / overlap intervals | Intervals |
| sliding-window max | Monotonic queue/stack |
| design a data structure with O(1) ops | Design/OOP |

## Suggested study-week mapping

| Week | Focus |
|---|---|
| 1 | Hash map · Two pointers · Sliding window · Prefix sum |
| 2 | Stack · Queue/deque · Linked list · Monotonic queue |
| 3 | Binary search · Tree traversal · BST-specific |
| 4 | BFS/DFS · Union-Find · Topological sort |
| 5 | Heap/Top-K · Greedy · Intervals · Dijkstra |
| 6 | Backtracking · DP 1D · DP 2D · Bit manipulation · Math · Matrix |
| 7 | Trie · Design/OOP · mixed review + full mock loops |

## Problem log template

| Date | Problem | Pattern | Diff | Time | Hint? | Complexity stated? | Edge cases tested? | One fix |
|---|---|---|---|---|---|---|---|---|
