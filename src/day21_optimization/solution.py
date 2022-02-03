# Standard library imports
import pathlib
import sys
import re
import math
import functools
import time


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


def part1(data):
    """Solve part 1"""
    position = [10, 7]
    score = [0, 0]
    dice_rolls = 0

    turn = 0
    while score[0] < 1000 and score[1] < 1000:
        rolls = 0
        for i in range(0, 3):
            dice_rolls += 1
            rolls += ((dice_rolls - 1) % 100) + 1
        position[turn] = ((position[turn] + rolls - 1) % 10) + 1
        score[turn] += position[turn]
        turn = (turn + 1) % 2

    return dice_rolls * min(score[0], score[1])


def part2(data):
    """Solve part 1"""
    position = [10, 7]
    score = [0, 0]

    winner = take_turn(0, 10, 7, 0, 0, 1)

    return max(winner[0], winner[1])


@functools.cache
def take_turn(player, position_0, position_1, score_0, score_1, times):
    possible_rolls = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    winner_0 = 0
    winner_1 = 0
    if score_0 >= 21:
        winner_0 += times
        return winner_0, winner_1
    if score_1 >= 21:
        winner_1 += times
        return winner_0, winner_1

    for steps in range(3, 10):
        if player == 0:
            position_0_new = ((position_0 + steps - 1) % 10) + 1
            score_0_new = score_0 + position_0_new
            winner_0_next, winner_1_next = take_turn((player + 1) % 2, position_0_new, position_1, score_0_new, score_1,
                                                     times * possible_rolls[steps])
        else:
            position_1_new = ((position_1 + steps - 1) % 10) + 1
            score_1_new = score_1 + position_1_new
            winner_0_next, winner_1_next = take_turn((player + 1) % 2, position_0, position_1_new, score_0, score_1_new,
                                                     times * possible_rolls[steps])
        winner_0 += winner_0_next
        winner_1 += winner_1_next
    return winner_0, winner_1


def solve(path):
    """Solve the puzzle for the given input"""

    puzzle_input = pathlib.Path(path).read_text().strip()
    data = parse(puzzle_input)
    start_1 = time.time()
    solution1 = part1(data)
    end_1 = time.time()
    print("time part 1:", end_1 - start_1)

    puzzle_input = pathlib.Path(path).read_text().strip()
    data = parse(puzzle_input)
    start_2 = time.time()
    solution2 = part2(data)
    end_2 = time.time()
    print("time part 2:", end_2 - start_2)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        solutions = solve(path)
        print("\n".join(str(solution) for solution in solutions))
