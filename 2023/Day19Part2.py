from aocd import get_data
from time import time
import re
import copy

start_time = time()

class Workflow:
    def __init__(self, name, rule_string_list, default_return):
        self.name = name
        self.rule_list = [Rule.parse_string_rule(r) for r in rule_string_list]
        self.default_return = default_return

    @staticmethod
    def parse_string_workflow(s):
        name, rules = s[:-1].split("{")
        rule_list = rules.split(",")
        default_return = rule_list[-1]
        rule_list = rule_list[:-1]
        return Workflow(name, rule_list, default_return)
    
    def apply_rules(self, part):
        for rule in self.rule_list:
            new_state = rule.apply(part)
            if new_state is not None:
                return new_state
        return self.default_return
    
class Rule:
    def __init__(self, comp_var, comp_op, comp_th, return_value):
        self.comp_var = comp_var
        self.comp_op = comp_op
        self.comp_th = comp_th
        self.return_value = return_value
    
    @staticmethod
    def parse_string_rule(s):
        """
        e.g. "x>10:one"
        """
        m = re.match("([xams])([<>])([0-9]+):([A-Za-z]+)", s)
        if m.group(2) not in ['<', '>']:
            raise ValueError(f"Invalid comparison operator in rule string {s}")
        r = Rule(m.group(1), m.group(2), int(m.group(3)), m.group(4))
        return r
    
    def __str__(self):
        return f"{self.comp_var}{self.comp_op}{self.comp_th}:{self.return_value}"
    
    def check_rule_applies(self, part: dict):
        return self.comp_var in part.keys()
    
    def apply(self, part):
        if self.comp_op == '>':
            if part[self.comp_var] > self.comp_th:
                return self.return_value
            return None
        elif self.comp_op == '<':
            if part[self.comp_var] < self.comp_th:
                return self.return_value
            return None

class PartRange:
    def __init__(self, x_min, x_max, m_min, m_max, s_min, s_max, a_min, a_max, state) -> None:
         """
         Values including
         """
         self.mins = {'x': x_min, 's': s_min, 'a': a_min, 'm': m_min}
         self.maxs = {'x': x_max, 's': s_max, 'a': a_max, 'm': m_max}
         self.state = state
    
    def get_n_combinations(self):
         return (self.maxs['x'] - self.mins['x'] + 1) * (self.maxs['m'] - self.mins['m'] + 1) * (self.maxs['a'] - self.mins['a'] + 1) * (self.maxs['s'] - self.mins['s'] + 1)
    
    def is_done(self):
         return self.state in ["A", "R"]
    
    def copy(self):
        return copy.deepcopy(self)

def parse_part(part_string):
    p = part_string.replace("=", ":").replace("x", "'x'").replace("m", "'m'").replace("a", "'a'").replace("s", "'s'")
    return eval(p)

"""
with open("input.txt", "r") as f:
    input = f.read()
"""
input = get_data(day=19)


workflow_list, _ = input.split("\n\n")
workflow_list = [Workflow.parse_string_workflow(w) for w in workflow_list.splitlines()]
workflows = {w.name: w for w in workflow_list}

not_done_part_ranges = [PartRange(1, 4000, 1, 4000, 1, 4000, 1, 4000, 'in')]

possible_combination_count = 0
while len(not_done_part_ranges) > 0:
    part_range = not_done_part_ranges.pop(0)
    
    workflow_to_apply = workflows[part_range.state]

    rules_applied = False

    for rule in workflow_to_apply.rule_list:
        # Is this rule relevant for the given range
        if part_range.mins[rule.comp_var] < rule.comp_th < part_range.maxs[rule.comp_var]:
            rules_applied = True
            # Split the range into two
            new_range1 = part_range.copy()
            new_range1.state = rule.return_value
            new_range2 = part_range.copy()

            if rule.comp_op == '>':
                new_range1.mins[rule.comp_var] = rule.comp_th + 1                
                new_range2.maxs[rule.comp_var] = rule.comp_th
            else:
                new_range1.maxs[rule.comp_var] = rule.comp_th - 1
                new_range2.mins[rule.comp_var] = rule.comp_th
                
            if new_range1.is_done():
                if new_range1.state == 'A':
                    possible_combination_count += new_range1.get_n_combinations()
            else:
                not_done_part_ranges.append(new_range1)
            not_done_part_ranges.append(new_range2)

            break

    # If no rules apply
    if not rules_applied:
        part_range.state = workflow_to_apply.default_return
        if part_range.is_done():
            if part_range.state == 'A':
                possible_combination_count += part_range.get_n_combinations()
        else:
            not_done_part_ranges.append(part_range)

print("Part 2:", possible_combination_count)
end_time = time()

print(f"Calculated solution in {end_time - start_time} seconds")