from aocd import get_data

input = get_data(day=6)

for i in range(14, len(input)):
    marker = input[i-14:i]

    if len(set(marker)) == len(marker):
        print(marker)
        print(i)
        break
