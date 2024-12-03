from utils import get_arg_parser, read_data
import numpy as np

parser = get_arg_parser()
args = parser.parse_args()
data = read_data(2, args.sample)

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