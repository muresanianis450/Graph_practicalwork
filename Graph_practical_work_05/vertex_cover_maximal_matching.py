from graph import Graph

def vertex_cover_maximal_matching(graph):
    """
    Finds a vertex cover using the maximal matching 2-approximation algorithm.

    :param graph: instance of Graph
    :return: set of vertices forming a vertex cover
    """
    matched_vertices = set()  # vertices that are already matched
    vertex_cover = set()

    # Iterate over all edges
    for edge_id in range(graph.edge_count):
        u, v, _ = graph.edges[edge_id]

        # If neither endpoint is matched, pick this edge for matching
        if u not in matched_vertices and v not in matched_vertices:
            matched_vertices.add(u)
            matched_vertices.add(v)
            vertex_cover.add(u)
            vertex_cover.add(v)

    return vertex_cover
if __name__ == "__main__":
    g = Graph("graph.txt")
    cover = vertex_cover_maximal_matching(g)
    print("Vertex cover (2-approx by maximal matching):", cover)
    g2 = Graph("graph10.txt")
    cover = vertex_cover_maximal_matching(g2)
    print("Vertex cover (2-approx by maximal matching):", cover)
    g3 = Graph("graph25.txt")
    cover = vertex_cover_maximal_matching(g3)
    print("Vertex cover (2-approx by maximal matching):", cover)