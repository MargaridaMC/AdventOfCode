def parse_input(data):
    equations = [row.split(": ") for row in data.splitlines()]
    equations = [tuple((int(result), list(map(int, equation.split(" "))))) for result, equation in equations]
    return equations

def s(n1, n2):
    return n1 + n2

def p(n1, n2):
    return n1 * n2

def c(n1, n2):
    return int(str(n1) + str(n2))

def check_result_is_correct(current_result, equation_values, final_result, i = 1, allow_concatenation = False):
    if i == len(equation_values):
        return current_result == final_result
    
    allowed_operator_list = [s, p, c] if allow_concatenation else [s, p]

    for op in allowed_operator_list:
        temp_result = op(current_result, equation_values[i])
        if temp_result <= final_result:
            op_is_correct = check_result_is_correct(temp_result, equation_values, final_result, i + 1, allow_concatenation)
            if op_is_correct:
                return True
            
    return False

def run(data, allow_concatenation):
    equations = parse_input(data)

    sum_allowed_results = 0

    for result, equation_values in equations:
        if check_result_is_correct(equation_values[0], equation_values, result, 1, allow_concatenation = allow_concatenation):
            sum_allowed_results += result

    return sum_allowed_results

def part1(data):
    return run(data, False)

def part2(data):
    return run(data, True)