#include "euler_path.h"
#include <unordered_set>

bool is_valid_next(const std::string& v, const std::vector<std::string>& path, const Graph& g) {
    if (std::find(path.begin(), path.end(), v) != path.end()) return false;
    if (!path.empty() && g.adj.at(path.back()).count(v) == 0) return false;
    return true;
}

bool dfs(const Graph& g, const std::string& curr, const std::string& end, std::vector<std::string>& path) {
    path.push_back(curr);
    if (path.size() == g.nodes.size()) return true;
    for (const std::string& neighbor : g.adj.at(curr)) {
        if (is_valid_next(neighbor, path, g)) {
            if (dfs(g, neighbor, end, path)) return true;
        }
    }
    path.pop_back();
    return false;
}

std::vector<std::string> find_hamiltonian_path(const Graph& g, const std::string& end_node) {
    if (g.nodes.empty()) return {};

    // Tìm node bắt đầu (node có chứa 'S' và degree lẻ)
    std::string start_node;
    for (const auto& node : g.nodes) {
        if (node.find('S') != std::string::npos && g.adj.at(node).size() % 2 != 0) {
            start_node = node;
            break;
        }
    }
    if (start_node.empty()) start_node = *g.nodes.begin();

    std::vector<std::string> path;
    if (dfs(g, start_node, end_node, path)) {
        return path;
    }
    return {};
}