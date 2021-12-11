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
	score = 0
	for line in data:
		score += calc_score_line(line)
	return score

def calc_score_line(line):
	stack = []
	for char in line:
		if char in {"(", "{", "[", "<"}:
			stack.append(char)
		else:
			top = stack[- 1]

			if (top == "(" and char != ")") or (top == "[" and char != "]") or (top == "{" and char != "}") or (
					top == "<" and char != ">"):
				return calc_score_char(char)
			else:
				stack.pop()
	return 0

def calc_score_char(char):
	if char == ")":
		return 3
	if char == "]":
		return 57
	if char == "}":
		return 1197
	if char == ">":
		return 25137



def part2(data):
	"""Solve part 2"""
	scores = []
	for line in data:
		needed_chars = autocomplete(line)
		score = calc_score_closing_stack(needed_chars)
		if score != 0:
			scores.append(score)
	scores.sort()
	return scores[int(len(scores)/2)]

def autocomplete(line):
	stack = []
	for char in line:
		if char in {"(", "{", "[", "<"}:
			stack.append(char)
		else:
			top = stack[- 1]

			if (top == "(" and char != ")") or (top == "[" and char != "]") or (top == "{" and char != "}") or (
					top == "<" and char != ">"):
				return []
			else:
				stack.pop()
	return stack

def calc_score_closing_stack(stack):
	score = 0
	print(stack)
	while len(stack) != 0:
		top = stack.pop()
		score *= 5
		score += calc_score_closing_char(top)
		print(score)
	return score


def calc_score_closing_char(char):
	if char == "(":
		return 1
	if char == "[":
		return 2
	if char == "{":
		return 3
	if char == "<":
		return 4
	print("fuck")

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
