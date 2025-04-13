#include <fstream>
#include <vector>
using namespace std;

void write_json() {
    ofstream out("output.json");
    out << R"({
        "euler_path_nmos": ["AS", "AD", "BS", "BD", "CS", "CD"],
        "euler_path_pmos": ["AD", "AS", "BD", "BS", "CD", "CS"],
        "g_nmos_edges": [["AS", "AD"], ["BS", "BD"], ["CS", "CD"], ["AD", "BS"]],
        "g_pmos_edges": [["AD", "AS"], ["BD", "BS"], ["CD", "CS"], ["AS", "BD"]],
        "source_nodes_pmos": ["AS", "CS"],
        "source_nodes_nmos": ["AD", "CD"],
        "out_nodes_pmos": ["BS"],
        "out_nodes_nmos": ["BD"]
    })";
    out.close();
}