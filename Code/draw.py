import matplotlib.pyplot as plt
from itertools import combinations
from expression import *

def createLogicElement(EulerPath_NMOS):
    logicElement = []
    seen = set()
    for node in EulerPath_NMOS:
        if node[0] not in seen:
            logicElement.append(node[0])
            seen.add(node[0])
    return logicElement

def draw_stick_diagram(g_nmos, g_pmos, euler_path_nmos,euler_path_pmos,source_nodes_pmos,source_nodes_nmos,out_nodes_pmos,out_nodes_nmos,logic_elements):
    fig, ax = plt.subplots();  
    ax.set_aspect('equal')
    ax.plot([-4.5, 14], [6, 6], 'b-', linewidth=2) 
    ax.text(14.5, 6, 'Vdd', verticalalignment='center', fontsize=12)
    ax.plot([-4.5, 14], [-1, -1], 'b-', linewidth=2) 
    ax.text(14.5, -1, 'Gnd', verticalalignment='center', fontsize=12)
    ax.plot([-3.5, 13], [5, 5], 'y-', linewidth=2)
    ax.text(13.5, 5, 'pdiff', verticalalignment='center', fontsize=12)
    ax.plot([-3.5, 13], [0, 0], 'g-', linewidth=2)
    ax.text(13.5, 0, 'ndiff', verticalalignment='center', fontsize=12)
    for element in logic_elements:
        x = 1.5 + logic_elements.index(element) * 2
        count = logic_elements.index(element)*2
        ax.plot([x, x], [-0.5, 5.5], 'r-')
        ax.text(x, 5.6, element, horizontalalignment='center', fontsize=10, color='black')
    coordinates_pmos = {}
    for pmos in euler_path_pmos:
        x = 1 + euler_path_pmos.index(pmos)
        ax.text(x,5.1,pmos,horizontalalignment='center', fontsize=10, color='red')
        coordinates_pmos[pmos] = (x, 5)
    count = 0.2
    connected_pmos = []
    for edge in g_pmos.edges:
        node1, node2 = edge
        x1, y1 = coordinates_pmos[node1]
        x2, y2 = coordinates_pmos[node2]
        if(abs(x2-x1) > 1):   
            connected_pmos.append((x1,x2))
            if ((x1,x2+1) in connected_pmos) or ((x1,x2-1) in connected_pmos) or (((x2,x1+1) in connected_pmos) or ((x2,x1-1) in connected_pmos)):
                pass
            else: 
                if ((x1+1,x2) in connected_pmos) or ((x1+1,x2) in connected_pmos) or (((x2+1,x1) in connected_pmos) or ((x2-1,x1) in connected_pmos)):
                    pass
                else:
                    ax.plot([x1, x1], [y1, y1-count], 'b-', linewidth=1)
                    ax.plot([x2, x2], [y2, y2-count], 'b-', linewidth=1) 
                    ax.plot([x1, x2], [y1-count, y2-count], 'b-', linewidth=1) 
                    ax.scatter(x1, y1, color='black', marker='x', s=50)
                    ax.scatter(x2, y2, color='black', marker='x', s=50)
        count += 0.2 
    coordinates_nmos = {}
    for nmos in euler_path_nmos:
        x = 1 + euler_path_nmos.index(nmos)
        ax.text(x,0.1,nmos,horizontalalignment='center', fontsize=10, color='red')
        coordinates_nmos[nmos] = (x, 0)
    count = 0.2
    connected_nmos = []
    for edge in g_nmos.edges:
        node1, node2 = edge
        x1, y1 = coordinates_nmos[node1]
        x2, y2 = coordinates_nmos[node2]
        if(abs(x2-x1) > 1):
            connected_nmos.append((x1,x2))
            if (((x1,x2+1) in connected_nmos) or ((x1,x2-1) in connected_nmos)) or (((x2,x1+1) in connected_nmos) or ((x2,x1-1) in connected_nmos)) :
                pass
            else: 
                if ((x1+1,x2) in connected_nmos) or ((x1-1,x2) in connected_nmos) or (((x2+1,x1) in connected_nmos) or ((x2-1,x1) in connected_nmos)):
                    pass
                else:
                    ax.plot([x1, x1], [y1, y1+count], 'b-', linewidth=1)  
                    ax.plot([x2, x2], [y2, y2+count], 'b-', linewidth=1) 
                    ax.plot([x1, x2], [y1+count, y2+count], 'b-', linewidth=1)  
                    ax.scatter(x1, y1, color='black', marker='x', s=50)
                    ax.scatter(x2, y2, color='black', marker='x', s=50)
        count += 0.2
    vdd_already_connected = []
    for node1, node2 in combinations(set(source_nodes_pmos), 2):
        x1,y1 = coordinates_pmos[node1]
        x2,y2 = coordinates_pmos[node2]
        if(abs(x2-x1) == 1):
            vdd_already_connected.append(x2)
            vdd_already_connected.append(x1)
    if len(set(source_nodes_pmos)) > 1:    
        for node1, node2 in combinations(set(source_nodes_pmos), 2):
            x1,y1 = coordinates_pmos[node1]
            x2,y2 = coordinates_pmos[node2]
            if(abs(x2-x1) == 1):
                x3 = (x1 + x2) /2
                y3 = (y1 + y2) /2
                ax.plot([x3,x3],[5,6],'b', linewidth=1)
                ax.scatter(x3, y3, color='black', marker='x', s=50)
            else:
                if x1 in vdd_already_connected or x2 in vdd_already_connected:
                    if (x1,x2) in connected_pmos or (x2,x1) in connected_pmos:
                        continue
                    else:
                        if(x1 in vdd_already_connected and x2 in vdd_already_connected):
                            continue
                        if x1 in vdd_already_connected:
                            for i in vdd_already_connected:
                                if (x2,i) in connected_pmos or (i,x2) in connected_pmos:
                                    vdd_already_connected.append(x2)
                                    continue
                            ax.plot([x2,x2],[5,6],'b', linewidth=1)
                            ax.scatter(x2, y2, color='blue', marker='x', s=50)
                            vdd_already_connected.append(x2)
                            continue
                        if x2 in vdd_already_connected:
                            for i in vdd_already_connected:
                                if (x1,i) in connected_pmos or (i,x1) in connected_pmos:
                                    vdd_already_connected.append(x1)
                                    continue
                            ax.plot([x1,x1],[5,6],'b', linewidth=1)
                            ax.scatter(x1, y1, color='blue', marker='x', s=50)
                            vdd_already_connected.append(x1)
                            continue
                else:
                    if (x1,x2) in connected_pmos or (x2,x1) in connected_pmos:
                        ax.plot([x1,x1],[5,6],'b', linewidth=1)
                        ax.scatter(x1, y1, color='blue', marker='x', s=50)
                        vdd_already_connected.append(x1)
                        vdd_already_connected.append(x2)
                    else:
                        ax.plot([x1,x1],[5,6],'b', linewidth=1)
                        ax.scatter(x1, y1, color='blue', marker='x', s=50)
                        ax.plot([x2,x2],[5,6],'b', linewidth=1)
                        ax.scatter(x2, y2, color='blue', marker='x', s=50)
                        vdd_already_connected.append(x1)
                        vdd_already_connected.append(x2)
    else:    
        for node in source_nodes_pmos:
            x1,y1 = coordinates_pmos[node]
            ax.plot([x1,x1],[5,6],'b', linewidth=1)
            ax.scatter(x1, y1, color='black', marker='x', s=50)
    gnd_already_connected = []
    for node1, node2 in combinations(set(source_nodes_nmos), 2):
        x1,y1 = coordinates_nmos[node1]
        x2,y2 = coordinates_nmos[node2]
        if(abs(x2-x1) == 1):
            gnd_already_connected.append(x1)
            gnd_already_connected.append(x2)
    if len(set(source_nodes_nmos)) > 1:    
        for node1, node2 in combinations(set(source_nodes_nmos), 2):
            x1,y1 = coordinates_nmos[node1]
            x2,y2 = coordinates_nmos[node2]
            if(abs(x2-x1) == 1):
                    x3 = (x1 + x2) /2
                    y3 = (y1 + y2) /2
                    ax.plot([x3,x3],[0,-1],'b', linewidth=1)
                    ax.scatter(x3, y3, color='black', marker='x', s=50)
            else:
                if x1 in gnd_already_connected or x2 in gnd_already_connected:
                    if (x1,x2) in connected_nmos or (x2,x1) in connected_nmos:
                        continue
                    else:
                        if(x1 in gnd_already_connected and x2 in gnd_already_connected):
                            continue
                        if x1 in gnd_already_connected:
                            for i in gnd_already_connected:
                                if (x2,i) in connected_nmos or (i,x2) in connected_nmos:
                                    gnd_already_connected.append(x2)
                                    continue
                            ax.plot([x2,x2],[0,-1],'b', linewidth=1)
                            ax.scatter(x2, y2, color='black', marker='x', s=50)
                            gnd_already_connected.append(x2)
                            continue 
                        if x2 in gnd_already_connected:
                            for i in gnd_already_connected:
                                if (x1,i) in connected_nmos or (i,x1) in connected_nmos:
                                    gnd_already_connected.append(x1)
                                    continue
                            ax.plot([x1,x1],[0,-1],'b', linewidth=1)
                            ax.scatter(x1, y1, color='black', marker='x', s=50)
                            gnd_already_connected.append(x1)
                            continue 
                else:
                    if (x1,x2) in connected_nmos or (x2,x1) in connected_nmos:
                        ax.plot([x1,x1],[0,-1],'b', linewidth=1)
                        ax.scatter(x1, y1, color='black', marker='x', s=50)
                        gnd_already_connected.append(x1)
                        gnd_already_connected.append(x2)
                    else:
                        ax.plot([x1,x1],[0,-1],'b', linewidth=1)
                        ax.scatter(x1, y1, color='black', marker='x', s=50)
                        ax.plot([x2,x2],[0,-1],'b', linewidth=1)
                        ax.scatter(x2, y2, color='black', marker='x', s=50)
                        gnd_already_connected.append(x1)
                        gnd_already_connected.append(x2)
    else: 
        for node in source_nodes_nmos:
            x1,y1 = coordinates_nmos[node]
            ax.plot([x1,x1],[0,-1],'b', linewidth=1)
            ax.scatter(x1, 0, color='black', marker='x', s=50)
    ax.text(12,2.5,'Y',horizontalalignment='center', fontsize=15, color='red')
    out_pmos_already_connected = []
    for node1, node2 in combinations(set(out_nodes_pmos), 2):
        x1,y1 = coordinates_pmos[node1]
        x2,y2 = coordinates_pmos[node2]
        if(abs(x2-x1) == 1):
            out_pmos_already_connected.append(x1)
            out_pmos_already_connected.append(x2)
    if len(set(out_nodes_pmos)) > 1:    
         for node1, node2 in combinations(set(out_nodes_pmos), 2):
            x1,y1 = coordinates_pmos[node1]
            x2,y2 = coordinates_pmos[node2]
            if(abs(x2-x1) == 1):
                x3 = (x1 + x2) /2
                y3 = (y1 + y2) /2
                ax.plot([x3,x3],[y3-2.5,y3],'b', linewidth=1)
                ax.plot([x3,12],[y3-2.5,2.5],'b', linewidth=1)
                ax.scatter(x3, y3, color='black', marker='x', s=50)
            else:
                if x1 in out_pmos_already_connected or x2 in out_pmos_already_connected:
                    if (x1,x2) in connected_pmos or (x2,x1) in connected_pmos:
                        continue
                    else:
                        if(x1 in out_pmos_already_connected and x2 in out_pmos_already_connected):
                            continue
                        if x1 in out_pmos_already_connected:
                            for i in out_pmos_already_connected:
                                if (x2,i) in connected_pmos or (i,x2) in connected_pmos:
                                    out_pmos_already_connected.append(x2)
                                    continue
                            ax.plot([x2,x2],[y2-2.5,y2],'b', linewidth=1)
                            ax.plot([x2,12],[y2-2.5,2.5],'b', linewidth=1)
                            ax.scatter(x2, y2, color='black', marker='x', s=50)
                            out_pmos_already_connected.append(x2)
                            continue
                        if x2 in out_pmos_already_connected:
                            for i in out_pmos_already_connected:
                                if (x1,i) in connected_pmos or (i,x1) in connected_pmos:
                                    out_pmos_already_connected.append(x1)
                                    continue
                            ax.plot([x1,x1],[y1-2.5,y1],'b', linewidth=1)
                            ax.plot([x1,12],[y1-2.5,2.5],'b', linewidth=1)
                            ax.scatter(x1, y1, color='black', marker='x', s=50)
                            out_pmos_already_connected.append(x1)
                            continue
                else:
                    if (x1,x2) in connected_pmos or (x2,x1) in connected_pmos:
                        ax.plot([x1,x1],[y1-2.5,y1],'b', linewidth=1)
                        ax.plot([x1,12],[y1-2.5,2.5],'b', linewidth=1)
                        ax.scatter(x1, y1, color='black', marker='x', s=50)
                        out_pmos_already_connected.append(x1)
                        out_pmos_already_connected.append(x2)
                    else:
                        ax.plot([x1,x1],[y1-2.5,y1],'b', linewidth=1)
                        ax.plot([x1,12],[y1-2.5,2.5],'b', linewidth=1)
                        ax.scatter(x1, y1, color='black', marker='x', s=50)
                        ax.plot([x2,x2],[y2-2.5,y2],'b', linewidth=1)
                        ax.plot([x2,12],[y2-2.5,2.5],'b', linewidth=1)
                        ax.scatter(x2, y2, color='black', marker='x', s=50)
                        out_pmos_already_connected.append(x1)
                        out_pmos_already_connected.append(x2)
    else: 
        for node_pmos in out_nodes_pmos:
            x1,y1 = coordinates_pmos[node_pmos]
            ax.plot([x1,x1],[y1-2.5,5],'b', linewidth=1)
            ax.plot([x1,12],[y1-2.5,2.5],'b', linewidth=1)
            ax.scatter(x1, y1, color='black', marker='x', s=50)
    out_nmos_already_connected = []
    for node1, node2 in combinations(set(out_nodes_nmos), 2):
        x1,y1 = coordinates_nmos[node1]
        x2,y2 = coordinates_nmos[node2]
        if(abs(x2-x1) == 1):
            out_nmos_already_connected.append(x2)
            out_nmos_already_connected.append(x1)
    if len(set(out_nodes_nmos)) > 1:    
         for node1, node2 in combinations(set(out_nodes_nmos), 2):
            x1,y1 = coordinates_nmos[node1]
            x2,y2 = coordinates_nmos[node2]
            if(abs(x2-x1) == 1):
                x3 = (x1 + x2) /2
                y3 = (y1 + y2) /2
                ax.plot([x3,x3],[y3+2.5,y3],'b', linewidth=1)
                ax.plot([x3,12],[y3+2.5,2.5],'b', linewidth=1)
                ax.scatter(x3, y3, color='black', marker='x', s=50)
            else:
                if x1 in out_nmos_already_connected or x2 in out_nmos_already_connected:
                    if (x1,x2) in connected_nmos or (x2,x1) in connected_nmos:
                        continue
                    else:
                        if(x1 in out_nmos_already_connected and x2 in out_nmos_already_connected):
                            continue
                        if x1 in out_nmos_already_connected:
                            for i in out_nmos_already_connected:
                                if (x2,i) in connected_nmos or (i,x2) in connected_nmos:
                                    out_nmos_already_connected.append(x2)
                                    continue
                            ax.plot([x2,x2],[y2+2.5,y2],'b', linewidth=1)
                            ax.plot([x2,12],[y2+2.5,2.5],'b', linewidth=1)
                            ax.scatter(x2, y2, color='black', marker='x', s=50)
                            out_nmos_already_connected.append(x2)
                            continue    
                        if x2 in out_nmos_already_connected:
                            for i in out_nmos_already_connected:
                                if (x1,i) in connected_nmos or (i,x1) in connected_nmos:
                                    out_nmos_already_connected.append(x1)
                                    continue
                            ax.plot([x1,x1],[y1+2.5,y1],'b', linewidth=1)
                            ax.plot([x1,12],[y1+2.5,2.5],'b', linewidth=1)
                            ax.scatter(x1, y1, color='black', marker='x', s=50)
                            out_nmos_already_connected.append(x1)
                            continue
                else:
                    if (x1,x2) in connected_nmos or (x2,x1) in connected_nmos:
                        ax.plot([x1,x1],[y1+2.5,y1],'b', linewidth=1)
                        ax.plot([x1,12],[y1+2.5,2.5],'b', linewidth=1)
                        ax.scatter(x1, y1, color='black', marker='x', s=50)
                        out_nmos_already_connected.append(x1)
                        out_nmos_already_connected.append(x2)
                    else:
                        ax.plot([x2,x2],[y2+2.5,y2],'b', linewidth=1)
                        ax.plot([x2,12],[y2+2.5,2.5],'b', linewidth=1)
                        ax.scatter(x2, y2, color='black', marker='x', s=50)
                        ax.plot([x1,x1],[y1+2.5,y1],'b', linewidth=1)
                        ax.plot([x1,12],[y1+2.5,2.5],'b', linewidth=1)
                        ax.scatter(x1, y1, color='black', marker='x', s=50)
                        out_nmos_already_connected.append(x1)
                        out_nmos_already_connected.append(x2)
    else: 
        for node_nmos in out_nodes_nmos:
            x1,y1 = coordinates_nmos[node_nmos]
            ax.plot([x1,x1],[y1+2.5,y1],'b', linewidth=1)
            ax.plot([x1,12],[y1+2.5,2.5],'b', linewidth=1)
            ax.scatter(x1, y1, color='black', marker='x', s=50)
    ax.axis('off')
    plt.show()
