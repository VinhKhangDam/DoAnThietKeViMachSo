#include <iostream>
#include "parser.h"
#include "cmos_generator.h"
#include "file_exporter.h"

int main() {
    std::string expr;
    std::cout << "Nhap bieu thuc logic (toi da 5 bien): ";
    std::cin >> expr;

    Node* root = parse_expression(expr);
    Circuit cmos = generate_cmos_circuit(root);
    export_to_file(cmos, "cmos_data.txt");

    std::cout << "Da xuat du lieu CMOS ra file 'cmos_data.txt'\n";
    return 0;
}
