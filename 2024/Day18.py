import numpy as np
from tqdm import tqdm

from common_methods import get_shortest_path_from_matrix

COLS = 71
ROWS = 71
N_CORRUPTED_BYTES = 1024
START_POS = (0, 0)
END_POS = (ROWS - 1, COLS - 1)

def parse_input(data):
    coords = [row.split(",") for row in data.splitlines()]
    return [(int(c[1]), int(c[0])) for c in coords]

def part1(data):

    memory_map = np.zeros((ROWS, COLS), dtype=int)
    corrupted_bytes_coords = parse_input(data)

    # First drop the first N corrupted bytes onto the map
    for x, y in corrupted_bytes_coords[:N_CORRUPTED_BYTES]:
        memory_map[x, y] = 1

    # Then get the shortest path
    return len(get_shortest_path_from_matrix(memory_map, START_POS, END_POS))

def part2(data):
    memory_map = np.zeros((ROWS, COLS), dtype=int)
    corrupted_bytes_coords = parse_input(data)

    # First drop the first N corrupted bytes onto the map
    for i, (x, y) in enumerate(tqdm(corrupted_bytes_coords)):
        memory_map[x, y] = 1

        # For the first N corrupted bytes, skip getting the shorted ath, since we know there is a path
        if i < N_CORRUPTED_BYTES:
            continue

        shortest_path = get_shortest_path_from_matrix(memory_map, START_POS, END_POS)
        if shortest_path is None:
            return y, x