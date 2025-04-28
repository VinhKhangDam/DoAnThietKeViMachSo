#include "Expression.h"
#include <algorithm>
#include <climits>
#include <queue>
#include <stack>

void Graph::addNode(const string& node) {
    _nodes.insert(node);
    if (_adjacencyList.find(node) == _adjacencyList.end()) {
        _adjacencyList[node] = set<string>();
    }
}

void Graph::addEdge(const string& from, const string& to) {
    addNode(from);
    addNode(to);
    _adjacencyList[from].insert(to);
    _adjacencyList[to].insert(from);
}

bool Graph::hasEdge(const string &from ,const string &to) {
    auto it = _adjacencyList.find(from);
    if(it != _adjacencyList.end()) {
        return it->second.find(to) != it->second.end();
    }
    return false;
}

vector<string> Graph::neighbors(const string& node) const {
    vector<string> result;
    auto it = _adjacencyList.find(node);
    if (it != _adjacencyList.end()) {
        result.assign(it->second.begin(), it->second.end());
    }
    return result;
}

int Graph::degree(const string& node) const {
    auto it = _adjacencyList.find(node);
    if (it != _adjacencyList.end()) {
        return it->second.size();
    }
    return 0;
}

vector<string>  Graph::nodes() const {
    return vector<string>(_nodes.begin(), _nodes.end());
}

vector<pair<string, string>> Graph::edges() const {
    vector<pair<string, string>> result;
    set<pair<string, string>> added;

    for (const auto& node : _nodes) {
        for (const auto& neighbor: _adjacencyList.at(node)) {
            pair<string, string> edge = (node < neighbor) ? make_pair(node, neighbor) : make_pair(neighbor, node);
            if (added.find(edge) == added.end()) {
                result.push_back(edge);
                added.insert(edge);
            }
        }
    }
    return result;
}

void Graph::removeEdge(const string& from, const string& to) {
    _adjacencyList[from].erase(to);
    _adjacencyList[to].erase(from);
}

//precedence
int precedence(char op) {
    if (op == '+') return 1;
    else if (op == '*') return 2;
    else return 0;
}

string apply_operator(const string& operand1, const string& operand2, char op) {
    if (op == '+') 
        return operand1 + " + " + operand2;
    else 
        return operand1 + " * " + operand2;
}

string apply_operator_inv(const string& operand1, const string& operand2, char op) {
    if (op == '+') 
        return operand1 + " * " + operand2;
    else 
        return operand1 + " + " + operand2;
}

string exvaluate_expression_inv(const string& expression, vector<string>& q) {
    stack<string> operand_stack;
    stack<char> operator_stack;
    size_t index = 0;

    while (index < expression.length()) {
        char token = expression[index];
        if (isalpha(token)) {
            operand_stack.push(string(1, token));
            index++;
        }
        else if (token == '+' || token == '*' || token == '/' || token == '^') {
            while (!operator_stack.empty() && precedence(operator_stack.top()) >= precedence(token)) {
                char op = operator_stack.top();
                operator_stack.pop();
                string operand2 = operand_stack.top();
                operand_stack.pop();
                string operand1 = operand_stack.top();
                operand_stack.pop();
                string result = apply_operator_inv(operand1, operand2, op);
                q.push_back(result);
                operand_stack.push(result); 
            }
            operator_stack.push(token);
            index++;
        }
        else if (token == '(') {
            operator_stack.push(token);
            index++;  
        }
        else if (token == ')') {
            while (operator_stack.top()!='(') {
                char op = operator_stack.top();
                operator_stack.pop();
                string operand2 = operand_stack.top();
                operand_stack.pop();
                string operand1 = operand_stack.top();
                operand_stack.pop();
                string result = apply_operator_inv(operand1, operand2, op);
                q.push_back(result);
                operand_stack.push(result); 
            }
            operator_stack.pop();
            index++;
        }
        else {
            index++;
        }
    }

    while (!operator_stack.empty()) {
        char op = operator_stack.top();
        operator_stack.pop();
        string operand2 = operand_stack.top();
        operand_stack.pop();
        string operand1 = operand_stack.top();
        operand_stack.pop();
        string result = apply_operator_inv(operand1, operand2, op);
        q.push_back(result);
        operand_stack.push(result); 
    }
    return operand_stack.empty() ? "" : operand_stack.top();
}

