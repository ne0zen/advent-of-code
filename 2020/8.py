#!/usr/bin/env python3

class Emulator():
    def __init__(self, instructions):
        self.pc = 0
        self.lines_run: [int] = []
        self.instructions = instructions.split('\n')
        self.acc = 0

    def acc(self, increment):
        self.acc += int(increment)

    def jmp(self, operand):
        return self.pc + int(operand)

    def nop(self, operand):
        pass

    def run_until_repeat_return_acc(self):
        while True:
            line = self.instructions[self.pc].strip()
            lineno = self.pc
            instruction, _, operand = line.partition(' ')
            #print("lineno:", lineno)
            #print("instruction:", instruction)
            #print("operand:", operand)
            #method = getattr(self, instruction, None)
            #print("method:", method)
            next_pc = self.pc + 1

            if 'acc' == instruction:
                self.acc += int(operand)
            elif 'nop' == instruction:
                pass
            elif 'jmp' == instruction:
                next_pc = self.pc + int(operand)

            if next_pc in self.lines_run:
                break
            self.lines_run.append(lineno)
            self.pc = next_pc

        return self.acc

if __name__ == "__main__":
    with open('input08.txt', 'rt') as f:
        emu = Emulator(f.read())
        acc = emu.run_until_repeat_return_acc()
        print('part1:', acc)


import pytest

def test_sample():
    sample = """
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6
    """.strip()
    emu = Emulator(sample)
    acc = emu.run_until_repeat_return_acc()
    print("emu.lines_run:", emu.lines_run)
    assert 5 == acc
