import itertools
import random
import re
import pandas as pd
from Graph import *
import numpy as np
from aocd import get_data
from tqdm import tqdm
from joblib import Parallel, delayed
from itertools import product
from dataclasses import dataclass

lines = get_data(day=16).splitlines()
#with open("test_input.txt") as f:
#    lines = f.read().splitlines()

STAY = "stay"

# Calculate distance matrix across all nodes
valve_list = []
neighbours_per_valve = {}
flow_rates = {}
for line in lines:
    match = re.match(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([A-Z\s,]+)", line)
    if match:
        valve, flow, tunnels = match.groups()
        valve_list.append(valve)
        flow_rates[valve] = int(flow)
        neighbours_per_valve[valve] = tunnels.split(", ")
init_graph = {v: dict() for v in neighbours_per_valve.keys()}
for valve, neighbours in neighbours_per_valve.items():
    init_graph[valve] = {neighbour: 1 for neighbour in neighbours}

adjacency_matrix = pd.DataFrame(columns=valve_list, index=valve_list, dtype = int)
graph = Graph(valve_list, init_graph)
for i, valve1 in enumerate(valve_list):
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=valve1)
    adjacency_matrix.loc[valve1] = shortest_path

@dataclass
class State:
    idx: int
    my_pos: str
    elephant_pos: str
    valve_openings: dict

    def copy(self):
        return State(self.idx, self.my_pos, self.elephant_pos, self.valve_openings.copy())


class QLearning:

    def __init__(self, total_episodes = 1000, epsilon = 0.9, alpha = 0.05, gamma = 0.9, graph_distance_matrix = None,
                 action_list=None, initial_state: State=None, initial_reward_per_episode = 0,
                 epsilon_decay = 0.99, time_limit = 26):

        self.total_episodes = total_episodes
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.graph_distance_matrix = graph_distance_matrix
        self.action_list: list = action_list
        self.state_list: dict = dict()
        self.state_list[(initial_state.my_pos, initial_state.elephant_pos, *initial_state.valve_openings)] = initial_state
        self.initial_state: State = initial_state
        self.time_limit = time_limit
        self.qtable: pd.DataFrame = self.initialize_q_table()
        self.initial_reward_per_episode = initial_reward_per_episode
        self.epsilon_decay = epsilon_decay

    def initialize_q_table(self):
        #n_states = len(self.state_list) + 1
        n_actions = len(self.action_list)
        table = pd.DataFrame(index = [0], columns = [str(a) for a in self.action_list], data = np.zeros((1, n_actions)))
        return table

    def load_from_file(self, path_to_qtable):
        self.qtable = pd.read_csv(path_to_qtable, index_col = 0)

    def choose_action(self, state, time_remaining_for_me, time_remaining_for_elephant):

        actions_allowed_for_me = [a for a in self.action_list if a[0] == STAY or
                                  (state.valve_openings[a[0]] == 0 and
                                   self.graph_distance_matrix.loc[state.my_pos, a[0]] + 1 <= time_remaining_for_me)
                                  ]
        allowed_actions = [a for a in actions_allowed_for_me if
                                    a[1] == STAY or (
                                        state.valve_openings[a[1]] == 0 and
                                        self.graph_distance_matrix.loc[state.elephant_pos, a[1]] + 1 <= time_remaining_for_elephant
                                    )]

        if len(allowed_actions) == 1:
            return allowed_actions[0]

        if np.random.uniform(0, 1) < self.epsilon:
            return random.sample(allowed_actions, 1)[0]
        else:
            allowed_actions = list(map(str, allowed_actions))
            if (self.qtable.loc[state.idx, allowed_actions] == 0).all():
                return eval(random.sample(allowed_actions, 1)[0])
            return eval(self.qtable.loc[state.idx, allowed_actions].idxmax())

    def do_action(self, current_state: State, action: str, time_remaining_for_me: int,
                  time_remaining_for_elephant: int):

        valves:dict = current_state.valve_openings.copy()
        action_for_me, action_for_elephant = action
    
        action_reward = 0
        if action_for_me == STAY:
            my_final_pos = current_state.my_pos
            time_remaining_for_me -= 1
        else:
            my_final_pos = action_for_me
            n_steps_to_new_valve = self.graph_distance_matrix.loc[current_state.my_pos, my_final_pos]

            if valves[my_final_pos] == 0:
                valves[my_final_pos] = 1
                n_steps_to_new_valve += 1
                action_reward += (time_remaining_for_me - n_steps_to_new_valve) * flow_rates[action_for_me]

            time_remaining_for_me -= n_steps_to_new_valve

        if action_for_elephant == STAY:
            elephant_final_pos = current_state.elephant_pos
            time_remaining_for_elephant -= 1
        else:
            elephant_final_pos = action_for_elephant
            n_steps_to_new_valve = self.graph_distance_matrix.loc[current_state.elephant_pos, action_for_elephant]

            if valves[elephant_final_pos] == 0:
                valves[elephant_final_pos] = 1
                n_steps_to_new_valve += 1
                action_reward += (time_remaining_for_elephant - n_steps_to_new_valve) * flow_rates[action_for_elephant]

            time_remaining_for_elephant -= n_steps_to_new_valve

        if (my_final_pos, elephant_final_pos, *valves.values()) in self.state_list.keys():
            next_state = self.state_list[(my_final_pos, elephant_final_pos, *valves.values())]
        else:
            next_state = State(max([s.idx for s in self.state_list.values()]) + 1, my_final_pos, elephant_final_pos, valves)
            self.state_list[(my_final_pos, elephant_final_pos, *valves.values())] = next_state

        return next_state, action_reward, time_remaining_for_me, time_remaining_for_elephant

    def update_q_table(self, current_state, next_state, action, action_reward):

        if next_state.idx not in self.qtable.index:
            self.qtable.loc[next_state.idx] = 0

        self.qtable.loc[current_state.idx, str(action)] = self.qtable.loc[current_state.idx, str(action)] + self.alpha * (
                action_reward + self.gamma * self.qtable.loc[next_state.idx].max() - self.qtable.loc[
                    current_state.idx, str(action)])

    def train(self, verbose = False):

        reward_per_episode = []
        best_action_sequence = None
        best_reward = 0

        for idx, episode in enumerate(range(self.total_episodes)):
            episode_reward, action_seq, rois, time_stamps = self.train_single_episode()
            reward_per_episode.append(episode_reward)

            if episode_reward > best_reward:
                best_reward = episode_reward
                best_action_sequence = action_seq
                if verbose:
                    print()
                    print(f"New max reward: {best_reward} on episode {idx}")
                    print("AA|AA", self.time_limit, "|", self.time_limit)
                    for i, action_pair in enumerate(action_seq):
                        print(f"{action_pair[0]}|{action_pair[1]} {time_stamps[i][0]}|{time_stamps[i][1]} -> Action reward: {rois[i]}")

            if idx%100 == 0:
                self.epsilon *= self.epsilon_decay
        return best_reward, best_action_sequence

    def train_single_episode(self):

        reward_running_sum = 0
        action_seq = []
        rois = []
        time_stamps = []
        
        # State = [my current position, whether valves are open or not for each valve...]
        current_state = self.initial_state.copy()
        
        time_remaining_for_me = self.time_limit
        time_remaining_for_elephant = self.time_limit

        while time_remaining_for_me > 0 or time_remaining_for_elephant > 0:

            action = self.choose_action(current_state, time_remaining_for_me, time_remaining_for_elephant)

            if action[0] != STAY:
                assert self.graph_distance_matrix.loc[current_state.my_pos, action[0]] <= (time_remaining_for_me - 1)
            if action[1] != STAY:
                assert self.graph_distance_matrix.loc[current_state.elephant_pos, action[1]] <= (time_remaining_for_elephant - 1)

            action_seq.append(action)
            next_state, action_reward, time_remaining_for_me, time_remaining_for_elephant = self.do_action(current_state, action,
                                                                              time_remaining_for_me, time_remaining_for_elephant)
            rois.append(action_reward)
            time_stamps.append((time_remaining_for_me, time_remaining_for_elephant))
            reward_running_sum += action_reward

            # Update q table with new values
            self.update_q_table(current_state, next_state, action, action_reward)

            current_state = next_state

        return reward_running_sum, action_seq, rois, time_stamps


