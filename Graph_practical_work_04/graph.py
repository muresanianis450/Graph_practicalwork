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
            if distances[vertex] + weight > distances[neighbor]:
                distances[neighbor] = distances[vertex] + weight
                predecessors[neighbor] = vertex

    path = []
    current = finish
    while current is not None:
        path.append(current)
        current = predecessors[current]

    path.reverse()
    return path, distances[finish]


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
