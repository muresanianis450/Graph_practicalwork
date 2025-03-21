#ifndef GRAPH_H
#define GRAPH_H

#include <vector>
#include <unordered_map>
#include <tuple>
#include <string>

using namespace std;

class Graph {
private:
    unordered_map<int, vector<pair<int, int>>> out_neighbours; // Adjacency list (with weights)
    unordered_map<int, tuple<int, int, int>> edges;  // Edge ID -> (source, target, weight)
    int edge_count;

public:
    Graph(const string& filename = "");

    void _read_from_file(const string& file_name);

    bool add_edge(int x, int y, int weight);

    bool remove_edge(int x, int y);

    bool remove_vertex(int x);

    bool add_vertex(int x);

    tuple<int, int, int> get_edge_by_id(int edge_id);

    vector<pair<int, int>> parse_out(int x);

    int get_number_vertices();

    vector<int> parse_vertices();

    static Graph read_from_file(const string& file_name);

    bool is_edge(int x, int y);

    void generate_random_graph(int number_vertices, int number_edges);

    int get_edge_count() const;

    friend void write_to_file(Graph& graph, const string& file_name);
};

#endif // GRAPH_H