// cmos_generator.cpp
#include "cmos_generator.h"
#include <iostream>

void traverse_nmos(Node* node, std::vector<TransistorGroup>& list) {
    if (!node) return;

    if (node->value == "*") {
        traverse_nmos(node->left, list);
        traverse_nmos(node->right, list);
    } else if (node->value == "+") {
        TransistorGroup group{PARALLEL, {}};
        auto left = node->left;
        auto right = node->right;

        if (left->value == "\'" || right->value == "\'") {
            // NOT gate
            std::string signal = (left->value == "\'") ? left->left->value : right->left->value;
            group.signals.push_back(signal + "\'");
        } else {
            group.signals.push_back(left->value);
            group.signals.push_back(right->value);
        }

        list.push_back(group);
    } else if (node->value == "\'") {
        TransistorGroup group{SERIES, {node->left->value + "\'"}};
        list.push_back(group);
    } else {
        TransistorGroup group{SERIES, {node->value}};
        list.push_back(group);
    }
}

void traverse_pmos(Node* node, std::vector<TransistorGroup>& list) {
    if (!node) return;

    if (node->value == "+") {
        traverse_pmos(node->left, list);
        traverse_pmos(node->right, list);
    } else if (node->value == "*") {
        TransistorGroup group{PARALLEL, {}};
        auto left = node->left;
        auto right = node->right;

        if (left->value == "\'" || right->value == "\'") {
            // NOT gate
            std::string signal = (left->value == "\'") ? left->left->value : right->left->value;
            group.signals.push_back(signal + "\'");
        } else {
            group.signals.push_back(left->value);
            group.signals.push_back(right->value);
        }

        list.push_back(group);
    } else if (node->value == "\'") {
        TransistorGroup group{PARALLEL, {node->left->value + "\'"}};
        list.push_back(group);
    } else {
        TransistorGroup group{PARALLEL, {node->value}};
        list.push_back(group);
    }
}

Circuit generate_cmos_circuit(Node* root) {
    Circuit result;
    traverse_nmos(root, result.nmos);
    traverse_pmos(root, result.pmos);
    return result;
}
