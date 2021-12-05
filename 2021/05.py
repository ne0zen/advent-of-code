#!/usr/bin/env python3

import collections


def interpolate(start: str, end: str, allow_diagonal=True):
    results = []
    x1, y1 = tuple(map(int, start.split(',')))
    x2, y2 = tuple(map(int, end.split(',')))

    # print(f"{x1=} {y1=} {x2=} {y2=}")

    points = []

    # for all below lines,
    if y1 == y2:  # if line is horizontal
        points = [
            (x, y1)
            for x in range(min(x1, x2), max(x1, x2) + 1)
        ]

    elif x1 == x2:  # if line is vertical
        points = [
            (x1, y)
            for y in range(min(y1, y2), max(y1, y2) + 1)
        ]
    elif allow_diagonal:
        points = []

        x = x1
        y = y1
        dx = 1 if x2 > x1 else -1
        dy = 1 if y2 > y1 else -1

        while x != x2 and y != y2:
            new_point = (x, y)
            points.append(new_point)
            x += dx
            y += dy

        points.append(
            (x2, y2)
        )

    return points


def count_overlaps(data, allow_diagonal=False):
    overlaps_by_point = collections.defaultdict(lambda: 0)
    for line in data:
        start, end = line.split(' -> ')
        for point in interpolate(start, end, allow_diagonal):
            overlaps_by_point[point] += 1

    num_overlaps = sum([
        1
        for point, count in overlaps_by_point.items()
        if count >= 2
    ])
    return num_overlaps


if __name__ == "__main__":
    with open('input05.txt', 'rt') as f:
        overlaps = count_overlaps(f)
        print('part1:', overlaps)
        f.seek(0)
        overlaps = count_overlaps(f, allow_diagonal=True)
        print('part2:', overlaps)


import io
import pytest # for decorator

sample = io.StringIO("""
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip())
def test_uut_part1():
    assert 5 == count_overlaps(sample)


@pytest.mark.parametrize('start,end,allow_diagonal,expected_points', [
    # An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    ['1,1', '1,3', True, [(1, 1), (1, 2), (1, 3)]],
    # An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
    ['9,7', '7,7', True, [(9, 7), (8, 7), (7, 7)]],

    # An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    ['1,1', '3,3', True, [(1, 1), (2, 2), (3, 3)]],

    # An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
    ['9,7', '7,9', True, [(9, 7), (8, 8), (7, 9)]],
])
def test_interpolate(start, end, allow_diagonal, expected_points):
    assert sorted(expected_points) == sorted(
        interpolate(start, end, allow_diagonal)
    )


@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)