string evaluate_expression(const string& expression, vector<string>& q) {
    stack<string> operand_stack;
    stack<char> operator_stack;
    size_t index = 0;

    while (index < expression.length()) {
        char token = expression[index];
        if (isalpha(token)) {
            operand_stack.push(string(1, token));
            index++;
        } else if (token == '+' || token == '*' || token == '/' || token == '^') {
            while (!operator_stack.empty() && precedence(operator_stack.top()) >= precedence(token)) {
                char op = operator_stack.top();
                operator_stack.pop();
                string operand2 = operand_stack.top();
                operand_stack.pop();
                string operand1 = operand_stack.top();
                operand_stack.pop();
                string result = apply_operator(operand1, operand2, op);
                q.push_back(result);
                operand_stack.push(result);
            }
            operator_stack.push(token);
            index++;
        } else if (token == '(') {
            operator_stack.push(token);
            index++;
        } else if (token == ')') {
            while (operator_stack.top() != '(') {
                char op = operator_stack.top();
                operator_stack.pop();
                string operand2 = operand_stack.top();
                operand_stack.pop();
                string operand1 = operand_stack.top();
                operand_stack.pop();
                string result = apply_operator(operand1, operand2, op);
                q.push_back(result);
                operand_stack.push(result);
            }
            operator_stack.pop();
            index++;
        } else {
            index++;
        }
    }

    while (!operator_stack.empty()) {
        char op = operator_stack.top();
        operator_stack.pop();
        string operand2 = operand_stack.top();
        operand_stack.pop();
        string operand1 = operand_stack.top();
        operand_stack.pop();
        string result = apply_operator(operand1, operand2, op);
        q.push_back(result);
        operand_stack.push(result);
    }

    return operand_stack.empty() ? "" : operand_stack.top();
}

string subtract_expression(const string& expression1, const string& expression2) {
    string result;
    size_t i = 0, j = 0;
    while (i < expression1.length()) {
        if (j >= expression2.length() || expression1[i] != expression2[j]) {
            result += expression1[i];
            i++;
        } else {
            i++;
            j++;
        }
    }
    return result;
}

string intersection_expressions(const string& expression1, const string& expression2) {
    string result;
    size_t i = 0, j = 0;
    while (i < expression1.length() && j < expression2.length()) {
        if (expression1[i] == expression2[j]) {
            result += expression1[i];
            i++; j++;
        } else {
            i++;
        }
    }
    return result;
}

void create_node(Graph& g, const string& node) {
    string node1 = node + "S";
    string node2 = node + "D";
    g.addNode(node1);
    g.addNode(node2);
    g.addEdge(node1, node2);
}

void add_edge_parallel_1(Graph& g, const string& node1, const string& node2) {
    string n1 = node1 + "S";
    string n2 = node1 + "D";
    string n3 = node2 + "S";
    string n4 = node2 + "D";
    g.addEdge(n1, n3);
    g.addEdge(n2, n4);
}

bool check_serial_connected(Graph& g, const string& token, const vector<string>& inter_arr) {
    if (inter_arr.empty()) return true;

    vector<string> arr1, arr2;
    size_t i = 0;

    while (i < inter_arr.size() && inter_arr[i] != "0") {
        arr1.push_back(inter_arr[i]);
        i++;
    }
    i++;

    while (i < inter_arr.size() && inter_arr[i] != "0") {
        arr2.push_back(inter_arr[i]);
        i++;
    }

    if (arr2.empty()) {
        string n1_s = token + "S";
        string n1_d = token + "D";
        for (size_t i = 0; i < arr1.size(); i++) {
            string n2_s = arr1[i] + "S";
            string n2_d = arr1[i] + "D";
            if (g.hasEdge(n1_s, n2_d)) return false;
            if (g.hasEdge(n1_d, n2_s)) return false;
        }
        return true;
    }
    else {
        for (size_t i = 0; i < arr1.size(); i++) {
            string n1_s = arr1[i] + "S";
            string n1_d = arr1[i] + "D";
            for (size_t j = 0; j< arr2.size(); j++) {
                string n2_s = arr2[j] + "S";
                string n2_d = arr2[j] + "D";
                if (g.hasEdge(n1_s, n2_d)) return false;
                if (g.hasEdge(n1_d, n2_s)) return false;
            }
        }
        return true;
    }
}

