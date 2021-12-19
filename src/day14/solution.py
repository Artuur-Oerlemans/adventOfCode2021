# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
    """Parse input"""
    start = puzzle_input.split("\n\n")[0]
    lines = puzzle_input.split("\n\n")[1].splitlines()
    poly_dict = dict()
    for line in lines:
        elements = line.split(" -> ")
        poly_dict[elements[0]] = elements[1]
    return start, poly_dict


def parse_line(line):
    regex = r"^(\d+)-(\d+) ([a-z]): ([a-z]+)"
    match = re.search(regex, line)

    minimum = int(match.group(1))
    maximum = int(match.group(2))
    letter = match.group(3)
    password = match.group(4)


def part1(state, poly_dict):
    """Solve part 1"""

    for i in range(0, 10):
        state = polymorph(state, poly_dict)

    return count_score(state)


def polymorph(state, poly_dict):
    new_state = state[0]
    for index in range(1, len(state)):
        new_state += poly_dict[state[index - 1] + state[index]] + state[index]
    return new_state

def count_score(state):
    frequency = {i: state.count(i) for i in set(state)}
    maxi = 0
    mini = 99999999999999999

    for letter in set(state):
        if frequency[letter] > maxi:
            maxi = frequency[letter]
        if frequency[letter] < mini:
            mini = frequency[letter]
    return maxi - mini

def part2(state, poly_dict):
    """Solve part 1"""
    first = state[0]
    last = state[-1]

    freq = state_to_freq_dict(state)

    for i in range(0, 1000000):
        freq = polymorph_freq(freq, poly_dict)

    return count_score_freq(freq, first, last)


def count_score_freq(freq, first, last):
    freq_char = dict()
    for key in freq:
        if key[0] in freq_char:
            freq_char[key[0]] += freq[key]
        else:
            freq_char[key[0]] = freq[key]
        if key[1] in freq_char:
            freq_char[key[1]] += freq[key]
        else:
            freq_char[key[1]] = freq[key]

    freq_char[first] += 1
    freq_char[last] += 1
    maxi = 0
    mini = freq_char[first]

    for key in freq_char:
        if freq_char[key] > maxi:
            maxi = freq_char[key]
        if freq_char[key] < mini:
            mini = freq_char[key]
    return (maxi - mini)//2

def polymorph_freq(freq, poly_dict):
    new_freq = dict()

    for key in freq:
        between = poly_dict[key]
        if key[0] + between in new_freq:
            new_freq[key[0] + between] += freq[key]
        else:
            new_freq[key[0] + between] = freq[key]

        if between + key[1] in new_freq:
            new_freq[between + key[1]] += freq[key]
        else:
            new_freq[between + key[1]] = freq[key]
    return new_freq

def state_to_freq_dict(state):
    state_set = set()
    for index in range(1, len(state)):
        state_set.add(state[index - 1] + state[index])
    frequency = {i: state.count(i) for i in state_set}
    return frequency


def solve(path):
    """Solve the puzzle for the given input"""
    puzzle_input = pathlib.Path(path).read_text().strip()
    state, poly_dict = parse(puzzle_input)
    solution1 = part1(state, poly_dict)

    puzzle_input = pathlib.Path(path).read_text().strip()
    state, poly_dict = parse(puzzle_input)
    solution2 = part2(state, poly_dict)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        solutions = solve(path)
        print("\n".join(str(solution) for solution in solutions))
