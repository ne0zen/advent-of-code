#!/usr/bin/env python3

import math
import sys

MAX_INT = sys.maxsize

def part1(timestamp_str, bus_ids_str):
    """
    What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?
    """
    # clean input
    timestamp = int(timestamp_str)
    # NOTE: ignore x bus_ids!
    bus_ids = [int(bus_id) for bus_id in bus_ids_str.split(',') if bus_id != 'x']

    minutes_from_now = [
        # minutes next bus will depart from current timestamp
        math.ceil(timestamp / bus_id) * bus_id - timestamp
        for bus_id in bus_ids
    ]

    min_bus_id = MAX_INT
    min_minutes_from_now = MAX_INT

    for idx, bus_id in enumerate(bus_ids):
        bus_minutes_from_now = minutes_from_now[idx]

        if bus_minutes_from_now < min_minutes_from_now:
            min_bus_id = bus_id
            min_minutes_from_now = bus_minutes_from_now
    return min_bus_id, min_minutes_from_now


def part2(bus_ids_str):
    split_bus_ids = bus_ids_str.split(',')
    bus_ids = [
            int(bus_id)
            for bus_id in split_bus_ids
            if 'x' != bus_id
    ]
    print()
    print("bus_ids:")
    print(*bus_ids, sep='\t')
    all_desired_minutes_from_now = [
            idx
            for idx, bus_id in enumerate(split_bus_ids)
            if 'x' != bus_id
    ]
    print("desired:")
    print(*all_desired_minutes_from_now, sep='\t')

    timestamp = 0
    interval = bus_ids[0]

    while True:
        calculated_minutes_from_now = [
            math.ceil(timestamp / bus_id) * bus_id - timestamp
            for bus_id in bus_ids
        ]
        calculated_minutes_from_now = []
        bail = False
        for idx, bus_id in enumerate(bus_ids):
            desired_minutes_for_this_bus = all_desired_minutes_from_now[idx]
            minutes_from_now_for_this_bus = math.ceil(timestamp / bus_id) * bus_id - timestamp

            # shortcut if this bus doesn't match at this timestamp
            if desired_minutes_for_this_bus != minutes_from_now_for_this_bus:
                bail = True
                break

            calculated_minutes_from_now.append(minutes_from_now_for_this_bus)

        if (not bail) and all_desired_minutes_from_now == calculated_minutes_from_now:
            return timestamp
        timestamp += interval


# works but godawful slow
#def part2(bus_ids_str):
    #"""
    #find the earliest timestamp such
    #that the first bus ID departs at that
    #time and each subsequent listed bus ID
    #departs at that subsequent minute.
    #"""

    #bus_ids = [
            #bus_id if 'x' == bus_id else int(bus_id)
            #for bus_id in bus_ids_str.split(',')
    #]
    #interval = bus_ids[0]
    ## starting timestamp
    #timestamp = 0
    #all_desired_minutes_from_now = list(range(len(bus_ids)))

    #while True:
        #calculated_minutes_from_now = []
        #for desired_minutes_from_now, bus_id in enumerate(bus_ids):
            #if 'x' == bus_id:
                ## skip calculation since we don't care for x bus_ids
                #minutes_from_now_for_this_bus = desired_minutes_from_now
            #else:
                ## do the real calculation
                #minutes_from_now_for_this_bus = math.ceil(timestamp / bus_id) * bus_id - timestamp
            ## shortcut if this bus doesn't match at this timestamp
            #if minutes_from_now_for_this_bus != desired_minutes_from_now:
                #break

            #calculated_minutes_from_now.append(
               #minutes_from_now_for_this_bus
            #)

        #if all_desired_minutes_from_now == calculated_minutes_from_now:
            #break

        ## next timestamp for first_bus_id
        #timestamp += interval

    #return timestamp

if __name__ == "__main__":
    with open('input13.txt', 'rt') as f:
        bus_id, minutes_from_now = part1(*f.read().strip().split('\n'))
        print("part1:", bus_id * minutes_from_now)
        f.seek(0)
        bus_ids = f.read().strip().split('\n')[1]
        print("part2(bus_ids):", part2(bus_ids))

sample = """
939
7,13,x,x,59,x,31,19
""".strip().split()

def test_exactly_on_arrival():
    timestamp = 10
    bus_ids = "2,3,7"
    bus_id, minutes_to_wait = part1(timestamp, bus_ids)
    assert 2 == bus_id
    assert 0 == minutes_to_wait

def test_part1_sample():
    bus_id, minutes_to_wait = part1(*sample)
    assert bus_id == 59
    assert 295 == bus_id * minutes_to_wait, f"nope, got: bus_id: {bus_id} minutes: {minutes_to_wait}"

def test_part2_sample():
    #assert 3417 == part2("17,x,13,19")
    #assert 754018 == part2("67,7,59,61")
    #assert 779210 == part2("67,x,7,59,61")
    #assert 1261476 == part2("67,7,x,59,61")
    #assert 1202161486 == part2("1789,37,47,1889")
    assert 1068781 == part2("7,13,x,x,59,x,31,19")
