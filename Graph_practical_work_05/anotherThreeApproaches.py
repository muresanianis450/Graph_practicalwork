
from graph import Graph
import random

def high_degree_vertex_cover(graph: Graph):
    """
    Heuristic approach: repeatedly pick the vertex with the highest degree.
    """
    g_copy = graph.deepcopy()  # Make a copy to preserve the original graph
    cover = set()  # This will store the selected vertex cover

    # Repeat until all edges are removed
    while g_copy.edge_count > 0:
        # Compute the degree of each vertex (i.e., number of neighbors)
        degrees = {v: len(g_copy.out_neighbours[v]) for v in g_copy.out_neighbours}

        # Select the vertex with the highest degree
        u = max(degrees, key=degrees.get)
        cover.add(u)  # Add it to the cover

        # Remove all edges incident to this vertex
        incident_edges = list(g_copy.edges.items())
        for eid, (x, y, _) in incident_edges:
            if x == u or y == u:
                g_copy.remove_edge(x, y)
                if eid in g_copy.edges:
                    del g_copy.edges[eid]
                    g_copy.edge_count -= 1  # Keep edge count in sync

    return cover

def edge_density_vertex_cover(graph: Graph):
    """
    Heuristic approach: pick vertices covering the most uncovered edges.
    Similar to the high-degree method, but recalculates "edge frequency"
    for all vertices based on current uncovered edges.
    """
    g_copy = graph.deepcopy()  # Work on a copy
    cover = set()

    # Loop until no edges are left
    while g_copy.edge_count > 0:
        freq = {}  # Frequency map: vertex -> number of incident uncovered edges

        # Count how many uncovered edges each vertex is involved in
        for _, (u, v, _) in g_copy.edges.items():
            freq[u] = freq.get(u, 0) + 1
            freq[v] = freq.get(v, 0) + 1

        # Pick the vertex that appears most often (covers the most uncovered edges)
        best = max(freq, key=freq.get)
        cover.add(best)  # Add it to the cover

        # Remove all incident edges from the graph
        incident_edges = list(g_copy.edges.items())
        for eid, (x, y, _) in incident_edges:
            if x == best or y == best:
                g_copy.remove_edge(x, y)
                if eid in g_copy.edges:
                    del g_copy.edges[eid]
                    g_copy.edge_count -= 1

    return cover


def hybrid_greedy_matching_vertex_cover(graph: Graph):
    """
    Hybrid approach: Combines greedy matching with vertex cover.
    Selects non-visited vertex pairs and adds both endpoints to the cover.
    """
    g_copy = graph.deepcopy()
    cover = set()      # Set of vertices in the cover
    visited = set()    # Set of already selected (covered) vertices

    # Iterate through each vertex
    for u in g_copy.out_neighbours:
        if u in visited:
            continue  # Skip if already covered

        # Try to match u with an uncovered neighbor v
        for v, _ in g_copy.out_neighbours[u]:
            if v in visited:
                continue

            # Add both u and v to the vertex cover
            cover.add(u)
            cover.add(v)
            visited.add(u)
            visited.add(v)

            # Remove


if __name__ == "__main__":
    # Test on multiple graphs
    g = Graph("graph.txt")
    print("\nHigh-Degree Heuristic:", high_degree_vertex_cover(g))
    print("Edge Density Heuristic:", edge_density_vertex_cover(g))
    print("Hybrid Greedy-Matching:", hybrid_greedy_matching_vertex_cover(g))

    g25 = Graph("graph25.txt")
    print("\n[graph25] High-Degree Heuristic:", high_degree_vertex_cover(g25))
    print("[graph25] Edge Density Heuristic:", edge_density_vertex_cover(g25))
    print("[graph25] Hybrid Greedy-Matching:", hybrid_greedy_matching_vertex_cover(g25))

    g10 = Graph("graph10.txt")
    print("\n[graph10] High-Degree Heuristic:", high_degree_vertex_cover(g10))
    print("[graph10] Edge Density Heuristic:", edge_density_vertex_cover(g10))
    print("[graph10] Hybrid Greedy-Matching:", hybrid_greedy_matching_vertex_cover(g10))