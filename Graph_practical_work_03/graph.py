import random
import copy
import heapq


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
    def get_out_neighbours_for_vertex(self,vertex):
        """
        Returns the out neighbours of a vertex
        :param vertex: the parent
        :return: the out neighbours

        """
        return self.out_neighbours[vertex]
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
        """Adds a directed edge from x to y with a given weight."""
        # Ensure both vertices exist in the graph
        if x not in self.out_neighbours:
            self.add_vertex(x)
        if y not in self.out_neighbours:
            self.add_vertex(y)

        # Add the edge if it doesn't already exist
        if y not in [neighbor for neighbor, _ in self.out_neighbours[x]]:
            self.out_neighbours[x].append((y, weight))
            self.edges[self.edge_count] = (x, y, weight)
            self.edge_count += 1
        return True

    def remove_edge(self, x, y):
        """Removes the directed edge from x to y."""
        for i, (neighbor, weight) in enumerate(self.out_neighbours[x]):
            if neighbor == y:
                del self.out_neighbours[x][i]
                return True

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

    def count_min_cost_walks(self, start_vertex, end_vertex):
        """
        Counts the number of distinct walks of minimum cost between start_vertex and end_vertex
        and prints all such walks.
        :param start_vertex: The starting vertex.
        :param end_vertex: The target vertex.
        :return: The number of distinct walks of minimum cost.
        """
        distances = {vertex: float('inf') for vertex in self.out_neighbours}
        distances[start_vertex] = 0
        path_count = {vertex: 0 for vertex in self.out_neighbours}
        path_count[start_vertex] = 1
        paths = {vertex: [] for vertex in self.out_neighbours}
        paths[start_vertex] = [[start_vertex]]
        visited = set()
        priority_queue = [(0, start_vertex)]  # (distance, vertex)

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            for neighbor, weight in self.out_neighbours[current_vertex]:
                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    path_count[neighbor] = path_count[current_vertex]
                    paths[neighbor] = [path + [neighbor] for path in paths[current_vertex]]
                    heapq.heappush(priority_queue, (new_distance, neighbor))
                elif new_distance == distances[neighbor]:
                    path_count[neighbor] += path_count[current_vertex]
                    paths[neighbor].extend(path + [neighbor] for path in paths[current_vertex])

        # Print all walks of minimum cost
        print(f"All distinct walks of minimum cost from {start_vertex} to {end_vertex}:")
        for walk in paths[end_vertex]:
            print(" -> ".join(map(str, walk)))

        return path_count[end_vertex]

    def dijkstra(self, start_vertex):
        """
        Dijkstra's algorithm to find the shortest path from a starting vertex to all other vertices.
        :param start_vertex: The starting vertex.
        :return: distances, parents
        """
        distances = {vertex: float('inf') for vertex in self.out_neighbours}
        distances[start_vertex] = 0
        parents = {vertex: None for vertex in self.out_neighbours}
        visited = set()
        priority_queue = [(0, start_vertex)]  # (distance, vertex)

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            for neighbor, weight in self.out_neighbours[current_vertex]:
                if neighbor not in visited:
                    new_distance = current_distance + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        parents[neighbor] = current_vertex
                        heapq.heappush(priority_queue, (new_distance, neighbor))

        return distances, parents

    def print_graph(graph):
        """
        Prints all vertices and edges of the graph, including their weights.
        :param graph: The graph object.
        """
        print("Graph vertices and their outgoing edges:")
        for vertex in graph.parse_vertices():
            print(f"Vertex {vertex}:")
            for neighbor, weight in graph.get_out_neighbours_for_vertex(vertex):
                print(f"  -> {neighbor} (weight: {weight})")




def results(distances, parents, start_vertex):
    # Print results
    print("Shortest distances from vertex", start_vertex)
    for vertex, distance in distances.items():
        print(f"Vertex {vertex}: {distance}")

    print("\nShortest paths:")
    for vertex in distances:
        if distances[vertex] == float('inf'):
            print(f"Path to {vertex}: No path")
            continue

        path = []
        current = vertex
        while current is not None:
            path.append(current)
            current = parents[current]
        print(f"Path to {vertex}: {' -> '.join(map(str, reversed(path)))}")

def run_problem1_simple_graph():
    # Example simulation
    graph = Graph()
    #graph.print_graph()

    # Run Dijkstra's algorithm
    start_vertex = 1
    distances, parents = graph.dijkstra(start_vertex)
    results(distances, parents, start_vertex)

def run_problem_large_graph():
    graph = Graph("graph1k.txt")
    start_vertex = 1
    distances, parents = graph.dijkstra(start_vertex)
    results(distances, parents, start_vertex)


#TODO show notion photo with the graph represented
def run_bonus_1():
    graph = Graph("graph50.txt")
    start_vertex = 0
    end_vertex = 4
    result = graph.count_min_cost_walks(start_vertex, end_vertex)
    print(f"Number of distinct walks of minimum cost from {start_vertex} to {end_vertex}: {result}")



#run_problem_large_graph()
#run_problem1_simple_graph()
run_bonus_1()









