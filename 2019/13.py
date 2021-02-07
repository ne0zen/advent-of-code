#!/usr/bin/env python3

from intcode import intcode

import sys

INT_MAX = sys.maxsize

def find_boundaries(tile_data):
    min_x = INT_MAX
    max_x = 0
    min_y = INT_MAX
    max_y = 0
    for i in range(0, len(tile_data), 3):
        x = tile_data[i]
        y = tile_data[i + 1]
        tile_id = tile_data[i + 2]
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if y < min_y:
            min_y = y

    return min_x, max_x, min_y, max_y


def build_tiles_from_tile_data(tile_data):
    min_x, max_x, min_y, max_y = find_boundaries(tile_data)
    # populate tiles
    tiles = [ [' '] * (max_x + 1) for _ in range(max_y + 1)]

    tiles_by_id = [' ', 'X', '#', '=', 'O']
    # populate tiles
    for i in range(0, len(tile_data), 3):
        x = tile_data[i]
        y = tile_data[i + 1]
        tile_id = tile_data[i + 2]

        tiles[y][x]= tiles_by_id[tile_id]
    return tiles


def draw_tiles(tile_data):
    min_x, max_x, min_y, max_y = find_boundaries(tile_data)
    # populate tiles
    tiles = [[' '] * 40 for _ in range(22)]

    tiles_by_id = [' ', 'X', '#', '=', 'O']
    # populate tiles
    for i in range(0, len(tile_data), 3):
        x = tile_data[i]
        y = tile_data[i + 1]
        tile_id = tile_data[i + 2]

        tiles[x - min_x][y - min_y] = tiles_by_id[tile_id]

    # paint
    for row in tiles:
        print(''.join(row))




def count_tile_of_type(tile_data: [str], tile_id_to_count: int):
    count = 0
    for i in range(0, len(tile_data), 3):
        x = tile_data[i]
        y = tile_data[i + 1]
        tile_id = tile_data[i + 2]
        if tile_id == tile_id_to_count:
            count += 1
    return count

if __name__ == "__main__":
    with open('input13.txt', 'rt') as f:
        prog = [int(t) for t in f.read().split(',')]
    tile_data = []
    # prime the arcade
    arcade = intcode(prog, input_list=[-1])

    try:
        for t in arcade:
            tile_data.append(next(arcade))
    except StopIteration:
        print("tile_data:", tile_data)

    assert len(tile_data) % 3 == 0, "tile_data length should be an exact multiple of three"
    print("len(tile_data):", len(tile_data))


    min_x, max_x, min_y, max_y = find_boundaries(tile_data)
    print(f"{min_x=}, {max_x=}, {min_y=}, {max_y=}")
    print("tile_data=", tile_data)


    print("paint:")
    draw_tiles(tile_data)
    print("part1:", count_tile_of_type(tile_data, 2))






# Test
def test_find_boundaries():
    tile_data = [1,2,3,6,5,4]
    # prime our painter
    min_x, max_x, min_y, max_y = find_boundaries(tile_data)
    assert 1 == min_x
    assert 6 == max_x
    assert 2 == min_y
    assert 5 == max_y


def test_build_tiles_from_tile_data():
    tile_data = [1,2,3,6,5,4]
    actual = build_tiles_from_tile_data(tile_data)
    assert actual[2][1] == '='
    assert actual[5][6] == 'O'


def test_count_tile_of_type():
    tile_data = [1,2,3,6,5,4]
    assert 1 == count_tile_of_type(tile_data, 3)
    assert 1 == count_tile_of_type(tile_data, 4)
