
from expression import *

expression = input("Enter Boolean Expression: ")
circuit = LogicCircuit(expression)
circuit.run()
circuit.display_info()
