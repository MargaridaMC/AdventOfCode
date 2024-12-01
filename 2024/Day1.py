from aocd import get_data
from collections import Counter
import numpy as np

data = get_data(day=1).splitlines()

# Parse input
l1 =[int(n.split("   ")[0]) for n in data]
l2 = [int(n.split("   ")[1]) for n in data]

# Part 1
diff = np.sum(np.abs((np.array(sorted(l1))- np.array(sorted(l2)))))
print(f"Part 1 solution: {diff}")

# Part 2
l2_number_count = Counter(l2)
similarity_score = sum(n * l2_number_count[n] for n in set(l1))
print(f"Part 2 solution: {similarity_score}")