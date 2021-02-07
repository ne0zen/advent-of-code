#!/usr/bin/env python3


def check_valid1(policy, password):
    # e.g.  "1-3 a: abcde"
    num_times, letter = policy.split()

    # e.g. 1-3
    lower_bound, upper_bound = num_times.split('-')
    lower_bound = int(lower_bound)
    upper_bound = int(upper_bound)
    return lower_bound <= password.count(letter) <= upper_bound


def check_valid2(policy, password):
    # e.g.  "1-3 a: abcde"
    positions, letter = policy.split()

    # e.g. 1-3
    possible1, possible2 = positions.split('-')
    possible1 = int(possible1)
    possible2 = int(possible2)

    first_matches = password[possible1 - 1] == letter
    second_matches = password[possible2 - 1] == letter
    return (first_matches and not second_matches) or (second_matches and not first_matches)


def find_num_valid(to_check, is_valid=check_valid1):
    valid_passwords = []

    for line in to_check:
        line = line.strip()
        policy, _, password = line.partition(':')
        password = password.strip()
        if is_valid(policy, password):
            valid_passwords.append(password)

    return len(valid_passwords)



if __name__ == "__main__":
    with open('input02.txt', 'rt') as f:
        entries = f.read().splitlines()
        print('part1:', find_num_valid(entries, is_valid=check_valid1))
        f.seek(0)
        print('part2:', find_num_valid(entries, is_valid=check_valid2))



## Tests
import pytest
import io
sample = io.StringIO("""
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
""".strip())
def test_find_num_valid():
    assert 2 == find_num_valid(sample, is_valid=check_valid1)

def test_find_num_valid_w_custom_checker():
    assert 1 == find_num_valid(sample, is_valid=check_valid2)

@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)
