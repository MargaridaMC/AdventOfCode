import numpy as np
from itertools import takewhile
from data_parsing import parse_input_to_np_2d_array

SPACE = 0
BOX = 1
WALL = 2
ROBOT = 3
BOX_LEFT = 4
BOX_RIGHT = 5

def parse_input(data, part1 = True):

    warehouse_map, instructions = data.split("\n\n")

    if not part1:
        warehouse_map = warehouse_map.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.").replace("[", str(BOX_LEFT)).replace("]", str(BOX_RIGHT))

    warehouse_map = warehouse_map.replace(".", str(SPACE)).replace("#", str(WALL)).replace("O", str(BOX)).replace("@", str(ROBOT))
    warehouse_map = parse_input_to_np_2d_array(warehouse_map).astype(int)

    instruction_direction_mapping = {'<': np.array([0, -1]), '>': np.array([0, 1]), 'v': np.array([1, 0]), '^': np.array([-1, 0])}
    instructions = [instruction_direction_mapping[i] for i in instructions.replace("\n", "")]
    return warehouse_map, instructions

def get_map_section_in_front_of_robot(warehouse_map, robot_position, direction_to_move):
    if direction_to_move[0] == 0:
        if direction_to_move[1] == 1:
            return warehouse_map[robot_position[0], robot_position[1] + 1:]
        else:
            return warehouse_map[robot_position[0], :robot_position[1]][::-1]
    else:
        if direction_to_move[0] == 1:
            return warehouse_map[robot_position[0] + 1:, robot_position[1]].T
        else:
            return warehouse_map[:robot_position[0], robot_position[1]][::-1].T


def move_robot_in_dir(warehouse_map, robot_position, direction_to_move):
    
    corridor_in_front_of_robot = get_map_section_in_front_of_robot(warehouse_map, robot_position, direction_to_move)

    # If there is no space in from of the robot then nothing can move or there is a wall directly in front
    if not any(corridor_in_front_of_robot == SPACE) or corridor_in_front_of_robot[0] == WALL or all(x > 0 for x in takewhile(lambda x: x != WALL, corridor_in_front_of_robot)): 
        return warehouse_map, robot_position
    
    new_robot_position = robot_position + direction_to_move
    i = 0
    while corridor_in_front_of_robot[i] != SPACE:
        i+=1
    warehouse_map[*(new_robot_position + i*direction_to_move)] = BOX

    warehouse_map[*new_robot_position] = ROBOT
    warehouse_map[*robot_position] = SPACE

    return warehouse_map, new_robot_position

def part1(data):
    warehouse_map, instructions = parse_input(data)
    #print_warehouse_map(warehouse_map)
    
    # First get the position of the robot
    robot_position = np.array(tuple(zip(*np.where(warehouse_map == ROBOT)))[0])

    # Now do the movements until the end
    for direction in instructions:
        warehouse_map, robot_position = move_robot_in_dir(warehouse_map, robot_position, direction)
        #print_warehouse_map(warehouse_map)

    # Finally check the final positions of the boxes
    score = sum(100 * x + y for x, y in zip(*np.where(warehouse_map == BOX)))

    return score

def move_robot_in_dir_part2(warehouse_map, robot_position, direction_to_move):
    
    corridor_in_front_of_robot = get_map_section_in_front_of_robot(warehouse_map, robot_position, direction_to_move)

    # If there is no space in from of the robot then nothing can move or there is a wall directly in front
    if not any(corridor_in_front_of_robot == SPACE) or corridor_in_front_of_robot[0] == WALL or all(x > 0 for x in takewhile(lambda x: x != WALL, corridor_in_front_of_robot)): 
        return warehouse_map, robot_position
    
    elif (direction_to_move == np.array([0, -1])).all() or (direction_to_move == np.array([0, 1])).all() or (corridor_in_front_of_robot[0] == SPACE).all():
        new_robot_position = robot_position + direction_to_move
        next_space_pos = np.argmax(corridor_in_front_of_robot == SPACE)
        for i in range(1, next_space_pos + 1)[::-1]:
            warehouse_map[*(new_robot_position + i*direction_to_move)] = warehouse_map[*(new_robot_position + (i - 1)*direction_to_move)]
        warehouse_map[*new_robot_position] = ROBOT
        warehouse_map[*robot_position] = SPACE

    else:
        # If we are pushing from below we have a possibly wider corridor to move

        # Do region growing to identiy spots that need to be moved
        new_robot_position = robot_position + direction_to_move
        seeds = [new_robot_position]
        checked_positions = np.zeros_like(warehouse_map, dtype = int)
        coords_to_move = []
        while len(seeds) > 0:
            pos_to_move = seeds.pop()
            checked_positions[*pos_to_move] = 1
            
            if warehouse_map[*pos_to_move] == WALL:
                coords_to_move = []
                break

            if warehouse_map[*pos_to_move] == BOX_LEFT:
                other_side_of_box = pos_to_move + np.array([0, 1])
            elif warehouse_map[*pos_to_move] == BOX_RIGHT:
                other_side_of_box = pos_to_move + np.array([0, -1])

            for pos in [pos_to_move, other_side_of_box]:
                
                # Add this position to the list of positions to move
                coords_to_move.append(pos)

                # Also check the position that comes after it 
                next_position_in_dir = pos + direction_to_move
                if not checked_positions[*next_position_in_dir] and warehouse_map[*next_position_in_dir] != SPACE:
                    seeds.append(next_position_in_dir)

        if len(coords_to_move) > 0:
            new_warehouse_map = warehouse_map.copy()
            new_warehouse_map[*robot_position] = SPACE
            for pos in coords_to_move:
                new_warehouse_map[*pos] = SPACE
            for pos in coords_to_move:
                new_warehouse_map[*(pos + direction_to_move)] = warehouse_map[*pos]
            new_warehouse_map[*new_robot_position] = ROBOT
            warehouse_map = new_warehouse_map.copy()
        else:
            new_robot_position = robot_position

    return warehouse_map, new_robot_position

def part2(data):
    warehouse_map, instructions = parse_input(data, False)
    #print_warehouse_map(warehouse_map, False)
    
    # First get the position of the robot
    robot_position = np.array(tuple(zip(*np.where(warehouse_map == ROBOT)))[0])

    # Now do the movements until the end
    for direction in instructions:
        warehouse_map, robot_position = move_robot_in_dir_part2(warehouse_map, robot_position, direction)

    print_warehouse_map(warehouse_map, False)

    # Finally check the final positions of the boxes
    score = sum(100 * x + y for x, y in zip(*np.where(warehouse_map == BOX_LEFT)))

    return score

def print_warehouse_map(warehouse_map, part1 = True):
    for row in warehouse_map.astype(str):
        print(''.join(row).replace(str(SPACE), ".").replace(str(WALL), "#").replace(str(BOX), "O").replace(str(BOX_LEFT), "[").replace(str(BOX_RIGHT), "]").replace(str(ROBOT), "@"))