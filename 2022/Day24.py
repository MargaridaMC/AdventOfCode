from dataclasses import dataclass
from telegram import SendTelegramMessage
import numpy as np
from aocd import get_data
from tqdm import tqdm

#lines = get_data(day=24).splitlines()
with open("test_input.txt") as f:
    lines = f.read().splitlines()

@dataclass
class Blizzard:
    direction: int
    start_row: int
    start_col: int
    def __copy__(self):
        return Blizzard(self.direction, self.start_row, self.start_col)

    def get_position_at_given_time(self, time_stamp, ground_map):

        map_n_rows_without_wall, map_n_cols_without_wall = ground_map.shape[0] - 2, ground_map.shape[1] - 2

        if self.direction == DIRECTION_RIGHT:
            relative_start_col = self.start_col - 1
            relative_end_col = (relative_start_col + time_stamp) % map_n_cols_without_wall
            return self.start_row, relative_end_col + 1
        elif self.direction == DIRECTION_DOWN:
            relative_start_row = self.start_row - 1
            relative_end_row = (relative_start_row + time_stamp) % map_n_rows_without_wall
            return relative_end_row + 1, self.start_col
        elif self.direction == DIRECTION_LEFT:
            relative_start_col = self.start_col - 1
            relative_end_col = (relative_start_col - time_stamp) % map_n_cols_without_wall
            return self.start_row, relative_end_col + 1
        else:
            relative_start_row = self.start_row - 1
            relative_end_row = (relative_start_row - time_stamp) % map_n_rows_without_wall
            return relative_end_row + 1, self.start_col

@dataclass
class State:
    minutes_past: int
    my_row: int
    my_col: int

GROUND = "."
WALL = "#"
DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3
WAIT = 4

ground_map = np.array([[letter for letter in line] for line in lines])
blizzards = []

up_blizzard_rows, up_blizzard_cols = np.where(ground_map=="^")
blizzards += [Blizzard(DIRECTION_UP, up_blizzard_rows[i], up_blizzard_cols[i]) for i in range(len(up_blizzard_rows))]
down_blizzard_rows, down_blizzard_cols = np.where(ground_map=="v")
blizzards += [Blizzard(DIRECTION_DOWN, down_blizzard_rows[i], down_blizzard_cols[i]) for i in range(len(down_blizzard_rows))]
left_blizzard_rows, left_blizzard_cols = np.where(ground_map=="<")
blizzards += [Blizzard(DIRECTION_LEFT, left_blizzard_rows[i], left_blizzard_cols[i]) for i in range(len(left_blizzard_rows))]
right_blizzard_rows, right_blizzard_cols = np.where(ground_map==">")
blizzards += [Blizzard(DIRECTION_RIGHT, right_blizzard_rows[i], right_blizzard_cols[i]) for i in range(len(right_blizzard_rows))]

def find_shortest_path_length(ground_map, start_row, start_col, end_row, end_col, start_time, max_time = 500):

    leaf_nodes = {(start_row, start_col)}
    all_nodes = []
    found_end_node = False
    shortest_time = np.inf

    for time in tqdm(range(max_time)):

        blizzard_positions_at_time_plus_one = set([b.get_position_at_given_time(start_time + time + 1, ground_map) for b in blizzards])

        new_leaf_nodes = set()

        for node in leaf_nodes:

            row, col = node
            if f"t{time}_{row}_{col}" in all_nodes:
                #print("Found a duplicate node", f"t{time}_{row}_{col}")
                continue
            all_nodes.append(f"t{time}_{row}_{col}")

            possible_movements = 0
            for move in [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]:
                possible_movements += 1
                new_row = row + move[0]
                new_col = col + move[1]
                if 0 <= new_row < ground_map.shape[0] and 0 <= new_col < ground_map.shape[1] and (new_row, new_col) not in blizzard_positions_at_time_plus_one and ground_map[new_row, new_col] != WALL:
                    new_leaf_nodes.add((new_row, new_col))
                    if new_row == end_row and new_col == end_col:
                        found_end_node = True
                        shortest_time = time + 1
                        break
            if found_end_node:
                break
        if found_end_node:
            break

        leaf_nodes = new_leaf_nodes.copy()

    return shortest_time

start_row = 0
start_col = 1
end_row = ground_map.shape[0] - 1
end_col = ground_map.shape[1] - 2

print("Looking for fastest path for first part of the path")
first_way = 373#260 #find_shortest_path_length(ground_map, start_row, start_col, end_row, end_col)
print(f"Fastest path found: {first_way} minutes")
SendTelegramMessage(f"Fastest path found: {first_way} minutes")

print("Looking for fastest path for second part of the path")
SendTelegramMessage("Looking for fastest path for second part of the path")
second_way = find_shortest_path_length(ground_map, end_row, end_col, start_row, start_col, start_time = first_way, max_time=1000)
print(f"Fastest path found: {second_way} minutes")
SendTelegramMessage(f"Fastest path found: {second_way} minutes")

print("Looking for fastest path for third part of the path")
SendTelegramMessage("Looking for fastest path for third part of the path")
third_way = find_shortest_path_length(ground_map, start_row, start_col, end_row, end_col, start_time = first_way + second_way, max_time=1000)
print(f"Fastest path found: {third_way} minutes")
SendTelegramMessage(f"Fastest path found: {third_way} minutes")

print(f"Total time spent going back and forward: {first_way + second_way + third_way} minutes")
