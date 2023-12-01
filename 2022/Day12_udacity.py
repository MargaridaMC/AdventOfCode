import sys

from aocd import get_data
import rustworkx as rx
import numpy as np
from string import ascii_lowercase
from itertools import product
import matplotlib
from rustworkx.visualization import mpl_draw
import matplotlib.pyplot as plt

import sys


class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        """
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
        """
        return graph

    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes

    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())

    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0
    shortest_path[start_node] = 0

    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    #print(" -> ".join(reversed(path)))
    return shortest_path[target_node]


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
#with open("jota.txt") as f:
#    data = f.read().splitlines()

# Convert data into np array
elevation_map_letters = np.array([[letter for letter in line] for line in data])

# The start position is marked by S and the end by E
start_pos = np.argwhere(elevation_map_letters == 'S')
end_pos = np.argwhere(elevation_map_letters == 'E')

# Now that we have the start and end positions we can replace S and E by the height value
elevation_map = np.char.replace(elevation_map_letters, "S", "a")
elevation_map = np.char.replace(elevation_map, "E", "z")

# Replace the letters by numeric values
for n, letter in enumerate(ascii_lowercase):
    elevation_map = np.char.replace(elevation_map, letter, str(n))
elevation_map = elevation_map.astype(int)


# Create graph
all_map_positions = list(product(range(elevation_map.shape[0]), range(elevation_map.shape[1])))

init_graph = {}
for node in all_map_positions:
    init_graph[str(node)] = {}

# For each pair of adjacent nodes create an edge if the height difference between the two is 0 or 1
for i, p0 in enumerate(all_map_positions):
    # Get adjacent coords
    for p1 in get_reachable_nodes(p0, elevation_map):
        #init_graph[str(p0)][str(p1)] = 1
        init_graph[str(p1)][str(p0)] = 1

graph = Graph(list(map(str, all_map_positions)), init_graph)
#previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=str(tuple(start_pos[0])))
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=str(tuple(end_pos[0])))

#print("Shortest path:", shortest_path)
print_result(previous_nodes, shortest_path, start_node=str(tuple(end_pos[0])), target_node=str(tuple(start_pos[0])))

# PART 2
xs, ys = np.where(elevation_map_letters == 'a')

current_min_distance = np.inf

for coords in zip(xs, ys):
    x, y = coords
    local_start = str((x, y))
    try:
        #previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=local_start)
        #n_steps = print_result(previous_nodes, shortest_path, start_node=local_start, target_node=str(tuple(end_pos[0])))
        n_steps = print_result(previous_nodes, shortest_path, start_node=str(tuple(end_pos[0])), target_node=local_start)
    except KeyError:
        print("Could not find target node")

    if n_steps < current_min_distance:
        print("Found smaller path with n steps:", n_steps)
        current_min_distance = n_steps


print("Smallest path:", current_min_distance)