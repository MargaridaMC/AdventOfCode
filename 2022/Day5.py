from aocd import get_data
import numpy as np
input = get_data(day=5)

# Question 1
crate_setup, instructions = input.split("\n\n")
crate_setup = crate_setup.replace("    ", " ")
crate_setup = [x.split(" ") for x in crate_setup.split("\n")[:-1]]
crate_setup = np.array(crate_setup).T.tolist()
crate_setup = [[y for y in x if y != ''] for x in crate_setup]

for instruction in instructions.split("\n"):
    _, n_crates_to_move, _, start_col, _, end_col = instruction.split(" ")
    start_col = int(start_col) - 1
    end_col = int(end_col) - 1
    for i in range(int(n_crates_to_move)):
        moved_crate = crate_setup[start_col].pop(0)
        crate_setup[end_col] = [moved_crate] + crate_setup[end_col]

result = [x[0] for x in crate_setup]
print("Question 1:", "".join(result).replace("[", "").replace("]", ""))

# Question 2
crate_setup, instructions = input.split("\n\n")
crate_setup = crate_setup.replace("    ", " ")
crate_setup = [x.split(" ") for x in crate_setup.split("\n")[:-1]]
crate_setup = np.array(crate_setup).T.tolist()
crate_setup = [[y for y in x if y != ''] for x in crate_setup]

for instruction in instructions.split("\n"):
    _, n_crates_to_move, _, start_col, _, end_col = instruction.split(" ")
    n_crates_to_move = int(n_crates_to_move)
    start_col = int(start_col) - 1
    end_col = int(end_col) - 1
    crates_to_move = crate_setup[start_col][:n_crates_to_move]
    crate_setup[start_col] = crate_setup[start_col][n_crates_to_move:]
    crate_setup[end_col] = crates_to_move + crate_setup[end_col]

result = [x[0] for x in crate_setup]
print("Question 2:", "".join(result).replace("[", "").replace("]", ""))