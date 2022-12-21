from aocd import get_data
import re
from sympy import solve, Eq, symbols

lines = get_data(day=21)
#with open("test_input.txt") as f:
#    lines = f.read()

monkey_shouts = lines.replace(": ", " = ").splitlines()

def try_to_exec_operations(operations_dict, defined_variables):

    total_new_vars = []
    unresolved_operations = operations_dict.copy()

    while True:
        n_new_vars = 0
        new_vars = []

        for var, op in unresolved_operations.items():
            _, _, op_var1, operator, op_var2 = op.split(" ")
            op = f"defined_variables[op_var1] {operator} defined_variables[op_var2]"
            try:
                defined_variables[var] = eval(op)
                new_vars.append(var)
                total_new_vars.append(var)
                n_new_vars += 1
            except KeyError:
                continue
        if n_new_vars == 0:
            break

        for var in new_vars:
            del unresolved_operations[var]

    # return unresolved operations
    return unresolved_operations, total_new_vars, defined_variables

## PART 1
variables = {l.split(" = ")[0]: int(l.split(" = ")[1]) for l in monkey_shouts if "+" not in l and "-" not in l and "/" not in l and "*" not in l}
operations = {l.split(" = ")[0]: l for l in monkey_shouts if "+" in l or "-" in l or "/" in l or "*" in l}

while "root" not in variables.keys():

    op_w_new_vars = {k:v for k,v in operations.items() if re.search("|".join(variables.keys()), v)}
    remaining_op_w_new_vars, new_vars, variables = try_to_exec_operations(op_w_new_vars, variables)
    for v in new_vars:
        del operations[v]

print("Root:", variables["root"])

## PART 2
var_values = {l.split("=")[0].strip(): l.split("=")[1].strip() for l in monkey_shouts}
root_operation_left, _, root_operation_right = var_values["root"].split(" ")
del var_values["root"]
del var_values["humn"]


while True:

    for var in re.findall("([a-z]{4})", root_operation_left):
        if var == 'humn': continue
        if var_values[var].isdigit():
            root_operation_left = root_operation_left.replace(var, var_values[var])
        else:
            root_operation_left = root_operation_left.replace(var, "(" + var_values[var] + ")")
    for var in re.findall("([a-z]{4})", root_operation_right):
        if var == 'humn': continue
        if var_values[var].isdigit():
            root_operation_right = root_operation_right.replace(var, var_values[var])
        else:
            root_operation_right = root_operation_right.replace(var, "(" + var_values[var] + ")")

    remaining_var_names = re.findall("([a-z]{4})", root_operation_left) + re.findall("([a-z]{4})", root_operation_right)
    if len(remaining_var_names) == 1:
        break

if len(re.findall("([a-z]{4})", root_operation_left)) == 0:
    root_value_left = eval(root_operation_left)
    humn = symbols('humn')
    expr = eval(root_operation_right)
    sol = solve(Eq(expr, root_value_left))
if len(re.findall("([a-z]{4})", root_operation_right)) == 0:
    root_value_right = eval(root_operation_right)
    humn = symbols('humn')
    expr = eval(root_operation_left)
    sol = solve(Eq(expr, root_value_right))

print("Value for humn =", int(sol[0]))
