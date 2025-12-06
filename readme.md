# CS3310-002 Final Project
## Fall 2025
### By: Jared Bake, Kevin Pett, Tate Thomas
### Project: Bipartite Dimension Problem
---

INSTRUCTIONS:
- Make sure to install python-sat
```
pip install python-sat
```
- All other libraries should be built-ins
- Run the following python command:
```
python3 run_this.py
```

Output as of Part 2 deadline:
```
ALGORITHM            | DATASET              | AVG TIME (s) | RESULT (k)
---------------------------------------------------------------------------
Kevin (Exact)        | Easy (Matching 6)    | 0.001944s    | k=6
Kevin (Exact)        | Medium (Matching 8)  | 0.196750s    | k=8
Kevin (Exact)        | Hard (Matching 9)    | 70.196191s    | k=10
---------------------------------------------------------------------------
Tate (Greedy)        | Easy (Matching 6)    | 0.000110s    | k=6
Tate (Greedy)        | Medium (Matching 8)  | 0.000126s    | k=8
Tate (Greedy)        | Hard (Matching 9)    | 0.001456s    | k=10
---------------------------------------------------------------------------
Jared (Matrix)       | Easy (Matching 6)    | 0.000021s    | k=2
Jared (Matrix)       | Medium (Matching 8)  | 0.000026s    | k=2
Jared (Matrix)       | Hard (Matching 9)    | 0.000094s    | k=5
---------------------------------------------------------------------------
```

Note:
It turns out Jared's Matrix Manipulation Algorithm doesn't specifically find a 'close' minimum biclique cover number of a graph, but it's output is heavily correlated. So if you need a lightning-fast algorithm that's ~100% faster than the more accurate approximation algorithm, and you're okay with a general ballpark under-approximation, then it's useful.