from aocd import get_data
from time import time
import numpy as np
import os

start_time = time()

def make_wall(dig_plan, start_pos):
    directions = {'R': (0, 1), 'D': (1, 0), 'L':(0, -1), 'U': (-1, 0)}
    x, y = start_pos

    # Make a big dig map
    dig_map = np.zeros((10000, 10000))
    dig_map[x, y] = 1

    for line in dig_plan:
        dir, meters, color = line.split(" ")
        meters = int(meters)
        new_x, new_y = x + directions[dir][0]*meters, y + directions[dir][1]*meters
        if new_x == x:
            start_y, end_y = min(y, new_y), max(y, new_y)
            if start_y < 0:
                raise ValueError(f"Found a negative column value:", start_y)
            dig_map[x, start_y: end_y+1] = 1
        else:
            start_x, end_x = min(x, new_x), max(x, new_x)
            if start_x < 0:
                raise ValueError(f"Found a negative row value:", start_x)
            dig_map[start_x: end_x+1, y] = 1

        x, y = new_x, new_y
        # os.system("cls")
        # print_map(dig_map, center_around=(x, y), n_cols=20)

    assert x == start_pos[0] and y==start_pos[1]

    return dig_map 


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

def print_map(m, col_lim = None, center_around = None, n_cols = 50):
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
start_pos = (500, 500)
dig_map = make_wall(input, start_pos)

# Do region growing starting at the pixel next to the start position
#dig_map = region_growing(dig_map, (start_pos[0] + 1, start_pos[1] + 1))
dig_map = region_growing(dig_map, (start_pos[0] - 1, start_pos[1] - 1))

print("Part 1: N lava cubic meters:", dig_map.sum())

end_time = time()
print(f"Calculated solution in {end_time - start_time} seconds.")