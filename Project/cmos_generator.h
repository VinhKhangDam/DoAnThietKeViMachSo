// cmos_generator.h
#ifndef CMOS_GENERATOR_H
#define CMOS_GENERATOR_H

#include "parser.h"
#include <vector>
#include <string>

enum ConnectType { SERIES, PARALLEL };

struct TransistorGroup {
    ConnectType type;
    std::vector<std::string> signals;
};

struct Circuit {
    std::vector<TransistorGroup> nmos;
    std::vector<TransistorGroup> pmos;
};

Circuit generate_cmos_circuit(Node* root);

#endif
