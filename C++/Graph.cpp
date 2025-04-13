#include "Graph.h"
#include <algorithm>

void Graph::addNode(const std::string& node) {
    if (!hasNode(node)) {
        nodes.push_back(node);
        adjacencyList[node] = std::set<std::string>();
    }
}

void Graph::addEdge(const std::string& node1, const std::string& node2) {
    if (!hasEdge(node1, node2)) {
        edges.emplace_back(node1, node2);
        adjacencyList[node1].insert(node2);
        adjacencyList[node2].insert(node1);
    }
}

const std::vector<std::string>& Graph::getNodes() const {
    return nodes;
}

const std::vector<std::pair<std::string, std::string>>& Graph::getEdges() const {
    return edges;
}

std::vector<std::string> Graph::getNeighbors(const std::string& node) const {
    std::vector<std::string> neighbors;
    if (adjacencyList.find(node) != adjacencyList.end()) {
        neighbors.assign(adjacencyList.at(node).begin(), adjacencyList.at(node).end());
    }
    return neighbors;
}

bool Graph::hasNode(const std::string& node) const {
    return std::find(nodes.begin(), nodes.end(), node) != nodes.end();
}

bool Graph::hasEdge(const std::string& node1, const std::string& node2) const {
    return std::find(edges.begin(), edges.end(), std::make_pair(node1, node2)) != edges.end() ||
           std::find(edges.begin(), edges.end(), std::make_pair(node2, node1)) != edges.end();
}

int Graph::degree(const std::string& node) const {
    return adjacencyList.at(node).size();
}