#include <iostream>
#include "graph_processor.h"

int main() {
    std::string expression = "A*(B+C)+D*E";
    
    Graph gNmos, gPmos;
    std::vector<std::string> eulerPathNmos, eulerPathPmos;
    std::vector<std::string> sourceNodesNmos, outNodesNmos;
    std::vector<std::string> sourceNodesPmos, outNodesPmos;
    
    ExpressionProcessor processor;
    processor.processExpression(expression, gNmos, gPmos, 
                              eulerPathNmos, eulerPathPmos,
                              sourceNodesNmos, outNodesNmos,
                              sourceNodesPmos, outNodesPmos);
    
    // Print results
    std::cout << "NMOS Euler Path: ";
    for (const auto& node : eulerPathNmos) {
        std::cout << node << " ";
    }
    std::cout << std::endl;
    
    std::cout << "PMOS Euler Path: ";
    for (const auto& node : eulerPathPmos) {
        std::cout << node << " ";
    }
    std::cout << std::endl;
    
    return 0;
}
