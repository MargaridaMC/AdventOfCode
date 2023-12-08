from aocd import get_data
import math
import re
from functools import reduce 
import operator

input = ["Time:      7  15   30", 
"Distance:  9  40  200"]
input = get_data(day=6).splitlines()

times, dist_records = input
times = [int(s) for s in re.sub("\s+", " ", times).split(": ")[1].split(" ")]
dist_records = [int(s) for s in re.sub("\s+", " ", dist_records).split(": ")[1].split(" ")]

ways_to_beat_record = []

for time, dist in zip(times, dist_records):
    x0 = math.ceil((- time + math.sqrt(time**2 - 4*dist)) / (-2) + 0.00001)
    x1 = math.floor((- time - math.sqrt(time**2 - 4*dist)) / (-2) - 0.00001)    
    ways_to_beat_record.append(len(range(x0, x1 + 1)))

print(ways_to_beat_record)
print("Part 1:", reduce(operator.mul, ways_to_beat_record, 1))

# Part 2
time, dist = input
time = int(time.split(": ")[1].replace(" ", ""))
dist = int(dist.split(": ")[1].replace(" ", ""))

x0 = math.ceil((- time + math.sqrt(time**2 - 4*dist)) / (-2) + 0.00001)
x1 = math.floor((- time - math.sqrt(time**2 - 4*dist)) / (-2) - 0.00001)    
ways_to_beat_record = len(range(x0, x1 + 1))
print("Part 2: ways to beat:", ways_to_beat_record)