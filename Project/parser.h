// parser.h
#ifndef PARSER_H
#define PARSER_H

#include <string>

struct Node {
    std::string value;
    Node* left;
    Node* right;

    Node(const std::string& val) : value(val), left(nullptr), right(nullptr) {}
};

Node* parse_expression(const std::string& expr);
void print_tree(Node* root, int level = 0);

#endif
