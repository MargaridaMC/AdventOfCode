import argparse
from time import time

def read_data(day: int, sample: bool = False):
    if sample:
        with open(f"day{day}_test_input.txt") as f:
            data = f.read().splitlines()
    else:
        with open(f"day{day}_input.txt") as f:
            data = f.read().splitlines()
    return data

def import_code_part1(day):
    match day:
        case 1:
            from Day1 import part1
        case 2:
            from Day2 import part1
        case 3:
            from Day3 import part1
        case 4: 
            from Day4 import part1
        case 5:
            from Day5 import part1
        case 6:
            from Day6 import part1
        case 7:
            from Day7 import part1
        case 8:
            from Day8 import part1
        case 9:
            from Day9 import part1
        case 10:
            from Day10 import part1
        case 11:
            from Day11 import part1
        case 12:
            from Day12 import part1
        case 13:
            from Day13 import part1
        case 14:
            from Day14 import part1
        case 15:
            from Day15 import part1
        case 16:
            from Day16 import part1
        case 17:
            from Day17 import part1
        case 18:
            from Day18 import part1
        case 19:
            from Day19 import part1
        case 20:
            from Day20 import part1
        case 21:
            from Day21 import part1
        case 22:
            from Day22 import part1
        case 23:
            from Day23 import part1
        case 24:
            from Day24 import part1
        case 25:
            from Day25 import part1
    return part1

def import_code_part2(day):
    match day:
        case 1:
            from Day1 import part2
        case 2:
            from Day2 import part2
        case 3:
            from Day3 import part2
        case 4: 
            from Day4 import part2
        case 5:
            from Day5 import part2
        case 6:
            from Day6 import part2
        case 7:
            from Day7 import part2
        case 8:
            from Day8 import part2
        case 9:
            from Day9 import part2
        case 10:
            from Day10 import part2
        case 11:
            from Day11 import part2
        case 12:
            from Day12 import part2
        case 13:
            from Day13 import part2
        case 14:
            from Day14 import part2
        case 15:
            from Day15 import part2
        case 16:
            from Day16 import part2
        case 17:
            from Day17 import part2
        case 18:
            from Day18 import part2
        case 19:
            from Day19 import part2
        case 20:
            from Day20 import part2
        case 21:
            from Day21 import part2
        case 22:
            from Day22 import part2
        case 23:
            from Day23 import part2
        case 24:
            from Day24 import part2
        case 25:
            from Day25 import part2
    return part2

def run_w_time(func, data):
    start_time = time()
    result = func(data)
    end_time = time()
    return result, end_time - start_time

def main(day: int, sample: bool):

    data = read_data(day, sample)

    try:
        part1 = import_code_part1(day)
        part1_result, run_time = run_w_time(part1, data)
        print(f"Part 1 result: {part1_result}")
        print(f"Running time: {run_time:.3f}s")
        print()
    except ImportError:
        print(f"Day {day} part 1 not implemented")
        return
    
    try:
        part2 = import_code_part2(day)
        part2_result, run_time = run_w_time(part2, data)
        print(f"Part 2 result: {part2_result}")
        print(f"Running time: {run_time:.3f}s")
    except ImportError:
        print(f"Day {day} part 2 not implemented")
        return
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--day", "-d", type=int)
    args = parser.parse_args()

    main(args.day, args.sample)