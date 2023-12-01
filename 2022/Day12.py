import sys

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


# Create graph
graph = rx.PyGraph()
all_map_positions = list(product(range(elevation_map.shape[0]), range(elevation_map.shape[1])))

# Create nodes for each point in the map
nodes_idx =  {point: graph.add_node(point) for point in all_map_positions}

# For each pair of adjacent nodes create an edge if the height difference between the two is 0 or 1
for i, p0 in enumerate(all_map_positions):
    # Get adjacent coords
    for p1 in get_reachable_nodes(p0, elevation_map):
        height_difference = elevation_map[p1] - elevation_map[p0]
        #if height_difference in [0, 1]:
        if height_difference <= 1:
            j = nodes_idx[p1]
            if (j, i) not in graph.edge_list():
                graph.add_edges_from(([(i, j, height_difference)]))



"""
# Each time add node is called, it returns a new node index
a = graph.add_node("A")
b = graph.add_node("B")
c = graph.add_node("C")

# add_edges_from takes tuples of node indices and weights,
# and returns edge indices
graph.add_edges_from([(a, b, 1.5), (a, c, 5.0), (b, c, 2.5)])
"""
# Returns the path A -> B -> C
start_node = np.where((all_map_positions == start_pos).all(axis = 1))[0][0]
end_node = np.where((all_map_positions == end_pos).all(axis = 1))[0][0]

# To make visualization easier removed the node that don't connect to anything
for node in graph.node_indices():
    if len(graph.neighbors(node)) == 0:
        graph.remove_node(node)

#mpl_draw(graph, with_labels=True)
#plt.show()

shortest_path = rx.dijkstra_shortest_paths(graph, start_node, end_node)

print("Shortest path:", shortest_path)
print("Shortest path length:", len(shortest_path[end_node]) - 1)

# Solution: PathMapping{3377: [3240, 3241, 3242, 3243, 3244, 3245, 3246, 3247, 3248, 3249, 3250, 3251, 3252, 3253, 3254, 3255, 3256, 3257, 3258, 3259, 3260, 3261, 3262, 3263, 3264, 3265, 3266, 3267, 3268, 3269, 3270, 3271, 3272, 3273, 3274, 3275, 3276, 3277, 3278, 3279, 3280, 3281, 3282, 3283, 3284, 3285, 3286, 3287, 3288, 3289, 3290, 3291, 3292, 3293, 3294, 3295, 3296, 3297, 3298, 3299, 3300, 3301, 3302, 3303, 3304, 3305, 3306, 3307, 3308, 3309, 3310, 3311, 3312, 3313, 3314, 3315, 3316, 3317, 3318, 3319, 3320, 3321, 3322, 3323, 3324, 3325, 3326, 3327, 3328, 3329, 3330, 3331, 3332, 3333, 3334, 3335, 3336, 3337, 3338, 3339, 3340, 3341, 3342, 3343, 3344, 3345, 3346, 3347, 3348, 3349, 3350, 3351, 3352, 3353, 3354, 3355, 3356, 3357, 3358, 3359, 3360, 3361, 3362, 3363, 3364, 3365, 3366, 3367, 3368, 3369, 3370, 3371, 3372, 3373, 3374, 3375, 3376, 3377]}

#sys.modules["matplotlib"] = "C:\\Users\\I539756\\.virtualenvs\\AdventOfCode-JHFMJjOH\\lib\\site-packages\\matplotlib\\__init__.py"