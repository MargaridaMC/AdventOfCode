from string import ascii_lowercase, ascii_uppercase
from aocd import get_data

input = get_data(day=3).splitlines()

# Question 1
running_sum = 0
LETTERS = {**{letter: index for index, letter in enumerate(ascii_lowercase, start=1)},
           **{letter: index for index, letter in enumerate(ascii_uppercase, start=27)}}

for rucksack in input:
    n_items = len(rucksack)
    compartment1 = rucksack[:int(n_items / 2)]
    compartment2 = rucksack[int(n_items / 2):]
    assert len(compartment1) == len(compartment2)

    repeated_items = set(compartment1).intersection(set(compartment2))
    assert len(repeated_items) == 1

    running_sum += LETTERS[list(repeated_items)[0]]

print("Part 1 total sum:", running_sum)

# Question 2
running_sum = 0

for index in range(0, len(input), 3):
    group_rucksacks = input[index: index + 3]
    badge_item_type = set(group_rucksacks[0]).intersection((group_rucksacks[1])).intersection(group_rucksacks[2])
    assert len(badge_item_type) == 1

    running_sum += LETTERS[list(badge_item_type)[0]]

print("Part 2 total sum:", running_sum)
