import re

def part1(data):

    # Extract relevant matches from the input string
    matches = re.findall(r"mul\(\d+,\d+\)", data)

    # Multiply the two numbers in each match and sum the results
    result = 0
    for match in matches:
        a, b = map(int, match[4:-1].split(","))
        result += a * b
    return result

def part2(data):

    matches = re.findall(r"(mul\(\d+,\d+\)|do\(\)|don't\(\))", data)
    result = 0
    do = True
    for match in matches:
        if "mul" in match and do:
            a, b = map(int, match[4:-1].split(","))
            result += a * b
        elif "don't" in match:
            do = False
        elif "do" in match:
            do = True
    return result