void add_edge_serial_1(Graph& g, const string& node1, const string& node2, const vector<string>& inter_arr, int mode) {
    string n1 = node1 + "S";
    string n2 = node1 + "D";
    string n3 = node2 + "S";
    string n4 = node2 + "D";

    if (mode == 0) {
        g.addEdge(n3, n2);
    }
    else {
        vector<string> arr = {node1, "0", node2, "0"};
        if (check_serial_connected(g, " ", arr)) {
            g.addEdge(n3, n2);
        }
    }
}

bool checking_parallel_connected(Graph& g, const string& k, const vector<string>& inter_arr) {
    if (inter_arr.empty()) return true;

    vector<string> arr1, arr2;
    size_t i = 0;
    
    while (i < inter_arr.size() && inter_arr[i] != "0") {
        arr1.push_back(inter_arr[i]);
        i++;
    }
    i++; // Skip the "0"
    
    while (i < inter_arr.size() && inter_arr[i] != "0") {
        arr2.push_back(inter_arr[i]);
        i++;
    }

    if (arr2.empty()) {
        for (size_t i = 0; i < arr1.size(); i++) {
            string n1 = arr1[i] + k;
            for (size_t j = i + 1; j < arr1.size(); j++) {
                string n2 = arr1[j] + k;
                if (g.hasEdge(n1, n2)) return false;
            }
        }
        return true;
    } else {
        for (size_t i = 0; i < arr1.size(); i++) {
            string n1 = arr1[i] + k;
            for (size_t j = 0; j < arr2.size(); j++) {
                string n2 = arr2[j] + k;
                if (g.hasEdge(n1, n2)) return false;
            }
        }
        return true;
    }
}
pair<string, int> lowest_degree_arr_node(const Graph& g, char k, int start_idx, const vector<string>& inter_arr, const string& except_node) {
    string min_node;
    int min_degree = INT_MAX;
    bool found = false;
    
    // Duyệt từ start_idx đến hết mảng inter_arr
    for (int i = start_idx; i < inter_arr.size(); i++) {
        if (inter_arr[i] == "0") {
            // Bỏ qua các phần tử phân cách
            continue;
        }
        
        string node = inter_arr[i] + k; // Thêm 'S' hoặc 'D'
        int degree = g.degree(node);
        
        // Kiểm tra node có phải là node cần bỏ qua không
        if (!except_node.empty() && node == except_node) {
            continue;
        }
        
        // Cập nhật node có degree nhỏ nhất
        if (degree < min_degree) {
            min_degree = degree;
            min_node = node;
            found = true;
        }
    }
    
    // Nếu không tìm thấy node hợp lệ
    if (!found) {
        return make_pair("", INT_MAX);
    }
    
    // Tìm vị trí tiếp theo để duyệt
    int next_idx = start_idx;
    while (next_idx < inter_arr.size() && inter_arr[next_idx] != "0") {
        next_idx++;
    }
    next_idx++; // Bỏ qua phần tử "0"
    
    return make_pair(min_node, min_degree);
}

string lowest_degree(const Graph& g, char k, const string& except_node1, const string& except_node2, const string& except_node3) {
    map<string, int> degrees;
    vector<string> nodes = g.nodes();

    for (const auto& node:nodes) {
        if (node.back() == k) {
            if (!except_node1.empty() && (node == except_node1 + "S" || node == except_node1 + "D")) continue;
            if (!except_node2.empty() && (node == except_node2 + "S" || node == except_node2 + "D")) continue;
            if (!except_node3.empty() && (node == except_node3 + "S" || node == except_node3 + "D")) continue;
            degrees[node] = g.degree(node);
        }
    }

    if (degrees.empty()) return "";

    auto min_it = min_element(degrees.begin(), degrees.end(),
                [](const pair<string, int>& a, const pair<string, int>& b) {
                    return a.second < b.second;
                });
    return min_it->first;
}

