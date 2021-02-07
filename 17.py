#!/usr/bin/env python3

from intcode import intcode

def build_scaffold_map(prog):
        scaffold_map = []
        row = []
        for out in intcode(prog):
            if out == 10:
                if row:
                    scaffold_map.append(row)
                    row = []
            else:
                row.append(chr(out))
        return scaffold_map


def is_intersection(scaffold_map, r, c):
    num_rows = len(scaffold_map)
    num_cols = len(scaffold_map[0])

    # if we're on the outer edge of the map, we can't be an intersection
    if c == 0 or r == 0 or c + 1 == num_cols or r + 1 == num_rows:
        return False

    required_scaffold = [
        scaffold_map[r - 1][c], # above
        scaffold_map[r + 1][c], # below
        scaffold_map[r][c],     # current
        scaffold_map[r][c - 1], # left
        scaffold_map[r][c + 1], # right
    ]

    for expected_scaffold in required_scaffold:
        #  '#' is a scaffold, ^ is us (and on a scaffold)
        if expected_scaffold != '#' and expected_scaffold != '^':
            return False
    return True


def find_intersections(scaffold_map):
    num_rows = len(scaffold_map)
    num_cols = len(scaffold_map[0])
    intersections = []

    for r in range(num_rows):
        for c in range(num_cols):
            if is_intersection(scaffold_map, r, c):
                intersections.append((r, c))
    return intersections

direction_possibilities_by_current_direction = {
    (0, -1): [       # Facing North
        (-1, 0),    # go West
        (1, 0),     # go East
    ],
    (-1, 0): [      # facing West
        (0, 1),     # go South
        (0, -1),    # go North
    ],
    (1, 0): [       # facing East
        (0, -1),    # go North
        (0, 1),     # go South
    ],
    (0, 1): [       # facing South
        (1, 0),     # go East
        (-1, 0),    # go West
    ]
}
def get_new_direction(current_direction, to_turn):
    if to_turn == 'L':
        to_turn = 0
    elif to_turn == 'R':
        to_turn = 1
    new_direction = direction_possibilities_by_current_direction[current_direction][to_turn]
    return new_direction


def exec_instructions(scaffold_map, instructions):
    direction = (0, -1)
    char_for_direction = {
        (1, 0):     '>',
        (-1, 0):    '<',
        (0, -1):     '^',
        (0, 1):     'V',
    }

    pos = [24,0]
    char_at = scaffold_map[pos[1]][pos[0]]
    halted = False
    for inst in instructions:
        if halted:
            break
        char_at = scaffold_map[pos[1]][pos[0]]
        if char_at == '.':
            halted=True
            continue

        if inst in 'LR':
            direction = get_new_direction(direction, inst)
        else:
            times = int(inst)
            for _ in range(times):
                char_at = scaffold_map[pos[1]][pos[0]]
                if char_at == '.':
                    halted = True
                    break
                # off left or right edge
                if pos[0] < 0 or pos[0] > len(scaffold_map[0]):
                    break

                if pos[1] < 0 or pos[1] > len(scaffold_map):
                    break
                scaffold_map[pos[1]][pos[0]] = char_for_direction[direction]
                dc, dr = direction
                pos = [pos[0] + dc, pos[1] + dr]
    scaffold_map[pos[1]][pos[0]] = char_for_direction[direction]

    # print the map
    for row in scaffold_map:
        print(''.join(row))


