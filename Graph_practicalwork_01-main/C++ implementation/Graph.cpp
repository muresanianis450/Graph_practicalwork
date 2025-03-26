#include <iostream>
#include <vector>
#include <unordered_map>
#include <fstream>
#include <string>
#include <sstream>
#include <cstdlib>
#include <algorithm>


using namespace std;

class Graph {
private:
    unordered_map<int, vector<pair<int, int>>> out_neighbours; // Adjacency list (with weights)
    unordered_map<int, tuple<int, int, int>> edges;  // Edge ID -> (source, target, weight)
    int edge_count;

public:
    Graph(const string& filename = "") {
        edge_count = 0;
        if (filename.empty()) {
            return;
        }
        _read_from_file(filename);
    }

    Graph deepcopy() const {
        Graph copy;
        copy.edge_count = this->edge_count;
        copy.out_neighbours = this->out_neighbours;
        copy.edges = this->edges;
        return copy;
    }

    void _read_from_file(const string& file_name) {
        ifstream file(file_name);
        if (!file.is_open()) {
            cerr << "Error: Could not open file " << file_name << endl;
            return;
        }

        int x, y;
        file >> x >> y;  // Read number of vertices and edges

        // Initialize the graph with 'x' vertices
        for (int i = 0; i < x; ++i) {
            out_neighbours[i] = {};
        }

        // Read the edges with weights and add them to the graph
        int u, v, w;
        while (file >> u >> v >> w) {
            add_edge(u, v, w);
        }

        file.close();
    }

    bool add_edge(int x, int y, int weight) {
        auto it = find_if(out_neighbours[x].begin(), out_neighbours[x].end(),
                          [y, weight](const pair<int, int>& p) { return p.first == y && p.second == weight; });
        if (it == out_neighbours[x].end()) {
            out_neighbours[x].push_back(make_pair(y, weight));
            edges[edge_count] = make_tuple(x, y, weight);
            edge_count++;
            return true;
        }
        return false;
    }

    bool remove_edge(int x, int y) {
        auto& neighbours = out_neighbours[x];
        for (auto it = neighbours.begin(); it != neighbours.end(); ++it) {
            if (it->first == y) {
                neighbours.erase(it);
                return true;
            }
        }
        return false;
    }

    bool remove_vertex(int x) {
        if (out_neighbours.find(x) != out_neighbours.end()) {
            out_neighbours.erase(x);
            return true;
        }
        return false;
    }

    bool add_vertex(int x) {
        if (out_neighbours.find(x) == out_neighbours.end()) {
            out_neighbours[x] = {};
            return true;
        }
        return false;
    }

    tuple<int, int, int> get_edge_by_id(int edge_id) {
        if (edges.find(edge_id) != edges.end()) {
            return edges[edge_id];
        }
        return make_tuple(-1, -1, -1);  // Return an invalid edge if not found
    }

    vector<pair<int, int>> parse_out(int x) {
        return out_neighbours[x];
    }

    int get_number_vertices() {
        return out_neighbours.size();
    }

    vector<int> parse_vertices() {
        vector<int> vertices;
        for (auto& entry : out_neighbours) {
            vertices.push_back(entry.first);
        }
        return vertices;
    }

    static Graph read_from_file(const string& file_name) {
        Graph graph(file_name);
        return graph;
    }

    bool is_edge(int x, int y) {
        for (int edge_id = 0; edge_id < edge_count; ++edge_id) {
            int source, target, _weight;
            tie(source, target, _weight) = edges[edge_id];
            if (source == x && target == y) {
                return true;
            }
        }
        return false;
    }

    void generate_random_graph(int number_vertices, int number_edges) {
        for (int i = 0; i < number_edges; ++i) {
            int x = rand() % number_vertices;
            int y = rand() % number_vertices;
            int weight = rand() % 100 + 1;  // Random weight between 1 and 100
            if (x != y && !is_edge(x, y)) {
                add_edge(x, y, weight);
            }
        }
    }

    int get_edge_count() const {
        return edge_count;
    }

    friend void write_to_file(Graph& graph, const string& file_name);
};

void write_to_file(Graph& graph, const string& file_name) {
    ofstream file(file_name);
    file << graph.get_number_vertices() << " " << graph.edges.size() << endl;
    for (int edge_id = 0; edge_id < graph.edges.size(); ++edge_id) {
        int source, target, weight;
        tie(source, target, weight) = graph.get_edge_by_id(edge_id);
        file << source << " " << target << " " << weight << endl;
    }
}

class GraphUI {
private:
    Graph graph;
    Graph copied_graph;
public:
    GraphUI(const string& filename = "graph.txt") : graph(filename) {}

    void copy_graph_ui() {
        copied_graph = graph.deepcopy();
        cout << "Graph copied successfully." << endl;
    }
    void show_copied_graph() {
        cout << "\nCopied Graph:" << endl;
        cout << "Vertices: ";
        vector<int> vertices = copied_graph.parse_vertices();
        for (int vertex : vertices) {
            cout << vertex << " ";
        }
        cout << endl;
        for (int edge_id = 0; edge_id < copied_graph.get_edge_count(); ++edge_id) {
            int source, target, weight;
            tie(source, target, weight) = copied_graph.get_edge_by_id(edge_id);
            cout << "Edge " << edge_id << ": " << source << " -> " << target << " (Weight: " << weight << ")" << endl;
        }
    }
    void load_graph_from_file_ui() {
        string file_name;
        cout << "Enter file name to load the graph: ";
        cin >> file_name;
        graph = Graph::read_from_file(file_name);
        cout << "Graph loaded from " << file_name << endl;
    }

