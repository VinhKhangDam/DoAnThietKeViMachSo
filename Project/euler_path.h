#ifdef EULER_PATH
#define EULER_PATH

#include <vector>
#include <string>
#include <map>
#include <set>
#include <utility>

class Graph{
private:
    std::set<std::string> nodes;
    std::set<std::pair<std::string, std::string>> edges;
    std::map<std::string, int> degrees;

public:
    void addNode(const std::string& node);
    void addEdge(const std::string& node1, const std::string& node2);
    bool hasEdge(const std::string& node1, const std::string& node2) const;
    void removeEdge(const std::string& node1, const std::string& node2);
    int degree(const std::string& node) const;
    std::set<std::string> getNode() const;
    std::set<std::string> getNeighbors(const std::string& node) const;
    std::set<std::pair<std::string, std::string>> getEdges() const;
};

class ExpressionProcessor {
private:
    int precedence(const std::string& op) const;
    std::string applyOperator(const std::string& operand1, const std::string& operand2, const std::string& op) const;
    std::string applyOperatorInv(const std::string& operand1, const std::string& operand2, const std::string& op) const;
    std::string evaluateExpression(const std::string& expression, std::vector<std::string>& q) const;
    std::string evaluateExpressionInv(const std::string& expression, std::vector<std::string>& q) const;
    std::string subtractExpressions(const std::string& expr1, const std::string& expr2) const;
    std::string intersectionExpressions(const std::string& expr1, const std::string& expr2) const;

public:
    void createNMOS(Graph& g, const std::string& expression, std::string& endNode, std::vector<std::string>& eulerPathNmos,
    std::vector<std::string>& sourceNodes, std::vector<std::string>& outNodes) const;
    void createPMOS(Graph& g, const std::string& expression, const std::vector<std::string>& eulerPathNmos,
    std::vector<std::string>& eulerPathPmos, std::vector<std::string>& sourceNodes, std::vector<std::string>& outNodes) const;
    void processExpression(const std::string& expression, Graph& gNmos, Graph& gPmos,
    std::vector<std::string>& eulerPathNmos, std::vector<std::string>& eulerPathPmos,
    std::vector<std::string>& sourceNodesNmos, std::vector<std::string>& outNodesNmos,
    std::vector<std::string>& sourceNodesPmos, std::vector<std::string>& outNodesPmos) const;
};
#endif // EULER_PATH

