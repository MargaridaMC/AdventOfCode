from aocd import get_data
import numpy as np

input = get_data(day=9).splitlines()
#input = "R 4\nU 4\nL 3\nD 1\nR 4\nD 1\nL 5\nR 2".splitlines()


def get_new_tail_pos_from_head_pos(h_pos, t_pos):
    # If the current positions are allowed then the tail does need to move
    if np.linalg.norm(h_pos - t_pos) <= np.sqrt(2):
        return t_pos

    # Else tail is two positions away from head
    move = (h_pos - t_pos)
    move[0] = move[0] / 2 if abs(move[0]) == 2 else move[0]
    move[1] = move[1] / 2 if abs(move[1]) == 2 else move[1]

    return (t_pos + move).astype(int)


# PART 1
h_pos = np.array((0, 0))
t_pos = np.array((0, 0))
visited_positions = set()
visited_positions.add(str(t_pos))

moves = {"R": [0, 1],
         "U": [-1, 0],
         "L": [0, -1],
         "D": [1, 0]}

for line in input:
    direction, count = line.split(" ")
    for i in range(int(count)):
        h_pos += moves[direction]
        t_pos = get_new_tail_pos_from_head_pos(h_pos, t_pos)
        visited_positions.add(str(t_pos))

print("Number of visited positions:", len(visited_positions))

# PART 2
knot_positions = [np.array((0, 0)) for _ in range(10)]
visited_positions = set()
visited_positions.add(str(np.array((0, 0))))
for line in input:
    direction, count = line.split(" ")
    for i in range(int(count)):
        knot_positions[0] += moves[direction]
        for knot_idx in range(1, 10):
            knot_positions[knot_idx] = get_new_tail_pos_from_head_pos(knot_positions[knot_idx - 1], knot_positions[knot_idx])
        visited_positions.add(str(knot_positions[-1]))

print("Number of visited positions:", len(visited_positions))
