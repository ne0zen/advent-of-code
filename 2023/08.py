#!/usr/bin/env python3


from dataclasses import dataclass
import itertools

from parse import parse


DEBUG = False


@dataclass()
class Node:
    id: str
    left: str
    right: str

    def repr(self):
        return f"{id} = ({left.id}, {right.id})"


def build_tree(idata):
    nodes = {}
    for line in idata:
        line = line.strip()
        node = Node(**parse("{id} = ({left}, {right})", line).named)
        nodes[node.id] = node
    if DEBUG:
        from pprint import pprint; pprint(nodes)
    return nodes


def part1(data):
    idata = iter(data)
    directions = next(idata).strip()
    next(idata)

    tree = build_tree(idata)

    steps = 0
    cur = tree['AAA']

    for next_dir in itertools.cycle(directions):
        if cur.id == 'ZZZ':
            break

        if 'L' == next_dir:
            cur = tree[cur.left]
        elif 'R' == next_dir:
            cur = tree[cur.right]
        steps += 1
    return steps


def part2(data):
    idata = iter(data)
    directions = next(idata).strip()
    next(idata)

    tree = build_tree(idata)

    steps = 0
    cur = tree['AAA']

    for next_dir in itertools.cycle(directions):
        if cur.id == 'ZZZ':
            break

        if 'L' == next_dir:
            cur = tree[cur.left]
        elif 'R' == next_dir:
            cur = tree[cur.right]
        steps += 1
    return steps
    result = []
    return result



##  Tests


import io     # for StringIO
import pytest # for decorator

sample = io.StringIO("""
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".strip())

sample2 = io.StringIO("""
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".strip())

def test_uut_part1_sample():
    """
    """
    assert 2 == part1(sample)

def test_uut_part1_sample2():
    """
    """
    assert 6 == part1(sample2)

def test_uut_part2():
    """
    """
    assert True

@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)
    sample2.seek(0)


if __name__ == "__main__":
    import os
    # extract number
    FNAME = 'input' + os.path.splitext(os.path.basename(__file__))[0] + '.txt'
    print("FNAME:", FNAME)
    with open(FNAME, 'rt') as f:
        print("part1:", part1(f))
        f.seek(0)
        print("part2:", part2(f))
