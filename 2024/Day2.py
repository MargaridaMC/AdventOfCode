
import numpy as np

def check_report_is_safe(report):
    consecutive_diff = np.array(report[1:]) - np.array(report[:-1])
    return (all(consecutive_diff >= 1) and all(consecutive_diff <= 3)) or (all(consecutive_diff >= -3) and all(consecutive_diff <= -1))

def parse_data(data):
    return list(list(map(int, row.split(" "))) for row in data.splitlines())

def part1(data):

    data = parse_data(data)

    # Part 1
    safe_count = 0
    for report in data:
        if check_report_is_safe(report):
            safe_count += 1

    return safe_count

def part2(data):
    
    data = parse_data(data)

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
    
    return safe_count