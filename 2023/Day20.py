from aocd import get_data
from time import time
from uuid import uuid4
from abc import ABC
from operator import mul
from functools import reduce

start_time = time()

class State:
    ON = 1
    OFF = 0

class Pulse:
    HIGH = 1
    LOW = 0

class Module(ABC):
    def __init__(self, id = None, dest_module_ids = []) -> None:
        self.id = uuid4() if id is None else id
        self.dest_module_ids = dest_module_ids

    def send_high_pulse(self):
        return self.send_pulse(Pulse.HIGH)
    
    def send_low_pulse(self):
        return self.send_pulse(Pulse.LOW)
    
    def send_pulse(self, pulse: Pulse):
        global pulses_to_send
        global RELEVANT_PULSES_FOUND
        for m in self.dest_module_ids:
            #m.receive_pulse(pulse, self.id)
            pulses_to_send.append((self.id, m, pulse))
            if pulse == Pulse.LOW and m in RELEVANT_PULSES_FOUND.keys():
                print(f"Found {m}")
                RELEVANT_PULSES_FOUND[m] = 1

    def receive_pulse(self, pulse: Pulse, input_module_id: str = '') -> None:
        global PULSE_COUNT
        PULSE_COUNT[pulse] += 1

class FlipFlopModule(Module):
    def __init__(self, id = None, dest_module_ids = []) -> None:
        super().__init__(id, dest_module_ids)
        self.state = State.OFF

    def receive_pulse(self, pulse: Pulse, input_module_id: str = ''):
        super().receive_pulse(pulse, input_module_id)
        if pulse == Pulse.LOW:
            if self.state == State.ON:
                self.state = State.OFF
                self.send_low_pulse()
            else:
                self.state = State.ON
                self.send_high_pulse()

class ConjunctionModule(Module):
    def __init__(self, id = None, dest_module_ids = [], input_module_ids = []) -> None:
        super().__init__(id, dest_module_ids)
        self.most_recent_pulses = {id: Pulse.LOW for id in input_module_ids}
    
    def receive_pulse(self, pulse: Pulse, input_module_id: str = '') -> None:
        super().receive_pulse(pulse, input_module_id)
        self.most_recent_pulses[input_module_id] = pulse
        if all(self.most_recent_pulses.values()):
            self.send_low_pulse()
        else:
            self.send_high_pulse()

class Broadcaster(Module):
    def receive_pulse(self, pulse: Pulse, input_module_id: str = '') -> None:
        super().receive_pulse(pulse, input_module_id)
        self.send_pulse(pulse)

class Button(Module):

    def push_button(self):
        self.send_low_pulse()

def parse_input(input):

    input_dest_id_mapping = dict()
    for row in input:
        input_module_id, dest_module_id = row.split(" -> ")
        dest_module_id = dest_module_id.split(", ")
        input_dest_id_mapping[input_module_id] = dest_module_id

    modules = dict()
    for input_module_id, dest_module_ids in input_dest_id_mapping.items():
        if input_module_id == 'broadcaster':
            modules[input_module_id] = Broadcaster(input_module_id, dest_module_ids=dest_module_ids)
        elif input_module_id[0] == '%':
            input_module_id = input_module_id[1:]
            modules[input_module_id] = FlipFlopModule(input_module_id, dest_module_ids=dest_module_ids)
        elif input_module_id[0] == '&':
            input_module_id = input_module_id[1:]
            input_modules = [id for id in input_dest_id_mapping.keys() if input_module_id in input_dest_id_mapping[id]]
            input_modules = [id[1:] if id.startswith("&") or id.startswith("%") else id for id in input_modules]
            modules[input_module_id] = ConjunctionModule(input_module_id, dest_module_ids=dest_module_ids, input_module_ids=input_modules)
        else:
            raise ValueError(f"Unknown module type: {row}")
        
    # If there are any unknown destination module IDs we won't be able to see them so add them manually to the list
    # Assume they are test modules
    for dest_module_ids in input_dest_id_mapping.values():
        for id in dest_module_ids:
            if id not in modules.keys():
                modules[id] = Module(id)

    modules['button'] = Button('button', ['broadcaster'])
    return modules

def push_button_and_process_pulses(all_modules):
    all_modules['button'].push_button()
    while len(pulses_to_send) > 0:
        from_mod, to_mod, pulse = pulses_to_send.pop(0)
        all_modules[to_mod].receive_pulse(pulse, from_mod)
    return all_modules

def find_flip_flop_cycle_period(flip_flop_modules_ids, all_modules):
    flip_flop_module_initial_state = [all_modules[id].state for id in flip_flop_modules_ids ]

    # Push button once and process pulses
    all_modules = push_button_and_process_pulses(all_modules)
    button_push_count = 1

    # Part 1
    new_flip_flop_state = [all_modules[id].state for id in flip_flop_modules_ids ]
    while new_flip_flop_state != flip_flop_module_initial_state:
        all_modules = push_button_and_process_pulses(all_modules)
        button_push_count += 1
        new_flip_flop_state =  [all_modules[id].state for id in flip_flop_modules_ids ]

    return button_push_count

"""
with open("input.txt", "r") as f:
    input = f.read().splitlines()
"""
input = get_data(day=20).splitlines()

pulses_to_send = []
PULSE_COUNT = [0, 0]

modules = parse_input(input)

""" Part 1
flip_flop_modules = [id for id, m in modules.items() if isinstance(m, FlipFlopModule) ]
button_push_count = find_flip_flop_cycle_period(flip_flop_modules, modules)

print(f"{button_push_count} button pushes were needed to get back to the initial state.")
print(f"This is equivalent to {PULSE_COUNT[Pulse.LOW]} low pulses and {PULSE_COUNT[Pulse.HIGH]} high pulses.")
print("Part 1:", PULSE_COUNT[Pulse.LOW] * PULSE_COUNT[Pulse.HIGH] * (1000/button_push_count) * (1000/button_push_count))
"""

# Part 2:
# rx is the output module to hj (conjunction node)
# hj has the following inputs: ks, jf, qs, zk (which connect respectively to the flip flop modules )
# hj will only send a low pulse to rx when all connecting modules have received a high pulse 
# The connecting modules are also conjunction modules so they will only send a high pulse if not all connecting modules have sent high pulses
# Hopefully they receive a high pulse with a regular frequency so we calculate the period for each module and calculate the lcm to get the value for rx
# (Assuming there is no phase in the cycle)

RELEVANT_PULSES_FOUND = {'ks':0, 'jf':0, 'qs':0, 'zk':0}
cycle_periods = dict()
cycle_period = 0

while not all(RELEVANT_PULSES_FOUND.values()):
    modules = push_button_and_process_pulses(modules)
    cycle_period += 1

    for module, found in RELEVANT_PULSES_FOUND.items():
        if found and module not in cycle_periods.keys():
            cycle_periods[module] = cycle_period

print("Part 2: min number of button pushes:", reduce(mul, cycle_periods.values()))

end_time = time()

print(f"Calculated solution in {end_time - start_time} seconds")

