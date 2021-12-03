#!/usr/bin/env python3


def power_consumption(data):
    gamma = ''
    epsilon = ''

    line_len = len(next(data).strip())

    for bitpos in range(line_len):
        bitpos_data = ''.join(line.strip()[bitpos] for line in data)
        num1s = sum(1 if i == '1' else 0 for i in bitpos_data)
        num0s = sum(1 if i == '0' else 0 for i in bitpos_data)
        # print(f"{num1s=} {num0s=}")
        gamma += '1' if num1s > num0s else '0'
        epsilon += '1' if num1s < num0s else '0'
        data.seek(0)
    # print("gamma:", gamma)
    # print("epsilon:", epsilon)

    return int(gamma, 2), int(epsilon, 2)


def life_support_rating(data):
    data = [line.strip() for line in data]

    line_len = len(data[0])

    def oxygen_rate_bit_criteria(num0s, num1s):
        return '1' if num1s >= num0s else '0'

    def co2_scrubber_bit_criteria(num0s, num1s):
        return '0' if num0s <= num1s else '1'

    def determine_rate(data, bit_criteria):
        data = data.copy()
        for bitpos in range(line_len):
            if len(data) == 1:
                break
            bitpos_data = [line[bitpos] for line in data]
            num1s = bitpos_data.count('1')
            num0s = bitpos_data.count('0')
            # print(f"{num1s=} {num0s=}")

            bit = bit_criteria(num0s, num1s)
            data = list(filter(
                lambda row: row[bitpos] == bit,
                data
            ))
            # print(f"{bitpos=} {data=}")
        return data[0]

    g_rate = determine_rate(data, oxygen_rate_bit_criteria)
    s_rate = determine_rate(data, co2_scrubber_bit_criteria)

    return int(g_rate, 2), int(s_rate, 2)


import io     # for StringIO
import pytest # for decorator

sample = io.StringIO("""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".strip())
def test_uut_part1():
    g, e = power_consumption(sample)
    # the gamma rate is the binary number 10110, or 22 in decimal.
    # the epsilon rate is 01001, or 9 in decimal
    # the power consumption, 198.
    assert 22 == g
    assert 9 == e
    assert 198 == g * e

def test_uut_part2():
    generator_rate, scrubber_rate = life_support_rating(sample)
    assert 10 == scrubber_rate
    assert 23 == generator_rate
    assert 230 == generator_rate * scrubber_rate

@pytest.fixture(autouse=True)
def run_around_tests():
    # run before
    yield
    # run after
    sample.seek(0)


if __name__ == "__main__":
    with open('input03.txt', 'rt') as f:
        g, e = power_consumption(f)
        print("part1:", g * e)
        f.seek(0)
        g, s = life_support_rating(f)
        print("part2:", g * s)
