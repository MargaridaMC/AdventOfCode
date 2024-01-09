from aocd import get_data
from time import time
import numpy as np
import re
start_time = time()
"""
with open("input.txt", "r") as f:
    input = f.read().splitlines()
"""
input = get_data(day=24).splitlines()

min_position = 200000000000000#7
max_position = 400000000000000#27

count = 0
for i, row1 in enumerate(input):
    m1 = re.match("([\-0-9]+), ([\-0-9]+), ([\-0-9]+) @ ([\-0-9]+), ([\-0-9]+), ([\-0-9]+)", row1.replace("  ", " "))
    x1, y1, z1, vx1, vy1, vz1 = [int(v) for v in m1.groups()]
    for row2 in input[i+1:]:
        m2 = re.match("([\-0-9]+), ([\-0-9]+), ([\-0-9]+) @ ([\-0-9]+), ([\-0-9]+), ([\-0-9]+)", row2.replace("  ", " "))
        x2, y2, z2, vx2, vy2, vz2 = [int(v) for v in m2.groups()]

        A = np.array([[vx1, -vx2], [vy1, -vy2]])
        b = np.array([x2 - x1, y2 - y1])
        try:
            t = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            continue

        if t[0] < 0 or t[1] < 0:
            continue

        collision_x = x1 + vx1*t[0]
        collision_y = y1 + vy1*t[0]
        if min_position <= collision_x <= max_position and min_position <= collision_y <= max_position:
             count += 1

print("Part 1:", count)

end_time = time()

print(f"Calculated solution in {end_time - start_time} seconds")