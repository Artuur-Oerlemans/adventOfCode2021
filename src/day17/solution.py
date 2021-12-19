
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
	max_y = -500

	for xd in range(1, 264):
		for yd in range(-79, 200):
			cur_xd = xd
			cur_yd = yd
			x_pos = 0
			y_pos = 0
			cur_max_y = 0
			target_hit = False

			while x_pos <= 262 and y_pos >= -78 and (xd != 0 or x_pos >= 236) and not target_hit:
				x_pos += cur_xd
				y_pos += cur_yd
				if y_pos > cur_max_y:
					cur_max_y = y_pos

				if cur_xd > 0:
					cur_xd -= 1
				cur_yd -= 1

				if 236 <= x_pos <= 262 and -78 <= y_pos <= -58:
					target_hit = True
					if cur_max_y > max_y:
						max_y = cur_max_y


	return max_y


def part2(data):
	"""Solve part 2"""
	max_y = -500
	times = 0

	for xd in range(1, 264):
		for yd in range(-79, 200):
			cur_xd = xd
			cur_yd = yd
			x_pos = 0
			y_pos = 0
			cur_max_y = 0
			target_hit = False

			while x_pos <= 262 and y_pos >= -78 and (xd != 0 or x_pos >= 236) and not target_hit:
				x_pos += cur_xd
				y_pos += cur_yd
				if y_pos > cur_max_y:
					cur_max_y = y_pos

				if cur_xd > 0:
					cur_xd -= 1
				cur_yd -= 1

				if 236 <= x_pos <= 262 and -78 <= y_pos <= -58:
					target_hit = True
					if cur_max_y > max_y:
						max_y = cur_max_y
					times += 1

	return times


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