//Main creation function

tuple<Graph, Graph, vector<string>, vector<string>, vector<string>, vector<string>, vector<string>, vector<string>>
Create_All(const string& expression) {
    Graph g_nmos;
    Graph g_pmos;
    string node;

    vector<string> q;
    evaluate_expression(expression, q);
    tie(g_nmos, node) = create_nmos(g_nmos, expression);

    vector<string> source_nodes_nmos, out_nodes_nmos;
    tie(source_nodes_nmos, out_nodes_nmos) = find_node_source_and_out(g_nmos);

    vector<string> serial_array_pmos, parallel_arrays_pmos;
    for (const auto& edge: g_nmos.edges()) {
        string n1 = edge.first.substr(0, 1);
        string n2 = edge.second.substr(0, 1);
        if (n1 == n2) continue;

        if (edge.first.back() == edge.second.back()) {
            serial_array_pmos.push_back(n1+n2);
        } else {
            parallel_arrays_pmos.push_back(n1+n2);
        }
    }

    //Find Euler path
    vector<string> euler_path_nmos, euler_path_pmos;
    tie(euler_path_nmos, euler_path_pmos) = euler_path(g_nmos, node);

    //create PMOS graph
    g_pmos = create_pmos(g_pmos, expression, euler_path_pmos);
    g_pmos = filter_edge_pmos(g_pmos, serial_array_pmos, parallel_arrays_pmos, euler_path_pmos);

    vector<string> source_node_pmos, out_nodes_pmos;
    tie(source_node_pmos, out_nodes_pmos) = find_node_source_and_out(g_pmos);

    return make_tuple(g_nmos, g_pmos, euler_path_nmos, euler_path_pmos, source_nodes_nmos, out_nodes_nmos, source_node_pmos, out_nodes_pmos);
}

pair<Graph, string> create_nmos(Graph& g, const string& expression) {
    vector<string> q;
    string end_node;
    evaluate_expression(expression, q);

    for (size_t i = 0; i < q.size(); i++) {
        tie(g, end_node) = create_graph(g, q, i, q[i], 0);
    }
    return make_pair(g, end_node);
}

Graph create_pmos(Graph& g, const string& expression, const vector<string>& euler_path) {
    vector<string> q;
    evaluate_expression(expression, q);

    for (size_t i = 0; i < euler_path.size(); i++) {
        g.addNode(euler_path[i]);
        if (i != 0) {
            g.addEdge(euler_path[i], euler_path[i-1]);
        }
    }

    for (size_t i = 0; i < q.size(); i++) {
        create_graph(g, q, i, q[i], 1);
    }
    return g;
}

bool is_valid_next_node(const string& v, const vector<string>& path,Graph& G) {
     // Check if node already in path
     if (find(path.begin(), path.end(), v) != path.end()) {
        return false;
    }
    
    // Check S/D nodes are adjacent
    string last_node = path.back();
    if (last_node[0] != v[0]) {
        if (last_node[1] == 'S') {
            string x = string(1, last_node[0]) + "D";
            if (find(path.begin(), path.end(), x) == path.end()) {
                return false;
            }
        } else if (last_node[1] == 'D') {
            string x = string(1, last_node[0]) + "S";
            if (find(path.begin(), path.end(), x) == path.end()) {
                return false;
            }
        }
    }
    
    // Check if nodes are connected
    return G.hasEdge(last_node, v);
}

vector<string> hamiltonian_dfs_endnode(const Graph& G, const string& start, const string& end, vector<string> path) {
    path.push_back(start);
    
    if (path.size() == G.nodes().size()) {
        return path;
    }
    
    for (const auto& v : G.neighbors(start)) {
        if (is_valid_next_node(v, path, G)) {
            vector<string> new_path = hamiltonian_dfs_endnode(G, v, end, path);
            if (!new_path.empty()) {
                return new_path;
            }
        }
    }
    
    return vector<string>();
}

