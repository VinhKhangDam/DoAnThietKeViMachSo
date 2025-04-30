import networkx as nx

#function: hỗ trợ xử lí biểu thức

#OperatorPrecedence: Xác định độ ưu tiên của biểu thức 
def OperatorPrecedence(operator):
    if operator == '+':
        return 1
    elif operator == '*':
        return 2
    else:
        return 0

def ApplyForOperand(operand1, operand2, operator, q):
    expression = str(operand1) + str(operator) + str(operand2)
    #q.append(expression)
    if operator == '+':
        return str(operand1) + str(operator) + str(operand2)
    else: return str(operand1) + str(operator) + str(operand2)

def ApplyForOperand_inv(operand1, operand2, operator):
    expression = str(operand1) + str(operator) + str(operand2)
    #q.append(expression)
    if operator == '+':
        return str(operand1) + '*' + str(operand2)
    else: return str(operand1) + '+' + str(operand2)


def evaluate_expression_inv(expression, q):
    operand_stack = []
    operator_stack = []
    index = 0

    while index < len(expression):
        token = expression[index]
        if token.isalpha():
            operand_stack.append((token))
            index += 1
        elif token in '+-*/^':
            while (len(operator_stack) != 0 and OperatorPrecedence(operator_stack[-1]) >= OperatorPrecedence(token)):
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = ApplyForOperand_inv(operand1, operand2, operator)
                q.append(result)
                operand_stack.append(result)
            operator_stack.append(token)
            index += 1
        elif token == '(':
            operator_stack.append(token)
            index += 1
        elif token == ')':
            while operator_stack[-1] != '(':
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = ApplyForOperand_inv(operand1, operand2, operator)
                q.append(result)
                operand_stack.append(result)
            operator_stack.pop()  
            index += 1
        else:
            index += 1

    while len(operator_stack) != 0:
        operator = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = ApplyForOperand_inv(operand1, operand2, operator)
        q.append(result)
        operand_stack.append(result)

    return operand_stack.pop()

def evaluate_expression(expression, q):
    operand_stack = []
    operator_stack = []
    index = 0

    while index < len(expression):
        token = expression[index]
        if token.isalpha():
            operand_stack.append((token))
            index += 1
        elif token in '+-*/^':
            while (len(operator_stack) != 0 and OperatorPrecedence(operator_stack[-1]) >= OperatorPrecedence(token)):
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = ApplyForOperand(operand1, operand2, operator, q)
                q.append(result)
                operand_stack.append(result)
            operator_stack.append(token)
            index += 1
        elif token == '(':
            operator_stack.append(token)
            index += 1
        elif token == ')':
            while operator_stack[-1] != '(':
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = ApplyForOperand(operand1, operand2, operator, q)
                q.append(result)
                operand_stack.append(result)
            operator_stack.pop()  
            index += 1
        else:
            
            index += 1

    while len(operator_stack) != 0:
        operator = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = ApplyForOperand(operand1, operand2, operator, q)
        q.append(result)
        operand_stack.append(result)

    return operand_stack.pop()

def subtract_expressions(expression1, expression2):
    i = 0
    j = 0
    result = ''
    while i < len(expression1):
        if(expression1[i] != expression2[j]):
            result += expression1[i]
            i += 1
        else:
            i += 1
            j += 1
        if j == len(expression2): break
    while i < len(expression1):
        result += expression1[i]
        i += 1
    
    return result
def intersection_expressions(expression1, expression2):
    i = 0
    j = 0
    result =''
    while i < len(expression1):
        if(expression1[i] == expression2[j]):
            result += expression1[i]
            i += 1
            j += 1
        else: i += 1
        if j == len(expression2): break
#    if not result: return 0
    return result

