#!/usr/bin/env python3

import re


def get_state(data):
    if data[0].startswith('    [D]'):
        # sample
        return list(map(lambda s: s.split(), [
            "Z N",
            "M C D",
            "P"
        ]))

    elif data[0].startswith("[J]             [F] [M]"):
        # created manually from puzzle input
        return list(map(lambda s: s.split(), [
            "N B D T V G Z J",
            "S R M D W O F",
            "V C R S Z",
            "R T J Z P H G",
            "T C J N D Z Q F",
            "N V P W G S F M",
            "G C V B P Q",
            "Z B P N",
            "W P J",
        ]))
    else:
        print(data[0])
        raise Exception("nope")


MOVE_REGEX = re.compile(r"move (\d+) from (\d+) to (\d+)")


def part1(data):
    data = data.split('\n')
    state = get_state(data)

    for line in data:
        match = MOVE_REGEX.search(line)
        if not match:
            continue
        num_to_move, src, dest = map(int, match.groups())

        # stack index adjust
        src -= 1
        dest -= 1

        for _ in range(num_to_move):
            state[dest].append(state[src].pop())

    return "".join(s[-1] for s in state)


def part2(data):
    data = data.split('\n')
    state = get_state(data)

    for line in data:
        match = MOVE_REGEX.search(line)

        if not match:
            continue

        num_to_move, src, dest = map(int, match.groups())

        # stack index adjust as they start at 1 in move desciptions
        # and 0 in state
        src -= 1
        dest -= 1

        to_move = []
        for _ in range(num_to_move):
            to_move.append(state[src].pop())

        for crate in reversed(to_move):
            state[dest].append(crate)

    return "".join(s[-1] for s in state)


import pytest

sample = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

def test_part1_sample():
    assert "CMZ" == part1(sample)

def test_part2_sample():
    assert "MCD" == part2(sample)


if __name__ == "__main__":
    with open('input05.txt', 'rt') as f:
        result = part1(f.read())
        print('part1:', result)
        f.seek(0)
        result = part2(f.read())
        print('part2:', result)
