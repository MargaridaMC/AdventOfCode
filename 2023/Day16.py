from aocd import get_data
from time import time
import numpy as np

start_time = time()

#with open("input.txt", "r") as f:
#    input = f.read().splitlines()

input = get_data(day=16).splitlines()

# Turn input into array
layout = np.array([[e for e in l] for l in input])

WEST_DIR = np.array([0, -1])
EAST_DIR = np.array([0, 1])
NORTH_DIR = np.array([-1, 0])
SOUTH_DIR = np.array([1, 0])

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

class Beam:

    def __init__(self, initial_position:np.array, direction: np.array):
        self.current_position = initial_position
        self.direction = direction
    
    def __str__(self):
        return str(self.current_position[0]) + str(self.current_position[1]) + str(self.direction[0]) + str(self.direction[1])

    def move(self):
        if self.direction == NORTH:
            self.current_position = self.current_position + NORTH_DIR
        elif self.direction == SOUTH:
            self.current_position = self.current_position + SOUTH_DIR
        elif self.direction == EAST:
            self.current_position = self.current_position + EAST_DIR
        elif self.direction == WEST:
            self.current_position = self.current_position + WEST_DIR

    def encounter_mirror(self, mirror_type: str):

        if self.direction == NORTH:
            match mirror_type:
                case '|':
                    return [self]
                case '-':
                    # Beam splits into two
                    beam1 = Beam(self.current_position, WEST)
                    beam2 = Beam(self.current_position, EAST)
                    return [beam1, beam2]
                case "\\":
                    self.direction = WEST
                    return [self]
                case "/":
                    self.direction = EAST
                    return [self]
        if self.direction == SOUTH:
            match mirror_type:
                case '|':
                    return [self]
                case '-':
                    # Beam splits into two
                    beam1 = Beam(self.current_position, WEST)
                    beam2 = Beam(self.current_position, EAST)
                    return [beam1, beam2]
                case "\\":
                    self.direction = EAST
                    return [self]
                case "/":
                    self.direction = WEST
                    return [self]
        if self.direction == EAST:
            match mirror_type:
                case '|':
                    # Beatm splits into two
                    beam1 = Beam(self.current_position, NORTH)
                    beam2 = Beam(self.current_position, SOUTH)
                    return [beam1, beam2]
                case '-':
                    return [self]
                case "\\":
                    self.direction = SOUTH
                    return [self]
                case "/":
                    self.direction = NORTH
                    return [self]
        if self.direction == WEST:
            match mirror_type:
                case '|':
                    # Beatm splits into two
                    beam1 = Beam(self.current_position, NORTH)
                    beam2 = Beam(self.current_position, SOUTH)
                    return [beam1, beam2]
                case '-':
                    return [self]
                case "\\":
                    self.direction = NORTH
                    return [self]
                case "/":
                    self.direction = SOUTH
                    return [self]

def position_in_layout(position, layout):
    n_rows, n_cols = layout.shape
    if position[0] < 0 or position[0] >= n_rows or position[1] < 0 or position[1] >= n_cols:
        return False
    else:
        return True

def get_direction_sign(dir):
    if (dir == NORTH).all():
        return "^"
    elif (dir == SOUTH).all():
        return "v"
    elif (dir == EAST).all():
        return ">"
    else:
        return "<"

def print_layout(layout):
    for r in range(len(layout)):
        print(''.join(layout[r]))


def find_n_energized_tiles(start_position, start_direction, layout):
    beam_list = [Beam(np.array(start_position), start_direction)]

    n_rows, n_cols = layout.shape
    beam_passed = np.zeros((n_rows, n_cols , 4))
    while len(beam_list) > 0:
        beam = beam_list.pop()
        x, y = beam.current_position    
        if x < 0 or x >= n_rows or y < 0 or y >= n_cols:
            continue
        if not beam_passed[x, y, beam.direction]:
            beam_passed[x, y, beam.direction] = 1
            if layout[x, y] in ['.', '<', '>', 'v', '^']:
                beam.move()
                beam_list.append(beam)
            else:
                new_beams = beam.encounter_mirror(layout[x, y])
                for beam in new_beams:
                    beam.move()
                beam_list += new_beams
    has_been_energized = beam_passed.any(axis = 2)
    return has_been_energized.sum()

print("Part 1: Number of energized tiles:", find_n_energized_tiles([0, 0], EAST, layout))
end_time = time()
print(f"Part1: Calculated solution in {end_time - start_time} seconds")

start_time = time()
best_value = 0
n_rows, n_cols = layout.shape
for i in range(n_rows):
    potential_count = find_n_energized_tiles([i, 0], EAST, layout)
    if potential_count > best_value:
        best_value = potential_count

    potential_count = find_n_energized_tiles([i, n_cols - 1], WEST, layout)
    if potential_count > best_value:
        best_value = potential_count

for j in range(n_cols):
    potential_count = find_n_energized_tiles([0, j], SOUTH, layout)
    if potential_count > best_value:
        best_value = potential_count

    potential_count = find_n_energized_tiles([n_rows - 1, j], NORTH, layout)
    if potential_count > best_value:
        best_value = potential_count

print("Part 2: best value:", best_value)
end_time = time()
print(f"Part2: Calculated solution in {end_time - start_time} seconds")