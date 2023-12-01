from aocd import get_data
import rustworkx as rx
import numpy as np
from string import ascii_lowercase
from itertools import product
import matplotlib
from rustworkx.visualization import mpl_draw
import matplotlib.pyplot as plt
def get_reachable_nodes(start_node_coords, array):
    x, y = start_node_coords
    max_x, max_y = array.shape
    adjacent_indices = []
    if x > 0 and (elevation_map[x - 1, y] - elevation_map[start_node_coords]) <= 1:
        adjacent_indices.append((x - 1, y))
    if x + 1 < max_x and (elevation_map[x + 1, y] - elevation_map[start_node_coords]) <= 1:
        adjacent_indices.append((x + 1, y))
    if y > 0 and (elevation_map[x, y - 1] - elevation_map[start_node_coords]) <= 1:
        adjacent_indices.append((x, y - 1))
    if y + 1 < max_y and (elevation_map[x, y + 1] - elevation_map[start_node_coords]) <= 1:
        adjacent_indices.append((x, y + 1))

    return adjacent_indices


def calculate_shortest_path_distance(elevation_map, end_pos):
    start_position = (0, 0)
    #next_positions_to_visit = {(0, 1): elevation_map[0, 1], (1, 0): elevation_map[1, 0]}
    next_positions_to_visit = {point: 1 for point in [(0, 1), (1, 0)] if (elevation_map[point] - elevation_map[0, 0]) <= 1}

    node_has_been_visited = np.zeros_like(elevation_map)
    node_has_been_visited[0, 0] = 1
    cumulative_distances = np.zeros_like(elevation_map)
    cumulative_distances[(0, 1)] = 1#elevation_map[0, 1]
    cumulative_distances[(1, 0)] = 1#elevation_map[1, 0]

    while len(next_positions_to_visit) > 0 and cumulative_distances[end_pos] == 0:

        node_w_smallest_dist = min(next_positions_to_visit, key=next_positions_to_visit.get)
        current_distance = next_positions_to_visit[node_w_smallest_dist]

        # Mark as visited
        node_has_been_visited[node_w_smallest_dist] = 1
        if elevation_map[node_w_smallest_dist] >= 24:
            print("Almost at the top")

        adjacent_nodes = get_reachable_nodes(node_w_smallest_dist, elevation_map)
        for node in adjacent_nodes:
            if not (node_has_been_visited[node]):# or cumulative_distances[node] != 0):
                cumulative_distances[node] = current_distance + 1 #elevation_map[bottom_adjacent_coords]
                next_positions_to_visit[node] = current_distance + 1 #elevation_map[bottom_adjacent_coords]

        # Remove from "to-visit" dict
        next_positions_to_visit.pop(node_w_smallest_dist)

        # print(node_w_smallest_dist)
        # print(cumulative_distances)
        # print(next_positions_to_visit)
        # print()

    return cumulative_distances[end_pos]

data = get_data(day=12).splitlines()
#with open("test_input.txt") as f:
#    data = f.read().splitlines()

# Convert data into np array
elevation_map = np.array([[letter for letter in line] for line in data])

# The start position is marked by S and the end by E
start_pos = np.argwhere(elevation_map == 'S')
end_pos = np.argwhere(elevation_map == 'E')

# Now that we have the start and end positions we can replace S and E by the height value
elevation_map = np.char.replace(elevation_map, "S", "a")
elevation_map = np.char.replace(elevation_map, "E", "z")

# Replace the letters by numeric values
for n, letter in enumerate(ascii_lowercase):
    elevation_map = np.char.replace(elevation_map, letter, str(n))
elevation_map = elevation_map.astype(int)

shortest_path_distance = calculate_shortest_path_distance(elevation_map, tuple(end_pos[0]))
print(shortest_path_distance)