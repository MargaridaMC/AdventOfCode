import numpy as np
from tqdm import tqdm
from aocd import get_data

data = get_data(day=11)
#with open("test_input.txt") as f:
#    data = f.read()


LCM = 5*11*2*13*7*3*17*19

class Monkey:
    def __init__(self, starting_item_list, operation, test_denominator, recipient_monkey_if_test_true, recipient_monkey_if_test_false):
        self.item_list = starting_item_list
        self.operation = operation
        self.test_denominator = test_denominator
        self.recipient_monkey_if_test_true = recipient_monkey_if_test_true
        self.recipient_monkey_if_test_false = recipient_monkey_if_test_false
        self.n_inspections = 0

    def inspect_all_items(self):

        throws = dict()

        if len(self.item_list) == 0:
            return throws

        for worry_level in self.item_list:

            # Step 1: monkey plays with item -> worry level increases
            new_worry_level = self.operation(worry_level)

            # Step 2: you relax because monkey did not break item
            #new_worry_level = int(np.floor(new_worry_level / 3))
            new_worry_level = new_worry_level%LCM

            # Step 3: test to see to which monkey this item is thrown to
            if new_worry_level%self.test_denominator == 0:
                throws[self.recipient_monkey_if_test_true] = throws[self.recipient_monkey_if_test_true] + [new_worry_level] if self.recipient_monkey_if_test_true in throws.keys() else [new_worry_level]
            else:
                throws[self.recipient_monkey_if_test_false] = throws[self.recipient_monkey_if_test_false] + [new_worry_level] if self.recipient_monkey_if_test_false in throws.keys() else [new_worry_level]

            # Register the number of total inspections
            self.n_inspections += 1

        # At the end of the monkey's move he'll have inspected and thrown all items
        self.item_list = []

        return throws

    def __cmp__(self, other):
        return __cmp__(self.n_inspections, other.n_inspections)

def parse_monkey(monkey_lines):
    _, starting_item_list, operation_string, test, if_test_true, if_test_false = monkey_lines.split("\n")

    starting_item_list = starting_item_list[len("  Starting items: "):].split(", ")
    starting_item_list = list(map(int, starting_item_list))

    operation_string = operation_string[len("  Operation: new = "):]
    operation = lambda old: eval(operation_string)

    test_denominator = int(test[len("  Test: divisible by "):])

    recipient_monkey_if_test_true = int(if_test_true[len("    If true: throw to monkey "):])
    recipient_monkey_if_test_false = int(if_test_false[len("    If false: throw to monkey "):])

    return Monkey(starting_item_list, operation, test_denominator, recipient_monkey_if_test_true, recipient_monkey_if_test_false)


def print_item_distribution(monkeys):

    for i, monkey in enumerate(monkeys):
        print(f"Monkey {i}: {', '.join(map(str, monkey.item_list))}")


# Initialize list of monkeys
monkeys = [parse_monkey(monkey) for monkey in data.split("\n\n")]

print("Item distribution at start:")
print_item_distribution(monkeys)

# Play
for round_count in tqdm(range(10000)):

    for monkey in monkeys:
        throws = monkey.inspect_all_items()
        if throws is not None:
            for recipient_monkey, item_list in throws.items():
                monkeys[recipient_monkey].item_list += item_list

    #print("Game state after round", round_count)
    #print_item_distribution(monkeys)
    #print()

top_2_monkeys_n_inspections = sorted([m.n_inspections for m in monkeys], reverse=True)[:2]
print("Monkey business:", top_2_monkeys_n_inspections[0]*top_2_monkeys_n_inspections[1])
