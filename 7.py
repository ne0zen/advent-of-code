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
    output = []

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
            output.append(to_out)
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
            break
        else:
            raise Exception(f"Unknown opcode: {opcode} @ {ip}: {current}")
        ip = next_ip
    return output


def get_thruster_signal(phase_setting_sequence, prog):
    last_output = [0]
    for phase_setting in phase_setting_sequence:
        last_output = intcode(prog.copy(), input_list=[phase_setting, last_output[-1]])
    return last_output[-1]


import itertools
def find_phase_sequence_with_max_thruster_signal(prog):
    max_output_signal = 0
    max_phase_setting = None
    for phase_setting_sequence in itertools.permutations([0,1,2,3,4]):
        output_signal = get_thruster_signal(phase_setting_sequence, prog)
        if output_signal > max_output_signal:
            max_phase_setting = phase_setting_sequence
            max_output_signal = output_signal
    return max_phase_setting, max_output_signal


if __name__ == '__main__':
    with open('input07.txt', 'rt') as f:
        prog = [int(e) for e in f.read().split(',')]

    phase_setting, max_signal = find_phase_sequence_with_max_thruster_signal(
        prog.copy()
    )
    print("part1")
    print("phase_setting:", phase_setting)
    print("max_signal:", max_signal)

# Tests
def test_example1():
    expected = 43210
    prog = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    phase_settings = 4,3,2,1,0
    assert expected == get_thruster_signal(phase_settings, prog)


def test_example1_find_phase_sequence_with_max_thruster_signal():
    prog = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    expected_max_signal = 43210
    expected_phase_setting = [4,3,2,1,0]
    actual_phase_setting, actual_max_signal = find_phase_sequence_with_max_thruster_signal(
        prog
    )
    assert expected_max_signal == actual_max_signal
    assert actual_phase_setting == actual_phase_setting


def test_example2():
    expected = 54321
    phase_settings = 0,1,2,3,4
    prog = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
            101,5,23,23,1,24,23,23,4,23,99,0,0]
    assert expected == get_thruster_signal(phase_settings, prog)


def test_example2_find_phase_sequence_with_max_thruster_signal():
    prog = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
            101,5,23,23,1,24,23,23,4,23,99,0,0]
    expected_max_signal = 54321
    expected_phase_setting = [0,1,2,3,4]
    actual_phase_setting, actual_max_signal = find_phase_sequence_with_max_thruster_signal(
        prog
    )
    assert expected_max_signal == actual_max_signal
    assert actual_phase_setting == actual_phase_setting


def test_example3():
    expected = 65210
    phase_settings = 1,0,4,3,2
    prog = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
            1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert expected == get_thruster_signal(phase_settings, prog)


def test_example3_find_phase_sequence_with_max_thruster_signal():
    prog = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
            1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    expected_max_signal = 65210
    expected_phase_setting = [1,0,4,3,2]
    actual_phase_setting, actual_max_signal = find_phase_sequence_with_max_thruster_signal(
        prog
    )
    assert expected_max_signal == actual_max_signal
    assert actual_phase_setting == actual_phase_setting


