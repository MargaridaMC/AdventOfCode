import numpy as np
from tqdm import tqdm

COLS = 71
ROWS = 71
N_CORRUPTED_BYTES = 1024
START_POS = (0, 0)
END_POS = (ROWS - 1, COLS - 1)

def parse_input(data):
    coords = [row.split(",") for row in data.splitlines()]
    return [(int(c[1]), int(c[0])) for c in coords]

def get_shortest_path_length(memory_map, start_pos, end_pos):
    rows, cols = memory_map.shape
    checked_positions = np.zeros_like(memory_map, dtype=int)
    checked_positions[*start_pos] = 1
    distances = [(start_pos, 0)]
    distance_map = np.full_like(memory_map, np.inf, dtype=int)

    while True:
        closest_position, closest_distance = distances.pop(0)
        distance_map[*closest_position] = closest_distance
        checked_positions[*closest_position] = 1
        for (x_dir, y_dir) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_position = (closest_position[0] + x_dir, closest_position[1] + y_dir)
            if 0 <= next_position[0] < rows and 0 <= next_position[1] < cols and memory_map[*next_position] != 1 and checked_positions[*next_position] == 0:
                if next_position == end_pos:
                    return closest_distance + 1
                distances.append((next_position, closest_distance + 1))
                checked_positions[*next_position] = 1
        
        if len(distances) == 0:
            return None

        # Sort distance list by distance
        distances = sorted(distances, key=lambda x: x[1])

def part1(data):

    memory_map = np.zeros((ROWS, COLS), dtype=int)
    corrupted_bytes_coords = parse_input(data)

    # First drop the first N corrupted bytes onto the map
    for x, y in corrupted_bytes_coords[:N_CORRUPTED_BYTES]:
        memory_map[x, y] = 1

    # Then get the shortest path
    return get_shortest_path_length(memory_map, START_POS, END_POS)

def part2(data):
    memory_map = np.zeros((ROWS, COLS), dtype=int)
    corrupted_bytes_coords = parse_input(data)

    # First drop the first N corrupted bytes onto the map
    for i, (x, y) in enumerate(tqdm(corrupted_bytes_coords)):
        memory_map[x, y] = 1

        # For the first N corrupted bytes, skip getting the shorted ath, since we know there is a path
        if i < N_CORRUPTED_BYTES:
            continue

        shortest_path_len = get_shortest_path_length(memory_map, START_POS, END_POS)
        if shortest_path_len is None:
            return y, x