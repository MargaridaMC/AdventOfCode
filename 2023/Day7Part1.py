from aocd import get_data
from collections import Counter
from dataclasses import dataclass
input = ["32T3K 765",
"T55J5 684",
"KK677 28",
"KTJJT 220",
"QQQJA 483"]
input = get_data(day=7).splitlines()

@dataclass
class Hand:
    hand: str
    bid: int
    type: int = 0

    def __post_init__(self):
        self.type = classify_hand(self.hand)
    
def classify_hand(hand):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    letter_count = dict(Counter(hand))

    if 5 in letter_count.values(): return FIVE_OF_A_KIND
    if 4 in letter_count.values(): return FOUR_OF_A_KIND
    if 3 in letter_count.values():
        if 2 in letter_count.values(): return FULL_HOUSE
        return THREE_OF_A_KIND
    if 2 in letter_count.values():
        if Counter(letter_count.values())[2] == 2: return TWO_PAIR
        return ONE_PAIR
    return HIGH_CARD

def compare_hands_of_equal_type(hand1, hand2):
    # Returns true if hand2 is larger than hand1
    LETTER_VALUE_MAPPING = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
    for l1, l2 in zip(hand1, hand2):
        if l2 != l1:
            return LETTER_VALUE_MAPPING[l2] > LETTER_VALUE_MAPPING[l1]

def quicksort(hand_bid_list):
    if len(hand_bid_list) <= 1:
        return hand_bid_list
    hand1 = hand_bid_list[0]
    smaller_values = []
    larger_values = []
    for hand2 in hand_bid_list[1:]:
        hand2_is_larger = hand2.type > hand1.type or (hand2.type == hand1.type and compare_hands_of_equal_type(hand1.hand, hand2.hand))
        if hand2_is_larger:
            larger_values.append(hand2)
        else:
            smaller_values.append(hand2)
    return quicksort(smaller_values) + [hand1] + quicksort(larger_values)

hand_list = [Hand(l.split(" ")[0], int(l.split(" ")[1])) for l in input]
sorted_hand_bid_list = quicksort(hand_list)
total_winnings = sum([(i+1) * hand.bid for i, hand in enumerate(sorted_hand_bid_list)])
print("Part1: Total winnings:", total_winnings)