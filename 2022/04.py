#!/usr/bin/env python3


def part1(data):
    result = 0

    def build_set(set_desc: str):
        start, end = map(int, set_desc.split('-'))
        print("start, end:", start, end)
        return set(range(start, end + 1))

    for line in data:
        s1, s2 = map(build_set, line.split(','))
        print(f"{s1=} {s2=}")
        if s1.issubset(s2) or s2.issubset(s1):
            result += 1

    return result


def part2(data):
    result = 0

    def build_set(set_desc: str):
        start, end = map(int, set_desc.split('-'))
        print("start, end:", start, end)
        return set(range(start, end + 1))

    for line in data:
        s1, s2 = map(build_set, line.split(','))
        print(f"{s1=} {s2=}")
        if s1.intersection(s2) or s2.intersection(s1):
            result += 1

    return result

import pytest

sample = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip().split()

def test_part1_sample():
    assert 2 == part1(sample)

def test_part2_sample():
    assert 4 == part2(sample)

if __name__ == "__main__":
    with open('input04.txt', 'rt') as f:
        result = part1(f)
        print('part1:', result)
        f.seek(0)
        result = part2(f)
        print('part2:', result)
