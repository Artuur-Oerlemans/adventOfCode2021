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
    return [[parse_line(line) for line in block.splitlines()] for block in puzzle_input.split("inp w\n")][1:]


def parse_line(line):
    values = line.split(" ")
    operation = values[0]
    return operation, values[1:]


def part1(data):
    """Solve part 1"""
    failed_attempts = [set(), set(), set(), set(), set(), set(), set(), set(), set(), set(), set(), set(), set(), set()]
    result = "-1"
    for w in range(1, 10):
        result = do_operations_on(w, 0, 0, 0, data, failed_attempts)
        if result != "-1":
            return result
        print("loop")

    # memory = [SpotValue("val", "w0", ""), SpotValue("val", 0, ""), SpotValue("val", 0, ""), SpotValue("val", 0, "")]
    # for i in range(len(data[:4])):
    #     memory[0] = SpotValue("val", "w" + str(i), "")
    #     for operator, values in data[i]:
    #         print(operator, values)
    #         pos = convert_to_mem(values[0])
    #         first = memory[pos]
    #         second = get_value(values[1], memory)
    #         memory[pos] = SpotValue(operator, first, second)
    #         memory[pos] = memory[pos].simplify()
    #         print_memory(memory)

    return result


def print_memory(memory):
    print("w=", memory[0].to_string(), ", x=", memory[1].to_string(), ", y=", memory[2].to_string(), ", z=",
          memory[3].to_string())


class SpotValue:

    def __init__(self, ope, first, second):
        self.ope = ope
        self.first = first
        self.second = second

    def to_string(self):
        if isinstance(self.first, SpotValue):
            s1 = self.first.to_string()
        else:
            s1 = str(self.first)
        if isinstance(self.second, SpotValue):
            s2 = self.second.to_string()
        else:
            s2 = str(self.second)

        if self.ope == "val":
            return s1
        elif self.ope == "add":
            return "(" + s1 + "+" + s2 + ")"
        elif self.ope == "mul":
            return s1 + "*" + s2
        elif self.ope == "div":
            return s1 + "//" + s2
        elif self.ope == "eql":
            return s1 + "==" + s2
        elif self.ope == "mod":
            return "(" + s1 + ")%" + s2

    def contains_multiply(self):
        print(self.to_string())
        if self.ope == "val":
            return False
        if self.ope == "mul":
            return True
        if self.ope == "add":
            return self.first.contains_multiply() or self.second.contains_multiply()
        print("no contains_multiply", self.to_string())

    def simplify(self):
        if self.ope == "mul":
            if self.second.ope == "val":
                if self.second.first == 0:
                    return SpotValue("val", 0, "")
                elif self.second.first == 1:
                    return self.first
            if self.first.ope == "val":
                if self.first.first == 0:
                    return SpotValue("val", 0, "")
                elif self.first.first == 1:
                    return self.second
        elif self.ope == "add":
            if self.first.ope == "val" and self.first.first == 0:
                return self.second
            if self.second.ope == "val" and self.second.first == 0:
                return self.first
            if self.first.ope == "val" and self.second.ope == "val" and not isinstance(self.first.first,
                                                                                       str) and not isinstance(
                    self.second.first, str):
                return SpotValue("val", self.first.first + self.second.first, "")
        elif self.ope == "mod" and self.second.ope == "val" and not isinstance(self.second.first, str):
            modulo = self.second.first
            # if self.first.ope == "mul" and self.first.second.ope == "val" and self.first.second.first == modulo:
            #     return SpotValue("val", 0, "")
            if self.first.contains_multiply():
                self.first = self.first.recursive_mod(modulo).simplify()
            if not self.first.contains_multiply():
                range_start, range_end = self.first.range()
                if range_end < modulo and 0 <= range_start:
                    return self.first
                elif range_start == range_end:
                    return SpotValue("val", range_end % modulo, "")
        elif self.ope == "div":
            if self.second.ope == "val" and self.second.first == 1:
                return self.first
        elif self.ope == "eql":
            range1_start, range1_end = self.first.range()
            range2_start, range2_end = self.second.range()
            if range1_end < range2_start or range2_end < range1_start:
                return SpotValue("val", 0, "")
            elif range1_start == range1_end and range1_end == range2_start and range2_start == range2_end:
                return SpotValue("val", 1, "")
        return self

    def range(self):
        if self.ope == "val":
            if isinstance(self.first, str):
                return 1, 9
            else:
                return self.first, self.first
        elif self.ope == "add":
            range1_start, range1_end = self.first.range()
            range2_start, range2_end = self.second.range()
            return range1_start + range2_start, range1_end + range2_end
        print("no range", self.to_string())

    def recursive_mod(self, modulo):
        if self.ope == "add":
            self.first = self.first.recursive_mod(modulo)
            self.second = self.second.recursive_mod(modulo)
        elif self.ope == "mul" and self.second.ope == "val" and self.second.first == modulo:
            return SpotValue("val", 0, "")
        item = self.simplify()
        return item

    def copy(self):
        if self.ope == "val":
            return SpotValue("val", self.first, self.second)
        else:
            return SpotValue(self.ope, self.first.copy(), self.second.copy())


def do_operations_on(w, x, y, z, blocks, failed_attempts):
    if len(blocks) == 0:
        if z == 0:
            return ""
        else:
            return "-1"
    key = (w, x, y, z)
    if key in failed_attempts[len(blocks) - 1]:
        return "-1"
    failed_attempts[len(blocks) - 1].add(key)
    block = blocks[0]
    memory = [w, x, y, z]
    for operation, values in block:
        pos = convert_to_mem(values[0])
        second = get_value_on(values[1], memory)

        if operation == "add":
            memory[pos] += second
        elif operation == "mul":
            memory[pos] *= second
        elif operation == "div":
            memory[pos] = memory[pos] // second
        elif operation == "mod":
            memory[pos] = memory[pos] % second
        elif operation == "eql":
            if second == memory[pos]:
                memory[pos] = 1
            else:
                memory[pos] = 0
        else:
            print("not working")
    result = "-1"
    for w2 in range(1, 10):
        # result = do_operations_on(w2, memory[1], memory[2], memory[3], blocks[1:], failed_attempts)
        result = do_operations_on(w2, 0, 0, memory[3], blocks[1:], failed_attempts)
        if len(blocks) > 11:
            print(len(blocks), len(failed_attempts[13]), len(failed_attempts[12]), len(failed_attempts[11]),
                  len(failed_attempts[0]))
        if result != "-1":
            print("succes")
            return str(w) + result
    return result


def get_value(char, memory):
    if char in ["w", "x", "y", "z"]:
        return memory[convert_to_mem(char)].copy()
    return SpotValue("val", int(char), "")


def get_value_on(char, memory):
    if char in ["w", "x", "y", "z"]:
        return memory[convert_to_mem(char)]
    return int(char)


def convert_to_mem(char):
    if char == "w":
        return 0
    if char == "x":
        return 1
    if char == "y":
        return 2
    if char == "z":
        return 3


def part2(data):
    """Solve part 2"""


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
