import networkx as nx
from itertools import combinations
from draw import draw_stick_diagram, createLogicElement

class LogicCircuit:
    def __init__(self, expression):
        self.expression = expression
        self.g_nmos = nx.Graph()
        self.g_pmos = nx.Graph()
        self.q_nmos = []
        self.q_pmos = []
        self.euler_path_nmos = []
        self.euler_path_pmos = []
        self.source_nodes_nmos = []
        self.out_nodes_nmos = []
        self.source_nodes_pmos = []
        self.out_nodes_pmos = []
        self.serial_array_pmos = []
        self.parallel_array_pmos = []
        self.end_node_nmos = ''

    def operator_precedence(self, op):
        return {'+': 1, '*': 2}.get(op, 0)

    def evaluate_expression(self, expr=None, inverse=False):
        expr = expr or self.expression
        q = self.q_pmos if inverse else self.q_nmos
        operand_stack = []
        operator_stack = []
        i = 0
        
        while i < len(expr):
            token = expr[i]
            if token.isalpha():
                operand_stack.append(token)
                i += 1
            elif token in '+*':
                while (operator_stack and 
                       self.operator_precedence(operator_stack[-1]) >= self.operator_precedence(token)):
                    op = operator_stack.pop()
                    b = operand_stack.pop()
                    a = operand_stack.pop()
                    res = self.apply_operand(a, b, op, q, inverse)
                    operand_stack.append(res)
                operator_stack.append(token)
                i += 1
            elif token == '(':
                operator_stack.append(token)
                i += 1
            elif token == ')':
                while operator_stack[-1] != '(':
                    op = operator_stack.pop()
                    b = operand_stack.pop()
                    a = operand_stack.pop()
                    res = self.apply_operand(a, b, op, q, inverse)
                    operand_stack.append(res)
                operator_stack.pop()
                i += 1
            else:
                i += 1

        while operator_stack:
            op = operator_stack.pop()
            b = operand_stack.pop()
            a = operand_stack.pop()
            res = self.apply_operand(a, b, op, q, inverse)
            operand_stack.append(res)

        return operand_stack.pop()

    def apply_operand(self, a, b, op, q, inverse=False):
        if inverse:
            op = '*' if op == '+' else '+'
        expr = f"{a}{op}{b}"
        q.append(expr)
        return expr

    def sub_expression(self, expr1, expr2):
        i = j = 0
        result = []
        while i < len(expr1) and j < len(expr2):
            if expr1[i] == expr2[j]:
                i += 1
                j += 1
            else:
                result.append(expr1[i])
                i += 1
        result.extend(expr1[i:])
        return ''.join(result)

    def intersection_expression(self, expr1, expr2):
        result = []
        i = j = 0
        while i < len(expr1) and j < len(expr2):
            if expr1[i] == expr2[j]:
                result.append(expr1[i])
                i += 1
                j += 1
            else:
                i += 1
        return ''.join(result)

    def create_node(self, g, node):
        node_s = node + 'S'
        node_d = node + 'D'
        g.add_node(node_s)
        g.add_node(node_d)
        g.add_edge(node_s, node_d)

    def parallel_edge_1(self, g, node1, node2):
        n1_s = node1 + 'S'
        n1_d = node1 + 'D'
        n2_s = node2 + 'S'
        n2_d = node2 + 'D'
        g.add_edge(n1_s, n2_s)
        g.add_edge(n1_d, n2_d)

    def serial_edge_1(self, g, node1, node2, inter_arr, mode):
        n1_s = node1 + 'S'
        n1_d = node1 + 'D'
        n2_s = node2 + 'S'
        n2_d = node2 + 'D'
        
        if mode == 0:  # NMOS
            g.add_edge(n2_s, n1_d)
        elif mode == 1:  # PMOS with check
            if self.check_serial(g, ' ', [node1, 0, node2, 0]):
                g.add_edge(n2_s, n1_d)

    def check_serial(self, g, token, inter_arr):
        if not inter_arr:
            return True
        
        arr1 = []
        arr2 = []
        i = 0
        
        while i < len(inter_arr):
            if inter_arr[i] == 0:
                i += 1
                break
            arr1.append(inter_arr[i])
            i += 1
            
        while i < len(inter_arr):
            if inter_arr[i] == 0:
                break
            arr2.append(inter_arr[i])
            i += 1
            
        if not arr2:
            n1_s = token + 'S'
            n1_d = token + 'D'
            for node in arr1:
                n2_s = node + 'S'
                n2_d = node + 'D'
                if (n1_s, n2_d) in g.edges() or (n1_d, n2_s) in g.edges():
                    return False
            return True
        else:
            for node1 in arr1:
                n1_s = node1 + 'S'
                n1_d = node1 + 'D'
                for node2 in arr2:
                    n2_s = node2 + 'S'
                    n2_d = node2 + 'D'
                    if (n1_s, n2_d) in g.edges() or (n1_d, n2_s) in g.edges():
                        return False
            return True

    def check_parallel(self, g, k, inter_arr):
        if not inter_arr:
            return True
            
        arr1 = []
        arr2 = []
        i = 0
        j = 0
        
        while True:
            if inter_arr[i] == 0:
                i += 1
                break
            arr1.append(inter_arr[i])
            i += 1
            
        while i < len(inter_arr):
            if inter_arr[i] == 0:
                break
            arr2.append(inter_arr[i])
            i += 1
            j += 1
            
        if not arr2:
            while i < len(arr1) - 1:
                n1 = arr1[i] + k
                j = i + 1
                while j < len(arr1):
                    n2 = arr1[j] + k
                    if (n1, n2) in g.edges():
                        return False
                    j += 1
                i += 1
            return True
        else:
            while i < len(arr1):
                n1 = arr1[i] + k
                j = 0
                while j < len(arr2):
                    n2 = arr2[j] + k
                    if (n1, n2) in g.edges():
                        return False
                    j += 1
                i += 1
            return True

    def create_graph(self, g, q, i, expression, mode):
        end_node = ''
        inter_arr = []
        t = i - 1
        expre = expression
        
        while t >= 0:
            element = q[t]
            inter = self.intersection_expression(expre, element)
            if len(inter) > 0:
                for char in inter:
                    if char.isalpha():
                        inter_arr.append(char)
                inter_arr.append(0)
            remain = self.sub_expression(expre, element)
            if len(remain) > 0:
                expre = remain
            t -= 1
            
        if expre == expression:
            sel = 0
            for token in expression:
                if token.isalpha():
                    self.create_node(g, token)
                    if sel == 0:
                        sel = 1
                        node1 = token
                    else:
                        node2 = token
                elif token in '+*':
                    operator = self.operator_precedence(token)
                    
            if operator == 1:
                self.parallel_edge_1(g, node1, node2)
            else:
                self.serial_edge_1(g, node1, node2, inter_arr, mode)
        else:
            node = ''
            for token in expre:
                if token in '+*':
                    operator = self.operator_precedence(token)
                elif token.isalpha():
                    node = token
                    self.create_node(g, token)
                    
            if operator == 1:
                if len(node) > 0:
                    self.parallel_edge_2(g, node, inter_arr)
                else:
                    self.parallel_edge_3(g, inter_arr, mode)
            else:
                if len(node):
                    self.serial_edge_2(g, node, inter_arr, mode)
                else:
                    self.serial_edge_3(g, inter_arr, mode)
            end_node = node
            
        return g, end_node

    def parallel_edge_2(self, g, node, inter_arr):
        n1 = node + 'S'
        n2 = node + 'D'
        outside_node = ''
        
        for n in g.nodes():
            n_char = n[0]
            if n_char not in inter_arr and n_char != node:
                outside_node = n_char
                break
                
        node1 = self.lowest_degree(g, 'S', node, node, outside_node)
        node2 = self.lowest_degree(g, 'D', node, node, outside_node)
        node1_degree = g.degree(node1)
        node2_degree = g.degree(node2)
        
        if node1_degree < node2_degree:
            s = 1
            g.add_edge(n1, node1)
        else:
            s = 2
            g.add_edge(n2, node2)
            
        if s == 1:
            node1_char = node1[0]
            node_connect = self.lowest_degree(g, 'D', node, node1_char, outside_node)
            g.add_edge(n2, node_connect)
        elif s == 2:
            node2_char = node2[0]
            node_connect = self.lowest_degree(g, 'S', node, node2_char, outside_node)
            g.add_edge(n1, node_connect)

    def parallel_edge_3(self, g, inter_arr, mode):
        i = 0
        j = 0
        n1, n1_degree, i = self.lowest_degree_node(g, 'S', i, inter_arr, '')
        t1 = i
        n2, n2_degree, i = self.lowest_degree_node(g, 'S', i, inter_arr, '')
        n3, n3_degree, j = self.lowest_degree_node(g, 'D', j, inter_arr, '')
        n4, n4_degree, j = self.lowest_degree_node(g, 'D', j, inter_arr, '')
        sel = 3
        
        if n1_degree + n2_degree < n3_degree + n4_degree:
            if self.check_parallel(g, 'S', inter_arr) and mode == 1:
                sel = 0
                g.add_edge(n1, n2)
            elif mode == 0:
                sel = 0
                g.add_edge(n1, n2)
        else:
            if self.check_parallel(g, 'D', inter_arr) and mode == 1:
                sel = 1
                g.add_edge(n3, n4)
            elif mode == 0:
                sel = 1
                g.add_edge(n3, n4)
                
        if sel == 1:
            except_node = n4[0]
            node_connect, _, _ = self.lowest_degree_node(g, 'S', t1, inter_arr, except_node)
            g.add_edge(n1, node_connect)
        elif sel == 2:
            except_node = n2[0]
            node_connect, _, _ = self.lowest_degree_node(g, 'D', t1, inter_arr, except_node)
            g.add_edge(n3, node_connect)

    def serial_edge_2(self, g, node, inter_arr, mode):
        n1 = node + 'S'
        n2 = node + 'D'
        i = j = 0
        node_connect1, _, i = self.lowest_degree_node(g, 'D', i, inter_arr, '')
        node_connect2, _, j = self.lowest_degree_node(g, 'S', j, inter_arr, '')
        
        if mode == 0:
            g.add_edge(n1, node_connect1)
            for n in g.nodes():
                if n[0] == node_connect1[0]:
                    continue
                if (node_connect1, n) in g.edges() and n[1] == 'D':
                    g.add_edge(n1, n)
        elif mode == 1:
            if self.check_serial(g, node, inter_arr):
                g.add_edge(n2, node_connect2)

    def serial_edge_3(self, g, inter_arr, mode):
        i = 0
        n1, _, i = self.lowest_degree_node(g, 'S', i, inter_arr, '')
        n2, _, i = self.lowest_degree_node(g, 'D', i, inter_arr, n1[0])
        
        if mode == 0:
            g.add_edge(n1, n2)
            for node in g.nodes():
                if (node, n1) in g.edges() and node[1] == 'S':
                    g.add_edge(node, n2)
                if (node, n2) in g.edges() and node[1] == 'D':
                    g.add_edge(node, n1)
        elif mode == 1:
            if self.check_serial(g, '', inter_arr):
                g.add_edge(n1, n2)

    def lowest_degree_node(self, g, k, i, inter_arr, except_node):
        t = i
        min_degree = 100
        min_node = None
        
        while True:
            if t >= len(inter_arr) or inter_arr[t] == 0:
                t += 1
                break
            node = inter_arr[t] + k
            degree = g.degree(node)
            if degree < min_degree and (not except_node or node[0] != except_node):
                min_node = node
                min_degree = degree
            t += 1
            
        return min_node, min_degree, t

    def lowest_degree(self, g, k, except_node1, except_node2, except_node3):
        degrees = dict(g.degree())
        
        if except_node1:
            degrees.pop(except_node1 + 'S', None)
            degrees.pop(except_node1 + 'D', None)
        if except_node2:
            degrees.pop(except_node2 + 'S', None)
            degrees.pop(except_node2 + 'D', None)
        if except_node3:
            degrees.pop(except_node3 + 'S', None)
            degrees.pop(except_node3 + 'D', None)
            
        filtered_degrees = {node: degree for node, degree in degrees.items() if node[-1] == k}
        if not filtered_degrees:
            return None
        return min(filtered_degrees, key=degrees.get)

    def create_nmos_graph(self):
        self.q_nmos = []
        self.evaluate_expression()
        i = 0
        self.end_node_nmos = ''
        
        while i < len(self.q_nmos):
            self.g_nmos, self.end_node_nmos = self.create_graph(
                self.g_nmos, self.q_nmos, i, self.q_nmos[i], 0
            )
            i += 1

    def create_pmos_graph(self):
        self.q_pmos = []
        self.evaluate_expression(inverse=True)
        i = 0
        
        while i < len(self.euler_path_pmos):
            n1 = self.euler_path_pmos[i]
            self.g_pmos.add_node(n1)
            if i != 0:
                n2 = self.euler_path_pmos[i - 1]
                self.g_pmos.add_edge(n1, n2)
            i += 1
            
        i = 0
        while i < len(self.q_pmos):
            self.create_graph(self.g_pmos, self.q_pmos, i, self.q_pmos[i], 1)
            i += 1

    def is_valid_next_node(self, v, path, g):
        if v in path:
            return False
            
        last_node = path[-1]
        if last_node[0] != v[0]:
            if last_node[1] == 'S':
                x = last_node[0] + 'D'
                if x in path:
                    return True
                return False
            elif last_node[1] == 'D':
                x = last_node[0] + 'S'
                if x in path:
                    return True
                return False
                
        if not path or v in g.neighbors(path[-1]):
            return True
        return False

    def hamilton_dfs(self, g, start, end_node=None, path=None):
        if path is None:
            path = []
        path = path + [start]
        
        if len(path) == len(g.nodes()):
            if end_node and (path[0][0] != end_node and path[-1][0] != end_node):
                return None
            return path
            
        for v in g.neighbors(start):
            if self.is_valid_next_node(v, path, g):
                new_path = self.hamilton_dfs(g, v, end_node, path)
                if new_path:
                    return new_path
        return None

    def find_hamilton(self, g, end_node=None):
        path = []
        
        # Try nodes ending with 'D' first
        for node in g.nodes():
            if node[1] == 'D':
                path = self.hamilton_dfs(g, node, end_node)
                if path:
                    break
                    
        if not path:
            # Try nodes ending with 'S' if no path found
            for node in g.nodes():
                if node[1] == 'S':
                    path = self.hamilton_dfs(g, node, end_node)
                    if path:
                        break
                        
        return path

    def euler_path(self):
        self.euler_path_nmos = self.find_hamilton(self.g_nmos, self.end_node_nmos)
        if not self.euler_path_nmos:
            return None
            
        self.euler_path_pmos = [None] * len(self.euler_path_nmos)
        i = 0
        s = False
        
        while i < len(self.euler_path_nmos) - 1:
            if s:
                self.euler_path_pmos[i] = self.euler_path_nmos[i+1]
                self.euler_path_pmos[i+1] = self.euler_path_nmos[i]
            else:
                self.euler_path_pmos[i] = self.euler_path_nmos[i]
                self.euler_path_pmos[i+1] = self.euler_path_nmos[i+1]
            s = not s
            i += 2

    def filter_edge_pmos(self):
        check_serial = []
        check_parallel = []
        i = 0
        
        while i < len(self.euler_path_pmos):
            n1 = self.euler_path_pmos[i]
            if i != 0:
                n2 = self.euler_path_pmos[i - 1]
                if n1[0] != n2[0] and n1[1] != n2[1]:
                    check_serial.append(n1[0] + n2[0])
                    check_serial.append(n2[0] + n1[0])
                if n1[0] != n2[0] and n1[1] == n2[1]:
                    check_parallel.append(n1[0] + n2[0] + n1[1])
                    check_parallel.append(n2[0] + n1[0] + n1[1])
            i += 1
            
        edges_to_remove = []
        edges_to_add = []
        
        for edge in list(self.g_pmos.edges()):
            n1 = edge[0][0]
            n2 = edge[1][0]
            if n1 == n2:
                continue
                
            n3 = edge[0][1]
            n4 = edge[1][1]
            
            if n3 != n4:
                node1 = n1 + n2
                node2 = n2 + n1
                s = 0
                
                if ((node1 in self.serial_array_pmos or node2 in self.serial_array_pmos) and 
                    (node1 not in check_serial and node2 not in check_serial)):
                    
                    if (n1 + 'S', n2 + 'D') in self.g_pmos.edges():
                        edges_to_remove.append((n1 + 'S', n2 + 'D'))
                        s = 1
                    if (n1 + 'D', n2 + 'S') in self.g_pmos.edges():
                        edges_to_remove.append((n1 + 'D', n2 + 'S'))
                        s = 2
                        
                    if s == 1:
                        for node in self.g_pmos.nodes():
                            if (node, n2 + 'D') in self.g_pmos.edges() and node[1] == 'S':
                                edges_to_add.append((n1 + 'S', node[0] + 'D'))
                                break
                            if (node, n1 + 'D') in self.g_pmos.edges() and node[1] == 'S':
                                edges_to_add.append((n2 + 'S', node[0] + 'D'))
                                break
                    elif s == 2:
                        for node in self.g_pmos.nodes():
                            if (node, n2 + 'S') in self.g_pmos.edges() and node[1] == 'D':
                                edges_to_add.append((n1 + 'D', node[0] + 'S'))
                                break
                            if (node, n1 + 'S') in self.g_pmos.edges() and node[1] == 'D':
                                edges_to_add.append((n2 + 'D', node[0] + 'S'))
                                break
            else:
                node1 = n1 + n2
                node2 = n2 + n1
                
                if node1 not in self.parallel_array_pmos and node2 not in self.parallel_array_pmos:
                    for n in check_parallel:
                        if node1 != n[0] + n[1] and node2 != n[0] + n[1]:
                            if n3 == n[2]:
                                if (n1 + n[2], n2 + n[2]) in self.g_pmos.edges():
                                    edges_to_remove.append((n1 + n[2], n2 + n[2]))
        
        for edge in edges_to_remove:
            if edge in self.g_pmos.edges():
                self.g_pmos.remove_edge(*edge)
                
        for edge in edges_to_add:
            self.g_pmos.add_edge(*edge)

    def check_edge(self, g, full_node, char_connected=''):
        for node in g.nodes():
            if node[0] == full_node[0]:
                continue
            if not char_connected:
                if (full_node, node) in g.edges():
                    return False
            else:
                if node[1] == char_connected and (full_node, node) in g.edges():
                    return False
        return True

    def find_nodes(self, g):
        source_nodes = []
        out_nodes = []
        
        # First pass: find source and output nodes from edges
        for edge in g.edges():
            if edge[0][0] == edge[1][0]:
                continue
            if edge[0][1] == edge[1][1]:
                if edge[0][1] == 'S':
                    source_nodes.append((edge[0][0], edge[1][0]))
                else:
                    out_nodes.append((edge[0][0], edge[1][0]))
                    
        # Process source nodes
        if source_nodes:
            temp1 = []
            for pair in source_nodes:
                n1, n2 = pair
                n1_s = n1 + 'S'
                n2_s = n2 + 'S'
                if (self.check_edge(g, n1_s, 'D') and self.check_edge(g, n2_s, 'D')):
                    temp1.append(n1_s)
                    temp1.append(n2_s)
            source_nodes = temp1
            
        # Process output nodes
        if out_nodes:
            temp2 = []
            for pair in out_nodes:
                n1, n2 = pair
                n1_d = n1 + 'D'
                n2_d = n2 + 'D'
                if (self.check_edge(g, n1_d, 'S') and self.check_edge(g, n2_d, 'S')):
                    temp2.append(n1_d)
                    temp2.append(n2_d)
            out_nodes = temp2
            
        # Fallback if no nodes found
        if not source_nodes:
            for node in g.nodes():
                if node[1] == 'S' and self.check_edge(g, node):
                    source_nodes.append(node)
                    
        if not out_nodes:
            for node in g.nodes():
                if node[1] == 'D' and self.check_edge(g, node):
                    out_nodes.append(node)
                    
        return source_nodes, out_nodes

    def run(self):
        """Main execution flow"""
        # Create NMOS graph
        self.create_nmos_graph()
        
        # Find serial and parallel arrays for PMOS
        for edge in self.g_nmos.edges():
            n1 = edge[0][0]
            n2 = edge[1][0]
            if n1 == n2:
                continue
            n3 = edge[0][1]
            n4 = edge[1][1]
            if n3 == n4:
                self.serial_array_pmos.append(n1 + n2)
            else:
                self.parallel_array_pmos.append(n1 + n2)
                
        # Find Euler paths
        self.euler_path()
        
        # Create PMOS graph
        self.create_pmos_graph()
        
        # Filter PMOS edges
        self.filter_edge_pmos()
        
        # Find source and output nodes
        self.source_nodes_nmos, self.out_nodes_nmos = self.find_nodes(self.g_nmos)
        self.source_nodes_pmos, self.out_nodes_pmos = self.find_nodes(self.g_pmos)

    def display_info(self):
        """Display circuit information and draw stick diagram"""
        print("Euler path PMOS:", self.euler_path_pmos)
        print("Euler path NMOS:", self.euler_path_nmos)
        print("PMOS edges:", list(self.g_pmos.edges()))
        print("NMOS edges:", list(self.g_nmos.edges()))
        print("Source nodes PMOS (VCC):", self.source_nodes_pmos)
        print("Source nodes NMOS (GND):", self.source_nodes_nmos)
        print("Output nodes PMOS (OUT):", self.out_nodes_pmos)
        print("Output nodes NMOS (OUT):", self.out_nodes_nmos)
        
        logic_elements = createLogicElement(self.euler_path_nmos)
        draw_stick_diagram(
            self.g_nmos, self.g_pmos,
            self.euler_path_nmos, self.euler_path_pmos,
            self.source_nodes_pmos, self.source_nodes_nmos,
            self.out_nodes_pmos, self.out_nodes_nmos,
            logic_elements
        )

if __name__ == '__main__':
    expression = input("Enter Boolean Expression: ")
    circuit = LogicCircuit(expression)
    circuit.run()
    circuit.display_info()
