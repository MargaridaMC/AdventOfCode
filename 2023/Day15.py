from aocd import get_data
from time import time

start_time = time()
"""
with open("input.txt", "r") as f:
    input = f.read().splitlines()[0]
"""
input = get_data(day=15).splitlines()[0]


initialization_sequence = input.split(",")

"""
Calculate hash:
Determine the ASCII code for the current character of the string.
Increase the current value by the ASCII code you just determined.
Set the current value to itself multiplied by 17.
Set the current value to the remainder of dividing itself by 256.
"""

def calculate_hash(s):
    current_value = 0
    for letter in s:
        ascii = ord(letter)    
        current_value += ascii
        current_value *= 17
        current_value = current_value%256
    return current_value

hash_list = [calculate_hash(step) for step in initialization_sequence]
print("Part1: Hash sum:", sum(hash_list))
end_time = time()
#rint(f"Calculated part 1 solution in {end_time - start_time} seconds")

## Part 2

def check_label_in_box(label, box):
    return len([lens for lens in box if lens[0] == label]) > 0

start_time = time()
boxes = [[] for _ in range(256)]
for step in initialization_sequence:
    label, focal_length = step.split("=") if "=" in step else step.split("-")
    hash = calculate_hash(label)
    box = boxes[hash]
    if '-' in step:
        if check_label_in_box(label, box):
            boxes[hash] = [lens for lens in box if lens[0] != label]
        else:
            pass
    elif '=' in step:
        focal_length = int(focal_length)
        if check_label_in_box(label, box):
            boxes[hash] = [lens if lens[0] != label else (label, focal_length) for lens in box]
        else:
            boxes[hash].append((label, focal_length))

total_focal_power = 0
for i, box in enumerate(boxes):
    total_focal_power += (i+1) * sum([(j + 1) * lens[1] for j, lens in enumerate(box)])

print(f"Part 2: total focal power:", total_focal_power)
end_time = time()
print(f"Calculated part 2 solution in {end_time - start_time} seconds")