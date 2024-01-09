from aocd import get_data
from time import time
import re
from sympy import symbols, Eq, solve

start_time = time()
"""
with open("input.txt", "r") as f:
    input = f.read().splitlines()
"""
input = get_data(day=24).splitlines()

start_positions = []
velocities = []
for i, row1 in enumerate(input[:3]):
    m1 = re.match("([\-0-9]+), ([\-0-9]+), ([\-0-9]+) @ ([\-0-9]+), ([\-0-9]+), ([\-0-9]+)", row1.replace("  ", " "))
    x1, y1, z1, vx1, vy1, vz1 = [int(v) for v in m1.groups()]
    start_positions.append((x1, y1, z1))
    velocities.append((vx1, vy1, vz1))

x0, y0, z0, vx0, vy0, vz0, t0a, t0b, t0c = symbols('x0, y0, z0, vx0, vy0, vz0, t0a, t0b, t0c')
eqs = [Eq(x0 + vx0*t0a, start_positions[0][0] + velocities[0][0] * t0a),
            Eq(y0 + vy0*t0a, start_positions[0][1] + velocities[0][1] * t0a),
            Eq(z0 + vz0*t0a, start_positions[0][2] + velocities[0][2] * t0a),
            Eq(x0 + vx0*t0b, start_positions[1][0] + velocities[1][0] * t0b),
            Eq(y0 + vy0*t0b, start_positions[1][1] + velocities[1][1] * t0b),
            Eq(z0 + vz0*t0b, start_positions[1][2] + velocities[1][2] * t0b),
            Eq(x0 + vx0*t0c, start_positions[2][0] + velocities[2][0] * t0c),
            Eq(y0 + vy0*t0c, start_positions[2][1] + velocities[2][1] * t0c),
            Eq(z0 + vz0*t0c, start_positions[2][2] + velocities[2][2] * t0c)]

sol = solve(eqs, [x0, y0, z0, vx0, vy0, vz0, t0a, t0b, t0c])
x0, y0, z0, _, _, _, _, _, _ = sol[0]
print("Part 2:", x0 + y0 + z0)

end_time = time()

print(f"Calculated solution in {end_time - start_time} seconds")