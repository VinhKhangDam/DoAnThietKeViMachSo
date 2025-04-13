#pragma once
#include <map>
#include <set>
#include <vector>
#include <string>

struct Graph {
    std::set<std::string> nodes;
    std::map<std::string, std::set<std::string>> adj;
};

void build_graph_nmos(Graph& g, const std::vector<std::string>& postfix, std::string& end_node);
std::vector<std::string> build_graph_pmos(Graph& g, const std::vector<std::string>& postfix_inv, const std::vector<std::string>& nmos_path);
void find_io_nodes(const Graph& g, std::vector<std::string>& sources, std::vector<std::string>& outputs);