// parser.cpp
#include "parser.h"
#include <stack>
#include <iostream>
#include <cctype>

// Độ ưu tiên: NOT > AND > OR
int precedence(char op) {
    if (op == '\'') return 3;
    if (op == '*') return 2;
    if (op == '+') return 1;
    return 0;
}

bool is_operator(char c) {
    return c == '+' || c == '*' || c == '\'';
}

// Chuyển trung tố sang hậu tố (postfix)
std::string to_postfix(const std::string& infix) {
    std::string postfix;
    std::stack<char> ops;

    for (size_t i = 0; i < infix.size(); ++i) {
        char token = infix[i];

        if (std::isspace(token)) continue;

        if (std::isalpha(token)) {
            postfix += token;
        } else if (token == '(') {
            ops.push(token);
        } else if (token == ')') {
            while (!ops.empty() && ops.top() != '(') {
                postfix += ops.top(); ops.pop();
            }
            if (!ops.empty()) ops.pop(); // pop '('
        } else if (is_operator(token)) {
            while (!ops.empty() && precedence(token) <= precedence(ops.top())) {
                postfix += ops.top(); ops.pop();
            }
            ops.push(token);
        }
    }

    while (!ops.empty()) {
        postfix += ops.top(); ops.pop();
    }

    return postfix;
}

// Tạo cây từ hậu tố
Node* build_tree(const std::string& postfix) {
    std::stack<Node*> stk;

    for (char c : postfix) {
        if (std::isalpha(c)) {
            stk.push(new Node(std::string(1, c)));
        } else if (c == '\'') {
            Node* a = stk.top(); stk.pop();
            Node* n = new Node("\'");
            n->left = a;
            stk.push(n);
        } else if (c == '+' || c == '*') {
            Node* b = stk.top(); stk.pop();
            Node* a = stk.top(); stk.pop();
            Node* n = new Node(std::string(1, c));
            n->left = a;
            n->right = b;
            stk.push(n);
        }
    }

    return stk.top();
}

Node* parse_expression(const std::string& expr) {
    std::string postfix = to_postfix(expr);
    return build_tree(postfix);
}

// Debug in cây
void print_tree(Node* root, int level) {
    if (!root) return;
    print_tree(root->right, level + 1);
    std::cout << std::string(level * 4, ' ') << root->value << "\n";
    print_tree(root->left, level + 1);
}