def check_serial_connected(g, token, inter_arr):
    if len(inter_arr) == 0:
        return True
    arr1 = [0] * len(inter_arr)
    arr2 = [0] * len(inter_arr)
    i = 0
    j = 0
    while(1):
        if inter_arr[i] == 0:
            i += 1
            break
        arr1[i] = inter_arr[i]
        i += 1
    while i < len(inter_arr):
        if inter_arr[i] == 0:
            break;
        arr2[j] = inter_arr[i]
        i += 1
        j += 1
    i = 0
    j = 0
    if arr2[0] == 0:
        n1_s = token + 'S'
        n1_d = token + 'D'
        while i < len(arr1) - 1:
            if arr1[i] == 0: break
            n2_s = arr1[i] + 'S'
            n2_d = arr1[i] + 'D'
            if(n1_s, n2_d) in g.edges():
                return False
            if(n1_d, n2_s) in g.edges():
                return False
            i += 1
        return True
    else:
        while i < len(arr1):
            if arr1[i] == 0: break
            n1_s = arr1[i] + 'S'
            n1_d = arr1[i] + 'D'
            j = 0
            while j < len(arr2):
                if arr2[j] == 0:
                    break
                n2_s = arr2[j] + 'S'
                n2_d = arr2[j] + 'D'
                if (n1_s, n2_d) in g.edges():
                    return False
                if(n1_d, n2_s) in g.edges():
                    return False
                j += 1
            i += 1
        return True
    
def checking_parallel_connected(g, k, inter_arr):
    if len(inter_arr) == 0:
        return True
    arr1 = []
    arr2 = []
    i = 0
    j = 0
    while(1):
        if inter_arr[i] == 0:
            i += 1
            break
        arr1.append(inter_arr[i])
        i += 1
    while i < len(inter_arr):
        if inter_arr[i] == 0: break
        arr2.append(inter_arr[i])
        i += 1
        j += 1
    i = 0
    j = 0
    if len(arr2) == 0:
        while i < len(arr1) - 1:
            n1 = arr1[i] + k
            j = i + 1
            while j < len(arr1):
                n2 = arr1[j] + k
                if(n1, n2) in g.edges():
                    return False
                j += 1
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
def create_node(g, node):
    node1 = node + 'S'
    node2 = node + 'D'
    g.add_node(node1)
    g.add_node(node2)
    g.add_edge(node1, node2)


def add_edge_parallel_1(g, node1, node2):
    n1 = node1 + 'S'
    n2 = node1 + 'D'
    n3 = node2 + 'S'
    n4 = node2 + 'D'
    g.add_edge(n1, n3)
    g.add_edge(n2, n4)
    

def add_edge_serial_1(g, node1, node2, inter_arr, mode):
    n1 = node1 + 'S'
    n2 = node1 + 'D'
    n3 = node2 + 'S'
    n4 = node2 + 'D'
    if mode == 0:
        g.add_edge(n3, n2)
    elif mode == 1:
        arr = [node1, 0, node2, 0];
        if check_serial_connected(g, ' ',arr) == True:
            g.add_edge(n3, n2)

def add_edge_serial_2(g, node, inter_arr, mode):
    n1 = node + 'S'
    n2 = node + 'D'
    i = j = 0
    node_connect1, node_degree1, i = lowest_degree_arr_node(g, 'D', i, inter_arr, '')
    node_connect2, node_degree2, j = lowest_degree_arr_node(g, 'S', j, inter_arr, '')
    if mode == 0:
        g.add_edge(n1, node_connect1)
        for node in g.nodes():
            if node[0] == node_connect1[0]: continue
            if (node_connect1, node) in g.edges() and node[1] == 'D':
                g.add_edge(n1, node)
    elif mode == 1:
        if check_serial_connected(g, node, inter_arr) == True:
            g.add_edge(n2, node_connect2)



def add_edge_parallel_2(g, node, inter_arr):
    n1 = node + 'S'
    n2 = node + 'D'
    outside_node = ''
    for n in g.nodes():
        n = n[0]
        if n not in inter_arr and n != node:
            outside_node = n
            break
    node1 = lowest_degree(g, 'S', node, node, outside_node)
    node2 = lowest_degree(g, 'D', node, node, outside_node)
    node1_degree = g.degree(node1)
    node2_degree = g.degree(node2)
    if node1_degree < node2_degree:
        s = 1
        g.add_edge(n1, node1)
    else:
        s = 2
        g.add_edge(n2, node2)
    if s == 1:
        node1 = node1[0]
        node_connect = lowest_degree(g, 'D', node, node1, outside_node)
        g.add_edge(n2, node_connect)
    elif s == 2:
        node2 = node2[0]
        node_connect = lowest_degree(g, 'S', node, node2, outside_node)
        g.add_edge(n1, node_connect)

