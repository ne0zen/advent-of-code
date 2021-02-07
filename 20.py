#!/usr/bin/env python3


import re
import itertools
import collections


class Tile:
    def __init__(self, rows):
        self.border_values = set()
        self.id: str = ''
        self.rows = rows
        # orientation-related fields
        self.rotated = 0
        self.flipped_v = False
        self.flipped_h = False

        match = re.search(r'\d+', rows[0])
        self.id = int(match.group(0))

        self.add_border(self.top)
        assert 2 == len(self.border_values)

        # bottom
        self.add_border(self.bottom)
        assert 4 == len(self.border_values)

        # left
        self.add_border(self.left)
        assert 6 == len(self.border_values)

        # right
        self.add_border(self.right)
        assert 8 == len(self.border_values)

    def add_border(self, value):
        if value is not str:
            value = ''.join(value)
        value = value.strip()
        assert len(self.top) == len(value)
        self.border_values.add(value)

        reversed_value = ''.join(reversed(value))
        assert value != reversed_value
        self.border_values.add(reversed_value)

    def fliph(self, to_flip=True):
        if not to_flip:
            return self
        new_rows = [self.rows[0]]
        new_rows[1:] = reversed(self.rows[1:])
        tile = Tile(new_rows)
        tile.flipped_h = True
        return tile

    def flipv(self, to_flip=True):
        if not to_flip:
            return self

        new_rows = [self.rows[0]]
        for i, row in enumerate(self.rows[1:]):
            new_rows.append(''.join(reversed(row)))
        tile = Tile(new_rows)
        tile.flipped_v = True
        return tile

    def rotate(self, num_times):
        "returns a copy of Tile that's been rotated `num_times` to the left"
        tile = self
        for _ in range(num_times):
            new_rows = [self.rows[0]]
            for col_num in range(1, len(tile.top) + 1):
                new_row = ''.join(row[-col_num] for row in tile.rows[1:])
                new_rows.append(new_row)
            tile = Tile(new_rows)
        tile.rotated = num_times
        return tile

    def __eq__(self, rhs):
        return self.rows == rhs.rows

    def border_match(self, rhs):
        matching_borders = self.border_values.intersection(rhs.border_values)
        num_matching_borders = len(matching_borders)
        return num_matching_borders > 0

    @property
    def top(self): return self.rows[1]
    @property
    def bottom(self): return self.rows[-1]
    @property
    def left(self): return ''.join(row[0] for row in self.rows[1:])
    @property
    def right(self): return ''.join(row[-1] for row in self.rows[1:])

    def orientation(self):
        return ''.join([
            str(self.rotated),
            'H' if self.flipped_h else '',
            'V' if self.flipped_v else '',
        ])

    def __repr__(self):
        return f"<Tile #{self.id} {self.orientation()}>"

    def determine_orientation(tile1, tile2, match_type='rightof'):
        for rotation in [0, 1, 3]:
            for fliph in [False, True]:
                for flipv in [False, True]:
                    transformed_tile2 = tile2.fliph(fliph).flipv(flipv).rotate(rotation)
                    if match_type == 'rightof' and tile1.right == transformed_tile2.left:
                        return transformed_tile2
                    elif match_type == 'below' and tile1.bottom == transformed_tile2.top:
                        return transformed_tile2

        raise Exception(f"can't find orientation for {transformed_tile2} {match_type} {tile1}")


def determine_orientations(tile1, tile2, match_type='rightof'):
    for rotation in [0, 1, 3]:
        for fliph in [False, True]:
            for flipv in [False, True]:
                for rotation2 in [0, 1, 3]:
                    for fliph2 in [False, True]:
                        for flipv2 in [False, True]:
                            tmp_tile1 = tile1.fliph(fliph).flipv(flipv).rotate(rotation)
                            tmp_tile2 = tile2.fliph(fliph2).flipv(flipv2).rotate(rotation2)
                            if match_type == 'rightof' and tmp_tile1.right == tmp_tile2.left:
                                return [tmp_tile1, tmp_tile2]
                            if match_type == 'below' and tmp_tile1.bottom == tmp_tile2.top:
                                return [tmp_tile1, tmp_tile2]


def get_tiles(data):
    tiles = []
    rows = []

    for line in data:
        line = line.strip()
        if line:
            rows.append(line)
        elif rows:
            tile = Tile(rows)
            tiles.append(tile)
            rows = []
    if rows:
        tile = Tile(rows)
        tiles.append(tile)
    return tiles


def find_corner_tiles(tiles):
    match_ids_by_tile_id = collections.defaultdict(set)
    # determine matches
    for tile1, tile2 in itertools.permutations(tiles, 2):
        if tile1.border_match(tile2):
            match_ids_by_tile_id[tile1.id].add(tile2.id)
            match_ids_by_tile_id[tile2.id].add(tile1.id)

    # figure out which tiles have only two matches
    corner_tile_ids = set(
            key for key in match_ids_by_tile_id.keys()
            if len(match_ids_by_tile_id[key]) == 2
    )
    return [tile for tile in tiles if tile.id in corner_tile_ids]


