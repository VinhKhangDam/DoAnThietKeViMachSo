#include "/Project/graph_processor.h"
#include <algorithm>
#include <stack>
#include <queue>
#include <climits>

void Graph::addNode(const std::string& node) {
    nodes.insert(node);
    degrees[node] = 0;
}

void Graph::addEdge(const std::string& node1, const std::string& node2) {
    if (nodes.find(node1) == nodes.end()) addNode(node1);
    if (nodes.find(node2) == nodes.end()) addNode(node2);
    
    edges.insert({node1, node2});
    edges.insert({node2, node1});
    degrees[node1]++;
    degrees[node2]++;
}

bool Graph::hasEdge(const std::string& node1, const std::string& node2) const {
    return edges.find({node1, node2}) != edges.end();
}

void Graph::removeEdge(const std::string& node1, const std::string& node2) {
    edges.erase({node1, node2});
    edges.erase({node2, node1});
    degrees[node1]--;
    degrees[node2]--;
}

int Graph::degree(const std::string& node) const {
    auto it = degrees.find(node);
    return it != degrees.end() ? it->second : 0;
}

std::set<std::string> Graph::getNodes() const {
    return nodes;
}

std::set<std::string> Graph::getNeighbors(const std::string& node) const {
    std::set<std::string> neighbors;
    for (const auto& edge : edges) {
        if (edge.first == node) {
            neighbors.insert(edge.second);
        }
    }
    return neighbors;
}

std::set<std::pair<std::string, std::string>> Graph::getEdges() const {
    return edges;
}

int ExpressionProcessor::precedence(const std::string& op) const {
    if (op == "+") return 1;
    if (op == "*") return 2;
    return 0;
}

std::string ExpressionProcessor::applyOperator(const std::string& operand1, const std::string& operand2, const std::string& op) const {
    if (op == "+") return operand1 + "+" + operand2;
    return operand1 + "*" + operand2;
}

std::string ExpressionProcessor::applyOperatorInv(const std::string& operand1, const std::string& operand2, const std::string& op) const {
    if (op == "+") return operand1 + "*" + operand2;
    return operand1 + "+" + operand2;
}

std::string ExpressionProcessor::evaluateExpression(const std::string& expression, std::vector<std::string>& q) const {
    std::stack<std::string> operandStack;
    std::stack<std::string> operatorStack;
    size_t index = 0;

    while (index < expression.length()) {
        std::string token(1, expression[index]);
        
        if (isalpha(expression[index])) {
            operandStack.push(token);
            index++;
        }
        else if (token == "+" || token == "*") {
            while (!operatorStack.empty() && precedence(operatorStack.top()) >= precedence(token)) {
                std::string op = operatorStack.top();
                operatorStack.pop();
                std::string operand2 = operandStack.top();
                operandStack.pop();
                std::string operand1 = operandStack.top();
                operandStack.pop();
                std::string result = applyOperator(operand1, operand2, op);
                q.push_back(result);
                operandStack.push(result);
            }
            operatorStack.push(token);
            index++;
        }
        else if (token == "(") {
            operatorStack.push(token);
            index++;
        }
        else if (token == ")") {
            while (!operatorStack.empty() && operatorStack.top() != "(") {
                std::string op = operatorStack.top();
                operatorStack.pop();
                std::string operand2 = operandStack.top();
                operandStack.pop();
                std::string operand1 = operandStack.top();
                operandStack.pop();
                std::string result = applyOperator(operand1, operand2, op);
                q.push_back(result);
                operandStack.push(result);
            }
            if (!operatorStack.empty()) operatorStack.pop();
            index++;
        }
        else {
            index++;
        }
    }

    while (!operatorStack.empty()) {
        std::string op = operatorStack.top();
        operatorStack.pop();
        std::string operand2 = operandStack.top();
        operandStack.pop();
        std::string operand1 = operandStack.top();
        operandStack.pop();
        std::string result = applyOperator(operand1, operand2, op);
        q.push_back(result);
        operandStack.push(result);
    }

    return operandStack.empty() ? "" : operandStack.top();
}

std::string ExpressionProcessor::evaluateExpressionInv(const std::string& expression, std::vector<std::string>& q) const {
    // Similar to evaluateExpression but using applyOperatorInv
    // Implementation omitted for brevity
    return "";
}

std::string ExpressionProcessor::subtractExpressions(const std::string& expr1, const std::string& expr2) const {
    size_t i = 0, j = 0;
    std::string result;
    
    while (i < expr1.length()) {
        if (j < expr2.length() && expr1[i] == expr2[j]) {
            i++;
            j++;
        }
        else {
            result += expr1[i];
            i++;
        }
    }
    
    return result;
}

std::string ExpressionProcessor::intersectionExpressions(const std::string& expr1, const std::string& expr2) const {
    size_t i = 0, j = 0;
    std::string result;
    
    while (i < expr1.length() && j < expr2.length()) {
        if (expr1[i] == expr2[j]) {
            result += expr1[i];
            i++;
            j++;
        }
        else {
            i++;
        }
    }
    
    return result;
}

void ExpressionProcessor::createNMOS(Graph& g, const std::string& expression, std::string& endNode, 
                                   std::vector<std::string>& eulerPathNmos,
                                   std::vector<std::string>& sourceNodes, 
                                   std::vector<std::string>& outNodes) const {
    // Implementation of NMOS graph creation
    // Similar to Python version but using C++ data structures
}

void ExpressionProcessor::createPMOS(Graph& g, const std::string& expression, 
                                   const std::vector<std::string>& eulerPathNmos,
                                   std::vector<std::string>& eulerPathPmos,
                                   std::vector<std::string>& sourceNodes, 
                                   std::vector<std::string>& outNodes) const {
    // Implementation of PMOS graph creation
    // Similar to Python version but using C++ data structures
}

void ExpressionProcessor::processExpression(const std::string& expression, Graph& gNmos, Graph& gPmos,
                                         std::vector<std::string>& eulerPathNmos, 
                                         std::vector<std::string>& eulerPathPmos,
                                         std::vector<std::string>& sourceNodesNmos, 
                                         std::vector<std::string>& outNodesNmos,
                                         std::vector<std::string>& sourceNodesPmos, 
                                         std::vector<std::string>& outNodesPmos) const {
    createNMOS(gNmos, expression, eulerPathNmos.back(), eulerPathNmos, sourceNodesNmos, outNodesNmos);
    createPMOS(gPmos, expression, eulerPathNmos, eulerPathPmos, sourceNodesPmos, outNodesPmos);
}