def add_edge_parallel_3(g, inter_arr, mode):
    i = 0
    j = 0
    n1 = n2 = n3 = n4 = ''
    n1_degree = n2_degree = n3_degree = n4_degree = 0
    n1, n1_degree, i = lowest_degree_arr_node(g, 'S', i, inter_arr, '')
    t1 = i
    n2, n2_degree, i = lowest_degree_arr_node(g, 'S', i, inter_arr, '')
    n3, n3_degree, j = lowest_degree_arr_node(g, 'D', j, inter_arr, '')
    n4, n4_degree, j = lowest_degree_arr_node(g, 'D', j, inter_arr, '')
    sel = 3
    if n1_degree + n2_degree < n3_degree + n4_degree :
        if checking_parallel_connected(g, 'S', inter_arr) == True and mode == 1:
            sel = 0
            g.add_edge(n1, n2)      #S->S
        elif mode == 0:
            sel = 0
            g.add_edge(n1, n2)      #S->S
    else:
        if checking_parallel_connected(g, 'D', inter_arr) == True and mode == 1:
            sel = 1
            g.add_edge(n3, n4)      #D->D
        elif mode == 0:
            sel = 1
            g.add_edge(n3, n4)      #D->D
    if sel == 1 :   #connect S -> S
        except_node = n4[0]
        node_connect, node_degree, t1 = lowest_degree_arr_node(g, 'S', t1, inter_arr, except_node)
        g.add_edge(n1, node_connect)
    elif sel == 2:           #connect d->D
        except_node = n2[0]
        node_connect, node_degree, t1 = lowest_degree_arr_node(g, 'D', t1, inter_arr, except_node)
        g.add_edge(n3, node_connect)
    return

def add_edge_serial_3(g, inter_arr, mode):
    i = 0
    n1, n1_degree, i = lowest_degree_arr_node(g, 'S', i, inter_arr, '')
    n2 , n2_degree, i = lowest_degree_arr_node(g, 'D', i, inter_arr, n1)
    if mode == 0:
        g.add_edge(n1, n2)
        for node in g.nodes():
            if (node, n1) in g.edges() and node[1] == 'S':
                g.add_edge(node, n2)
            if (node, n2) in g.edges() and node[1] == 'D':
                g.add_edge(node, n1)
    elif mode == 1:
        if check_serial_connected(g, '', inter_arr) == True:
           g.add_edge(n1, n2) 
    

def lowest_degree_arr_node(g, k, i, inter_arr, except_node):
    t = i
    min_degree1 = 100
    min_degree2 = 100
    while 1:
        if inter_arr[t] == 0:
            t += 1
            break
        n1_degree = g.degree(inter_arr[t] + k)
        n1 = inter_arr[t] + k
        if (n1_degree < min_degree1) and (n1 != except_node):
            min_node1 = n1
            min_degree1 = n1_degree
        t += 1
    return min_node1, min_degree1, t

def lowest_degree(g, k, except_node1, except_node2, except_node3):
    degrees = dict(g.degree())
    if except_node1 != '':
        degrees.pop(except_node1 + 'S', None)
        degrees.pop(except_node1 + 'D', None)
    if except_node2 != '':
        degrees.pop(except_node2 + 'S', None)
        degrees.pop(except_node2 + 'D', None)
    if except_node3 != '':
        degrees.pop(except_node3 + 'S', None)
        degrees.pop(except_node3 + 'D', None)
    filtered_degrees = {node: degree for node, degree in degrees.items() if node[-1] == k}
    lowest_degree_node = min(filtered_degrees, key=degrees.get)
    return lowest_degree_node

