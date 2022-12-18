from dataclasses import dataclass, field
from aocd import get_data
import numpy as np

#lines = get_data(day=18).splitlines()
with open("test_input.txt") as f:
    lines = f.read().splitlines()

@dataclass
class Cube:
    x: int
    y: int
    z: int
    left_is_exposed: bool = field(init=False, default=True)
    right_is_exposed: bool = field(init=False, default=True)
    top_is_exposed: bool = field(init=False, default=True)
    bottom_is_exposed: bool = field(init=False, default=True)
    front_is_exposed: bool = field(init=False, default=True)
    back_is_exposed: bool = field(init=False, default=True)

    def get_n_exposed_faces(self):
        return self.left_is_exposed + self.right_is_exposed + self.top_is_exposed + self.bottom_is_exposed + self.back_is_exposed + self.front_is_exposed

# Read input
cubes = [Cube(*map(int, line.split(","))) for line in lines]

# Find faces touching
for cube in cubes:
    if cube.get_n_exposed_faces() == 0:
        continue
    if cube.left_is_exposed:
        left_cube = [c for c in cubes if c.x == cube.x - 1 and c.y == cube.y and c.z == cube.z]
        if len(left_cube) > 0:
            cube.left_is_exposed = False
            left_cube[0].right_is_exposed = False
    if cube.right_is_exposed:
        right_cube = [c for c in cubes if c.x == cube.x + 1 and c.y == cube.y and c.z == cube.z]
        if len(right_cube) > 0:
            cube.right_is_exposed = False
            right_cube[0].left_is_exposed = False

    if cube.top_is_exposed:
        top_cube = [c for c in cubes if c.y == cube.y + 1 and c.x == cube.x and c.z == cube.z]
        if len(top_cube) > 0:
            cube.top_is_exposed = False
            top_cube[0].bottom_is_exposed = False
    if cube.bottom_is_exposed:
        bottom_cube = [c for c in cubes if c.y == cube.y - 1 and c.x == cube.x and c.z == cube.z]
        if len(bottom_cube) > 0:
            cube.bottom_is_exposed = False
            bottom_cube[0].top_is_exposed = False

    if cube.front_is_exposed:
        front_cube = [c for c in cubes if c.z == cube.z + 1 and c.x == cube.x and c.y == cube.y]
        if len(front_cube) > 0:
            cube.front_is_exposed = False
            front_cube[0].back_is_exposed = False
    if cube.back_is_exposed:
        back_cube = [c for c in cubes if c.z == cube.z - 1 and c.x == cube.x and c.y == cube.y]
        if len(back_cube) > 0:
            cube.back_is_exposed = False
            back_cube[0].front_is_exposed = False

total_exposed_faces = sum([c.get_n_exposed_faces() for c in cubes])
print("Total exposed faces:", total_exposed_faces)
