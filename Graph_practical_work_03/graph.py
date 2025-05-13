import random
import copy
import heapq

from fontTools.ttLib.ttVisitor import visit


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
        distances = {vertex: float('inf') for vertex in self.out_neighbours} # Initialise distance to all vertices to infinity
        distances[start_vertex] = 0 # Set distance to start vertex to 0

        #Path count keeps track of how many distinct paths(walks) lead to each vertex
        path_count = {vertex: 0 for vertex in self.out_neighbours} # Initialise path count to all vertices to 0
        path_count[start_vertex] = 1 # Set path count to start vertex to 1 (itself)

        #paths is a dictionary that stores all distinct walks of minimum cost to each vertex
        paths = {vertex: [] for vertex in self.out_neighbours}
        paths[start_vertex] = [[start_vertex]] #The only path to the start_vertex is itself

        # Priority queue for Dijkstra's algorithm
        # implemented as a heap to precess vertices in the order of increasing distance
        visited = set()
        priority_queue = [(0, start_vertex)]  # (distance, vertex) #Starts with start_vertex having a distance of 0


        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_vertex in visited: # Skip if already visited
                continue
            visited.add(current_vertex) # Add current vertex to visited set

            # Update neighboring vertices, for each neighbor of current_vertex we calculate
            # the new_distace to reach that neighbor by adding the edge weight to current_distance

            for neighbor, weight in self.out_neighbours[current_vertex]:
                new_distance = current_distance + weight

                # If the new distance is less than the current known distance, update it
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    path_count[neighbor] = path_count[current_vertex]
                    #We update path_count for the neighbor to inherit the path count of the current_vertex
                    #Because it is the minimum cost path to reach the neighbor
                    paths[neighbor] = [path + [neighbor] for path in paths[current_vertex]]
                    heapq.heappush(priority_queue, (new_distance, neighbor))

                #We add the new paths from current_vertex to neighbor to the paths dictionary and increment the path_count
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
        # Initialize distances and parents
        distances = {vertex: float('inf') for vertex in self.out_neighbours}
        distances[start_vertex] = 0
        parents = {vertex: None for vertex in self.out_neighbours}
        visited = set()

        # Priority queue setup
        priority_queue = [(0, start_vertex)]  # (distance, vertex)

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # Skip if already visited
            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            # Update neighboring vertices
            for neighbor, weight in self.out_neighbours[current_vertex]:
                if neighbor not in visited:
                    new_distance = current_distance + weight
                    # Relaxation: Update distance if a shorter path is found
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

#_________________BONUS 1____________________


def run_bonus_1():
    graph = Graph("graph50.txt")
    start_vertex = 0
    end_vertex = 4
    result = graph.count_min_cost_walks(start_vertex, end_vertex)
    print(f"Number of distinct walks of minimum cost from {start_vertex} to {end_vertex}: {result}")


print("_______________RUNNING PROBLEM_________________")

#run_problem_large_graph()          #!!!!!!!!!!!!!!!!!!!!!!!
run_problem1_simple_graph()


print("_______________RUNNING BONUS 1_________________")
run_bonus_1()





#______________BONUS 2____________________
from collections import defaultdict, deque
class DAG:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.graph = defaultdict(list) #Adjacency list representation of the graph
        self.in_degree = [0] * num_vertices # #In-degree of each vertex

    def add_edge(self, u, v):
        self.graph[u].append(v)  # u -> v is a directed edge
        self.in_degree[v] += 1   # increase in-degree of v

    def count_walks(self, start, end):
        # Step 1: Topological Sort (Kahn's Algorithm)
        topo_order = [] # Will store vertices in topological order
        # Initialize queue with vertices having in-degree of 0
        queue = deque([v for v in range(self.num_vertices) if self.in_degree[v] == 0])

        while queue:
            u = queue.popleft()
            topo_order.append(u) #Add the vertex to the topological order
            for v in self.graph[u]:
                self.in_degree[v] -= 1 #For each neighbour, decrease in-degree
                if self.in_degree[v] == 0: # If in-degree becomes 0, add to queue
                    queue.append(v)

        # Step 2: Dynamic Programming
        ways = [0] * self.num_vertices # ways[i] = number of ways to reach vertex i
        ways[start] = 1                # There's one way to reach the start vertex

        for u in topo_order:
            for v in self.graph[u]:
                ways[v] += ways[u]

        return ways[end]

