from aocd import get_data

def is_flat_list(l):
    return type(l) == list and all([type(e) == int for e in l])
def compare_packets(left, right):

    if type(left) == int and type(right) == int:
        if left < right:
            return True
        elif right < left:
            return False
        else:
            return None

    if type(left) == list and type(right) == list:
        if len(right) == 0 and len(left) == 0:
            return None
        elif len(right) == 0:
            return False
        elif len(left) == 0:
            return True
        else:
            result = compare_packets(left[0], right[0])
            if result is not None:
                return result
            else:
                return compare_packets(left[1:], right[1:])

    if type(left) == list and type(right) == int:
        return compare_packets(left, [right])

    if type(left) == int and type(right) == list:
        return compare_packets([left], right)


#data = get_data(day=13).split("\n\n")
with open("test_input.txt") as f:
    data = f.read().split("\n\n")

right_order_packet_indices = []
for idx, packet_pair in enumerate(data):
    left, right = packet_pair.splitlines()

    if compare_packets(eval(left), eval(right)):
        right_order_packet_indices.append(idx + 1)

print("Correct packets:", right_order_packet_indices)
print("Sum of correct packet indices:", sum(right_order_packet_indices))

## PART 2
def quicksort(l: list):
    sorted_list = l.copy()

    if len(sorted_list) <= 1:
        return sorted_list
    pivot = sorted_list[-1]
    pivot_pos = len(sorted_list) - 1

    i = 0
    while True:
        # Find the first value larger than the pivot
        while compare_packets(sorted_list[i], pivot):
            i += 1
        first_larger_value = sorted_list[i]

        # Next look for the next value that is smaller than the pivot
        j = i + 1
        while j < len(l) and compare_packets(pivot, sorted_list[j]):
            if j == len(l) - 1:
                print("Going out of index")
            j += 1

        if j == len(l):
            # The pivot is the largest value in the list
            return quicksort(sorted_list[:-1]) + [pivot]

        # Swap the larger with the smaller value
        sorted_list[i] = sorted_list[j].copy() if type(sorted_list[j]) == list else sorted_list[j]
        sorted_list[j] = first_larger_value.copy() if type(first_larger_value) == list else first_larger_value

        if j == pivot_pos:
            break

    return quicksort(sorted_list[:i]) + [pivot] + quicksort(sorted_list[i + 1:])



data = get_data(day=13).replace("\n\n", "\n").splitlines()
#with open("test_input.txt") as f:
#    data = f.read().replace("\n\n", "\n").splitlines()

data = [eval(x) for x in data]

sorted_list = quicksort(data + [[[2]], [[6]]])
#for row in sorted_list:
#    print(row)

pos1, pos2 = [idx for idx, value in enumerate(sorted_list) if value == [[2]] or value == [[6]]]
result = (pos1 + 1) * (pos2 + 1)
print("Final result:", result)