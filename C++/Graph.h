#ifndef GRAPH_H
#define GRAPH_H

#include <vector>
#include <string>
#include <map>
#include <set>

class Graph {
public:
    void addNode(const std::string& node);
    void addEdge(const std::string& node1, const std::string& node2);
    const std::vector<std::string>& getNodes() const;
    const std::vector<std::pair<std::string, std::string>>& getEdges() const;
    std::vector<std::string> getNeighbors(const std::string& node) const;
    bool hasNode(const std::string& node) const;
    bool hasEdge(const std::string& node1, const std::string& node2) const;
    int degree(const std::string& node) const;

private:
    std::vector<std::string> nodes;
    std::vector<std::pair<std::string, std::string>> edges;
    std::map<std::string, std::set<std::string>> adjacencyList;
};

#endif // GRAPH_H