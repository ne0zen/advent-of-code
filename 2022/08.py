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
    for ny in range(y):
        yield x, ny

def to_south(board, x, y):
    for ny in range(y + 1, len(board)):
        yield x, ny

def to_east(board, x, y):
    for nx in range(x + 1, len(board[0])):
        yield nx, y

def to_west(board, x, y):
    for nx in range(x):
        yield nx, y


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


# def find_basins(board):
#     for l_x, l_y in find_low_spots(board):
#         basin_coords = set()
#         queue = collections.deque([(l_x, l_y)])

#         while len(queue) > 0:
#             coord = queue.popleft()
#             basin_coords.add(coord)
#             this_val = at(board, *coord)

#             for a_coord, val in gen_around(board, *coord):
#                 if val < 9 and val > this_val and a_coord not in basin_coords:
#                     queue.append(a_coord)
#         yield basin_coords


# def find_basin_area_total(board):
#     basin_sizes = []
#     for basin in find_basins(board):
#         # dump_basin(board, basin)
#         basin_sizes.append(len(basin))

#     return functools.reduce(operator.mul, sorted(basin_sizes)[-3:], 1)

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
    import copy
    high_spots = list(find_high_spots(sample))

    # print("board:"); dump(sample)

    # print("\nmarked:")
    # marked = copy.deepcopy(sample)
    # for x, y in high_spots:
    #     marked[y][x] = 'H'
    # dump(marked)

    assert 21 == len(high_spots)

if __name__ == "__main__":
    with open('input08.txt', 'rt') as f:
        data = parse(f)
    # 1835 too low
    print('part1:', len(list(find_high_spots(data))))

    # draws a picture of all basins
    # for line in data:
    #     print(''.join('X' if c < 9 else ' ' for c in line))
