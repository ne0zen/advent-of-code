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

    # perf improvement, sum(ub - lb) == diff*(diff+1)/2
    # 1 should NOT be added to upper bound
    lb = min(src, dest)
    # +1 because range() is not inclusive (and we want it to be)
    ub = max(src, dest) + 1
    return sum(range(ub - lb))


def compute_min_expensive_distance(data):
    """
    determine point with minimal cost
    to move crab positions to

    cost to move N spaces = 1+2+3...+N

    returns:int cost to move crabs to that point
    """
    crab_positions = crab_positions_from_data(data)

    # min_pos = min(crab_positions)
    min_pos = 0
    max_pos = max(crab_positions)

    min_cost = float('inf')
    min_cost_pos = None
    for possible_dest in range(min_pos, max_pos + 1):
        move_crabs_cost = 0
        bailed_early = False
        for crab_pos in crab_positions:
            move_crab_cost = compute_expensive_cost(possible_dest, crab_pos)

            # if this is true, we chould bail now as we'll never beat current min
            if move_crab_cost + move_crabs_cost > min_cost:
                bailed_early = True
                break

            move_crabs_cost += move_crab_cost

        if not bailed_early and move_crabs_cost < min_cost:
            min_cost = move_crabs_cost
            min_cost_pos = possible_dest

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
