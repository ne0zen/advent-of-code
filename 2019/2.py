#!/usr/bin/env python3


def intcode(prog):
    ip = 0

    inst = prog[ip]
    while (inst != 99):
        if inst == 1:
            lhs, rhs, outaddr = prog[ip+1:ip+4]
            prog[outaddr] = prog[lhs] + prog[rhs]
            ip += 4
        elif inst == 2:
            lhs, rhs, outaddr = prog[ip+1:ip+4]
            prog[outaddr] = prog[lhs] * prog[rhs]
            ip += 4
        inst = prog[ip]
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


if __name__ == '__main__':
    with open('input02.txt', 'rt') as f:
        prog = [int(e) for e in f.read().split(',')]
        # part 1
        # prog[1] = 12
        # prog[2] = 2
        # print('part1:', intcode(prog)[0])
        for i in range(99):
            for j in range(99):
                trial = prog.copy()
                trial[1] = i
                trial[2] = j
                out = intcode(trial)[0]
                if out == 19690720:
                    print('part2:', i * 100 + j)
                    import sys; sys.exit(1)
