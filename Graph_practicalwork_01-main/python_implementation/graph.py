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
        """Adds an edge from x to y with a given weight."""
        if y not in self.out_neighbours[x]:
            self.out_neighbours[x].append((y, weight))
            self.edges[self.edge_count] = (x, y, weight)
            self.edge_count += 1
            return True
        else:
            return False

    def remove_edge(self, x, y):
        """Removes the edge from x to y."""
        for i, (neighbor, weight) in enumerate(self.out_neighbours[x]):
            if neighbor == y:
                del self.out_neighbours[x][i]
                return True
        return False

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

class GraphUI:

    def __init__(self, graph=None):
        """
        Initializes the UI with a graph.
        If no graph is provided, a random graph is created by default.
        """
        if graph is None:
            self.graph = Graph("graph.txt")  # Default to reading from "graph.txt"
        else:
            self.graph = graph
        self.deep_copied_graph = None  # To store the deep copy of the graph

    def load_graph_from_file_ui(self):
        """Prompts user to load a graph from a file."""
        file_name = input("Enter file name to load the graph: ")
        self.graph = Graph.read_from_file(file_name)
        print(f"Graph loaded from {file_name}")

    def save_graph_to_file_ui(self):
        """Prompts user to save the graph to a file."""
        file_name = input("Enter file name to save the graph: ")
        write_to_file(self.graph, file_name)
        print(f"Graph saved to {file_name}")

    def print_deep_copy(self):
        """Prints the deep copy of the graph."""
        if self.deep_copied_graph:
            print("\nDeep Copy of Graph:")
            print("Vertices:", list(self.deep_copied_graph.parse_vertices()))
            for edge_id, (source, target, weight) in self.deep_copied_graph.edges.items():
                print(f"Edge {edge_id}: {source} -> {target} (Weight: {weight})")
        else:
            print("No deep copy available to print.")

    def save_deep_copy_to_file_ui(self):
        """Saves the deep copy of the graph to a file."""
        if self.deep_copied_graph:
            write_to_file(self.deep_copied_graph, "deepcopy.txt")
            print("Deep copy of the graph saved to deepcopy.txt")
        else:
            print("No deep copy available to save.")

    def display_menu(self):
        """Displays the console menu for user interaction."""
        print("\nGraph Menu:")
        print("1. Show Graph")
        print("2. Add Vertex")
        print("3. Remove Vertex")
        print("4. Add Edge")
        print("5. Remove Edge")
        print("6. Get In-Degree of a Vertex")
        print("7. Get Out-Degree of a Vertex")
        print("8. Check if an Edge Exists")
        print("9. Show All Vertices")
        print("10. Show Outbound Edges of a Vertex")
        print("11. Show Inbound Edges of a Vertex")
        print("12. Save Graph to File")
        print("13. Load Graph from File")
        print("14. Generate Random Graph")
        print("15. Deep Copy Graph")
        print("16. Save Deep Copy to File")
        print("17. Print Deep Copy")
        print("18. Exit")

    def handle_menu_option(self, option):
        """Handles user input and executes the corresponding graph operation."""
        if option == 1:
            self.show_graph()
        elif option == 2:
            self.add_vertex_ui()
        elif option == 3:
            self.remove_vertex_ui()
        elif option == 4:
            self.add_edge_ui()
        elif option == 5:
            self.remove_edge_ui()
        elif option == 6:
            self.get_in_degree_ui()
        elif option == 7:
            self.get_out_degree_ui()
        elif option == 8:
            self.check_edge_ui()
        elif option == 9:
            self.show_vertices()
        elif option == 10:
            self.show_outbound_edges_ui()
        elif option == 11:
            self.show_inbound_edges_ui()
        elif option == 12:
            self.save_graph_to_file_ui()
        elif option == 13:
            self.load_graph_from_file_ui()
        elif option == 14:
            self.generate_random_graph_ui()
        elif option == 15:
            self.deep_copy_graph_ui()
        elif option == 16:
            self.save_deep_copy_to_file_ui()
        elif option == 17:
            self.print_deep_copy()
        elif option == 18:
            print("Exiting...")
            return False
        else:
            print("Invalid option. Please try again.")
        return True

    def show_graph(self):
        """Displays the graph's vertices and edges for visualization."""
        print("\nGraph:")
        print("Vertices:", list(self.graph.parse_vertices()))
        for edge_id, (source, target, weight) in self.graph.edges.items():
            print(f"Edge {edge_id}: {source} -> {target} (Weight: {weight})")

    def add_vertex_ui(self):
        """Prompt user to add a vertex to the graph."""
        vertex = int(input("Enter vertex to add: "))
        self.graph.add_vertex(vertex)
        print(f"Vertex {vertex} added.")

    def remove_vertex_ui(self):
        """Prompt user to remove a vertex from the graph."""
        vertex = int(input("Enter vertex to remove: "))
        self.graph.remove_vertex(vertex)
        print(f"Vertex {vertex} removed.")

    def add_edge_ui(self):
        """Prompt user to add an edge to the graph."""
        x = int(input("Enter source vertex: "))
        y = int(input("Enter target vertex: "))
        weight = int(input("Enter weight of the edge: "))
        if self.graph.add_edge(x, y, weight):
            print(f"Edge {x} -> {y} with weight {weight} added.")
        else:
            print(f"Edge {x} -> {y} already exists.")

    def remove_edge_ui(self):
        """Prompt user to remove an edge from the graph."""
        x = int(input("Enter source vertex: "))
        y = int(input("Enter target vertex: "))
        if self.graph.remove_edge(x, y):
            print(f"Edge {x} -> {y} removed.")
        else:
            print(f"Edge {x} -> {y} does not exist.")

    def get_in_degree_ui(self):
        """Prompt user to get the in-degree of a vertex."""
        vertex = int(input("Enter vertex to get in-degree: "))
        in_degree = self.graph.get_in_degree(vertex)
        print(f"In-degree of vertex {vertex}: {in_degree}")

    def get_out_degree_ui(self):
        """Prompt user to get the out-degree of a vertex."""
        vertex = int(input("Enter vertex to get out-degree: "))
        out_degree = self.graph.get_out_degree(vertex)
        print(f"Out-degree of vertex {vertex}: {out_degree}")

    def check_edge_ui(self):
        """Prompt user to check if an edge exists."""
        x = int(input("Enter source vertex: "))
        y = int(input("Enter target vertex: "))
        edge_id = self.graph.is_edge(x, y)
        if edge_id is not None:
            print(f"Edge {x} -> {y} exists with edge ID: {edge_id}")
        else:
            print(f"Edge {x} -> {y} does not exist.")

    def show_vertices(self):
        """Displays all vertices in the graph."""
        print("\nVertices:", list(self.graph.parse_vertices()))

    def show_outbound_edges_ui(self):
        """Displays outbound edges of a vertex."""
        vertex = int(input("Enter vertex to show outbound edges: "))
        edges = self.graph.parse_out(vertex)
        print(f"Outbound edges for vertex {vertex}:")
        for target, weight in edges:
            print(f"Target: {target}, Weight: {weight}")

    def show_inbound_edges_ui(self):
        """Displays inbound edges of a vertex."""
        vertex = int(input("Enter vertex to show inbound edges: "))
        inbound_edges = [(source, edge_id) for edge_id, (source, target, _) in self.graph.edges.items() if target == vertex]
        print(f"Inbound edges for vertex {vertex}:")
        for source, edge_id in inbound_edges:
            print(f"Source: {source}, Edge ID: {edge_id}")

    def generate_random_graph_ui(self):
        """Generates a random graph."""
        number_vertices = int(input("Enter number of vertices: "))
        number_edges = int(input("Enter number of edges: "))
        self.graph.generate_random_graph(number_vertices, number_edges)
        print(f"Random graph generated with {number_vertices} vertices and {number_edges} edges.")

    def deep_copy_graph_ui(self):
        """Creates a deep copy of the graph."""
        self.deep_copied_graph = self.graph.deepcopy()
        print("Deep copy of the graph created. You can now modify them independently.")

    def run(self):
        """Runs the menu-driven UI in a loop."""
        while True:
            self.display_menu()
            option = int(input("Enter option: "))
            if not self.handle_menu_option(option):
                break


# Example usage:
if __name__ == "__main__":
    ui = GraphUI()  # Initialize UI with graph from "graph.txt"
    ui.run()  # Start the console-based menu system