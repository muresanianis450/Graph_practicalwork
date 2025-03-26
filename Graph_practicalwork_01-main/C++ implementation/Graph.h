#ifndef GRAPH_H
#define GRAPH_H

#include <iostream>
#include <vector>
#include <unordered_map>
#include <fstream>
#include <cstdlib>
#include <ctime>

class Graph {
private:
    std::unordered_map<int, std::vector<std::pair<int, int>>> out_neighbours;
    std::unordered_map<int, std::tuple<int, int, int>> edges;
    int edge_count;

    void readFromFile(const std::string& filename);

public:
    Graph(const std::string& filename);
    Graph(int vertices);

    bool addEdge(int x, int y, int weight);
    bool removeEdge(int x, int y);
    bool removeVertex(int x);
    void addVertex(int x);

    std::tuple<int, int, int> getEdgeById(int edgeId) const;
    std::vector<std::pair<int, int>> parseOut(int x) const;

    int getNumberVertices() const;
    std::vector<int> parseVertices() const;

    static Graph readFromFileStatic(const std::string& filename);

    int isEdge(int x, int y) const;
    void generateRandomGraph(int numberVertices, int numberEdges);
    Graph deepcopy() const;

    void displayGraph() const;
    void writeToFile(const std::string& filename) const;
};

#endif // GRAPH_H
