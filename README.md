🚀 Directed Graph Algorithms

📌 Project Overview

This project is a practical implementation of a Directed Graph Abstract Data Type with various functionalities, including:

✅ Reading a directed graph from a text file 📄
✅ Parsing vertices and edges 🔄
✅ Checking edge existence and retrieving Edge_id 🔍
✅ Calculating in-degree & out-degree of vertices 📊
✅ Iterating outbound and inbound edges 🔄
✅ Adding and removing vertices and edges ➕➖
✅ Storing and modifying edge costs 💰
✅ Copying graphs independently 📋
✅ Generating random graphs 🎲
✅ Saving a graph to a text file 💾

📂 File Format

The graph is stored in a text file with the following format:

<number_of_vertices> <number_of_edges>
<source_vertex> <target_vertex> <cost>
<source_vertex> <target_vertex> <cost>
...

Example:

5 7
0 1 10
0 2 15
1 3 20
2 3 25
2 4 30
3 4 35
4 0 40

🛠️ Setup & Usage

1️⃣ Clone the Repository

git clone https://github.com/your-username/graph-algorithms.git
cd graph-algorithms

2️⃣ Run the Program

Ensure you have Python 3+ installed. Then, execute:

python main.py

3️⃣ Generate a Random Graph

Run:

python generate_graph.py <num_vertices> <num_edges>

Example:

python generate_graph.py 1000 4000

4️⃣ Read Graph from File

python read_graph.py graph.txt

📜 Features & Complexity

Operation

Complexity

Get number of vertices

O(1)

Check if edge exists (Edge_id)

O(deg(x) + deg(y))

Get in-degree / out-degree

O(1)

Parse vertices

O(n)

Parse outbound/inbound edges

O(deg(x))

Add / Remove edge

O(1)

Add / Remove vertex

O(n)

Get / Set edge cost

O(1)

Copy graph

O(n + m)

🔗 Contributing

Feel free to fork this project and submit pull requests! Contributions are always welcome. 😊

📜 License

This project is open-source under the MIT License. 📄

Happy Coding! 💻✨

