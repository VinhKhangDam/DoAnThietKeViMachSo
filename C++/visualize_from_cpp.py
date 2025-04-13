import json
import matplotlib.pyplot as plt
from draw_stick_diagram import draw_stick_diagram, create_logic_element

def load_data_from_cpp():
    with open('output.json') as f:
        data = json.load(f)
    
    # Convert data to the format expected by draw_stick_diagram
    # This would involve creating NetworkX graphs from the edge lists
    # and processing other data as needed
    
    g_nmos = nx.Graph()
    for edge in data['g_nmos_edges']:
        g_nmos.add_edge(edge[0], edge[1])
    
    g_pmos = nx.Graph()
    for edge in data['g_pmos_edges']:
        g_pmos.add_edge(edge[0], edge[1])
    
    logic_elements = create_logic_element(data['euler_path_nmos'])
    
    draw_stick_diagram(
        g_nmos, g_pmos,
        data['euler_path_nmos'], data['euler_path_pmos'],
        data['source_nodes_pmos'], data['source_nodes_nmos'],
        data['out_nodes_pmos'], data['out_nodes_nmos'],
        logic_elements
    )

if __name__ == "__main__":
    load_data_from_cpp()
    plt.show()