#TODO show picture with the graph represented
def run_bonus_2():
    dag = DAG(6)
    dag.add_edge(0, 1)
    dag.add_edge(0, 2)
    dag.add_edge(1, 3)
    dag.add_edge(2, 3)
    dag.add_edge(3, 4)
    dag.add_edge(3, 5)

    start_vertex = 0
    end_vertex = 5

    print(f"Number of distinct walks from {start_vertex} to {end_vertex}:",
          dag.count_walks(start_vertex, end_vertex))
print("_______________RUNNING BONUS 2_________________")
run_bonus_2()                    #  !!!!!!!!!!!!!!!!!!!!!!!




#______________BONUS 3__________________

import heapq

def bridge_and_torch(times):
    """
    Solves the Bridge and Torch problem using the A* search algorithm.
    :param times: A list of integers where each element represents the time taken by a person to cross the bridge.
    :return: The minimum total time required for all people to cross the bridge.
    """
    n = len(times)  # Number of people
    people = list(range(n))  # List of people represented by their indices
    all_people = frozenset(people)  # Set of all people
    start_state = (all_people, 'L')  # Initial state: all people on the left side
    goal_state = (frozenset(), 'R')  # Goal state: all people on the right side

    def is_goal(state):
        """
        Checks if the current state is the goal state.
        :param state: The current state (set of people on the left, torch side).
        :return: True if the goal state is reached, False otherwise.
        """
        return state == goal_state

    def heuristic(state):
        """
        Heuristic function to estimate the remaining cost to reach the goal.
        :param state: The current state.
        :return: The maximum crossing time of people still on the left side if the torch is on the left,
                 otherwise 0 (no cost if the torch is on the right).
        """
        if state[1] == 'L':  # If the torch is on the left side
            return max([times[p] for p in state[0]]) if state[0] else 0
        else:  # If the torch is on the right side
            return 0

    def neighbors(state):
        """
        Generates all possible next states from the current state.
        :param state: The current state.
        :yield: A tuple containing the next state, the cost of the transition, and the people who moved.
        """
        left, torch_side = state
        if torch_side == 'L':  # Torch is on the left side
            # Move 1 or 2 people from left to right
            for p1 in left:
                for p2 in left:
                    if p2 < p1:  # Avoid duplicate pairs
                        continue
                    group = frozenset([p1, p2]) if p1 != p2 else frozenset([p1])
                    new_left = left - group  # Update the left side
                    cost = max(times[p1], times[p2]) if p1 != p2 else times[p1]
                    yield ((new_left, 'R'), cost, (p1, p2) if p1 != p2 else (p1,))
        else:  # Torch is on the right side
            # Move 1 person back from right to left
            right = all_people - left
            for p in right:
                new_left = left | frozenset([p])  # Update the left side
                cost = times[p]
                yield ((new_left, 'L'), cost, (p,))

    def a_star(start):
        """
        A* search algorithm to find the optimal solution.
        :param start: The initial state.
        :return: A tuple containing the total cost and the solution path, or None if no solution is found.
        """
        queue = [(heuristic(start), 0, start, [])]  # Priority queue: (estimated total cost, cost so far, state, path)
        visited = {}  # Dictionary to track visited states and their costs

        while queue:
            est_total_cost, cost_so_far, current_state, path = heapq.heappop(queue)

            if is_goal(current_state):  # If the goal state is reached
                return cost_so_far, path

            if current_state in visited and visited[current_state] <= cost_so_far:
                continue  # Skip if the state has already been visited with a lower cost
            visited[current_state] = cost_so_far  # Mark the state as visited

            # Explore neighbors
            for next_state, transition_cost, moved_people in neighbors(current_state):
                new_cost = cost_so_far + transition_cost
                new_path = path + [(current_state, moved_people, transition_cost)]
                est = new_cost + heuristic(next_state)  # Calculate the estimated total cost
                heapq.heappush(queue, (est, new_cost, next_state, new_path))
        return None  # Return None if no solution is found

    result = a_star(start_state)  # Run the A* algorithm
    if result is None:
        print("No solution found.")
        return

    total_time, solution_path = result

    # Display results
    print(f"Minimum total time: {total_time}")
    for idx, (state, moved, cost) in enumerate(solution_path):
        left_side = sorted(list(state[0]))
        torch = state[1]
        move_direction = "->" if torch == 'L' else "<-"
        names = " & ".join(f"Person {i} ({times[i]} min)" for i in moved)
        print(f"Step {idx+1}: {names} {move_direction}  ({cost} min)")

    return total_time
print("_______________RUNNING BONUS 3_________________")

#Example usage:
times = [1, 2, 5, 10]              #!!!!!!!!!!!!!!!!!!!!!!!
bridge_and_torch(times)





