import random
import copy
from collections import deque


class Graph:
    def __init__(self, v=None):
        """
        Constructor for the graph class. Reads from a file if 'v' is a string (filename).
        If 'v' is an integer, creates a graph with vertices from 0 to v-1.

        :param v: Can be an integer for the number of vertices or a string with the filename to read from.
        """
        self.out_neighbours = {}  # Adjacency list (with weights)
        self.edges = {}  # Mapping EDGE_ID -> (source, target, weight)
        self.edge_count = 0

        if isinstance(v, str):  # If v is a filename, read the graph from the file
            self._read_from_file(v)
        elif isinstance(v, int):  # If v is an integer, create a graph with v vertices
            for vertex in range(v):
                self.out_neighbours[vertex] = []

    def get_out_neighbours_for_vertex(self, vertex):
        """Returns the out-neighbours of a vertex."""
        return self.out_neighbours.get(vertex, [])

    def _read_from_file(self, file_name):
        """Reads a graph from the specified file."""
        with open(file_name, "r") as f:
            x, y = map(int, f.readline().split())
            for vertex in range(x):
                self.out_neighbours[vertex] = []
            for line in f:
                u, v, w = map(int, line.split())
                self.add_edge(u, v, w)

    def add_edge(self, x, y, weight):
        """Adds a directed edge from x to y with a given weight."""
        if y not in [neighbor for neighbor, _ in self.out_neighbours.get(x, [])]:
            self.out_neighbours.setdefault(x, []).append((y, weight))
            self.edges[self.edge_count] = (x, y, weight)
            self.edge_count += 1

    def remove_edge(self, x, y):
        """Removes the directed edge from x to y."""
        if x in self.out_neighbours:
            self.out_neighbours[x] = [
                (neighbor, weight) for neighbor, weight in self.out_neighbours[x] if neighbor != y
            ]

    def remove_vertex(self, x):
        """Removes vertex x from the graph."""
        if x in self.out_neighbours:
            del self.out_neighbours[x]
        for vertex in self.out_neighbours:
            self.out_neighbours[vertex] = [
                (neighbor, weight) for neighbor, weight in self.out_neighbours[vertex] if neighbor != x
            ]

    def add_vertex(self, x):
        """Adds vertex x to the graph."""
        if x not in self.out_neighbours:
            self.out_neighbours[x] = []

    def get_edge_by_id(self, edge_id):
        """Returns the edge with the given ID."""
        return self.edges.get(edge_id, None)

    def parse_out(self, x):
        """Returns an iterable containing all outbound neighbors of x."""
        return self.out_neighbours.get(x, [])

    def get_number_vertices(self):
        """Returns the number of vertices in the graph."""
        return len(self.out_neighbours)

    def parse_vertices(self):
        """Returns an iterable containing all vertices of the graph."""
        return self.out_neighbours.keys()

    def is_edge(self, x, y):
        """Returns True if there is an edge from x to y in the graph."""
        return any(neighbor == y for neighbor, _ in self.out_neighbours.get(x, []))

    def generate_random_graph(self, number_vertices, number_edges):
        """Generates a random graph."""
        self.__init__(number_vertices)
        for _ in range(number_edges):
            x = random.randint(0, number_vertices - 1)
            y = random.randint(0, number_vertices - 1)
            weight = random.randint(1, 100)
            if x != y and not self.is_edge(x, y):
                self.add_edge(x, y, weight)

    def deepcopy(self):
        """Creates a deep copy of the graph."""
        new_graph = Graph()
        new_graph.out_neighbours = copy.deepcopy(self.out_neighbours)
        new_graph.edges = copy.deepcopy(self.edges)
        new_graph.edge_count = self.edge_count
        return new_graph


def write_to_file(graph: Graph, file_name):
    """Writes the graph to a file."""
    with open(file_name, "w") as f:
        f.write(f"{graph.get_number_vertices()} {graph.edge_count}\n")
        for edge_id in range(graph.edge_count):
            source, target, weight = graph.get_edge_by_id(edge_id)
            f.write(f"{source} {target} {weight}\n")


def is_dag(graph: Graph):
    """Check if the graph is a Directed Acyclic Graph (DAG)."""
    in_degree = {vertex: 0 for vertex in graph.parse_vertices()} # Initialize in-degree of all vertices
    for vertex in graph.parse_vertices(): # Calculate in-degrees
        for neighbor, _ in graph.get_out_neighbours_for_vertex(vertex):
            in_degree[neighbor] += 1 # Increment in-degree for each neighbor

    queue = deque([vertex for vertex, degree in in_degree.items() if degree == 0]) # Initialize queue with vertices of in-degree 0
    visited_count = 0 #Initialised visit count

    while queue: #While we have something in the queue
        current = queue.popleft() #dequeue the first element
        visited_count += 1
        for neighbor, _ in graph.get_out_neighbours_for_vertex(current):
            in_degree[neighbor] -= 1 # Decrease in-degree of neighbors
            if in_degree[neighbor] == 0:  # If in-degree becomes 0, add to queue
                queue.append(neighbor)
    # If all vertices are visited, it's a DAG
    return visited_count == len(graph.out_neighbours)



