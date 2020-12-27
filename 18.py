#!/usr/bin/env python3
"""
For example, the steps to evaluate the expression
1 + 2 * 3 + 4 * 5 + 6 are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71

Parentheses can override this order; for example, here is what
happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51

Here are a few more examples:

    2 * 3 + (4 * 5) becomes 26.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

Before you can help with the homework, you need to understand it
yourself. Evaluate the expression on each line of the homework; what
is the sum of the resulting values?
"""

import itertools


def yield_tokens(string):
    token = ''
    for c in string:
        if c.isspace():
            if token:
                yield token
                token = ''
        elif c.isnumeric():
            token += c
        else:  # handle things like ( and )
            if token:
                yield token
                token = ''
            yield c
    # the final token after string exhausted
    if token:
        yield token


ALLOWED_OPERATORS = set('+-*/')

def handle_tokens1(token_iter, in_parens=False):
    last_op = '+'
    total_so_far = 0

    for token in token_iter:
        # print("in_parens:", in_parens, "token:", token)
        if token in ALLOWED_OPERATORS:
            # handle new operator
            last_op = token
        elif token == '(':
            token = str(handle_tokens1(token_iter, in_parens=True))
        elif in_parens and token == ')':
            return total_so_far  # end earlier recursion
        elif token == ')' and not in_parens:
            raise Exception("unmatched )")
        if token.isnumeric():
            # do math
            lhs = total_so_far
            rhs = int(token)
            new_total = None
            if last_op == '+':
                new_total = lhs + rhs
            elif last_op == '-':
                new_total = lhs - rhs
            elif last_op == '*':
                new_total = lhs * rhs
            elif last_op == '/':
                new_total = lhs / rhs
            total_so_far = new_total
    return total_so_far


def parenthesize_expression(token_iter):
    """
    parenthesizes expression taking custom operator precedence into account

    Algorithm modified from that used in an early FORTRAN 1 compiler
    see: Padua, David (2000). "The Fortran I Compiler"
    """
    yield from '(('
    for token in token_iter:
        if token in '+-':    # prioritizes +- over */ here be the odd
            yield from ')'
            yield token
            yield from '('
        elif token in '*/':
            yield from '))'
            yield token
            yield from '(('
        elif token == '(':
            # add two parens to each left paren
            yield from '(('
        elif token == ')':
            # add two parens to each left paren
            yield from '))'
        elif token.isnumeric():
            yield token
        else:
            raise Exception(f"Unknown token: {token}")
    yield from '))'


def weird_math1(string):
    token_iter = yield_tokens(string)
    total_so_far = handle_tokens1(token_iter)
    return total_so_far


def weird_math2(string):
    # 1 + 2 * 3 + 4 * 5 + 6
    #   3   * 3 + 4 * 5 + 6
    #   3   *   7   * 5 + 6
    #   3   *   7   *  11
    #      21       *  11
    #          231
    token_iter = yield_tokens(string)
    parenthesized_iter = parenthesize_expression(token_iter)
    total_so_far = handle_tokens1(parenthesized_iter)

    return total_so_far

if __name__ == "__main__":
    with open('input18.txt', 'rt') as f:
        part1 = 0
        for line in f:
            part1 += weird_math1(line)
        print("part1:", part1)

    with open('input18.txt', 'rt') as f:
        part2 = 0
        for line in f:
            part2 += weird_math2(line)
        print("part2:", part2)


# Test

def test_part1_no_parens():
    #  1 + 2 * 3 + 4 * 5 + 6
    #   3   * 3 + 4 * 5 + 6
    #       9   + 4 * 5 + 6
    #          13   * 5 + 6
    #              65   + 6
    #                  71
    assert 71 == weird_math1("1 + 2 * 3 + 4 * 5 + 6")


def test_part1_with_parens():
    #  1 + (2 * 3) + (4 * (5 + 6))
    #  1 +    6    + (4 * (5 + 6))
    #       7      + (4 * (5 + 6))
    #       7      + (4 *   11   )
    #       7      +     44
    #              51
    assert 51 == weird_math1("1 + (2 * 3) + (4 * (5 + 6))")


def test_part1_moar():
    cases = """
    1 + 2 * 3 + 4 * 5 + 6 becomes 71
    2 * 3 + (4 * 5) becomes 26
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632
    """.strip().split('\n')

    for case in cases:
        case = case.strip()
        if not case: continue
        math, _, expected = case.rpartition(' becomes ')
        assert int(expected) == weird_math1(math)


def test_part2_no_parens():
    assert 231 == weird_math2("1 + 2 * 3 + 4 * 5 + 6")


def test_part2_regression():
    assert 51 == weird_math2("1 + (2 * 3) + (4 * (5 + 6))")


def test_part2_moar():
    cases = """
    1 + (2 * 3) + (4 * (5 + 6)) becomes 51
    2 * 3 + (4 * 5) becomes 46
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340
    """.strip().split('\n')

    for case in cases:
        case = case.strip()
        if not case: continue
        math, _, expected = case.rpartition(' becomes ')
        assert int(expected) == weird_math2(math)
