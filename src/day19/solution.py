# Standard library imports
import pathlib
import sys
import re
import math
import numpy as np
from numpy.linalg import matrix_power


def parse(puzzle_input):
    """Parse input"""
    return [[parse_line(line) for line in section.splitlines()[1:]] for section in puzzle_input.split("\n\n")]


def parse_line(line):
    return np.array([int(i) for i in line.split(",")])


def rotate_vector_in_all_directions(vector):
    all_directions = dict()
    for xy in range(0, 4):
        for zx in range(0, 2):
            for zxy in range(0, 3):
                all_directions[(xy, zx, zxy)] = rotate_vector(vector, xy, zx, zxy)
    return all_directions


# each direction at most  4   2   3
def rotate_vector(vector, xy, zx, zxy):
    xy_mat = np.array([[0, 1, 0],
                       [-1, 0, 0],
                       [0, 0, 1]])
    zx_mat = np.array([[-1, 0, 0],
                       [0, 1, 0],
                       [0, 0, -1]])
    zxy_mat = np.array([[0, 1, 0],
                        [0, 0, 1],
                        [1, 0, 0]])

    return np.matmul(np.matmul(matrix_power(zxy_mat, zxy), matrix_power(zx_mat, zx)),
                     matrix_power(xy_mat, xy)).dot(vector)


def invert_rotate_vector(vector, xy, zx, zxy):
    xy_mat = np.array([[0, -1, 0],
                       [1, 0, 0],
                       [0, 0, 1]])
    zx_mat = np.array([[-1, 0, 0],
                       [0, 1, 0],
                       [0, 0, -1]])
    zxy_mat = np.array([[0, 0, 1],
                        [1, 0, 0],
                        [0, 1, 0]])

    return np.matmul(np.matmul(matrix_power(xy_mat, xy), matrix_power(zx_mat, zx)),
                     matrix_power(zxy_mat, zxy)).dot(vector)


def part1(data):
    """Solve part 1"""

    vector = np.array([1, 2, 3])
    for xy in range(0, 4):
        for zx in range(0, 2):
            for zxy in range(0, 3):
                new_vector = invert_rotate_vector(rotate_vector(vector, xy, zx, zxy), xy, zx, zxy)
                print(xy, zx, zxy, new_vector)

    differences_per_scanner_per_orientation = calc_differences_per_scanner_per_orientation(data)

    scanner_to_scanner = dict()
    scanner_to_scanner_inverse = dict()

    for scanner in range(0, len(data)):
        for other_scanner in range(scanner + 1, len(data)):
            scanner_set = differences_per_scanner_per_orientation[scanner][(0, 0, 0)]
            for key in differences_per_scanner_per_orientation[other_scanner].keys():
                other_scanner_set = differences_per_scanner_per_orientation[other_scanner][key]
                number_of_differences = len(scanner_set.intersection(other_scanner_set))
                if number_of_differences >= 132:
                    print(scanner, other_scanner, key, number_of_differences)
                    if scanner not in scanner_to_scanner:
                        connections = list()
                        connections.append((other_scanner, key))
                        scanner_to_scanner[scanner] = connections
                    else:
                        scanner_to_scanner[scanner].append((other_scanner, key))

                    if other_scanner not in scanner_to_scanner_inverse:
                        connections = list()
                        connections.append((scanner, key))
                        scanner_to_scanner_inverse[other_scanner] = connections
                    else:
                        scanner_to_scanner_inverse[other_scanner].append((scanner, key))

    indexed_scanners = set()
    indexed_scanners.add(0)

    beacons, scanners = index_connected_scanners(0, indexed_scanners, scanner_to_scanner, scanner_to_scanner_inverse, data)
    print("part 1:", len(beacons))

    max_distance = 0
    for scanner in scanners:
        for scanner1 in scanners:
            distance = abs(scanner[0] - scanner1[0]) + abs(scanner[1] - scanner1[1]) + abs(scanner[2] - scanner1[2])
            if distance > max_distance:
                max_distance = distance
                # print(max_distance, scanner, scanner1)
    print("part 2:", max_distance)
    return 0


