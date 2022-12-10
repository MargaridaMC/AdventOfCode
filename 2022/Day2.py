from dataclasses import dataclass, field
from aocd import get_data

input = get_data(day=2).splitlines()

ROCK = "R"
PAPER = "P"
SCISSORS = "S"


@dataclass
class RPSMove:
    letter: str = field(repr=False)
    move: str = field(init=False)

    def __post_init__(self):
        letter_move_mapping = {"A": ROCK,
                               "B": PAPER,
                               "C": SCISSORS,
                               "X": ROCK,
                               "Y": PAPER,
                               "Z": SCISSORS}
        self.move = letter_move_mapping[self.letter]

    def __eq__(self, other):
        if type(other) == str:
            return self.move == other
        else:
            return self.move == other.move

    def __gt__(self, other):
        return (self.move == PAPER and other.move == ROCK) or (self.move == ROCK and other.move == SCISSORS) or (
                    self.move == SCISSORS and other.move == PAPER)


score = 0
for play in input:
    other_move, my_move = [RPSMove(letter) for letter in play.split(" ")]

    if my_move.move == ROCK:
        score += 1
    elif my_move.move == PAPER:
        score += 2
    else:
        score += 3

    if my_move > other_move:
        score += 6
    elif my_move == other_move:
        score += 3

# Question 1
print("Final score:", score)

# Question 2
score = 0
for play in input:
    other_move = RPSMove(play.split(" ")[0])
    final_state = play.split(" ")[1]

    if final_state == 'X':
        # We need to loose
        if other_move == ROCK:
            # We play scissors
            score += 3
        elif other_move == PAPER:
            # We play rock
            score += 1
        else:
            # We play paper
            score += 2

    elif final_state == "Y":
        score += 3
        # It's a draw
        if other_move == ROCK:
            score += 1
        elif other_move == PAPER:
            score += 2
        else:
            score += 3

    else:
        # We win
        score += 6
        if other_move == ROCK:
            # We play paper
            score += 2
        elif other_move == PAPER:
            # We play scissors
            score += 3
        else:
            score += 1

print("Final score:", score)
