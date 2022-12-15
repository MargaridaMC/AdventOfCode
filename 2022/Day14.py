import numpy as np
from aocd import get_data

data = get_data(day=14).splitlines()
#with open("test_input.txt") as f:
#    data = f.read().splitlines()

# Setup map
map_lines = [[list(map(int,coordinate.split(","))) for coordinate in line.split(" -> ")] for line in data]
max_x = max([point[0] for line in map_lines for point in line])
max_y = max([point[1] for line in map_lines for point in line])
cave_map = np.zeros((max_y + 3, 2 * max_x))
cave_map[-1, :] = 1

for line in map_lines:
    start_point = line[0]

    point_iterator = iter(line[1:])
    next_point = next(point_iterator, None)
    while next_point is not None:
        start_x, end_x = min(start_point[1], next_point[1]), max(start_point[1], next_point[1])
        start_y, end_y = min(start_point[0], next_point[0]), max(start_point[0], next_point[0])
        cave_map[start_x: end_x + 1, start_y: end_y + 1] = 1
        start_point = next_point
        next_point = next(point_iterator, None)

def find_next_position(position, cave_map):

    # If we've reach the bottom of the map we can't fill the caves anymore
    if position[0] == cave_map.shape[0] - 1:
        return None

    # First check if there is a position directly down
    if cave_map[position[0] + 1, position[1]] == 0:
        return find_next_position([position[0] + 1, position[1]], cave_map)
    # Then check the left diagonal
    elif cave_map[position[0] + 1, position[1] - 1] == 0:
        return find_next_position([position[0] + 1, position[1] - 1], cave_map)
    # Then check the right diagonal
    elif cave_map[position[0] + 1, position[1] + 1] == 0:
        return find_next_position([position[0] + 1, position[1] + 1], cave_map)
    # Finally if none of these possibilities work the grain of sand must stay where it is
    return position

# Let the sand drop
grain_count = 0
while True:
    next_position = find_next_position([0, 500 ], cave_map)
    if next_position is None:
        break
    cave_map[next_position[0], next_position[1]] = 2
    grain_count += 1

print("Number of grains of sand that fit cave:", grain_count)

## PART 2
grain_count = 0
while cave_map[0, 500] == 0:
    next_position = find_next_position([0, 500], cave_map)
    cave_map[next_position[0], next_position[1]] = 2
    grain_count += 1

print("Number of grains of sand that in part 2:", grain_count)