from enum import Enum, auto
import numpy as np
from tqdm import tqdm

from data_parsing import parse_input_to_np_2d_array
from common_methods import get_shortest_path_from_matrix, check_map_value_in_pos

class MapValues(Enum):
    WALL = 1
    TRACK = 0
    START = auto()
    END = auto()

def parse_input(data):

    for str_value, enum_value in {'#': MapValues.WALL, '.': MapValues.TRACK, 'S': MapValues.START, 'E': MapValues.END}.items():
        data = data.replace(str_value, str(enum_value.value))

    race_map = parse_input_to_np_2d_array(data, convert_to_int=True)
    return race_map
    
def get_cheats_w_n_steps(race_map, race_path, n):
    """
    Gets the start and end position of all cheats
    """

    def get_locations_accessible_in_n_steps(start_pos, race_map, n):
        """
        Get all the locations that can be reached in n steps from start_pos
        """
        locations = []
        for i, j in zip(range(-n, n+1), list(reversed(range(-n, 1))) + list(range(-n + 1, 1))):
            if check_map_value_in_pos(start_pos[0] + i, start_pos[1] + j, race_map, MapValues.TRACK.value):
                locations.append((start_pos[0] + i, start_pos[1] + j))
        for i, j in zip(range(-n, n+1), list(range(0, n + 1)) + list(reversed(range(0, n)))):
            if check_map_value_in_pos(start_pos[0] + i, start_pos[1] + j, race_map, MapValues.TRACK.value):
                locations.append((start_pos[0] + i, start_pos[1] + j))
        return locations


    cheats = set()
    for i, (x, y) in enumerate(tqdm(race_path)):
        accessible_locations = get_locations_accessible_in_n_steps((x, y), race_map, n)
        for next_position in accessible_locations:
            if next_position in race_path[i+1:]:
                jumped_pos = race_path.index(next_position)
                cheats.add((i, jumped_pos))

    return cheats

def run(data, max_cheat_len, saving_lower_bound):
    race_map = parse_input(data)
    start_pos = list(zip(*np.where(race_map == MapValues.START.value)))[0]
    end_pos = list(zip(*np.where(race_map == MapValues.END.value)))[0]
    race_map[start_pos] = MapValues.TRACK.value
    race_map[end_pos] = MapValues.TRACK.value

    # First of all get the length of the shortest path between the start and end positions
    # Given the setup of the map, there is only one possible path anyway, but it's helpful to know the order in which the positions are visited
    shortest_path = get_shortest_path_from_matrix(race_map, start_pos, end_pos)

    # Now we try to cheat in each of the track positions
    pico_seconds_saved = []
    for c in range(2, max_cheat_len + 1):
        print(f"Checking for cheats with {c} steps")
        for start_idx, end_idx in get_cheats_w_n_steps(race_map, shortest_path, c):
            pico_seconds_saved.append(end_idx - start_idx - c)
    
    return sum(s >= saving_lower_bound for s in pico_seconds_saved)

def part1(data):
    return run(data, 2, 100)

def part2(data):
    return run(data, 20, 100)