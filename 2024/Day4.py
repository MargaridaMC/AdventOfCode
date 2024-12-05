import numpy as np

def parse_input(data):
    return np.array([[letter for letter in row] for row in data.splitlines()])

def check_letter_in_position(letter_map, x, y, expected_letter):
    max_x, max_y = letter_map.shape
    if 0 <= x < max_x and 0 <= y < max_y and letter_map[x, y] == expected_letter:
        return True
    else:
        return False
    
def find_mas_in_positions(letter_map, expected_letter_positions):
    for (next_x, next_y), expected_letter in zip(expected_letter_positions, 'MAS'):
        if not check_letter_in_position(letter_map, next_x, next_y, expected_letter):
            return False
    return True

def part1(data):
    letter_map = parse_input(data)

    # Find the starting positions
    start_positions = np.where(letter_map == 'X')
    allowed_directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    # Look for the letter M A and S in the 8 allowed directions
    xmas_count = 0
    for x, y in zip(*start_positions):
        for x_dir, y_dir in allowed_directions:
            expected_letter_positions = [(x + i*x_dir, y + i*y_dir) for i in range(1, 4)]
            if find_mas_in_positions(letter_map, expected_letter_positions):
                xmas_count += 1

    return xmas_count

def part2(data):
    letter_map = parse_input(data)

    # Find the starting positions - where the central A is located
    start_positions = np.where(letter_map == 'A')
    allowed_directions = [(1, -1), (-1, 1), (1, 1), (-1, -1)]

    xmas_count = 0
    for x, y in zip(*start_positions):

        if x == 0 or y == 0:
            continue

        for x_dir, y_dir in allowed_directions:
            expected_letter_positions = [(x + i*x_dir, y + i*y_dir) for i in range(-1, 2)]
            
            # Look for MAS in one diagonal
            found_xmas_one_diagonal = find_mas_in_positions(letter_map, expected_letter_positions)

            # If we found it in one diagonal, we need to check the other diagonal
            # Here we neeed to consider that the we can find the letters in two directions
            if found_xmas_one_diagonal:
                x_dir = -x_dir
                expected_letter_positions = [(x + i*x_dir, y + i*y_dir) for i in range(-1, 2)]
                found_xmas_other_diagonal = find_mas_in_positions(letter_map, expected_letter_positions)

                if found_xmas_other_diagonal:
                    xmas_count += 1
                    break

                else:
                    found_xmas_other_diagonal = find_mas_in_positions(letter_map, expected_letter_positions[::-1])
                    if found_xmas_other_diagonal:
                        xmas_count += 1
                        break

    return xmas_count