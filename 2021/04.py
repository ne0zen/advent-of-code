#!/usr/bin/env python3


BOARD_SIZE = 5


def parse(data):
    data_iter = iter(data)
    moves = [int(item) for item in next(data_iter).split(',')]

    next(data_iter)  # blank line

    boards = []
    # for _ in range(3):
    while data_iter:
        try:
            board = [
                [
                    [int(item), False]
                    for item in next(data_iter).split()
                ]
                for _ in range(BOARD_SIZE)
            ]
        except StopIteration:
            break

        try:
            next(data_iter) # blank line?
        except StopIteration:
            pass
        # try:
        #     next(data_iter) # blank line?
        # except StopIteration:
        #     pass

        if board:
            boards.append(board)
    return boards, moves


def apply_move(board, move):
    # -> board
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            node = board[y][x]
            if node[0] == move:
                node[1] = True
    return board


WINNING_PATTERNS = []
for raw_win_row in """
0,0 0,1 0,2 0,3 0,4
1,0 1,1 1,2 1,3 1,4
2,0 2,1 2,2 2,3 2,4
3,0 3,1 3,2 3,3 3,4
4,0 4,1 4,2 4,3 4,4

0,0 1,0 2,0 3,0 4,0
0,1 1,1 2,1 3,1 4,1
0,2 1,2 2,2 3,2 4,2
0,3 1,3 2,3 3,3 4,3
0,4 1,4 2,4 3,4 4,4
""".strip().split('\n'):
    raw_win_row = raw_win_row.strip()
    if not raw_win_row:
        continue
    WINNING_PATTERNS.append([
        tuple(map(int, pair.split(',')))
        for pair in raw_win_row.split()
    ])


def has_win(board):
    """
    args: board

    returns set of points for winning "line"
    """
    # -> []
    for winning_row in WINNING_PATTERNS:
        if all(
            board[y][x][1]
            for x, y in winning_row
        ):
            return True

    return None


def determine_last_win(data):
    data = [line.strip() for line in data]
    boards, moves = parse(data)

    win_state = [False for _ in range(len(boards))]

    last_winner = None
    for move in moves:
        for i, board in enumerate(boards):
            if win_state[i]:
                continue
            board = apply_move(board, move)
            if has_win(board):
                # print(f"board #{i} won")
                win_state[i] = True
                if all(win_state):
                    last_winner = board
                    last_move = move
                    break
        # dump_state(boards, move)
        if last_winner:
            break

    winning_score = sum(
        last_winner[y][x][0]
        for x in range(BOARD_SIZE)
        for y in range(BOARD_SIZE)
        if last_winner[y][x][1] == False
    )
    return winning_score, last_move


def determine_first_win(data):
    data = [line.strip() for line in data]
    boards, moves = parse(data)

    winning_board = None
    for move in moves:
        for i, board in enumerate(boards):
            board = apply_move(board, move)
            if has_win(board):
                winning_board = board
                winning_move = move
                break
        # dump_state(boards, move)
        if winning_board:
            break

    winning_score = sum(
        winning_board[y][x][0]
        for x in range(BOARD_SIZE)
        for y in range(BOARD_SIZE)
        if winning_board[y][x][1] == False
    )
    return winning_score, move


def dump_state(boards, move):
    print('\033c')
    print("move:", move)
    dboards = []
    for board in boards:
        dboard = list(dump_board(board))
        dboards.append(dboard)
    input()

def dump_board(board):
    for row in board:
        yield ' '.join(
            f"{'[' if picked == True else ' '}{num:02}{']' if picked == True else ' '}"
            for num, picked in row
        )

# Tests
import io
import pytest # for decorator

sample = io.StringIO("""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".strip())
def test_uut_part1():
    winning_score, winning_move = determine_first_win(sample)
    assert 188 == winning_score
    assert 24 == winning_move

def test_uut_part2():
    winning_score, winning_move = determine_last_win(sample)
    assert 148 == winning_score
    assert 13 == winning_move



sample2 = io.StringIO("""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".strip())
def test_parse_more_boards():
    boards, moves = parse(sample2)
    assert 6 == len(boards)

@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)


if __name__ == "__main__":
    with open('input04.txt', 'rt') as f:
        winning_score, last_move = determine_first_win(f)
        print('part1:', winning_score * last_move)
        f.seek(0)
        winning_score, last_move = determine_last_win(f)
        print('part2:', winning_score * last_move)
