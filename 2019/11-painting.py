#!/usr/bin/env python3

# part1
painted_white = set([])
# part2
# painted_white = set([(0, 0)])


from intcode import intcode


direction_possibilities_by_current_direction = {
    (0, 1): [       # Facing North
        (-1, 0),    # go West
        (1, 0),     # go East
    ],
    (-1, 0): [      # facing West
        (0, -1),    # go South
        (0, 1),     # go North
    ],
    (1, 0): [       # facing East
        (0, 1),     # go North
        (0, -1),    # go South
    ],
    (0, -1): [      # facing South
        (1, 0),     # go East
        (-1, 0),    # go West
    ]
}
def get_new_direction(current_direction, to_turn):
    new_direction = direction_possibilities_by_current_direction[current_direction][to_turn]


with open('input11.txt', 'rt') as f:
    prog = [int(e) for e in f.read().split(',')]
# prime the robot
robot = intcode(prog)
next(robot)

x = 0
y = 0
painted = set([])
painted_black = set([])


direction = (0, 1)
while True:
    # figure out next input
    pos = (x, y)
    # provide 0 if the robot is over a black panel or 1 if the robot is over a white panel
    if pos in painted_white:
        current_tile_color = 'white'
        to_send = 1
    elif pos in painted_black:
        current_tile_color = 'black'
        to_send = 0
    elif pos not in painted:
        current_tile_color = 'black'
        to_send = 0
    else:
        raise "hell"
    # send it
    paint_it = robot.send(to_send)
    assert paint_it in [0, 1]

    # 0 means to paint the panel black, and 1 means to paint the panel white.
    if 0 == paint_it:
        painted_white.discard(pos)
        painted_black.add(pos)
    elif 1 == paint_it:
        painted_black.discard(pos)
        painted_white.add(pos)
    else:
        raise Exception(f"Unknown color to paint: {paint_it}")
    # track that we painted it any color at all
    painted.add(pos)

    to_turn = next(robot)
    assert to_turn in [0, 1], f"{to_turn=} not in [0, 1]"
    new_direction = direction_possibilities_by_current_direction[direction][to_turn]
    # print(f"{pos=}\t{direction=}\t{current_tile_color=}\t{paint_it=}\t{to_turn=}\t{new_direction=}")
    # perform the turn
    direction = new_direction
    dx, dy = direction
    # After the robot turns, it should always move forward exactly one panel. The robot starts facing up.
    x += dx
    y += dy
    try:
        robot.send(None)
    except StopIteration:
        break

import itertools
from matplotlib import pyplot as plt
def paint(painted_white, painted_black):
    painted = painted_white | painted_black
    min_x = min(x for x, _ in painted)
    max_x = max(x for x, _ in painted)

    min_y = min(y for _, y in painted)
    max_y = max(y for _, y in painted)

    x_range = max_x - min_x
    y_range = max_y - min_y

    # print(f"{min_x=} {max_x=} {min_y=} {max_y=} {x_range=} {y_range=}")
    for y in range(min_y, max_y + 1):
    # flip painting vertically
    # for y in range(max_y + 1, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            if (x, y) in painted_white:
                draw = '#'
            else:
                draw = ' '
            print(draw, end='')
        print()
    # exes = itertools.chain(
    #     (t[0] for t in painted_white),
    #     # (t[0] for t in painted_black)
    # )
    # whys = itertools.chain(
    #     (t[1] for t in painted_white),
    #     # (t[1] for t in painted_black)
    # )
    # colors = itertools.chain(
    #     ('#ffff00' for t in painted_white),
    #     # ('#000000' for t in painted_black)
    # )
    # thing = plt.scatter(x=list(exes), y=list(whys), c=list(colors))
    # plt.show()

print("len(painted):", len(painted))
print("painting")
paint(painted_white, painted_black)
