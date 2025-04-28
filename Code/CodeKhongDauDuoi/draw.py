import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations

# ================================
# Hàm hỗ trợ
# ================================

def create_logic_element(euler_path_nmos):
    logic_elements = []
    seen = set()
    for node in euler_path_nmos:
        if node[0] not in seen:
            logic_elements.append(node[0])
            seen.add(node[0])
    return logic_elements

def draw_stick_diagram(g_nmos, g_pmos, euler_path_nmos, euler_path_pmos,
                       source_nodes_pmos, source_nodes_nmos,
                       out_nodes_pmos, out_nodes_nmos,
                       logic_elements):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Draw power lines
    ax.plot([-4.5, 14], [6, 6], 'b-', linewidth=2) 
    ax.text(14.5, 6, 'Vdd', verticalalignment='center', fontsize=12)
    ax.plot([-4.5, 14], [-1, -1], 'b-', linewidth=2) 
    ax.text(14.5, -1, 'Gnd', verticalalignment='center', fontsize=12)

    ax.plot([-3.5, 13], [5, 5], 'y-', linewidth=2)
    ax.plot([-3.5, 13], [0, 0], 'g-', linewidth=2)

    for i, element in enumerate(logic_elements):
        x = 1.5 + i * 2
        ax.plot([x, x], [-0.5, 5.5], 'r-')
        ax.text(x, 5.6, element, horizontalalignment='center', fontsize=10, color='black')

    # PMOS positions
    coordinates_pmos = {}
    for i, node in enumerate(euler_path_pmos):
        x = 1 + i
        ax.text(x, 5.1, node, horizontalalignment='center', fontsize=10, color='red')
        coordinates_pmos[node] = (x, 5)

    for u, v in g_pmos.edges():
        if u in coordinates_pmos and v in coordinates_pmos:
            x1, y1 = coordinates_pmos[u]
            x2, y2 = coordinates_pmos[v]
            ax.plot([x1, x2], [y1, y2], 'b-')

    # NMOS positions
    coordinates_nmos = {}
    for i, node in enumerate(euler_path_nmos):
        x = 1 + i
        ax.text(x, 0.1, node, horizontalalignment='center', fontsize=10, color='red')
        coordinates_nmos[node] = (x, 0)

    for u, v in g_nmos.edges():
        if u in coordinates_nmos and v in coordinates_nmos:
            x1, y1 = coordinates_nmos[u]
            x2, y2 = coordinates_nmos[v]
            ax.plot([x1, x2], [y1, y2], 'b-')

    # Draw OUT
    ax.text(12, 2.5, 'Y', horizontalalignment='center', fontsize=15, color='red')

    ax.axis('off')
    plt.show()

# ================================
# Đọc dữ liệu xuất từ C++
# ================================

def read_edges(filename):
    g = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            u, v = line.strip().split()
            g.add_edge(u, v)
    return g

def read_list(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# ================================
# Main
# ================================

def main():
    g_nmos = read_edges("output/edges_nmos.txt")
    g_pmos = read_edges("output/edges_pmos.txt")
    logic_elements = read_list("output/logic_elements.txt")

    # Tạo Euler path đơn giản (có thể cải thiện sau)
    euler_path_nmos = list(g_nmos.nodes())
    euler_path_pmos = list(g_pmos.nodes())

    # Tìm node source/output
    source_nodes_nmos = [n for n in g_nmos.nodes() if g_nmos.degree[n] == 1 and n.endswith('S')]
    out_nodes_nmos = [n for n in g_nmos.nodes() if g_nmos.degree[n] == 1 and n.endswith('D')]

    source_nodes_pmos = [n for n in g_pmos.nodes() if g_pmos.degree[n] == 1 and n.endswith('S')]
    out_nodes_pmos = [n for n in g_pmos.nodes() if g_pmos.degree[n] == 1 and n.endswith('D')]

    draw_stick_diagram(
        g_nmos, g_pmos,
        euler_path_nmos, euler_path_pmos,
        source_nodes_pmos, source_nodes_nmos,
        out_nodes_pmos, out_nodes_nmos,
        logic_elements
    )

if __name__ == "__main__":
    main()
