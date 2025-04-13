#include "logic_parser.h"
#include <stack>

int precedence(char op) {
    if (op == '+') return 1;
    if (op == '*') return 2;
    return 0;
}

std::vector<std::string> to_postfix(const std::string& expr) {
    std::vector<std::string> output;
    std::stack<char> ops;
    for (char ch : expr) {
        if (isalpha(ch)) output.push_back(std::string(1, ch));
        else if (ch == '(') ops.push(ch);
        else if (ch == ')') {
            while (!ops.empty() && ops.top() != '(') {
                output.push_back(std::string(1, ops.top()));
                ops.pop();
            }
            if (!ops.empty()) ops.pop();
        } else if (ch == '+' || ch == '*') {
            while (!ops.empty() && precedence(ops.top()) >= precedence(ch)) {
                output.push_back(std::string(1, ops.top()));
                ops.pop();
            }
            ops.push(ch);
        }
    }
    while (!ops.empty()) {
        output.push_back(std::string(1, ops.top()));
        ops.pop();
    }
    return output;
}

std::vector<std::string> to_postfix_inv(const std::string& expr) {
    std::vector<std::string> output;
    std::stack<char> ops;
    for (char ch : expr) {
        if (isalpha(ch)) output.push_back(std::string(1, ch));
        else if (ch == '(') ops.push(ch);
        else if (ch == ')') {
            while (!ops.empty() && ops.top() != '(') {
                char op = ops.top(); ops.pop();
                output.push_back(op == '+' ? "*" : "+");
            }
            if (!ops.empty()) ops.pop();
        } else if (ch == '+' || ch == '*') {
            while (!ops.empty() && precedence(ops.top()) >= precedence(ch)) {
                char op = ops.top(); ops.pop();
                output.push_back(op == '+' ? "*" : "+");
            }
            ops.push(ch);
        }
    }
    while (!ops.empty()) {
        char op = ops.top(); ops.pop();
        output.push_back(op == '+' ? "*" : "+");
    }
    return output;
}
