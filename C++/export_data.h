#pragma once
#include "graph_builder.h"
#include <string>
#include <vector>

void export_to_json(const std::string& filename,
                    const Graph& g_nmos,
                    const Graph& g_pmos,
                    const std::vector<std::string>& euler_nmos,
                    const std::vector<std::string>& euler_pmos,
                    const std::vector<std::string>& src_nmos,
                    const std::vector<std::string>& out_nmos,
                    const std::vector<std::string>& src_pmos,
                    const std::vector<std::string>& out_pmos);
