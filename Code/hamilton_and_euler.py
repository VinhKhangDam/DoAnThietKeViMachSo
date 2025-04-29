from graph import *
from checking import *

def Hamilton_DFS_endNode(G, start, end, path=[]):
    path = path + [start]
    if len(path) == len(G.nodes()):
        return path
    for v in G.neighbors(start):
        if isValidNextMode(v, path, G):
            newPath = Hamilton_DFS_endNode(G, v, end, path)
            if newPath:
                return newPath
    return None

def Hamilton_DFS(G, start, path = []):
    path = path + [start]
    if len(path) == len(G.nodes()):
        return path
    for v in G.neighbors(start):
        if isValidNextMode(v, path ,G):
            newPath = Hamilton_DFS(G, v, path)
            if newPath:
                return newPath
    return None

def findHamilton(g, endNode):
    path = []
    for node in g.nodes():
        if node(1) == 'S': continue
        if endNode != '':
            path = Hamilton_DFS_endNode(g, node, endNode)
            if path:
                if (path[0][0] != endNode and path[-1][0] != endNode):
                    path = []
        else:
            path = Hamilton_DFS(g, node)
        if path:
            break
        path = []
    if path:
        return path
    else:
        for node in g.nodes():
            if node[1] == 'D' : continue
            if endNode != '':
                path = Hamilton_DFS_endNode(g, node, endNode)
                if path:
                    if (path[0][0] != endNode and path[-1][0] != endNode):
                        path = []
            else:
                path = Hamilton_DFS(g, node)
            if path:
                break
            path = []
        return path

def EulerPath(g, endNode):
    EulerPath_NMOS = findHamilton(g, endNode)
    if not EulerPath_NMOS:
        return None
    EulerPath_PMOS = [None] * len(EulerPath_NMOS)
    i = 0
    s = False
    while i < len(EulerPath_NMOS) - 1:
        if s == True:
            EulerPath_PMOS[i] = EulerPath_NMOS[i+1]
            EulerPath_PMOS[i+1] = EulerPath_NMOS[i]
        else:
            EulerPath_PMOS[i] = EulerPath_NMOS[i]
            EulerPath_PMOS[i+1] = EulerPath_NMOS[i+1]
        s = not s
        i += 2
    return EulerPath_NMOS, EulerPath_PMOS

def FilterEdge_PMOS(g, arr1, arr2, EulerPath):