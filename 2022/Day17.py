import numpy as np
import pandas as pd
from aocd import get_data
from tqdm import tqdm
def check_if_position_allowed(rock, top_left_row, top_left_col):
    # Check if rock can be placed in the given position
    # (Position given by coords of top left corner)

    # First check limits of map
    if top_left_row < 0:
        print("Not enough vertical space upwards to fit this rock.")
        return False
    if top_left_row + rock.shape[0] > chambers.shape[0]:
        return False
    if top_left_col < 0:
        return False
    if top_left_col + rock.shape[1] > chambers.shape[1]:
        return False

    # Now check if being placed in this new position won't make rock overlap with other objects
    temp = chambers[top_left_row:top_left_row + rock.shape[0],
        top_left_col: top_left_col + current_rock.shape[1]].copy()
    temp += current_rock

    # If any of the values in the chamber map are now 2 it means that this rock would now be overlaping another one
    # (Movement not allowed) Otherwise we can keep this movement
    if (temp == 2).any():
        return False
    else:
        return True

#jet_pattern = get_data(day=17)
with open("test_input.txt") as f:
    jet_pattern = f.read()

rocks = [np.array([[1, 1, 1, 1]]),
         np.array([[0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0]]),
         np.array([[0, 0, 1],
                   [0, 0, 1],
                   [1, 1, 1]]),
         np.array([[1],
                   [1],
                   [1],
                   [1]]),
         np.array([[1, 1],
                   [1, 1]])
         ]
chambers = np.zeros((5000, 7))
move_count = 0

height_sum = 0
heights = [0]
for rock_count in tqdm(range(100000)):

    current_rock = rocks[rock_count % 5]

    highest_rock_row = np.argmax(chambers.any(axis = 1))

    # Pos of top left
    if highest_rock_row == 0:
        highest_rock_row = chambers.shape[0]
    current_rock_row = highest_rock_row - 3 - current_rock.shape[0]
    current_rock_col = 2

    # While rock is falling
    while True:
        # Check if rock can be pushed by jet
        if jet_pattern[move_count%len(jet_pattern)] == ">":
            if check_if_position_allowed(current_rock, current_rock_row, current_rock_col + 1):
                current_rock_col += 1
        else:
            if check_if_position_allowed(current_rock, current_rock_row, current_rock_col - 1):
                current_rock_col -= 1
        move_count += 1

        # Check if it can move downward
        if check_if_position_allowed(current_rock, current_rock_row + 1, current_rock_col):
            current_rock_row += 1
        else:
            break
    chambers[current_rock_row:current_rock_row+current_rock.shape[0],
        current_rock_col:current_rock_col + current_rock.shape[1]] += current_rock
    heights.append(height_sum + chambers.shape[0] - np.argmax(chambers.any(axis = 1)))

    # Remove the lowest rows to reduce memory
    if np.argmax(chambers.any(axis = 1)) < 3000:
        height_sum += 500
        chambers = np.concatenate((np.zeros((500, 7)), chambers[:chambers.shape[0] - 500]))

print("Result:", height_sum + (chambers.shape[0] - np.argmax(chambers.any(axis = 1))))

## PART 2
# Find cycles in the height differences

total_n_rocks = 2022
height_diffs = pd.Series([heights[i] - heights[i-1] for i in range(1, len(heights))])
found_cycle_length = False
cycle_length = 0
cycle_height = 0
for rows_to_skip in [100, 200, 300]:
    for possible_cycle_length in range(1, 5000):
      sums = height_diffs.iloc[rows_to_skip:].rolling(possible_cycle_length).sum()
      if sums.nunique() == 1:#len(sums) > len(set(sums)) and len(set(sums)) <= 3:
        print("Found one. Factor:", possible_cycle_length, sums.unique())
        found_cycle_length = True
        cycle_length = possible_cycle_length
        cycle_height = sums.unique()[-1]
        break
    if found_cycle_length:
        break

height_of_skipped_rows = height_diffs[:rows_to_skip].sum()
n_full_cycles = np.floor((total_n_rocks - rows_to_skip) / cycle_length)
n_unaccounted_for_rocks = int(total_n_rocks - rows_to_skip - n_full_cycles*cycle_length)
full_height = height_of_skipped_rows + n_full_cycles*cycle_height + height_diffs[rows_to_skip: rows_to_skip+n_unaccounted_for_rocks].sum()

print("Result:", full_height)