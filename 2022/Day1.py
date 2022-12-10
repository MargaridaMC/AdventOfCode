from aocd import get_data

input = get_data(day=1).splitlines()

cal_list = ",".join(input)
cal_list_per_elf = cal_list.split(",,")

cal_list_per_elf = list(map(lambda x: [int(v) for v in x.split(",")], cal_list_per_elf))

calorie_count_per_elf = list(map(sum, cal_list_per_elf))

# Answer to part 1:
print("Max calories:", max(calorie_count_per_elf))

sorted_calorie_count_per_elf = sorted(calorie_count_per_elf)

# Answer to part 2:
print("Sum of top 3 calories:", sum(sorted_calorie_count_per_elf[-3:]))
