import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--sample", action="store_true")
args = parser.parse_args()

if args.sample:
    with open("day2_test_input.txt") as f:
        data = f.read().splitlines()
else:
    with open("day2_input.txt") as f:
        data = f.read().splitlines()
data = list(list(map(int, row.split(" "))) for row in data)

def check_report_is_safe(report):
    consecutive_diff = np.array(report[1:]) - np.array(report[:-1])
    return (all(consecutive_diff >= 1) and all(consecutive_diff <= 3)) or (all(consecutive_diff >= -3) and all(consecutive_diff <= -1))

# Part 1
safe_count = 0
for report in data:
    if check_report_is_safe(report):
        safe_count += 1
print(f"Part 1 solution: {safe_count}")

# Part 2
safe_count = 0
for report in data:
    if check_report_is_safe(report):
        safe_count += 1
    else:
        for i in range(len(report)):
            report_copy = report[:i] + report[i+1:]
            if check_report_is_safe(report_copy):
                safe_count += 1
                break
print(f"Part 2 solution: {safe_count}")