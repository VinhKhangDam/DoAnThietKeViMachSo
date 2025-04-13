#include "export_data.h"
#include <fstream>
#include "json.hpp"
using json = nlohmann::json;

void export_to_json(const std::string& filename,
                    const Graph& g_nmos,
                    const Graph& g_pmos,
                    const std::vector<std::string>& euler_nmos,
                    const std::vector<std::string>& euler_pmos,
                    const std::vector<std::string>& src_nmos,
                    const std::vector<std::string>& out_nmos,
                    const std::vector<std::string>& src_pmos,
                    const std::vector<std::string>& out_pmos) {
    json j;
    j["euler_nmos"] = euler_nmos;
    j["euler_pmos"] = euler_pmos;
    j["source_nmos"] = src_nmos;
    j["out_nmos"] = out_nmos;
    j["source_pmos"] = src_pmos;
    j["out_pmos"] = out_pmos;

    for (const auto& [n1, neighbors] : g_nmos.adj) {
        for (const std::string& n2 : neighbors) {
            if (n1 < n2)
                j["edges_nmos"].push_back({n1, n2});
        }
    }
    for (const auto& [n1, neighbors] : g_pmos.adj) {
        for (const std::string& n2 : neighbors) {
            if (n1 < n2)
                j["edges_pmos"].push_back({n1, n2});
        }
    }
    std::ofstream out(filename);
    out << j.dump(2);
}