def topological_sort(graph: Graph):
    """Performs a topological sorting of the graph."""
    in_degree = {vertex: 0 for vertex in graph.parse_vertices()} # Initialize in-degree of all vertices
    # Calculate in-degrees
    for vertex in graph.parse_vertices():
        for neighbor, _ in graph.get_out_neighbours_for_vertex(vertex):
            in_degree[neighbor] += 1
    # Initialize queue with vertices of in-degree 0
    queue = deque([vertex for vertex, degree in in_degree.items() if degree == 0])
    sorted_queue = []

    while queue:
        current = queue.popleft() #dequeue the first element
        sorted_queue.append(current)
        for neighbor, _ in graph.get_out_neighbours_for_vertex(current): # Decrease in-degree of neighbors
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_queue # Topologically sorted vertices


def longest_path(graph: Graph, start: int, finish: int):
    """Finds the longest path between two vertices in a directed graph."""
    if not is_dag(graph):
        raise ValueError("The graph is not a DAG")

    topological_order = topological_sort(graph)
    distances = {vertex: float('-inf') for vertex in graph.parse_vertices()}
    distances[start] = 0
    predecessors = {vertex: None for vertex in graph.parse_vertices()}

    for vertex in topological_order:
        for neighbor, weight in graph.get_out_neighbours_for_vertex(vertex):
            if distances[vertex] + weight > distances[neighbor]: # Update the distance if it's longer
                distances[neighbor] = distances[vertex] + weight
                predecessors[neighbor] = vertex # Update the predecessor

    path = [] # Reconstruct the path
    current = finish # Start from the finish vertex
    while current is not None: # While we have a predecessor
        path.append(current)
        current = predecessors[current] # Move to the predecessor

    path.reverse()
    return path, distances[finish]


#_____________________BONUS 1_____________________
def reconstruct_tree(pre_order : list , post_order: list, in_order: list):
    """
    Reconstructs a tree from three lists.
    :param pre_order: list parced in pre-order
    :param post_order: list parced in post-order
    :param in_order: list parced in in-order
    :return: a tree
    """
    if len(pre_order) == 0 or len(post_order) == 0 or len(in_order) == 0:
        return None

    root = pre_order[0] # The first element of the pre-order list is the root
    root_index = in_order.index(root) #Find the index of the root in the in-order list

    left_subtree = reconstruct_tree(pre_order[1:root_index + 1], post_order[:root_index], in_order[:root_index]) #Reconstruct the left subtree
    right_subtree = reconstruct_tree(pre_order[root_index + 1:], post_order[root_index:-1], in_order[root_index + 1:]) #Reconstruct the right subtree

    """
    preorder = ['A', 'B', 'C', 'D', 'E']
    postorder = ['B', 'D', 'E', 'C', 'A']
    inorder = ['B', 'A', 'D', 'C', 'E']
    """
    return root, left_subtree, right_subtree
def print_tree(node, level=0, is_left=None):
    """
    Prints the tree in a structured format.
    :param node: The current node (root, left, right).
    :param level: The current depth level of the tree.
    :param is_left: Whether the node is a left child.
    """
    if node is None:
        return

    root, left, right = node

    # Print the current node with indentation
    indent = " " * (4 * level)
    if level == 0:
        print(f"{indent}{root}")
    elif is_left:
        print(f"{indent}/ {root}")
    else:
        print(f"{indent}\\ {root}")

    # Recursively print the left and right subtrees
    print_tree(left, level + 1, is_left=True)
    print_tree(right, level + 1, is_left=False)




#_________________________BONUS 2_____________________

def bonus_2(graph : Graph):
    """
    Verify if it is a DAG.
    If it is:
    Perform a topological sort.
    Count the number of distinct paths from a start node to an end node in O(m + n) time.
    :param graph: Graph Object
    :return: A dictionary with the number of paths to each vertex
    """

    if not is_dag(graph):
        raise ValueError("The graph is not a DAG")

    topological_order = topological_sort(graph)
    paths_count = {vertex: 0 for vertex in graph.parse_vertices()}
    paths_count[topological_order[0]] = 1  # Start node has one path to itself
    for vertex in topological_order:
        for neighbor, _ in graph.get_out_neighbours_for_vertex(vertex):
            paths_count[neighbor] += paths_count[vertex]
    return paths_count


