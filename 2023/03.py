#!/usr/bin/env python3

from dataclasses import dataclass
import string
import sys

DEBUG = False


@dataclass(init=True)
class Loc:
    x: int
    y: int


def find_numbers_and_number_location_groups(schematic):
    numbers = []
    number_location_groups = []
    # to understand comments in code, consider this sample input line
    # 467..114
    try:
        for y, row in enumerate(schematic):
            current_number = 0
            current_number_locs = []
            was_number = False

            for x, c in enumerate(row):
                if c.isnumeric():
                    # 467..114
                    # ^^^  ^^^
                    current_number_locs.append(Loc(x, y))

                    if was_number:
                        # 467..114
                        #  ^^   ^^
                        current_number *= 10
                        current_number += int(c)
                    else:
                        # 467..114
                        # ^    ^
                        current_number = int(c)
                elif current_number:
                    # 467..114
                    #    ^
                    numbers.append(current_number)
                    number_location_groups.append(current_number_locs)
                    current_number_locs = []
                    current_number = 0
                was_number = c.isnumeric()

                if x == len(row) - 1 and was_number and current_number:
                    # 467..114
                    #        ^
                    numbers.append(current_number)
                    number_location_groups.append(current_number_locs)
                # print(''.join(row))
                # print(' ' * x + '^')
                # print("numbers:", numbers)

        if y == len(schematic) - 1 and was_number:
            numbers.append(current_number)
            number_location_groups.append(current_number_locs)
            number_location_groups = []
            current_number_locs = []
            current_number = 0

    except Exception as e:
        print(f"Error @ {x=} {y=} {current_number=}", file=sys.stderr)
        raise

    return numbers, number_location_groups


def build_search_locs(location_group):
    for loc in location_group:
        yield (loc.x - 1, loc.y - 1) # NW
        yield (loc.x - 1, loc.y)     # W
        yield (loc.x - 1, loc.y + 1) # SW
        yield (loc.x, loc.y - 1)     # N
        yield (loc.x, loc.y + 1)     # S
        yield (loc.x + 1, loc.y - 1) # NE
        yield (loc.x + 1, loc.y)     # E
        yield (loc.x + 1, loc.y + 1) # SE


def find_part_numbers(schematic_str):
    schematic = [
        [c for x, c in enumerate(line.strip())]
        for y, line in enumerate(schematic_str.read().splitlines())
    ]
    def char_at(x, y):
        try:
            return schematic[y][x]
        except IndexError:
            return '.'

    numbers, number_loc_groups = find_numbers_and_number_location_groups(schematic)
    if DEBUG:
        print("numbers:", numbers, file=sys.stderr)
        from pprint import pprint; pprint(number_loc_groups)
    part_numbers = []

    for idx, loc_group in enumerate(number_loc_groups):
        found_sym = False
        for search_loc in build_search_locs(loc_group):
            c = char_at(*search_loc)
            number = numbers[idx]
            if c != '.' and c in string.punctuation:
                if DEBUG:
                    print(f'{c} found near {number} @ {search_loc}', file=sys.stderr)
                part_numbers.append(number)
                found_sym = True
                break
        # if found_sym:
        #     break
    return part_numbers


import io     # for StringIO
import pytest # for decorator

sample = io.StringIO("""
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip())


def test_find_numbers():
    schematic = [
        [c for x, c in enumerate(line.strip())]
        for y, line in enumerate(sample.read().splitlines())
    ]
    numbers, loc_groups = find_numbers_and_number_location_groups(schematic)
    expected_numbers = list(map(int, "467 114 35 633 617 58 592 755 664 598".strip().split()))
    assert expected_numbers == numbers


def test_find_part_numbers():
    expected_numbers = list(map(int, "467 35 633 617 592 644 598".strip().split()))
    assert expected_numbers == find_part_numbers(sample)


def test_uut_part1():
    """
    In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.
    """
    assert 4361 == sum(find_part_numbers(sample))

sample2 = io.StringIO("""
""".strip())

def test_uut_part2():
    """
    In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
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
        print("part1:", sum(find_part_numbers(f)))
        f.seek(0)
        print("part2:", 'TBD')
