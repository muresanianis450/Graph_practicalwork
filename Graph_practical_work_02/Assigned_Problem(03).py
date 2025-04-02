from Graph_practical_work_02.graph import Graph

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

# Example usage
g = Graph(7)
g.add_edge(0,1,1)
g.add_edge(1,2,1)
g.add_edge(3,4,1)
g.add_edge(4,5,1)


components = find_conected_components(g)
print("Connected components:", components)