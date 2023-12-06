#!/usr/bin/env python3


import sys


DEBUG = False


def prnt(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs, file=sys.stderr, flush=True)

class Almanac:

    @staticmethod
    def parse_seeds(data_iter):
        # parse seeds
        _, _, seed_str = next(data_iter).partition(': ')
        return list(map(int,seed_str.split()))

    @staticmethod
    def from_data(data):
        data_iter = iter(data)
        self = Almanac()
        self.seeds = Almanac.parse_seeds(data_iter)

        map_name = None

        self.map_by_name = {}
        try:
            while line := next(data_iter):
                line = line.strip()

                if line.endswith(' map:'):
                    map_name, _ = line.split()
                    self.map_by_name[map_name] = {}
                    prnt(f"parsing map for {map_name}...", end='')

                elif map_name and line:
                    # parse lines into map
                    dest_start, src_start, range_len = map(int, line.split())
                    # print(dest_start, range_len)
                    src_end = src_start + range_len
                    self.map_by_name[map_name][
                        range(src_start, src_end)
                    ] = dest_start

                elif not line:
                    map_name = None
                    prnt(f"done")

                else:
                    pass
        except StopIteration:  # no more to parse
            pass
        return self


    def value_in_map_for_id(self, map_name, src_id):
        matching_range = None
        needed_map = self.map_by_name[map_name]
        for possible_range in needed_map.keys():
            if src_id in possible_range:
                matching_range = possible_range
                break
        if matching_range:
            dest_start = needed_map[matching_range]
            offset = src_id - matching_range.start
            return dest_start + offset
        else:
            return src_id


def part1(data):
    result = []
    almanac = Almanac.from_data(data)

    def seed_id_to_location_id(seed_id):
        prnt(f"{seed_id=}")
        map_names = """
        seed-to-soil
        soil-to-fertilizer
        fertilizer-to-water
        water-to-light
        light-to-temperature
        temperature-to-humidity
        humidity-to-location
        """.strip().split()

        current_id = seed_id
        for map_name in map_names:
            current_id = almanac.value_in_map_for_id(map_name, current_id)
            prnt(f"{current_id}")

        return current_id


    return min(seed_id_to_location_id(seed_id) for seed_id in almanac.seeds)


def part2(data):
    result = []
    return result



##  Tests


import io     # for StringIO
import pytest # for decorator

sample = io.StringIO("""
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".strip())

def test_uut_part1():
    """
    """
    assert 35 == part1(sample)

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
    # sample2.seek(0)


if __name__ == "__main__":
    import os
    # extract number
    FNAME = 'input' + os.path.splitext(os.path.basename(__file__))[0] + '.txt'
    print("FNAME:", FNAME)
    with open(FNAME, 'rt') as f:
        print("part1:", part1(f))
        f.seek(0)
        print("part2:", part2(f))
