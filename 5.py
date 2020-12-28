#!/usr/bin/env python3

def intcode(prog, input_list=None):
    ip = 0

    while (current := prog[ip]) != 99:
        opcode = current % 100
        # determine param modes
        # 0 is "position"
        # 1 is "value"
        param1_mode = current % 1000 // 100
        param2_mode = current % 10000 // 1000
        param3_mode = current // 10000
        # print("IP:", ip, end=' ')
        # print("modes:", [param1_mode, param2_mode, param3_mode], ' ', end='')
        if opcode == 1:
            # print("ADD: ", prog[ip:ip + 4])
            param1, param2, param3 = prog[ip+1:ip+4]
            assert 0 == param3_mode, "param3 mode should be zero in an add"
            assert param3 >= 0, "add: outaddr should be >= 0"
            # adjust lhs, rhs, outaddr based on param modes
            if param1_mode == 0:   # position
                lhs = prog[param1]
            elif param1_mode == 1: # value
                lhs = param1
            else:
                raise Exception(f"Unknown Param mode {param1_mode} @ {ip}: {current}")
            if param2_mode == 0:   # position
                rhs = prog[param2]
            elif param2_mode == 1: # value
                rhs = param2
            else:
                raise Exception(f"Unknown Param mode {param2_mode} @ {ip}: {current}")
            prog[param3] = lhs + rhs
            ip += 4
            # print("ADD: ", prog[ip:ip + 4], f"prog[{param3}] = {lhs} + {rhs} = {lhs + rhs}")
        elif opcode == 2:
            param1, param2, param3 = prog[ip + 1:ip + 4]
            assert 0 == param3_mode, "mut: param3 mode should be zero"
            assert param3 >= 0, "mult: outaddr should be >= 0"
            # adjust lhs, rhs, outaddr based on param modes
            if param1_mode == 0:   # position
                lhs = prog[param1]
            elif param1_mode == 1: # value
                lhs = param1
            else:
                raise Exception(f"Unknown Param mode {param1_mode} @ {ip}: {current}")
            if param2_mode == 0:   # position
                rhs = prog[param2]
            elif param2_mode == 1: # value
                rhs = param2
            else:
                raise Exception(f"Unknown Param mode {param2_mode} @ {ip}: {current}")
            prog[param3] = lhs * rhs
            # print("MULT: ", prog[ip:ip + 4], f"prog[{param3}] = {lhs} * {rhs} = {lhs * rhs}")
            ip += 4
        elif opcode == 3:
            # print("IN:", prog[ip:ip + 2])
            if input_list:
                read =  input_list.pop(0)
            else:
                read = input("input? ")
            prog[prog[ip + 1]] = int(read)
            ip += 2
        elif opcode == 4:
            # print("OUT:", prog[ip:ip + 2])
            to_out = prog[prog[ip + 1]]
            print(to_out)
            ip += 2
        else:
            raise Exception(f"Unknown opcode: {opcode} @ {ip}: {current}")
    return prog

def test1():
    prog = [1,0,0,0,99]
    expected = [2,0,0,0,99]
    assert expected == intcode(prog)


def test2():
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

if __name__ == '__main__':
    with open('input05.txt', 'rt') as f:
        prog = [int(e) for e in f.read().split(',')]
        print("len(prog):", len(prog))
        print("part1:")
        intcode(prog, input_list=[1])
