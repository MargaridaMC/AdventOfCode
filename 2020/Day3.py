from aocd import get_data
import numpy as np

lines = get_data(day=3, year=2020).splitlines()
#with open("../test_input.txt") as f:
#    lines = f.read().splitlines()

TREE = "#"
GROUND = "."

ground_map = np.array([[e for e in line] for line in lines])
n_rows, n_cols = ground_map.shape

tree_count = 0
for row in range(1, n_rows):
    col = (row*3)%n_cols
    tree_count += ground_map[row, col] == TREE

print("Part 1 number of trees on the day:", tree_count)

tree_count_prod = 1
for right_slope, down_slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    tree_count = 0
    for row in range(down_slope, n_rows, down_slope):
        col = (int(row / down_slope)*right_slope) % n_cols
        tree_count += ground_map[row, col] == TREE
    tree_count_prod *= tree_count
    print(f"For slope right {right_slope}, down {down_slope} fround {tree_count} trees")

print("Part 2 product of number of trees per slope:", tree_count_prod)

#1320379648 too low