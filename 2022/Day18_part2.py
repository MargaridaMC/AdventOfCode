from aocd import get_data
import numpy as np
from dataclasses import dataclass, field

lines = get_data(day=18).splitlines()
#with open("test_input.txt") as f:
#    lines = f.read().splitlines()

@dataclass
class Cube:
    x: int
    y: int
    z: int
    left_is_exposed: bool = field(init=False, default=False)
    right_is_exposed: bool = field(init=False, default=False)
    top_is_exposed: bool = field(init=False, default=False)
    bottom_is_exposed: bool = field(init=False, default=False)
    front_is_exposed: bool = field(init=False, default=False)
    back_is_exposed: bool = field(init=False, default=False)

    def get_n_exposed_faces(self):
        return self.left_is_exposed + self.right_is_exposed + self.top_is_exposed + self.bottom_is_exposed + self.back_is_exposed + self.front_is_exposed

# Read input
cubes = [Cube(*map(int, line.split(","))) for line in lines]


cube_coords = np.array([list(map(int, line.split(","))) for line in lines])
max_x, max_y, max_z = max(cube_coords[:, 0]), max(cube_coords[:, 1]), max(cube_coords[:, 2])
seed_points = {(0, 0, 0), (0, 0, max_z + 1), (0, max_y + 1, 0), (0, max_y + 1, max_z + 1), (max_x + 1, 0, 0), (max_x + 1, 0, max_z + 1),
               (max_x + 1, max_y + 1, 0), (max_x + 1, max_y + 1, max_z + 1)}
explored_points = np.zeros((max_x + 2, max_y + 2, max_z + 2))

while len(seed_points) > 0:

    x, y, z = seed_points.pop()
    explored_points[x, y, z] = 1

    if x > 0:
        left_cube = [c for c in cubes if c.x == x - 1 and c.y == y and c.z == z]
        if len(left_cube) > 0:
            left_cube[0].right_is_exposed = True
        elif not explored_points[x - 1, y, z]:
            seed_points.add((x - 1, y, z))
    if x < max_x:
        right_cube = [c for c in cubes if c.x == x + 1 and c.y == y and c.z == z]
        if len(right_cube) > 0:
            right_cube[0].left_is_exposed = True
        elif not explored_points[x + 1, y, z]:
            seed_points.add((x + 1, y, z))
    if y > 0:
        top_cube = [c for c in cubes if c.y == y - 1 and c.x == x and c.z == z]
        if len(top_cube) > 0:
            top_cube[0].bottom_is_exposed = True
        elif not explored_points[x, y - 1, z]:
            seed_points.add((x, y - 1, z))
    if y < max_y:
        bottom_cube = [c for c in cubes if c.y == y + 1 and c.x == x and c.z == z]
        if len(bottom_cube) > 0:
            bottom_cube[0].top_is_exposed = True
        elif not explored_points[x, y + 1, z]:
            seed_points.add((x, y + 1, z))
    if z > 0:
        back_cube = [c for c in cubes if c.z == z - 1 and c.y == y and c.x == x]
        if len(back_cube) > 0:
            back_cube[0].front_is_exposed = True
        elif not explored_points[x, y, z - 1]:
            seed_points.add((x, y, z - 1))
    if z < max_z:
        front_cube = [c for c in cubes if c.z == z + 1 and c.y == y and c.x == x]
        if len(front_cube) > 0:
            front_cube[0].back_is_exposed = True
        elif not explored_points[x, y, z + 1]:
            seed_points.add((x, y, z + 1))

# Also consider that cubes that are right at the border have that face visible
for cube in cubes:
    if cube.x == 0:
        cube.left_is_exposed = True
    if cube.y == 0:
        cube.top_is_exposed = True
    if cube.z == 0:
        cube.front_is_exposed = True

total_exposed_faces = sum([c.get_n_exposed_faces() for c in cubes])
print("Total exposed faces:", total_exposed_faces)

# 2566 too low
# 2575 too low