import re

from aocd import get_data
from itertools import combinations
import numpy as np

lines = get_data(day=2, year=2020).splitlines()
#with open("../test_input.txt") as f:
#    lines = f.read().splitlines()

## PART 1
valid_password_count = 0
for line in lines:
    match = re.match("(\d+)-(\d+) ([a-z]): ([a-z]+)", line)
    min_count, max_count, letter, password = match.groups()

    if password.count(letter) in range(int(min_count), int(max_count) + 1):
        valid_password_count += 1

print("Part 1 total valid passwords:", valid_password_count)

## PART 2
valid_password_count = 0
for line in lines:
    match = re.match("(\d+)-(\d+) ([a-z]): ([a-z]+)", line)
    first_pos, second_pos, letter, password = match.groups()

    if (password[int(first_pos) - 1] == letter or password[int(second_pos) - 1] == letter) and not (password[int(first_pos) - 1] == letter and password[int(second_pos) - 1] == letter):
        valid_password_count += 1

print("Part 2 total valid passwords:", valid_password_count)