"""AoC [[day]], [[year]][% if puzzle_name %]: [[puzzle_name]][% endif %]"""

# Standard library imports
import pathlib
import sys
import re


class Display:
    def __init__(self, line):
        parts = line.split(" | ")
        self.all_digits = [self.sort_characters(string) for string in parts[0].split(" ")]
        self.displayed_digits = [self.sort_characters(string) for string in parts[1].split(" ")]
        self.meaning_digits = ["x"] * 10

    def times_simple(self):
        counter = 0
        for digit in self.displayed_digits:
            if len(digit) == 2 or len(digit) == 4 or len(digit) == 3 or len(digit) == 7:
                counter += 1
        return counter

    def get_digits_of_length(self, length):
        result = []
        for digit in self.all_digits:
            if len(digit) == length:
                result.append(digit)
        return result

    def get_actual_reading(self):
        self.fill_meaning_digits()
        result_string = ""
        for digit in self.displayed_digits:
            for i in range(10):
                if digit == self.meaning_digits[i]:
                    result_string += str(i)
        print(self.displayed_digits)
        print(result_string)
        return int(result_string)

    def fill_meaning_digits(self):
        self.meaning_digits[1] = self.get_digits_of_length(2)[0]
        self.meaning_digits[4] = self.get_digits_of_length(4)[0]
        self.meaning_digits[7] = self.get_digits_of_length(3)[0]
        self.meaning_digits[8] = self.get_digits_of_length(7)[0]
        length_6 = self.get_digits_of_length(6)
        for string in length_6:
            if self.check_if_contained(self.meaning_digits[4], string):
                self.meaning_digits[9] = string
        length_6.remove(self.meaning_digits[9])

        for string in length_6:
            if self.check_if_contained(self.meaning_digits[7], string):
                self.meaning_digits[0] = string
        length_6.remove(self.meaning_digits[0])
        self.meaning_digits[6] = length_6[0]

        length_5 = self.get_digits_of_length(5)
        for string in length_5:
            if self.check_if_contained(self.meaning_digits[7], string):
                self.meaning_digits[3] = string
        length_5.remove(self.meaning_digits[3])

        for string in length_5:
            if self.check_if_contained(string, self.meaning_digits[6]):
                self.meaning_digits[5] = string
        length_5.remove(self.meaning_digits[5])
        self.meaning_digits[2] = length_5[0]
        print(self.meaning_digits)

    def check_if_contained(self, small: str, big: str):
        for char in small:
            if char not in big:
                return False
        return True

    def sort_characters(self, string):
        return "".join(sorted(string))


def parse(puzzle_input):
    """Parse input"""
    return [Display(line) for line in puzzle_input.splitlines()]


def parse_line(line):
    regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
    match = re.search(regex, line)

    minimum = int(match.group(1))
    maximum = int(match.group(2))
    letter = match.group(3)
    password = match.group(4)


def part1(data):
    """Solve part 1"""
    counter = 0
    for display in data:
        counter += display.times_simple()
    return counter


def part2(data):
    """Solve part 2"""
    counter = 0
    for display in data:
        counter += display.get_actual_reading()
    return counter


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
