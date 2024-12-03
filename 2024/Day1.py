from collections import Counter
import numpy as np

def part1(data):
    # Parse input
    l1 =[int(n.split("   ")[0]) for n in data]
    l2 = [int(n.split("   ")[1]) for n in data]

    diff = np.sum(np.abs((np.array(sorted(l1))- np.array(sorted(l2)))))
    return diff

def part2(data):
    # Parse input
    l1 =[int(n.split("   ")[0]) for n in data]
    l2 = [int(n.split("   ")[1]) for n in data]
    l2_number_count = Counter(l2)
    similarity_score = sum(n * l2_number_count[n] for n in l1)
    return similarity_score