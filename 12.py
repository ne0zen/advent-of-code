#!/usr/bin/env python3

import math

import sys

def manhattan_distance(result):
    return sum(map(abs, result))

def part1(instructions):
    """
    Action N means to move north by the given value.
    Action S means to move south by the given value.
    Action E means to move east by the given value.
    Action W means to move west by the given value.
    Action L means to turn left the given number of degrees.
    Action R means to turn right the given number of degrees.
    Action F means to move forward by the given value in the direction the ship is currently facing.
    """

    angle = 0   # "east"
    x = 0
    y = 0

    for lineno, line in enumerate(instructions):
        inst, *amount = line
        amount = int(''.join(amount))
        delta_x = 0
        delta_y = 0
        delta_angle = 0
        if 'N' == inst:
            delta_y = amount
        elif 'E' == inst:
            delta_x = amount
        elif 'W' == inst:
            delta_x = -amount
        elif 'S' == inst:
            delta_y = -amount
        elif 'L' == inst:
            delta_angle = math.radians(amount)
        elif 'R' == inst:
            delta_angle = math.radians(-amount)
        elif 'F' == inst:
            delta_x = math.cos(angle) * amount
            delta_y = math.sin(angle) * amount
        else:
            raise Exception(f"Unknown Instruction {inst} on line #{lineno}: {line}")

        #print("delta_x:", delta_x, "delta_y:", delta_y, "delta_angle:", delta_angle)
        x += delta_x
        y += delta_y
        angle += delta_angle
    return x, y


def rotate_around_origin(x, y, angle):
    """
    rotates a point (x, y) <angle> degrees around the origin
    returns x1, y1
    """
    angle_in_radians = math.radians(angle)
    #r = math.isqrt(pow(x, 2) + pow(y, 2))
    #current_angle = math.atan(y / x)
    #print("math.degrees(current_angle):", math.degrees(current_angle))
    #new_angle = current_angle + math.radians(angle)
    #print("math.degrees(new_angle):", math.degrees(new_angle))
    #x1 = round(math.cos(new_angle) * r)
    #y1 = round(math.sin(new_angle) * r)
    c = math.cos(angle_in_radians)
    s = math.sin(angle_in_radians)
    x1 = round(x * c - y * s)
    y1 = round(x * s + y * c)
    return x1, y1



def part2(instructions):
    """
    N means to move the waypoint north by the given value.
    S means to move the waypoint south by the given value.
    E means to move the waypoint east by the given value.
    W means to move the waypoint west by the given value.
    L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
    R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
    F means to move forward to the waypoint a number of times equal to the given value.

    waypoint starts 10 units east and 1 unit north relative to the ship.
    The waypoint is relative to the ship; that is, if the ship moves, the waypoint
    moves with it.
    """
    # ship x, y
    x = 0
    y = 0
    waypoint_x = 10
    waypoint_y = 1

    for lineno, line in enumerate(instructions):
        inst, *amount = line
        amount = int(''.join(amount))
        delta_x = 0
        delta_y = 0
        delta_waypoint_x = 0
        delta_waypoint_y = 0

        if 'N' == inst:
            delta_waypoint_y = amount
        elif 'E' == inst:
            delta_waypoint_x = amount
        elif 'W' == inst:
            delta_waypoint_x = -amount
        elif 'S' == inst:
            delta_waypoint_y = -amount
        elif 'L' == inst:
            waypoint_x, waypoint_y = rotate_around_origin(waypoint_x, waypoint_y, amount)
        elif 'R' == inst:
            waypoint_x, waypoint_y = rotate_around_origin(waypoint_x, waypoint_y, -amount)
        elif 'F' == inst:
            delta_x = waypoint_x * amount
            delta_y = waypoint_y * amount
        else:
            raise Exception(f"Unknown Instruction {inst} on line #{lineno}: {line}")

        x += delta_x
        y += delta_y
        waypoint_x += delta_waypoint_x
        waypoint_y += delta_waypoint_y
    return x, y


if __name__ == "__main__":
    with open('input12.txt') as f:
        print("part1:", manhattan_distance(part1(f)))
        f.seek(0)
        print("part2:", manhattan_distance(part2(f)))

def test_part1_forward():
    instructions = "F10".split()
    assert 10, 0 == part1(instructions)
    assert 10 == manhattan_distance(part1(instructions))

def test_part1_E_then_forward():
    instructions = "E10 F10".split()
    assert 20, 0 == part1(instructions)
    assert 20 == manhattan_distance(part1(instructions))

def test_part1_W_then_forward():
    instructions = "W10 F10".split()
    assert (0, 0) == part1(instructions)
    assert 0 == manhattan_distance(part1(instructions))

def test_part1_S_then_forward():
    instructions = "S10 F10".split()
    assert (10, -10) == part1(instructions)
    assert 20 == manhattan_distance(part1(instructions))

def test_part1_sample():
    sample = """
    F10
    N3
    F7
    R90
    F11
    """.strip().split()
    assert (17, -8) == part1(sample)
    assert 25 == manhattan_distance(part1(sample))

def test_part2_forward():
    instructions = "F1".split()
    assert (10, 1) == part2(instructions)
    assert 11 == manhattan_distance(part2(instructions))

def test_part2_forward_lots():
    sample = "F10".split()
    result = part2(sample)
    assert (100, 10) == result
    assert 110 == manhattan_distance(result)

def test_part2_S_then_forward():
    instructions = "S1 F1".split()
    assert (10, 0) == part2(instructions)
    assert 10 == manhattan_distance(part2(instructions))

def test_part2_sanify_then_L90_then_forward():
    # moves waypoint to 10 units directly E of boat
    # then rotates waypoint 90 degrees to left (ie. to 10 units N of boat)
    # then moves boat 1 unit in direction of waypoint (10 units N)
    instructions = "S1 L90 F1".split()
    assert (0, 10) == part2(instructions)
    assert 10 == manhattan_distance(part2(instructions))

def test_part2_full_sample():
    sample = """
    F10
    N3
    F7
    R90
    F11
    """.strip().split()
    result = part2(sample)
    assert (214, -72) == result
    assert 286 == manhattan_distance(result)

