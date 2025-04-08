from Graph_practical_work_02.graph import Graph
from collections import deque
import heapq
# This code implements Kosaraju's algorithm to find strongly connected components in a directed graph.
def kosaraju_scc(g: Graph):
    """
    Finds the strongly connected components of a directed graph using Kosaraju's algorithm.
    :param g: Graph object
    :return: List of strongly connected components
    """
    def dfs(graph, node, visited, stack):
        visited.add(node)
        for neighbour, _ in graph.get_out_neighbours_for_vertex(node):
            if neighbour not in visited:
                dfs(graph, neighbour, visited, stack)
        stack.append(node)

    def reverse_graph(graph):
        reversed_g = Graph(graph.get_number_vertices())
        for edge_id in range(graph.edge_count):
            source, target, weight = graph.get_edge_by_id(edge_id)
            reversed_g.add_edge(target, source, weight)
        return reversed_g

    def fill_order(graph, visited, stack):
        for vertex in range(graph.get_number_vertices()):
            if vertex not in visited:
                dfs(graph, vertex, visited, stack)

    def get_sccs(graph, stack):
        visited = set()
        sccs = []
        while stack:
            node = stack.pop()
            if node not in visited:
                component = []
                dfs(graph, node, visited, component)
                sccs.append(component)
        return sccs

    stack = []
    visited = set()
    fill_order(g, visited, stack)
    reversed_g = reverse_graph(g)
    sccs = get_sccs(reversed_g, stack)
    return sccs



def dfs(g: Graph, node, visited, component):
    """
    Depth First Search
    :param g: graph object
    :param node: starting vertex
    :param visited: set of visited vertices
    :param component: list of vertices in the order they were visited
    :return: None
    """
    visited.add(node)
    component.append(node)
    for neighbour, _ in g.get_out_neighbours_for_vertex(node):
        if neighbour not in visited:
            dfs(g, neighbour, visited, component)

def find_conected_components(g):
    """
    Finds the connected components of the graph
    :param g: Graph object
    :return: list of connected components
    """
    visited = set()
    components = []
    for node in range(g.get_number_vertices()):
        if node not in visited:
            component = []  # Store current component
            dfs(g, node, visited, component)
            components.append(component)
    return components

# This code implements Tarjan's algorithm to find biconnected components in an undirected graph.
def tarjan_bcc(g: Graph):
    """
    Finds the biconnected components of an undirected graph using Tarjan's algorithm.
    :param g: Graph object
    :return: List of biconnected components
    """
    def dfs(u, parent, time):
        nonlocal current_time
        visited[u] = True
        discovery_time[u] = low[u] = current_time
        current_time += 1
        children = 0
        stack.append(u)

        for v, _ in g.get_out_neighbours_for_vertex(u):
            if not visited[v]:
                children += 1
                parent[v] = u
                dfs(v, parent, time)
                low[u] = min(low[u], low[v])

                if (parent[u] is None and children > 1) or (parent[u] is not None and low[v] >= discovery_time[u]):
                    bcc = []
                    while stack[-1] != v:
                        bcc.append(stack.pop())
                    bcc.append(stack.pop())
                    bcc.append(u)
                    biconnected_components.append(bcc)
            elif v != parent[u]:
                low[u] = min(low[u], discovery_time[v])

    current_time = 0
    visited = [False] * g.get_number_vertices()
    discovery_time = [-1] * g.get_number_vertices()
    low = [-1] * g.get_number_vertices()
    parent = [None] * g.get_number_vertices()
    stack = []
    biconnected_components = []

    for i in range(g.get_number_vertices()):
        if not visited[i]:
            dfs(i, parent, current_time)

    return biconnected_components


def wolf_goat_cabbage():
    initial_state = (1, 1, 1, 1)  # (man, wolf, goat, cabbage) on the left bank
    goal_state = (0, 0, 0, 0)  # (man, wolf, goat, cabbage) on the right bank
    visited = set()
    queue = deque([(initial_state, [])])

    def is_valid(state):
        man, wolf, goat, cabbage = state
        if wolf == goat and man != wolf:
            return False
        if goat == cabbage and man != goat:
            return False
        return True

    while queue:
        state, path = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        if state == goal_state:
            return path

        man, wolf, goat, cabbage = state
        next_states = [
            (1 - man, wolf, goat, cabbage),
            (1 - man, 1 - wolf, goat, cabbage) if man == wolf else None,
            (1 - man, wolf, 1 - goat, cabbage) if man == goat else None,
            (1 - man, wolf, goat, 1 - cabbage) if man == cabbage else None,
        ]

        for next_state in next_states:
            if next_state and is_valid(next_state):
                queue.append((next_state, path + [next_state]))

    return None

