from aocd import get_data
from time import time
import numpy as np
import sys
from dataclasses import dataclass
from operator import itemgetter
from heapq import heappush, heappop
from tqdm import tqdm

start_time = time()

directions = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}

@dataclass(frozen=True)
class Node:
    x: int
    y: int
    dir: int

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.dir == other.dir

def print_path(current_node, prev_nodes, array):
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    if (current_node.x, current_node.y) == (0, 0): 
        return 
    path = [(current_node.x, current_node.y)]
    prev = prev_nodes[current_node]

    prev_step = (current_node.x - directions[current_node.dir][0], current_node.y - directions[current_node.dir][1])
    while prev_step != (prev.x, prev.y):
        path.append(prev_step)
        prev_step = (prev_step[0] - directions[current_node.dir][0], prev_step[1] - directions[current_node.dir][1])

    while (prev.x, prev.y) != (0, 0):
        path.append((prev.x, prev.y))

        prev_step = (prev.x - directions[prev.dir][0], prev.y - directions[prev.dir][1])
        while prev_step != (prev_nodes[prev].x, prev_nodes[prev].y):
            path.append(prev_step)
            prev_step = (prev_step[0] - directions[prev.dir][0], prev_step[1] - directions[prev.dir][1])

        prev = prev_nodes[prev]
    path.append((0, 0))

    nrows, ncols = array.shape

    for r in range(0, nrows):
        for c in range(0, ncols):

            if (r,c) in path:
                print(f"{bcolors.OKGREEN}{array[r, c]}{bcolors.ENDC}", end="")
            else:
                print(array[r,c], end="")
        print()


def calculate_distance(lava_map, x1, y1, x2, y2):
    if x1 == x2:
        min_y, max_y = min(y1, y2), max(y1, y2)
        return lava_map[x1, min_y:max_y + 1].sum()
    else:
        min_x, max_x = min(x1, x2), max(x1, x2)
        return lava_map[min_x:max_x + 1, y1].sum()
    
"""
with open("input copy.txt", "r") as f:
    input = f.read().splitlines()
"""
input = get_data(day=17).splitlines()


input = [[e for e in r] for r in input]
lava_map = np.array(input).astype(int)

min_steps_in_same_direction = 4 #1
max_steps_in_same_direction = 10 #3

n_rows, n_cols = lava_map.shape

shortest_paths = dict()

unvisited_nodes = []
start_node = Node(0, 0, 0)
heappush(unvisited_nodes, (0, start_node))
visited_nodes = set()
prev_nodes = dict()

pbar = tqdm(total=n_rows*n_cols*4)

while len(unvisited_nodes) > 0:

    # Have a look at the node with the shortest length
    dist_to_node, node = heappop(unvisited_nodes)
    visited_nodes.add(node)

    if shortest_paths.get(node, sys.maxsize) < dist_to_node:
        continue

    # Get neighbours
    for rotation in [1, -1]:
        new_dir = (node.dir + rotation)%4
        
        for i in range(min_steps_in_same_direction, max_steps_in_same_direction + 1):
            new_x, new_y = node.x + directions[new_dir][0] * i, node.y + directions[new_dir][1] * i
            if not (0 <= new_x <= n_rows - 1 and 0 <= new_y <= n_cols - 1):
                break

            neighbour_node = Node(new_x, new_y, new_dir)
            new_len = dist_to_node + calculate_distance(lava_map, node.x + directions[new_dir][0], node.y + directions[new_dir][1], new_x, new_y)
            if new_len < shortest_paths.get(neighbour_node, sys.maxsize):
                shortest_paths[neighbour_node] = new_len
                prev_nodes[neighbour_node] = node

                if (neighbour_node.x, neighbour_node.y) == (n_rows - 1, n_cols - 1):
                    print(f"Found an end with distance {new_len}")
                    break
        
            if neighbour_node not in visited_nodes:
                current_shortest_path = min([shortest_paths.get(Node(n_rows - 1, n_cols - 1, dir), sys.maxsize) for dir in range(4)])
                min_dist_to_end = new_len + n_rows - new_x + n_cols - new_y + 2
                if min_dist_to_end < current_shortest_path:
                    heappush(unvisited_nodes, (new_len, neighbour_node))

min_dir, min_dist = min(enumerate([shortest_paths.get(Node(n_rows - 1, n_cols - 1, dir), sys.maxsize) for dir in range(4)]), key=itemgetter(1))
print_path(Node(n_rows - 1, n_cols - 1, min_dir), prev_nodes, lava_map)
print("Part 2: min distance to final node:", min_dist)
end_time = time()

print(f"Calculated solution in {end_time - start_time} seconds")