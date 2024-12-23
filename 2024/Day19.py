from functools import cache

def parse_input(data):
    available_towel_patterns, desired_designs = data.split("\n\n")
    available_towel_patterns = tuple(available_towel_patterns.split(", "))
    desired_designs = desired_designs.splitlines()
    return available_towel_patterns, desired_designs

@cache
def count_possible_towel_combination(desired_design, available_towel_patterns, break_on_first_match=False):
    if len(desired_design) == 0:
        return 1
    
    local_count = 0
    for pattern in available_towel_patterns:
        if desired_design.startswith(pattern):
            temp = count_possible_towel_combination(desired_design[len(pattern):], available_towel_patterns, break_on_first_match)
            if temp > 0 and break_on_first_match:
                return temp
            local_count += temp

    return local_count

def part1(data):
    available_towel_patterns, desired_designs = parse_input(data)
    possible_design_count = 0
    for desired_design in desired_designs:
        if count_possible_towel_combination(desired_design, available_towel_patterns, break_on_first_match=True) > 0:
            possible_design_count += 1
    return possible_design_count

def part2(data):
    available_towel_patterns, desired_designs = parse_input(data)
    possible_design_count = 0
    for desired_design in desired_designs:
        possible_design_count += count_possible_towel_combination(desired_design, available_towel_patterns)
    return possible_design_count