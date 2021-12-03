#!/usr/bin/env python3


import operator
import functools


def compute_final_position(data):
    x = 0
    y = 0
    for line in data:
        line = line.strip()
        direction, num = line.split()
        num = int(num)
        if 'up' == direction:
            y -= num
        elif 'down' == direction:
            y += num
        elif 'forward' == direction:
            x += num
        else:
            raise f"Unknown direction: {direction}"
    return x, y


def compute_final_position2(data):
    x = 0
    y = 0
    aim = 0
    for line in data:
        line = line.strip()
        direction, num = line.strip().split()
        num = int(num)
        if 'up' == direction:
            aim -= num
        elif 'down' == direction:
            aim += num
        elif 'forward' == direction:
            x += num
            y += num * aim
        else:
            raise f"Unknown direction: {direction}"
        # print(f"{line=}: {x=} {y=} {aim=}")
    return x, y


if __name__ == "__main__":
    with open('input02.txt', 'rt') as f:
        x, y = compute_final_position(f)
        print('part1:', x * y)
        f.seek(0)
        x, y = compute_final_position2(f)
        print("part2:", x * y)


import io
import pytest # for decorator

sample = io.StringIO("""
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".strip())
def test_uut_part1():
    x, y = compute_final_position(sample)
    assert 15 == x
    assert 10 == y

def test_uut_part2():
    x, y = compute_final_position2(sample)
    assert 15 == x
    assert 60 == y

@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)
