#include <iostream>
#include "LogicExpression.h"
using namespace std;
int main() {
    string expr;
    cout << "Enter logic expression: ";
    cin >> expr;
    LogicExpression logic(expr);
    logic.parse();
    logic.buildNMOS();
    logic.buildPMOS();
    logic.exportData("output");
    cout << "Data exported. Done.\n";
    return 0;
}
