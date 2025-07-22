import gurobipy
import sys

# Find the installation path of gurobipy
for path in sys.path:
    if "gurobipy" in path.lower():
        print("Gurobi might be installed here:", path)

# Check the actual location of the gurobipy package
print("Gurobipy module is located at:", gurobipy.__file__)
