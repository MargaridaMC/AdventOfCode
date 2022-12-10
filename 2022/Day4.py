from aocd import get_data

input = get_data(day=4).splitlines()

# Question 1
count = 0

for pair in input:
    elf1, elf2 = pair.split(",")
    min1, max1 = map(int, elf1.strip().split("-"))
    min2, max2 = map(int, elf2.strip().split("-"))

    if (min1 >= min2 and max1 <= max2) or (min2 >= min1 and max2 <= max1):
        count += 1

print("Question 1:", count)

# Question 2
count = 0

for pair in input:
    elf1, elf2 = pair.split(",")
    min1, max1 = map(int, elf1.strip().split("-"))
    min2, max2 = map(int, elf2.strip().split("-"))

    if min1 in range(min2, max2 + 1) or max1 in range(min2, max2 + 1) or min2 in range(min1, max1 + 1) or max2 in range(min1, max1 + 1):
        count += 1

print("Question 2:", count)