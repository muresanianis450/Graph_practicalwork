import random
from graph import Graph
def local_search_vertex_cover(graph, max_iterations=1000):
    """
    Local search heuristic for the Vertex Cover problem.
    Tries to remove vertices from the cover while maintaining edge coverage.

    :param graph: instance of Graph
    :param max_iterations: maximum number of iterations
    :return: approximate vertex cover
    """
    # Start with a naive cover: include both endpoints of every edge
    cover = set()
    for _, (u, v, _) in graph.edges.items():
        cover.add(u)
        cover.add(v)

    def is_valid_cover(cover_set):
        """Check if all edges are covered by the current vertex set."""
        for _, (u, v, _) in graph.edges.items():
            if u not in cover_set and v not in cover_set:
                return False
        return True

    vertices = list(cover)
    iterations = 0
    improved = True

    while improved and iterations < max_iterations:
        improved = False
        random.shuffle(vertices)
        for v in vertices:
            new_cover = cover - {v}
            if is_valid_cover(new_cover):
                cover = new_cover
                vertices.remove(v)
                improved = True
                break
        iterations += 1

    return cover


def run_local_search(file_path):
    print(f"\n📂 Running Local Search Heuristic on {file_path}")
    graph = Graph(file_path)
    cover = local_search_vertex_cover(graph)
    print(f"✅ Approximate Vertex Cover (no guarantee): {sorted(cover)}")
    print(f"🔢 Size of Vertex Cover: {len(cover)}")
    print(f"📌 Number of Vertices: {graph.get_number_vertices()}")
    print(f"📎 Number of Edges: {graph.edge_count}")
    print("=" * 50)

def main_heuristic():
    files = ["graph.txt", "graph10.txt", "graph25.txt"]
    for file in files:
        run_local_search(file)

if __name__ == "__main__":
    main_heuristic()
