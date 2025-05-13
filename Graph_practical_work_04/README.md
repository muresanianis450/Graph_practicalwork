# DAG and Tree Algorithms

This repository contains implementations of graph and tree algorithms focusing on Directed Acyclic Graphs (DAGs), topological sorting, longest and shortest paths, and tree reconstruction.

***

## ✅ Problem 4 – DAG Verification, Topological Sort, and Highest Cost Path

### Description
Given a graph with costs:
- Verify if the graph is a DAG (Directed Acyclic Graph).
- If it is a DAG:
  - Perform a topological sort using the predecessor counters (Kahn’s algorithm).
  - Find the highest cost path between two given vertices in **O(m + n)** time, where:
    - `n` is the number of vertices
    - `m` is the number of edges

***

## ⭐ Bonus 1B – Tree Reconstruction from Two Traversals

### Description
Given any **two** of the three traversal orders of a binary tree:
- **Pre-order**
- **In-order**
- **Post-order**

Reconstruct the original tree and print its structure.

***

## ⭐ Bonus 2B – Number of Distinct Paths in a DAG

### Description
Given a graph:
- Verify if it is a DAG.
- If it is:
  - Perform a topological sort.
  - Count the number of **distinct paths** from a start node to an end node in **O(m + n)** time.

***

## ⭐ Bonus 3B – Number of Distinct Lowest-Cost Paths in a DAG

### Description
Given a **weighted graph**:
- Verify if it is a DAG.
- If it is:
  - Perform a topological sort.
  - Find the number of **distinct lowest-cost paths** from a source node to a destination node in **O(m + n)** time.

