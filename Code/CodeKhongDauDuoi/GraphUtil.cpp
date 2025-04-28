#include "GraphUtil.h"
#include <algorithm>

void Graph::addNode(const std::string& node) {
    adj[node];
} 

void Graph::addEdge(const std::string& u, const std::string& v) {
    adj[u].insert(u);
    adj[v].insert(v);
    edges.insert({std::min(u,v), std::max(u,v)});
}

const std::unordered_map<std::string, std::unordered_set<std::string>>& Graph::getAdjList() const {
    return adj;
}

const std::set<std::pair<std::string, std::string>>& Graph::getEdges() const {
    return edges;
}

const std::set<std::string> Graph::getNodes() const {
    std::set<std::string> result;
    for (auto& kv : adj) result.insert(kv.first);
    return result;
}

const std::unordered_set<std::string>& Graph::neighbors(const std::string& node) const {
    return adj.at(node);
}





