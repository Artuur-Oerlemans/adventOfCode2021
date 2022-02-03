
# Standard library imports
import pathlib
import sys
import re
import math
import functools
import time


def parse(puzzle_input):
	"""Parse input"""
	lines = puzzle_input.splitlines()
	cucumbers = dict()
	for x in range(len(lines)):
		for y in range(len(lines[x])):
			if lines[x][y] != ".":
				cucumbers[(x,y)] = lines[x][y]
	return cucumbers, len(lines), len(lines[0])


def parse_line(line):
	regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
	match = re.search(regex, line)

	minimum = int(match.group(1))
	maximum = int(match.group(2))
	letter = match.group(3)
	password = match.group(4)


def part1(data, x_len, y_len):
	"""Solve part 1"""
	counter = 0
	moved = True
	while moved:
		data, moved = movement(data, x_len, y_len)
		counter += 1
	return counter

def movement(old_cucumbers, x_len, y_len):
	east_move = dict()
	new_cucumbers = dict()
	moved = False

	for coor, direc in old_cucumbers.items():
		if direc == ">" and (coor[0], (coor[1] + 1) % y_len) not in old_cucumbers:
			east_move[(coor[0],( coor[1] + 1) % y_len)] = direc
			moved = True
		else:
			east_move[coor] = direc

	for coor, direc in east_move.items():
		if direc == "v" and ((coor[0] + 1) % x_len, coor[1]) not in east_move:
			new_cucumbers[((coor[0] + 1) % x_len, coor[1])] = direc
			moved = True
		else:
			new_cucumbers[coor] = direc

	return new_cucumbers, moved


def part2(data, x_len, y_len):
	"""Solve part 2"""


def solve(path):
	"""Solve the puzzle for the given input"""

	puzzle_input = pathlib.Path(path).read_text().strip()
	data, x_len, y_len = parse(puzzle_input)
	start_1 = time.time()
	solution1 = part1(data, x_len, y_len)
	end_1 = time.time()
	print("time part 1:", end_1 - start_1)

	puzzle_input = pathlib.Path(path).read_text().strip()
	data, x_len, y_len = parse(puzzle_input)
	start_2 = time.time()
	solution2 = part2(data, x_len, y_len)
	end_2 = time.time()
	print("time part 2:", end_2 - start_2)

	return solution1, solution2


if __name__ == "__main__":
	for path in sys.argv[1:]:
		print(f"{path}:")
		solutions = solve(path)
		print("\n".join(str(solution) for solution in solutions))
