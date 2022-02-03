# Standard library imports
import pathlib
import sys
import re
import math
import time


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


def parse_line(line):
    regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
    match = re.search(regex, line)

    minimum = int(match.group(1))
    maximum = int(match.group(2))
    letter = match.group(3)
    password = match.group(4)


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
    winner = [0, 0]

    take_turn(0, position, score, 1, winner)

    return max(winner[0], winner[1])


def take_turn(player, position, score, times, winner):
    possible_rolls = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    if score[0] >= 21:
        winner[0] += times
        return
    if score[1] >= 21:
        winner[1] += times
        return

    for steps in range(3, 10):
        position_copy = position.copy()
        score_copy = score.copy()

        position_copy[player] = ((position_copy[player] + steps - 1) % 10) + 1
        score_copy[player] += position_copy[player]
        take_turn((player + 1) % 2, position_copy, score_copy, times * possible_rolls[steps], winner)



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