vector<string> hamiltonian_dfs(const Graph& G, const string& start, vector<string> path) {
    path.push_back(start);
    
    if (path.size() == G.nodes().size()) {
        return path;
    }
    
    for (const auto& v : G.neighbors(start)) {
        if (is_valid_next_node(v, path, G)) {
            vector<string> new_path = hamiltonian_dfs(G, v, path);
            if (!new_path.empty()) {
                return new_path;
            }
        }
    }
    
    return vector<string>();
}

vector<string> find_hamilton_path(const Graph& g, const string& end_node) {
    vector<string> path;
    vector<string> nodes = g.nodes();
    
    // Try D nodes first
    for (const auto& node : nodes) {
        if (node.back() == 'D') {
            if (!end_node.empty()) {
                path = hamiltonian_dfs_endnode(g, node, end_node);
                if (!path.empty()) {
                    // Check if end_node is at start or end
                    if (path[0][0] != end_node[0] && path.back()[0] != end_node[0]) {
                        path.clear();
                        continue;
                    }
                    break;
                }
            } else {
                path = hamiltonian_dfs(g, node);
                if (!path.empty()) break;
            }
        }
    }
    
    // If no path found, try S nodes
    if (path.empty()) {
        for (const auto& node : nodes) {
            if (node.back() == 'S') {
                if (!end_node.empty()) {
                    path = hamiltonian_dfs_endnode(g, node, end_node);
                    if (!path.empty()) {
                        if (path[0][0] != end_node[0] && path.back()[0] != end_node[0]) {
                            path.clear();
                            continue;
                        }
                        break;
                    }
                } else {
                    path = hamiltonian_dfs(g, node);
                    if (!path.empty()) break;
                }
            }
        }
    }
    
    return path;
}

pair<vector<string>, vector<string>> euler_path(const Graph& g, const string& end_node) {
    vector<string> euler_path_nmos = find_hamilton_path(g, end_node);
    vector<string> euler_path_pmos;
    
    if (euler_path_nmos.empty()) {
        return make_pair(vector<string>(), vector<string>());
    }
    
    euler_path_pmos.resize(euler_path_nmos.size());
    bool s = false;
    
    for (size_t i = 0; i < euler_path_nmos.size() - 1; i += 2) {
        if (s) {
            euler_path_pmos[i] = euler_path_nmos[i+1];
            euler_path_pmos[i+1] = euler_path_nmos[i];
        } else {
            euler_path_pmos[i] = euler_path_nmos[i];
            euler_path_pmos[i+1] = euler_path_nmos[i+1];
        }
        s = !s;
    }
    
    return make_pair(euler_path_nmos, euler_path_pmos);
}

