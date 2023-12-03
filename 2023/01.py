#!/usr/bin/env python3


def find_first_last_digit(line):
    result = ''
    for c in line:
        if c.isnumeric():
            result += c
            break

    for c in reversed(line):
        if c.isnumeric():
            result += c
            break

    if len(result) < 2:
        return 0

    return int(result)


VALUE_BY_WORD = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
}
def find_first_last_digit_from_words(line):
    found_num = complex(0, 1)
    min_idx = float('Inf')
    for word, word_val in VALUE_BY_WORD.items():
        idx = line.find(word)
        if idx >= 0 and idx < min_idx:
            found_num = word_val
            min_idx = idx
    result = found_num * 10

    found_num = complex(0, 2)
    max_idx = float('-Inf')
    for word, word_val in VALUE_BY_WORD.items():
        idx = line.rfind(word)
        if idx >= 0 and idx > max_idx:
            found_num = word_val
            max_idx = idx
    result += found_num
    try:
        return int(result)
    except TypeError as e:
        return 0


def find_calibration_values(data, mode=1):
    if 1 == mode:
        func =  find_first_last_digit
    elif 2 == mode:
        func = find_first_last_digit_from_words
    return [func(line.strip()) for line in data]


def sum_calibration_values(data, mode=1):
    calibration_values = find_calibration_values(data, mode=mode)
    return sum(calibration_values)


##  Tests



import io     # for StringIO
import pytest # for decorator

sample = io.StringIO("""
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""".strip())
def test_find_calibration_values_part1():
    [12, 38, 15, 77] == find_calibration_values(sample)

def test_uut_part1():
    """
    In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.
    """
    assert 142 == sum_calibration_values(sample)

sample2 = io.StringIO("""
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""".strip())

def test_find_calibration_values_shared_letters():
    [79, 83] == find_calibration_values("sevenine\neighthree", mode=2)

def test_find_calibration_values_part2():
    [29, 83, 13, 24, 42, 14, 76] == find_calibration_values(sample2, mode=2)

def test_uut_part2():
    """
    In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
    """
    assert 281 == sum_calibration_values(sample2, mode=2)

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
        print("part1:", sum_calibration_values(f))
        f.seek(0)
        print("part2:", sum_calibration_values(f, mode=2))
