from checking import *

def CreateNode(g, node):
    node1 = node + 'S'
    node2 = node + 'D'
    g.addNode(node1)
    g.addNode(node2)
    g.addEdge(node1, node2)

def AddEdgeParallel_1(g, node1, node2):
    n1 = node1 + 'S'
    n2 = node1 + 'D'
    n3 = node2 + 'S'
    n4 = node2 + 'D'
    g.addEdge(n1, n3)
    g.addEdge(n2, n4)

def AddEdgeSerial_1(g, node1, node2, inter_arr, mode):
    n1 = node1 + 'S'
    n2 = node1 + 'D'
    n3 = node2 + 'S'
    n4 = node2 + 'D'
    if mode == 0:
        g.addEdge(n3, n2)
    elif mode == 1:
        arr = [node1, 0, node2, 0];
        if CheckSerialConnected(g, ' ', arr) == True:
            g.addEdge(n3, n2)

def AddEdgeSerial_2(g, node, inter_arr, mode):
    n1 = node + 'S'
    n2 = node + 'D'
    i = j = 0
    nodeConnect_1, nodeDegree_1, i = LowestDegreeArrNode(g, 'D', i, inter_arr, '')
    nodeConnect_2, nodeDegree_2, j = LowestDegreeArrNode(g, 'S', j, inter_arr, '')
    if mode == 0:
        g.addEdge(n1, nodeConnect_1)
        for node in g.nodes():
            if node[0] == nodeConnect_1[0]:continue
            if(nodeConnect_1,node) in g.edges() and node[1] == 'D':
                g.addEdge(n1, node)
    elif mode == 1:
        if CheckSerialConnected(g, node, inter_arr) == True:
            g.addEdge(n2, nodeConnect_2)

def AddEdgeParallel_2(g, node, inter_arr):
    n1 = node + 'S'
    n2 = node + 'D'
    out_node = ''
    for n in g.nodes():
        n = n[0]
        if n not in inter_arr and n != node:
            out_node = n
            break
    node1 = LowestDegreeArrNode(g, 'S', node, node, out_node)
    node2 = LowestDegreeArrNode(g, 'D', node, node, out_node)
    node1_degree = g.Degree(node1)
    node2_degree = g.Degree(node2)

    if node1_degree < node2_degree:
        s = 1
        g.addEdge(n1, node1)
    else:
        s = 2
        g.addEdge(n2, node2)
    if s == 1:
        node1 = node1[0]
        NodeConnect = LowestDegree(g, 'D', node, node1, out_node)
        g.addEdge(n2, NodeConnect)
    elif s == 2:
        node2 = node2[0]
        NodeConnect = LowestDegree(g, 'S', node, node2, out_node)
        g.addEdge(n1, NodeConnect)


def AddEdgeParallel_3(g, inter_arr, mode):
    i = 0
    j = 0
    n1 = n2 = n3 = n4 = ''
    n1_degree = n2_degree = n3_degree = n4_degree = 0
    n1, n1_degree, i = LowestDegreeArrNode(g, 'S', i, inter_arr, '')
    t1 = i
    n2, n2_degree, i = LowestDegreeArrNode(g, 'S', i, inter_arr, '')
    n3, n3_degree, j = LowestDegreeArrNode(g, 'D', j, inter_arr, '')
    n4, n4_degree, j = LowestDegreeArrNode(g, 'D', j, inter_arr, '')
    sel = 3

    if n1_degree + n2_degree < n3_degree + n4_degree:
        if CheckParallelConnected(g, 'S', inter_arr) == True and mode == 1:
            sel = 0
            g.addEdge(n1, n2)
        elif mode == 0:
            sel = 0
            g.addEdge(n1, n2)
    else:
        if CheckParallelConnected(g,'D', inter_arr) == True and mode == 1:
            sel = 1
            g.addEdge(n3, n4)
        elif mode == 0:
            sel = 1
            g.addEdge(n3, n4)
    if sel == 1:
        ExceptNode = n4[0]
        NodeConnect, NodeDegree, t1 = LowestDegreeArrNode(g, 'S', t1, inter_arr, ExceptNode)
        g.addEdge(n1, NodeConnect)
    elif sel == 2:
        ExceptNode = n2[0]
        NodeConnect, NodeDegree, t1 = LowestDegreeArrNode(g, 'D', t1, inter_arr, ExceptNode)
        g.addEdge(n3, NodeConnect)
    return

