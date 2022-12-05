#!/usr/bin/env python3


def part1(data):
    result = 0

    def build_set(set_desc: str):
        start, end = map(int, set_desc.split('-'))
        return set(range(start, end + 1))

    for line in data:
        half_idx = len(line) // 2

        s1 = set(line[:half_idx])
        s2 = set(line[half_idx:])

        # find common
        in_both = list(s1.intersection(s2))[0]

        # calculate priority
        if in_both.islower():
            priority = ord(in_both) - ord('a') + 1
        else:
            priority = ord(in_both) - ord('A') + 27

        result += priority

    return result


def build_groups(data):
    groups = []
    group = []
    for idx, line in enumerate(data):
        line = line.strip()
        if idx % 3 == 0 and idx != 0:
            groups.append(group)
            group = []
        group.append(line)
    groups.append(group)
    return groups


def part2(data):
    groups = list(build_groups(data))
    result = 0

    for group in groups:
        badge_type = list(set(group[0]).intersection(set(group[1])).intersection(set(group[2])))[0]

        if badge_type.islower():
            priority = ord(badge_type) - ord('a') + 1
        else:
            priority = ord(badge_type) - ord('A') + 27
        print("badge_type, priority:",  badge_type, priority)
        result += priority

    return result


import pytest

sample = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip().split()

def test_part1_sample():
    assert 157 == part1(sample)

def test_build_groups():
    assert [
            ['vJrwpWtwJgWrhcsFMMfFFhFp', 'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL', 'PmmdzqPrVvPwwTWBwg'],
            ['wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn', 'ttgJtRGJQctTZtZT', 'CrZsJsPPZsGzwwsLwLmpwMDw'],
    ] == build_groups(sample)

def test_part2_sample():
    assert 70 == part2(sample)


if __name__ == "__main__":
    with open('input03.txt', 'rt') as f:
        result = part1(f)
        print('part1:', result)
        f.seek(0)
        result = part2(f)
        print('part2:', result)
