from aocd import get_data
from time import time
import numpy as np
import re

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
    
    def apply(self, part):
        if self.comp_op == '>':
            if part[self.comp_var] > self.comp_th:
                return self.return_value
            return None
        elif self.comp_op == '<':
            if part[self.comp_var] < self.comp_th:
                return self.return_value
            return None

def parse_part(part_string):
    p = part_string.replace("=", ":").replace("x", "'x'").replace("m", "'m'").replace("a", "'a'").replace("s", "'s'")
    return eval(p)

"""
with open("input.txt", "r") as f:
    input = f.read()
"""
input = get_data(day=19)


workflow_list, parts = input.split("\n\n")
workflow_list = [Workflow.parse_string_workflow(w) for w in workflow_list.splitlines()]
workflows = {w.name: w for w in workflow_list}
parts = [parse_part(p) for p in parts.splitlines()]

accepted_parts = []
for part in parts:
    state = 'in'
    while state not in ["A", "R"]:
        workflow_to_apply = workflows[state]
        state = workflow_to_apply.apply_rules(part)

    if state == 'A':
        accepted_parts.append(part)

sum_of_ratings = [sum(p.values()) for p in accepted_parts]
print("Part 1:", sum(sum_of_ratings))
end_time = time()

print(f"Calculated solution in {end_time - start_time} seconds")