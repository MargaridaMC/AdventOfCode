from aocd import get_data
import numpy as np

"""
The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)
def get_next_move_per_pipe(pipe, direction_we_come_from):
    match pipe:
        case '|':
            assert direction_we_come_from in [NORTH, SOUTH], "Invalid direction for pipe |"
            return SOUTH if direction_we_come_from == NORTH else NORTH
        case '-':
            assert direction_we_come_from in [EAST, WEST], "Invalid direction for pipe -"
            return EAST if direction_we_come_from == WEST else WEST
        case 'L':
            assert direction_we_come_from in [EAST, NORTH], "Invalid direction for pipe L"
            return EAST if direction_we_come_from == NORTH else NORTH
        case 'J':
            assert direction_we_come_from in [NORTH, WEST], "Invalid direction for pipe J"
            return WEST if direction_we_come_from == NORTH else NORTH
        case '7':
            assert direction_we_come_from in [SOUTH, WEST], "Invalid direction for pipe 7"
            return WEST if direction_we_come_from == SOUTH else SOUTH
        case 'F':
            assert direction_we_come_from in [EAST, SOUTH], "Invalid direction for pipe F"
            return EAST if direction_we_come_from == SOUTH else SOUTH

def find_pipe_type(connection_direction1, connection_direction2):
    if set([connection_direction1, connection_direction2]) == set([NORTH, SOUTH]): return '|'
    if set([connection_direction1, connection_direction2]) == set([EAST, WEST]): return '-'
    if set([connection_direction1, connection_direction2]) == set([EAST, NORTH]): return 'L'
    if set([connection_direction1, connection_direction2]) == set([NORTH, WEST]): return 'J'
    if set([connection_direction1, connection_direction2]) == set([SOUTH, WEST]): return '7'
    if set([connection_direction1, connection_direction2]) == set([EAST, SOUTH]): return 'F'

def get_next_inside_point(current_pipe, next_pipe, current_inside_point):
    if current_pipe == '|':
        if next_pipe == '|': return current_inside_point
        if current_inside_point[1] == 1: # On the right of the pipe
            match next_pipe:
                case '7': return (0, 1)
                case 'L': return (-1, 1)
                case 'J': return (1, 0)
                case 'F': return (1, 1)
        else:
            match next_pipe:
                case '7': return (1, -1)
                case 'L': return (1, 0)
                case 'J': return (-1, -1)
                case 'F': return (0, -1)
    if current_pipe == '-':
        if next_pipe == '-': return current_inside_point
        if current_inside_point[0] == -1: # On top of the pipe
            match next_pipe:
                case '7': return (0, 1)
                case 'J': return (-1, -1)
                case 'L': return (-1, 1)
                case 'F': return (0, -1)
        else:
            match next_pipe:
                case '7': return (1, -1)
                case 'J': return (1, 0)
                case 'L': return (1, 0)
                case 'F': return (1, 1)
    if current_pipe == 'L':
        if current_inside_point[1] == 1:
            match next_pipe:
                case '-': return (-1, 0)
                case '|': return (0, 1)
                case '7': return (0, 1)
                case 'J': return (-1, -1)
                case 'F': return (1, 1)
        else:
            match next_pipe:
                case '-': return (1, 0)
                case '|': return (0, -1)
                case '7': return (1, -1)
                case 'J': return (1, 0)
                case 'F': return (0, -1)
    if current_pipe == 'J':
        if current_inside_point[0] == 1:
            match next_pipe:
                case '|': return (0, 1)
                case 'L': return (1, 0)
                case '-': return (1, 0)
                case '7': return (0, 1)
                case 'F': return (1, 1)
        else:
            match next_pipe:
                case '|': return (0, -1)
                case 'L': return (-1, 1)
                case '-': return (-1, 0)
                case '7': return (1, -1)
                case 'F': return (0, -1)
    if current_pipe == '7':
        if current_inside_point[0] == 1:
            match next_pipe:
                case '|': return (0, -1)
                case 'L': return (1, 0)
                case 'J': return (-1, -1)
                case '-': return (1, 0)
                case 'F': return (1, 1)
        else:
            match next_pipe:
                case '|': return (0, 1)
                case 'L': return (-1, 1)
                case 'J': return (1, 0)
                case '-': return (-1, 0)
                case 'F': return (0, -1)
    if current_pipe == 'F':
        if current_inside_point[0] == 0:
            match next_pipe:
                case 'J': return (-1, -1)
                case '-': return (-1, 0)
                case '7': return (0, 1)
                case '|': return (0, -1)
                case 'L': return (1, 0)
        else:
            match next_pipe:
                case 'J': return (1, 0)
                case '-': return (1, 0)
                case '7': return (1, -1)
                case '|': return (0, 1)
                case 'L': return (-1, 1)
    else:
        raise ValueError(f"No match found from {current_pipe} to {next_pipe}")

input = ['.F----7F7F7F7F-7....',
'.|F--7||||||||FJ....',
'.||.FJ||||||||L7....',
'FJL7L7LJLJ||LJ.L-7..',
'L--J.L7...LJS7F-7L7.',
'....F-J..F7FJ|L7L7L7',
'....L7.F7||L7|.L7L7|',
'.....|FJLJ|FJ|F7|.LJ',
'....FJL-7.||.||||...',
'....L---J.LJ.LJLJ...']
"""
input = ['...........',
'.S-------7.',
'.|F-----7|.',
'.||.....||.',
'.||.....||.',
'.|L-7.F-J|.',
'.|..|.|..|.',
'.L--J.L--J.',
'...........']"""
input = get_data(day=10).splitlines()
input = np.array([[l for l in row] for row in input])
distances_from_s = -np.ones_like(input, dtype = int)
# First find the start position
s_pos = np.where(input == 'S')
sx, sy = s_pos[0][0], s_pos[1][0]

# Figure out the pipes which surround S and connect to it
connecting_positions = []
connecting_directions = []
## Pipe north of S
if sx > 0 and input[sx - 1, sy] in ['|', '7', 'F']: 
    connecting_positions.append((sx - 1, sy))
    connecting_directions.append(NORTH)
## Pipe south of S
if sx < len(input) and input[sx + 1, sy] in ['|', 'L', 'J']: 
    connecting_positions.append((sx + 1, sy))
    connecting_directions.append(SOUTH)
## Pipe West of S
if sy > 0 and input[sx, sy - 1] in ['-', 'L', 'F']: 
    connecting_positions.append((sx, sy - 1))
    connecting_directions.append(WEST)
## Pipe East of S
if sy < len(input[0]) and input[sx, sy + 1] in ['-', 'J', '7']: 
    connecting_positions.append((sx, sy + 1))
    connecting_directions.append(EAST)


# For each pipe that connects to S follow the loop until we reach back to S
distances_from_s[sx, sy] = 0
for next_position in connecting_positions:
    current_position = (sx, sy)
    distance_count = 0
    while next_position != (sx, sy):

        direction_we_come_from = (current_position[0] - next_position[0], current_position[1] - next_position[1])
        current_position = next_position
        distance_count += 1
        if distances_from_s[current_position[0], current_position[1]] == -1 or distances_from_s[current_position[0], current_position[1]] > distance_count:
            distances_from_s[current_position[0], current_position[1]]= distance_count

        next_move = get_next_move_per_pipe(input[current_position[0], current_position[1]], direction_we_come_from)
        next_position = (next_position[0] + next_move[0], next_position[1] + next_move[1])
        
#print(distances_from_s)
print("Part1: max dist:", distances_from_s.max())

# Part 2: Idea: go around the loop always checking the spots on the inside of the loop (looking to the left if you imagine walking through the loop)
loop_pipes = np.where(distances_from_s > -1, input, '.')

# Figure out the type of pipe in S and replace it on the map
loop_pipes[sx, sy] = find_pipe_type(connecting_directions[0], connecting_directions[1])

inside_seeds = set()
# To make things easier try to find a place where the pipe is '|' to start navigating
# Look left to right
start_position = None
for i in range(input.shape[0]):
    if (loop_pipes[i] == '.').all():
        continue
    first_pipe_col = np.argmax(loop_pipes[i] != '.')
    if loop_pipes[i, first_pipe_col] == '|': 
        start_position = (i, first_pipe_col)
        next_position = (i+1, first_pipe_col)
        inside_point_relative_to_me = (0, 1)
        break

# Look top to bottom for '-'
if start_position is None:
    for j in range(input.shape[1]):
        if (loop_pipes[:, j] == '.').all():
            continue
        first_pipe_row = np.argmax(loop_pipes[:, j] != '.')
        if loop_pipes[first_pipe_row, j] == '-': 
            start_position = (first_pipe_row, j)
            next_position = (first_pipe_row, j + 1)
            inside_point_relative_to_me = (1, 0)
            break

assert start_position is not None, "No start position found"

current_position = start_position
if loop_pipes[current_position[0] + inside_point_relative_to_me[0], current_position[1] + inside_point_relative_to_me[1]] == '.':
    inside_seeds.add(current_position[0] + inside_point_relative_to_me[0], current_position[1] + inside_point_relative_to_me[1])

while next_position != start_position:
    
    direction_we_come_from = (current_position[0] - next_position[0], current_position[1] - next_position[1])
    previous_pipe = loop_pipes[current_position[0], current_position[1]]
    current_position = next_position
    current_pipe = loop_pipes[current_position[0], current_position[1]]
    inside_point_relative_to_me = get_next_inside_point(previous_pipe, current_pipe, inside_point_relative_to_me)
    x, y = current_position[0] + inside_point_relative_to_me[0], current_position[1] + inside_point_relative_to_me[1]
    if loop_pipes[x, y] == '.':
        inside_seeds.add((x, y))

    next_move = get_next_move_per_pipe(loop_pipes[current_position[0], current_position[1]], direction_we_come_from)    
    next_position = (next_position[0] + next_move[0], next_position[1] + next_move[1])
print(len(inside_seeds))

for x, y in inside_seeds:
    loop_pipes[x, y] = 'I'
"""
for row in loop_pipes:
    print("".join(row))
"""
# Do region growing on the discovered points
while len(inside_seeds) > 0:
    x, y = inside_seeds.pop()
    loop_pipes[x, y] = 'I'

    if x > 0 and loop_pipes[x - 1, y] == '.':
        inside_seeds.add((x - 1, y))
    if x + 1 < loop_pipes.shape[0] and loop_pipes[x + 1, y] == '.':
        inside_seeds.add((x + 1, y))
    if y > 0 and loop_pipes[x, y- 1] == '.':
        inside_seeds.add((x, y- 1))
    if y + 1 < loop_pipes.shape[1] and loop_pipes[x, y + 1] == '.':
        inside_seeds.add((x, y + 1))

inside_points = (loop_pipes == 'I').sum()
print("Part2: number of inside points:", inside_points)

