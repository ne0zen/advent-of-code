#!/usr/bin/env python3


def process(raw):
    result = []
    for line in raw:
        line = line.strip()
        if not line:
            continue
        item = int(line)
        result.append(item)
    return result


def count_increases(data):
    """
    count number of increases from one element to the next
    """
    last = data[0]
    result = 0

    for item in data[1:]:
        if item > last:
            result += 1
        last = item
    return result


import collections
def count_window_increases(data):
    """
    count number of increases in sum of sliding window (size 3)
    window at each stage:
    199  A
    200  A B
    208  A B C
    210    B C D
    200  E   C D
    207  E F   D
    240  E F G
    269    F G H
    260      G H
    263        H
    """
    window = collections.deque(data[:3], maxlen=3)
    last_sum = sum(window)
    sums = [last_sum]
    result = 0

    for item in data[3:]:
        window.append(item)
        current_sum = sum(window)
        sums.append(current_sum)
        if current_sum > last_sum:
            result += 1
        last_sum = sum(window)

    return result


import io
sample1 = io.StringIO("""
199
200
208
210
200
207
240
269
260
263
""".strip())
def test1():
    sample1.seek(0)
    assert 7 == count_increases(process(sample1))

def test2():
    sample1.seek(0)
    assert 5 == count_window_increases(process(sample1))


if __name__ == '__main__':
    with open('input01.txt', 'rt') as f:
        part1 = count_increases(process(f))
        print("part1:", part1)

    with open('input01.txt', 'rt') as f:
        part2 = count_window_increases(process(f))
        print("part2:", part2)