relevant_valves = [v for v in valve_list if flow_rates[v] > 0]
initial_state = State(0, "AA", "AA", {v:0 for v in relevant_valves})

action_list = list(itertools.combinations([STAY] + relevant_valves, 2))
action_list += [a[::-1] for a in action_list]
action_list.append((STAY, STAY))
"""
a, g, e, e_decay = (0.75, 0.876, 0.25, 0.98)
q = QLearning(graph_distance_matrix = adjacency_matrix, action_list=action_list, initial_state=initial_state,
              epsilon=e, total_episodes=10000, gamma = g, alpha=a, epsilon_decay=e_decay, time_limit=26)
best_reward, best_action = q.train(verbose=True)

print("Final amount of pressure released:", best_reward)
print("Action sequence:", best_action)
"""
tested_hyperparameters = dict()
best_hyperparameter_set = None
highest_reward_so_far = 0

alphas = np.linspace(0, 1, 21)
gammas = np.linspace(0.8, 0.99, 21)
epsilon = np.linspace(0, 1, 21)
epsilon_decays = np.linspace(0.8, 1, 21)

def run_single_tuning(i):

    a = random.choice(alphas)
    g = random.choice(gammas)
    e = random.choice(epsilon)
    e_decay = random.choice(epsilon_decays)

    while (a, g, e, e_decay) in tested_hyperparameters.keys():
        a = random.choice(alphas)
        g = random.choice(gammas)
        e = random.choice(epsilon)
        e_decay = random.choice(epsilon_decays)

    q = QLearning(graph_distance_matrix = adjacency_matrix, action_list=action_list, initial_state=initial_state,
              epsilon=e, total_episodes=1000, gamma = g, alpha=a, epsilon_decay=e_decay, time_limit=26)
    #q.load_from_file("qtable.csv")
    try_reward, try_action_seq = q.train()
    tested_hyperparameters[(a, g, e, e_decay)] = try_reward

    global highest_reward_so_far
    global best_hyperparameter_set
    if try_reward > highest_reward_so_far:
        highest_reward_so_far = try_reward
        best_hyperparameter_set = (a, g, e, e_decay)
        print("Run", i, "Found a new best for hyperparameters", best_hyperparameter_set, "reward =", highest_reward_so_far, "Actions:", try_action_seq)

    return try_reward

#rewards = Parallel(n_jobs=16)(delayed(run_single_tuning)(i) for i in tqdm(range(1000)))
rewards = []
for i in tqdm(range(1000)):
    rewards.append(run_single_tuning(i))

print(rewards)
print(tested_hyperparameters)

print("Best hyperparameters:", best_hyperparameter_set)
print("Best reward achieved:", highest_reward_so_far)
