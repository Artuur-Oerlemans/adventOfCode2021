# Standard library imports
import pathlib
import sys
import re
import math
import functools
import time
from itertools import product


def parse(puzzle_input):
    """Parse input"""
    return [parse_line(line) for line in puzzle_input.splitlines()]


def parse_line(line):
    regex = r"^(.{2,3}) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)"
    match = re.search(regex, line)

    is_on = match.group(1) == "on"
    x_pos = (int(match.group(2)), int(match.group(3)))
    y_pos = (int(match.group(4)), int(match.group(5)))
    z_pos = (int(match.group(6)), int(match.group(7)))
    return Cuboid(is_on, x_pos, y_pos, z_pos)


def part1(data):
    """Solve part 1"""
    all_cuboids = set()

    for intersector in data[:20]:
        new_all_cuboid = set()
        for cuboid in all_cuboids:
            new_all_cuboid.update(cuboid.intersect(intersector))
        if intersector.is_on:
            new_all_cuboid.add(intersector)
        all_cuboids = new_all_cuboid

    cubes_on = 0

    for cuboid in all_cuboids:
        cubes_on += cuboid.area()

    return cubes_on


class Cuboid:

    def __init__(self, is_on, x_pos, y_pos, z_pos):
        self.is_on = is_on
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

    def intersect(self, intersector):
        remainder = set()
        if contained(self.x_pos, intersector.x_pos) and contained(self.y_pos, intersector.y_pos) and contained(
                self.z_pos, intersector.z_pos):
            return set()
        elif overlap(self.x_pos, intersector.x_pos) and overlap(self.y_pos, intersector.y_pos) and overlap(self.z_pos,
                                                                                                           intersector.z_pos):
            if self.is_on:
                remainder.add(self)
                intersection = Cuboid(False,
                                      inter_coor(self.x_pos, intersector.x_pos),
                                      inter_coor(self.y_pos, intersector.y_pos),
                                      inter_coor(self.z_pos, intersector.z_pos))
                remainder.add(intersection)
            else:
                remainder.add(self)
                intersection = Cuboid(True,
                                      inter_coor(self.x_pos, intersector.x_pos),
                                      inter_coor(self.y_pos, intersector.y_pos),
                                      inter_coor(self.z_pos, intersector.z_pos))
                remainder.add(intersection)
        else:
            remainder.add(self)
        return remainder

    def area(self):
        if self.is_on:
            sign = 1
        else:
            sign = -1
        return sign * segments_in(self.x_pos) * segments_in(self.y_pos) * segments_in(self.z_pos)

def segments_in(pos):
    return pos[1] - pos[0] + 1

def inter_coor(pos_1, pos_2):
    return max(pos_1[0], pos_2[0]), min(pos_1[1], pos_2[1])


def overlap(pos_1, pos_2):
    return pos_2[0] <= pos_1[1] and pos_1[0] <= pos_2[1]


# 1 being contained by 2
def contained(pos_1, pos_2):
    return pos_2[0] <= pos_1[0] and pos_1[1] <= pos_2[1]


def part2(data):
    """Solve part 2"""
    all_cuboids = set()

    for intersector in data:
        new_all_cuboid = set()
        for cuboid in all_cuboids:
            new_all_cuboid.update(cuboid.intersect(intersector))
        if intersector.is_on:
            new_all_cuboid.add(intersector)
        all_cuboids = new_all_cuboid

    cubes_on = 0

    for cuboid in all_cuboids:
        cubes_on += cuboid.area()

    return cubes_on


def solve(path):
    """Solve the puzzle for the given input"""

    puzzle_input = pathlib.Path(path).read_text().strip()
    data = parse(puzzle_input)
    start_1 = time.time()
    solution1 = part1(data)
    end_1 = time.time()
    print("time part 1:", end_1 - start_1)

    puzzle_input = pathlib.Path(path).read_text().strip()
    data = parse(puzzle_input)
    start_2 = time.time()
    solution2 = part2(data)
    end_2 = time.time()
    print("time part 2:", end_2 - start_2)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        solutions = solve(path)
        print("\n".join(str(solution) for solution in solutions))
