from aocd import get_data
import numpy as np

input = get_data(day=8).splitlines()
#input = "30373\n25512\n65332\n33549\n35390".splitlines()

# Part 1
tree_heights = np.array(list(map(list, input))).astype(int)
nrows, ncols = tree_heights.shape

# Check visibility from the top
visibility_from_top = np.zeros_like(tree_heights)
# Edge is all visible
visibility_from_top[0, :] = 1
for col in range(ncols):
    current_max_height = tree_heights[0, col]
    for row in range(1, nrows):
        height = tree_heights[row, col]
        if all(height > tree_heights[:row, col]):
            visibility_from_top[row, col] = 1
            current_max_height = height
            if current_max_height == 9:
                # We won't find any taller trees, so we can stop now
                break

# Visibility from bottom
visibility_from_bottom = np.zeros_like(tree_heights)
visibility_from_bottom[-1, :] = 1
for col in range(ncols):
    current_max_height = tree_heights[-1, col]
    for row in reversed(range(nrows - 1)):
        height = tree_heights[row, col]
        if all(height > tree_heights[row+1:, col]):
            visibility_from_bottom[row, col] = 1
            current_max_height = height
            if current_max_height == 9:
                # We won't find any taller trees, so we can stop now
                break


# Check visibility from the left
visibility_from_left = np.zeros_like(tree_heights)
visibility_from_left[:, 0] = 1
for row in range(nrows):
    current_max_height = tree_heights[row, 0]
    for col in range(1, ncols):
        height = tree_heights[row, col]
        if all(height > tree_heights[row, :col]):
            visibility_from_left[row, col] = 1
            current_max_height = height
            if current_max_height == 9:
                # We won't find any taller trees, so we can stop now
                break

# Check visibility from the right
visibility_from_right = np.zeros_like(tree_heights)
visibility_from_right[:, -1] = 1
for row in range(nrows):
    current_max_height = tree_heights[row, -1]
    for col in reversed(range(ncols - 1)):
        height = tree_heights[row, col]
        if all(height > tree_heights[row, col+1:]):
            visibility_from_right[row, col] = 1
            current_max_height = height
            if current_max_height == 9:
                # We won't find any taller trees, so we can stop now
                break

visible_trees = visibility_from_top | visibility_from_bottom | visibility_from_right | visibility_from_left

#print(tree_heights)
#print(visible_trees)

print("Total number of visible trees:", visible_trees.sum())

# Part 2

# Only the visible trees are candidates to be the best option

def calculate_score(x, y):
    score = 1
    height = tree_heights[x, y]

    # Check visibility towards top
    top_trees = tree_heights[:x, y][::-1]
    score *= (np.argmax(top_trees >= height) + 1 if any(top_trees >= height) else len(top_trees))

    # Bottom
    bottom_trees = tree_heights[x+1:, y]
    score *= (np.argmax(bottom_trees >= height) + 1 if any(bottom_trees >= height) else len(bottom_trees))

    # Left
    left_trees = tree_heights[x, :y][::-1]
    score *= (np.argmax(left_trees >= height) + 1 if any(left_trees >= height) else len(left_trees))

    # Right
    right_trees = tree_heights[x, y+1:]
    score *= (np.argmax(right_trees >= height) + 1 if any(right_trees >= height) else len(right_trees))

    return score

xs, ys = np.where(visible_trees)
scores = [calculate_score(x, y) for x, y in zip(xs, ys)]

print("Best score:", max(scores))
