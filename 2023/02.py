#!/usr/bin/env python3

import re

def parse_withdraw_sets(raw_str):
    """
    Example input:
    3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    """
    withdraw_sets = []
    split_sets = raw_str.strip().split('; ')

    for withdraw_desc in split_sets:
        new_set = {}
        for withdraw in withdraw_desc.split(', '):
            num_str, _, color = withdraw.partition(' ')
            new_set[color] = int(num_str)
        withdraw_sets.append(new_set)
    return withdraw_sets


def get_withdraw_sets_by_id(games_data):
    games_by_id = {}

    withdraw_specs = []
    for line in games_data:
        game_id_raw, _, withdraw_sets_str = line.strip().partition(':')
        game_id = int(re.search(r'Game (\d+)', game_id_raw).group(1))

        withdraw_sets = parse_withdraw_sets(withdraw_sets_str)
        games_by_id[game_id] = withdraw_sets
    return games_by_id


def is_possible(withdraw_sets, bag_state):
    for withdraw_set in withdraw_sets:
        for color in ['red', 'green', 'blue']:
            if not withdraw_set.get(color, 0) <= bag_state.get(color, 0):
                return False
    return True


def find_possible_games(games_data, bag_state):
    result = []
    games_by_id = get_withdraw_sets_by_id(games_data)
    for id, withdraw_specs in games_by_id.items():
        if is_possible(withdraw_specs, bag_state):
            result.append(id)
    return result


def find_min_bag_states(withdraw_sets):
    min_bag_states = []
    for withdraws in withdraw_sets:
        min_bag_state = {}
        for color in ['red', 'green', 'blue']:
            min_bag_state[color] = max(
                withdraw.get(color, 0)
                for withdraw in withdraws
            )
        min_bag_states.append(min_bag_state)
    return min_bag_states



##  Tests



import io     # for StringIO
import pytest # for decorator

def test_build_withdraw_specs():
    assert [
      {'blue': 3, 'red': 4},
      {'red': 1, 'green': 2, 'blue': 6},
      {'green': 2}
    ] == parse_withdraw_sets("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")

sample = io.StringIO("""
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip())
def test_uut_part1():
    """
    In the example above, games 1, 2, and 5 would have been possible if the bag
    had been loaded with that configuration. However, game 3 would have been
    impossible because at one point the Elf showed you 20 red cubes at once;
    similarly, game 4 would also have been impossible because the Elf showed you 15
    blue cubes at once. If you add up the IDs of the games that would have been
    possible, you get 8.
    """
    bag_state = {'red': 12, 'green': 13, 'blue': 14}
    assert [1, 2, 5] == find_possible_games(sample, bag_state)

@pytest.mark.parametrize(
    'expected_str,withdraw_sets_str', [
    ("4 red, 2 green, and 6 blue", "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"),
    ("1 red, 3 green, and 4 blue cubes.", "1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"),
    ("20 red, 13 green, and 6 blue cubes", "8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"),
    ("14 red, 3 green, and 15 blue cubes.", "1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"),
    ("6 red, 3 green, and 2 blue cubes", "6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"),
])
def test_find_min_bag_states(expected_str, withdraw_sets_str):
    expected = {
        k: int(v)
        for k, v in
        re.search(
            '(?P<red>\d+) red, (?P<green>\d+) green, and (?P<blue>\d+) blue',
            expected_str
        ).groupdict().items()
    }
    assert [expected] == find_min_bag_states([parse_withdraw_sets(withdraw_sets_str)])



# test helpers

@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)


if __name__ == "__main__":
    import os
    import operator
    # extract number
    FNAME = 'input' + os.path.splitext(os.path.basename(__file__))[0] + '.txt'
    print("FNAME:", FNAME)
    with open(FNAME, 'rt') as f:
        bag_state = {'red': 12, 'green': 13, 'blue': 14}
        print("part1:", sum(find_possible_games(f, bag_state)))
        f.seek(0)
        print("part2:", sum(
            bag_state['red'] * bag_state['green'] * bag_state['blue']
            for bag_state in find_min_bag_states(
                [
                    v
                    for _, v in get_withdraw_sets_by_id(f).items()
                ]
            )
        ))
