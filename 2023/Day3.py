from aocd import get_data
import numpy as np
import re
from operator import mul

input = ['467..114..',
'...*......',
'..35..633.',
'......#...',
'617*......',
'.....+.58.',
'..592.....',
'......755.',
'...$.*....',
'.664.598..']

input = get_data(day=3).splitlines()
symbols = set(''.join(input))
symbols.discard('.')
for i in range(10):
    symbols.discard(str(i))

input_array = np.array([[l for l in row] for row in input])

part_numbers = []
for i, row in enumerate(input):
    numbers = re.finditer("([0-9]+)", row)
    for n in numbers:
        search_col_start = max(n.span()[0] - 1, 0)
        search_col_end = min(n.span()[1] + 1, len(input[0]))
        # Check row above
        if i > 0:
            adjacent_characters = input[i - 1][search_col_start:search_col_end]
            if any ([s in adjacent_characters for s in symbols]):
                part_numbers.append(int(n.group(0)))
                continue
        # Check row below
        if i < len(input) - 1:
            adjacent_characters = input[i + 1][search_col_start:search_col_end]
            if any ([s in adjacent_characters for s in symbols]):
                part_numbers.append(int(n.group(0)))
                continue
        if n.span()[0] > 0 and row[search_col_start] in symbols:
            part_numbers.append(int(n.group(0)))
            continue
        if n.span()[1] < len(input[0]) - 1 and row[search_col_end - 1] in symbols:
            part_numbers.append(int(n.group(0)))
            continue
#print(part_numbers)
print("Part 1: Sum of part numbers:", sum(part_numbers))

# Part 2
numbers_adjacent_to_potential_gears = {}
for i, row in enumerate(input):
    numbers = re.finditer("([0-9]+)", row)
    for n in numbers:
        search_row_start = max(0, i - 1)
        search_row_end= min(len(input), i + 2)
        search_col_start = max(n.span()[0] - 1, 0)
        search_col_end = min(n.span()[1] + 1, len(input[0]))

        adjacent_gears = np.where(input_array[search_row_start: search_row_end, search_col_start: search_col_end] == '*')
        for x, y in zip(adjacent_gears[0], adjacent_gears[1]):
            gear_id = f'g_{x+search_row_start}_{y + search_col_start}'
            if gear_id not in numbers_adjacent_to_potential_gears.keys():
                numbers_adjacent_to_potential_gears[gear_id] = []
            numbers_adjacent_to_potential_gears[gear_id].append(int(n.group(0)))

gear_ratios = [v[0] * v[1] for _, v in numbers_adjacent_to_potential_gears.items() if len(v) == 2]
print("Part 2: Sum of gear ratios:", sum(gear_ratios))