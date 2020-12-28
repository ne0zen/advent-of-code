#!/usr/bin/env python3


def get_param_from_prog(param_num, prog, ip):
    # determine param modes
    current = prog[ip]
    param1_mode = current % 1000 // 100
    param2_mode = current % 10000 // 1000
    param3_mode = current // 10000
    assert param_num < 3

    # print("modes:", [param1_mode, param2_mode, param3_mode], ' ', end='')
    raw_param = prog[ip + param_num]
    param_mode = locals()[f'param{param_num}_mode']

    # 1 is "value"
    result = None
    if 0 == param_mode:         # position in prog
        result = prog[raw_param]
    elif 1 == param_mode:       # value
        result = raw_param
    else:
        raise Exception(f"Unknown Param mode {param_mode} @ {ip}: {current}")

    # print(f"{param_num=}, {param_mode=}, {result=}")
    return result

num_params_by_opcode = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
}
def intcode(prog, input_list=None):
    ip = 0

    # so lower calls don't have to pass prog and ip
    def param(param_num):
        return get_param_from_prog(param_num, prog, ip)

    while (current := prog[ip]):
        opcode = current % 100
        # default for next_ip (adding 1 to skip opcode itself)
        next_ip = ip + 1 + num_params_by_opcode.get(opcode, 0)
        if opcode == 1:
            lhs = param(1)
            rhs = param(2)
            param3 = prog[ip + 3]
            assert param3 >= 0, "ADD: outaddr should be >= 0"
            prog[param3] = lhs + rhs
            # print("ADD: ", prog[ip:ip + 4], f"prog[{param3}] = {lhs} + {rhs} = {lhs + rhs}")
        elif opcode == 2:
            lhs = param(1)
            rhs = param(2)
            param3 = prog[ip + 3]
            assert param3 >= 0, "MUL: param3 should be >= 0"
            prog[param3] = lhs * rhs
            # print("MULT: ", prog[ip:ip + 4], f"prog[{param3}] = {lhs} * {rhs} = {lhs * rhs}")
        elif opcode == 3:
            # print("IN:", prog[ip:ip + 2])
            if input_list:
                read =  input_list.pop(0)
            else:
                read = input("input? ")
            prog[prog[ip + 1]] = int(read)
        elif opcode == 4:
            # print("OUT:", prog[ip:ip + 2])
            to_out = param(1)
            print(to_out)
        elif opcode == 5: # jmp if nonzero
            if param(1) != 0:
                next_ip = param(2)
        elif opcode == 6: # jmp if zero
            if param(1) == 0:
                next_ip = param(2)
        elif opcode == 7: # prog[param3] = 1 if first < second else 0
            first = param(1)
            second = param(2)
            prog[prog[ip + 3]] = 1 if first < second else 0
        elif opcode == 8: # prog[param3] = 1 if first == second else 0
            first = param(1)
            second = param(2)
            prog[prog[ip + 3]] = 1 if first == second else 0
        elif opcode == 99:
            print(f"(HALT @ {ip})")
            break
        else:
            raise Exception(f"Unknown opcode: {opcode} @ {ip}: {current}")
        ip = next_ip
    return prog


if __name__ == '__main__':
    with open('input05.txt', 'rt') as f:
        orig_prog = [int(e) for e in f.read().split(',')]
        # print("len(orig_prog):", len(orig_prog))
        print("part1:")
        intcode(orig_prog.copy(), input_list=[1])
        print("part2:")
        intcode(orig_prog.copy(), input_list=[5])

        # run part2 after result of part1
        # prog = [int(e) for e in f.read().split(',')]
        # print("len(prog):", len(prog))
        # print("part1:")
        # intcode(prog, input_list=[1])
        # print("part2:")
        # intcode(prog, input_list=[5])


# Tests
def test_pos_add():
    # adds prog[0] + prog[0] and stores @ prog[0]
    prog = [1,0,0,0,99]
    assert [2,0,0,0,99] == intcode(prog)


def test_pos_mult():
    prog = [2,3,0,3,99]
    expected = [2,3,0,6,99]
    assert expected == intcode(prog)


def test3():
    prog = [2,4,4,5,99,0]
    expected = [2,4,4,5,99,9801]
    assert expected == intcode(prog)


def test4():
    prog = [1,1,1,4,99,5,6,0,99]
    expected = [30,1,1,4,2,5,6,0,99]
    assert expected == intcode(prog)

def test_value_param1():
    prog = [
        101, 2, 4, 5,
        99,
        0
    ]
    # should store 2 + prog[4] (99) = 101 into 5
    expected = prog.copy()
    expected[5] = 101
    assert expected == intcode(prog)

def test_value_param2():
    prog = [
        1001, 2, 4, 5,
        99,
        0
    ]
    # should store prog[2] (4) + 4 = 8 into 5
    expected = prog.copy()
    expected[5] = 8
    assert expected == intcode(prog)

def test_input():
    prog = [3, 3, 99, 0]
    input_list = [42]
    assert [3, 3, 99, input_list[0]] == intcode(prog, input_list=input_list), """
        should set 3 to input (42)""".strip()
    assert len(input_list) == 0, "should read all input"

