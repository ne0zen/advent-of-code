#!/usr/bin/env python3

import copy

CHAIR = 'L'
OCCUPIED = '#'
FLOOR = '.'
TOO_MANY_SEATS = 4


def get_neighbors(board, row, column):
    num_rows = len(board)
    num_columns = len(board[0])
    row_possibilities = [row - 1, row, row + 1]
    column_possibilities = [column - 1, column, column + 1]

    # compute neighbors
    neighbors = set()
    for row_try in row_possibilities:
        if not (row_try >= 0 and row_try < num_rows):
            continue
        for column_try in column_possibilities:
            if not (column_try >= 0 and column_try < num_columns):
                continue
            neighbors.add((row_try, column_try))
    neighbors.discard((row, column))
    return neighbors


def count_all_occupied(board):
    num = 0
    for row in board:
        for pos in row:
            if OCCUPIED == pos:
                num += 1
    return num

def count_nearby_occupied_seats(board, row, column):
    neighbors = get_neighbors(board, row, column)

    num = 0
    for row, column in neighbors:
        pos = board[row][column]
        if pos == OCCUPIED:
            num += 1
    return num


def step(board):
    num_cols = len(board[0])
    num_rows = len(board)

    next_board = copy.deepcopy(board)
    for row in range(num_rows):
        for column in range(num_cols):
            pos = board[row][column]
            nearby_occupied_seats = count_nearby_occupied_seats(board, row, column)
            if FLOOR == pos: # skip floor
                continue
            elif CHAIR == pos:
                if nearby_occupied_seats == 0:
                    next_board[row][column] = OCCUPIED
            elif OCCUPIED == pos:
                if nearby_occupied_seats >= TOO_MANY_SEATS:
                    next_board[row][column] = CHAIR
            else:
                raise Exception(f"Unknown char {pos} @ {row},{column}(")
    return next_board


def stabilize(original):
    board = copy.deepcopy(original)
    last_board = None
    gen = 0
    while board != last_board:
        last_board = copy.deepcopy(board)
        board = step(board)
        gen += 1
    return board


# Helpers
def make_board(board_str):
    return list(
        list(row.strip())
        for row in board_str.strip().split()
    )
def print_board(board):
    print(chr(27)+'[2j')# clear screen
    for row in board:
        print(''.join(row))

if __name__ == "__main__":
    with open('input11.txt', 'rt') as f:
        board = make_board(f.read())
        stabilized = stabilize(board)

        print("part1:", count_all_occupied(stabilized))


# Tests

def test_get_neighbors():
    board = make_board("""
    L.
    LL
    """)
    print("get_neighbors(board, 0, 0):", get_neighbors(board, 0, 0))
    assert {(0, 1), (1, 0), (1, 1)} == get_neighbors(board, 0, 0)


def test_step_occupies_chairs():
    sample = make_board("""
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
    """)
    gen_1 = make_board("""
    #.##.##.##
    #######.##
    #.#.#..#..
    ####.##.##
    #.##.##.##
    #.#####.##
    ..#.#.....
    ##########
    #.######.#
    #.#####.##
    """)
    assert gen_1 == step(sample)

def test_step_depopulates():
    gen_1 = make_board("""
    #.##.##.##
    #######.##
    #.#.#..#..
    ####.##.##
    #.##.##.##
    #.#####.##
    ..#.#.....
    ##########
    #.######.#
    #.#####.##
    """)

    gen_2 = make_board("""
    #.LL.L#.##
    #LLLLLL.L#
    L.L.L..L..
    #LLL.LL.L#
    #.LL.LL.LL
    #.LLLL#.##
    ..L.L.....
    #LLLLLLLL#
    #.LLLLLL.L
    #.#LLLL.##
    """)
    assert gen_2 == step(gen_1)

def test_sample():
    sample = make_board("""
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
    """)
    stable = make_board("""
    #.#L.L#.##
    #LLL#LL.L#
    L.#.L..#..
    #L##.##.L#
    #.#L.LL.LL
    #.#L#L#.##
    ..L.L.....
    #L#L##L#L#
    #.LLLLLL.L
    #.#L#L#.##
    """)
    stabilized = stabilize(sample)
    assert stable == stabilized
    assert 37 == count_all_occupied(stabilized)
