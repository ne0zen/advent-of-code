#!/usr/bin/env python3


def get_paramvis_from_prog(param_num, prog, ip):
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
        result = f"[{raw_param}]"
    elif 1 == param_mode:       # value
        result = str(raw_param)
    else:
        raise Exception(f"Unknown Param mode {param_mode} @ {ip}: {current}")

    # print(f"{param_num=}, {param_mode=}, {result=}")
    return result


INSTRUCTION_SIZE_BY_OPCODE = {
    1: 4,
    2: 4,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 4,
    8: 4,
    99: 1
}



def intcode_disassemble(prog):
    ip = 0
    print("len(prog):", len(prog))

    # so lower calls don't have to pass prog and ip
    def param(param_num):
        return get_paramvis_from_prog(param_num, prog, ip)

    halted = False
    while (ip < len(prog)):
        current = prog[ip]
        opcode = current % 100
        instruction_size = INSTRUCTION_SIZE_BY_OPCODE.get(opcode, 1)
        # default for next_ip (adding 1 to skip opcode itself)
        next_ip = ip + instruction_size
        print(f"{ip:04d}:",  end='\t')
        # print data
        if halted:
            print(" " * 20 + f"DAT {current}")
            ip += instruction_size
            continue
        else:
            format_string = ("{:04d} " + "{:03d} " * (instruction_size - 1))
            full_instruction = prog[ip:ip + instruction_size]
            print(format_string.format(*full_instruction).ljust(20), end='')
        if opcode == 1:
            lhs = param(1)
            rhs = param(2)
            param3 = prog[ip + 3]
            assert param3 >= 0, "ADD: outaddr should be >= 0"
            # prog[param3] = lhs + rhs
            print(f"[{param3}] = {lhs} + {rhs}")
        elif opcode == 2:
            lhs = param(1)
            rhs = param(2)
            param3 = prog[ip + 3]
            assert param3 >= 0, "MUL: param3 should be >= 0"
            print(f"[{param3}] = {lhs} * {rhs}")
        elif opcode == 3:
            print(f"[{prog[ip + 1]}] = IN")
        elif opcode == 4:
            print(f"OUT {param(1)}")
        elif opcode == 5:   # jmp if nonzero
            print("JNZ", param(1), param(2))
        elif opcode == 6:   # jmp if zero
            print("JZ", param(1), param(2))
        elif opcode == 7:   # prog[param3] = 1 if first < second else 0
            print(f"[{prog[ip + 3]}] = 1 if {param(1)} < {param(2)} else 0")
        elif opcode == 8:   # prog[param3] = 1 if first < second else 0
            first = param(1)
            second = param(2)
            print(f"[{prog[ip + 3]}] = 1 if {param(1)} < {param(2)} else 0")
        elif opcode == 99:
            print(f"HALT")
            halted = True
        else:
            raise Exception(f"Unknown opcode: {opcode}, {ip}")
        ip = next_ip


prog = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
        27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
intcode_disassemble(prog)


# prog = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
#         -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
#         53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
# intcode_disassemble(prog)
