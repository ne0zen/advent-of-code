#!/usr/bin/env python3


import re


def score_cards(data):
    for line in data:
        line = line.strip()
        if not line:
            continue
        yield score_card(line)


def score_card(card_line):
    card_id_raw, _, card_desc = card_line.strip().partition(': ')
    try:
        card_id = int(re.search(r'Card\s*(\d+)', card_id_raw).group(1))
    except AttributeError:
        breakpoint()
        raise
    winning_numbers_str, _, my_numbers_str = card_desc.partition(' | ')

    winning_numbers = set(map(int, winning_numbers_str.split()))
    my_numbers = set(map(int, my_numbers_str.split()))

    intersection = list(winning_numbers & my_numbers)

    if intersection:
        score = 1
    else:
        score = 0
    for _ in intersection[1:]:
        score *= 2

    return score


def part2(data):
    result = []
    return result


##  Tests


import io     # for StringIO
import pytest # for decorator

sample = io.StringIO("""
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".strip())

def test_score_cards():
    assert [8, 2, 2, 1, 0, 0] == list(score_cards(sample))

def test_uut_part1():
    """
    """
    assert 13 == sum(score_cards(sample))

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


if __name__ == "__main__":
    import os
    # extract number
    FNAME = 'input' + os.path.splitext(os.path.basename(__file__))[0] + '.txt'
    print("FNAME:", FNAME)
    with open(FNAME, 'rt') as f:
        print("part1:", sum(score_cards(f)))
        f.seek(0)
        print("part2:", part2(f))
