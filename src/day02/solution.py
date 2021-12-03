"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re


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
	regex = r"(\d+)$"
	horizontal = 0
	depth = 0
	aim = 0
	for line in data:
		match = re.search(regex, line)
		if line.startswith("forward"):
			horizontal += int(match.group(1))
		elif line.startswith("up"):
			depth -= int(match.group(1))
		elif line.startswith("down"):
			depth += int(match.group(1))

	return horizontal * depth


def part2(data):
	"""Solve part 2"""
	regex = r"(\d+)$"
	horizontal = 0
	depth = 0
	aim = 0
	for line in data:
		match = re.search(regex, line)
		if line.startswith("forward"):
			horizontal += int(match.group(1))
			depth += aim * int(match.group(1))
		elif line.startswith("up"):
			aim -= int(match.group(1))
		elif line.startswith("down"):
			aim += int(match.group(1))

	return horizontal * depth


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
