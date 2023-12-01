from aocd import get_data
from itertools import combinations
import numpy as np

numbers = list(map(int, get_data(day=1, year=2020).splitlines()))
#with open("../test_input.txt") as f:
#    numbers = list(map(int, f.read().splitlines()))

pairs_of_numbers = list(combinations(numbers, 2))
sum_of_pairs = np.array(list(map(sum, pairs_of_numbers)))
result_pair = pairs_of_numbers[np.argmax(sum_of_pairs == 2020)]

print("Part 1 result:", result_pair[0] * result_pair[1])

pairs_of_numbers = list(combinations(numbers, 3))
sum_of_pairs = np.array(list(map(sum, pairs_of_numbers)))
result_triple = pairs_of_numbers[np.argmax(sum_of_pairs == 2020)]

print("Part 2 result:", result_triple[0] * result_triple[1] * result_triple[2])