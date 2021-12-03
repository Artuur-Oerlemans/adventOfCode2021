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
	width = len(data[0])

	gamma = ""
	epsilon = ""

	for i in range(0, width):
		number1 = 0
		for line in data:
			if line[i] == '1':
				number1 += 1
		if number1 > len(data) - number1:
			gamma += "1"
			epsilon += "0"
		else:
			gamma += "0"
			epsilon += "1"
	return int(gamma, 2) * int(epsilon, 2)

def oxygen_eliminator(lines, place):
	number1 = 0
	result = list()
	for line in lines:
		if line[place] == '1':
			number1 += 1

	for line in lines:
		if number1 >= len(lines) - number1 and line[place] == '1':
			result.append(line)
		elif number1 < len(lines) - number1 and line[place] == '0':
			result.append(line)
	return result


def co2_eliminator(lines, place):
	number1 = 0
	result = list()
	for line in lines:
		if line[place] == '1':
			number1 += 1

	for line in lines:
		if number1 < len(lines) - number1 and line[place] == '1':
			result.append(line)
		elif number1 >= len(lines) - number1 and line[place] == '0':
			result.append(line)
	return result


def part2(data):
	"""Solve part 2"""
	width = len(data[0])


	oxygen_lines = data
	while len(oxygen_lines) > 1:
		for place in range(0, width):
			oxygen_lines = oxygen_eliminator(oxygen_lines, place)

	co2_lines = data
	while len(co2_lines) > 1:
		for place in range(0, width):
			if len(co2_lines) > 1:
				co2_lines = co2_eliminator(co2_lines, place)

	oxygen = oxygen_lines[0]
	co2 = co2_lines[0]

	return int(oxygen, 2) * int(co2, 2)


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
