# Standard library imports
import copy
import pathlib
import sys
import re
import json


def parse(puzzle_input):
    """Parse input"""
    return [json.loads(line) for line in puzzle_input.splitlines()]


def parse_line(line):
    regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
    match = re.search(regex, line)

    minimum = int(match.group(1))
    maximum = int(match.group(2))
    letter = match.group(3)
    password = match.group(4)


def part1(data):
    """Solve part 1"""
    print(data)
    total = compress(data[0])
    print(total)
    for line in data[1:]:
        total = compress([total, line])

    return calc_magnitude(total)


def compress(line):
    changed = True
    while changed:
        changed = False
        location_4_deep = find_first_4_deep_pair(line)
        location_split = find_splittable_regular(line)

        if location_4_deep:
            changed = True
            explode(line, location_4_deep)
        elif location_split:
            changed = True
            split(line, location_split)

    return line


def explode(line, location_pair):
    pair = get_pair(line, location_pair)

    right_regular_location = find_right_regular(line, location_pair)
    if right_regular_location:
        pair_of_right_regular = get_pair(line, right_regular_location[:len(right_regular_location) - 1])
        pair_of_right_regular[right_regular_location[-1]] += pair[1]

    left_regular_location = find_left_regular(line, location_pair)
    if left_regular_location:
        pair_of_left_regular = get_pair(line, left_regular_location[:len(left_regular_location) - 1])
        pair_of_left_regular[left_regular_location[-1]] += pair[0]

    pair_to_remove_from = get_pair(line, location_pair[:3])
    pair_to_remove_from[location_pair[-1]] = 0


def find_left_regular(line, location_pair):
    location = location_pair.copy()
    value = location.pop()
    while value == 0:
        if location:
            value = location.pop()
        else:
            value = -1

    if value == -1:
        return []
    location.append(0)
    while isinstance(get_pair(line, location), list):
        location.append(1)
    return location


def find_right_regular(line, location_pair):
    location = location_pair.copy()
    value = location.pop()
    while value == 1:
        if location:
            value = location.pop()
        else:
            value = -1

    if value == -1:
        return []
    location.append(1)
    while isinstance(get_pair(line, location), list):
        location.append(0)
    return location


def find_first_4_deep_pair(line):
    location = [0]
    while location:
        if len(location) == 5:
            return location[:4]

        if isinstance(get_pair(line, location), list):
            location.append(0)
        elif location[-1] == 0:
            location[-1] = 1
        else:
            value = location.pop()
            while value == 1 and len(location) > 0:
                value = location.pop()
                if value == 0:
                    location.append(1)
    return []


def find_splittable_regular(line):
    location = [0]
    while location:
        here_at = get_pair(line, location)
        if isinstance(here_at, list):
            location.append(0)
        elif here_at >= 10:
            return location
        elif location[-1] == 0:
            location[-1] = 1
        else:
            value = location.pop()
            while value == 1 and len(location) > 0:
                value = location.pop()
                if value == 0:
                    location.append(1)
    return []


def split(line, location_split):
    pair_of_split = get_pair(line, location_split[:len(location_split) - 1])
    to_split = pair_of_split[location_split[-1]]
    pair_of_split[location_split[-1]] = [to_split // 2, to_split - (to_split // 2)]


def get_pair(line, location):
    pair = line
    for step in location:
        pair = pair[step]
    return pair


def calc_magnitude(line):
    left = line[0]
    right = line[1]
    if isinstance(left, list):
        left = calc_magnitude(left)
    if isinstance(right, list):
        right = calc_magnitude(right)
    return 3 * left + 2 * right


def part2(data):
    """Solve part 2"""
    max_magnitude = 0
    for index1 in range(0, len(data)):
        for index2 in range(0, len(data)):
            if index1 != index2:
                line = compress([copy.deepcopy(data[index1]), copy.deepcopy(data[index2])])
                magnitude = calc_magnitude(line)
                if magnitude > max_magnitude:
                    max_magnitude = magnitude

    return max_magnitude



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
