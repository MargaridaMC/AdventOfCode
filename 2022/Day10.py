from aocd import get_data
import numpy as np

input = get_data(day=10).splitlines()
#input = "addx 15\naddx -11\naddx 6\naddx -3\naddx 5\naddx -1\naddx -8\naddx 13\naddx 4\nnoop\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx -35\naddx 1\naddx 24\naddx -19\naddx 1\naddx 16\naddx -11\nnoop\nnoop\naddx 21\naddx -15\nnoop\nnoop\naddx -3\naddx 9\naddx 1\naddx -3\naddx 8\naddx 1\naddx 5\nnoop\nnoop\nnoop\nnoop\nnoop\naddx -36\nnoop\naddx 1\naddx 7\nnoop\nnoop\nnoop\naddx 2\naddx 6\nnoop\nnoop\nnoop\nnoop\nnoop\naddx 1\nnoop\nnoop\naddx 7\naddx 1\nnoop\naddx -13\naddx 13\naddx 7\nnoop\naddx 1\naddx -33\nnoop\nnoop\nnoop\naddx 2\nnoop\nnoop\nnoop\naddx 8\nnoop\naddx -1\naddx 2\naddx 1\nnoop\naddx 17\naddx -9\naddx 1\naddx 1\naddx -3\naddx 11\nnoop\nnoop\naddx 1\nnoop\naddx 1\nnoop\nnoop\naddx -13\naddx -19\naddx 1\naddx 3\naddx 26\naddx -30\naddx 12\naddx -1\naddx 3\naddx 1\nnoop\nnoop\nnoop\naddx -9\naddx 18\naddx 1\naddx 2\nnoop\nnoop\naddx 9\nnoop\nnoop\nnoop\naddx -1\naddx 2\naddx -37\naddx 1\naddx 3\nnoop\naddx 15\naddx -21\naddx 22\naddx -6\naddx 1\nnoop\naddx 2\naddx 1\nnoop\naddx -10\nnoop\nnoop\naddx 20\naddx 1\naddx 2\naddx 2\naddx -6\naddx -11\nnoop\nnoop\nnoop".splitlines()

# PART 1
operation_n_cycles = [2 if line.startswith("addx") else 1 for line in input]
cumulative_n_cycles = np.cumsum(operation_n_cycles)
values_to_add = [int(line.split(" ")[1]) if line.startswith("addx") else 0 for line in input]

signal_strength = 0
for cycle in [20, 60, 100, 140, 180, 220]:
    n_operations_to_consider = np.argmax(cumulative_n_cycles >= cycle)
    #print(f"Signal strength at cycle {cycle}:", (sum(values_to_add[:n_operations_to_consider]) + 1) * cycle)
    signal_strength += ((sum(values_to_add[:n_operations_to_consider]) + 1) * cycle)

print("Signal strength:", signal_strength)

# PART 2
CRT = np.empty((6, 40), dtype=str)
for crt_row in range(6):
    for crt_col in range(40):
        cycle = crt_row * 40 + crt_col
        n_operations_to_consider = 0 if all(cumulative_n_cycles > cycle) else np.argmax(cumulative_n_cycles > cycle)
        if cumulative_n_cycles[0] == cycle:
            n_operations_to_consider = 1
        X = sum(values_to_add[:n_operations_to_consider]) + 1
        if crt_col in range(X - 1, X + 2):
            CRT[crt_row, crt_col] = "#"
        else:
            CRT[crt_row, crt_col] = "."

for row in CRT:
    print("".join(row))
