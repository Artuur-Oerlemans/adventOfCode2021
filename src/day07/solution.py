"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
    """Parse input"""
    return [int(i) for i in puzzle_input.split(",")]


def parse_line(line):
    regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
    match = re.search(regex, line)

    minimum = int(match.group(1))
    maximum = int(match.group(2))
    letter = match.group(3)
    password = match.group(4)


def part1(data):
    """Solve part 1"""
    # lowerbound = min(data)
    # upperbound = max(data)
    #
    # lowest_fuel_cost = 9999999999999999999999999999999999999
    #
    # for position in range(lowerbound, upperbound + 1):
    #     fuel_cost = 0
    #     for crab in data:
    #         fuel_cost += abs(crab - position)
    #
    #     if fuel_cost < lowest_fuel_cost:
    #         lowest_fuel_cost = fuel_cost
    # return lowest_fuel_cost

    data.sort()
    lowest_position = data[int(len(data)/2)]
    fuel_cost = 0
    for crab in data:
        fuel_cost += abs(crab - lowest_position)

    return fuel_cost

def part2(data):
    """Solve part 2"""

    lowest_position = lowest_position_part_2(data)

    return calc_fuel_cost_part_2(lowest_position, data)

def lowest_position_part_2(data):
    # originally used brute force with sum_list to first compute the answer
    a = 0
    b = 0
    for crab in data:
        a += 1
        b += 1 - 2 * crab

    return int(-b / (2 * a))

def calc_fuel_cost_part_2(position, data):
    fuel_cost = 0
    for crab in data:
        fuel_cost += sum_list(abs(crab - position))
    return fuel_cost

def sum_list(n):
    return int(n * (n + 1) / 2)


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
