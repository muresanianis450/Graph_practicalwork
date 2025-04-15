# 📊 Graph Algorithms – Practical Work No. 3

🗓 **Due Date:** Week 9–10

🔔 **Important:**  
Computing the **minimum cost walk** (as a list of vertices) is a **mandatory** part of the assignment.

---

## ✅ Assigned Problem

### 1. 🔍 Find Lowest Cost Walk Using Dijkstra's Algorithm

Write a program that, given a graph with **positive costs** and two vertices, finds a **lowest cost walk** between the given vertices using the **Dijkstra algorithm**.

- The result should include the list of vertices that form the walk.
- The graph should be represented using the **abstract data type (ADT)** created for **Lab 1**.
- Modify the ADT if necessary to support cost annotations and path tracking.

---

## 🌟 Bonus Problems

You may implement **one or more** of the following bonus problems for extra credit or practice:

### 1B. 🔢 Count Minimum Cost Walks
Write a program that, given a graph with **costs** and **no negative cost cycles**, and a pair of vertices, **counts the number of distinct walks** of **minimum cost** between them.

---

### 2B. 🔄 Count Walks in a DAG
Write a program that, given a **directed acyclic graph (DAG)** and a pair of vertices, finds the **number of distinct walks** between the given vertices.

---

### 3B. 🌉 Bridge and Torch Problem
Using a lowest cost path algorithm and a new implementation of the interface from Lab 1, solve the classic **Bridge and Torch** problem:

> A number of people (up to 20) must cross a bridge at night. They have a single torch that can light the way for **at most two people** at a time. Each person takes a specific time to cross the bridge **alone**. If two people cross together, they do so at the **pace of the slower** person. Find a solution for **all to cross** using as **little time as possible**.
