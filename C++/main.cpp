#include <iostream>
#include <fstream>
#include "ExpressionParser.h"
#include "Graph.h"

void writeOutputToFile(const Graph& g_nmos, const Graph& g_pmos,
                      const std::vector<std::string>& euler_path_nmos,
                      const std::vector<std::string>& euler_path_pmos,
                      const std::vector<std::string>& source_nodes_nmos,
                      const std::vector<std::string>& out_nodes_nmos,
                      const std::vector<std::string>& source_nodes_pmos,
                      const std::vector<std::string>& out_nodes_pmos) {
    std::ofstream outFile("output.json");
    outFile << "{\n";
    
    // Write all the data to the JSON file
    // Example for g_nmos edges:
    outFile << "\"g_nmos_edges\": [";
    for (const auto& edge : g_nmos.getEdges()) {
        outFile << "[\"" << edge.first << "\", \"" << edge.second << "\"],";
    }
    outFile << "],\n";
    
    // Similar for other data...
    
    outFile << "}\n";
    outFile.close();
}

int main() {
    std::string expression;
    std::cout << "Enter expression: ";
    std::getline(std::cin, expression);
    
    auto [g_nmos, g_pmos] = ExpressionParser::createGraphs(expression);
    auto euler_path_nmos = ExpressionParser::findEulerPath(g_nmos);
    auto euler_path_pmos = ExpressionParser::findEulerPath(g_pmos);
    auto source_nodes_nmos = ExpressionParser::findSourceNodes(g_nmos);
    auto out_nodes_nmos = ExpressionParser::findOutputNodes(g_nmos);
    auto source_nodes_pmos = ExpressionParser::findSourceNodes(g_pmos);
    auto out_nodes_pmos = ExpressionParser::findOutputNodes(g_pmos);
    
    writeOutputToFile(g_nmos, g_pmos, euler_path_nmos, euler_path_pmos,
                    source_nodes_nmos, out_nodes_nmos, source_nodes_pmos, out_nodes_pmos);
    
    return 0;
}