#!/usr/bin/env python3

import itertools

def find_xmas_vuln(data, preamble_size=25):
    window = list(int(v) for v in data[:preamble_size])

    for v in data[preamble_size:]:
        v = int(v)
        found = False or len(window) < 2
        for i1, i2 in itertools.permutations(window, 2):
            if i1 + i2 == v:
                found = True
                break
        if found:
            window.append(v)
            if len(window) > preamble_size:
                window.pop(0)
        else:
            return v

def find_int_range(raw_data, preamble_size=25):
    vuln = find_xmas_vuln(raw_data, preamble_size)
    data = [int(v) for v in raw_data]

    i = 0
    while i < len(data):
        size = 0
        while True:
            size += 1
            stuff = data[i:i+size]
            if ((sum_stuff := sum(stuff)) >= vuln):
                break
        if sum_stuff == vuln:
            return stuff
        i += 1



if __name__ == "__main__":
    with open('input09.txt', 'rt') as f:
        data = f.read().split()
    print("part1:", find_xmas_vuln(data))
    part2 = find_int_range(data)
    print("min(part2) + max(part2):", min(part2) + max(part2))

import io
sample = """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
""".strip().split()

def test_find_xmas_vuln():
    assert 127 == find_xmas_vuln(sample, preamble_size=5)

def test_find_int_range():
    part2 = find_int_range(sample, preamble_size=5)
    assert 62 == min(part2) + max(part2)

