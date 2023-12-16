from aocd import get_data
import numpy as np
"""
with open("input.txt", "r") as f:
    input = f.read()
"""
input = get_data(day=13)

# Parse input    
ash_maps_str = [m.split("\n") for m in input.split("\n\n")]
ash_maps_str = [[[l for l in e] for e in m] for m in ash_maps_str]
ash_maps = [(np.array(m) == "#").astype(int) for m in ash_maps_str]


def find_horizontal_mirror_col(m):
    n_rows, n_cols = m.shape
    mirror_row = None
    for i in range(n_rows-1):
        right_row = True
        remaining_rows = min(i + 1, n_rows - i - 1)
        for j in range(remaining_rows):
            if (m[i-j] != m[i+j+1]).any():
                right_row = False
                break
        if right_row:
            mirror_row = i + 1
            break
    return mirror_row

def find_vertical_mirror_col(m):
    n_rows, n_cols = m.shape
    mirror_col = None
    for i in range(n_cols-1):
        right_col = True
        remaining_cols = min(i + 1, n_cols - i - 1)
        for j in range(remaining_cols):
            if (m[:, i-j] != m[:, i+j+1]).any():
                right_col = False
                break
        if right_col:
            mirror_col = i + 1
            break

    return mirror_col

mirror_cols = []
mirror_rows = []
for i, m in enumerate(ash_maps):

    col = find_vertical_mirror_col(m)
    if col is None:
        row = find_horizontal_mirror_col(m)
        if row is None:
            print(f"No mirror found in map {i}")
        mirror_rows.append(row)
    else:
        mirror_cols.append(col)

s = sum(mirror_cols) + sum([100 * r for r in mirror_rows])
print("Part1:", s)