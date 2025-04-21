// ===============================
// File: LogicExpression.cpp (Đã nâng cấp parser + Thêm lại buildNMOS, buildPMOS, exportData)
// ===============================
#include "LogicExpression.h"
#include <stack>
#include <fstream>
#include <algorithm>
#include <set>
#include <iostream>
#include <unordered_map>
#include <cctype>

LogicExpression::LogicExpression(const std::string& expr) : expression(expr) {}

int LogicExpression::precedence(char op) {
    if (op == '+') return 1;
    if (op == '*') return 2;
    return 0;
}

void LogicExpression::parse() {
    std::stack<char> ops;
    std::vector<std::string> tokens;
    std::string current;

    for (char ch : expression) {
        if (isalnum(ch)) {
            current += ch;
        } else {
            if (!current.empty()) {
                tokens.push_back(current);
                variables.insert(current);  // Thêm biến vào tập hợp
                current.clear();
            }
            if (ch == '+' || ch == '*' || ch == '(' || ch == ')') {
                tokens.push_back(std::string(1, ch));
            }
        }
    }
    if (!current.empty()) {
        tokens.push_back(current);
        variables.insert(current);  // Thêm biến cuối cùng
    }
    // ==== Infix to Postfix (Shunting Yard) ====
    for (const auto& token : tokens) {
        if (isalnum(token[0])) {
            postfix.push_back(token);
        } else if (token == "(") {
            ops.push('(');
        } else if (token == ")") {
            while (!ops.empty() && ops.top() != '(') {
                postfix.push_back(std::string(1, ops.top()));
                ops.pop();
            }
            if (!ops.empty()) ops.pop();
            else {
                std::cerr << "Mismatched parentheses\n";
                return;
            }
        } else if (token == "+" || token == "*") {
            while (!ops.empty() && precedence(ops.top()) >= precedence(token[0])) {
                postfix.push_back(std::string(1, ops.top()));
                ops.pop();
            }
            ops.push(token[0]);
        }
    }
    while (!ops.empty()) {
        if (ops.top() == '(' || ops.top() == ')') {
            std::cerr << "Mismatched parentheses\n";
            return;
        }
        postfix.push_back(std::string(1, ops.top()));
        ops.pop();
    }

    std::cout << "Postfix expression: ";
    for (const auto& token : postfix) std::cout << token << " ";
    std::cout << std::endl;
}

void LogicExpression::buildNMOS() {
    std::set<std::string> created;  // Đảm bảo mỗi biến chỉ tạo node một lần

    for (const auto& token : postfix) {
        if (isalnum(token[0]) && created.insert(token).second) {
            std::string dNode = token + "_D";  // NMOS Drain node
            std::string sNode = token + "_S";  // NMOS Source node
            g_nmos.addNode(token);            // Tạo node chỉ là "A", "B", "C", ...
            g_nmos.addNode(dNode);            // Tạo node "A_D", "B_D", "C_D", ...
            g_nmos.addNode(sNode);            // Tạo node "A_S", "B_S", "C_S", ...
            g_nmos.addEdge(dNode, sNode);     // Kết nối NMOS: D -> S
        }
    }
}




void LogicExpression::buildPMOS() {
    std::set<std::string> created;  // Đảm bảo mỗi biến chỉ tạo node một lần

    for (const auto& token : postfix) {
        if (isalnum(token[0]) && created.insert(token).second) {
            std::string sNode = token + "_S";  // PMOS Source node
            std::string dNode = token + "_D";  // PMOS Drain node
            g_pmos.addNode(token);             // Tạo node chỉ là "A", "B", "C", ...
            g_pmos.addNode(sNode);             // Tạo node "A_S", "B_S", "C_S", ...
            g_pmos.addNode(dNode);             // Tạo node "A_D", "B_D", "C_D", ...
            g_pmos.addEdge(sNode, dNode);      // Kết nối PMOS: S -> D
        }
    }
}


void LogicExpression::exportData(const std::string& dir) {
    std::ofstream f1(dir + "/edges_nmos.txt");
    for (auto& e : g_nmos.getEdges()) f1 << e.first << " " << e.second << "\n";

    std::ofstream f2(dir + "/edges_pmos.txt");
    for (auto& e : g_pmos.getEdges()) f2 << e.first << " " << e.second << "\n";

    std::ofstream f3(dir + "/logic_elements.txt");
    std::set<std::string> seen;
    for (auto& node : g_nmos.getNodes()) {
        std::string base = node;
        // Kiểm tra và loại bỏ hậu tố "_S" hoặc "_D" nếu có
        if (base.size() > 2 && (base.substr(base.size() - 2) == "_S" || base.substr(base.size() - 2) == "_D")) {
            base = base.substr(0, base.size() - 2);
        }
        if (seen.insert(base).second)
            f3 << base << "\n";
    }
}

