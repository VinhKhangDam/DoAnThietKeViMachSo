#include "ExpressionParser.h"
#include <stack>
#include <algorithm>
#include <stdexcept>

using namespace std;

// Hàm xác định độ ưu tiên của toán tử
int ExpressionParser::precedence(char op) {
    if (op == '+') return 1;
    else if (op == '*') return 2;
    else return 0;
}

// Hàm áp dụng toán tử cho hai toán hạng
string ExpressionParser::applyOperator(const string& a, const string& b, char op) {
    if (op == '+') return a + "+" + b;
    else return a + "*" + b;
}

// Hàm chuyển đổi biểu thức sang dạng chuỗi kết quả (tương tự Python)
string ExpressionParser::evaluateExpression(const string& expr, vector<string>& queue) {
    stack<string> operands;
    stack<char> operators;

    for (size_t i = 0; i < expr.size(); ++i) {
        char c = expr[i];
        if (isalpha(c)) {
            operands.push(string(1, c));
        } else if (c == '(') {
            operators.push(c);
        } else if (c == ')') {
            while (!operators.empty() && operators.top() != '(') {
                string b = operands.top(); operands.pop();
                string a = operands.top(); operands.pop();
                char op = operators.top(); operators.pop();
                string res = applyOperator(a, b, op);
                queue.push_back(res);
                operands.push(res);
            }
            operators.pop(); // Remove '('
        } else if (c == '+' || c == '*') {
            while (!operators.empty() && precedence(operators.top()) >= precedence(c)) {
                string b = operands.top(); operands.pop();
                string a = operands.top(); operands.pop();
                char op = operators.top(); operators.pop();
                string res = applyOperator(a, b, op);
                queue.push_back(res);
                operands.push(res);
            }
            operators.push(c);
        }
    }

    while (!operators.empty()) {
        string b = operands.top(); operands.pop();
        string a = operands.top(); operands.pop();
        char op = operators.top(); operators.pop();
        string res = applyOperator(a, b, op);
        queue.push_back(res);
        operands.push(res);
    }

    return operands.top();
}

// Tạo đồ thị NMOS từ biểu thức
void ExpressionParser::createNMOSGraph(Graph& graph, const string& expr) {
    vector<string> queue;
    evaluateExpression(expr, queue);

    // Logic tạo đồ thị NMOS (đơn giản hóa)
    for (const auto& token : queue) {
        if (token.size() == 1 && isalpha(token[0])) {
            graph.addNode(token + "S");
            graph.addNode(token + "D");
            graph.addEdge(token + "S", token + "D");
        } else if (token.find('*') != string::npos) {
            // Xử lý kết nối serial
            size_t op_pos = token.find('*');
            string a = token.substr(0, op_pos);
            string b = token.substr(op_pos + 1);
            graph.addEdge(a + "D", b + "S");
        } else if (token.find('+') != string::npos) {
            // Xử lý kết nối parallel
            size_t op_pos = token.find('+');
            string a = token.substr(0, op_pos);
            string b = token.substr(op_pos + 1);
            graph.addEdge(a + "S", b + "S");
            graph.addEdge(a + "D", b + "D");
        }
    }
}

// Tạo đồ thị PMOS từ biểu thức và Euler path
void ExpressionParser::createPMOSGraph(Graph& graph, const string& expr, const vector<string>& eulerPath) {
    vector<string> queue;
    string inverted_expr;
    for (char c : expr) {
        if (c == '+') inverted_expr += '*';
        else if (c == '*') inverted_expr += '+';
        else inverted_expr += c;
    }
    evaluateExpression(inverted_expr, queue);

    // Thêm các node từ Euler path
    for (const auto& node : eulerPath) {
        graph.addNode(node);
    }

    // Thêm các cạnh từ Euler path
    for (size_t i = 1; i < eulerPath.size(); ++i) {
        graph.addEdge(eulerPath[i-1], eulerPath[i]);
    }

    // Logic tạo đồ thị PMOS (đơn giản hóa)
    for (const auto& token : queue) {
        if (token.find('*') != string::npos) {
            // Xử lý kết nối parallel cho PMOS
            size_t op_pos = token.find('*');
            string a = token.substr(0, op_pos);
            string b = token.substr(op_pos + 1);
            graph.addEdge(a + "S", b + "S");
        } else if (token.find('+') != string::npos) {
            // Xử lý kết nối serial cho PMOS
            size_t op_pos = token.find('+');
            string a = token.substr(0, op_pos);
            string b = token.substr(op_pos + 1);
            graph.addEdge(a + "D", b + "S");
        }
    }
}

// Tìm Euler path (đơn giản hóa)
vector<string> ExpressionParser::findEulerPath(const Graph& graph) {
    // Trong thực tế cần triển khai thuật toán Hierholzer
    // Ở đây chỉ trả về danh sách node đơn giản
    return graph.getNodes();
}

// Tìm các node nguồn (kết nối VDD)
vector<string> ExpressionParser::findSourceNodes(const Graph& graph) {
    vector<string> sources;
    for (const auto& node : graph.getNodes()) {
        if (node.back() == 'S') {
            bool is_source = true;
            for (const auto& neighbor : graph.getNeighbors(node)) {
                if (neighbor.back() == 'D') {
                    is_source = false;
                    break;
                }
            }
            if (is_source) sources.push_back(node);
        }
    }
    return sources;
}

// Tìm các node đầu ra (kết nối OUT)
vector<string> ExpressionParser::findOutputNodes(const Graph& graph) {
    vector<string> outputs;
    for (const auto& node : graph.getNodes()) {
        if (node.back() == 'D') {
            bool is_output = true;
            for (const auto& neighbor : graph.getNeighbors(node)) {
                if (neighbor.back() == 'S') {
                    is_output = false;
                    break;
                }
            }
            if (is_output) outputs.push_back(node);
        }
    }
    return outputs;
}

// Hàm chính tạo cả hai đồ thị
pair<Graph, Graph> ExpressionParser::createGraphs(const string& expr) {
    Graph g_nmos, g_pmos;
    createNMOSGraph(g_nmos, expr);
    
    vector<string> euler_path_nmos = findEulerPath(g_nmos);
    vector<string> euler_path_pmos;
    for (const auto& node : euler_path_nmos) {
        euler_path_pmos.push_back(node);
    }
    reverse(euler_path_pmos.begin(), euler_path_pmos.end());
    
    createPMOSGraph(g_pmos, expr, euler_path_pmos);
    return {g_nmos, g_pmos};
}