#_________________________BONUS 3_____________________

def bonus_3(graph : Graph):
    """
    Given a weighted graph:
    Verify if it is a DAG.
    If it is:
    Perform a topological sort.
    Find the number of distinct lowest-cost paths from a source node to a destination node in O(m + n) time.
    :param graph: graph object
    :return: dictionary with the number of paths to each vertex
    """
    if not is_dag(graph):
        raise ValueError("The graph is not a DAG")

    topological_order = topological_sort(graph)
    paths_count = {vertex: 0 for vertex in graph.parse_vertices()}
    paths_count[topological_order[0]] = 1  # Start node has one path to itself
    min_cost = {vertex: float('inf') for vertex in graph.parse_vertices()}
    min_cost[topological_order[0]] = 0

    # Iterate through the topological order
    for vertex in topological_order:
        for neighbor, weight in graph.get_out_neighbours_for_vertex(vertex):
            if min_cost[vertex] + weight < min_cost[neighbor]: # Update the minimum cost
                min_cost[neighbor] = min_cost[vertex] + weight
                paths_count[neighbor] = paths_count[vertex] # Reset the path
            elif min_cost[vertex] + weight == min_cost[neighbor]: # If the cost is equal, add the number of paths
                paths_count[neighbor] += paths_count[vertex]

    return paths_count

# Example usage
if __name__ == "__main__":
    print("DAG graph")
    graph = Graph("graph.txt")
    try:
        path, distance = longest_path(graph, 0, 5)
        print(f"Longest path: {path}")
        print(f"Distance: {distance}")
    except ValueError as e:
        print(e)

    print("\nNot DAG graph")
    #Exemple for a graph that is not DAG
    graph_no_DAG = Graph("no_dag.txt")
    try:
        path, distance = longest_path(graph_no_DAG, 0, 5)
        print(f"Longest path: {path}")
        print(f"Distance: {distance}")
    except ValueError as e:
        print(e)


#_____________________BONUS 1_____________________
print("__________Reconstructing tree from lists____________")
preorder = ['A', 'B', 'C', 'D', 'E']
inorder = ['B', 'A', 'D', 'C', 'E']
postorder = ['B', 'D', 'E', 'C', 'A']
tree = reconstruct_tree(preorder, postorder, inorder)
print_tree(tree)
"""
      A
     / \
    B   C
       / \
      D   E`

"""
preorder = [10, 5, 20, 15, 25]
postorder = [5, 15, 25, 20, 10]
inorder = [5, 10, 15, 20, 25]
tree = reconstruct_tree(preorder, postorder, inorder)
print_tree(tree)
"""
      10
     /  \
    5    20
        /  \
      15    25
"""

#_________________________BONUS 2_____________________
print("__________Counting paths in DAG____________")
graph = Graph("graph.txt")
number_paths_graph = bonus_2(graph)
print("Number of paths from start(vertex 0) to each vertex:")
for vertex, count in number_paths_graph.items():
    print(f"Vertex {vertex}: {count} paths")

try:
    number_paths_graph_no_dag = bonus_2(graph_no_DAG)
    print("Number of paths from start to each vertex:")
    for vertex, count in number_paths_graph_no_dag.items():
        print(f"Vertex {vertex}: {count} paths")
except ValueError as e:
    print(e)


#_________________________BONUS 3_____________________
print("__________Counting lowest-cost paths in DAG____________")
graph = Graph("graph_bonus_3.txt")

number_paths_graph = bonus_3(graph)
print("Number of lowest-cost paths from start(vertex 0) to each vertex:")
for vertex, count in number_paths_graph.items():
    print(f"Vertex {vertex}: {count} paths")
try:
    number_paths_graph_no_dag = bonus_3(graph_no_DAG)
    print("Number of lowest-cost paths from start to each vertex:")
    for vertex, count in number_paths_graph_no_dag.items():
        print(f"Vertex {vertex}: {count} paths")
except ValueError as e:
    print(e)

#Modified graph_bonus_3.txt for testing, path from 2 -> 4 is 5 instead of 3 -> modified output for lowest cost path from 0 -> 4
"""
6 8
0 1 1
0 2 1
1 3 2
2 3 2
1 4 3
2 4 3
3 5 1
4 5 1"""
"""
6 8
0 1 1
0 2 1
1 3 2
2 3 2
1 4 3
2 4 5
3 5 1
4 5 1
"""
