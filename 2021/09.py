#!/usr/bin/env python3


import collections
import functools
import operator

def parse(raw_data):
    return [
        [int(c) for c in line.strip()]
        for line in raw_data
    ]


def at(board, x, y):
    x_len = len(board[0])
    y_len = len(board)
    if not 0 <= x < x_len or not 0 <= y < y_len:
        return float('inf')
    else:
        return board[y][x]

    return board[y][x]


def gen_around(board, x, y):
    for coord in [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    ]:
        yield (coord, at(board, *coord))


def is_low_spot(board, x, y):
    compare_to = at(board, x, y)

    return all(
        compare_to < val for coord, val in gen_around(board, x, y)
    )


def find_low_spots(data):
    for y in range(len(data)):
        for x in range(len(data[0])):
            if is_low_spot(data, x, y):
                yield (x, y)


def find_sum_risk_levels(data):
    total = 0
    for x, y in find_low_spots(data):
        v = at(data, x, y)
        total += v + 1

    return total



def find_basins(board):
    for l_x, l_y in find_low_spots(board):
        basin_coords = set()
        queue = collections.deque([(l_x, l_y)])

        while len(queue) > 0:
            coord = queue.popleft()
            basin_coords.add(coord)
            this_val = at(board, *coord)

            for a_coord, val in gen_around(board, *coord):
                if val not in (9, float('inf')) and val > this_val:
                    queue.append(a_coord)

        yield basin_coords


def find_basin_area_total(board):
    basin_sizes = []
    for basin in find_basins(board):
        # dump_basin(board, basin)
        basin_sizes.append(len(basin))

    return functools.reduce(operator.mul, sorted(basin_sizes)[-3:], 1)


def dump_basin(board, basin):
    import copy
    b = copy.deepcopy(board)
    print("basin:", basin)

    for x,y in basin:
        b[y][x] = 'X'

    for line in b:
        print(''.join(str(c) for c in line))
    input()


import pytest

@pytest.fixture()
def sample():
    return parse("""
    2199943210
    3987894921
    9856789892
    8767896789
    9899965678
    """.strip().split('\n'))


# def test_find_low_spots(sample):
#     assert [1, 0, 5, 5] == find_low_spots(sample)


def test_find_risk_levels_sum(sample):
    assert 15 == find_sum_risk_levels(sample)


def test_find_basin_area_total(sample):
    assert 1134 == find_basin_area_total(sample)


if __name__ == "__main__":
    with open('input09.txt', 'rt') as f:
        data = parse(f)
    print('part1:', find_sum_risk_levels(data))
    print('part2:', find_basin_area_total(data))

    # draws a picture of all basins
    # for line in data:
    #     print(''.join('X' if c < 9 else ' ' for c in line))
