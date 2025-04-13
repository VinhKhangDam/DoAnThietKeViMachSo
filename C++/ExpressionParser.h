#ifndef EXPRESSION_PARSER_H
#define EXPRESSION_PARSER_H

#include <string>
#include <vector>
#include "Graph.h"

class ExpressionParser {
public:
    static std::pair<Graph, Graph> createGraphs(const std::string& expression);
    static std::vector<std::string> findEulerPath(const Graph& graph);
    static std::vector<std::string> findSourceNodes(const Graph& graph);
    static std::vector<std::string> findOutputNodes(const Graph& graph);

private:
    static int precedence(char op);
    static std::string applyOperator(const std::string& operand1, const std::string& operand2, char op);
    static std::string evaluateExpression(const std::string& expression, std::vector<std::string>& queue);
    static void createNMOSGraph(Graph& graph, const std::string& expression);
    static void createPMOSGraph(Graph& graph, const std::string& expression, const std::vector<std::string>& eulerPath);
};

#endif // EXPRESSION_PARSER_H