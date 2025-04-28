#pragma once
#ifndef EXPRESSION_H
#define EXPRESSION_H

#include <string>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <utility>

using namespace std;

class Graph {
private:
    set<string> _nodes;
    map<string, set<string>> _adjacencyList;

public:
    void addNode(const string& node);
    void addEdge(const string& from, const string& to);
    bool hasEdge(const string& from, const string& to);
    vector<string> neighbors(const string& node) const;
    int degree(const string& node) const;
    vector<string> nodes() const;
    vector<pair<string, string>> edges() const;
    void removeEdge(const string& from, const string& to);
};

int precedence(char op);
string apply_operator(const string& operand1, const string& operand2, char op);
string apply_operator_inv(const string& operand1, const string& operand2, char op);
string exvaluate_expression_inv(const string& expression, vector<string>& q);
string exvaluate_expression(const string& expression, vector<string>& q);
string subtract_expression(const string& expression1, const string& expression2);
string intersection_expressions(const string& expression1, const string& expression2);
bool check_serial_connected(const Graph& g, const string& token, const vector<string>& inter_arr);
bool checking_parallel_connected(const Graph& g, const string& k, const vector<string>& inter_arr);
void create_node(Graph& g, const string& node);
void add_edge_parallel_1(Graph& g, const string& node1, const string& node2);
void add_edge_serial_1(Graph& g, const string& node1, const string& node2, const vector<string>& inter_arr, int mode);
void add_edge_serial_2(Graph& g, const string& node, const vector<string>& inter_arr, int mode);
void add_edge_parallel_2(Graph& g, const string& node, const vector<string>& inter_arr);
void add_edge_parallel_3(Graph& g, const vector<string>& inter_arr, int mode);
void add_edge_serial_3(Graph& g, const vector<string>& inter_arr, int mode);
pair<string, int> lowest_degree_arr_node(const Graph& g, char k, int t, const vector<string> inter_arr, const string& except_node);
string lowest_degree(const Graph& g, char k, int t, const string& except_node1, const string& except_node2, const string& except_node3);
pair<Graph, string> create_graph(Graph& g, const vector<string>& q, int i, const string& expression, int mode);
pair<Graph, string> create_nmos(Graph& g, const string& expression);
Graph create_pmos(Graph& g, const string& expression, const vector<string>& euler_path);
bool is_valid_next_node(const string& v, const vector<string>& path, const Graph& G);
vector<string> hamiltonian_dfs_endnode(const Graph& G, const string& start, const string& end, vector<string> path = {});
vector<string> hamiltonian_dfs(const Graph& G, const string& start, vector<string> path = {});
vector<string> find_hamilton_path(const Graph& g, const string& end_node);
pair<vector<string>, vector<string>> euler_path(const Graph& g, const string& end_node);
Graph filter_edge_pmos(Graph& g, const vector<string>& arr1, const vector<string>& arr2, const vector<string>& euler_path);
bool checking_edge(const Graph& g, const string& full_node, char char_connected);
pair<vector<string>, vector<string>> find_node_source_and_out(const Graph& g);
tuple<Graph, Graph, vector<string>, vector<string>, vector<string>, vector<string>, vector<string>, vector<string>> Create_All(const string& expression);
#endif