
# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
	"""Parse input"""
	lines = puzzle_input.splitlines()
	path_dict = dict()
	for line in lines:
		places = line.split("-")
		if places[0] in path_dict:
			path_dict[places[0]].add(places[1])
		else:
			path_dict[places[0]] = set()
			path_dict[places[0]].add(places[1])
		if places[1] in path_dict:
			path_dict[places[1]].add(places[0])
		else:
			path_dict[places[1]] = set()
			path_dict[places[1]].add(places[0])
	return path_dict


def part1(data):
	"""Solve part 1"""
	number_paths_traveled = 0

	my_path = ["start"]
	number_paths_traveled = travel_paths(my_path, data)

	return number_paths_traveled

def travel_paths(my_path, data):
	ends_found = 0
	for place in data[my_path[-1]]:
		if (place.islower() and place not in my_path) or place.isupper():
			if place == 'end':
				ends_found += 1
			else:
				new_path = my_path.copy()
				new_path.append(place)
				ends_found += travel_paths(new_path, data)

	return ends_found


def travel_paths2(my_path, data):
	ends_found = 0
	dups = [x for i, x in enumerate(my_path) if x in my_path[:i]]
	has_no_lower_dup = True
	for dup in dups:
		if dup.islower():
			has_no_lower_dup = False
	for place in data[my_path[-1]]:
		if (place.islower() and has_no_lower_dup and place != "start") or (place.islower() and place not in my_path) or place.isupper():
			if place == 'end':
				ends_found += 1
			else:
				new_path = my_path.copy()
				new_path.append(place)
				ends_found += travel_paths2(new_path, data)

	return ends_found

def part2(data):
	number_paths_traveled = 0

	my_path = ["start"]
	number_paths_traveled = travel_paths2(my_path, data)
	return number_paths_traveled


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
