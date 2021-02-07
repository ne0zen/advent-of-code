#!/usr/bin/env python3


def get_paramvis_from_prog(param_num, prog, ip, relative_base):
    # determine param modes
    current = prog[ip]
    param1_mode = current % 1000 // 100
    param2_mode = current % 10000 // 1000
    param3_mode = current // 10000
    assert param_num < 3

    raw_param = prog[ip + param_num]
    param_mode = locals()[f'param{param_num}_mode']

    # 1 is "value"
    result = None
    if 0 == param_mode:         # position in prog
        result = f"m[{raw_param}]"
    elif 1 == param_mode:       # value
        result = str(raw_param)
    elif 2 == param_mode:
        # if 0 == relative_base:
        #     result = f"[{raw_param}]"
        # else:
        #     result = f"[{raw_param} {relative_base}]"
        result = f"m[{raw_param} + {relative_base}]"
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
    9: 2,
    99: 1
}



def intcode_disassemble(prog):
    ip = 0
    relative_base = 0
    print("len(prog):", len(prog))

    # so lower calls don't have to pass prog and ip
    def param(param_num):
        return get_paramvis_from_prog(param_num, prog, ip, relative_base)

    halted = False
    while (ip < len(prog)):
        current = prog[ip]
        opcode = current % 100
        # default for next_ip (adding 1 to skip opcode itself)
        instruction_size = INSTRUCTION_SIZE_BY_OPCODE.get(opcode, 1)
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
            print(f"m[{param3}] = {lhs} + {rhs}")

        elif opcode == 2:
            lhs = param(1)
            rhs = param(2)
            param3 = prog[ip + 3]
            assert param3 >= 0, "MUL: param3 should be >= 0"
            print(f"m[{param3}] = {lhs} * {rhs}")

        elif opcode == 3:
            print(f"m[{prog[ip + 1]}] = IN")

        elif opcode == 4:
            print(f"OUT {param(1)}")

        elif opcode == 5:   # jmp if nonzero
            print("JNZ", param(1), param(2))

        elif opcode == 6:   # jmp if zero
            print("JZ", param(1), param(2))

        elif opcode == 7:   # prog[param3] = 1 if first < second else 0
            print(f"m[{prog[ip + 3]}] = 1 if {param(1)} < {param(2)} else 0")

        elif opcode == 8:   # prog[param3] = 1 if first < second else 0
            first = param(1)
            second = param(2)
            print(f"m[{prog[ip + 3]}] = 1 if {param(1)} < {param(2)} else 0")

        elif opcode == 9:
            offset = int(param(1))
            sign = ''
            if offset > 0:
                sign = '+'
            elif offset < 0:
                sign = '-'
            print(f"BASE {sign}= {param(1)}")
            relative_base += offset
        elif opcode == 99:
            print(f"HALT")
            halted = True
        else:
            raise Exception(f"Unknown opcode: {opcode} @ {ip}")
        ip = next_ip

prog = 109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
intcode_disassemble(prog)

