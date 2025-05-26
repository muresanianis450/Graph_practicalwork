
from graph import Graph

def primal_dual_vertex_cover(graph):
    """
    Finds a 2-approximate vertex cover using the Primal-Dual method.

    :param graph: instance of Graph (undirected)
    :return: set of vertices forming a vertex cover
    """
    num_vertices = graph.get_number_vertices()
    cover = set()  # Final vertex cover
    dual = {}  # Dual variables for each edge
    covered_edges = set()  # Set of covered edge IDs

    while len(covered_edges) < graph.edge_count:
        # Pick an uncovered edge (u, v)
        for edge_id in range(graph.edge_count):
            if edge_id in covered_edges:
                continue
            u, v, _ = graph.get_edge_by_id(edge_id)

            # Increase dual value for (u,v) until a constraint becomes tight
            # (i.e., a vertex hits the constraint of total dual weight ≤ 1)
            # Since we pick uncovered edge arbitrarily and increase its dual until tight, just include both u or v (here, any tight one)

            # For simplicity, add both u and v when (u,v) is uncovered (greedy primal-dual)
            if u not in cover and v not in cover:
                cover.add(u)
                cover.add(v)

            # Mark all edges incident to u or v as covered
            for neighbor, _ in graph.parse_out(u):
                eid = graph.is_edge(u, neighbor)
                if eid is not None:
                    covered_edges.add(eid)
            for neighbor, _ in graph.parse_out(v):
                eid = graph.is_edge(v, neighbor)
                if eid is not None:
                    covered_edges.add(eid)

            break  # Only process one uncovered edge at a time

    return cover


def run_primal_dual(file_path):
    print(f"\n📂 Running Primal-Dual Approximation on {file_path}")
    graph = Graph(file_path)
    cover = primal_dual_vertex_cover(graph)
    print(f"✅ Approximate Vertex Cover (≤ 2×OPT): {sorted(cover)}")
    print(f"🔢 Size of Vertex Cover: {len(cover)}")
    print(f"📌 Number of Vertices: {graph.get_number_vertices()}")
    print(f"📎 Number of Edges: {graph.edge_count}")
    print("=" * 50)

def main():
    files = ["graph.txt", "graph10.txt", "graph25.txt"]
    for file in files:
        run_primal_dual(file)

if __name__ == "__main__":
    main()