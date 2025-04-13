#pragma once
#include "graph_builder.h"
#include <vector>
#include <string>
#include <algorithm>


std::vector<std::string> find_hamiltonian_path(const Graph& g, const std::string& end_node);