def create_graph(g, q, i, expression, mode):
    end_node = ''
    inter_arr = []
    t = i - 1
    expre = expression
    while t >= 0:
        element = q[t]
        inter = intersection_expressions(expre, element)
        if len(inter) > 0:
            for char in inter:
                if char.isalpha():
                    inter_arr.append(char)
            inter_arr.append(0)
        remain = subtract_expressions(expre, element)
        if len(remain) > 0:
            expre = remain
        t -= 1
    if expre == expression:
        sel = 0
        for token in expression:
            if token.isalpha():
                create_node(g, token)
                if sel == 0:
                   sel = 1
                   node1 = token
                else:
                    node2 = token
                   
            elif token in '+*':
                operator = OperatorPrecedence(token)
                
        if operator == 1:
            add_edge_parallel_1(g, node1, node2)
        else:
            add_edge_serial_1(g, node1, node2, inter_arr, mode)

    else:
        node = ''
        for token in expre:
            
            if token in '+*':
                operator = OperatorPrecedence(token)
            elif token.isalpha():
                node = token
                create_node(g, token)
        if operator == 1:
            if len(node) > 0:
                add_edge_parallel_2(g, node, inter_arr)
            else:
                add_edge_parallel_3(g, inter_arr, mode)
        else:
            if len(node):
                add_edge_serial_2(g, node, inter_arr, mode)
            else:
                add_edge_serial_3(g, inter_arr, mode)
        end_node = node
    return g, end_node

def create_nmos(g, expression):
    q = []
    end_node = ''
    evaluate_expression(expression, q)
    i = 0
    while i < len(q):
        g, end_node = create_graph(g, q, i, q[i], 0)
        i += 1
    return g, end_node

def create_pmos(g, expression, euler_path):
    q = []
    evaluate_expression_inv(expression, q)
    i = 0
    while i < len(euler_path):
        n1 = euler_path[i]
        g.add_node(n1)
        if i != 0:
            n2 = euler_path[i - 1]
            g.add_edge(n1, n2)
        i += 1
    i = 0
    while i < len(q):
        create_graph(g, q, i, q[i], 1)
        i += 1
    return g

def is_valid_next_node(v, path, G):
    # Kiểm tra xem đỉnh v đã được thêm vào path chưa
    if v in path:
        return False
    #Kiểm tra các node S D có nằm cạnh nhau không
    last_node = path[-1]
    if last_node[0] != v[0] :
        if last_node[1] == 'S':
            x = last_node[0] + 'D'
            if x in path:
                return True
            else: return False
        if last_node[1] == 'D':
            x = last_node[0] + 'S'
            if x in path:
                return True
            else: return False

    # Kiểm tra xem đỉnh v có kề với đỉnh cuối cùng của path không
    if not path or v in G.neighbors(path[-1]):
        return True
    return False


def hamiltonian_dfs_endnode(G, start, end, path=[]):
    path = path + [start]
    if len(path) == len(G.nodes()):
        return path
    for v in G.neighbors(start):
        if is_valid_next_node(v, path, G):
            new_path = hamiltonian_dfs_endnode(G, v, end, path)
            if new_path:
                return new_path
    return None

def hamiltonian_dfs(G, start, path=[]):
    path = path + [start]
    if len(path) == len(G.nodes()):
        return path
    for v in G.neighbors(start):
        if is_valid_next_node(v, path, G):
            new_path = hamiltonian_dfs(G, v, path)
            if new_path:
                return new_path
    return None

def find_hamilton_path(g, end_node):
    path = []
    for node in g.nodes():
        if node[1] == 'S': continue
        if end_node != '':
            path = hamiltonian_dfs_endnode(g, node, end_node)
            if path:
                if (path[0][0] != end_node and path[-1][0] != end_node):
                    path = []
        else:  path = hamiltonian_dfs(g, node)
        if path :
            break
        path = []
    if path:
        return path
    else: 
        for node in g.nodes():
            if node[1] == 'D': continue
            if end_node != '':
                path = hamiltonian_dfs_endnode(g, node, end_node)
                if path:
                    if (path[0][0] != end_node and path[-1][0] != end_node):
                        path = []
            else:  path = hamiltonian_dfs(g, node)
            if path :
                break
            path = []
    return path
