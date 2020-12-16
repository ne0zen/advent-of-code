#!/usr/bin/env python3

TREE = '#'

import operator
import functools

def uut(map_file, route=(3, 1)):
    delta_x, delta_y = route

    rows = map_file.read().splitlines()

    len_row = len(rows[0])
    num_rows = len(rows)

    pos_trees = []
    current_row, current_column = 0, 0
    while current_row < len(rows):
        column_to_check = current_column if current_column < len_row else current_column % len_row

        if rows[current_row][column_to_check] == '#':
            pos_trees.append((current_row, current_column))

        # update pos
        current_row += delta_y
        current_column += delta_x

    return len(pos_trees)


if __name__ == "__main__":
    with open('input03.txt', 'rt') as f:
        print('part1:', uut(f, route=(3, 1)))
        f.seek(0)

        routes = [
            (1,1),
            (3,1),
            (5,1),
            (7,1),
            (1,2),
        ]

        num_trees = []
        for route in routes:
            num_trees.append(uut(f, route))
            f.seek(0)
        print("part2:", functools.reduce(operator.mul, num_trees, 1))


import io
import pytest # for decorator

sample = io.StringIO("""
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".strip())
def test_uut_part1():
    assert 7 == uut(sample)

def test_uut_part2():
    routes = [
        (1,1),
        (3,1),
        (5,1),
        (7,1),
        (1,2),
    ]

    num_trees = []
    for route in routes:
        num_trees.append(uut(sample, route))
        sample.seek(0)
    assert [2, 7, 3 ,4, 2] == num_trees
    assert 336 == functools.reduce(operator.mul, num_trees, 1)


@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)
