#!/usr/bin/env python3


import collections
import functools
import itertools
import operator


def parse(raw_data):
    return [
        [int(c) for c in line.strip()]
        for line in raw_data
    ]


def at(board, x, y):
    x_len = len(board[0])
    y_len = len(board)
    outside_board = not 0 <= x < x_len or not 0 <= y < y_len
    if outside_board:
        # makes border appear really short
        return float('-inf')
    else:
        # returns height @ x, y
        return board[y][x]

def to_north(board, x, y):
    return [
        (x, ny)
        for ny in range(y - 1 , -1, -1)
    ]


def to_west(board, x, y):
    return [
        (nx, y)
        for nx in range(x - 1, -1, -1)
    ]


def to_east(board, x, y):
    return [
        (nx, y)
        for nx in range(x + 1, len(board[y]), 1)
    ]


def to_south(board, x, y):
    return [
        (x, ny)
        for ny in range(y + 1, len(board), 1)
    ]


def is_high_spot(board, x, y):
    this_height = at(board, x, y)
    if x == 0 or x == len(board[0]) - 1:
        return True
    if x == 0 or y == len(board) - 1:
        return True

    return any(
        all(this_height > at(board, *coord) for coord in func(board, x, y))
        for func in [to_north, to_south, to_east, to_west]
    )


def find_high_spots(data):
    for y in range(len(data)):
        for x in range(len(data[0])):
            if is_high_spot(data, x, y):
                yield (x, y)

def part1(data):
    import copy
    high_spots = list(find_high_spots(data))

    # print("board:"); dump(sample)

    # print("\nmarked:")
    # marked = copy.deepcopy(sample)
    # for x, y in high_spots:
    #     marked[y][x] = 'H'
    # dump(marked)
    return len(high_spots)


def find_viewing_distance(board, coord, coords):
    result = 0
    x, y = coord
    if (x == 0
        or x + 1 == len(board[0])
        or y == 0
        or y + 1 == len(board)
    ):
        return 0

    this_height = at(board, *coord)
    coords_can_see = []
    for other in coords:
        x, y = coord
        coords_can_see.append(other)
        # stop if you reach an edge
        if (
            x == 0 or y == 0
            or x + 1 == len(board[y]) or y + 1 == len(board)
        ):
            break
        elif at(board, *other) >= this_height:
            # at the first tree that is the same height
            # or taller than the tree under consideration
            break
    # print(
    #     "coords:", coords,
    #     "this_height:", this_height,
    #     "heights:", [at(board, *other) for other in coords],
    #     "coords_can_see:", coords_can_see,
    # )
    return len(coords_can_see)

    return result


def find_viewing_distances(board, *coord):
    # print("@", coord)
    return [
        find_viewing_distance(board, coord, func(board, *coord))
        for func in [to_north, to_west, to_east, to_south]
    ]


def part2(data):
    def scenic_score(x, y):
        return functools.reduce(
            operator.mul,
            find_viewing_distances(data, x, y),
        )

    scenic_scores = [
        scenic_score(x, y)
        for y in range(len(data))
        for x in range(len(data[y]))
    ]
    return max(scenic_scores)

def dump(board):
    for line in board:
        print(''.join(str(c) for c in line))


import pytest

@pytest.fixture()
def sample():
    return parse("""
    30373
    25512
    65332
    33549
    35390
    """.strip().split('\n'))

def test_part1(sample):
    assert 21 == part1(sample)


def test_find_viewing_distances(sample):
    assert at(sample, 2, 1) == 5
    assert [1, 1, 2, 2] == find_viewing_distances(sample, 2, 1)
    assert at(sample, 2, 3) == 5
    assert [2, 2, 2, 1] == find_viewing_distances(sample, 2, 3)


def test_part2(sample):
    assert 8 == part2(sample)

if __name__ == "__main__":
    with open('input08.txt', 'rt') as f:
        data = parse(f)
    print('part1:', part1(data))
    print('part2:', part2(data))


    # draws a picture of all basins
    # for line in data:
    #     print(''.join('X' if c < 9 else ' ' for c in line))
