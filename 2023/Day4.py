from aocd import get_data
import re

input = ['Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11']
input = get_data(day=4).splitlines()

point_sum = 0
for card in input:
    card = card.split(": ")[1].replace('  ', ' ').strip()
    winning_numbers, numbers_we_have = card.split(" | ")
    winning_numbers = [int(n) for n in winning_numbers.split(" ")]
    numbers_we_have = [int(n) for n in numbers_we_have.split(" ")]
    n_matches = len(set(winning_numbers).intersection(set(numbers_we_have)))
    if n_matches > 0:
        point_sum += pow(2, n_matches - 1)

print("Part 1: Number of points:", point_sum)

# Part 2
cards_to_look_through = {i: 1 for i in range(1, len(input) + 1)}
card_count = len(input)
while sum(cards_to_look_through.values()) > 0:
    available_cards = [(c, cards_to_look_through[c]) for c in cards_to_look_through.keys() if cards_to_look_through[c] > 0]
    card_id, n_copies = available_cards[0]
    cards_to_look_through[card_id] = 0
    winning_numbers, numbers_we_have = input[card_id - 1].split(": ")[1].replace('  ', ' ').strip().split(" | ")
    winning_numbers = [int(n) for n in winning_numbers.split(" ")]
    numbers_we_have = [int(n) for n in numbers_we_have.split(" ")]
    n_matches = len(set(winning_numbers).intersection(set(numbers_we_have)))

    card_count += (n_matches * n_copies)
    for j in range(1, n_matches + 1):
        cards_to_look_through[card_id + j] += n_copies

print("Part 2: Total card count:", card_count)