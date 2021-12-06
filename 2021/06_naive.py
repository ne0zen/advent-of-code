#!/usr/bin/env python3

new_fish_value = 8

import copy
import pickle
import sys

STATE_FNAME = "/Volumes/RAM/last_state"
TESTING = 'pytest' in sys.modules


"""
really wasteful on storage, but just _barely_ able to get response in reasonable time w/ pypy3
"""

def thing1(data, num_days):
    new_fish = 0
    if TESTING:
        # ignore state file
        last_state = list(map(int, data.read().strip().split(',')))
        cur_day = 1
    else:
        # open file from last run before crash
        print("loading...", end='', flush=True, file=sys.stderr)
        try:
            with open(STATE_FNAME, mode='rb') as f:
                last_state = pickle.load(f)
                new_fish = pickle.load(f)
                cur_day = pickle.load(f)
        except Exception as e:
            last_state = list(map(int, data.read().split(',')))
            cur_day = 1
        finally:
            print('done', flush=True, file=sys.stderr)
    print("day:", cur_day)

    new_state = None
    while cur_day <= num_days:
        new_state = last_state.copy()
        new_fish = 0

        print("calculation...", end='', flush=True, file=sys.stderr)
        # Each day, a 0 becomes a 6 and adds a new 8 to the end of the list,
        # while each other number decreases by 1 if it was present at the start of the day.
        for i, fish in enumerate(new_state):
            if new_state[i] == 0:
                new_state[i] = 6
                new_fish += 1
            else:
                new_state[i] -= 1
        print("done", flush=True, file=sys.stderr)

        print("alloc...", end='', flush=True, file=sys.stderr)
        new_state.extend(new_fish * [new_fish_value])
        print('done', flush=True, file=sys.stderr)
        print(f"day{str(cur_day).zfill(3)}: {len(new_state)}", file=sys.stderr)

        if not TESTING:
            with open(STATE_FNAME, mode='wb') as f:
                print('writing_state...', end='', flush=True, file=sys.stderr)
                pickle.dump(new_state, f)
                pickle.dump(new_fish, f)
                pickle.dump(cur_day, f)
                print('done', flush=True, file=sys.stderr)

        # get ready for next day
        last_state = new_state
        cur_day += 1

    return last_state


if TESTING:
    import pytest

    import io
    sample1 = io.StringIO("""
    3,4,3,1,2
    """.strip())
    @pytest.mark.parametrize('row', map(lambda l: l.strip(), """
    1   2,3,2,0,1
    2   1,2,1,6,0,8
    3   0,1,0,5,6,7,8
    4   6,0,6,4,5,6,7,8,8
    5   5,6,5,3,4,5,6,7,7,8
    6   4,5,4,2,3,4,5,6,6,7
    7   3,4,3,1,2,3,4,5,5,6
    8   2,3,2,0,1,2,3,4,4,5
    9   1,2,1,6,0,1,2,3,3,4,8
    10  0,1,0,5,6,0,1,2,2,3,7,8
    11  6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
    12  5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
    13  4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
    14  3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
    15  2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
    16  1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
    17  0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
    18  6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
    """.strip().split('\n')))
    def test_expected_values(row):
        # parsing
        num_days, expected_values_raw = row.strip().split()
        expected_values = list(map(int, expected_values_raw.split(',')))
        num_days = int(num_days)
        assert expected_values == thing1(sample1, num_days)


    @pytest.mark.parametrize('row', map(lambda l: l.strip(),
        # day expected_fish
        """
        18      26
        80      5934
        """.strip().split('\n')
    ))
    def test_num_fish(row):
        num_days, expected_fish = map(int, row.split())
        assert expected_fish == len(thing1(sample1, num_days))


    @pytest.fixture(autouse=True)
    def run_around_tests():
        # run before
        yield
        # run after
        sample1.seek(0)



if __name__ == '__main__':
    with open('input06.txt', 'rt') as f:
        part1 = thing1(f, 80)
        print("part1:", len(part1))