# Example usage of finding connected components by simulating a non-directed graph
graph = Graph(7)
graph.add_edge(0, 1, 1)
graph.add_edge(1, 0, 1)  # Add reverse edge
graph.add_edge(1, 2, 1)
graph.add_edge(2, 1, 1)  # Add reverse edge
graph.add_edge(3, 4, 1)
graph.add_edge(4, 3, 1)  # Add reverse edge
graph.add_edge(4, 5, 1)
graph.add_edge(5, 4, 1)  # Add reverse edge
components = find_conected_components(graph)
print("Connected components:", components)



# Example usage of Kosaraju's algorithm(finding strongly connected components)
g = Graph(7)
g.add_edge(0, 1, 1)
g.add_edge(1, 2, 1)
#g.add_edge(2, 0, 1)
#g.add_edge(1, 3, 1)
g.add_edge(3, 4, 1)
g.add_edge(4, 5, 1)
g.add_edge(5, 3, 1)
g.add_edge(5, 6, 1)

sccs = kosaraju_scc(g)
print("Strongly connected components:", sccs)

# Example usage of Tarjan's algorithm(finding biconnected components)
g = Graph(7)
g.add_edge(0, 1, 1)
#g.add_edge(1, 0, 1)
g.add_edge(1, 2, 1)
#g.add_edge(2, 1, 1)
g.add_edge(1, 3, 1)
#g.add_edge(3, 1, 1)
g.add_edge(3, 4, 1)
g.add_edge(4, 3, 1)
g.add_edge(4, 5, 1)
g.add_edge(5, 4, 1)
g.add_edge(5, 6, 1)
g.add_edge(6, 5, 1)
g.add_edge(3,6,1)
g.add_edge(6, 3, 1)

bccs = tarjan_bcc(g)
print("Biconnected components:", bccs)

solution = wolf_goat_cabbage()
print("Wolf, Goat, and Cabbage Solution:", solution)


import heapq
from copy import deepcopy

class Fifteen:
    def __init__(self, tiles=None, parent=None, move=None):
        self.goal_positions = self._compute_goal_positions()
        self.previous_moves = parent.previous_moves + [move] if parent else []
        self.depth = parent.depth + 1 if parent else 0
        self.tiles = [row[:] for row in tiles] if tiles else self.default_board()  # Avoid deepcopy
        self.zero_x, self.zero_y = self.find(0)
        self.h_score = self.manhattan()
        self.undo_move = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}.get(move, None)

    def default_board(self):
        return [[1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [0, 13, 14, 15]
        ]

    def _compute_goal_positions(self):
        goal = {}
        for i in range(4):
            for j in range(4):
                val = i * 4 + j + 1
                goal[val % 16] = (j, i)
        return goal

    def find(self, tile):
        for y in range(4):
            for x in range(4):
                if self.tiles[y][x] == tile:
                    return x, y

    def move_tile(self, direction):
        x, y = self.zero_x, self.zero_y
        dxdy = {'u': (0, -1), 'd': (0, 1), 'l': (-1, 0), 'r': (1, 0)}
        dx, dy = dxdy[direction]
        new_x, new_y = x + dx, y + dy

        if not (0 <= new_x < 4 and 0 <= new_y < 4):
            return None

        new_tiles = [row[:] for row in self.tiles]  # Avoid deepcopy
        new_tiles[y][x], new_tiles[new_y][new_x] = new_tiles[new_y][new_x], new_tiles[y][x]
        return Fifteen(new_tiles, self, direction)

    def generate_next_states(self):
        directions = ['u', 'd', 'l', 'r']
        next_states = []
        for dir in directions:
            if dir != self.undo_move:  # Avoid reversing the last move
                new_state = self.move_tile(dir)
                if new_state:
                    next_states.append(new_state)
        return next_states

    def manhattan(self):
        return sum(
            abs(x - self.goal_positions[val][0]) + abs(y - self.goal_positions[val][1])
            for y in range(4) for x in range(4)
            if (val := self.tiles[y][x]) != 0
        )

    def __lt__(self, other):
        return (self.depth + self.h_score) < (other.depth + other.h_score)

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.tiles))

    def __eq__(self, other):
        return self.tiles == other.tiles

    def astar(self):
        queue = [(self.h_score, self)]
        visited = set()

        while queue:
            _, current = heapq.heappop(queue)
            state_hash = hash(current)
            if state_hash in visited:
                continue
            visited.add(state_hash)

            if current.h_score == 0:
                print("Solution found!")
                current.show_steps()
                print(f"Total moves: {len(current.previous_moves)}")
                return

            for neighbor in current.generate_next_states():
                if hash(neighbor) not in visited:
                    heapq.heappush(queue, (neighbor.depth + neighbor.h_score, neighbor))

        print("No solution found.")

    def show_steps(self):
        state = deepcopy(self)
        print("Initial State:")
        state.PrintState()
        for move in self.previous_moves:
            print(f"Move: {move}")
            next_state = state.move_tile(move)
            if next_state:  # Ensure the move is valid
                state = next_state
                state.PrintState()

    def PrintState(self):
        for row in self.tiles:
            print(" ".join(f"{n:2}" for n in row))
        print()


fifteen = Fifteen()
fifteen.astar()