Graph filter_edge_pmos(Graph& g, const vector<string>& arr1, const vector<string>& arr2, const vector<string>& euler_path) {
    vector<string> check_serial;
    vector<string> check_parallel;
    
    // Analyze Euler path for connections
    for (size_t i = 0; i < euler_path.size(); i++) {
        if (i != 0) {
            string n1 = euler_path[i];
            string n2 = euler_path[i-1];
            
            if (n1[0] != n2[0] && n1[1] != n2[1]) {
                check_serial.push_back(string(1, n1[0]) + n2[0]);
                check_serial.push_back(string(1, n2[0]) + n1[0]);
            }
            if (n1[0] != n2[0] && n1[1] == n2[1]) {
                check_parallel.push_back(string(1, n1[0]) + n2[0] + n1[1]);
                check_parallel.push_back(string(1, n2[0]) + n1[0] + n1[1]);
            }
        }
    }
    
    // Filter edges based on analysis
    vector<pair<string, string>> edges = g.edges();
    for (const auto& edge : edges) {
        string n1 = string(1, edge.first[0]);
        string n2 = string(1, edge.second[0]);
        
        if (n1 == n2) continue;
        
        char n3 = edge.first[1];
        char n4 = edge.second[1];
        
        if (n3 != n4) {
            string node1 = n1 + n2;
            string node2 = n2 + n1;
            
            bool in_arr1 = (find(arr1.begin(), arr1.end(), node1) != arr1.end()) || 
                          (find(arr1.begin(), arr1.end(), node2) != arr1.end());
            
            bool in_check_serial = (find(check_serial.begin(), check_serial.end(), node1) != check_serial.end()) || 
                                 (find(check_serial.begin(), check_serial.end(), node2) != check_serial.end());
            
            if (in_arr1 && !in_check_serial) {
                if (g.hasEdge(n1 + "S", n2 + "D")) {
                    g.removeEdge(n1 + "S", n2 + "D");
                    
                    // Find alternative connections
                    vector<string> nodes = g.nodes();
                    for (const auto& node : nodes) {
                        if (g.hasEdge(node, n2 + "D") && node[1] == 'S') {
                            g.addEdge(n1 + "S", string(1, node[0]) + "D");
                            break;
                        }
                        if (g.hasEdge(node, n1 + "D") && node[1] == 'S') {
                            g.addEdge(n2 + "S", string(1, node[0]) + "D");
                            break;
                        }
                    }
                }
                
                if (g.hasEdge(n1 + "D", n2 + "S")) {
                    g.removeEdge(n1 + "D", n2 + "S");
                    
                    // Find alternative connections
                    vector<string> nodes = g.nodes();
                    for (const auto& node : nodes) {
                        if (g.hasEdge(node, n2 + "S") && node[1] == 'D') {
                            g.addEdge(n1 + "D", string(1, node[0]) + "S");
                            break;
                        }
                        if (g.hasEdge(node, n1 + "S") && node[1] == 'D') {
                            g.addEdge(n2 + "D", string(1, node[0]) + "S");
                            break;
                        }
                    }
                }
            }
        } else {
            string node1 = n1 + n2;
            string node2 = n2 + n1;
            
            bool in_arr2 = (find(arr2.begin(), arr2.end(), node1) != arr2.end()) || 
                          (find(arr2.begin(), arr2.end(), node2) != arr2.end());
            
            if (!in_arr2) {
                for (const auto& n : check_parallel) {
                    if (node1 != n.substr(0, 2) && node2 != n.substr(0, 2)) {
                        if (n3 == n[2]) {
                            if (g.hasEdge(n1 + n.substr(2, 1), n2 + n.substr(2, 1))) {
                                g.removeEdge(n1 + n.substr(2, 1), n2 + n.substr(2, 1));
                            }
                        }
                    }
                }
            }
        }
    }
    
    return g;
}

bool checking_edge(Graph& g, const string& full_node, char char_connected) {
    vector<string> nodes = g.nodes();
    for (const auto& node : nodes) {
        if (node[0] == full_node[0]) continue;
        
        if (char_connected == '\0') {
            if (g.hasEdge(full_node, node)) {
                return false;
            }
        } else {
            if (node[1] == char_connected) {
                if (g.hasEdge(full_node, node)) {
                    return false;
                }
            }
        }
    }
    return true;
}

pair<vector<string>, vector<string>> find_node_source_and_out(const Graph& g) {
    vector<string> source_nodes;
    vector<string> out_nodes;
    
    // First pass: find source and output node pairs
    vector<pair<string, string>> source_pairs;
    vector<pair<string, string>> out_pairs;
    
    for (const auto& edge : g.edges()) {
        string n1 = string(1, edge.first[0]);
        string n2 = string(1, edge.second[0]);
        
        if (n1 == n2) continue;
        
        if (edge.first[1] == edge.second[1]) {
            if (edge.first[1] == 'S') {
                source_pairs.emplace_back(n1, n2);
            } else {
                out_pairs.emplace_back(n1, n2);
            }
        }
    }
    
    // Filter source pairs
    vector<pair<string, string>> temp_source_pairs;
    for (const auto& pair : source_pairs) {
        string n1_s = pair.first + "S";
        string n2_s = pair.second + "S";
        
        if (checking_edge(g, n1_s, 'D') && checking_edge(g, n2_s, 'D')) {
            temp_source_pairs.push_back(pair);
        }
    }
    
    // Convert valid pairs to node list
    for (const auto& pair : temp_source_pairs) {
        source_nodes.push_back(pair.first + "S");
        source_nodes.push_back(pair.second + "S");
    }
    
    // Filter output pairs
    vector<pair<string, string>> temp_out_pairs;
    for (const auto& pair : out_pairs) {
        string n1_d = pair.first + "D";
        string n2_d = pair.second + "D";
        
        if (checking_edge(g, n1_d, 'S') && checking_edge(g, n2_d, 'S')) {
            temp_out_pairs.push_back(pair);
        }
    }
    
    // Convert valid pairs to node list
    for (const auto& pair : temp_out_pairs) {
        out_nodes.push_back(pair.first + "D");
        out_nodes.push_back(pair.second + "D");
    }
    
    // If no pairs found, look for individual nodes
    if (source_nodes.empty()) {
        vector<string> nodes = g.nodes();
        for (const auto& node : nodes) {
            if (node[1] == 'S' && checking_edge(g, node, '\0')) {
                source_nodes.push_back(node);
            }
        }
    }
    
    if (out_nodes.empty()) {
        vector<string> nodes = g.nodes();
        for (const auto& node : nodes) {
            if (node[1] == 'D' && checking_edge(g, node, '\0')) {
                out_nodes.push_back(node);
            }
        }
    }
    
    return make_pair(source_nodes, out_nodes);
}

