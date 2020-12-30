# The Damned IntCode interpreter
# Yeesh!

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
