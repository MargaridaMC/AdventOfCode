import numpy as np
import random
from data_parsing import parse_input_to_np_2d_array
from colorama import Back, Style

DIRECTIONS =  [(0, 1), (1, 0), (-1, 0), (0, -1)]
PERPENDICULAR_DIRECTIONS = {(0, 1): (1, 0), (1, 0): (0, 1), (-1, 0): (0, 1), (0, -1): (1, 0)}

def parse_input(data):
    return parse_input_to_np_2d_array(data)

def check_position_value_in_map(x, y, garden_map, expected_value):
    rows, cols = garden_map.shape
    return 0 <= x < rows and 0 <= y < cols and garden_map[x, y] == expected_value

def print_map(garden_map, plant_patch_locations, zoom_in = False):

    _, cols = plant_patch_locations.shape

    if zoom_in:
        min_col = max(0, np.argmax(plant_patch_locations.sum(axis = 0) > 0) - 3)
        max_col = min(cols, cols - np.argmax(plant_patch_locations.sum(axis = 0)[::-1] > 0) + 3)
    else:
        min_col, max_col = 0, cols

    for row in range(0, len(plant_patch_locations)):
        if zoom_in and all(plant_patch_locations[row] == 0): continue
        for col in range(min_col, max_col):
            if plant_patch_locations[row, col]:
                print(Back.GREEN + garden_map[row, col], end = '')
                print(Style.RESET_ALL, end = '')
            else:
                print(garden_map[row, col], end = '')
        print()


def part1(data):
    garden_map = parse_input(data)
    explored_map = np.zeros_like(garden_map, dtype=int)
    score = 0

    while (explored_map == 0).sum() > 0:
        
        seed = random.sample(list(zip(*np.nonzero(explored_map == 0))), 1)[0]

        plant_in_patch = garden_map[*seed]
        patch_locations = np.zeros_like(garden_map, dtype = int)
        perimeter = 0

        seeds = [seed]
        visited_positions = {seed}

        while len(seeds) > 0:
            seed = seeds.pop()
            patch_locations[*seed] = 1
            
            for dir in DIRECTIONS:
                new_pos = (seed[0] + dir[0], seed[1] + dir[1])
                if check_position_value_in_map(new_pos[0], new_pos[1], garden_map, plant_in_patch):
                    if new_pos not in visited_positions:
                        seeds.append(new_pos)
                        visited_positions.add(new_pos)
                else:
                    perimeter += 1
        
        explored_map += patch_locations
        area = patch_locations.sum()
        score += (area * perimeter)

        """
        print_map(garden_map, plant_patch_locations, True)
        print("Area:", area)
        print("Perimeter:", perimeter)
        print()
        """

    return score

def part2(data):
    garden_map = parse_input(data)
    rows, cols = garden_map.shape
    explored_map = np.zeros_like(garden_map, dtype=int)
    score = 0

    while (explored_map == 0).sum() > 0:
        
        # First do region growing to find the patch
        seed = random.sample(list(zip(*np.nonzero(explored_map == 0))), 1)[0]

        plant_in_patch = garden_map[*seed]
        patch_locations = np.zeros_like(garden_map, dtype = int)
        found_edges = set()

        seeds = [seed]
        visited_positions = {seed}

        while len(seeds) > 0:
            seed = seeds.pop()
            patch_locations[*seed] = 1
            
            for dir in DIRECTIONS:
                new_pos = (seed[0] + dir[0], seed[1] + dir[1])
                if check_position_value_in_map(new_pos[0], new_pos[1], garden_map, plant_in_patch):
                    if new_pos not in visited_positions:
                        seeds.append(new_pos)
                        visited_positions.add(new_pos)
                else:
                    found_edges.add((new_pos, dir))
        
        # Progressively merge the existing edges if they are continuous
        # Each tuple will be x_start, x_end, y_start, y_end_, dir
        merged_edges = [(e[0][0], e[0][0], e[0][1], e[0][1], e[1]) for e in found_edges]
        while True:
            found_new_edges_to_merge = False
            new_merged_edges = []
            for edge in merged_edges:
                perpendicular_dir = PERPENDICULAR_DIRECTIONS[edge[4]]
                
                next_x_end, next_y_end = edge[0] - perpendicular_dir[0], edge[2] - perpendicular_dir[1]
                matching_edges_before = [e for e in new_merged_edges if e[1] == next_x_end and e[3] == next_y_end and e[4] == edge[4]]

                next_x_start, next_y_start = edge[1] + perpendicular_dir[0], edge[3] + perpendicular_dir[1]
                matching_edges_after = [e for e in new_merged_edges if e[0] == next_x_start and e[2] == next_y_start and e[4] == edge[4] ]

                if any(matching_edges_before):
                    # Merge the two
                    found_new_edges_to_merge = True
                    matching_edge = matching_edges_before[0]
                    new_edge = [matching_edge[0], edge[1], matching_edge[2], edge[3], edge[4]]
                    new_merged_edges.remove(matching_edge)
                    new_merged_edges.append(new_edge)
                elif any(matching_edges_after):
                    # Merge the two
                    found_new_edges_to_merge = True
                    matching_edge = matching_edges_after[0]
                    new_edge = [edge[0], matching_edge[1], edge[2], matching_edge[3], edge[4]]
                    new_merged_edges.remove(matching_edge)
                    new_merged_edges.append(new_edge)
                else:
                    new_merged_edges.append(edge)

            merged_edges = new_merged_edges.copy()

            if not found_new_edges_to_merge:
                break
                
        explored_map += patch_locations
        area = patch_locations.sum()
        score += (area * len(merged_edges))

        """
        print_map(garden_map, plant_patch_locations, True)
        print("Area:", area)
        print("Perimeter:", perimeter)
        print()
        """

    return score