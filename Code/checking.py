from expression import *

def CheckSerialConnected(g, token, inter_arr):
    #check ket noi noi tiep
    if len(inter_arr) == 0:
        return True
    arr1 = [0] * len(inter_arr)
    arr2 = [0] * len(inter_arr)
    i = 0
    j = 0
    while (1):
        if inter_arr[i] == 0:
            i += 1
            break
        arr1[i] = inter_arr[i]
        i += 1
    while i < len(inter_arr):
        if inter_arr[i] == 0:
            break
        arr2[j] = inter_arr[i]
        j += 1
        i += 1
    i = 0
    j = 0

    if arr2[0] == 0:
        n1_s = token + 'S'
        n1_d = token + 'D'
        while i < len(arr1) - 1:
            if arr1[i] == 0 : break
            n2_s = arr1[i] + 'S'
            n2_d = arr1[i] + 'D'
            if(n1_s, n2_d) in g.edges():
                return False
            if (n1_d, n2_s) in g.edges():
                return False
            i += 1
        return True
    else:
        while i < len(arr1):
            if arr1[i] == 0 : break
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
                if (n1_d, n2_s) in g.edges():
                    return False
                j += 1
            i += 1
        return True
    
def CheckParallelConnected(g, k, inter_arr):
    if len(inter_arr) == 0;
        return True
    arr1 = []
    arr2 = []
    i = 0
    j = 0
    while (1) :
        if inter_arr[i] == 0:
            i += 1
            break
        arr1.append(inter_arr[i])
        i += 1
    while i < len(inter_arr):
        if inter_arr[i] == 0 : break
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
                if (n1, n2) in g.edges():
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

def isValidNextMode(v, path, G):
    if v in path:
        return False
    lastMode = path[-1]
    if lastMode[0] != v[0]:
        if lastMode[1] == 'S':
            x = lastMode[0] + 'D'
            if x in path:
                return True
            else: return False
        if lastMode[1] == 'D':
            x = lastMode[0] + 'S'
            if x in path:
                return True
            else: return False
    if not path or v in G.neighbors(path[-1]):
        return True
    return False
