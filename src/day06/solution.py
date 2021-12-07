"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
    """Parse input"""
    fishes = puzzle_input.split(",")
    fish_dict = make_empty_dict()

    for fish in fishes:
        fish_dict[int(fish)] += 1

    return fish_dict


def make_empty_dict():
    return {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}


def parse_line(line):
    regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
    match = re.search(regex, line)

    minimum = int(match.group(1))
    maximum = int(match.group(2))
    letter = match.group(3)
    password = match.group(4)


def part1(fish_dict):
    """Solve part 1"""
    for i in range(80):
        fish_dict = update_fishes(fish_dict)

    result = 0
    for i in range(0, 9):
        result += fish_dict[i]
    return result


def update_fishes(fish_dict):
    new_fish_dict = {}
    for i in range(1, 9):
        new_fish_dict[i - 1] += fish_dict[i]

    new_fish_dict[6] += fish_dict[0]
    new_fish_dict[8] += fish_dict[0]
    return new_fish_dict


def part2(fish_dict):
    """Solve part 2"""
    for i in range(256):
        fish_dict = update_fishes(fish_dict)

    result = 0
    for i in range(0, 9):
        result += fish_dict[i]
    return result


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        solutions = solve(pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
