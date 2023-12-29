from aocd import get_data
from time import time
import numpy as np
import os

start_time = time()

def drop_useless_rows(dig_map):
    n_useless_rows = 0
    while len(dig_map[n_useless_rows]) == 0:
        n_useless_rows+=1   

    dig_map = [l for l in dig_map[n_useless_rows:] if len(l) > 0]
    return dig_map, n_useless_rows

def make_wall(dig_plan, start_pos):
    directions = {'0': (0, 1), '1': (1, 0), '2':(0, -1), '3': (-1, 0)}
    x, y = start_pos

    # Make a big dig map
    dig_map = [set() for _ in range(80000000)]
    dig_map[x] = set([y])

    for line in dig_plan:
        _, _, hex = line.split(" ")
        dir = hex[-2]
        meters = int(hex[2:-2], 16)
        new_x, new_y = x + directions[dir][0]*meters, y + directions[dir][1]*meters
        if new_x == x:
            start_y, end_y = min(y, new_y), max(y, new_y)
            if start_y < 0:
                raise ValueError(f"Found a negative column value:", start_y)
            if end_y > len(dig_map):
                raise ValueError(f"Found a too big column value:", end_y)
            dig_map[x] = dig_map[x].union(set(range(start_y, end_y + 1)))
        else:
            start_x, end_x = min(x, new_x), max(x, new_x)
            if start_x < 0:
                raise ValueError(f"Found a negative row value:", start_x)
            if end_x > len(dig_map):
                raise ValueError(f"Found a too big row value:", end_x)
            for i in range(start_x, end_x + 1):
                dig_map[i].add(y)

        x, y = new_x, new_y
        # os.system("cls")
        # print_map(dig_map, center_around=(x, y), n_cols=20)

    assert x == start_pos[0] and y==start_pos[1]

    # Drop useless rows
    dig_map, n_useless_rows = drop_useless_rows(dig_map)
    return dig_map, n_useless_rows

def print_map(dig_map):
    for i, row in enumerate(dig_map):
        if len(row) == 0:
            continue
        row = sorted(list(row))
        for j, value in enumerate(row):
            if j == 0:
                print('.'*(value), end="")
                print('#', end="")
            else:
                print('.'*(value - 1 - row[j-1]), end = '')
                print('#', end='')
        print()

def find_row_copies(dig_map):
    row_copies = {i: [] for i in range(len(dig_map))}
    i = 0
    while i < len(dig_map):
        ref_row = dig_map[i]
        j = i 
        while j < len(dig_map) and dig_map[j] == ref_row :
            if i not in row_copies.keys():
                row_copies[i] = []
            row_copies[i].append(j)
            j += 1
        i = j 
    row_copies = {k: v for k, v in row_copies.items() if len(v) > 0}
    return row_copies

def drop_repeated_rows(dig_map):
    row_copies = find_row_copies(dig_map)
    dig_map = [dig_map[i] for i in sorted(row_copies.keys())]
    return row_copies, dig_map

def transpose(dig_map):
    max_col_count = max(map(max, dig_map))
    dig_map_col = [set() for _ in range(max_col_count + 1)]
    for row, col_values in enumerate(dig_map):
        for v in col_values:
            dig_map_col[v].add(row)
    return drop_useless_rows(dig_map_col)

def region_growing(dig_map, start_pos):

    nrows, ncols = dig_map.shape
    seeds = [start_pos]

    while len(seeds) > 0:
        x, y = seeds.pop()

        if x > 0 and dig_map[x-1, y] != 1:
            dig_map[x-1, y] = 1
            seeds.append((x-1, y))
        if x < nrows - 1 and dig_map[x+1, y] != 1:
            dig_map[x+1, y] = 1
            seeds.append((x+1, y))
        if y > 0 and dig_map[x, y-1] != 1:
            dig_map[x, y-1] = 1
            seeds.append((x, y-1))
        if y < ncols - 1 and dig_map[x, y+1] != 1:
            dig_map[x, y+1] = 1
            seeds.append((x, y+1))
    
    return dig_map

def find_region_growing_start_pos(dig_map):
    cols = np.where(dig_map[1] == 1)[0]
    return (1, cols[0] + 1)

def print_map_array(m, col_lim = None, center_around = None, n_cols = 50):
    if center_around is not None:
        start_x, end_x = max(0, center_around[0]-n_cols), min(m.shape[0], center_around[0]+n_cols)
        start_y, end_y = max(0, center_around[1]-n_cols), min(m.shape[1], center_around[1]+n_cols)
        m_copy = m[start_x:end_x, start_y:end_y]
    else:
        m_copy = m.copy()
        m_copy = m_copy[:, ~np.all(m_copy == 0, axis=0)]
        m_copy = m_copy[~np.all(m_copy == 0, axis=1)]
    if col_lim is None:
        col_lim = m_copy.shape[1]
    for r in range(len(m_copy)):
        print(''.join(m_copy[r, :col_lim].astype(int).astype(str)).replace("0", ".").replace("1", "#"))

"""
with open("input.txt", "r") as f:
    input = f.read().splitlines()
"""
input = get_data(day=18).splitlines()

# To give some space leave some space around the start position
start_pos = (10000000, 10000000)
dig_map, n_useless_rows = make_wall(input, start_pos)
print("Wall built!")
#print_map(dig_map)

# Do region growing starting at the pixel next to the start position
# However, there are a lot of repeated rows so we can just multiply the counts from those rows with however many repetitions there are 
row_copies, dig_map = drop_repeated_rows(dig_map)
row_copy_count = {k: len(v) for k, v in row_copies.items()}

# Transpose rows to columns and repeat the same thing of removing the repeated columns
dig_map_col, n_useless_cols = transpose(dig_map)
col_copies, dig_map_col = drop_repeated_rows(dig_map_col)
col_copy_count = {k: len(v) for k, v in col_copies.items()}
dig_map_array = np.zeros((max(map(max, dig_map_col)) + 1, len(dig_map_col)))
for col, row_list in enumerate(dig_map_col):
    for row in row_list:
        dig_map_array[row, col] = 1

dig_map_array = region_growing(dig_map_array, find_region_growing_start_pos(dig_map_array))
counts = np.array(list(row_copy_count.values())).reshape( -1, 1) * (dig_map_array*list(col_copy_count.values()))

#print_map(dig_map)
print("Part 2: N lava cubic meters:", counts.sum())

end_time = time()
print(f"Calculated solution in {end_time - start_time} seconds.")