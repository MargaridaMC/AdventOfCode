import numpy as np
from aocd import get_data
import re


USING_EXAMPLE = False

SPACE = 0
WALL = 1
NOTHINGNESS = 2

DIRECTION_RIGHT = 0
DIRECTION_BOTTOM = 1
DIRECTION_LEFT = 2
DIRECTION_TOP = 3
def rotate(initial_facing, rotation_direction):
    if rotation_direction is None:
        return initial_facing
    elif rotation_direction == "R":
        return (initial_facing + 1) % 4
    else:
        return (initial_facing - 1) % 4

def identify_current_face(row, col, using_example = USING_EXAMPLE):

    if using_example:
        if row < 4: return 1
        if row < 8:
            if col < 4:
                return 2
            if col < 8:
                return 3
            else:
                return 4
        if col < 12:
            return 5
        else:
            return 6
    else:
        if row < 50:
            if col < 100:
                return 1
            else:
                return 2
        if row < 100:
            return 3
        if row < 150:
            if col < 50:
                return 4
            else:
                return 5
        else:
            return 6



# For the example
cube_face_starts = {1: {"row": 0, "col": 8},
                    2: {"row": 4, "col": 0},
                    3: {"row": 4, "col": 4},
                    4: {"row": 4, "col": 8},
                    5: {"row": 8, "col": 8},
                    6: {"row": 8, "col": 12}} if USING_EXAMPLE else {1: {"row": 0, "col": 50},
                    2: {"row": 0, "col": 100},
                    3: {"row": 50, "col": 50},
                    4: {"row": 100, "col": 0},
                    5: {"row": 100, "col": 50},
                    6: {"row": 150, "col": 0}}