def AddEdgeSerial_3(g, inter_arr, mode):
    i = 0
    n1, n1_degree, i = LowestDegreeArrNode(g, 'S', i, inter_arr, '')
    n2, n2_degree, i = LowestDegreeArrNode(g, 'D', i, inter_arr, n1)
    if mode == 0:
        g.addEdge(n1, n2)
        for node in g.nodes():
            if(node, n1) in g.edges() and node[1] == 'S':
                g.addEdge(node, n2)
            if (node, n2) in g.edges() and node[1] == 'D':
                g.addEdge(node, n1)
    elif mode == 1:
        if CheckSerialConnected(g, '', inter_arr) == True:
            g.AddEdge(n1, n2)

def LowestDegreeArrNode(g, k, i, inter_arr, except_node):
    t = i
    min_degree1 = 100
    min_degree2 = 100
    while 1:
        if inter_arr[t] == 0:
            t += 1
            break
        n1_degree = g.degree(inter_arr[t] + k)
        n1 = inter_arr[t] + k

        if (n1.degree < min.degree1) and (n1 != except_node):
            min_node1 = n1
            min_degree1 = n1_degree
        t += 1
    return min_node1, min_degree1, t
def LowestDegree(g, k, except_node1, except_node2, except_node3):     
    degrees = dict(g.degree())
    if except_node1 != '':
        degrees.pop(except_node1 + 'S', None)
        degrees.pop(except_node1 + 'D', None)
    if except_node2 != '':
        degrees.pop(except_node2 + 'S', None)
        degrees.pop(except_node2 + 'D', None)
    if except_node2 != '':
        degrees.pop(except_node3 + 'S', None)
        degrees.pop(except_node3 + 'D', None)
    filtered_degrees = {node: degree for node, degree in degrees.items() if node[-1] == k}
    lowest_degree_node = min(filtered_degrees, key = degrees.get)
    return lowest_degree_node

def createGraph(g, q, i, expression, mode):
    endNode = ''
    inter_arr = []
    t = i - 1
    expre = expression
    while t >= 0:
        element = q[t]
        inter = IntersectionExpression(expre, element)
        if len(inter) > 0:
            for char in inter:
                if char.isalpha():
                    inter_arr.append(char)
            inter_arr.append(0)
        remain = SubtractExpression(expre, element)
        if len(remain) > 0:
            expre = remain
        t -= 1
    if expre == expression:
        sel = 0
        for token in expression:
            if token.isalpha():
                CreateNode(g, token)
                if sel == 0:
                    sel = 1
                    node1 = token
                else:
                    node2 = token
            elif token in '+*':
                operator = OperatorPrecedence(token)

        if operator == 1:
            AddEdgeParallel_1(g, node1, node2)
        else:
            AddEdgeSerial_1(g, node1, node2, inter_arr, mode)
    else:
        node = ''
        for token in expre:
            if token in '+*':
                operator = OperatorPrecedence(token)
            elif token.isalpha():
                node = token
                CreateNode(g, token)
        if operator == 1:
            if len(node) > 0:
                AddEdgeParallel_2(g, node, inter_arr)
            else:
                AddEdgeParallel_3(g, inter_arr, mode)
        else:
            if len(node):
                AddEdgeSerial_2(g, node, inter_arr, mode)
            else:
                AddEdgeSerial_3(g, inter_arr, mode)
        endNode = node
    return g, endNode

def createNMOS(g, expression):
    q = []
    endNode = ''
    EvaluateExpression(expression, q)
    i = 0
    while i < len(q):
        g, endNode = createGraph(g, q, i, q[i], 0)
        i += 1
    return g, endNode
def createPMOS(g, expression, EulerPath):
    q = []
    EvaluateExpression_inv(expression, q)
    i = 0
    while i < len(EulerPath):
        n1 = EulerPath[i]
        g.addNode(n1)
        if i != 0:
            n2 = EulerPath[i - 1]
            g.addEdge(n1, n2)
        i += 1
    i = 0
    while i < len(q):
        createGraph(g, q, i, q[i], 1)
        i += 1
    return g
