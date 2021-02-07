#!/usr/bin/env python3

import io


CHECK_FOR = 2020

import itertools
import operator
import functools


def find_product(entries):
    to_check = list(itertools.permutations(entries, 2))
    for lhs, rhs in to_check:
        if lhs + rhs == CHECK_FOR:
            return lhs * rhs


def find_product_of_all(entries):
    to_check = list(itertools.permutations(entries, 3))

    terms = set()
    for possible in to_check:
        if sum(possible) == CHECK_FOR:
            for term in possible:
                terms.add(term)
    print("terms:", terms)
    return functools.reduce(operator.mul, terms, 1)


def test_find_product():
    expense_report = io.StringIO("""
    1721
    979
    366
    299
    675
    1456
    """.strip())
    entries = [int(line) for line in expense_report]
    assert find_product(entries) == 514579


def test_find_product_of_all():
    expense_report = io.StringIO("""
    1721
    979
    366
    299
    675
    1456
    """.strip())
    entries = [int(line) for line in expense_report]
    assert find_product_of_all(entries) == 241861950


if __name__ == "__main__":
    with open('input01.txt', 'rt') as expense_report:
        entries = [int(line) for line in expense_report]
        print("part1:", find_product(entries))
        print("part2:", find_product_of_all(entries))