def index_connected_scanners(scanner, indexed_scanners, scanner_to_scanner,
                             scanner_to_scanner_inverse, data):
    beacons = set()
    scanners = set()

    for beacon in data[scanner]:
        beacons.add(tuple(beacon))
    scanners.add((0, 0, 0))

    if scanner in scanner_to_scanner:
        for other_scanner, rotate in scanner_to_scanner[scanner]:
            if other_scanner not in indexed_scanners:
                print(scanner, other_scanner)
                indexed_scanners.add(other_scanner)

                normalized_rotation = [rotate_vector(beacon, rotate[0], rotate[1], rotate[2]) for beacon in
                                       data[other_scanner]]
                difference = find_difference(data[scanner], normalized_rotation)

                moved_rotated_tuple_beacons, moved_rotated_tuple_scanners = index_connected_scanners(other_scanner,
                                                                                                     indexed_scanners,
                                                                                                     scanner_to_scanner,
                                                                                                     scanner_to_scanner_inverse,
                                                                                                     data)
                other_beacons = normalize_other_points(moved_rotated_tuple_beacons, rotate, difference, False)
                other_scanners = normalize_other_points(moved_rotated_tuple_scanners, rotate, difference, False)

                for beacon in other_beacons:
                    beacons.add(tuple(beacon))
                for other_scanner_in_list in other_scanners:
                    scanners.add(tuple(other_scanner_in_list))
                print(len(data[scanner]), len(other_beacons), len(beacons))

    if scanner in scanner_to_scanner_inverse:
        for other_scanner, rotate in scanner_to_scanner_inverse[scanner]:
            if other_scanner not in indexed_scanners:
                print(scanner, other_scanner)
                indexed_scanners.add(other_scanner)

                normalized_rotation = [invert_rotate_vector(beacon, rotate[0], rotate[1], rotate[2]) for beacon in
                                       data[other_scanner]]
                difference = find_difference(data[scanner], normalized_rotation)

                moved_rotated_tuple_beacons, moved_rotated_tuple_scanners = index_connected_scanners(other_scanner,
                                                                                                     indexed_scanners,
                                                                                                     scanner_to_scanner,
                                                                                                     scanner_to_scanner_inverse,
                                                                                                     data)

                other_beacons = normalize_other_points(moved_rotated_tuple_beacons, rotate, difference, True)
                other_scanners = normalize_other_points(moved_rotated_tuple_scanners, rotate, difference, True)

                for beacon in other_beacons:
                    beacons.add(tuple(beacon))
                for other_scanner_in_list in other_scanners:
                    scanners.add(tuple(other_scanner_in_list))
                print(len(data[scanner]), len(other_beacons), len(beacons))
    return beacons, scanners


def normalize_other_points(moved_rotated_tuple_points, rotate, difference, inverted):
    moved_rotated_points = [np.array(tuple_beacon) for tuple_beacon in moved_rotated_tuple_points]

    if inverted:
        moved_points = [invert_rotate_vector(beacon, rotate[0], rotate[1], rotate[2]) for beacon in
                        moved_rotated_points]
    else:
        moved_points = [rotate_vector(beacon, rotate[0], rotate[1], rotate[2]) for beacon in
                        moved_rotated_points]

    other_points = [np.add(vector, difference) for vector in moved_points]

    return other_points


def find_difference(beacons_scanner, beacons_other_scanner):
    for beacon1 in beacons_scanner:
        for beacon2 in beacons_scanner:
            if not np.array_equal(beacon1, beacon2):
                difference_1_and_2 = np.subtract(beacon1, beacon2)

                for other_beacon1 in beacons_other_scanner:
                    for other_beacon2 in beacons_other_scanner:
                        if not np.array_equal(other_beacon1, other_beacon2):

                            if np.array_equal(np.subtract(other_beacon1, other_beacon2), difference_1_and_2):
                                return np.subtract(beacon1, other_beacon1)
    print("stuff is not good")


def calc_differences_per_scanner_per_orientation(data):
    differences_per_scanner_per_orientation = dict()
    for scanner in range(0, len(data)):
        scanner_data = data[scanner]
        differences_per_orientation = dict()
        for xy in range(0, 4):
            for zx in range(0, 2):
                for zxy in range(0, 3):
                    rotated_scanner_data = [rotate_vector(vector, xy, zx, zxy) for vector in scanner_data]
                    differences = set()
                    for i in range(0, len(scanner_data)):
                        for j in range(0, len(scanner_data)):
                            if i != j:
                                difference = np.subtract(rotated_scanner_data[i], rotated_scanner_data[j])
                                if tuple(difference) in differences:
                                    print("doubles")
                                differences.add(tuple(difference))
                    differences_per_orientation[(xy, zx, zxy)] = differences
        differences_per_scanner_per_orientation[scanner] = differences_per_orientation
    return differences_per_scanner_per_orientation


def attempt_one(data):
    differences_per_scanner = list()
    for scanner in range(0, len(data)):
        scanner_data = data[scanner]
        differences = set()
        for i in range(0, len(scanner_data)):
            for j in range(0, len(scanner_data)):
                if i != j:
                    difference = np.subtract(scanner_data[i], scanner_data[j])
                    differences.add(tuple(difference))
        differences_per_scanner.append(differences)

    for scanner in range(0, len(data)):
        for other_scanner in range(scanner + 1, len(data)):
            number_of_differences = len(
                differences_per_scanner[scanner].intersection(differences_per_scanner[other_scanner]))
            if number_of_differences >= 132:
                print(scanner, other_scanner, number_of_differences)


def part2(data):
    """Solve part 2"""


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
