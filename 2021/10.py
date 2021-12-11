#!/usr/bin/env python3


import collections
import functools
import operator


def parse(raw_data):
    return [
        line.strip()
        for line in raw_data
    ]


CLOSE_BY_OPEN = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
def find_corrupted_lines(data):
    corrupted_lines = []
    stack = collections.deque()

    for line in data:
        is_corrupt = False
        for i, char in enumerate(line):
            try:
                acceptable_char = CLOSE_BY_OPEN.get(stack[-1], None)
            except IndexError:
                acceptable_char = None
            if char in '([{<':
                stack.append(char)
            elif char == acceptable_char:
                stack.pop()
            else:
                is_corrupt = True
                break

        if is_corrupt:
            # print("line, char:", line, char)
            yield (line, char)
            stack.clear()


def score_corrupted_lines(data):
    SCORE_BY_ILLEGAL_CHAR = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    return sum(
        SCORE_BY_ILLEGAL_CHAR.get(unexpected_char, 0)
        for _, unexpected_char in find_corrupted_lines(data)
    )


def find_incomplete_lines(data):
    stack = collections.deque()

    for line in data:
        line = line.strip()
        for i, char in enumerate(line):
            try:
                acceptable_char = CLOSE_BY_OPEN.get(stack[-1], None)
            except IndexError:
                acceptable_char = None
            if char in '([{<':
                stack.append(char)
            elif char == acceptable_char:
                stack.pop()
            else:
                # corrupt
                # print(line)
                # print(f"{'-' * i}^  Expected: {acceptable_char}, Found: {char}")
                stack.clear()
                break

        if len(stack):
            completion = ''.join(CLOSE_BY_OPEN[char] for char in reversed(stack))
            yield (line, completion, score(completion))
            stack.clear()
        else:
            # print("balanced:", line)
            pass


def score(completion):
    SCORE_BY_CHAR = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    result = 0
    for char in completion:
        result *= 5
        result += SCORE_BY_CHAR.get(char, 0)
    return result


import pytest

@pytest.fixture()
def sample():
    return parse(
"""
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip().split('\n')
)


@pytest.mark.parametrize('row',
"""
{([(<{}[<>[]}>{[]{[(<()>    }
[[<[([]))<([[{}[[()]]]      )
[{[{({}]{}}([{[{{{}}([]     ]
[<(<(<(<{}))><([]([]()      )
<{([([[(<>()){}]>(<<{{      >
""".strip().split('\n'), ids=lambda r: r.split(None, 1)[0])
def test_find_corrupted_lines(row, sample):
    expected_line, expected_char = row.strip().split()
    assert (expected_line, expected_char) in find_corrupted_lines(sample)


INCOMPLETE__COMPLETION__SCORES = """
[({(<(())[]>[[{[]{<()<>>    }}]])})]    288957
[(()[<>])]({[<{<<[]>>(      )}>]})      5566
(((({<>}<{<{<>}{[]{[]{}     }}>}>))))   1480781
{<[[]]>}<{[{[{[]{()[[[]     ]]}}]}]}>   995444
<{([{{}}[<[[[<>{}]]]>[]]    ])}>        294
""".strip().split('\n')


@pytest.mark.parametrize(
    'row',
    INCOMPLETE__COMPLETION__SCORES,
    ids=lambda r: r.split(None, 1)[0]
)
def test_find_incomplete_lines_completes_and_scores(row, sample):
    expected_line, expected_completion, expected_score = row.strip().split()

    found = False
    for line, completion, score in find_incomplete_lines(sample):
        if expected_line == line:
            assert expected_completion == completion
            assert int(expected_score) == score
            found = True
            break
    assert found, f'{expected_line} not found'


if __name__ == "__main__":
    with open('input10.txt', 'rt') as f:
        data = parse(f)
    print('part1:', score_corrupted_lines(data))
    scores = sorted(r[-1] for r in find_incomplete_lines(data))
    # print("len(scores):", len(scores))
    assert len(scores) % 2 == 1, "should always have an odd number of scores"
    middle_pos = len(scores) // 2
    # print("len(scores):", len(scores), "middle_pos:", middle_pos)
    middle_score = scores[middle_pos]
    print('part2:', middle_score)

    # WRONG answers
    # 17704191719
    # 17795493347
