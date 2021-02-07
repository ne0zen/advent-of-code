#!/usr/bin/env python3


def gen_value(multiplier):
    while True:
        x = yield
        print("in: ", x, flush=True)
        if x is None:
            raise Exception("hell")
        yield (multiplier * x)


amp = gen_value(2)
# "prime" the generator
print("sent None, got", amp.send(None))

last_value = 1
# for _ in range(10):
count = 0
while count < 10:
    last_value = amp.send(last_value)
    print("out:", last_value, flush=True)
    # prime it... again?
    next(amp)
    count += 1
