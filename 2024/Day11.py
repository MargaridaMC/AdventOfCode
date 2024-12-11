def parse_input(data):
    return list(map(int, data.splitlines()[0].split(' ')))

def transform_stone(number: int):
    if number == 0:
        return [1]
    elif len(str(number)) % 2 == 0:
        number_str = str(number)
        split_loc = len(number_str)//2
        return [int(number_str[:split_loc]), int(number_str[split_loc:])]
    else:
        return [number * 2024]

def run(data, n_blinks):
    stones = {s: 1 for s in parse_input(data)}

    for _ in range(n_blinks):
        new_stones = dict()
        for stone, repeat_count in stones.items():
            for new_stone in transform_stone(stone):
                new_stones[new_stone] = new_stones.get(new_stone, 0) + repeat_count
        stones = new_stones.copy()

    return sum(stones.values())

def part1(data):
    return run(data, 25)

def part2(data):
    return run(data, 75)