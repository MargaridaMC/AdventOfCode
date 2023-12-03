from aocd import get_data
import re
"""
input = ['Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green']
"""
input = get_data(day=2).splitlines()

# only 12 red cubes, 13 green cubes, and 14 blue cubes?

def parse_single_set(s):
    red_matches = re.search("([0-9]+) red", s)
    green_matches = re.search("([0-9]+) green", s)
    blue_matches = re.search("([0-9]+) blue", s)

    red_count = int(red_matches.group(1)) if red_matches is not None else 0
    green_count = int(green_matches.group(1)) if green_matches is not None else 0
    blue_count = int(blue_matches.group(1)) if blue_matches is not None else 0

    return (red_count, green_count, blue_count)

max_red_cubes = 12
max_green_cubes = 13
max_blue_cubes = 14
allowed_games = []
for i, game in enumerate(input):
    game = game.split(": ")[1].split(";")
    cube_count = list(map(parse_single_set, game))
    
    if all([l[0] <= max_red_cubes for l in cube_count]) and all([l[1] <= max_green_cubes for l in cube_count]) and all([l[2] <= max_blue_cubes for l in cube_count]):
        allowed_games.append(i + 1)

print("Part 1: Sum of IDs of allowed games:", sum(allowed_games))

# Part 2
cube_count_per_game = [[parse_single_set(set) for set in game] for game in [game.split(": ")[1].split(";") for game in input] ]
min_n_cubes_per_game = [(max(l[0] for l in game), max(l[1] for l in game), max(l[2] for l in game)) for game in cube_count_per_game]
powers = [game[0] * game[1] * game[2] for game in min_n_cubes_per_game]
print("Part 2: Sum of powers:", sum(powers))