def find_path(scaffold_map, pos=(24,0)):
    direction = (0, -1)
    path = []

    def move(direction):
        x = pos[0] + direction[0]
        y = pos[1] + direction[1]
        try:
            return scaffold_map[y][x]
        except IndexError:
            return '.'

    def pick_direction(current_direction):
        """
        returns first direction that is a scaffold
        in scaffold_map
        """
        picked_direction, picked_turn = None, None
        possibles = direction_possibilities_by_current_direction[
            current_direction
        ]
        for idx, new_direction in enumerate(possibles):
            if move(new_direction) == '#':
                picked_direction = new_direction
                picked_turn = idx
                break
        return picked_direction, picked_turn

    times_forward = 0
    while True:
        if move(direction) == '#':
            times_forward += 1
            # move in direction
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            continue
        elif times_forward:
            path.append(str(times_forward))
            times_forward = 0

        picked_direction, picked_turn = pick_direction(direction)

        if picked_direction:
            path.append('LR'[picked_turn])
            direction = picked_direction
        else:
            if times_forward:
                path.append(str(times_forward))
            return path


# Tests

def test_find_intersections():
    sample = list(map(list, """
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..
    """.strip().split('\n')))

    intersections = find_intersections(sample)
    assert len(intersections) > 0



def longest_common_prefix(a, b):
    """
    >>> longest_common_prefix('ab', 'abc')
    'ab'
    >>> longest_common_prefix('abcd', 'ab')
    'ab'
    """
    N = min(len(a), len(b))
    for i in range(N):
        if a[i] != b[i]:
            return a[:i]
            break
    return a[:N]


def longest_repeated_subsequence(s, debug=False):
    """
    using suffix array & lcp

    Source: https://www.coursera.org/lecture/cs-algorithms-theory-machines/longest-repeated-substring-hkJBt

    >>> longest_repeated_subsequence('abcab')
    'ab'
    >>> longest_repeated_subsequence('ababc')
    'ab'
    >>> longest_repeated_subsequence('dababc')
    'ab'
    """
    suffixes = [s[i:] for i in range(0, len(s))]
    suffixes.sort()

    lrs = ''
    for idx, suffix in enumerate(suffixes[:-1]):
        possible = longest_common_prefix(suffix, suffixes[idx + 1])
        if len(possible) >= len(lrs) and len(possible) > 1:
            if debug and possible != lrs:
                print(possible, file=sys.stderr)
            lrs = possible
    return lrs


def find_subsequence(sequence, subsequence):
    result = []
    len_of_seq = len(sequence)
    for i in range(len(sequence)):
        found = True
        for j in range(len(subsequence)):
            if i + j >= len_of_seq or sequence[i+j] != subsequence[j]:
                found = False
                break
        if found:
            result.append(i)
    return result

if __name__ == "__main__":
    with open('input17.txt', 'rt') as f:
        prog = [int(t) for t in f.read().split(',')]
        scaffold_map = build_scaffold_map(prog)

        intersections = find_intersections(scaffold_map)

        part1 = 0
        for r, c in intersections:
            part1 += r * c
        print("part1:", part1)

        path = find_path(scaffold_map)
        print("path:", ' '.join(path))

        # path = "L 10 L 8 R 8 L 8 R 6 L 10 L 8 R 8 L 8 R 6 R 6 R 8 R 8 R 6 R 6 L 8 L 10".split()
        # part 2
        exec_instructions(
            scaffold_map,
            path
        )
    seq = path

    print("len(sequence):", len(seq))
    lrs = longest_repeated_subsequence(seq)
    print("longest_repeated_subsequence(sequence):", lrs)
    print("len(lrs):", len(lrs))
    lrs_of_lrs = longest_repeated_subsequence(lrs)
    print("longest_repeated_subsequence(lrs):", lrs_of_lrs)
    print("len:", len(lrs_of_lrs))
    lrs_of_lrs_of_lrs = longest_repeated_subsequence(lrs_of_lrs)
    print("longest_repeated_subsequence(lrs_of_lrs_of_lrs):", lrs_of_lrs_of_lrs)
    print("len:", len(lrs_of_lrs_of_lrs))



    print("find_subsequence(lrs):", find_subsequence(seq, lrs))
    print("find_subsequence(seq, lrs_of_lrs_of_lrs):", find_subsequence(seq, lrs_of_lrs_of_lrs))

    C = ['R', '6', 'R', '8', 'R', '8']
