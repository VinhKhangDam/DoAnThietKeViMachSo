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

    // ==== Tokenizer nâng cao ====
    std::string current;
    for (size_t i = 0; i < expression.size(); ++i) {
        char ch = expression[i];
        if (isalnum(ch)) {
            current += ch;
        } else {
            if (!current.empty()) {
                tokens.push_back(current);
                current.clear();
            }
            if (ch == '+' || ch == '*' || ch == '(' || ch == ')') {
                tokens.push_back(std::string(1, ch));
            } else if (!isspace(ch)) {
                std::cerr << "Invalid character in expression: '" << ch << "'\n";
                return;
            }
        }
    }
    if (!current.empty()) tokens.push_back(current);

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
    std::stack<std::vector<std::string>> stack;
    std::unordered_map<std::string, int> varCount;
    auto fresh_name = [&](const std::string& var) {
        return var + "_" + std::to_string(varCount[var]++);
    };

    for (const auto& token : postfix) {
        if (isalnum(token[0])) {
            std::string vname = fresh_name(token);
            g_nmos.addNode(vname + "S");
            g_nmos.addNode(vname + "D");
            g_nmos.addEdge(vname + "S", vname + "D");
            stack.push({vname});
        } else if (token == "+" || token == "*") {
            if (stack.size() < 2) {
                std::cerr << "Invalid expression (not enough operands for '" << token << "')\n";
                return;
            }
            auto b = stack.top(); stack.pop();
            auto a = stack.top(); stack.pop();
            std::vector<std::string> result;
            if (token == "+") {
                for (const auto& x : a) {
                    for (const auto& y : b) {
                        g_nmos.addEdge(x + "S", y + "S");
                        g_nmos.addEdge(x + "D", y + "D");
                    }
                }
            } else if (token == "*") {
                for (const auto& x : a) {
                    for (const auto& y : b) {
                        g_nmos.addEdge(x + "D", y + "S");
                    }
                }
            }
            result.insert(result.end(), a.begin(), a.end());
            result.insert(result.end(), b.begin(), b.end());
            stack.push(result);
        }
    }
}

void LogicExpression::buildPMOS() {
    std::stack<std::vector<std::string>> stack;
    std::unordered_map<std::string, int> varCount;
    auto fresh_name = [&](const std::string& var) {
        return var + "_" + std::to_string(varCount[var]++);
    };

    for (const auto& token : postfix) {
        if (isalnum(token[0])) {
            std::string vname = fresh_name(token);
            g_pmos.addNode(vname + "S");
            g_pmos.addNode(vname + "D");
            g_pmos.addEdge(vname + "S", vname + "D");
            stack.push({vname});
        } else if (token == "+" || token == "*") {
            if (stack.size() < 2) {
                std::cerr << "Invalid expression (not enough operands for '" << token << "')\n";
                return;
            }
            auto b = stack.top(); stack.pop();
            auto a = stack.top(); stack.pop();
            std::vector<std::string> result;
            if (token == "*") {
                for (const auto& x : a) {
                    for (const auto& y : b) {
                        g_pmos.addEdge(x + "S", y + "S");
                        g_pmos.addEdge(x + "D", y + "D");
                    }
                }
            } else if (token == "+") {
                for (const auto& x : a) {
                    for (const auto& y : b) {
                        g_pmos.addEdge(x + "D", y + "S");
                    }
                }
            }
            result.insert(result.end(), a.begin(), a.end());
            result.insert(result.end(), b.begin(), b.end());
            stack.push(result);
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
        std::string base = node.substr(0, node.size() - 1); // remove S/D
        if (seen.insert(base).second)
            f3 << base << "\n";
    }
}