def euler_path(g, end_node):
    euler_path_nmos = find_hamilton_path(g, end_node)
    if not euler_path_nmos:
        return None
    euler_path_pmos = [None] * len(euler_path_nmos)
    i = 0
    s = False
    while i < len(euler_path_nmos) - 1:
        if s == True:
            euler_path_pmos[i] = euler_path_nmos[i+1]
            euler_path_pmos[i+1] = euler_path_nmos[i]
        else:
            euler_path_pmos[i] = euler_path_nmos[i]
            euler_path_pmos[i+1] = euler_path_nmos[i+1]
        s = not s
        i += 2
    return euler_path_nmos, euler_path_pmos

def filter_edge_pmos(g, arr1, arr2, euler_path):
    i = 0
    check_serial = []
    check_parallel = []
    while i < len(euler_path):
        n1 = euler_path[i]
        if i != 0:
            n2 = euler_path[i - 1]
            if n1[0] != n2[0] and n1[1] != n2[1]:
                check_serial.append(n1[0] + n2[0])
                check_serial.append(n2[0] + n1[0])
            if n1[0] != n2[0] and n1[1] == n2[1]:
                check_parallel.append(n1[0] + n2[0] + n1[1])
                check_parallel.append(n2[0] + n1[0] + n1[1])
        i += 1
    for edge in g.edges():
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
            if (node1 in arr1 or node2 in arr1) and (node1 not in check_serial or node2 not in check_serial):
                if (n1 + 'S', n2 + 'D') in g.edges:
                    g.remove_edge(n1 + 'S', n2 + 'D')
                    s = 1
                if (n1 + 'D', n2 + 'S') in g.edges:
                    g.remove_edge(n1 + 'D', n2 + 'S')
                    s = 2
                if s == 1:
                    s = 0
                    for node in g.nodes():
                        if (node, n2 + 'D') in g.edges() and node[1] == 'S':
                            g.add_edge(n1 + 'S', node[0] + 'D')
                            break
                        if (node, n1 + 'D') in g.edges() and node[1] == 'S':
                            g.add_edge(n2 + 'S', node[0] + 'D')
                            break
                elif s == 2:
                    s = 0
                    for node in g.nodes():
                        if (node, n2 + 'S') in g.edges() and node[1] == 'D':
                            g.add_edge(n1 + 'D', node[0] + 'S')
                            break
                        if (node, n1 + 'S') in g.edges() and node[1] == 'D':
                            g.add_edge(n2 + 'D', node[0] + 'S')
                            break
        else:
            node1 = n1 + n2
            node2 = n2 + n1
            if(node1 not in arr2 and node2 not in arr2):
                for n in check_parallel:
                    if node1 != n[0] + n[1] and node2 != n[0] + n[1]:
                        if n3 == n[2]:
                            if(n1 + n[2], n2 + n[2]) in g.edges():
                                g.remove_edge(n1 + n[2], n2 + n[2])
    return g

def checking_edge(g, full_node, char_connected):
    for node in g.nodes():
        if node[0] == full_node[0] : continue
        if char_connected == '':
            if(full_node, node) in g.edges():
                return False
        else:
            if node[1] == char_connected:
                if(full_node, node) in g.edges():
                    return False
    return True