// Final implementation of graph_utils.cpp

pair<Graph, string> create_graph(Graph& g, const vector<string>& q, int i, const string& expression, int mode) {
    string end_node;
    vector<string> inter_arr;
    int t = i - 1;
    string expre = expression;
    
    // Find intersecting expressions
    while (t >= 0) {
        string element = q[t];
        string inter = intersection_expressions(expre, element);
        if (!inter.empty()) {
            for (char c : inter) {
                if (isalpha(c)) {
                    inter_arr.push_back(string(1, c));
                }
            }
            inter_arr.push_back("0");
        }
        string remain = subtract_expression(expre, element);
        if (!remain.empty()) {
            expre = remain;
        }
        t--;
    }

    if (expre == expression) {
        // Create nodes for basic expression
        string node1, node2;
        char op;
        bool first_alpha = true;
        
        for (char token : expression) {
            if (isalpha(token)) {
                create_node(g, string(1, token));
                if (first_alpha) {
                    node1 = string(1, token);
                    first_alpha = false;
                } else {
                    node2 = string(1, token);
                }
            } else if (token == '+' || token == '*') {
                op = token;
            }
        }

        // Add edges based on operator
        if (precedence(op) == 1) { // Parallel
            add_edge_parallel_1(g, node1, node2);
        } else { // Serial
            add_edge_serial_1(g, node1, node2, inter_arr, mode);
        }
    } else {
        // Handle complex expressions
        string node;
        char op;
        
        for (char token : expre) {
            if (isalpha(token)) {
                node = string(1, token);
                create_node(g, node);
            } else if (token == '+' || token == '*') {
                op = token;
            }
        }

        if (precedence(op) == 1) { // Parallel
            if (!node.empty()) {
                add_edge_parallel_2(g, node, inter_arr);
            } else {
                add_edge_parallel_3(g, inter_arr, mode);
            }
        } else { // Serial
            if (!node.empty()) {
                add_edge_serial_2(g, node, inter_arr, mode);
            } else {
                add_edge_serial_3(g, inter_arr, mode);
            }
        }
        end_node = node;
    }
    
    return make_pair(g, end_node);
}

void add_edge_parallel_2(Graph& g, const string& node, const vector<string>& inter_arr) {
    string n1 = node + "S";
    string n2 = node + "D";
    string outside_node;
    
    // Find an outside node
    vector<string> nodes = g.nodes();
    for (const auto& n : nodes) {
        string node_char = string(1, n[0]);
        bool found = false;
        for (const auto& inter : inter_arr) {
            if (inter == "0") continue;
            if (inter == node_char) {
                found = true;
                break;
            }
        }
        if (!found && node_char != node) {
            outside_node = node_char;
            break;
        }
    }

    if (outside_node.empty()) return;

    // Find lowest degree nodes
    string node1 = lowest_degree(g, 'S', node, node, outside_node);
    string node2 = lowest_degree(g, 'D', node, node, outside_node);
    
    int node1_degree = g.degree(node1);
    int node2_degree = g.degree(node2);

    if (node1_degree < node2_degree) {
        g.addEdge(n1, node1);
        string node_connect = lowest_degree(g, 'D', node, string(1, node1[0]), outside_node);
        g.addEdge(n2, node_connect);
    } else {
        g.addEdge(n2, node2);
        string node_connect = lowest_degree(g, 'S', node, string(1, node2[0]), outside_node);
        g.addEdge(n1, node_connect);
    }
}

