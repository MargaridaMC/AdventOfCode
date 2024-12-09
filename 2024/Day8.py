import numpy as np
from itertools import combinations

def parse_input(data):
    antenna_map = np.array([[char for char in row] for row in data.splitlines()])
    antenna_types = [char for char in data.replace("\n", "").replace(".", "")]
    antenna_locations = dict()
    for antenna in antenna_types:
        antenna_locations[antenna] = [(x, y) for x, y in zip(*np.where(antenna_map == antenna))]
    return antenna_map, antenna_locations

def part1(data):

    antenna_map, all_antenna_locations = parse_input(data)
    rows, cols = antenna_map.shape
    antinode_locations = set()

    for antenna_locations in all_antenna_locations.values():
        for loc1, loc2 in combinations(antenna_locations, 2):
            dist = (loc2[0] - loc1[0], loc2[1] - loc1[1])
            antinode1 = (loc1[0] - dist[0], loc1[1] - dist[1])
            antinode2 = (loc2[0] + dist[0], loc2[1] + dist[1])

            for antinode in [antinode1, antinode2]:
                if 0 <= antinode[0] < rows and 0 <= antinode[1] < cols:
                    antinode_locations.add(antinode)

    return len(antinode_locations)

def part2(data):

    antenna_map, all_antenna_locations = parse_input(data)
    rows, cols = antenna_map.shape
    antinode_locations = set()

    for antenna_locations in all_antenna_locations.values():
        for loc1, loc2 in combinations(antenna_locations, 2):
            dist = (loc2[0] - loc1[0], loc2[1] - loc1[1])
            
            new_antinode_loc = loc1
            i = 0
            while 0 <= new_antinode_loc[0] < rows and 0 <= new_antinode_loc[1] < cols:
                antinode_locations.add(new_antinode_loc)

                i += 1
                new_antinode_loc = (loc1[0] + i * dist[0], loc1[1] + i * dist[1])

            i = 1
            new_antinode_loc = (loc1[0] - dist[0], loc1[1] - dist[1])
            while 0 <= new_antinode_loc[0] < rows and 0 <= new_antinode_loc[1] < cols:
                antinode_locations.add(new_antinode_loc)

                i += 1
                new_antinode_loc = (loc1[0] - i * dist[0], loc1[1] - i * dist[1])
                
    return len(antinode_locations)