# Standard library imports
import pathlib
import sys
import re
import math


def parse(puzzle_input):
    """Parse input"""
    return "".join([bin(int(hexi, 16))[2:].zfill(4) for hexi in puzzle_input])


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
    index = 0

    score = 0

    while non_zero_exists(data, index):
        ID = int(data[index + 3: index + 6], 2)
        if ID == 4:
            version, length = read_literal(data, index)
        else:
            version, length = read_operator(data, index)
        index += length
        score += version
    return score


def non_zero_exists(data, index):
    for bit in data[index:]:
        if bit == '1':
            return True
    return False


def read_literal(data, index):
    subindex = 6
    while data[index + subindex] == "1":
        subindex += 5
    # fill = 4 - ((subindex + 5) % 4)
    # length = subindex + 5 + fill
    length = subindex + 5
    return int(data[index:index + 3], 2), length


def read_operator(data, index):
    subindex = 6
    if data[index + subindex] == "0":
        subindex += 1 + 15
    else:
        subindex += 1 + 11

    return int(data[index:index + 3], 2), subindex


def part2(data):
    """Solve part 2"""
    index = 0

    score = 0

    while non_zero_exists(data, index):
        ID = int(data[index + 3: index + 6], 2)
        if ID == 4:
            points, length = read_literal2(data, index)
        else:
            points, length = read_operator2(data, index)
        index += length
        score += points
        print(data[index:])
    return score


def read_literal2(data, index):
    subindex = 6
    literal_binary = data[index + subindex + 1:index + subindex + 1 + 4]
    while data[index + subindex] == "1":
        literal_binary += data[index + subindex + 1 + 5:index + subindex + 1 + 4 + 5]
        subindex += 5
    # fill = 4 - ((subindex + 5) % 4)
    # length = subindex + 5 + fill
    length = subindex + 5
    return int(literal_binary, 2), length


def read_operator2(data, index):
    subindex = 6
    if data[index + subindex] == "0":
        length = int(data[index + subindex + 1: index + subindex + 1 + 15], 2)
        subindex += 1 + 15
        print("length type 0, bits ", length)
        values = read_data(data[index + subindex:], length)
        subindex += length
    else:
        print("length type 1")
        print("data to read", data[index + index:])
        print("number of packets", int(data[index + subindex + 1: index + subindex + 1 + 11], 2))
        values, length = read_subpackets(data[index + subindex + 1 + 11:],
                                         int(data[index + subindex + 1: index + subindex + 1 + 11], 2))
        subindex += 1 + 11 + length

    operator = int(data[index + 3: index + 6], 2)
    points = 0
    if operator == 0:
        points = sum(values)
    elif operator == 1:
        points = math.prod(values)
    elif operator == 2:
        points = min(values)
    elif operator == 3:
        points = max(values)
    elif operator == 4:
        print("something is wrong")
    elif operator == 5:
        if values[0] > values[1]:
            points = 1
    elif operator == 6:
        if values[0] < values[1]:
            points = 1
    elif operator == 7:
        if values[0] == values[1]:
            points = 1

    return points, subindex


def read_data(data, bits):
    values = []
    index = 0
    print("number bits needed", bits)
    while index < bits:
        print("bits so far left", data[index:])
        ID = int(data[index + 3: index + 6], 2)
        if ID == 4:
            points, length = read_literal2(data, index)
        else:
            points, length = read_operator2(data, index)
        index += length
        values.append(points)
    print("bits left", index - bits, "number bits needed", bits)
    return values


def read_subpackets(data, total):
    values = []
    index = 0
    while len(values) < total:
        print("total", total)
        print("data left", data[index:])
        print("values", values)
        ID = int(data[index + 3: index + 6], 2)
        if ID == 4:
            points, length = read_literal2(data, index)
        else:
            points, length = read_operator2(data, index)
        index += length
        values.append(points)
    print("read_subpackets bits left", len(data) - index)
    return values, index


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