def get_next_position_on_next_face(row, col, facing, using_example = USING_EXAMPLE):
    current_cube_face = identify_current_face(row, col, using_example)

    new_row, new_col, new_facing = row, col, facing
    if using_example:
        if current_cube_face == 1:
            row_relative_to_start_of_face = row - cube_face_starts[1]["row"]
            col_relative_to_start_of_face = col - cube_face_starts[1]["col"]
            if facing == DIRECTION_RIGHT:
                # The cube face at the right of face 1 is face 6 but it's upside down relative to 1
                new_facing = DIRECTION_LEFT
                new_row = 3 - row_relative_to_start_of_face + cube_face_starts[6]["row"]
                new_col = cube_face_starts[6]["col"] + 3
            if facing == DIRECTION_TOP:
                # The cube face at the top of face 1 is face 2 but it's upside down relative to 1
                new_facing = DIRECTION_BOTTOM
                new_row = cube_face_starts[2]["row"]
                new_col = 3 - col_relative_to_start_of_face + cube_face_starts[2]["col"]
            if facing == DIRECTION_LEFT:
                # The cube face at the left of face 1 is face 3 and it's perpendicular relative to 1
                new_facing = DIRECTION_BOTTOM
                new_row = cube_face_starts[3]["row"]
                new_col = row + cube_face_starts[3]["col"]
        if current_cube_face == 2:
            row_relative_to_start_of_face = row - cube_face_starts[2]["row"]
            col_relative_to_start_of_face = col - cube_face_starts[2]["col"]
            if facing == DIRECTION_TOP:
                # Face 1
                new_facing = DIRECTION_BOTTOM
                new_row = cube_face_starts[1]["row"]
                new_col = 3 - col_relative_to_start_of_face + cube_face_starts[1]["col"]
            if facing == DIRECTION_LEFT:
                # Face 6
                new_facing = DIRECTION_TOP
                new_row = 11
                new_col = 3 - row + 12
            if facing == DIRECTION_BOTTOM:
                # Face 5
                new_facing = DIRECTION_TOP
                new_row = 11
                new_col = 3 - col + 8
        if current_cube_face == 3:
            if facing == DIRECTION_TOP:
                # Face 1
                new_facing = DIRECTION_RIGHT
                new_row = col - 4
                new_col = 8
            if facing == DIRECTION_BOTTOM:
                # Face 5
                new_facing = DIRECTION_RIGHT
                new_row = 3 - (col - 4) + 8
                new_col = 8
        if current_cube_face == 4:
            if facing == DIRECTION_RIGHT:
                # Face 6
                new_facing = DIRECTION_BOTTOM
                new_row = 8
                new_col = 3 - (row - 4) + 12
        if current_cube_face == 5:
            if facing == DIRECTION_LEFT:
                # Face 3
                new_facing = DIRECTION_TOP
                new_row = 7
                new_col = 3 - (row - 8) + 4
            if facing == DIRECTION_BOTTOM:
                # Face 2
                new_facing = DIRECTION_TOP
                new_row = 7
                new_col = 3 - (col - 8)
        if current_cube_face == 6:
            row_relative_to_start_of_face = row - 8
            col_relative_to_start_of_face = col - 12
            if facing == DIRECTION_TOP:
                # Face 4
                new_facing = DIRECTION_LEFT
                new_row = 3 - row_relative_to_start_of_face + cube_face_starts[4]["row"]
                new_col = cube_face_starts[4]["col"] + 3
            if facing == DIRECTION_RIGHT:
                # Face 1
                new_facing = DIRECTION_LEFT
                new_row = 3 - row_relative_to_start_of_face
                new_col = cube_face_starts[1]["col"] + 3
            if facing == DIRECTION_BOTTOM:
                # Face 2
                new_facing = DIRECTION_RIGHT
                new_row = 3 - col_relative_to_start_of_face + cube_face_starts[2]["row"]
                new_col = cube_face_starts[2]["col"]
    else:
        if current_cube_face == 1:
            row_relative_to_start_of_face = row - cube_face_starts[1]["row"]
            col_relative_to_start_of_face = col - cube_face_starts[1]["col"]
            if facing == DIRECTION_LEFT:
                # Face 4
                new_facing = DIRECTION_RIGHT
                new_row = 49 - row_relative_to_start_of_face + cube_face_starts[4]["row"]
                new_col = cube_face_starts[4]["col"]
            if facing == DIRECTION_TOP:
                # Face 6
                new_facing = DIRECTION_RIGHT
                new_row = col_relative_to_start_of_face + cube_face_starts[6]["row"]
                new_col = cube_face_starts[6]["col"]
        if current_cube_face == 2:
            row_relative_to_start_of_face = row - cube_face_starts[2]["row"]
            col_relative_to_start_of_face = col - cube_face_starts[2]["col"]
            if facing == DIRECTION_TOP:
                # Face 6
                new_facing = DIRECTION_TOP
                new_row = 49 + cube_face_starts[6]["row"]
                new_col = col_relative_to_start_of_face + cube_face_starts[6]["col"]
            if facing == DIRECTION_RIGHT:
                # Face 5
                new_facing = DIRECTION_LEFT
                new_row = 49 - row_relative_to_start_of_face + cube_face_starts[5]["row"]
                new_col = 49 + cube_face_starts[5]["col"]
            if facing == DIRECTION_BOTTOM:
                # Face 3
                new_facing = DIRECTION_LEFT
                new_row = col_relative_to_start_of_face + cube_face_starts[3]["row"]
                new_col = 49 + cube_face_starts[3]["col"]
        if current_cube_face == 3:
            row_relative_to_start_of_face = row - cube_face_starts[3]["row"]
            col_relative_to_start_of_face = col - cube_face_starts[3]["col"]
            if facing == DIRECTION_LEFT:
                # Face 4
                new_facing = DIRECTION_BOTTOM
                new_row = cube_face_starts[4]["row"]
                new_col = row_relative_to_start_of_face + cube_face_starts[4]["col"]
            if facing == DIRECTION_RIGHT:
                # Face 2
                new_facing = DIRECTION_TOP
                new_row = 49 + cube_face_starts[2]["row"]
                new_col = row_relative_to_start_of_face + cube_face_starts[2]["col"]
        if current_cube_face == 4:
            row_relative_to_start_of_face = row - cube_face_starts[4]["row"]
            col_relative_to_start_of_face = col - cube_face_starts[4]["col"]
            if facing == DIRECTION_LEFT:
                # Face 1
                new_facing = DIRECTION_RIGHT
                new_row = 49 - row_relative_to_start_of_face + cube_face_starts[1]["row"]
                new_col = cube_face_starts[1]["col"]
            if facing == DIRECTION_TOP:
                # Face 3
                new_facing = DIRECTION_RIGHT
                new_row = col_relative_to_start_of_face + cube_face_starts[3]["col"]
                new_col = cube_face_starts[3]["col"]
        if current_cube_face == 5:
            row_relative_to_start_of_face = row - cube_face_starts[5]["row"]
            col_relative_to_start_of_face = col - cube_face_starts[5]["col"]
            if facing == DIRECTION_RIGHT:
                # Face 2
                new_facing = DIRECTION_LEFT
                new_row = 49 - row_relative_to_start_of_face + cube_face_starts[2]["row"]
                new_col = 49 + cube_face_starts[2]["col"]
            if facing == DIRECTION_BOTTOM:
                # Face 6
                new_facing = DIRECTION_LEFT
                new_row = col_relative_to_start_of_face + cube_face_starts[6]["row"]
                new_col = 49 + cube_face_starts[6]["col"]
        if current_cube_face == 6:
            row_relative_to_start_of_face = row - cube_face_starts[6]["row"]
            col_relative_to_start_of_face = col - cube_face_starts[6]["col"]
            if facing == DIRECTION_LEFT:
                # Face 1
                new_facing = DIRECTION_BOTTOM
                new_row = cube_face_starts[1]["row"]
                new_col = row_relative_to_start_of_face + cube_face_starts[1]["col"]
            if facing == DIRECTION_BOTTOM:
                # Face 2
                new_facing = DIRECTION_BOTTOM
                new_row = cube_face_starts[2]["row"]
                new_col = col_relative_to_start_of_face + cube_face_starts[2]["col"]
            if facing == DIRECTION_RIGHT:
                # Face 5
                new_facing = DIRECTION_TOP
                new_row = 49 + cube_face_starts[5]["row"]
                new_col = row_relative_to_start_of_face + cube_face_starts[5]["col"]

    return new_row, new_col, new_facing


