
# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
	"""Parse input"""
	datas = puzzle_input.split("\n\n")
	points = set()
	for point in datas[0].splitlines():
		point_coor = point.split(",")
		points.add((int(point_coor[0]), int(point_coor[1])))
	return points, datas[1].splitlines()


def parse_line(line):
	regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
	match = re.search(regex, line)

	minimum = int(match.group(1))
	maximum = int(match.group(2))
	letter = match.group(3)
	password = match.group(4)


def part1(points, folds):
	"""Solve part 1"""
	regex = r"^fold along ([a-z])=(\d+)$"
	match = re.search(regex, folds[0])

	direction = match.group(1)
	coor = int(match.group(2))

	new_points = set()
	if direction == "x":
		for point in points:
			if point[0] > coor:
				new_points.add((2 * coor - point[0], point[1]))
			else:
				new_points.add(point)
	else:
		for point in points:
			if point[1] > coor:
				new_points.add((point[0], 2 * coor - point[1]))
			else:
				new_points.add(point)


	return len(new_points)


def part2(points, folds):
	"""Solve part 2"""
	for fold in folds:
		points = fold_points(points, fold)

	for y in range(0, 65):
		line = ""
		for x in range(0, 200):
			if (x, y) in points:
				line += "#"
			else:
				line += "."
		print(line)


def fold_points(points, fold):
	regex = r"^fold along ([a-z])=(\d+)$"
	match = re.search(regex, fold)

	direction = match.group(1)
	coor = int(match.group(2))

	new_points = set()
	if direction == "x":
		for point in points:
			if point[0] > coor:
				new_points.add((2 * coor - point[0], point[1]))
			else:
				new_points.add(point)
	else:
		for point in points:
			if point[1] > coor:
				new_points.add((point[0], 2 * coor - point[1]))
			else:
				new_points.add(point)
	return new_points

def solve(path):
	"""Solve the puzzle for the given input"""
	puzzle_input = pathlib.Path(path).read_text().strip()
	points, folds = parse(puzzle_input)
	solution1 = part1(points, folds)

	puzzle_input = pathlib.Path(path).read_text().strip()
	points, folds = parse(puzzle_input)
	solution2 = part2(points, folds)

	return solution1, solution2


if __name__ == "__main__":
	for path in sys.argv[1:]:
		print(f"{path}:")
		solutions = solve(path)
		print("\n".join(str(solution) for solution in solutions))
