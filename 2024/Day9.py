from dataclasses import dataclass
import numpy as np
from itertools import takewhile, dropwhile

@dataclass
class Block:
    id: int
    size: int
    space_to_right: int

def parse_input(data):

    blocks = []
    for i in range(0, len(data), 2):
        space_to_right = int(data[i + 1]) if i < len(data) - 1 else 0
        blocks.append(Block(i//2, int(data[i]), space_to_right))

    return blocks

def calculate_checksum(blocks):
    checksum = 0
    i = 0
    for block in blocks:
        checksum += block.id * sum(range(i, i + block.size))
        i += (block.size + block.space_to_right)
    return checksum

def print_blocks(blocks):
    for block in blocks:
        print(str(block.id) * block.size, end = '')
        print('.' * block.space_to_right, end = '')
    print()

def check_file_system_is_compact(blocks):
    # Given our implementation, the filesystem is only compact when only the rightmost block has available space
    block_is_full = [b.space_to_right == 0 for b in blocks]
    return all(block_is_full[:-1])
    
def part1(data):
    blocks = parse_input(data)

    # Compact the filesystem
    while not check_file_system_is_compact(blocks):

        # Move the rightmost file 
        last_block = blocks[-1]
        first_block_w_space = np.argmax([b.space_to_right > 0 for b in blocks])
        if blocks[first_block_w_space].id == last_block.id:
            blocks[first_block_w_space].size += 1
            blocks[first_block_w_space].space_to_right -= 1
        else:
            new_block = Block(last_block.id, size = 1, space_to_right=blocks[first_block_w_space].space_to_right - 1)
            blocks.insert(first_block_w_space + 1, new_block)
            blocks[first_block_w_space].space_to_right = 0

        last_block.size -= 1
        if last_block.size == 0:
            blocks.pop()

        #print_blocks(blocks)

    return calculate_checksum(blocks)

def part2(data):
    blocks = parse_input(data)

    for block_to_move in blocks.copy()[::-1]:

        new_blocks = []

        for i, block in enumerate(blocks):
            if block.id == block_to_move.id:
                # We don't have a chance of moving it anymore
                new_blocks += blocks[i:]
                break

            new_blocks.append(block)
            if block.space_to_right >= block_to_move.size:
                space_gained_in_place_of_block = block_to_move.size + block_to_move.space_to_right
                block_to_move.space_to_right = new_blocks[-1].space_to_right - block_to_move.size
                new_blocks[-1].space_to_right = 0
                new_blocks.append(block_to_move)
                new_blocks += takewhile(lambda b: b.id != block_to_move.id, blocks[i + 1:])
                new_blocks[-1].space_to_right += space_gained_in_place_of_block
                new_blocks += list(dropwhile(lambda b: b.id != block_to_move.id, blocks))[1:]
                break
        
        #print_blocks(new_blocks)
        blocks = new_blocks.copy()
        
    return calculate_checksum(blocks)