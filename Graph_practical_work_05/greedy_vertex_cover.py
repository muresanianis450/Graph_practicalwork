from graph import Graph

def greedy_vertex_cover(graph: Graph):
    """
    2-Approximation algorithm for Minimum Vertex Cover using a greedy approach.

    :param graph: An instance of the Graph class (undirected)
    :return: A set containing the approximate vertex cover
    """
    # Make a deepcopy of the graph to safely modify it
    g_copy = graph.deepcopy()
    cover = set()

    # Keep track of all covered edges
    while g_copy.edge_count > 0:
        # Pick any edge (from the edges dictionary)
        edge_id, (u, v, _) = next(iter(g_copy.edges.items()))  # Get any edge

        # Add both endpoints of the edge to the cover
        cover.add(u)
        cover.add(v)

        # Remove all edges incident to u or v
        incident_edges = list(g_copy.edges.items())  # Create a static list of edges
        for eid, (x, y, _) in incident_edges:
            if x == u or y == u or x == v or y == v:  # Check if edge is incident to u or v
                g_copy.remove_edge(x, y)  # Remove edge from adjacency list
                del g_copy.edges[eid]  # Remove edge from edges dictionary
                g_copy.edge_count -= 1

    return cover


if __name__ == "__main__":
    g = Graph("graph.txt")  # Or Graph(5) + g.add_edge(...)
    cover = greedy_vertex_cover(g)
    print("Approximate vertex cover (≤ 2×OPT):", cover)
    g25 = Graph("graph25.txt")
    cover = greedy_vertex_cover(g25)
    print("Approximate vertex cover for graph25 (≤ 2×OPT):", cover)
    g10 = Graph("graph10.txt")
    cover = greedy_vertex_cover(g10)
    print("Approximate vertex cover for graph10 (≤ 2×OPT):", cover)