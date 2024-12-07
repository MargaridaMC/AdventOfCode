from itertools import pairwise

def parse_input(data):
    equations = [row.split(": ") for row in data.splitlines()]
    equations = [tuple((int(result), list(map(int, equation.split(" "))))) for result, equation in equations]
    return equations

def check_result_is_correct(current_result, equation_values, final_result, i = 1, allow_concatenation = False):
    if i == len(equation_values):
        return current_result == final_result
    
    # Try sum
    result_w_sum = current_result + equation_values[i]
    if result_w_sum <= final_result:
        sum_is_correct = check_result_is_correct(result_w_sum, equation_values, final_result, i + 1, allow_concatenation)
        if sum_is_correct:
            return True

    # Try product
    result_w_product = current_result * equation_values[i]
    if result_w_product <= final_result:
        product_is_correct = check_result_is_correct(result_w_product, equation_values, final_result, i + 1, allow_concatenation)
        if product_is_correct:
            return True
    
    # Try concatenation 
    if allow_concatenation:
        result_w_concatenation = int(str(current_result) + str(equation_values[i]))
        if result_w_concatenation <= final_result:
            concatenation_is_correct = check_result_is_correct(result_w_concatenation, equation_values, final_result, i + 1, allow_concatenation)
            if concatenation_is_correct:
                return True

    return False

def part1(data):
    equations = parse_input(data)

    sum_allowed_results = 0

    for result, equation_values in equations:
        if check_result_is_correct(equation_values[0], equation_values, result, 1):
            sum_allowed_results += result

    return sum_allowed_results

def part2(data):
    equations = parse_input(data)

    sum_allowed_results = 0

    for result, equation_values in equations:
        if check_result_is_correct(equation_values[0], equation_values, result, 1, allow_concatenation = True):
            sum_allowed_results += result

    return sum_allowed_results