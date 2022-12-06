#!/usr/bin/env python3



def get_outcome_score(opponent_val, my_val):
    """
    Rock (1) beats Scissors (3)
    Scissors (3) beats Paper (2)
    Paper (2) beats Rock (1)
    """
    # key: (opponent_val, my_val)
    # value: 0 if you lost, 3 if the round was a draw, and 6 if you won
    return {
        # draws
        (1, 1): 3,
        (2, 2): 3,
        (3, 3): 3,
        # I lost
        (3, 2): 0,
        (1, 3): 0,
        (2, 1): 0,
        # I won!
        (2, 3): 6,
        (3, 1): 6,
        (1, 2): 6,
    }[(opponent_val, my_val)]


def find_score_increment(opponent_choice, my_choice):
    opponent_val = ord(opponent_choice) - ord("A") + 1
    my_val = ord(my_choice) - ord("X") + 1

    outcome_score = get_outcome_score(opponent_val, my_val)
    # 1 for Rock, 2 for Paper, and 3 for Scissors
    shape_score = my_val
    # print("outcome_score, shape_score:", outcome_score, shape_score)

    return outcome_score + shape_score

def part1(data):
    rounds = list(map(lambda s: s.split(), data.strip().splitlines()))
    score = 0

    for opponent_choice, my_choice in rounds:
        score_increment = find_score_increment(opponent_choice, my_choice)
        score += score_increment

    return score


def part2(data):
    return


import pytest

sample = """
A Y
B X
C Z
"""

def test_part1_sample():
    assert 15 == part1(sample)

# def test_part2_sample():
#     assert 45000 == part2(sample.strip().split('\n'))

if __name__ == "__main__":
    with open('input02.txt', 'rt') as f:
        result = part1(f.read())
        print('part1:', result)
        f.seek(0)
        result = part2(f.read())
        print('part2:', result)
