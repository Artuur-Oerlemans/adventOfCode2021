"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
	"""Parse input"""
	return [[int(i) for i in line] for line in puzzle_input.splitlines()]


def parse_line(line):
	regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
	match = re.search(regex, line)

	minimum = int(match.group(1))
	maximum = int(match.group(2))
	letter = match.group(3)
	password = match.group(4)


def part1(data):
	"""Solve part 1"""
	x_max = len(data)
	y_max = len(data[0])

	flashes = 0
	for i in range(0, 100):
		increase_by_one(data, x_max, y_max)
		flashes += wave(data, x_max, y_max)

	return flashes

def increase_by_one(data, x_max, y_max):
	for x in range(0, x_max):
		for y in range(0, y_max):
			data[x][y] += 1

def wave(data, x_max, y_max):
	need_to_shine = set()
	shined = set()

	for x in range(0, x_max):
		for y in range(0, y_max):
			if data[x][y] > 9:
				need_to_shine.add((x,y))

	while len(need_to_shine) != 0:
		point = need_to_shine.pop()
		shined.add(point)

		for xd in range(max(0,point[0] -1), min(x_max, point[0] + 2)):
			for yd in range(max(0, point[1] - 1), min(y_max, point[1] + 2)):
				if (xd, yd) != point:
					data[xd][yd] += 1
					if data[xd][yd] > 9 and (xd, yd) not in need_to_shine and (xd, yd) not in shined:
						need_to_shine.add((xd, yd))

	for x in range(0, x_max):
		for y in range(0, y_max):
			if data[x][y] > 9:
				data[x][y] = 0
	return len(shined)

def part2(data):
	"""Solve part 1"""
	x_max = len(data)
	y_max = len(data[0])

	for i in range(1, 1000):
		increase_by_one(data, x_max, y_max)
		flashes = wave(data, x_max, y_max)
		print(i)
		print(data)
		if flashes == 100:
			return i



def solve(puzzle_input):
	"""Solve the puzzle for the given input"""
	puzzle_input = pathlib.Path(path).read_text().strip()
	data = parse(puzzle_input)
	solution1 = part1(data)
	# I completed part 1 quite sometime before my friends, but got stuck for 21 minutes on F***ING REUSING CODE
	puzzle_input = pathlib.Path(path).read_text().strip()
	data = parse(puzzle_input)
	solution2 = part2(data)

	return solution1, solution2


if __name__ == "__main__":
	for path in sys.argv[1:]:
		print(f"{path}:")
		solutions = solve(path)
		print("\n".join(str(solution) for solution in solutions))