def build_image(tiles):
    match_ids_by_tile_id = collections.defaultdict(set)
    # determine matches
    print("finding adjacencies...", end='', flush=True)
    for tile1, tile2 in itertools.permutations(tiles, 2):
        if tile1.border_match(tile2):
            match_ids_by_tile_id[tile1.id].add(tile2.id)
            match_ids_by_tile_id[tile2.id].add(tile1.id)
    print("done.", flush=True)

    # build graph & render w/ neato graphviz
    # import graphviz
    # graph = graphviz.Graph('20-tiles', strict=True, engine='neato', format='png')
    # for tile_id, match_ids in match_ids_by_tile_id.items():
    #     graph.node(str(tile_id), f'{tile_id}\n{len(match_ids)}')
    #     for match_id in match_ids:
    #         graph.edge(str(tile_id), str(match_id))
    # graph.view()
    tile_by_tile_id = {tile.id: tile for tile in tiles}

    corners = [tile_by_tile_id[tile_id] for tile_id, matches in match_ids_by_tile_id.items() if len(matches) == 2]
    to_place = {tile.id for tile in tiles}
    result = [list() for _ in range(12)]


    print(determine_orientations(tile_by_tile_id[3593], tile_by_tile_id[3109], match_type='rightof'))
    print(determine_orientations(tile_by_tile_id[3593], tile_by_tile_id[1877], match_type='below'))

    top_left = tile_by_tile_id[3593]
    right_of_top_left = tile_by_tile_id[list(match_ids_by_tile_id[top_left.id])[0]]
    to_place.discard(right_of_top_left.id)
    top_left, right_of_top_left = determine_orientations(top_left, right_of_top_left)
    row_num = 0
    result[row_num].append(top_left)
    to_place.discard(top_left.id)
    result[row_num].append(right_of_top_left)
    to_place.discard(right_of_top_left.id)
    last_tile = right_of_top_left

    # fill top row
    while len(result[row_num]) < 11:
        # 3 because we want something on the edge
        next_tile_id = next(match_id for match_id in match_ids_by_tile_id[last_tile.id] if match_id in to_place and len(match_ids_by_tile_id[match_id]) == 3)
        next_tile = last_tile.determine_orientation(tile_by_tile_id[next_tile_id], match_type='rightof')
        result[row_num].append(next_tile)
        to_place.discard(next_tile.id)
        last_tile = next_tile
    # place the corner
    next_tile_id = next(iter(match_ids_by_tile_id[last_tile.id].intersection(to_place)))
    next_tile_id = next(match_id for match_id in match_ids_by_tile_id[last_tile.id] if match_id in to_place and len(match_ids_by_tile_id[match_id]) in [2, 3])
    next_tile = last_tile.determine_orientation(tile_by_tile_id[next_tile_id], match_type='rightof')
    result[row_num].append(next_tile)
    to_place.discard(next_tile_id)
    assert len(result[0]) == 12

    # first of following row
    row_num = 1
    last_tile = result[row_num - 1][0]
    print("match_ids_by_tile_id[last_tile.id]:", match_ids_by_tile_id[last_tile.id])
    next_tile_id = next(iter(match_ids_by_tile_id[last_tile.id].intersection(to_place)))
    print("next_tile_id:", next_tile_id)
    next_tile = last_tile.determine_orientation(tile_by_tile_id[next_tile_id], match_type='below')
    result[row_num].append(next_tile)
    to_place.discard(next_tile.id)
    last_tile = next_tile
    while len(result[row_num]) < 11:
        # 4 because we want something in the middle
        next_tile_id = next(match_id for match_id in match_ids_by_tile_id[last_tile.id] if match_id in to_place and len(match_ids_by_tile_id[match_id]) == 4)
        next_tile = last_tile.determine_orientation(tile_by_tile_id[next_tile_id], match_type='rightof')
        result[row_num].append(next_tile)
        to_place.discard(next_tile.id)
        last_tile = next_tile

    from pprint import pprint; pprint(result)
    print("last_tile.id:", last_tile.id)


    # sides = {tile_id for tile_id, matches in match_ids_by_tile_id.items() if len(matches) == 3}
    # middle = {tile_id for tile_id, matches in match_ids_by_tile_id.items() if len(matches) == 4}
    # print("len(corners):", len(corners))
    # print("len(sides):", len(sides))
    # print("len(middle):", len(middle))


def main():
    with open('input20.txt', 'rt') as f:
        tiles = get_tiles(f)

    # corner_tiles = find_corner_tiles(tiles)
    # import functools
    # import operator
    # print("part1:", functools.reduce(operator.mul, (tile.id for tile in corner_tiles)))
    image = build_image(tiles)





if __name__ == "__main__":
    main()


# Tests
def test_tile_fliph():
    tile = Tile([
        '12', # id
        'ab',
        'cd',
    ])
    assert tile == tile.fliph(False)
    assert tile.fliph() == Tile([
        '12',
        'cd',
        'ab',
    ])


def test_tile_flipv():
    tile = Tile([
        '12', # id
        'ab',
        'cd',
    ])
    assert tile == tile.flipv(False)
    assert tile.flipv() == Tile([
        '12',
        'ba',
        'dc',
    ])


def test_tile_rotate():
    tile = Tile([
        '12',
        'ab',
        'cd',
    ])

    assert tile.rotate(1) == Tile([
        '12',
        'bd',
        'ac'
    ])


def test_tile_rotate2():
    tile = Tile([
        '12',
        'ab',
        'cd',
    ])

    assert tile.rotate(2) == Tile([
        '12',
        'dc',
        'ba'
    ])

def test_tile_rotate3():
    tile = Tile([
        '12',
        'ab',
        'cd',
    ])

    assert tile.rotate(3) == Tile([
        '12',
        'ca',
        'db'
    ])

def test_fliphv_is_rotate2():
    tile = Tile([
        '12',
        'ab',
        'cd',
    ])
    assert tile.rotate(2) == tile.fliph().flipv()


import io
sample = io.StringIO("""
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
""".strip())
def test_part1():
    # expected = list(map(lambda s: s.split(), """
    # 1951    2311    3079
    # 2729    1427    2473
    # 2971    1489    1171
    # """.strip().split('\n')))
    expected = {1951,3079,2971,1171}
    tiles = get_tiles(sample)
    assert expected == {tile.id for tile in find_corner_tiles(tiles)}