def find_node_source_and_out(g):
    source_nodes = []
    out_nodes = []
    for edge in g.edges():
        if edge[0][0] == edge[1][0]: continue
        if edge[0][1] == edge[1][1]:
            if edge[0][1] == 'S':
                source_nodes.append((edge[0][0], edge[1][0]))
            else:
                out_nodes.append((edge[0][0], edge[1][0]))
    if len(source_nodes) > 0:
        temp1 = []
        for pair in source_nodes:
            temp1.append(pair)
        for pair in temp1:
            n1 = pair[0]
            n2 = pair[1]
            n1_s = n1 + 'S'
            n2_s = n2 + 'S'
            if checking_edge(g, n1_s, 'D') == False or checking_edge(g, n2_s, 'D') == False:
                source_nodes.remove((n1, n2))
        if len(source_nodes) > 0:
            temp1 = []
            i = 0
            j = len(source_nodes)
            while i < j:
                n1 = source_nodes[0][0]
                n2 = source_nodes[0][1]
                n1_s = n1 + 'S'
                n2_s = n2 + 'S'
                source_nodes.remove((n1, n2))
                temp1.append(n1_s)
                temp1.append(n2_s)
                i += 1
            source_nodes = temp1
    if len(out_nodes) > 0:
        temp2 = []
        for pair in out_nodes:
            temp2.append(pair)
        for pair in temp2:

            n1 = pair[0]
            n2 = pair[1]
            n1_d = n1 + 'D'
            n2_d = n2 + 'D'
            if checking_edge(g, n1_d, 'S') == False or checking_edge(g, n2_d, 'S') == False:
                out_nodes.remove((n1, n2))
        if len(out_nodes) > 0:
            temp2 = []
            i = 0
            j = len(out_nodes)
            while i < j:
                n1 = out_nodes[0][0]
                n2 = out_nodes[0][1]
                n1_s = n1 + 'D'
                n2_s = n2 + 'D'
                out_nodes.remove((n1, n2))
                temp2.append(n1_s)
                temp2.append(n2_s)
                i += 1
            out_nodes = temp2
    
    temp1 = []
    for node in source_nodes:
        temp1.append(node)

    for node in temp1:
        if checking_edge(g, node, '') == False:
            if node in source_nodes:
                source_nodes.remove(node)
    if len(source_nodes) == 0:            
        for node in g.nodes():
            if node[1] == 'S':
                if checking_edge(g, node, '') == True:
                    source_nodes.append(node)
    if len(source_nodes) == 0: source_nodes = temp1

    temp2 = []
    for node in out_nodes:
        temp2.append(node)
    for node in temp2:
        if checking_edge(g, node, '') == False:
            if node in out_nodes:
                out_nodes.remove(node)
    if len(out_nodes) == 0:
        for node in g.nodes():
            if node[1] == 'D':
                if checking_edge(g, node, '') == True:
                    out_nodes.append(node)
    if len(out_nodes) == 0: out_nodes = temp2
                
    return source_nodes, out_nodes

'''def find_node_source_and_out(g):
    source_nodes = []
    out_nodes = []
    for node in g.nodes():
        if node[1] == 'S':
            if checking_edge(g, node, 'D') == True:
                source_nodes.append(node)
        else:
            if checking_edge(g, node, 'S') == True:
                out_nodes.append(node)
    return source_nodes, out_nodes'''

def Create_All(expression):
    g_nmos = nx.Graph()
    g_pmos = nx.Graph()
    node = ''
    g_nmos, node = create_nmos(g_nmos, expression)
    source_nodes_nmos, out_nodes_nmos = find_node_source_and_out(g_nmos);
    serial_array_pmos = []
    parallel_array_pmos = []
    for edge in g_nmos.edges():
        n1 = edge[0][0]
        n2 = edge[1][0]
        if n1 == n2:
            continue
        n3 = edge[0][1]
        n4 = edge[1][1]
        if n3 == n4:
            serial_array_pmos.append(n1 + n2)
        else:
            parallel_array_pmos.append(n1 + n2)
    euler_path_nmos, euler_path_pmos = euler_path(g_nmos, node)
    g_pmos = create_pmos(g_pmos, expression, euler_path_pmos)
    g_pmos = filter_edge_pmos(g_pmos, serial_array_pmos, parallel_array_pmos, euler_path_pmos)
    #g_pmos.add_edge('AS', 'ED')
    source_nodes_pmos, out_nodes_pmos = find_node_source_and_out(g_pmos);
    return g_nmos, g_pmos, euler_path_nmos, euler_path_pmos, source_nodes_nmos, out_nodes_nmos,source_nodes_pmos, out_nodes_pmos

expression = "A*(B+C)+D*E"
g_nmos, g_pmos, euler_path_nmos, euler_path_pmos, source_nodes_nmos, out_nodes_nmos,source_nodes_pmos, out_nodes_pmos = Create_All(expression)

# Test the function
#Test expression:
#A*(B+C)+D
#(A+B*C)*D
#(A+B+C)*D
#A*B*C+D
#A*B+C*D
#(A+B)*(C+D)
