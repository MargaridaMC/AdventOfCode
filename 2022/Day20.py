import numpy as np
from aocd import get_data

lines = get_data(day=20).splitlines()
#with open("test_input.txt") as f:
#    lines = f.read().splitlines()

class Element:
    def __init__(self, value, start_pos, n_elements):
        self.original_value: int = value
        self.value: int = np.sign(value) * (abs(value) % (n_elements-1))
        self.start_pos: int = start_pos
        self.previous_element: Element = None
        self.next_element: Element = None

    def __delete__(self):
        self.previous_element.next_element = self.next_element
        self.next_element.previous_element = self.previous_element

    def __str__(self):
        return f"Value: {self.value}. Previous value: {self.previous_element.value}. Next value {self.next_element.value}."

def move_element(element, n_steps):
    element.__delete__()

    if n_steps < 0:
        prev_element = element.previous_element
        for _ in range(abs(n_steps)):
            prev_element = prev_element.previous_element
        next_element = prev_element.next_element
        prev_element.next_element = element
        element.previous_element = prev_element
        next_element.previous_element = element
        element.next_element = next_element
        return
    else:
        next_element = element.next_element
        for _ in range(abs(n_steps)):
            next_element = next_element.next_element
        previous_element = next_element.previous_element
        next_element.previous_element = element
        element.next_element = next_element
        previous_element.next_element = element
        element.previous_element = previous_element
        return

def print_list(file):
    print(linked_list_to_value_list(file))

def linked_list_to_value_list(file):
    element = file[0]
    values = []
    for _ in range(n_elements):
        element = element.next_element
        values.append(element.original_value)
    return values

constant = 811589153
encrypted_file = list(Element(value*constant, pos, len(lines)) for pos, value in enumerate(map(int, lines)))
n_elements = len(encrypted_file)
for i in range(1, n_elements - 1):
    encrypted_file[i].previous_element = encrypted_file[i - 1]
    encrypted_file[i].next_element = encrypted_file[i + 1]

encrypted_file[0].previous_element = encrypted_file[-1]
encrypted_file[0].next_element = encrypted_file[1]
encrypted_file[-1].previous_element = encrypted_file[-2]
encrypted_file[-1].next_element = encrypted_file[0]

decrypted_file = encrypted_file.copy()
#print_list(decrypted_file)
n_mix_rounds = 10
for mix_round in range(n_mix_rounds):
    for value in decrypted_file:

        if value.value % n_elements == 0:
            continue

        move_element(value, value.value)

    #print_list(decrypted_file)

decrypted_list = linked_list_to_value_list(decrypted_file)
position_of_0 = np.where(np.array(decrypted_list) == 0)[0][0]
value_at_1000 = decrypted_list[(position_of_0 + 1000) % n_elements]
value_at_2000 = decrypted_list[(position_of_0 + 2000) % n_elements]
value_at_3000 = decrypted_list[(position_of_0 + 3000) % n_elements]
result = value_at_3000 + value_at_2000 + value_at_1000
print(value_at_1000, value_at_2000, value_at_3000)
print("Result:", result)

# 4542 too high
# 2792 too low