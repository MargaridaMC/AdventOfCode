import numpy as np
from aocd import get_data
import re


def rotate(initial_facing, rotation_direction):
    if rotation_direction is None:
        return initial_facing
    elif rotation_direction == "R":
        return (initial_facing + 1) % 4
    else:
        return (initial_facing - 1) % 4

lines = get_data(day=22)
n_extra_chars = 2
#with open("test_input.txt") as f:
#    lines = f.read()
#    n_extra_chars = 1

grove_map, instructions = lines.split("\n\n")

# Interpret instructions
match = re.findall("\d+[RL]{1}", instructions)
instructions = [(int(m[:-1]), m[-1]) for m in match] + [(int(instructions[-n_extra_chars:]), None)]

# Convert the grove map into an array
SPACE = 0
WALL = 1
NOTHINGNESS = 2
grove_map = grove_map.replace(" ", str(NOTHINGNESS)).replace(".", str(SPACE)).replace("#", str(WALL)).splitlines()
grove_map_max_length = max(map(len, grove_map))
grove_map = [[char for char in l.ljust(grove_map_max_length, str(NOTHINGNESS))] for l in grove_map]
grove_map = np.array(grove_map).astype(int)

DIRECTION_RIGHT = 0
DIRECTION_BOTTOM = 1
DIRECTION_LEFT = 2
DIRECTION_TOP = 3
current_facing = DIRECTION_RIGHT
current_row = 0
current_col = np.where(grove_map[0, :] == SPACE)[0][0]

def walk(potential_path, n_steps, map_row_or_col, start_pos, inverse_direction = False):

    width_of_path = len(map_row_or_col[map_row_or_col!=NOTHINGNESS])
    position_of_first_not_nothing = np.where((map_row_or_col == SPACE) | (map_row_or_col == WALL))[0][0]

    if inverse_direction:
        relative_start_pos = len(map_row_or_col) - start_pos - position_of_first_not_nothing
    else:
        relative_start_pos = start_pos - position_of_first_not_nothing

    # If there are only empty spaces in the path just walk all steps
    if len(potential_path) >= n_steps and (potential_path[:n_steps+1] == SPACE).all():
        n_walked_steps = n_steps
        relative_end_pos = (relative_start_pos + n_walked_steps) % width_of_path
        if inverse_direction:
            end_pos = len(map_row_or_col) - (relative_end_pos + position_of_first_not_nothing)
        else:
            end_pos = relative_end_pos + position_of_first_not_nothing

    # If we encounter a wall we just stop at the previous column
    elif len(potential_path) >= n_steps and any(potential_path[:n_steps+1] == WALL):
        n_walked_steps = np.where(potential_path == WALL)[0][0] - 1
        relative_end_pos = (relative_start_pos + n_walked_steps) % width_of_path
        if inverse_direction:
            end_pos = len(map_row_or_col) - (relative_end_pos + position_of_first_not_nothing)
        else:
            end_pos = relative_end_pos + position_of_first_not_nothing

    # Else if there is nothingness we need to wrap around the path
    else:
        map_row_or_col_without_preceding_nothingness = map_row_or_col[position_of_first_not_nothing:]
        wrapped_path = np.concatenate([potential_path[potential_path!=NOTHINGNESS], map_row_or_col_without_preceding_nothingness])
        end_pos = walk(wrapped_path, n_steps, map_row_or_col, start_pos, inverse_direction)
    return end_pos % len(map_row_or_col)


for n_steps, rotation in instructions:

    # Check how many steps can be walked in this direction
    if current_facing == DIRECTION_RIGHT:
        potential_path = grove_map[current_row, current_col:current_col+n_steps + 1]
        current_col = walk(potential_path, n_steps, grove_map[current_row, :], current_col)

    # Per direction
    if current_facing == DIRECTION_BOTTOM:
        potential_path = grove_map[current_row: current_row + n_steps + 1, current_col]
        current_row = walk(potential_path, n_steps, grove_map[:, current_col], current_row)

    if current_facing == DIRECTION_LEFT:
        start_col = max(0, current_col - n_steps)
        potential_path = grove_map[current_row, start_col:current_col + 1][::-1]
        current_col = walk(potential_path, n_steps, grove_map[current_row, :][::-1], current_col, True)

    if current_facing == DIRECTION_TOP:
        start_row = max(0, current_row - n_steps)
        potential_path = grove_map[start_row: current_row + 1, current_col][::-1]
        current_row = walk(potential_path, n_steps, grove_map[:, current_col][::-1], current_row, True)

    # Rotate
    current_facing = rotate(current_facing, rotation)

result = 1000 * (current_row + 1) + 4 * (current_col + 1) + current_facing
print("Result:", result)
# 21038  -> too low
# 127838 -> too high