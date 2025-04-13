import json
import matplotlib.pyplot as plt
import networkx as nx

with open("output_data.json") as f:
    data = json.load(f)

def draw_from_json(data):
    g_nmos = nx.Graph()
    g_pmos = nx.Graph()

    for u, v in data["edges_nmos"]:
        g_nmos.add_edge(u, v)
    for u, v in data["edges_pmos"]:
        g_pmos.add_edge(u, v)

    euler_nmos = data["euler_nmos"]
    euler_pmos = data["euler_pmos"]
    src_nmos = data["source_nmos"]
    out_nmos = data["out_nmos"]
    src_pmos = data["source_pmos"]
    out_pmos = data["out_pmos"]

    def draw_path(ax, path, y, label):
        for i, node in enumerate(path):
            x = i * 2
            ax.plot([x, x], [y - 0.5, y + 0.5], 'k-')
            ax.text(x, y + 0.6, node, ha='center', fontsize=8)
        ax.text(-2, y, label, fontsize=12, color='blue')

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    draw_path(ax, euler_pmos, y=5, label="PMOS Path")
    draw_path(ax, euler_nmos, y=0, label="NMOS Path")

    ax.plot([-2, len(euler_nmos)*2], [6, 6], 'r-', linewidth=2)
    ax.plot([-2, len(euler_nmos)*2], [-1, -1], 'r-', linewidth=2)
    ax.text(len(euler_nmos)*2 + 1, 6, 'Vdd', fontsize=10)
    ax.text(len(euler_nmos)*2 + 1, -1, 'Gnd', fontsize=10)

    ax.text(len(euler_nmos)*2, 2.5, 'Y', fontsize=14, color='red')

    ax.axis('off')
    plt.title("Simplified Stick Diagram from JSON")
    plt.show()

draw_from_json(data)
