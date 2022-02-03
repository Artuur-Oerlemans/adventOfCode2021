# Standard library imports
import pathlib
import sys
import re
import math


def parse(puzzle_input):
    """Parse input"""
    parts = puzzle_input.split("\n\n")
    algorithm = [0 if char == "." else 1 for char in parts[0]]
    input_image = [[0 if char == "." else 1 for char in line] for line in parts[1].splitlines()]
    return algorithm, input_image


def parse_line(line):
    regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
    match = re.search(regex, line)

    minimum = int(match.group(1))
    maximum = int(match.group(2))
    letter = match.group(3)
    password = match.group(4)


def part1(algorithm, input_image):
    """Solve part 1"""
    output_image = set()
    for x in range(-1, len(input_image) + 2):
        for y in range(-1, len(input_image[0]) + 2):
            bin_value = ""
            for xd in range(x - 1, x + 2):
                for yd in range(y - 1, y + 2):
                    if 0 <= xd < len(input_image) and 0 <= yd < len(input_image[0]):
                        bin_value += str(input_image[xd][yd])
                    else:
                        bin_value += str(0)
            if algorithm[int(bin_value, 2)] == 1:
                output_image.add((x, y))
    print(output_image)
    print(len(output_image))
    rep_output_image = set()

    for x in range(-2, len(input_image) + 3):
        for y in range(-2, len(input_image[0]) + 3):
            bin_value = ""
            for xd in range(x - 1, x + 2):
                for yd in range(y - 1, y + 2):
                    if -1 <= xd < len(input_image) + 2 and -1 <= yd < len(input_image[0]) + 2:
                        if (xd, yd) in output_image:
                            bin_value += str(1)
                        else:
                            bin_value += str(0)
                    else:
                        bin_value += str(algorithm[0])
            if algorithm[int(bin_value, 2)] == 1:
                rep_output_image.add((x, y))

    for time in range(2, 51):
        output_image = enhance_again(output_image, algorithm, time, len(input_image[0]), len(input_image))
    return len(output_image)

def enhance_again(input_image_set, algorithm, time, width_original, length_original):
    output_image = set()

    for x in range(-time, length_original + 1 + time):
        for y in range(-time, width_original + 1 + time):
            bin_value = ""
            for xd in range(x - 1, x + 2):
                for yd in range(y - 1, y + 2):
                    if -time + 1 <= xd < length_original + time and -time + 1 <= yd < width_original + time:
                        if (xd, yd) in input_image_set:
                            bin_value += str(1)
                        else:
                            bin_value += str(0)
                    elif time % 2 == 0:
                        bin_value += str(algorithm[0])
                    else:
                        bin_value += str(0)
            if algorithm[int(bin_value, 2)] == 1:
                output_image.add((x, y))
    return output_image

def part2(algorithm, input_image):
    """Solve part 2"""


def solve(path):
    """Solve the puzzle for the given input"""
    puzzle_input = pathlib.Path(path).read_text().strip()
    algorithm, input_image = parse(puzzle_input)
    solution1 = part1(algorithm, input_image)

    puzzle_input = pathlib.Path(path).read_text().strip()
    algorithm, input_image = parse(puzzle_input)
    solution2 = part2(algorithm, input_image)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        solutions = solve(path)
        print("\n".join(str(solution) for solution in solutions))
