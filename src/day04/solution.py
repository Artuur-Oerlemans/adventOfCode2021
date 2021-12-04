"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
	"""Parse input"""
	return puzzle_input.split(",")


def parse_cards(cards_input):
	"""Parse input"""
	card_strings = cards_input.split("\n\n")

	return [parse_card(card_input) for card_input in card_strings]

def parse_card(card_input):
	return [parse_rule(rule_input) for rule_input in card_input.splitlines()]

def parse_rule(rule_input):
	regex = r"^( ?\d+) ( ?\d+) ( ?\d+) ( ?\d+) ( ?\d+)$"
	match = re.search(regex, rule_input)
	rules_with_whitespace = [match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)]
	return [characters.strip() for characters in rules_with_whitespace]


def parse_line(line):
	regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
	match = re.search(regex, line)

	minimum = int(match.group(1))
	maximum = int(match.group(2))
	letter = match.group(3)
	password = match.group(4)


def part1(data, cards):
	"""Solve part 1"""

	for number in data:
		update_cards(number, cards)

		check = check_if_winner(cards)

		if check > -1:
			return calc_score(cards[check], number)

	return "-666"

def update_cards(number, cards):
	for card in cards:
		for rule in card:
			for i in range(0, 5):
				if rule[i] == number:
					rule[i] = "x"


def check_if_winner(cards):
	for card_index in range(0, len(cards)):
		if check_card(cards[card_index]):
			return card_index

	return -1

def check_card(card):
	for i in range(0, 5):
		row = ""
		for j in range(0, 5):
			row += card[i][j]
		if row == "xxxxx":
			return True

	for j in range(0, 5):
		row = ""
		for i in range(0, 5):
			row += card[i][j]
		if row == "xxxxx":
			return True
	return False

def calc_score(card, number):
	values = 0
	for j in range(0, 5):
		for i in range(0, 5):
			if card[i][j] != "x":
				values += int(card[i][j])

	return values * int(number)

def part2(data, cards):
	"""Solve part 2"""

	scores = []

	for number in data:
		update_cards(number, cards)

		winners = check_if_winners(cards)

		for winner in winners:
			scores.append(calc_score(cards[winner], number))
			cards[winner] = "x"
			print(scores)

		for i in range(0,len(winners)):
			for j in range(0, len(cards)):
				if cards[j] == "x":
					cards.pop(j)
					break

	return scores[len(scores) - 1]


def check_if_winners(cards):
	winners = []
	for card_index in range(0, len(cards)):
		if check_card(cards[card_index]):
			winners.append(card_index)

	return winners

def solve(puzzle_input, cards):
	"""Solve the puzzle for the given input"""
	data = parse(puzzle_input)
	data_cards = parse_cards(cards)
	solution1 = part1(data, data_cards)
	data = parse(puzzle_input)
	data_cards = parse_cards(cards)
	solution2 = part2(data, data_cards)

	return solution1, solution2


if __name__ == "__main__":
	path = sys.argv[1]
	path2 = sys.argv[2]
	print(f"{path}:")
	solutions = solve(pathlib.Path(path).read_text().strip(), pathlib.Path(path2).read_text().strip())
	print("\n".join(str(solution) for solution in solutions))
