from aocd import get_data
"""
input = ['0 3 6 9 12 15',
'1 3 6 10 15 21',
'10 13 16 21 30 45']"""
input = get_data(day=9).splitlines()
input = [list(map(int, row.split(" "))) for row in input]

def predict_next_value(value_hist):
    if set(value_hist) == {0}:
        return 0
    diff = [value_hist[i+1] - value_hist[i] for i in range(len(value_hist) - 1)]
    return predict_next_value(diff) + value_hist[-1]

next_values = [predict_next_value(row) for row in input]
#print(next_values)
print("Part 1: sum of next values:", sum(next_values))

def predict_previous_value(value_hist):
    if set(value_hist) == {0}:
        return 0
    diff = [value_hist[i+1] - value_hist[i] for i in range(len(value_hist) - 1)]
    return value_hist[0] - predict_previous_value(diff)
previous_values = [predict_previous_value(row) for row in input]
#print(previous_values)
print("Part 2: sum of previous values:", sum(previous_values))