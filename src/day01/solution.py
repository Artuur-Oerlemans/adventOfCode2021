"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
	"""Parse input"""
	lines = puzzle_input.splitlines()
	return [int(s) for s in lines]


def parse_line(line):
	regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
	match = re.search(regex, line)

	minimum = int(match.group(1))
	maximum = int(match.group(2))
	letter = match.group(3)
	password = match.group(4)


def part1(data):
	"""Solve part 1"""
	increases = 0
	for i in range(1, len(data)):
		if data[i-1] < data[i]:
			increases += 1

	return increases


def part2(data):
	"""Solve part 2"""
	increases = 0
	for i in range(3, len(data)):
		if data[i - 3] < data[i]:
			increases += 1

	return increases


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
