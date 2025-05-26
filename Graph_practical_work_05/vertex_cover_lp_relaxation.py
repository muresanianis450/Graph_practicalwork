import numpy as np
from graph import Graph
from scipy.optimize import linprog
def vertex_cover_lp_relaxation(graph):
    """
    Finds a vertex cover using LP relaxation and rounding.

    :param graph: instance of Graph
    :return: set of vertices forming a vertex cover (2-approximation)
    """

    num_vertices = graph.get_number_vertices()
    num_edges = graph.edge_count

    # Objective: Minimize sum of x_i (vertex variables)
    c = np.ones(num_vertices)

    # Constraints: For each edge (u, v), x_u + x_v >= 1
    # Rewrite as: -x_u - x_v <= -1 for linprog standard form
    A = np.zeros((num_edges, num_vertices))
    b = np.full(num_edges, -1)

    for i in range(num_edges):
        u, v, _ = graph.edges[i]
        A[i, u] = -1
        A[i, v] = -1

    # Bounds for each x_i: 0 <= x_i <= 1
    bounds = [(0, 1) for _ in range(num_vertices)]

    # Solve LP using linprog (minimize c^T x subject to A x <= b)
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if not result.success:
        raise Exception("LP solver failed: " + result.message)

    x = result.x  # fractional solution

    # Rounding: Include vertices with x_i >= 0.5
    vertex_cover = {v for v in range(num_vertices) if x[v] >= 0.5}

    return vertex_cover

def run_lp_approximation(file_path):
    print(f"\nRunning LP Relaxation on {file_path}")
    graph = Graph(file_path)
    cover = vertex_cover_lp_relaxation(graph)
    print(f"Approximate Vertex Cover (≤ 2×OPT): {sorted(cover)}")
    print(f"Size of Vertex Cover: {len(cover)}")
    print(f"Number of Vertices: {graph.get_number_vertices()}")
    print(f"Number of Edges: {graph.edge_count}")

def main():
    files = ["graph.txt", "graph10.txt", "graph25.txt"]
    for file in files:
        run_lp_approximation(file)

#if __name__ == "__main__":
 #   main()