# Standard library imports
import pathlib
import sys
import re
import math
import functools
import time


def parse(puzzle_input):
    """Parse input"""
    places = dict()
    lines = puzzle_input.splitlines()
    for x in range(len(lines)):
        for y in range(len(lines[x])):
            if lines[x][y] not in ["#", " "]:
                places[(x, y)] = lines[x][y]
    for i in range(0, 4):
        del places[(1, 3 + i * 2)]
    return places


def part1(data):
    """Solve part 1"""

    return make_move(data, 0, 9999999999, dict())

def make_move(places, fuel_spent, lowest_fuel_cost, moves_made):
    if fuel_spent >= lowest_fuel_cost:
        return lowest_fuel_cost
    string_dict = str(places)
    if string_dict in moves_made:
        if moves_made[string_dict] <= fuel_spent:
            return lowest_fuel_cost
    moves_made[string_dict] = fuel_spent

    no_move_made = True
    for pos, color in places.items():
        if color != '.':
            possible_moves = can_move_to(places, pos)
            move_cost = calc_fuel_cost(possible_moves, pos, color)
            for move, cost in sorted(move_cost.items(), key=lambda item: item[1]):
                places_copy = places.copy()

                places_copy[pos] = '.'
                places_copy[move] = color

                lowest_fuel_cost = min(make_move(places_copy, fuel_spent + cost, lowest_fuel_cost, moves_made), lowest_fuel_cost)
                no_move_made = False

    if no_move_made:
        for pos, color in places.items():
            if pos[0] == 1 and color != '.':
                return lowest_fuel_cost
        return fuel_spent
    return lowest_fuel_cost

def calc_fuel_cost(possible_moves, pos, color):
    move_cost = dict()
    cost_per_color = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    multiplier = cost_per_color[color]
    for move in possible_moves:
        cost = 0
        cost += move[0] - 1
        cost += pos[0] - 1
        cost += abs(move[1] - pos[1])
        move_cost[move] = cost * multiplier
    return move_cost

def can_move_from_room(places, amphipod):
    for x in range(2, amphipod[0]):
        if places[(x, amphipod[1])] != '.':
            return False
    return True

def can_move_to(places, amphipod):
    possible_moves = set()

    if in_final_position(places, amphipod):
        return possible_moves
    elif amphipod[0] > 2:
        if not can_move_from_room(places, amphipod):
            return possible_moves

    if amphipod[0] != 1:
        block_right = False
        width = amphipod[1] + 1
        while not block_right and width <= 11:
            if width not in [3, 5, 7, 9]:
                if places[(1, width)] == '.':
                    possible_moves.add((1, width))
                else:
                    block_right = True
            width += 1

        block_left = False
        width = amphipod[1] - 1
        while not block_left and width > 0:
            if width not in [3, 5, 7, 9]:
                if places[(1, width)] == '.':
                    possible_moves.add((1, width))
                else:
                    block_left = True
            width -= 1

    list_final_pos = possible_final_position(places, places[amphipod])
    if len(list_final_pos) > 0:
        final_pos = list_final_pos[0]
        direction = sign(final_pos[1] - amphipod[1])
        width = amphipod[1] + direction
        not_blocked = True
        while final_pos[1] != width and not_blocked:
            if width not in [3, 5, 7, 9]:
                not_blocked = places[(1, width)] == '.'
            width += direction
        if not_blocked:
            possible_moves = set()
            possible_moves.add(final_pos)

    return possible_moves


def sign(x):
    return int(math.copysign(1, x))

def possible_final_position(places, color):
    possible_move = list()
    color_to_column = {'A': 3, 'B': 5, 'C': 7, 'D': 9}

    column = color_to_column[color]

    depth = 5
    while depth > 1:
        if (depth, column) in places:
            if places[(depth, column)] == '.':
                possible_move.append((depth, column))
                return possible_move
            elif places[(depth, column)] != color:
                return possible_move
        depth -= 1
    return possible_move


def in_final_position(places, amphipod):
    color = places[amphipod]
    color_to_column = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
    if color_to_column[color] != amphipod[1]:
        return False

    for x in range(amphipod[0] + 1, 6):
        if (x, amphipod[1]) in places and places[(x, amphipod[1])] != color:
            return False
    return True


def solve(path):
    """Solve the puzzle for the given input"""

    puzzle_input = pathlib.Path(path).read_text().strip()
    data = parse(puzzle_input)
    start_1 = time.time()
    solution1 = part1(data)
    end_1 = time.time()
    print("time part 1:", end_1 - start_1)

    return solution1


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        solutions = solve(path)
        print("\n".join(str(solution) for solution in solutions))
