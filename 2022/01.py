#!/usr/bin/env python3


def part1(data):
    totals = [0]
    idx = 0

    for line in data:
        if not line.strip():
            idx += 1
            totals.append(0)
            continue
        totals[idx] += int(line)

    return max(totals)


def part2(data):
    totals = [0]
    idx = 0

    for line in data:
        if not line.strip():
            idx += 1
            totals.append(0)
            continue
        totals[idx] += int(line)

    return sum(sorted(totals, reverse=True)[:3])


import pytest

sample = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def test_part1_sample():
    assert 24000 == part1(sample.strip().split('\n'))

def test_part2_sample():
    assert 45000 == part2(sample.strip().split('\n'))

if __name__ == "__main__":
    with open('input01.txt', 'rt') as f:
        result = part1(f)
        print('part1:', result)
        f.seek(0)
        result = part2(f)
        print('part2:', result)
