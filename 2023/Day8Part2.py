from aocd import get_data
from functools import reduce # Valid in Python 2.6+, required in Python 3
import operator

"""
input = ['LR',
'',
'11A = (11B, XXX)',
'11B = (XXX, 11Z)',
'11Z = (11B, XXX)',
'22A = (22B, XXX)',
'22B = (22C, 22C)',
'22C = (22Z, 22Z)',
'22Z = (22B, 22B)',
'XXX = (XXX, XXX)']"""
input = get_data(day=8).splitlines()

instructions = input[0]
network = input[2:]
 
# For easier handling convert all 3 letter nodes into ints
letter_id_mapping = {node[:3]: i for i, node in enumerate(network)}
zzz_node_ids = [id for letter, id in letter_id_mapping.items() if letter[-1] == 'Z']
for letter, id in letter_id_mapping.items():
    network = [node.replace(letter, str(id)) for node in network]

# Organize the network such that it is just a list of tuples of ints (right and left for each node)
network = [eval(node.split("= ")[1]) for node in network]

first_z_positions_per_start_pos = []
for start_postition in [id for letter, id in letter_id_mapping.items() if letter[-1] == 'A']:
    instruction_count = 0
    current_position = start_postition
    while current_position not in zzz_node_ids:
        if instructions[instruction_count%len(instructions)] == 'R':
            current_position = network[current_position][1]
        else:
            current_position = network[current_position][0]
        instruction_count += 1
    first_z_positions_per_start_pos.append(instruction_count)

print("Part2: Least common multiple:", reduce(operator.mul, [pos / len(instructions) for pos in first_z_positions_per_start_pos], 1) * len(instructions))