void add_edge_parallel_3(Graph& g, const vector<string>& inter_arr, int mode) {
    int i = 0;
    pair<string, int> n1_info = lowest_degree_arr_node(g, 'S', i, inter_arr, "");
    string n1 = n1_info.first;
    int n1_degree = n1_info.second;
    
    pair<string, int> n2_info = lowest_degree_arr_node(g, 'S', i, inter_arr, "");
    string n2 = n2_info.first;
    int n2_degree = n2_info.second;
    
    pair<string, int> n3_info = lowest_degree_arr_node(g, 'D', i, inter_arr, "");
    string n3 = n3_info.first;
    int n3_degree = n3_info.second;
    
    pair<string, int> n4_info = lowest_degree_arr_node(g, 'D', i, inter_arr, "");
    string n4 = n4_info.first;
    int n4_degree = n4_info.second;

    int sel = 3;
    if (n1_degree + n2_degree < n3_degree + n4_degree) {
        if ((checking_parallel_connected(g, "S", inter_arr) && mode == 1) || mode == 0) {
            sel = 0;
            g.addEdge(n1, n2);
        }
    } else {
        if ((checking_parallel_connected(g, "D", inter_arr) && mode == 1) || mode == 0) {
            sel = 1;
            g.addEdge(n3, n4);
        }
    }

    if (sel == 1) {
        string except_node = string(1, n4[0]);
        pair<string, int> node_connect_info = lowest_degree_arr_node(g, 'S', i, inter_arr, except_node);
        g.addEdge(n1, node_connect_info.first);
    } else if (sel == 2) {
        string except_node = string(1, n2[0]);
        pair<string, int> node_connect_info = lowest_degree_arr_node(g, 'D', i, inter_arr, except_node);
        g.addEdge(n3, node_connect_info.first);
    }
}

void add_edge_serial_2(Graph& g, const string& node, const vector<string>& inter_arr, int mode) {
    string n1 = node + "S";
    string n2 = node + "D";
    
    int i = 0;
    pair<string, int> node_connect1_info = lowest_degree_arr_node(g, 'D', i, inter_arr, "");
    string node_connect1 = node_connect1_info.first;
    
    i = 0;
    pair<string, int> node_connect2_info = lowest_degree_arr_node(g, 'S', i, inter_arr, "");
    string node_connect2 = node_connect2_info.first;

    if (mode == 0) {
        g.addEdge(n1, node_connect1);
        
        vector<string> nodes = g.nodes();
        for (const auto& node : nodes) {
            if (node[0] == node_connect1[0]) continue;
            if (g.hasEdge(node_connect1, node) && node[1] == 'D') {
                g.addEdge(n1, node);
            }
        }
    } else if (mode == 1) {
        if (check_serial_connected(g, node, inter_arr)) {
            g.addEdge(n2, node_connect2);
        }
    }
}

void add_edge_serial_3(Graph& g, const vector<string>& inter_arr, int mode) {
    int i = 0;
    pair<string, int> n1_info = lowest_degree_arr_node(g, 'S', i, inter_arr, "");
    string n1 = n1_info.first;
    
    pair<string, int> n2_info = lowest_degree_arr_node(g, 'D', i, inter_arr, string(1, n1[0]));
    string n2 = n2_info.first;

    if (mode == 0) {
        g.addEdge(n1, n2);
        
        vector<string> nodes = g.nodes();
        for (const auto& node : nodes) {
            if (g.hasEdge(node, n1) && node[1] == 'S') {
                g.addEdge(node, n2);
            }
            if (g.hasEdge(node, n2) && node[1] == 'D') {
                g.addEdge(node, n1);
            }
        }
    } else if (mode == 1) {
        if (check_serial_connected(g, "", inter_arr)) {
            g.addEdge(n1, n2);
        }
    }
}