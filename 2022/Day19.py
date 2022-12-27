import random

import numpy as np
from aocd import get_data
from dataclasses import dataclass
import re

WAIT_ACTION = 0
BUILD_ORE_ROBOT_ACTION = 1
BUILD_CLAY_ROBOT_ACTION = 2
BUILD_OBSIDIAN_ROBOT_ACTION = 3
BUILD_GEODE_ROBOT_ACTION = 4

lines = get_data(day=19).splitlines()
#with open("test_input.txt") as f:
#    lines = f.read().splitlines()

@dataclass()
class Blueprint:
    idx: int
    geode_robot_cost:dict
    obsidian_robot_cost:dict
    clay_robot_cost:int
    ore_robot_cost:int

    def check_can_build_ore_robot(self, n_ore_available, n_clay_available, n_obsidian_available):
        return n_ore_available >= self.ore_robot_cost

    def check_can_build_clay_robot(self, n_ore_available, n_clay_available, n_obsidian_available):
        return n_ore_available >= self.clay_robot_cost

    def check_can_build_obsidian_robot(self, n_ore_available, n_clay_available, n_obsidian_available):
        return n_ore_available >= self.obsidian_robot_cost["ore"] and n_clay_available >= self.obsidian_robot_cost["clay"]

    def check_can_build_geode_robot(self, n_ore_available, n_clay_available, n_obsidian_available):
        return n_ore_available >= self.geode_robot_cost["ore"] and n_obsidian_available >= self.geode_robot_cost["obsidian"]

    def build_ore_robot(self, n_ore_available, n_clay_available, n_obsidian_available):
        return n_ore_available - self.ore_robot_cost, n_clay_available, n_obsidian_available

    def build_clay_robot(self, n_ore_available, n_clay_available, n_obsidian_available):
        return n_ore_available - self.clay_robot_cost, n_clay_available, n_obsidian_available

    def build_obsidian_robot(self, n_ore_available, n_clay_available, n_obsidian_available):
        return n_ore_available - self.obsidian_robot_cost["ore"], n_clay_available - self.obsidian_robot_cost["clay"], n_obsidian_available

    def build_geode_robot(self, n_ore_available, n_clay_available, n_obsidian_available):
        return n_ore_available - self.geode_robot_cost["ore"], n_clay_available, n_obsidian_available - self.geode_robot_cost["obsidian"]

@dataclass
class State:
    n_ore: int
    n_clay: int
    n_obsidian: int
    n_geodes: int
    n_ore_robots: int
    n_clay_robots: int
    n_obsidian_robots: int
    n_geode_robots: int

    def get_allowed_actions(self, bp):
        allowed_actions = [WAIT_ACTION]
        if bp.check_can_build_ore_robot(self.n_ore, self.n_clay, self.n_obsidian): allowed_actions.append(BUILD_ORE_ROBOT_ACTION)
        if bp.check_can_build_clay_robot(self.n_ore, self.n_clay, self.n_obsidian): allowed_actions.append(BUILD_CLAY_ROBOT_ACTION)
        if bp.check_can_build_obsidian_robot(self.n_ore, self.n_clay, self.n_obsidian): allowed_actions.append(BUILD_OBSIDIAN_ROBOT_ACTION)
        if bp.check_can_build_geode_robot(self.n_ore, self.n_clay, self.n_obsidian): allowed_actions.append(BUILD_GEODE_ROBOT_ACTION)
        return allowed_actions

    def go_to_next_state(self, action, bp):

        # Regardless of the action chosen the existing robots produce materials
        n_ore = self.n_ore + self.n_ore_robots
        n_clay = self.n_clay + self.n_clay_robots
        n_obsidian = self.n_obsidian + self.n_obsidian_robots
        n_geodes = self.n_geodes + self.n_geode_robots
        n_ore_robots = self.n_ore_robots
        n_clay_robots = self.n_clay_robots
        n_obsidian_robots = self.n_obsidian_robots
        n_geode_robots = self.n_geode_robots

        if action == BUILD_ORE_ROBOT_ACTION:
            n_ore, n_clay, n_obsidian = bp.build_ore_robot(n_ore, n_clay, n_obsidian)
            n_ore_robots += 1
        elif action == BUILD_CLAY_ROBOT_ACTION:
            n_ore, n_clay, n_obsidian = bp.build_clay_robot(n_ore, n_clay, n_obsidian)
            n_clay_robots += 1
        elif action == BUILD_OBSIDIAN_ROBOT_ACTION:
            n_ore, n_clay, n_obsidian = bp.build_obsidian_robot(n_ore, n_clay, n_obsidian)
            n_obsidian_robots += 1
        elif action == BUILD_GEODE_ROBOT_ACTION:
            n_ore, n_clay, n_obsidian = bp.build_geode_robot(n_ore, n_clay, n_obsidian)
            n_geode_robots += 1

        return State(n_ore, n_clay, n_obsidian, n_geodes, n_ore_robots, n_clay_robots, n_obsidian_robots, n_geode_robots)

