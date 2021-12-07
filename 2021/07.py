#!/usr/bin/env python3

import statistics


def crab_positions_from_data(data):
    return [int(n) for n in data.read().strip().split(',')]


def compute_min_distance(data):
    """
    compute point with minimal cost
    to move crab positions to
    (cost to move one space assumed to be constant of 1)
    """
    crab_positions = crab_positions_from_data(data)
    point = int(statistics.median(crab_positions))
    return sum(abs(pos - point) for pos in crab_positions)


def compute_expensive_cost(src: int, dest: int):
    """
    >>> compute_expensive_cost(3, 3)
    0
    >>> compute_expensive_cost(0, 2)
    3
    >>> compute_expensive_cost(0, 3)
    6
    >>> compute_expensive_cost(8, 5)
    6
    """
    if src == dest:
        return 0

    lb = min(src, dest)     # 3
    ub = max(src, dest) + 1 # 4
    span = range(ub - lb)
    return sum(span)


def compute_min_expensive_distance(data):
    """
    compute point with minimal cost
    to move crab positions to

    cost to move N spaces = sum(1..N)
    """
    crab_positions = crab_positions_from_data(data)

    # min_pos = min(crab_positions)
    min_pos = 0
    max_pos = max(crab_positions)


    min_cost = float('inf')
    min_cost_pos = None
    for possible_dest in range(min_pos, max_pos + 1):
        cost_to_move_crabs_to_dest = sum(
            compute_expensive_cost(possible_dest, crab_pos)
            for crab_pos in crab_positions
        )

        if cost_to_move_crabs_to_dest < min_cost:
            min_cost_pos = possible_dest
            min_cost = cost_to_move_crabs_to_dest

    return min_cost


import io
import pytest # for decorator

sample = io.StringIO("""
16,1,2,0,4,2,7,1,2,14
""".strip())
def test_uut_part1():
    distance = compute_min_distance(sample)
    assert 37 == distance

def test_uut_part2():
    distance = compute_min_expensive_distance(sample)
    assert 168 == distance


@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)


if __name__ == "__main__":
    with open('input07.txt', 'rt') as f:
        distance = compute_min_distance(f)
        print('part1:', distance)
        f.seek(0)
        distance = compute_min_expensive_distance(f)
        print('part2:', distance)