    void save_graph_to_file_ui() {
        string file_name;
        cout << "Enter file name to save the graph: ";
        cin >> file_name;
        write_to_file(graph, file_name);
        cout << "Graph saved to " << file_name << endl;
    }

    void show_graph() {
        cout << "\nGraph:" << endl;
        cout << "Vertices: ";
        vector<int> vertices = graph.parse_vertices();
        for (int vertex : vertices) {
            cout << vertex << " ";
        }
        cout << endl;
        for (int edge_id = 0; edge_id < graph.get_edge_count(); ++edge_id) {
            int source, target, weight;
            tie(source, target, weight) = graph.get_edge_by_id(edge_id);
            cout << "Edge " << edge_id << ": " << source << " -> " << target << " (Weight: " << weight << ")" << endl;
        }
    }

    void display_menu() {
        cout << "\nGraph Menu:" << endl;
        cout << "1. Show Graph" << endl;
        cout << "2. Add Vertex" << endl;
        cout << "3. Remove Vertex" << endl;
        cout << "4. Add Edge" << endl;
        cout << "5. Remove Edge" << endl;
        cout << "6. Check if an Edge Exists" << endl;
        cout << "7. Show All Vertices" << endl;
        cout << "8. Show Outbound Edges of a Vertex" << endl;
        cout << "9. Save Graph to File" << endl;
        cout << "10. Load Graph from File" << endl;
        cout << "11. Generate Random Graph" << endl;
        cout << "12. Exit" << endl;
        cout << "13. Copy Graph" << endl;
        cout << "14. Show Copied Graph" << endl;
    }

    void handle_menu_option(int option) {
        switch (option) {
            case 1:
                show_graph();
                break;
            case 2:
                add_vertex_ui();
                break;
            case 3:
                remove_vertex_ui();
                break;
            case 4:
                add_edge_ui();
                break;
            case 5:
                remove_edge_ui();
                break;
            case 6:
                check_edge_ui();
                break;
            case 7:
                show_vertices();
                break;
            case 8:
                show_outbound_edges_ui();
                break;
            case 9:
                save_graph_to_file_ui();
                break;
            case 10:
                load_graph_from_file_ui();
                break;
            case 11:
                generate_random_graph_ui();
                break;
            case 12:
                cout << "Exiting..." << endl;
                exit(0);
            case 13:
                copy_graph_ui();
            case 14:
                show_copied_graph();
                break;
            default:
                cout << "Invalid option. Please try again." << endl;
        }
    }

    void add_vertex_ui() {
        int vertex;
        cout << "Enter vertex to add: ";
        cin >> vertex;
        if (graph.add_vertex(vertex)) {
            cout << "Vertex " << vertex << " added." << endl;
        } else {
            cout << "Vertex already exists." << endl;
        }
    }

    void remove_vertex_ui() {
        int vertex;
        cout << "Enter vertex to remove: ";
        cin >> vertex;
        if (graph.remove_vertex(vertex)) {
            cout << "Vertex " << vertex << " removed." << endl;
        } else {
            cout << "Vertex does not exist." << endl;
        }
    }

    void add_edge_ui() {
        int x, y, weight;
        cout << "Enter source vertex: ";
        cin >> x;
        cout << "Enter target vertex: ";
        cin >> y;
        cout << "Enter weight of the edge: ";
        cin >> weight;
        if (graph.add_edge(x, y, weight)) {
            cout << "Edge " << x << " -> " << y << " with weight " << weight << " added." << endl;
        } else {
            cout << "Edge " << x << " -> " << y << " already exists." << endl;
        }
    }

    void remove_edge_ui() {
        int x, y;
        cout << "Enter source vertex: ";
        cin >> x;
        cout << "Enter target vertex: ";
        cin >> y;
        if (graph.remove_edge(x, y)) {
            cout << "Edge " << x << " -> " << y << " removed." << endl;
        } else {
            cout << "Edge does not exist." << endl;
        }
    }

    void check_edge_ui() {
        int x, y;
        cout << "Enter source vertex: ";
        cin >> x;
        cout << "Enter target vertex: ";
        cin >> y;
        if (graph.is_edge(x, y)) {
            cout << "Edge " << x << " -> " << y << " exists." << endl;
        } else {
            cout << "Edge does not exist." << endl;
        }
    }

    void show_vertices() {
        cout << "\nVertices: ";
        vector<int> vertices = graph.parse_vertices();
        for (int vertex : vertices) {
            cout << vertex << " ";
        }
        cout << endl;
    }

    void show_outbound_edges_ui() {
        int vertex;
        cout << "Enter vertex to show outbound edges: ";
        cin >> vertex;
        vector<pair<int, int>> edges = graph.parse_out(vertex);
        cout << "Outbound edges for vertex " << vertex << ":" << endl;
        for (const auto& edge : edges) {
            cout << "Target: " << edge.first << ", Weight: " << edge.second << endl;
        }
    }

    void generate_random_graph_ui() {
        int number_vertices, number_edges;
        cout << "Enter number of vertices: ";
        cin >> number_vertices;
        cout << "Enter number of edges: ";
        cin >> number_edges;
        graph.generate_random_graph(number_vertices, number_edges);
        cout << "Random graph generated with " << number_vertices << " vertices and " << number_edges << " edges." << endl;
    }

    void run() {
        while (true) {
            display_menu();
            int option;
            cout << "Enter option: ";
            cin >> option;
            handle_menu_option(option);
        }
    }
};

int main() {
    GraphUI ui("graph.txt");  // Initialize UI with graph from "graph.txt"
    ui.run();  // Start the console-based menu system
    return 0;
}