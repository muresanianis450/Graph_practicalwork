# Graph Algorithms - Practical Work No. 5

## Problem Statement

**Task:**  
Given an undirected graph, find a **vertex cover** (a set of vertices such that every edge has at least one endpoint in the set) of size at most **twice the size of the optimal (minimum) vertex cover**.

**Constraints:**  
- The algorithm must run in **O(n + m)** time, where:
  - `n` is the number of vertices
  - `m` is the number of edges

**Requirements:**  
- Use the **abstract data type (ADT)** for graphs created in **Lab 1**.  
- Modify the ADT if necessary to support the implementation.

---


# ✅ 1. Greedy 2-Approximation Algorithm
### Idea: Always pick both endpoints of an arbitrary uncovered edge until all edges are covered.

## Steps:
````
Initialize an empty vertex cover set C = {}.

While there are uncovered edges:

Pick any edge (u, v).

Add both u and v to C.

Remove all edges incident to u or v.

Guarantee: This yields a vertex cover of size ≤ 2 × OPT.

Pros: Simple, fast, effective in practice.
Time Complexity: O(E) if edges are stored efficiently.
````

# ✅ 2. Maximal Matching Based Algorithm
### Idea: Use any maximal matching, then include both endpoints of each matched edge.

## Steps:
```
Find a maximal matching M (a set of disjoint edges such that no additional edge can be added).

Let C be the set of all endpoints of edges in M.

Guarantee: Also gives a 2-approximation.
(Proof: Any valid vertex cover must include at least one endpoint of each edge in the matching.)

Pros: Theoretically solid and gives same performance as greedy 2-approx.
Time Complexity: O(E) with a greedy matching algorithm.
```

# ✅ 3. Linear Programming Relaxation (LP) + Rounding
### Idea: Solve the LP relaxation of the integer program for vertex cover, then round fractional values.

## Integer Program:
```
Minimize: ∑ xᵢ

s.t. xᵤ + xᵥ ≥ 1 for all edges (u,v)

xᵢ ∈ {0, 1}

Relaxed LP:

Same constraints but allow 0 ≤ xᵢ ≤ 1

Rounding:

For each vertex v: If xᵢ ≥ 0.5, include v in the vertex cover.

Guarantee: 2-approximation due to rounding.

Pros: Often performs better than greedy on structured instances.
Time Complexity: Polynomial time using LP solvers.
```

# ✅ 4. Primal-Dual Approximation Algorithm
### Idea: Use primal-dual schema of approximation to iteratively build a cover and dual solution.

## Outline:
```
Start with dual variables set to 0.

For uncovered edges, increase duals until some vertex’s constraint is tight.

Add that vertex to the cover.

Repeat until all edges are covered.

Guarantee: 2-approximation.

Pros: Theoretically elegant; useful when LP is expensive to solve directly.
Time Complexity: Polynomial.
```

# ✅ 5. Local Search Heuristic
### Idea: Iteratively improve a vertex cover by exchanging vertices.

## Steps:
```Start with a vertex cover (e.g., greedy solution).

While improving:

Try removing a vertex and check if the set still covers all edges.

If yes, accept the new set.

Variants: May use simulated annealing or other metaheuristics.

Pros: No approximation guarantee but can yield better-than-2-approx results in practice.
Time Complexity: Depends on iterations and checks (can be exponential in worst case without cutoff).

```

# Summary Table
```
| Approach                     |Approximation Ratio| Time Complexity           |        Notes         |
| Greedy 2-Approximation       |        2× OPT     |         O(E)              | Simple and efficient |
| Maximal Matching             |        2× OPT     |         O(E)              | Theoretically sound  |
| LP + Rounding | 2× OPT       |       Poly-time   |   Solves LP, then rounds  | -------------------- |
| Primal-Dual Algorithm        |        2× OPT     |       Poly-time           | Dual-based method    |
| Local Search / Metaheuristic |    Not guaranteed | Varies | Good in practice | ---------------------|
```       
