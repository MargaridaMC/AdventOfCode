import re
import numpy as np
import math

def parse_input(data, part1 = True):
    """
    Example block:

    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400
    """

    configurations_and_prizes = data.split("\n\n")

    configurations = []
    prizes = []

    for cp in configurations_and_prizes:
        parts = cp.splitlines()

        configuration_buttons = []
        for conf in parts[:2]:
            match = re.match("Button [AB]: X\+(\d+), Y\+(\d+)", conf)
            configuration_buttons.append((int(match.group(1)), int(match.group(2))))

        configurations.append(configuration_buttons)
        
        match = re.match("Prize: X=(\d+), Y=(\d+)", parts[-1])
        if part1:
            prizes.append((int(match.group(1)), int(match.group(2))))
        else:
            prizes.append((10000000000000 + int(match.group(1)), 10000000000000 + int(match.group(2))))

    return configurations, prizes

def get_token_cost(buttons, prize_locations):
    token_cost = 0

    for button_conf, loc in zip(buttons, prize_locations):
        a = np.array([[button_conf[0][0], button_conf[1][0]], [button_conf[0][1], button_conf[1][1]]])
        b = np.array([loc[0], loc[1]])
        solution = np.linalg.solve(a, b)

        diff0 = float(solution[0]) - round(solution[0])
        diff1 = float(solution[1]) - round(solution[1])
        if math.isclose(diff0, 0, rel_tol = 1e-4, abs_tol=1e-4) and math.isclose(diff1, 0, rel_tol = 1e-4, abs_tol=1e-4):
            token_cost += (3 * solution[0] + solution[1])

    return token_cost

def part1(data):
    buttons, prize_locations = parse_input(data)
    return get_token_cost(buttons, prize_locations)

def part2(data):
    buttons, prize_locations = parse_input(data, False)
    return get_token_cost(buttons, prize_locations)
