//============================================================
// LogicExpression : phan tich bieu thuc, tao do thi NMOS/PMOS
//============================================================

#pragma once
#ifndef LOGIC_EXPRESSION
#define LOGIC_EXPRESSION
#include "GraphUtil.h"
#include <vector>
#include <string>

class LogicExpression {
public:
    LogicExpression(const std::string& expr);
    void parse();
    void buildNMOS();
    void buildPMOS();
    void exportData(const std::string& dir);

private:
    std::string expression;
    std::vector<std::string> postfix;
    Graph g_nmos, g_pmos;
    std::unordered_map<std::string, Graph> g_nmos_map;
    std::unordered_map<std::string, Graph> g_pmos_map;
    std::set<std::string> variables;
    int precedence(char op);
};

#endif