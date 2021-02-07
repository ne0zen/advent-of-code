#!/usr/bin/env python3

from dataclasses import dataclass
import collections
import re


COLOR_PATTERN = re.compile(r"""
(?P<color>\w+\s\w+)
\s
bags?
""".strip(), re.VERBOSE)

def solve_part1(rules, to_house='shiny gold'):

    child_colors_by_parent_color = {}
    parent_colors_by_child_color = collections.defaultdict(list)
    # build data structures
    for rule in rules:
        parent_color, *child_colors = COLOR_PATTERN.findall(rule)

        if child_colors == ['no other']:
            child_colors = []
        child_colors_by_parent_color[parent_color] = child_colors

        for child_color in child_colors:
            parent_colors_by_child_color[child_color].append(parent_color)

    # determine number of parents
    can_hold = set()
    to_add = collections.deque(parent_colors_by_child_color[to_house])
    while len(to_add) > 0:
        current = to_add.popleft()
        can_hold.add(current)
        to_add.extend(parent_colors_by_child_color[current])

    return can_hold



@dataclass(frozen=True)
class Node:
    count: int
    color: str


def count_children(children_by_parent_color, root='shiny gold', count_self=False):
    """
    counts total number of children
    """
    child_counts = [
        int(child.count) * count_children(
            children_by_parent_color,
            root=child.color,
            count_self=True
        )
        for child in children_by_parent_color[root]
    ]

    sum_child_counts = sum(child_counts)

    return sum_child_counts + (1 if count_self else 0)


# Helpers
def build_children_by_parent_color(rules):
    children_by_parent_color = collections.defaultdict(list)
    for rule in rules:
        rule = rule.strip()
        # first two words
        parent_color = re.match(r'\w+\s\w+', rule).group()
        # number followed by two words
        child_matches = re.findall(r'(\d+)\s(\w+\s\w+)', rule)

        children_by_parent_color[parent_color] = [
            Node(*match)
            for match in child_matches
        ]
    return children_by_parent_color

if __name__ == "__main__":
    with open('input07.txt', 'rt') as f:
        results = solve_part1(f)
        print("part1:", len(results))
        f.seek(0)
        results = count_children(build_children_by_parent_color(f), 'shiny gold')
        print("part2:", results)



# Tests

import io
sample = io.StringIO("""
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip())
def test_all_parents_sample():
    assert 4 == len(solve_part1(sample))


def test_count_children_sample1():
    expected_color_strings = [
        '0 faded blue',
        '0 dotted black',
        '11 vibrant plum',
        '7 dark olive',
    ]
    #So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!
    children_by_parent_color = build_children_by_parent_color(sample)
    for string in expected_color_strings:
        expected, _, color = string.partition(' ')
        expected = int(expected)
        print("color:", color)
        assert expected == count_children(children_by_parent_color, color)


def test_count_children_sample2():
    rules = """
    shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.
    dark yellow bags contain 2 dark green bags.
    dark green bags contain 2 dark blue bags.
    dark blue bags contain 2 dark violet bags.
    dark violet bags contain no other bags.
    """.strip().split('\n')

    children_by_parent_color = build_children_by_parent_color(rules)
    print("dark violet:")
    assert 0 == count_children(children_by_parent_color, 'dark violet')
    print("dark blue:")
    assert 2 == count_children(children_by_parent_color, 'dark blue')
    #assert 8 == count_children(children_by_parent_color, 'dark green')
    assert 126 == count_children(children_by_parent_color, 'shiny gold')




import pytest
@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)
