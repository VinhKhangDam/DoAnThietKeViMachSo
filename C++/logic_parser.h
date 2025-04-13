#pragma once
#include <vector>
#include <string>

int precedence(char op);
std::vector<std::string> to_postfix(const std::string& expr);
std::vector<std::string> to_postfix_inv(const std::string& expr);