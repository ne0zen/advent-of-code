#!/usr/bin/env python3

import collections

def part1(data):
    expected_unique = 4
    window = collections.deque([None] * expected_unique, maxlen=expected_unique)

    for idx, c in enumerate(data.strip(), start=1):
        window.append(c)
        if None not in window and len(set(window)) == expected_unique:
            return idx


def part2(data):
    expected_unique = 14
    window = collections.deque([None] * expected_unique, maxlen=expected_unique)

    for idx, c in enumerate(data.strip(), start=1):
        window.append(c)
        if None not in window and len(set(window)) == expected_unique:
            return idx


import pytest

@pytest.mark.parametrize('row', """
mjqjpqmgbljsphdztnvjfqwrcgsmlb      7
bvwbjplbgvbhsrlpgdmjqwftvncz        5
nppdvjthqldpwncqszvftbrmjlhg        6
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg   10
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw    11
""".strip().splitlines())
def test_part1_sample(row):
    sample, answer = row.split()
    assert int(answer) == part1(sample)

@pytest.mark.parametrize('row', """
mjqjpqmgbljsphdztnvjfqwrcgsmlb      19
bvwbjplbgvbhsrlpgdmjqwftvncz        23
nppdvjthqldpwncqszvftbrmjlhg        23
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg   29
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw    26
""".strip().splitlines())
def test_part2_sample(row):
    sample, answer = row.split()
    assert int(answer) == part2(sample)


if __name__ == "__main__":
    with open('input06.txt', 'rt') as f:
        result = part1(f.read())
        print('part1:', result)
        f.seek(0)
        result = part2(f.read())
        print('part2:', result)
