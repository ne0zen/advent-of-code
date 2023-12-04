#!/usr/bin/env python3


import re
import sys


DEBUG = False


def prnt(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr)


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

    winning_numbers = set(map(int, winning_numbers_str.strip().split()))
    my_numbers = set(map(int, my_numbers_str.strip().split()))

    intersection = list(winning_numbers & my_numbers)

    if intersection:
        score = 1
    else:
        score = 0
    for _ in intersection[1:]:
        score *= 2

    return score


def score_cards_with_copies(card_data):
    winning_numbers_by_id = {}
    matching_numbers_by_id = {}

    max_card_id = 0

    for card_line in card_data:
        card_id_raw, _, card_desc = card_line.strip().partition(': ')
        try:
            card_id = int(re.search(r'Card\s*(\d+):', card_line).group(1))
        except AttributeError:
            breakpoint()
            raise
        winning_numbers_str, _, my_numbers_str = card_desc.partition(' | ')
        winning_numbers_by_id[card_id] = winning_numbers = set(winning_numbers_str.strip().split())
        my_numbers = set(my_numbers_str.strip().split())

        if matching_numbers := list(winning_numbers & my_numbers):
            matching_numbers_by_id[card_id] = matching_numbers

        max_card_id = card_id

    copies_by_id = {
        card_id: 1 # 1 if winning_numbers_by_id[card_id] else 0
        for card_id in range(1, max_card_id + 1)
    }

    for card_id, matching_numbers in matching_numbers_by_id.items():
        num_winning = len(matching_numbers_by_id[card_id])
        card_ids_to_incr = [card_id + inc for inc in range(1, num_winning + 1)]
        current_num_copies = copies_by_id[card_id]

        for i in range(0, current_num_copies):
            prnt(f"Card {card_id} wins {num_winning} cards, to_wit: {card_ids_to_incr}")
            for card_id_to_incr in card_ids_to_incr:
                if card_id_to_incr in copies_by_id:
                    copies_by_id[card_id_to_incr] += 1


    prnt(copies_by_id)

    return list(copies_by_id.values())




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
    """
    Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
    Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
    Card 4 has one winning number (84), so it is worth 1 point.
    Card 5 has no winning numbers, so it is worth no points.
    Card 6 has no winning numbers, so it is worth no points.
    """
    assert [8, 2, 2, 1, 0, 0] == list(score_cards(sample))

def test_score_cards_with_copies():
    """
    Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6.
    """
    assert [1, 2, 4, 8, 14, 1] == score_cards_with_copies(sample)

def test_uut_part1():
    """
    So, in this example, the Elf's pile of scratchcards is worth 13 points.
    """
    assert 13 == sum(score_cards(sample))

def test_uut_part2():
    """
    In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!
    """
    assert 30 == sum(score_cards_with_copies(sample))


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
        print("part2:", sum(score_cards_with_copies(f)))
