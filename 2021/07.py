#!/usr/bin/env python3

import statistics


def crab_positions_from_data(data):
    return [int(n) for n in data.split(',')]


def compute_min_distance(data):
    """
    compute point with minimal cost
    to move crab positions to
    (cost to move one space assumed to be constant of 1)
    """
    crab_positions = crab_positions_from_data(data)
    point = int(statistics.median(crab_positions))
    return sum(abs(pos - point) for pos in crab_positions)


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
        distance = compute_min_distance(f.read())
        print('part1:', distance)
        f.seek(0)
        x, y = compute_final_position2(f)
        print("part2:", x * y)
