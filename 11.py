#!/usr/bin/env python3

# part1
painted_white = set([])
# part2
painted_white = set([(0, 0)])


def get_param_from_prog(param_num, prog, ip, relative_base):
    # determine param modes
    current = prog[ip]
    param1_mode = current % 1000 // 100
    param2_mode = current % 10000 // 1000
    param3_mode = current // 10000
    assert param_num < 3

    raw_param = prog[ip + param_num]
    param_mode = locals()[f'param{param_num}_mode']

    result = None
    if 0 == param_mode:         # position in prog
        result = prog[raw_param]
    elif 1 == param_mode:       # value
        result = raw_param
    elif 2 == param_mode:
        result = prog[raw_param + relative_base]
    else:
        raise Exception(f"Unknown Param mode {param_mode} @ {ip}: {current}")

    # print(f"{param_num=}, {param_mode=}, {result=}")
    return result


NUM_PARAMS_BY_OPCODE = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 1,
    99: 1,
}
def intcode(orig_prog, input_list=None, trace=False):
    ip = 0
    output = []
    relative_base = 0

    prog = [0] * 65536
    # copy orig_prog to prog
    for i, value in enumerate(orig_prog):
        prog[i] = value

    # so lower calls don't have to pass prog and ip
    def param(param_num):
        return get_param_from_prog(param_num, prog, ip, relative_base)

    def update_memory(address, value):
        if current > 20000:
            address += relative_base
        assert address >= 0, "dest address should be zero"
        prog[address] = value

    while (current := prog[ip]):
        opcode = current % 100
        # default for next_ip (adding 1 to skip opcode itself)
        next_ip = ip + 1 + NUM_PARAMS_BY_OPCODE.get(opcode, 0)

        if trace:
            instruction_size = 1 + NUM_PARAMS_BY_OPCODE.get(opcode, 0)
            full_instruction = prog[ip:ip + instruction_size]
            print(f"{ip:04d}: {full_instruction}")

        if opcode == 1:
            lhs = param(1)
            rhs = param(2)
            param3 = prog[ip + 3]
            update_memory(param3, lhs + rhs)
            # print("ADD: ", prog[ip:ip + 4], f"prog[{param3}] = {lhs} + {rhs} = {lhs + rhs}")
        elif opcode == 2:
            lhs = param(1)
            rhs = param(2)
            param3 = prog[ip + 3]
            update_memory(param3, lhs * rhs)
            # print("MULT: ", prog[ip:ip + 4], f"prog[{param3}] = {lhs} * {rhs} = {lhs * rhs}")
        elif opcode == 3:
            if input_list:
                read_value = input_list.pop(0)
            else:
                read_value = (yield)
            if read_value is None:
                raise Exception("hell")
            if current > 200:
                prog[prog[ip + 1] + relative_base] = int(read_value)
            else:
                prog[prog[ip + 1]] = int(read_value)
        elif opcode == 4:
            to_out = param(1)
            yield to_out
        elif opcode == 5: # jmp if nonzero
            if param(1) != 0:
                next_ip = param(2)
        elif opcode == 6: # jmp if zero
            if param(1) == 0:
                next_ip = param(2)
        elif opcode == 7: # prog[param3] = 1 if first < second else 0
            first = param(1)
            second = param(2)
            update_memory(prog[ip + 3], 1 if first < second else 0)
        elif opcode == 8: # prog[param3] = 1 if first == second else 0
            first = param(1)
            second = param(2)
            update_memory(prog[ip + 3], 1 if first == second else 0)
        elif opcode == 9:
            relative_base += param(1)
        elif opcode == 99:
            break
        else:
            raise Exception(f"Unknown opcode: {opcode} @ {ip}: {current}")
        ip = next_ip


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

def paint(painted_white, painted_black):
    painted = painted_white | painted_black
    min_x = min(x for x, y in painted)
    max_x = max(x for x, y in painted)

    min_y = min(y for x, y in painted)
    max_y = max(y for x, y in painted)


    x_range = max_x - min_x
    y_range = max_y - min_y

    # print(f"{min_x=} {max_x=} {min_y=} {max_y=} {x_range=} {y_range=}")
    # for y in range(min_y, max_y + 1):
    # flip painting vertically
    for y in range(max_y + 1, min_y - 1, -1):
        adj_y = y + min_y
        adj_y = y
        for x in range(min_x, max_x + 1):
            adj_x = x + min_x
            adj_x = x
            # print("adj_x", adj_x, "adj_y", adj_y)
            if (adj_x, adj_y) in painted_white:
                draw = '#'
            else:
                draw = ' '
            print(draw, end='')
        print()

print("len(painted):", len(painted))
print("painting")
paint(painted_white, painted_black)
