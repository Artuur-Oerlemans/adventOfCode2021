"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re
from itertools import repeat
import math


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


def part1(data):
    """Solve part 1"""
    highest = find_highest(data)
    the_array = create_2d_array(highest)

    for line in data:
        regex = r"^(\d+),(\d+) -> (\d+),(\d+)"
        match = re.search(regex, line)

        x0 = int(match.group(1))
        y0 = int(match.group(2))
        x1 = int(match.group(3))
        y1 = int(match.group(4))

        if x0 == x1:
            if y0 < y1 + 1:
                for y in range(y0, y1 + 1):
                    the_array[x0][y] += 1
            else:
                for y in range(y1, y0 + 1):
                    the_array[x0][y] += 1
        elif y0 == y1:
            if x0 < x1 + 1:
                for x in range(x0, x1 + 1):
                    the_array[x][y0] += 1
            else:
                for x in range(x1, x0 + 1):
                    the_array[x][y0] += 1

    return calc_result(the_array)


def find_highest(data):
    max_width = 0
    for line in data:
        regex = r"^(\d+),(\d+) -> (\d+),(\d+)"
        match = re.search(regex, line)

        for i in range(1, 5):
            if int(match.group(i)) > max_width:
                max_width = int(match.group(i))
    return max_width


def create_2d_array(max_width):
    the_array = []

    for i in range(0, max_width + 1):
        the_array.append(list(repeat(0, max_width + 1)))

    return the_array


def part2(data):
    """Solve part 2"""
    highest = find_highest(data)
    the_array = create_2d_array(highest)

    for line in data:
        regex = r"^(\d+),(\d+) -> (\d+),(\d+)"
        match = re.search(regex, line)

        x0 = int(match.group(1))
        y0 = int(match.group(2))
        x1 = int(match.group(3))
        y1 = int(match.group(4))

        if x0 == x1:
            if y0 < y1 + 1:
                for y in range(y0, y1 + 1):
                    the_array[x0][y] += 1
            else:
                for y in range(y1, y0 + 1):
                    the_array[x0][y] += 1
        elif y0 == y1:
            if x0 < x1 + 1:
                for x in range(x0, x1 + 1):
                    the_array[x][y0] += 1
            else:
                for x in range(x1, x0 + 1):
                    the_array[x][y0] += 1
        elif abs(x1 - x0) - abs(y1 - y0) == 0:
            x_sign = int(math.copysign(1, x1 - x0))
            y_sign = int(math.copysign(1, y1 - y0))
            for i in range(0, abs(x1 - x0) + 1):
                the_array[x0 + x_sign * i][y0 + y_sign * i] += 1

    return calc_result(the_array)

def calc_result(the_array):
    result = 0
    for x in the_array:
        for xy in x:
            if xy > 1:
                result += 1

    return result

def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    # 8111
    # 22088

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        solutions = solve(pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
