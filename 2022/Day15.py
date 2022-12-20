import math

from aocd import get_data
import re
import numpy as np
from tqdm import tqdm

SENSOR = 1
BEACON = 2
AREA_W_NO_BEACONS = 3

def contains(sensor1, radius1, sensor2, radius2):
  d = math.sqrt(
        (sensor2[0] - sensor1[0]) ** 2 +
        (sensor2[1] - sensor1[1]) ** 2)
  return radius1  > (d + radius2)

def read_lines(lines):
    sensor_and_radius = dict()
    beacon_coords = []

    for line in lines:
        match = re.match(r"Sensor at x=(\d+), y=(\d+): closest beacon is at x=(\d+), y=(\d+)", line)
        if match:
            sensor_col, sensor_row, beacon_col, beacon_row = match.groups()
            sensor_col, sensor_row, beacon_col, beacon_row = int(sensor_col), int(sensor_row), int(beacon_col), int(
                beacon_row)
            beacon_coords.append((beacon_row, beacon_col))
            sensor_and_radius[(sensor_row, sensor_col)] = abs(sensor_row - beacon_row) + abs(sensor_col - beacon_col)

    return sensor_and_radius, beacon_coords

def build_sensor_map_per_row(test_row_idx, sensor_and_radius, start_col, end_col):
    sensor_beacon_map = np.zeros(end_col - start_col)

    for sensor_idx, (sensor, radius) in enumerate(tqdm(sensor_and_radius.items())):
        if sensor[0] - radius >= test_row_idx or sensor[0] + radius < test_row_idx:
            continue
        for col in range(start_col, end_col):
            if abs(test_row_idx - sensor[0]) + abs(col - sensor[1]) <= radius:
                sensor_beacon_map[col] = AREA_W_NO_BEACONS
        if sensor[0] == test_row_idx:
            sensor_beacon_map[sensor[1]] = SENSOR
        beacon = beacon_coords[sensor_idx]
        if beacon[0] == test_row_idx:
            sensor_beacon_map[beacon[1]] = BEACON
    return sensor_beacon_map

lines = get_data(day=15).splitlines()
#with open("test_input.txt") as f:
#    lines = f.read().splitlines()


sensor_and_radius, beacon_coords = read_lines(lines)
sensors_to_ignore = set()
for sensor1, radius1 in sensor_and_radius.items():
    for sensor2, radius2 in sensor_and_radius.items():
        if sensor1 == sensor2:
            continue
        if contains(sensor1, radius1, sensor2, radius2):
            #print(f"Sensor at {sensor1} (radius: {radius1}) fully encloses sensor at {sensor2} (radius: {radius2})")
            sensors_to_ignore.add(sensor2)

sensor_and_radius = {k:v for k,v in sensor_and_radius.items() if k not in sensors_to_ignore}

## PART 1
sensor_beacon_map = build_sensor_map_per_row(2000000, sensor_and_radius, -2000000, 6000000)
print("Number of positions where there can be no more beacons:", (sensor_beacon_map == AREA_W_NO_BEACONS).sum())

## PART 2
def check_if_point_outside_any_sensor_area(row, col):

    for sensor2, radius2 in sensor_and_radius.items():
        if abs(sensor2[0] - row) + abs(sensor2[1] - col) <= radius2:
            return False
    return True

def check_no_adjacent_cells_are_free(row, col):
    if check_if_point_outside_any_sensor_area(row - 1, col):
        return False
    if check_if_point_outside_any_sensor_area(row + 1, col):
        return False
    if check_if_point_outside_any_sensor_area(row, col + 1):
        return False
    if check_if_point_outside_any_sensor_area(row, col - 1):
        return False
    return True

max_pos = 4000000
min_reasonable_position = 3000000
max_reasonable_position = 4000000
row, col = 0, 0
for sensor1, radius1 in tqdm(sensor_and_radius.items()):
    found_right_positions = False

    # Check top right corner
    for i in range(radius1 + 2):
        col = sensor1[1] + i
        if col < min_reasonable_position or col > max_reasonable_position: continue
        row = sensor1[0] - (radius1 + 1 - i)
        if row < min_reasonable_position or col > max_reasonable_position: continue
        found_right_positions = check_if_point_outside_any_sensor_area(row, col) and check_no_adjacent_cells_are_free(row, col)
        if found_right_positions:
            freq = col * 4000000 + row
            print(f"Found beacon at x = {col}, y = {row}, frequency: {freq}")
            break
    if found_right_positions:
       break

    # Check bottom right corner
    for i in range(radius1 + 1):
        col = sensor1[1] + i
        if col < min_reasonable_position or col > max_reasonable_position: continue
        row = sensor1[0] + (radius1 + 1 - i)
        if row < min_reasonable_position or col > max_reasonable_position: continue
        found_right_positions = check_if_point_outside_any_sensor_area(row, col) and check_no_adjacent_cells_are_free(row, col)
        if found_right_positions:
            freq = col * 4000000 + row
            print(f"Found beacon at x = {col}, y = {row}, frequency: {freq}")
            break
    if found_right_positions:
        break

    # Check top left corner
    for i in range(1, radius1 + 2):
        col = sensor1[1] - i
        if col < min_reasonable_position or col > max_reasonable_position: continue
        row = sensor1[0] - (radius1 + 1 - i)
        if row < min_reasonable_position or col > max_pos: continue
        found_right_positions = check_if_point_outside_any_sensor_area(row, col) and check_no_adjacent_cells_are_free(row, col)
        if found_right_positions:
            freq = col * 4000000 + row
            print(f"Found beacon at x = {col}, y = {row}, frequency: {freq}")
            break
    if found_right_positions:
        break

    # Check bottom left corner
    for i in range(1, radius1 + 1):
        col = sensor1[1] - i
        if col < min_reasonable_position or col > max_reasonable_position: continue
        row = sensor1[0] + (radius1 + 1 - i)
        if row < min_reasonable_position or col > max_reasonable_position: continue
        found_right_positions = check_if_point_outside_any_sensor_area(row, col) and check_no_adjacent_cells_are_free(row, col)
        if found_right_positions:
            freq = col * 4000000 + row
            print(f"Found beacon at x = {col}, y = {row}, frequency: {freq}")
            break
    if found_right_positions:
        break