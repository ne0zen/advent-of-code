#!/usr/bin/env python3

import copy
import re

NUM_BITS = 36
MASK_PATTERN = re.compile(r"mask = (?P<mask>.{36})$")
WRITE_PATTERN = re.compile(r"mem\[(?P<address>\d+)\] = (?P<value>\d+)")
BINARIFY = f'0{NUM_BITS}b'


def run(program):
    """
    The bitmask is always given as a string of 36 bits, written with
    the most significant bit (representing 2^35) on the left and the
    least significant bit (2^0, that is, the 1s bit) on the right. The
    current bitmask is applied to values immediately before they are
    written to memory: a 0 or 1 overwrites the corresponding bit in the
    value, while an X leaves the bit in the value unchanged.
    """
    mem = {}
    mask = 'X' * NUM_BITS  # init to don't care

    for line in program.split('\n'):
        line = line.strip()
        if not line: continue  # skip empty lines

        if match := MASK_PATTERN.match(line):
            data = match.groupdict()
            # handle mask
            mask = data['mask']
        elif match := WRITE_PATTERN.match(line):
            data = match.groupdict()
            # handle write
            key = int(data['address'])
            value = int(data['value'])
            # init a temporary "write register" to value
            wr = list(format(value, BINARIFY))
            # apply mask to the write register
            for idx, bit in enumerate(mask):
                if bit != 'X':
                    wr[idx] = bit
            # store the masked value
            mem[key] = int(''.join(wr), base=2)
        else:
            raise Exception(f"Unknown Instruction: {line}")
    return mem


def run2(program):
    """
    A version 2 decoder chip doesn't modify
    the values being written at all.
    Instead, it acts as a memory address
    decoder. Immediately before a value is
    written to memory, each bit in the
    bitmask modifies the corresponding bit
    of the destination memory address in
    the following way:


    - If the bitmask bit is 0, the
      corresponding memory address bit is
      unchanged.
    - If the bitmask bit is 1, the
      corresponding memory address bit is
      overwritten with 1.
    - If the bitmask bit is X, the
      corresponding memory address bit is
      floating.

    A floating bit is not connected to
    anything and instead fluctuates
    unpredictably. In practice, this means
    the floating bits will take on all
    possible values, potentially causing
    many memory addresses to be written all
    at once!
    """
    mem = {}
    mask = 'X' * NUM_BITS  # init to don't care

    for line in program.split('\n'):
        line = line.strip()
        if not line: continue  # skip empty lines

        if match := MASK_PATTERN.match(line):
            data = match.groupdict()
            # handle mask
            mask = data['mask']
        elif match := WRITE_PATTERN.match(line):
            data = match.groupdict()
            orig_address = int(data['address'])
            value = int(data['value'])
            # determine dest addresses
            addresses = determine_dest_addresses(mask, orig_address)
            # perform write(s)
            for key in addresses:
                mem[key] = value
        else:
            raise Exception(f"Unknown Instruction: {line}")
    return mem


def determine_dest_addresses(mask, orig_address):
    # handle simple case (no X in mask)
    if 'X' not in mask:
        return [orig_address | int(mask, base=2)]

    destinations = set()
    masked_destination = list(format(orig_address, BINARIFY))
    # overwrite bits in dest where mask has 1 or X
    for idx, bit in enumerate(mask):
        if '0' != bit:
            masked_destination[idx] = bit

    x_positions = [i for i,bit in enumerate(mask) if bit == 'X']

    # value is a counter which tells us which X bits for a
    # particular destination are 0 and which are 1
    for value in range(2**len(x_positions)):
        destination = copy.deepcopy(masked_destination)
        bitstring = list(format(value, f'0{len(x_positions)}b'))
        for idx, which_x_pos in enumerate(x_positions):
            destination[which_x_pos] = bitstring[idx]
        destinations.add(int(''.join(destination), base=2))

    return destinations


if __name__ == "__main__":
    with open('input14.txt', 'rt') as f:
        mem = run(f.read())
        part1 = sum(mem.values())
        print("part1:", part1)
        f.seek(0)
        mem = run2(f.read())
        part2 = sum(mem.values())
        print("part2:", part2)

# Tests

def test_run_single_write():
    program = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
    """
    mem = run(program)
    assert 73 == sum(mem.values())

def test_run_more_writes():
    program = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
    """
    mem = run(program)
    assert 101 + 64 == sum(mem.values())

def test_run2_single_X_mask():
    program = """
mask = 00000000000000000000000000000001001X
mem[42] = 100
    """
    mem = run2(program)
    from pprint import pprint; pprint(mem)
    # check specific destinations
    assert mem[58] == 100
    assert mem[59] == 100
    # check we didn't write 100 to other addresses
    assert 100 + 100 == sum(mem.values())

def test_run2_2X_mask():
    program = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
    """
    mem = run2(program)
    from pprint import pprint; pprint(mem)
    # check specific destinations
    for address in map(int, "26 27 58 59".split()):
        assert mem[address] == 100

    # check we didn't write 100 to other addresses
    assert 400 == sum(mem.values())

def test_run2_complex():
    program = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
    """
    mem = run2(program)
    assert 208 == sum(mem.values())
