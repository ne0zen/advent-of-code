#!/usr/bin/env python3

import copy
import collections
from dataclasses import dataclass
import functools
import operator

@dataclass(repr=False)
class Node():
    val: int = 0
    x: int = 0
    y: int = 0

    @property
    def flashed(self):
        return self.val > 9

    @property
    def coord(self):
        return (self.x, self.y)

    def reset(self):
        """
        call me after you've covered the whole board
        """
        self.val = 0

    def increment(self):
        self.val += 1

    def __repr__(self):
    #     return f"{self.val} @ ({self.x}, {self.y})"
        return f"<Node {self.val}>"


class Board():

    def __init__(self, raw_data):
        self.grid = [
            [
                Node(int(c), x, y)
                for x, c in enumerate(line.strip())
            ]
            for y, line in enumerate(raw_data.strip().split('\n'))
        ]
        self.num_flashes = 0
        self.steps = 0


    def all_around(self, x, y):
        for coord in [
            (x - 1, y),     # left
            (x - 1, y - 1), # UL
            (x, y - 1),  # up
            (x + 1, y - 1), # UR
            (x + 1, y),  # right
            (x, y + 1),  # down
            (x - 1, y + 1), # DL
            (x + 1, y + 1), # DR

        ]:
            yield self.at(*coord)

    def at(self, x, y):
        x_len = len(self.grid[0])
        y_len = len(self.grid)
        outside_board = not 0 <= x < x_len or not 0 <= y < y_len
        if outside_board:
            return Node()
        else:
            # returns height @ x, y
            return self.grid[y][x]

    def dump(self, *args, **kwargs):
        print('\033')
        print(*args, **kwargs)
        print(self)
        print("self.num_flashes:", self.num_flashes)

    def __str__(self):
        # for line in self.grid:
        #     print(''.join(str(node.val) for node in line))
        return '\n'.join(
            ' '.join(
                f"{'*' if node.flashed else ' '}{node.val:2}{'*' if node.flashed else ' '}"
                # f"{'*' if node.flashed else ' '}  {'*' if node.flashed else ' '}"
                for node in line
            )
            for line in self.grid
        )

    def run(self, num_steps):
        for _ in range(num_steps):
            self.advance()

    def advance(self):
        self.steps += 1
        self.flashed = set()
        flash_queue = collections.deque()

        # increment everything
        newly_flashed = set()
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                node.increment()

                if node.flashed and node.coord not in self.flashed:
                    newly_flashed.add(node.coord)
        flash_queue.extend(newly_flashed)

        assert len(flash_queue) == len(set(flash_queue))
        # account for flashes
        while flash_queue:

            flashed_coord = flash_queue.popleft()
            self.flashed.add(flashed_coord)

            for node in self.all_around(*flashed_coord):
                node.increment()

                if (node.flashed
                    and node.coord not in self.flashed
                    and node.coord not in flash_queue
                ):
                    flash_queue.append(node.coord)

        self.num_flashes += len(self.flashed)

        for coord in self.flashed:
            node = self.at(*coord)
            node.reset()
        # [node.reset() for node in map(lambda coord: self.at(*coord), flashed)]
        return self.flashed


import pytest


def test_flash():
    board = Board("""
    11111
    19991
    19191
    19991
    11111
    """)

    board.advance()
    print("after:")
    print(board)
    expected_grid = Board("""
    34543
    40004
    50005
    40004
    34543
    """)
    expected_grid.num_flashes = 9

    assert expected_grid.grid == board.grid
    assert expected_grid.num_flashes == board.num_flashes


@pytest.fixture()
def sample():
    return parse(
"""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
)


if __name__ == "__main__":
    with open('input11.txt', 'rt') as f:
        board = Board(f.read())
    while board.steps < 100:
        print("\033c", end='')
        flashed_this_round = len(board.advance())
        # input()
    print("part1:", board.num_flashes)


    while True:
        flashed_this_round = len(board.advance())
        if 100 == flashed_this_round:
            print("part2:", board.steps)
            break
