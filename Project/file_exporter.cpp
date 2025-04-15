// file_exporter.cpp
#include "file_exporter.h"
#include <fstream>
#include <iostream>

void write_transistor_group(std::ofstream& out, const std::vector<TransistorGroup>& groups, const std::string& label) {
    out << label << "\n";
    for (const auto& group : groups) {
        out << (group.type == SERIES ? "series" : "parallel");
        for (const auto& signal : group.signals) {
            out << " " << signal;
        }
        out << "\n";
    }
}

void export_to_file(const Circuit& circuit, const std::string& filename) {
    std::ofstream out(filename);
    if (!out.is_open()) {
        std::cerr << "Khong the mo file de ghi: " << filename << "\n";
        return;
    }

    write_transistor_group(out, circuit.nmos, "NMOS");
    write_transistor_group(out, circuit.pmos, "PMOS");

    out.close();
}
