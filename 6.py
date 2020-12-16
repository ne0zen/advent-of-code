#!/usr/bin/env python3

import io
import operator
import functools


def num_intersection_answers_for_group(lines):
    all_groups = []
    this_group = set()
    is_first_data_line_for_group = True

    for line in lines:
        line = line.strip()

        if line and is_first_data_line_for_group:
            this_group = set(line)
            is_first_data_line_for_group = False
        elif line:
            this_group.intersection_update(line)
        else: # empty line (i.e. end of group)
            all_groups.append(this_group)
            is_first_data_line_for_group = True

    # add last group before EOF
    all_groups.append(this_group)

    num_answers_for_group = list(map(len, all_groups))
    return num_answers_for_group


def num_union_answers_for_group(lines):
    yes_answers_for_groups = []
    yes_answers_for_group = set()

    for line in lines:
        line = line.strip()
        is_data_line = line and lines.readable()

        if is_data_line:
            # parse new yes answers
            new_affirmative_answers = list(line)
            yes_answers_for_group.update(new_affirmative_answers)
        else:
            yes_answers_for_groups.append(yes_answers_for_group)
            yes_answers_for_group = set()

    #FIXME debugging
    if len(yes_answers_for_groups) < 10:
        print("yes_answers_for_groups:", yes_answers_for_groups)
    # handle last group before EOF
    yes_answers_for_groups.append(yes_answers_for_group)

    num_yes_answers_for_groups = list(map(len, yes_answers_for_groups))
    return num_yes_answers_for_groups


if __name__ == "__main__":
    with open('input06.txt', 'rt') as f:
        print('part1:', sum(num_union_answers_for_group(f)))
        f.seek(0)
        print("part2:", sum(num_intersection_answers_for_group(f)))


import io
import pytest # for decorator

sample = io.StringIO("""
abc

a
b
c

ab
ac

a
a
a
a

b
""".strip())
def test_part1_sample():
    num_yes_answers_for_groups = num_union_answers_for_group(sample)
    assert [3, 3, 3, 1, 1] == num_yes_answers_for_groups
    assert 11 == sum(num_yes_answers_for_groups)

def test_part2_sample():
    answers_for_groups = num_intersection_answers_for_group(sample)
    assert [3, 0, 1, 1, 1] == answers_for_groups
    assert 6 == sum(answers_for_groups)


@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)
