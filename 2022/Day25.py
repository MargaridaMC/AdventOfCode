from dataclasses import dataclass
from telegram import SendTelegramMessage
import numpy as np
from aocd import get_data
from tqdm import tqdm
import pandas as pd

calculation_matrix = pd.DataFrame(columns = ["2", "1", "0", "-", "="], index = ["2", "1", "0", "-", "="])
calculation_matrix.loc["2", "2"] = "1-"
calculation_matrix.loc["2", "1"] = "1="
calculation_matrix.loc["1", "2"] = "1="
calculation_matrix.loc["2", "0"] = "2"
calculation_matrix.loc["0", "2"] = "2"
calculation_matrix.loc["2", "-"] = "1"
calculation_matrix.loc["-", "2"] = "1"
calculation_matrix.loc["2", "="] = "0"
calculation_matrix.loc["=", "2"] = "0"
calculation_matrix.loc["1", "1"] = "2"
calculation_matrix.loc["1", "0"] = "1"
calculation_matrix.loc["0", "1"] = "1"
calculation_matrix.loc["1", "-"] = "0"
calculation_matrix.loc["-", "1"] = "0"
calculation_matrix.loc["1", "="] = "-"
calculation_matrix.loc["=", "1"] = "-"
calculation_matrix.loc["0", "0"] = "0"
calculation_matrix.loc["0", "-"] = "-"
calculation_matrix.loc["-", "0"] = "-"
calculation_matrix.loc["0", "="] = "="
calculation_matrix.loc["=", "0"] = "="
calculation_matrix.loc["-", "-"] = "="
calculation_matrix.loc["-", "="] = "-2"
calculation_matrix.loc["=", "-"] = "-2"
calculation_matrix.loc["=", "="] = "-1"
print(calculation_matrix)

lines = get_data(day=25).splitlines()
#with open("test_input.txt") as f:
#    lines = f.read().splitlines()

max_length = max(map(len, lines))
numbers = [[digit for digit in l.zfill(max_length)] for l in lines]
numbers = list(zip(*numbers))
numbers = [[]] + list(map(list, numbers))

complete_result = ""

def sum_list_of_digits(digit_list):

    carry_overs = []
    result = digit_list[0]

    for number in digit_list[1:]:
        result = calculation_matrix.loc[result, number]
        if len(result) > 1:
            carry_overs.append(result[:-1])
            result = result[-1]

    return result, carry_overs

for position in range(1, len(numbers)):

    position_numbers = numbers[-position]
    position_result, carry_overs = sum_list_of_digits(position_numbers)

    numbers[-(position + 1)] += carry_overs
    complete_result = position_result + complete_result

print("Sum:", complete_result)