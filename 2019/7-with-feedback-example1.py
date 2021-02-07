#!/usr/bin/env python3


def part2example2(phase):
    print("phase:", phase)
    adj_phase = phase - 4
    i = 5
    while i > 0:
        signal = (yield)
        if signal is None:
            raise "hell"
        signal = signal * 2 + adj_phase
        yield signal
        i -= 1
        if i == 0:
            break

NUM_AMPLIFIERS = 5

import itertools
def get_thruster_signal_with_feedback(phase_settings, prog):
    amps = []
    choose_amp = itertools.cycle(range(NUM_AMPLIFIERS))

    # initialize the amps with phase setting and first signal
    outputs = [None] * NUM_AMPLIFIERS
    # init and prime the amplifier generators
    for phase_setting in phase_settings:
        amplifier = part2example2(phase_setting)
        # prime the amp
        amplifier.send(None)
        amps.append(amplifier)

    last_value = 0
    while True:
        amp_idx = next(choose_amp)
        amp = amps[amp_idx]
        result = amp.send(last_value)
        outputs[amp_idx] = result
        # print(f"{amp_idx=}\t{phase_settings[amp_idx]=}\t{outputs[amp_idx]=}")
        print(f"{amp_idx=}\t{outputs=}")
        last_value = result
        try:
            amp.send(None)
        except StopIteration:
            if amp == amps[-1]:
                break

    return outputs[-1]

expected = 139629729
phase_settings = 9,8,7,6,5
prog = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
        27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
actual = get_thruster_signal_with_feedback(phase_settings, prog)
assert expected == actual, f"{expected} != {actual}"

