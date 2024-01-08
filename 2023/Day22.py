from aocd import get_data
from time import time
import numpy as np
from tqdm import tqdm
import string
import re

start_time = time()

def parse_input(input):
    blocks = dict()
    letter_ids = list(string.ascii_uppercase)
    if len(letter_ids) < len(input):
        rep = 1
        while len(letter_ids) < len(input):
            letter_ids += [l + str(rep) for l in string.ascii_uppercase]
            rep += 1
    for row, letter in zip(input, letter_ids):
        m = re.match("([0-9]+),([0-9]+),([0-9]+)~([0-9]+),([0-9]+),([0-9]+)", row)
        start_x, start_y, start_z, end_x, end_y, end_z = [int(m.group(i)) for i in range(1, 7)]
        blocks[letter] = (start_x, start_y, start_z, end_x, end_y, end_z)
    return blocks

def setup_block_map(blocks):
    max_x, max_y = 10, 10
    max_z = 380
    block_map = np.full((max_x, max_y, max_z), '', dtype = np.dtype('U100'))
    for letter, b in blocks.items():
        if b[3] > max_x or b[4] > max_y or b[5] > max_z:
            raise ValueError(f"Found value bigger than map: {b}")
        set_map_value(block_map, b, letter)
    return block_map

def get_new_block_position(block_map, block_coords, letter_id):
    start_x, start_y, start_z, end_x, end_y, end_z = block_coords
    
    # If the block is already in the bottommost row then it cannot fall anymore
    if start_z == 1 or end_z == 1:
        return block_coords
    
    # Check the row below the block. If there is any block there then it cannot move (we also need to consider the block itself being marked in the map)
    if not np.logical_or(block_map[start_x: end_x+1, start_y:end_y+1, start_z-1:end_z] == '', block_map[start_x: end_x+1, start_y:end_y+1, start_z-1:end_z] == letter_id).all():
        return block_coords
    else:
        return (start_x, start_y, start_z-1, end_x, end_y, end_z-1)

def set_map_value(m, coords, value):
    start_x, start_y, start_z, end_x, end_y, end_z = coords
    m[start_x:end_x+1, start_y:end_y+1, start_z:end_z+1] = value

def drop_all_blocks(block_map, blocks):

    count_moved_blocks = 0

    # Go row by row and drop the blocks
    for row in range(block_map.shape[-1]):
        blocks_in_row = [l for l in np.unique(block_map[:, :, row]) if l != '']

        for letter in blocks_in_row:
            block_moved = False
            while True:
                old_coords = blocks[letter]
                new_coords = get_new_block_position(block_map, old_coords, letter)
                if new_coords != old_coords:                
                    blocks[letter] = new_coords
                    set_map_value(block_map, old_coords, '')
                    set_map_value(block_map, new_coords, letter)
                    block_moved = True
                    # os.system('cls')
                    # print_block_slice(block_map)
                    # print()
                    # print_block_slice(block_map, False)
                    # print()
                    # break
                else:
                    break
            if block_moved:
                count_moved_blocks += 1
    return block_map, blocks, count_moved_blocks

def check_any_block_falls(block_map, blocks):
    for letter, b in blocks.items():
        new_block_coords = get_new_block_position(block_map, b, letter)
        if new_block_coords != b:
            return True
    return False

def check_if_block_can_be_removed(block_map, block_letter, block_dict):
    block_map_without_block = block_map.copy()
    b = block_dict[block_letter]
    set_map_value(block_map_without_block, b, '')
    # We don't need to check all blocks, just the ones on the row above this one
    upper_row_blocks = set([block_map[c[0], c[1], b[5] + 1] for c in np.argwhere(block_map[:, :, b[5] + 1] != '') ])
    upper_row_blocks = {l for l in upper_row_blocks if l != block_letter}
    for letter in upper_row_blocks:
        old_coords = block_dict[letter]
        new_coords = get_new_block_position(block_map_without_block, old_coords, letter)
        if old_coords != new_coords:
            return False
    return True

def print_block_slice(block_map, x_slice = True):
    if x_slice:
        _, n_cols, n_rows = block_map.shape
        for r in range(n_rows)[::-1]:
            for c in range(n_cols):
                if (block_map[:, c, r] == '').all():
                    print(".", end='')
                else:
                    first_letter = block_map[np.argmax(block_map[:, c, r] != ''), c, r]
                    print(first_letter, end = '')
            print()

    else:

        n_cols, _, n_rows = block_map.shape
        for r in range(n_rows)[::-1]:
            for c in range(n_cols):
                if (block_map[c, :, r] == '').all():
                    print(".", end='')
                else:
                    first_letter = block_map[c, np.argmax(block_map[c, :, r] != ''), r]
                    print(first_letter, end = '')
            print()


"""
with open("input.txt", "r") as f:
    input = f.read().splitlines()
"""
input = get_data(day=22).splitlines()


blocks = parse_input(input)
block_map = setup_block_map(blocks)
# print_block_slice(block_map)
# print()
# print_block_slice(block_map, False)

# Drop the blocks once
block_map, blocks, _ = drop_all_blocks(block_map, blocks)
# print()
# print_block_slice(block_map)
# print()
# print_block_slice(block_map, False)

# Check if we can remove any block
"""
desintegrateable_block_count = 0
for l in tqdm(blocks.keys()):
    desintegrate_block = check_if_block_can_be_removed(block_map, l, blocks)
    if desintegrate_block: 
        desintegrateable_block_count += 1

print(f"Part 1: N blocks which are safe to desintegrate: {desintegrateable_block_count}")
"""

fallen_brick_count = dict()
for block_letter in tqdm(blocks.keys()):
    block_map_without_block = block_map.copy()
    block_dict_without_block = {l:b for l, b in blocks.items() if l != block_letter}
    b = blocks[block_letter]
    set_map_value(block_map_without_block, b, '')
    _, _, count = drop_all_blocks(block_map_without_block, block_dict_without_block)
    fallen_brick_count[block_letter] = count

print("Part 2:", sum(fallen_brick_count.values()))

end_time = time()

print(f"Calculated solution in {end_time - start_time} seconds")
