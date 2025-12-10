# CS3310-002 Final Project
## Fall 2025
### By: Jared Bake, Kevin Pett, Tate Thomas
### Project: Bipartite Dimension Problem
---

**INSTRUCTIONS for running Part 3:** (Our custom algorithms)

- No package or library installation should be needed for this part
- Navigate to src/custom
- Run the following python command:
```
python3 custom_driver.py
```


**INSTRUCTIONS for running Part 2:** (Implemented algorithms)

- Make sure to install python-sat
```
pip install python-sat
```
- All other libraries should be built-ins
- Run the following python command:
```
python3 run_this.py
```

**INSTRUCTIONS for running Part 3:**

###Output as of Part 2 deadline:
```
ALGORITHM            | DATASET              | AVG TIME (s) | RESULT (k)
---------------------------------------------------------------------------
Kevin (Exact)        | Easy (Matching 6)    | 0.001944s    | k=6
Kevin (Exact)        | Medium (Matching 8)  | 0.196750s    | k=8
Kevin (Exact)        | Hard (Matching 10)    | 70.196191s    | k=10
---------------------------------------------------------------------------
Tate (Greedy)        | Easy (Matching 6)    | 0.000110s    | k=6
Tate (Greedy)        | Medium (Matching 8)  | 0.000126s    | k=8
Tate (Greedy)        | Hard (Matching 10)    | 0.001456s    | k=10
---------------------------------------------------------------------------
Jared (Matrix)       | Easy (Matching 6)    | 0.000021s    | k=2
Jared (Matrix)       | Medium (Matching 8)  | 0.000026s    | k=2
Jared (Matrix)       | Hard (Matching 9)    | 0.000094s    | k=5
---------------------------------------------------------------------------
```

**Note 1**:
It turns out Jared's Matrix Manipulation Algorithm doesn't specifically find a 'close' minimum biclique cover number of a graph, but it's output is heavily correlated. So if you need a lightning-fast algorithm that's ~100% faster than the more accurate approximation algorithm, and you're okay with a general ballpark under-approximation, then it's useful.

**Note 2**: In an earlier version of the repo the dataset said Hard (matching 9) when it should say (matching 10) as it does now.

###Output as of Part 3:
```
ALGORITHM            | DATASET              | AVG TIME (s) | RESULT (k)
---------------------------------------------------------------------------
Kevin (Custom, DP)   | Easy (Matching 6)    | 0.000042s    | k=6
Kevin (Custom, DP)   | Medium (Matching 8)  | 0.000089s    | k=8
Kevin (Custom, DP)   | Hard (Matching 10)   | 0.001038s    | k=10
---------------------------------------------------------------------------
Tate (Custom)        | Easy (Matching 6)    | 0.000080s    | k=6
Tate (Custom)        | Medium (Matching 8)  | 0.000085s    | k=8
Tate (Custom)        | Hard (Matching 10)   | 0.000393s    | k=10
---------------------------------------------------------------------------
Jared (Custom)       | Easy (Matching 6)    | 0.000046s    | k=6
Jared (Custom)       | Medium (Matching 8)  | 0.000069s    | k=8
Jared (Custom)       | Hard (Matching 10)   | 0.000347s    | k=10
---------------------------------------------------------------------------
```

**Note 3**: As you can see from the two outputs, our custom algorithms either improved the runtime or the accuracy of the algorithms compared to the implemented algorithms when ran with the same data. As with other NP-Hard problems, there would likely be noticable downsides to our custom algorithms if the input graphs were more complicated and/or larger. In other words, we haven't shown that our custom algorithms would out-perform the implemented algorithms in general.