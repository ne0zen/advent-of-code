#!/usr/bin/env python3

from typing import *

import collections
import functools
import re


CMD_PREFIX = re.compile(r'^\$ ', re.MULTILINE)


class Node:

    def __init__(self, name, size=0):
        self.parent = None
        self.name = name
        self._size = size
        self.children = {}
        self._indent = 0

    def add_child(self, node):
        node.parent = self
        self.children.setdefault(node.name, node)
        return self

    @property
    def size(self):
        if self._size > 0:
            return self._size
        total = 0

        for child_name, child in self.children.items():
            total += child.size

        self._size = total
        return self._size

    def __repr__(self):
        return f"{self.path} size={self.size}"

    def path(self):
        this = self
        parent_names = []
        path = '/'
        while this.parent is not None:
            parent_names.append(this.parent.name)
            this = this.parent
        parent_names.reverse()
        for parent_name in parent_names[1:]:
            if parent_name != '/':
                path += f'{parent_name}/'
        path += self.name
        return path


def build_tree(data):
    # build tree
    split_cmds = CMD_PREFIX.split(data)[1:]

    root = Node('/')

    visitor = root

    for line in split_cmds:
        line = line.strip()
        if not line:
            continue
        cmd, *results = line.splitlines()

        if 'cd /' == cmd:
            visitor = root
        elif 'cd ..' == cmd:  # up
            if visitor.parent is not None:
                visitor = visitor.parent
        elif cmd.startswith('cd '):  # into
            dest_name = cmd.split()[-1]
            assert dest_name != '/', "unexpected / for cd destination"
            assert dest_name, "expected dest_name, got:" + dest_name
            if dest_name not in visitor.children:
                # haven't been here yet
                visitor.add_child(
                    Node(name=dest_name)
                )
            visitor = visitor.children[dest_name]
        elif 'ls' == cmd:
            for child_rec in results:
                t1, child_name = child_rec.split()
                if 'dir' == t1:
                    child = Node(name=child_name)
                else: # file
                    size = int(t1)
                    child = Node(name=child_name, size=size)

                visitor.add_child(child)
        else:
            raise Exception(f"Unexpected: {cmd}")

    return root


def part1(data):
    result = 0
    UPPER_BOUND = 100000
    root = build_tree(data)

    results = []
    def visit(node):
        if not isinstance(node, Node):
            return
        if node.children and node.size <= UPPER_BOUND:
            results.append(node)

        for name, child in node.children.items():
            visit(child)
    visit(root)
    assert results
    return sum(d.size for d in results)


def part2(data):
    result = 0

    return result


import pytest

sample = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip()

def test_part1_sample():
    assert 95437 == part1(sample)

# def test_part2_sample():
#     assert 70 == part2(sample)


if __name__ == "__main__":
    with open('input07.txt', 'rt') as f:
        result = part1(f.read())
        print('part1:', result)
        f.seek(0)
        result = part2(f)
        print('part2:', result)
