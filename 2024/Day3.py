from utils import get_arg_parser, read_data
import re

parser = get_arg_parser()
args = parser.parse_args()
data = read_data(3, args.sample)[0]

# Part 1
# Extract relevant matches from the input string
matches = re.findall(r"mul\(\d+,\d+\)", data)

# Multiply the two numbers in each match and sum the results
result = 0
for match in matches:
    a, b = map(int, match[4:-1].split(","))
    result += a * b
print("Part 1 solution:", result)

# Part 2
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
print("Part 2 solution:", result)