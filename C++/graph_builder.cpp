// graph_builder.cpp
#include "graph_builder.h"
#include <stack>
#include <algorithm>

void add_edge(Graph& g, const std::string& a, const std::string& b) {
    g.nodes.insert(a);
    g.nodes.insert(b);
    g.adj[a].insert(b);
    g.adj[b].insert(a);
}

void build_graph_nmos(Graph& g, const std::vector<std::string>& postfix, std::string& end_node) {
    std::stack<std::string> stk;
    for (const std::string& token : postfix) {
        if (token == "+" || token == "*") {
            std::string op2 = stk.top(); stk.pop();
            std::string op1 = stk.top(); stk.pop();
            
            if (token == "*") {  // Series connection
                std::string new_node = op1 + "_" + op2;
                add_edge(g, op1 + "D", op2 + "S");
                stk.push(new_node);
                end_node = op2 + "D";
            } 
            else {  // Parallel connection
                add_edge(g, op1 + "S", op2 + "S");
                add_edge(g, op1 + "D", op2 + "D");
                stk.push(op1 + op2);
            }
        } 
        else {  // Single transistor
            add_edge(g, token + "S", token + "D");
            stk.push(token);
        }
    }
}
std::vector<std::string> build_graph_pmos(Graph& g, const std::vector<std::string>& postfix_inv, const std::vector<std::string>& nmos_path) {
    std::vector<std::string> euler_pmos(nmos_path.size());
    for (size_t i = 0; i < nmos_path.size(); ++i) {
        euler_pmos[i] = nmos_path[i];
    }
    for (const std::string& token : postfix_inv) {
        if (token != "+" && token != "*") {
            add_edge(g, token + "S", token + "D");
        }
    }
    for (size_t i = 1; i < euler_pmos.size(); ++i) {
        add_edge(g, euler_pmos[i-1], euler_pmos[i]);
    }
    return euler_pmos;
}

void find_io_nodes(const Graph& g, std::vector<std::string>& sources, std::vector<std::string>& outputs) {
    for (const auto& node : g.nodes) {
        if (g.adj.at(node).size() == 1) {
            if (node.back() == 'S') sources.push_back(node);
            else if (node.back() == 'D') outputs.push_back(node);
        }
    }
}

