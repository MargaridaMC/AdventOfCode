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


def find_horizontal_mirror_row(m, avoid_row=None):
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
            potential_mirror_row = i + 1
            if avoid_row is not None and avoid_row == potential_mirror_row:
                continue
            mirror_row = potential_mirror_row
            break
    return mirror_row

def find_vertical_mirror_col(m, avoid_col = None):
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
            potential_mirror_col = i + 1
            if avoid_col is not None and avoid_col == potential_mirror_col:
                continue
            mirror_col = potential_mirror_col
            break

    return mirror_col

def print_mirror_map(m):
    for r in range(len(m)):
        print(''.join([str(r) for r in m[r]]))

mirror_cols = []
mirror_rows = []
original_reflexion_row = None
original_reflexion_col = None
for idx, m in enumerate(ash_maps):

    original_reflexion_col = find_vertical_mirror_col(m)
    if original_reflexion_col is None:
        original_reflexion_row = find_horizontal_mirror_row(m)
        if original_reflexion_row is None:
            print(f"No mirror found")

    n_rows, n_cols = m.shape
    found_new_mirror = False
    for i in range(n_rows):
        for j in range(n_cols):

            m_copy = m.copy()
            m_copy[i, j] = 0 if m[i, j] == 1 else 1
            col = find_vertical_mirror_col(m_copy, original_reflexion_col)
            row = find_horizontal_mirror_row(m_copy, original_reflexion_row)

            if col is None and row is None:
                continue

            if col is not None:
                if original_reflexion_col is not None and col == original_reflexion_col:
                    continue
                else:
                    found_new_mirror = True
                    mirror_cols.append(col)
                    break
            elif row is not None:
                if original_reflexion_row is not None and row == original_reflexion_row:
                    continue
                else:
                    found_new_mirror = True
                    mirror_rows.append(row)
                    break

        if found_new_mirror:
            break
    if not found_new_mirror:
        print(f"Found no new mirror in map {idx}.")
        if original_reflexion_col is not None:
            mirror_cols.append(original_reflexion_col)
        if original_reflexion_row is not None:
            mirror_rows.append(original_reflexion_row)
        

s = sum(mirror_cols) + sum([100 * r for r in mirror_rows])
print("Part2:", s)