def walk(grove_map, row, col, facing, step_count):
    def walk_as_many_steps_as_possible_along_path(path, steps):
        hit_wall = False
        # If there are only empty spaces in the path just walk all steps
        if (path == SPACE).all():
            n_walked_steps = len(path) - 1
        # If we encounter a wall we just stop at the previous column
        elif (path == WALL).any():
            n_walked_steps = np.where(path == WALL)[0][0] - 1
            hit_wall = True
        else:
            # Otherwise stop before reaching the "void"
            n_walked_steps = np.where(path == NOTHINGNESS)[0][0] - 1
        return n_walked_steps, hit_wall

    if facing == DIRECTION_RIGHT:
        desired_path_ahead = grove_map[row, col: col + step_count + 1]
        n_walked_steps_in_current_cube_face, hit_wall = walk_as_many_steps_as_possible_along_path(desired_path_ahead,
                                                                                                  step_count)
        col += n_walked_steps_in_current_cube_face

    elif facing == DIRECTION_BOTTOM:
        desired_path_ahead = grove_map[row: row + step_count + 1, col]
        n_walked_steps_in_current_cube_face, hit_wall = walk_as_many_steps_as_possible_along_path(desired_path_ahead,
                                                                                                  step_count)
        row += n_walked_steps_in_current_cube_face

    elif facing == DIRECTION_LEFT:
        start_col = max(0, col - step_count)
        desired_path_ahead = grove_map[row, start_col:col + 1][::-1]
        n_walked_steps_in_current_cube_face, hit_wall = walk_as_many_steps_as_possible_along_path(desired_path_ahead,
                                                                                                  step_count)
        col -= n_walked_steps_in_current_cube_face

    else:
        start_row = max(0, row - step_count)
        desired_path_ahead = grove_map[start_row: row + 1, col][::-1]
        n_walked_steps_in_current_cube_face, hit_wall = walk_as_many_steps_as_possible_along_path(desired_path_ahead,
                                                                                                  step_count)
        row -= n_walked_steps_in_current_cube_face

    # If we walked fewer steps than what we wanted but it was not because we hit a wall then we need to continue to the next cube face
    if n_walked_steps_in_current_cube_face < step_count and not hit_wall:
        new_row, new_col, new_facing = get_next_position_on_next_face(row, col, facing)
        if grove_map[new_row, new_col] == SPACE:
            # Note, going to the next face already counts as one step
            row, col, facing = walk(grove_map, new_row, new_col, new_facing, step_count - n_walked_steps_in_current_cube_face - 1)

    return row, col, facing

if USING_EXAMPLE:
    with open("test_input.txt") as f:
        lines = f.read()
        n_extra_chars = 1
else:
    lines = get_data(day=22)
    n_extra_chars = 2

grove_map, instructions = lines.split("\n\n")

# Interpret instructions
match = re.findall("\d+[RL]{1}", instructions)
instructions = [(int(m[:-1]), m[-1]) for m in match] + [(int(instructions[-n_extra_chars:]), None)]

# Convert the grove map into an array
grove_map = grove_map.replace(" ", str(NOTHINGNESS)).replace(".", str(SPACE)).replace("#", str(WALL)).splitlines()
grove_map_max_length = max(map(len, grove_map))
grove_map = [[char for char in l.ljust(grove_map_max_length, str(NOTHINGNESS))] for l in grove_map]
grove_map = np.array(grove_map).astype(int)

current_facing = DIRECTION_RIGHT
current_row = 0
current_col = np.where(grove_map[0, :] == SPACE)[0][0]


for n_steps, rotation in instructions:
    # Walk
    current_row, current_col, current_facing = walk(grove_map, current_row, current_col, current_facing, n_steps)

    # Rotate
    current_facing = rotate(current_facing, rotation)

result = 1000 * (current_row + 1) + 4 * (current_col + 1) + current_facing
print("Result:", result)
# 21038  -> too low
# 127838 -> too high