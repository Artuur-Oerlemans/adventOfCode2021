"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
    """Parse input"""
    return [[int(i) for i in line] for line in puzzle_input.splitlines()]


def parse_line(line):
    regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
    match = re.search(regex, line)

    minimum = int(match.group(1))
    maximum = int(match.group(2))
    letter = match.group(3)
    password = match.group(4)


def part1(data):
    """Solve part 1"""
    width = len(data[0])
    length = len(data)

    score = 0

    for x in range(0, width):
        for y in range(0, length):
            score += calc_low_point_score(x, y, data, width, length)

    return score


def calc_low_point_score(x, y, data, width, length):
    for xd in range(max(0, x - 1), min(width, x + 2)):
        if data[y][x] >= data[y][xd] and x != xd:
            return 0
    for yd in range(max(0, y - 1), min(length, y + 2)):
        if data[y][x] >= data[yd][x] and y != yd:
            return 0
    return data[y][x] + 1


def part2(data):
    """Solve part 2"""
    width = len(data[0])
    length = len(data)

    score = 0
    low_points = set()

    for x in range(0, width):
        for y in range(0, length):
            if calc_low_point_score(x, y, data, width, length) > 0:
                low_points.add((y, x))

    basin_sizes = []
    for point in low_points:
        basin_sizes.append(calc_basin_size(point, data, width, length, low_points))

    basin_sizes.sort()
    return basin_sizes

def calc_basin_size(point, data, width, length, low_points):
    basin = {point}
    adjacents = set()

    for xd in range(max(0, point[1] - 1), min(width, point[1] + 2)):
        if 9 != data[point[0]][xd] and point[1] != xd:
            adjacents.add((point[0], xd))
    for yd in range(max(0, point[0] - 1), min(length, point[0] + 2)):
        if 9 != data[yd][point[1]] and point[0] != yd:
            adjacents.add((yd, point[1]))

    while len(adjacents) != 0:
        adjacent = adjacents.pop()
        basin.add(adjacent)
        expand_basin(adjacent, data, width, length, basin, adjacents)
    print(basin)
    return len(basin)


def expand_basin(point, data, width, length, basin, adjacents):
    for xd in range(max(0, point[1] - 1), min(width, point[1] + 2)):
        if 9 != data[point[0]][xd] and (point[0], xd) not in basin and (point[0], xd) not in adjacents:
            adjacents.add((point[0], xd))
    for yd in range(max(0, point[0] - 1), min(length, point[0] + 2)):
        if 9 != data[yd][point[1]] and (yd, point[1]) not in basin and (yd, point[1]) not in adjacents:
            adjacents.add((yd, point[1]))


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
