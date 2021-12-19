# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
    """Parse input"""
    return [[int(risk) for risk in line] for line in puzzle_input.splitlines()]


def parse_line(line):
    regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
    match = re.search(regex, line)

    minimum = int(match.group(1))
    maximum = int(match.group(2))
    letter = match.group(3)
    password = match.group(4)


def part1(data):
    """Solve part 1"""
    width_x = len(data)
    width_y = len(data[0])

    easiest_route = []
    first_line = [0]
    for y in range(1, width_y):
        first_line.append(data[0][y] + first_line[y - 1])
    easiest_route.append(first_line)

    for x in range(1, width_x):
        line = list()
        line.append(easiest_route[x - 1][0] + data[x][0])
        for y in range(1, width_y):
            line.append(min(data[x][y] + line[y - 1], data[x][y] + easiest_route[x - 1][y]))
        easiest_route.append(line)

    updated = True
    while updated:
        updated = False
        for x in range(0, width_x):
            for y in range(0, width_y):
                for xd in range(max(0, x - 1), min(width_x - 1, x + 2)):
                    if easiest_route[xd][y] + data[x][y] < easiest_route[x][y] and xd != x:
                        updated = True
                        easiest_route[x][y] = easiest_route[xd][y] + data[x][y]
                for yd in range(max(0, y - 1), min(width_y - 1, y + 2)):
                    if easiest_route[x][yd] + data[x][y] < easiest_route[x][y] and yd != y:
                        updated = True
                        easiest_route[x][y] = easiest_route[x][yd] + data[x][y]

    return easiest_route[width_x - 1][width_y - 1]


def risk(data, x, y):
    width_x = len(data)
    width_y = len(data[0])
    increase_risk = x // width_x + y // width_y

    return (data[x % width_x][y % width_y] + increase_risk - 1) % 9 + 1


def part2(data):
    """Solve part 2"""
    width_x = len(data) * 5
    width_y = len(data[0]) * 5

    easiest_route = []
    first_line = [0]
    for y in range(1, width_y):
        first_line.append(risk(data, 0, y) + first_line[y - 1])
    easiest_route.append(first_line)

    for x in range(1, width_x):
        line = list()
        line.append(easiest_route[x - 1][0] + risk(data, x, 0))
        for y in range(1, width_y):
            line.append(min(risk(data, x, y) + line[y - 1], risk(data, x, y) + easiest_route[x - 1][y]))
        easiest_route.append(line)

    updated = True
    while updated:
        updated = False
        for x in range(0, width_x):
            for y in range(0, width_y):
                for xd in range(max(0, x - 1), min(width_x - 1, x + 2)):
                    if easiest_route[xd][y] + risk(data, x, y) < easiest_route[x][y] and xd != x:
                        updated = True
                        easiest_route[x][y] = easiest_route[xd][y] + risk(data, x, y)
                for yd in range(max(0, y - 1), min(width_y - 1, y + 2)):
                    if easiest_route[x][yd] + risk(data, x, y) < easiest_route[x][y] and yd != y:
                        updated = True
                        easiest_route[x][y] = easiest_route[x][yd] + risk(data, x, y)
        print()

    return easiest_route[width_x - 1][width_y - 1]


def solve(path):
    """Solve the puzzle for the given input"""
    puzzle_input = pathlib.Path(path).read_text().strip()
    data = parse(puzzle_input)
    solution1 = part1(data)

    puzzle_input = pathlib.Path(path).read_text().strip()
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        solutions = solve(path)
        print("\n".join(str(solution) for solution in solutions))
