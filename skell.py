#!/usr/bin/env python3


import operator
import functools


def uut(map_file, route=(3, 1)):
    pass

if __name__ == "__main__":
    with open('input04.txt', 'rt') as f:
        print('part1:', uut(f)
        f.seek(0)
        print("part2:", uut(f))


import io
import pytest # for decorator

sample = io.StringIO("""
""".strip())
def test_uut_part1():
    pass
def test_uut_part2():
    pass

@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)
