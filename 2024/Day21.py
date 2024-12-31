from itertools import pairwise, permutations
from tqdm import tqdm
from functools import cache
import numpy as np

def get_movement_combinations(button_mapping, unallowed_movements):
    movement_combinations = dict()
    for start_letter, unnallowed_movement in unallowed_movements.items():
        movement_combinations[start_letter] = dict()
        for next_letter in unallowed_movements.keys():
            next_letter = str(next_letter)
            if next_letter == start_letter:
                movement_combinations[start_letter][next_letter] = ['']
            else:
                possible_permutations = [''.join(instruction) for instruction in permutations(button_mapping[start_letter][next_letter]) ]
                movement_combinations[start_letter][next_letter] = [instruction for instruction in possible_permutations if unnallowed_movement is None or not instruction.startswith(unnallowed_movement)]
    return movement_combinations

NUMERIC_PAD_SHORTEST_PATHS = {'0': {'0': '', '1': '^<', '2': '^', '3': '^>', '4': '^^<', '5': '^^', '6': '^^>', '7': '^^^<', '8': '^^^', '9': '^^^>', 'A': '>'}, 
                              '1': {'0': '>v', '1': '', '2': '>', '3': '>>', '4': '^', '5': '^>', '6': '^>>', '7': '^^', '8': '^^>', '9': '^^>>', 'A': '>>v'}, 
                              '2': {'0': 'v', '1': '<', '2': '', '3': '>', '4': '<^', '5': '^', '6': '^>', '7': '^^<', '8': '^^', '9': '^^>', 'A': '>v'}, 
                              '3': {'0': '<v', '1': '<<', '2': '<', '3': '', '4': '<<^', '5': '<^', '6': '^', '7': '<<^^', '8': '<^^', '9': '^^', 'A': 'v'}, 
                              '4': {'0': '>vv', '1': 'v', '2': 'v>', '3': 'v>>', '4': '', '5': '>', '6': '>>', '7': '^', '8': '^>', '9': '^>>', 'A': '>>vv'}, 
                              '5': {'0': 'vv', '1': 'v<', '2': 'v', '3': 'v>', '4': '<', '5': '', '6': '>', '7': '^<', '8': '^', '9': '^>', 'A': '^vv'}, 
                              '6': {'0': 'vv<', '1': 'v<<', '2': 'v<', '3': 'v', '4': '<<', '5': '<', '6': '', '7': '<<^', '8': '<^', '9': '^', 'A': 'vv'}, 
                              '7': {'0': '>vvv', '1': 'vv', '2': 'vv>', '3': 'vv>>', '4': 'v', '5': 'v>', '6': 'v>>', '7': '', '8': '>', '9': '>>', 'A': '>>vvv'}, 
                              '8': {'0': 'vvv', '1': 'vv<', '2': 'vv', '3': 'vv>', '4': 'v<', '5': 'v', '6': 'v>', '7': '<', '8': '', '9': '>', 'A': '>vvv'}, 
                              '9': {'0': 'vvv<', '1': '<<vv', '2': '<vv', '3': 'vv', '4': '<<v', '5': '<v', '6': 'v', '7': '<<', '8': '<', '9': '', 'A': 'vvv'},
                              'A': {'0': '<', '1': '^<<', '2': '^<', '3': '^', '4': '^^<<', '5': '^^<', '6': '^^', '7': '^^^<<', '8': '^^^<', '9': '^^^', 'A': ''}
                              }
start_letter_and_unallowed_movement = {'0': '<', '1': 'v', '2': None, '3': None, '4': 'vv', '5': None, '6': None, '7': 'vvv', '8': None, '9': None, 'A': '<<'}
NUMERIC_PAD_SHORTEST_PATHS = get_movement_combinations(NUMERIC_PAD_SHORTEST_PATHS, start_letter_and_unallowed_movement)

DIRECTIONAL_PAD_SHORTEST_PATHS = {'<': {'<': '', '>': '>>', '^': '>^', 'v': '>', 'A': '>>^'},
                                  '>': {'<': '<<', '>': '', '^': '<^', 'v': '<', 'A': '^'},
                                 '^': {'<': 'v<', '>': 'v>', '^': '', 'v': 'v', 'A': '>'},
                                 'v': {'<': '<', '>': '>', '^': '^', 'v': '', 'A': '>^'},
                                 'A': {'<': 'v<<', '>': 'v', '^': '<', 'v': '<v', 'A': ''},
                                    }
start_letter_and_unallowed_movement = {'<': '^', '>': None, '^': '<', 'v': None, 'A': '<<'}
DIRECTIONAL_PAD_SHORTEST_PATHS = get_movement_combinations(DIRECTIONAL_PAD_SHORTEST_PATHS, start_letter_and_unallowed_movement)

def parse_input(data):
    codes = data.splitlines()
    return codes

@cache
def get_shortest_sequence_length(button_seq: str, depth: int, directional_pad_count = 2):
    if depth == directional_pad_count:
        return len(button_seq)
    
    result = 0
    #return sum([get_sequence_length(DIRECTIONAL_PAD_SHORTEST_PATHS[current_button][next_button] + "A", depth + 1, directional_pad_count) for current_button, next_button in pairwise("A" + button_seq)])
    for current_button, next_button in pairwise("A" + button_seq):
        shortest_length = np.inf
        for instruction in DIRECTIONAL_PAD_SHORTEST_PATHS[current_button][next_button]:
            t = get_shortest_sequence_length(instruction + "A", depth + 1, directional_pad_count)
            if t < shortest_length:
                shortest_length = t
        result += shortest_length
    return result

def run(data, directional_pad_count = 2):

    codes = parse_input(data)
    complexities = []

    for code in codes:

        # Get the first robot instrictuctions
        final_instruction_length = 0
        for current_button, next_button in pairwise("A" + code):
            shortest_seq_length = np.inf
            for instruction in NUMERIC_PAD_SHORTEST_PATHS[current_button][next_button]:
                t = get_shortest_sequence_length(instruction + "A", 0, directional_pad_count)
                if t < shortest_seq_length:
                    shortest_seq_length = t
            final_instruction_length += shortest_seq_length

        complexity = final_instruction_length * int(code[:-1])
        complexities.append(complexity)

    return sum(complexities)

def part1(data):
    return run(data, 2)

def part2(data):
    return run(data, 25)