#!/usr/bin/env python3

from dataclasses import dataclass
import string
import sys


DEBUG = False


@dataclass(init=True, frozen=True)
class Loc:
    x: int
    y: int


def find_number_location_groups(schematic):
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
                    number_location_groups.append(current_number_locs)
                    current_number_locs = []
                    current_number = 0
                was_number = c.isnumeric()

                if x == len(row) - 1 and was_number and current_number:
                    # 467..114
                    #        ^
                    number_location_groups.append(current_number_locs)
                # print(''.join(row))
                # print(' ' * x + '^')
                # print("numbers:", numbers)

        if y == len(schematic) - 1 and was_number:
            number_location_groups.append(current_number_locs)
            current_number_locs = []
            current_number = 0

    except Exception as e:
        print(f"Error @ {x=} {y=} {current_number=}", file=sys.stderr)
        raise

    return number_location_groups


def build_search_locs(location_group):
    for loc in location_group:
        yield Loc(loc.x - 1, loc.y - 1) # NW
        yield Loc(loc.x - 1, loc.y)     # W
        yield Loc(loc.x - 1, loc.y + 1) # SW
        yield Loc(loc.x, loc.y - 1)     # N
        yield Loc(loc.x, loc.y + 1)     # S
        yield Loc(loc.x + 1, loc.y - 1) # NE
        yield Loc(loc.x + 1, loc.y)     # E
        yield Loc(loc.x + 1, loc.y + 1) # SE


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

    number_loc_groups = find_number_location_groups(schematic)
    if DEBUG:
        from pprint import pprint; pprint(number_loc_groups)
    part_numbers = []

    for idx, loc_group in enumerate(number_loc_groups):
        found_sym = False
        for search_loc in build_search_locs(loc_group):
            c = char_at(search_loc.x, search_loc.y)
            number = int(''.join(
                char_at(loc.x, loc.y)
                for loc in loc_group)
            )
            if c != '.' and c in string.punctuation:
                if DEBUG:
                    print(f'{c} found near {number} @ {search_loc}', file=sys.stderr)
                part_numbers.append(number)
                found_sym = True
                break
    return part_numbers


def find_gear_ratios(schematic_str):
    schematic = [
        [c for x, c in enumerate(line.strip())]
        for y, line in enumerate(schematic_str.read().splitlines())
    ]
    def char_at(x, y):
        try:
            return schematic[y][x]
        except IndexError:
            return '.'

    number_loc_groups = find_number_location_groups(schematic)
    if DEBUG:
        from pprint import pprint; pprint(number_loc_groups)

    gear_locations = []

    # find * locs
    for y, row in enumerate(schematic):
        for x, char in enumerate(row):
            if '*' == char:
                gear_locations.append(Loc(x, y))
    if DEBUG:
        print("gear_locations:", gear_locations, file=sys.stderr)

    gear_ratios = []
    for gear_location in gear_locations:
        matches = []
        search_locs = set(build_search_locs([gear_location]))
        for group_idx, location_group in enumerate(number_loc_groups):
            lhs = search_locs
            rhs = set(location_group)
            # if DEBUG:
            #     print(f"attempting match between {''.join(char_at(loc.x, loc.y) for loc in search_locs)} and {rhs=}", file=sys.stderr)
            if intersection := search_locs & set(location_group):
                number = int(''.join(
                    char_at(loc.x, loc.y)
                    for loc in location_group
                ))
                matches.append(number)
                found_match = True
                if DEBUG:
                    print(f"Found {number} near * @ {gear_location}", file=sys.stderr)

        if len(matches) > 1:
            gear_ratio = matches[0] * matches[1]
            gear_ratios.append(gear_ratio)

    return gear_ratios


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
    numbers = [
        int(
            ''.join(schematic[loc.y][loc.x]
            for loc in location_group
        ))
        for location_group in find_number_location_groups(schematic)
    ]
    expected_numbers = list(map(int, "467 114 35 633 617 58 592 755 664 598".strip().split()))
    assert expected_numbers == numbers


def test_find_part_numbers():
    expected_numbers = list(map(int, "467 35 633 617 592 755 664 598".strip().split()))
    assert expected_numbers == find_part_numbers(sample)

def test_find_gear_ratios():
    assert [16345, 451490] == find_gear_ratios(sample)

def test_uut_part1():
    assert 4361 == sum(find_part_numbers(sample))

def test_uut_part2():
    """
    In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
    """
    assert 467835 == sum(find_gear_ratios(sample))


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
        print("part1:", sum(find_part_numbers(f)))
        f.seek(0)
        print("part2:", sum(find_gear_ratios(f)))
