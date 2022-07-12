
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


def parse_line(line):
	regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
	match = re.search(regex, line)

	minimum = int(match.group(1))
	maximum = int(match.group(2))
	letter = match.group(3)
	password = match.group(4)


def part1(data):
	"""Solve part 1"""
	suma = 0
	for i in range(0, 1000):
		if i % 3 == 0 or i % 5 == 0:
			suma += i
	return suma


def part2(data):
	"""Solve part 2"""


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
