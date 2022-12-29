import numpy as np
from aocd import get_data
from itertools import chain
def create_move_proposal(current_elf_row, current_elf_col, current_round):

    def check_north():
        return ground_map[current_elf_row - 1, current_elf_col - 1: current_elf_col + 2].sum() == 0

    def check_south():
        return ground_map[current_elf_row + 1, current_elf_col - 1: current_elf_col + 2].sum() == 0

    def check_west():
        return ground_map[current_elf_row - 1: current_elf_row + 2, current_elf_col - 1].sum() == 0

    def check_east():
        return ground_map[current_elf_row - 1: current_elf_row + 2, current_elf_col + 1].sum() == 0

    north = (current_elf_row - 1, current_elf_col)
    south = (current_elf_row + 1, current_elf_col)
    west = (current_elf_row, current_elf_col - 1)
    east = (current_elf_row, current_elf_col + 1)

    checks = [check_north(), check_south(), check_west(), check_east()]
    if not any(checks): return None

    proposals = [north, south, west, east]
    first_proposal_to_consider = current_round % 4
    temp = ["N", "S", "W", "E"]
    ordered_checks = checks[first_proposal_to_consider:] + checks[:first_proposal_to_consider]
    ordered_proposals = proposals[first_proposal_to_consider:] + proposals[:first_proposal_to_consider]
    ordered_temp = temp[first_proposal_to_consider:] + proposals[:first_proposal_to_consider]
    chosen_dir = ordered_temp[np.argmax(ordered_checks)]
    return ordered_proposals[np.argmax(ordered_checks)]

def find_elves_with_common_proposal(move_proposals_dict):
    rev_dict = {}
    for key, value in move_proposals_dict.items():
        rev_dict.setdefault(value, set()).add(key)

    result = set(chain.from_iterable(
        values for key, values in rev_dict.items()
        if len(values) > 1))

    return result


lines = get_data(day=23)
#with open("test_input.txt") as f:
#    lines = f.read()

GROUND = 0
ELF = 1

ground_map = [[letter for letter in line] for line in lines.replace(".", str(GROUND)).replace("#", str(ELF)).splitlines()]
ground_map = np.array(ground_map).astype(int)
ground_map = np.pad(ground_map, 1000, "constant")

# Get the positions of all the elves
elf_coords = list(zip(*np.where(ground_map == ELF)))
n_elfs = len(elf_coords)
# Calculate movement proposals
#for game_round in range(10):
game_round = 0
while True:
    print(game_round)

    move_proposals = dict()
    elf_coords = list(zip(*np.where(ground_map == ELF)))
    assert len(elf_coords) == n_elfs

    for elf_row, elf_col in elf_coords:

        # If there are no elves in the 8 positions around then don't move
        if ground_map[elf_row-1:elf_row+2, elf_col-1:elf_col+2].sum() == 1:
            continue

        # Otherwise check each direction
        elf_move_proposal = create_move_proposal(elf_row, elf_col, game_round)
        if elf_move_proposal is not None:
            move_proposals[(elf_row, elf_col)] = elf_move_proposal

    # Now if there are two elves who want to move to the same positions delete their proposals
    elves_w_duplicate_proposals = find_elves_with_common_proposal(move_proposals)
    for elf_coord in elves_w_duplicate_proposals:
        del move_proposals[elf_coord]

    if len(move_proposals) == 0:
        break

    # Now make the moves
    for start_coords, end_coords in move_proposals.items():
        ground_map[start_coords[0], start_coords[1]] = GROUND
        ground_map[end_coords[0], end_coords[1]] = ELF
        #elf_coords.remove(start_coords)
        #elf_coords.append(end_coords)

    game_round += 1

    #print(f"Round {game_round + 1}")
    #print(
    #    '\n'.join([''.join(line).replace(str(GROUND), ".").replace(str(ELF), "#") for line in ground_map.astype(str)]))
    #print()

"""
# Trim down the map to only the positions where there are elves
elf_rows, elf_cols = np.where(ground_map == ELF)
trimmed_ground_map = ground_map[min(elf_rows): max(elf_rows) + 1, min(elf_cols): max(elf_cols) + 1 ]
#print(f"Trimmed map:")
#print(
#    '\n'.join([''.join(line).replace(str(GROUND), ".").replace(str(ELF), "#") for line in trimmed_ground_map.astype(str)]))
part1_result = (trimmed_ground_map == GROUND).sum()
print("Part 1 result:", part1_result)
"""

print("First round where no elf moves:", game_round + 1)