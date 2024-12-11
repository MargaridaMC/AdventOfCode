import numpy as np

def parse_input(data):
    top_map = np.array([[e for e in row] for row in data.splitlines()])
    top_map = top_map.astype(int)
    return top_map

def get_next_positions(x, y, top_map):
    rows, cols = top_map.shape
    current_height = top_map[x, y]
    next_positions = []
    if 0 <= x - 1 and top_map[x - 1, y] == current_height + 1: 
        next_positions.append((x - 1, y))
    if x + 1 < rows and top_map[x + 1, y] == current_height + 1: 
        next_positions.append((x + 1, y))
    if 0 <= y - 1 and top_map[x, y - 1] == current_height + 1: 
        next_positions.append((x, y - 1))
    if y + 1 < cols and top_map[x, y + 1] == current_height + 1: 
        next_positions.append((x, y + 1))
    return next_positions

def part1(data):

    top_map = parse_input(data)

    # First off identify the starting positions
    start_positions = list(zip(*np.where(top_map == 0)))
    trail_ends = list()

    # For each start position do a depth first search until you find all the trailheads
    for start_x, start_y in start_positions:
        heads = {(start_x, start_y)}
        checked_positions = set()

        while len(heads) > 0:
            x, y = heads.pop()
            next_positions = get_next_positions(x, y, top_map)

            for next_x, next_y in next_positions:

                if (next_x, next_y) in checked_positions: 
                    continue
                else:
                    checked_positions.add((next_x, next_y))

                if top_map[next_x, next_y] == 9:
                    trail_ends.append((next_x, next_y))
                else:
                    heads.add((next_x, next_y))


    return len(trail_ends)

def part2(data):
    top_map = parse_input(data)

    # First off identify the starting positions
    start_positions = list(zip(*np.where(top_map == 0)))
    all_trails = list()

    # For each start position do a depth first search until you find all the trailheads
    for start_x, start_y in start_positions:
        trails_w_start = [[(start_x, start_y)]]

        while len(trails_w_start) > 0:
            
            current_trail = trails_w_start.pop()
            x, y = current_trail[-1]
            next_positions = get_next_positions(x, y, top_map)

            for next_x, next_y in next_positions:
                updated_trail = current_trail + [(next_x, next_y)]
                if top_map[next_x, next_y] == 9:
                    all_trails.append(updated_trail)
                else:
                    trails_w_start.append(updated_trail)


    return len(all_trails)