blueprints = []
for line in lines:
    match = re.match("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line)
    blueprint_id, ore_robot_cost, clay_robot_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost = match.groups()
    blueprints.append(Blueprint(int(blueprint_id),
                          ore_robot_cost = int(ore_robot_cost),
                          clay_robot_cost=int(clay_robot_cost),
                          obsidian_robot_cost={"ore": int(obsidian_robot_ore_cost), "clay": int(obsidian_robot_clay_cost)},
                          geode_robot_cost={"ore": int(geode_robot_ore_cost), "obsidian": int(geode_robot_obsidian_cost)},
                          ))


def generate_random_action_sequence(blueprint, length = 24, initial_state=State(0, 0, 0, 0, 1, 0, 0, 0)):
    action_sequence = []
    state = initial_state
    for i in range(length):
        allowed_actions = state.get_allowed_actions(blueprint)
        action = random.choice(allowed_actions)
        state = state.go_to_next_state(action, blueprint)
        action_sequence.append(action)

    return action_sequence

def calculate_n_geodes(action_sequence):
    n_ticks = len(action_sequence)
    positions_of_geode_robot_creation = np.where(np.array(action_sequence) == BUILD_GEODE_ROBOT_ACTION)[0]

    n_geodes = 0
    for pos in positions_of_geode_robot_creation:
        n_geodes += (n_ticks - pos - 1)

    return n_geodes

def rate_action_list(action_sequence):
    n_ticks = len(action_sequence)
    positions_of_geode_robot_creation = np.where(np.array(action_sequence) == BUILD_GEODE_ROBOT_ACTION)[0]

    n_geodes = 0
    for pos in positions_of_geode_robot_creation:
        n_geodes += (n_ticks - pos - 1)

    return n_geodes + sum(action_sequence)

def combine_action_sequences(action_seq1, action_seq2, blueprint, mutation_prob):
    child1 = []
    child2 = []

    child1_state = initial_state
    child2_state = initial_state

    # While they are the same keep them.
    # When they are not choose the action of one parent with 50% probability
    for i, action1 in enumerate(action_seq1):
        child1_allowed_actions = child1_state.get_allowed_actions(blueprint)
        child2_allowed_actions = child2_state.get_allowed_actions(blueprint)

        # With a certain probability just induce a mutation at this point
        if np.random.uniform(0, 1) <= mutation_prob:
            #child1_action = random.choice(child1_allowed_actions)
            #child2_action = random.choice(child2_allowed_actions)
            child1_action = action_seq1[i] + 1 if action_seq1[i] + 1 in child1_allowed_actions else random.choice(child1_allowed_actions)
            child2_action = action_seq2[i] + 1 if action_seq2[i] + 1 in child2_allowed_actions else random.choice(child2_allowed_actions)
        else:
            if np.random.uniform(0, 1) < 0.5:
                child1_action = action1 if action1 in child1_allowed_actions else random.choice(child1_allowed_actions)
                child2_action = action_seq2[i] if action_seq2[i] in child2_allowed_actions else random.choice(child2_allowed_actions)
            else:
                child1_action = action_seq2[i] if action_seq2[i] in child1_allowed_actions else random.choice(child1_allowed_actions)
                child2_action = action1 if action1 in child2_allowed_actions else random.choice(
                    child2_allowed_actions)

        # If it's possible to construct a geode bot just do it
        #if BUILD_GEODE_ROBOT_ACTION in child1_allowed_actions:
        #    child1_action = BUILD_GEODE_ROBOT_ACTION
        #if BUILD_GEODE_ROBOT_ACTION in child2_allowed_actions:
        #    child2_action = BUILD_GEODE_ROBOT_ACTION

        child1.append(child1_action)
        child2.append(child2_action)
        child1_state = child1_state.go_to_next_state(child1_action, blueprint)
        child2_state = child2_state.go_to_next_state(child2_action, blueprint)

    return child1, child2


initial_state = State(0, 0, 0, 0, 1, 0, 0, 0)
mutation_prob = 0.25
time_limit = 32 #24

#total_quality = 0
max_geodes_per_blueprint = []


for blueprint in blueprints[:3]:

    print(f"Calculating quality for blueprint {blueprint.idx}")

    max_geodes = 0
    size_of_generation = 2000
    action_sequence_pool = [generate_random_action_sequence(blueprint, length=time_limit) for _ in range(size_of_generation)]
    n_gens_without_improvement = 0

    for n_gens in range(10000):

        #if n_gens % 1000 == 0 and n_gens != 0:
        #    size_of_generation -= 30

        # Rate the sequences
        rating_per_action_seq = list(map(rate_action_list, action_sequence_pool))

        # Select the top 4 action sequences with highest number of geodes
        action_sequence_pool = [a for _, a in sorted(zip(rating_per_action_seq, action_sequence_pool), reverse=True)][:size_of_generation]

        # Combine the chosen sequences two by two to create children
        random.shuffle(action_sequence_pool)
        new_action_sequences = []
        for i in range(0, len(action_sequence_pool), 2):
            new_action_sequences += combine_action_sequences(action_sequence_pool[i], action_sequence_pool[i+1], blueprint, mutation_prob)
        action_sequence_pool += new_action_sequences

        # Calculate n geodes for all action sequences
        n_geodes_per_action_seq = list(map(calculate_n_geodes, action_sequence_pool))
        gen_max_geodes = max(n_geodes_per_action_seq)

        if gen_max_geodes > max_geodes:
            max_geodes = gen_max_geodes
            n_gens_without_improvement = 0
            print(f"Found a new max geodes at generation {n_gens}: {gen_max_geodes} (Action seq: {action_sequence_pool[np.argmax(n_geodes_per_action_seq)]})")
        else:
            n_gens_without_improvement += 1

        if n_gens_without_improvement >= 1000:
            print(f"Stopping calculation for blueprint {blueprint.idx} due to lack of improvement for the last 1000 generations")
            break

    print(f"Max geodes that can be produced with blueprint {blueprint.idx}: {max_geodes}")
    print()
    max_geodes_per_blueprint.append(max_geodes)
    #total_quality += max_geodes*blueprint.idx

print()
#print("Part 1 result: Total quality level:", total_quality)
print("Number of geodes produced when using the first three blueprints:", max_geodes_per_blueprint)
print("Part 2 result:", np.prod(max_geodes_per_blueprint))

# 9576 ([56, 9, 19]) -> too low
# 10773 ([57, 9, 21]) -> too low