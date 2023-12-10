from aocd import get_data
"""
input = ['RL',
'',
'AAA = (BBB, CCC)',
'BBB = (DDD, EEE)',
'CCC = (ZZZ, GGG)',
'DDD = (DDD, DDD)',
'EEE = (EEE, EEE)',
'GGG = (GGG, GGG)',
'ZZZ = (ZZZ, ZZZ)']
"""
"""
input = ['LLR',
'',
'AAA = (BBB, BBB)',
'BBB = (AAA, ZZZ)',
'ZZZ = (ZZZ, ZZZ)']"""
input = get_data(day=8).splitlines()

instructions = input[0]
network = input[2:]
 
# For easier handling convert all 3 letter nodes into ints
letter_id_mapping = {node[:3]: i for i, node in enumerate(network)}
zzz_node_id = letter_id_mapping['ZZZ']
for letter, id in letter_id_mapping.items():
    network = [node.replace(letter, str(id)) for node in network]

# Organize the network such that it is just a list of tuples of ints (right and left for each node)
network = [eval(node.split("= ")[1]) for node in network]

current_position = letter_id_mapping["AAA"]
instruction_count = 0
while current_position != zzz_node_id:
    if instructions[instruction_count%len(instructions)] == 'R':
        current_position = network[current_position][1]
    else:
        current_position = network[current_position][0]
    instruction_count += 1

print("Part1: Number of instructions:", instruction_count)