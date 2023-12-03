from aocd import get_data

input = get_data(day=1).splitlines()
digits = [[i for i in l if i.isdigit()] for l in input]
calibration_values = [int(l[0] + l[-1]) for l in digits]
print("Part1: Sum of calibration values:", sum(calibration_values))

# Part 2
#input = ['two1nine','eightwothree','abcone2threexyz','xtwone3four','4nineeightseven2','zoneight234','7pqrstsixteen']
input = [l.lower() for l in input]
parsed_input = []
letter_digits_mapping = {"one": '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

calibration_values = []

for i, l in enumerate(input):
    j = 0
    first_digit = None
    while first_digit is None:

        if l[j].isdigit():
            first_digit = l[j]
            break

        for n_chars in range(3, 6):
            if l[j:j+n_chars] in letter_digits_mapping.keys():
                first_digit = letter_digits_mapping[l[j:j+n_chars]]
                break
        
        j += 1
        
    last_digit = None
    j = len(l) - 1
    while last_digit is None:

        if l[j].isdigit():
            last_digit = l[j]
        for n_chars in range(3, 6):
            if l[j-n_chars + 1:j + 1] in letter_digits_mapping.keys():
                last_digit = letter_digits_mapping[l[j-n_chars + 1:j + 1]]
                break
        j -= 1
    calibration_values.append(int(first_digit + last_digit))

print("Part2: Sum of calibration values:", sum(calibration_values))