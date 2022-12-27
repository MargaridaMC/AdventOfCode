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
    valve_openings: dict

    def copy(self):
        return State(self.idx, self.my_pos, self.valve_openings.copy())


def get_possible_states_list(all_valves):
    i = 0
    states = dict()
    for my_pos in all_valves:
        for open_valves in product([0, 1], repeat=len(all_valves)):
            state = State(i, my_pos, {all_valves[j]: open_valves[j] for j in range(len(all_valves))})
            states[(my_pos, *open_valves)] = state
            i += 1
    return states

class QLearning:

    def __init__(self, total_episodes = 1000, epsilon = 0.9, alpha = 0.05, gamma = 0.9, graph_distance_matrix = None,
                 state_list = None, action_list=None, initial_state=None, initial_reward_per_episode = 0,
                 epsilon_decay = 0.99, time_limit = 30):

        self.total_episodes = total_episodes
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.graph_distance_matrix = graph_distance_matrix
        self.action_list: list = action_list
        self.state_list: list = state_list
        self.initial_state: State = initial_state
        self.time_limit = time_limit
        self.qtable: pd.DataFrame = self.initialize_q_table()
        self.initial_reward_per_episode = initial_reward_per_episode
        self.epsilon_decay = epsilon_decay

    def initialize_q_table(self):
        n_states = len(self.state_list)
        n_actions = len(self.action_list)
        return pd.DataFrame(index = range(n_states), columns = self.action_list, data = np.zeros((n_states, n_actions)))

    def load_from_file(self, path_to_qtable):
        self.qtable = pd.read_csv(path_to_qtable, index_col = 0)

    def choose_action(self, state, time_remaining):

        allowed_actions = [a for a in self.action_list if a == STAY or (state.valve_openings[a] == 0 and self.graph_distance_matrix.loc[state.my_pos, a] < time_remaining - 1)]
        if len(allowed_actions) == 1:
            return allowed_actions[0]

        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(allowed_actions, 1)[0]
        else:
            if (self.qtable.loc[state.idx, allowed_actions] == 0).all():
                return np.random.choice(allowed_actions, 1)[0]
            return self.qtable.loc[state.idx, allowed_actions].idxmax()

    def do_action(self, current_state: State, action: str, time_remaining: int):

        valves:dict = current_state.valve_openings.copy()
    
        action_reward = 0
        if action == STAY:
            return current_state, 0, time_remaining - 1
        else:
            # Move to another valve
            n_steps_to_new_valve = self.graph_distance_matrix.loc[current_state.my_pos, action]
            if valves[action] == 0:
                valves[action] = 1
                n_steps_to_new_valve += 1
                action_reward = (time_remaining-n_steps_to_new_valve) * flow_rates[action]

            next_state = self.state_list[(action, *valves.values())]

            return next_state, action_reward, time_remaining - n_steps_to_new_valve

    def update_q_table(self, current_state, next_state, action, action_reward):

        self.qtable.loc[current_state.idx, action] = self.qtable.loc[current_state.idx, action] + self.alpha * (
                action_reward + self.gamma * self.qtable.loc[next_state.idx].max() - self.qtable.loc[
                    current_state.idx, action])

    def train(self, verbose = False):

        reward_per_episode = []
        best_action_sequence = None
        best_reward = 0

        for idx, episode in enumerate(range(self.total_episodes)):
            episode_reward, action_seq = self.train_single_episode()
            reward_per_episode.append(episode_reward)

            if episode_reward > best_reward:
                best_reward = episode_reward
                best_action_sequence = action_seq

            if idx%100 == 0:
                self.epsilon *= self.epsilon_decay
                if verbose:
                    print(f"Episode {idx} reward:", episode_reward, "Best so far:", best_reward, f"({','.join(best_action_sequence)})")
        return best_reward, best_action_sequence

    def train_single_episode(self):

        reward_running_sum = self.initial_reward_per_episode
        action_seq = []
        
        # State = [my current position, whether valves are open or not for each valve...]
        current_state = self.initial_state.copy()
        
        time_remaining = self.time_limit

        while time_remaining > 0:

            # Choose and take action
            action = self.choose_action(current_state, time_remaining)
            action_seq.append(action)
            next_state, action_reward, time_remaining = self.do_action(current_state, action, time_remaining)
            reward_running_sum += action_reward

            # Update q table with new values
            self.update_q_table(current_state, next_state, action, action_reward)

            current_state = next_state

        return reward_running_sum, action_seq


relevant_valves = [v for v in valve_list if flow_rates[v] > 0]
all_states = get_possible_states_list(relevant_valves)
initial_state = State(max([v.idx for v in all_states.values()])+1, "AA", {v:0 for v in relevant_valves})
all_states[("AA", *[0]*len(relevant_valves))] = initial_state
action_list = [STAY] + relevant_valves

q = QLearning(graph_distance_matrix = adjacency_matrix, state_list = all_states, action_list=action_list, initial_state=initial_state,
              epsilon=0.65, total_episodes=10000, gamma = 0.89, alpha=0.95, epsilon_decay=0.86)
q.load_from_file("qtable.csv")
best_reward, best_action = q.train(verbose=True)

#q.qtable.to_csv("qtable.csv")

print("Final amount of pressure released:", best_reward)
print("Action sequence:", best_action)

# 1300 (GF,EK,AW,GV,XG,stay,stay,stay) -> too low
# 1423 (GF,EK,YQ,AW,DT,ZB,stay,stay) -> too low
# 1532.0 (GF,EK,AW,YQ,XR,ZB,CD,stay) -> too low
# 1537
# 1574
# 1583
# Found a new best for hyperparameters (0.9500000000000001, 0.8855000000000001, 0.65, 0.86) reward = 1595.0
"""
tested_hyperparameters = dict()
best_hyperparameter_set = None
highest_reward_so_far = 0

alphas = np.linspace(0, 1, 21)
gammas = np.linspace(0.8, 0.99, 21)
epsilon = np.linspace(0, 1, 21)
epsilon_decays = np.linspace(0.8, 1, 21)

def run_single_tuning():

    a = random.choice(alphas)
    g = random.choice(gammas)
    e = random.choice(epsilon)
    e_decay = random.choice(epsilon_decays)

    while (a, g, e, e_decay) in tested_hyperparameters.keys():
        a = random.choice(alphas)
        g = random.choice(gammas)
        e = random.choice(epsilon)
        e_decay = random.choice(epsilon_decays)

    q = QLearning(graph_distance_matrix = adjacency_matrix, state_list = all_states, action_list=action_list, initial_state=initial_state,
              epsilon=e, total_episodes=1000, gamma = g, alpha=a, epsilon_decay=e_decay)
    q.load_from_file("qtable.csv")
    try_reward, _ = q.train()
    tested_hyperparameters[(a, g, e, e_decay)] = try_reward

    global highest_reward_so_far
    global best_hyperparameter_set
    if try_reward > highest_reward_so_far:
        highest_reward_so_far = try_reward
        best_hyperparameter_set = (a, g, e, e_decay)
        print("Found a new best for hyperparameters", best_hyperparameter_set, "reward =", highest_reward_so_far)

    return try_reward

rewards = Parallel(n_jobs=16)(delayed(run_single_tuning)() for i in tqdm(range(1000)))
print(rewards)
print(tested_hyperparameters)

print("Best hyperparameters:", best_hyperparameter_set)
print("Best reward achieved:", highest_reward_so_far)
"""