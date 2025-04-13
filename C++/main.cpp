// main.cpp
#include <iostream>
#include <string>
#include "logic_parser.h"
#include "graph_builder.h"
#include "euler_path.h"
#include "export_data.h"

int main() {
    std::string expression;
    std::cout << "Enter logic expression (e.g. A*(B+C)+D*E): ";
    std::getline(std::cin, expression);

    // Parse expression into postfix form
    std::vector<std::string> postfix = to_postfix(expression);

    // Build NMOS graph
    Graph g_nmos;
    std::string nmos_end_node;
    build_graph_nmos(g_nmos, postfix, nmos_end_node);

    // Find Euler path for NMOS
    std::vector<std::string> euler_nmos = find_hamiltonian_path(g_nmos, nmos_end_node);

    // Build PMOS graph using inverted expression
    Graph g_pmos;
    std::vector<std::string> postfix_inv = to_postfix_inv(expression);
    std::vector<std::string> euler_pmos = build_graph_pmos(g_pmos, postfix_inv, euler_nmos);

    // Find source/output nodes
    std::vector<std::string> src_nmos, out_nmos, src_pmos, out_pmos;
    find_io_nodes(g_nmos, src_nmos, out_nmos);
    find_io_nodes(g_pmos, src_pmos, out_pmos);

    // Export to JSON
    export_to_json("output_data.json", g_nmos, g_pmos, euler_nmos, euler_pmos, src_nmos, out_nmos, src_pmos, out_pmos);

    std::cout << "Done. Data exported to output_data.json" << std::endl;
    return 0;
}