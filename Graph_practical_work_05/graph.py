import random
import copy

class Graph:
    def __init__(self, v="graph.txt"):
        """
        Constructor for the graph class. Reads from a file if 'v' is a string (filename).
        If 'v' is an integer, creates a graph with vertices from 0 to v-1.

        :param v: Can be an integer for the number of vertices or a string with the filename to read from.
        """
        self.out_neighbours = {}  # Adjacency list (with weights)
        self.edges = {}  # Mapping EDGE_ID -> (source, target, weight)
        self.edge_count = 0

        # If v is a filename (string), read the graph from the file
        if isinstance(v, str):
            self._read_from_file(v)
        # If v is an integer, create a graph with v vertices
        elif isinstance(v, int):
            for vertex in range(v):
                self.out_neighbours[vertex] = []

    def _read_from_file(self, file_name):
        """
        Reads a graph from the specified file.

        :param file_name: The filename from which the graph is read.
        """
        with open(file_name, "r") as f:
            # Read the number of vertices and edges (not used here, since we're reading lines)
            x, y = map(int, f.readline().split())
            self.__init__(x)  # Re-initialize the graph with 'x' vertices

            # Read the edges with weights and add them to the graph
            for line in f:
                u, v, w = map(int, line.split())
                self.add_edge(u, v, w)

    def add_edge(self, x, y, weight):
        """Adds an undirected edge between x and y with a given weight."""
        if y not in [neighbor for neighbor, _ in self.out_neighbours.get(x, [])]:
            self.out_neighbours.setdefault(x, []).append((y, weight))
            self.out_neighbours.setdefault(y, []).append((x, weight))  # Add reverse edge
            self.edges[self.edge_count] = (x, y, weight)
            self.edge_count += 1
            return True
        else:
            return False

    def remove_edge(self, x, y):
        """Removes the undirected edge between x and y."""
        removed = False
        for i, (neighbor, weight) in enumerate(self.out_neighbours.get(x, [])):
            if neighbor == y:
                del self.out_neighbours[x][i]
                removed = True
                break
        for i, (neighbor, weight) in enumerate(self.out_neighbours.get(y, [])):
            if neighbor == x:
                del self.out_neighbours[y][i]
                removed = True
                break
        return removed

    def remove_vertex(self, x):
        """Removes vertex x from the graph."""
        if x in self.out_neighbours:
            del self.out_neighbours[x]
            return True
        else:
            return False

    def add_vertex(self, x):
        """Adds vertex x to the graph."""
        if x not in self.out_neighbours:
            self.out_neighbours[x] = []
        else:
            raise ValueError("Vertex already exists")

    def get_edge_by_id(self, edge_id):
        """Returns the edge with the given ID."""
        return self.edges.get(edge_id, None)

    def parse_out(self, x):
        """Returns an iterable containing all outbound neighbors of x."""
        return [(neighbor, weight) for neighbor, weight in self.out_neighbours[x]]

    def get_number_vertices(self):
        """Returns the number of vertices in the graph."""
        return len(self.out_neighbours)

    def parse_vertices(self):
        """Returns an iterable containing all vertices of the graph."""
        return self.out_neighbours.keys()

    @staticmethod
    def read_from_file(file_name):
        """Static method to read a graph from a file."""
        with open(file_name, "r") as f:
            x, y = map(int, f.readline().split())
            graph = Graph(x)  # Initialize the graph with x vertices
            for line in f:
                u, v, w = map(int, line.split())
                graph.add_edge(u, v, w)
        return graph

    def is_edge(self, x, y):
        """
        Returns True if there is an edge from x to y in the graph.
        :param x: source vertex
        :param y: target vertex
        :return: returns the edge_id from x to y if it exists, otherwise None
        """
        for edge_id in range(self.edge_count):
            source, target, _ = self.edges[edge_id]
            if source == x and target == y:
                return edge_id
        return None

    def generate_random_graph(self, number_vertices, number_edges):
        """
        Generates a random graph.
        :param number_vertices: number of vertices
        :param number_edges: number of edges
        """
        self.__init__(number_vertices)  # Re-initialize the graph with the given number of vertices
        for _ in range(number_edges):
            x = random.randint(0, number_vertices - 1)
            y = random.randint(0, number_vertices - 1)
            weight = random.randint(1, 100)  # Random weight between 1 and 100
            if x != y and self.is_edge(x, y) is None:
                self.add_edge(x, y, weight)

    def deepcopy(self):
        """
        Creates a deep copy of the graph.
        :return: A new Graph object that is a deep copy of the current graph.
        """
        new_graph = Graph()
        new_graph.out_neighbours = copy.deepcopy(self.out_neighbours)
        new_graph.edges = copy.deepcopy(self.edges)
        new_graph.edge_count = self.edge_count
        return new_graph


def write_to_file(graph: Graph, file_name):
    """
    Writes the graph to a file.
    :param graph: graph object
    :param file_name: file name
    """
    with open(file_name, "w") as f:
        f.write(f"{graph.get_number_vertices()} {graph.edge_count}\n")
        for edge_id in range(graph.edge_count):
            source, target, weight = graph.get_edge_by_id(edge_id)
            f.write(f"{source} {target} {weight}\n")







