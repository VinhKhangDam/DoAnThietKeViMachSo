//=========================================
// GraphUtil.h : xu li do thi (node, edge)
//========================================

#pragma once
#ifndef GRAPH_UNTIL
#define GRAPH_UNTIL
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <string>

class Graph {
    public:
        void addNode (const std::string& node);
        void addEdge (const std::string&u, const std::string&v);
        const std::unordered_map<std::string, std::unordered_set<std::string>>& getAdjList() const;
        const std::set<std::pair<std::string, std::string>>& getEdges() const;
        const std::set<std::string> getNodes() const;
        const std::unordered_set<std::string>& neighbors(const std::string& node) const;

    private:
        std::unordered_map<std::string, std::unordered_set<std::string>> adj;
        std::set<std::pair<std::string, std::string>> edges;
};

#endif