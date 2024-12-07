import numpy as np
from tqdm import tqdm

OBSTRUCTION = 1
SPACE = 0
START = 2
DIRECTIONS = {0: np.array((-1, 0)), 1: np.array((0, 1)), 2: np.array((1, 0)), 3: np.array((0, -1))}

def parse_input(data):
    lab_map = data.replace("#", str(OBSTRUCTION)).replace(".", str(SPACE)).replace("^", str(START))
    lab_map = np.array([[int(cell) for cell in row] for row in lab_map.splitlines()])
    start_direction = 0
    start_position = np.argwhere(lab_map == START)[0]
    lab_map[*start_position] = SPACE
    return lab_map, start_direction, start_position

def get_map_section_in_front_of_guard(lab_map, direction, current_position):
    if DIRECTIONS[direction][0] == 0:
        if DIRECTIONS[direction][1] == 1:
            return lab_map[current_position[0], current_position[1] + 1:]
        else:
            return lab_map[current_position[0], :current_position[1]][::-1]
    else:
        if DIRECTIONS[direction][0] == 1:
            return lab_map[current_position[0] + 1:, current_position[1]].T
        else:
            return lab_map[:current_position[0], current_position[1]][::-1].T

def get_visited_positions(lab_map, current_direction, current_position):
    visited_positions = {tuple(current_position)}
    turn_positions = set()
    turn_position_repeat_tolerance = 0

    while True:
        corridor_in_front = get_map_section_in_front_of_guard(lab_map, current_direction, current_position)
        
        if OBSTRUCTION not in corridor_in_front:
            newly_visited_positions = {tuple(current_position + i*DIRECTIONS[current_direction]) for i in range(1, len(corridor_in_front) + 1)}   
            visited_positions = visited_positions.union(newly_visited_positions)
            return visited_positions
            
        next_obstruction_pos = np.where(corridor_in_front == OBSTRUCTION)[0][0]
        newly_visited_positions = {tuple(current_position + i*DIRECTIONS[current_direction]) for i in range(1, next_obstruction_pos + 1)}   
        visited_positions = visited_positions.union(newly_visited_positions)

        current_position = current_position + next_obstruction_pos*DIRECTIONS[current_direction]
        if tuple(current_position) in turn_positions:
            # Guard has made a loop
            turn_position_repeat_tolerance += 1
            if turn_position_repeat_tolerance == 4:
                return None
        
        turn_positions.add(tuple(current_position))
        current_direction = (current_direction + 1) % 4


    
def part1(data):
    lab_map, current_direction, current_position = parse_input(data)
    visited_positions = get_visited_positions(lab_map, current_direction, current_position)
    return len(visited_positions)

def part2(data):

    # It only makes sense to add obstructions to the map in positions which the guard visits, so, for each of the visited positions, we will add an obstruction in the direction of the guard and check if she gets stuck in a loop

    original_lab_map, current_direction, current_position = parse_input(data)

    visited_positions = get_visited_positions(original_lab_map, current_direction, current_position)
    loop_count = 0

    for position in tqdm(visited_positions):

        new_lab_map = original_lab_map.copy()
        new_lab_map[*position] = OBSTRUCTION

        if get_visited_positions(new_lab_map, current_direction, current_position) is None:
            # Guard gets stuck in a loop
            loop_count += 1

    return loop_count