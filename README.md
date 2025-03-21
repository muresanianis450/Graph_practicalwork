# 📚 Graph Algorithms - Practical Work No. 1

Design and implement an abstract data type **directed graph** and various functions to read, modify, and manipulate the graph from a text file. The goal is to manage a **directed graph** with operations to retrieve edge information, vertex properties, and other required functionalities.

---

## 📝 Objective

You will design a **directed graph** with vertices represented as integers (0 to n-1) and edges that may either be a pair of vertex identifiers or a unique **Edge_id**. Additionally, you'll implement operations to:

1. Parse the graph's vertices and edges.
2. Retrieve and modify edge properties.
3. Add or remove vertices and edges.
4. Read from and write to a text file representing the graph.
5. Create random graphs with specified numbers of vertices and edges.

---

## 🔧 Requirements

### ⚙️ Core Operations

1. **🔢 Number of Vertices**:  
   Get the total number of vertices in the graph.

2. **🔄 Parse Vertices**:  
   Iterate through the set of vertices in the graph.

3. **🔗 Edge Existence**:  
   Given two vertices, check if there is an edge from the first to the second. If it exists, retrieve the **Edge_id**.

4. **📊 In-Degree & Out-Degree**:  
   Retrieve the in-degree (number of incoming edges) and out-degree (number of outgoing edges) of a specified vertex.

5. **🔀 Iterate Outbound & Inbound Edges**:  
   Retrieve the **Edge_id** for each outbound and inbound edge for a specific vertex.

6. **📍 Edge Endpoints**:  
   For a given **Edge_id**, retrieve the endpoints (source and target vertices).

7. **💾 Edge Information**:  
   Retrieve or modify the integer value (cost) attached to a specified edge.

8. **🛠️ Graph Modifications**:  
   - ➕ Add and remove vertices.
   - ➖ Add and remove edges.
   - 🔄 Ensure that edge properties and vertex identifiers are managed appropriately.

---

### 📏 Performance Requirements

- Operations must take no more than:
    - **O(deg(x) + deg(y))** for verifying the existence of an edge and for retrieving the edge between two given vertices.
    - **O(1)** for operations such as:
        - Getting the first or next edge inbound or outbound from a given vertex.
        - Getting the endpoints or modifying the attached integer for an edge.
        - Getting the total number of vertices or edges.
        - Getting the in-degree or out-degree of a given vertex.

### ⚖️ Additional Constraints

- The object returned by the parse functions shall **not** allow modifying the graph through its public functions. So, don't return sets by reference. Return iterators instead! 📜

---

## 📂 File Format

The graph will be read from a text file with the following format:

- **First line**: the number `n` of vertices and the number `m` of edges.
- **Each of the following `m` lines**: three numbers `x`, `y`, and `c`, describing an edge: the origin vertex `x`, the target vertex `y`, and the cost `c` of the edge.

**Example**:
```txt
5 4
0 1
1 2
2 3
3 4
```

---

## 🎲 Bonus Operations (Optional)

- **Multilingual Implementation**:  
   Do the implementation in two distinct languages:
   - Java (~2p)
   - C# (~2p)
   - C++ (~4p)

___



