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

# Exemple usage of finding connected components by simulating a non-directed graph
graph = Graph(7)
graph.add_edge(0,1,1)
graph.add_edge(1,2,1)
graph.add_edge(3,4,1)
graph.add_edge(4,5,1)
components = find_conected_components(graph)
print("Connected components:", components)



# Example usage of Kosaraju's algorithm(finding strongly connected components)
g = Graph(7)
g.add_edge(0, 1, 1)
g.add_edge(1, 2, 1)
g.add_edge(2, 0, 1)
g.add_edge(1, 3, 1)
g.add_edge(3, 4, 1)
g.add_edge(4, 5, 1)
g.add_edge(5, 3, 1)
g.add_edge(5, 6, 1)

sccs = kosaraju_scc(g)
print("Strongly connected components:", sccs)

# Example usage of Tarjan's algorithm(finding biconnected components)
g = Graph(7)
g.add_edge(0, 1, 1)
g.add_edge(1, 0, 1)
g.add_edge(1, 2, 1)
g.add_edge(2, 1, 1)
g.add_edge(1, 3, 1)
g.add_edge(3, 1, 1)
g.add_edge(3, 4, 1)
g.add_edge(4, 3, 1)
g.add_edge(4, 5, 1)
g.add_edge(5, 4, 1)
g.add_edge(5, 6, 1)
g.add_edge(6, 5, 1)

bccs = tarjan_bcc(g)
print("Biconnected components:", bccs)

solution = wolf_goat_cabbage()
print("Wolf, Goat, and Cabbage Solution:", solution)

import heapq


class PuzzleState:
    def __init__(self, board, empty_pos, moves=0, previous=None):
        self.board = board
        self.empty_pos = empty_pos
        self.moves = moves
        self.previous = previous
        self.h_cost = self.manhattan_distance()  # Precompute heuristic
        self.f_cost = self.moves + self.h_cost  # A* function: f(n) = g(n) + h(n)

    def __lt__(self, other):
        return self.f_cost < other.f_cost  # Use precomputed f-cost

    def manhattan_distance(self):
        """Compute the Manhattan distance heuristic."""
        distance = 0
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                if value != 0:  # Ignore empty tile
                    target_x = (value - 1) // 4
                    target_y = (value - 1) % 4
                    distance += abs(i - target_x) + abs(j - target_y)
        return distance

    def is_goal(self):
        """Check if the puzzle is solved."""
        return self.board == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

    def get_neighbors(self):
        """Generate valid neighboring states."""
        neighbors = []
        x, y = self.empty_pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 4 and 0 <= ny < 4:
                new_board = [row[:] for row in self.board]  # Deep copy
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                neighbors.append(PuzzleState(new_board, (nx, ny), self.moves + 1, self))
        return neighbors


def is_solvable(board):
    """Check if a given 15-puzzle configuration is solvable."""
    flat_board = [num for row in board for num in row if num != 0]
    inversions = sum(
        1 for i in range(len(flat_board)) for j in range(i + 1, len(flat_board)) if flat_board[i] > flat_board[j])

    # Find the row index of the empty tile, counting from the **bottom** (1-based index)
    empty_row = 4 - next(i for i, row in enumerate(board) if 0 in row)

    return (inversions + empty_row) % 2 == 0  # Correct condition for solvability


def solve_15_puzzle(initial_board):
    """Solve the 15-puzzle using an optimized A* search."""
    if not is_solvable(initial_board):
        return None  # If unsolvable, return None

    empty_pos = next((i, j) for i in range(4) for j in range(4) if initial_board[i][j] == 0)
    initial_state = PuzzleState(initial_board, empty_pos)

    priority_queue = []
    heapq.heappush(priority_queue, initial_state)

    visited = set()
    visited.add(tuple(map(tuple, initial_state.board)))  # Store only board state

    while priority_queue:
        current_state = heapq.heappop(priority_queue)

        if current_state.is_goal():
            path = []
            while current_state:
                path.append(current_state.board)
                current_state = current_state.previous
            return path[::-1]  # Return solution path

        for neighbor in current_state.get_neighbors():
            neighbor_tuple = tuple(map(tuple, neighbor.board))
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                heapq.heappush(priority_queue, neighbor)

    return None  # If no solution found (should never happen)


# Example usage
initial_board = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 15, 14, 0]
]

solution = solve_15_puzzle(initial_board)
for step in solution:
    for row in step:
        print(row)
    print()


