"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re
from itertools import repeat
import math


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
	highest = find_highest(data)
	the_array = create_2d_array(highest)

	# add some point I started accidentally using the first value of a input coordinate as y and the second as x
	for line in data:
		regex = r"^(\d+),(\d+) -> (\d+),(\d+)"
		match = re.search(regex, line)
		print(highest)
		print(line)
		if int(match.group(1)) == int(match.group(3)):
			if int(match.group(2)) < int(match.group(4)) + 1:
				for x in range(int(match.group(2)), int(match.group(4)) + 1):
					the_array[x][int(match.group(1))] += 1
			else:
				for x in range(int(match.group(4)), int(match.group(2)) + 1):
					the_array[x][int(match.group(1))] += 1

		if int(match.group(2)) == int(match.group(4)):
			if int(match.group(1)) < int(match.group(3)) + 1:
				for y in range(int(match.group(1)), int(match.group(3)) + 1):
					the_array[int(match.group(2))][y] += 1
			else:
				for y in range(int(match.group(3)), int(match.group(1)) + 1):
					the_array[int(match.group(2))][y] += 1


	result = 0
	for x in the_array:
		for xy in x:
			if xy > 1:
				result += 1

	return result

def find_highest(data):
	max_width = 0
	for line in data:
		regex = r"^(\d+),(\d+) -> (\d+),(\d+)"
		match = re.search(regex, line)

		for i in range(1, 5):
			if int(match.group(i)) > max_width:
				max_width = int(match.group(i))
	return max_width

def create_2d_array(max_width):
	the_array = []

	for i in range(0, max_width+1):
		the_array.append(list(repeat(0, max_width+1)))


	return the_array

def part2(data):
	"""Solve part 2"""
	highest = find_highest(data)
	the_array = create_2d_array(highest)

	# add some point I started accidentally using the first value of a input coordinate as y and the second as x
	for line in data:
		regex = r"^(\d+),(\d+) -> (\d+),(\d+)"
		match = re.search(regex, line)
		print(highest)
		print(line)
		if int(match.group(1)) == int(match.group(3)):
			if int(match.group(2)) < int(match.group(4)) + 1:
				for x in range(int(match.group(2)), int(match.group(4)) + 1):
					the_array[x][int(match.group(1))] += 1
			else:
				for x in range(int(match.group(4)), int(match.group(2)) + 1):
					the_array[x][int(match.group(1))] += 1
		elif int(match.group(2)) == int(match.group(4)):
			if int(match.group(1)) < int(match.group(3)) + 1:
				for y in range(int(match.group(1)), int(match.group(3)) + 1):
					the_array[int(match.group(2))][y] += 1
			else:
				for y in range(int(match.group(3)), int(match.group(1)) + 1):
					the_array[int(match.group(2))][y] += 1
		elif abs(int(match.group(3)) - int(match.group(1))) - abs(int(match.group(4)) - int(match.group(2))) == 0:
			x_sign = int(math.copysign(1,  int(match.group(3)) - int(match.group(1))))
			y_sign = int(math.copysign(1, int(match.group(4)) - int(match.group(2))))
			for i in range(0, abs(int(match.group(3)) - int(match.group(1))) + 1):
				the_array[int(match.group(2)) + y_sign * i][int(match.group(1)) + x_sign * i] += 1


	result = 0
	for x in the_array:
		for xy in x:
			if xy > 1:
				result += 1

	return result


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
