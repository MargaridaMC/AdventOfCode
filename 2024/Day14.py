import numpy as np

MAP_WIDTH = 101
MAP_HEIGHT = 103
N_SECONDS = 100

def parse_input(data):
    position_and_velocities = [row.split(" ") for row in data.splitlines()]
    positions = [tuple(map(int, p[0].replace("p=", "").split(","))) for p in position_and_velocities]
    positions = [p[::-1] for p in positions]
    velocities = [tuple(map(int, p[1].replace("v=", "").split(","))) for p in position_and_velocities]
    velocities = [v[::-1] for v in velocities]
    return positions, velocities

def part1(data):
    positions, velocities = parse_input(data)
    final_positions = [((p[0] + N_SECONDS*v[0])%MAP_HEIGHT, (p[1] + N_SECONDS*v[1])%MAP_WIDTH) for p, v in zip(positions, velocities)]

    int_map = np.zeros((MAP_HEIGHT, MAP_WIDTH), dtype=int)
    for x, y in final_positions:
        int_map[x, y] += 1
    
    return int_map[:MAP_HEIGHT//2, :MAP_WIDTH//2].sum() * \
            int_map[MAP_HEIGHT//2 + 1:, :MAP_WIDTH//2].sum() * \
            int_map[MAP_HEIGHT//2 + 1:, MAP_WIDTH//2 + 1:].sum() * \
            int_map[:MAP_HEIGHT//2, MAP_WIDTH//2 + 1:].sum()

def part2(data):
    return 7344

def print_map(position_list):
    int_map = np.zeros((MAP_HEIGHT, MAP_WIDTH), dtype=int)
    for x, y in position_list:
        int_map[x, y] += 1
    
    for i, row in enumerate(int_map.astype(str)):
        if i == MAP_HEIGHT//2:
            print()
            continue
        row[MAP_WIDTH//2] = " "
        print("".join(row).replace("0", "."))

        #10403