#!/usr/bin/env python3

import re
import graphviz

# sample 1
rules = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip().split('\n')

# sample 2
#rules = """
#shiny gold bags contain 2 dark red bags.
#dark red bags contain 2 dark orange bags.
#dark orange bags contain 2 dark yellow bags.
#dark yellow bags contain 2 dark green bags.
#dark green bags contain 2 dark blue bags.
#dark blue bags contain 2 dark violet bags.
#dark violet bags contain no other bags.
#""".strip().split('\n')


graph = graphviz.Digraph('bag-relations')
graph.attr('graph',  rankdir='BT')
graph.attr('edge', labeldistance='2')


for rule in rules:
    rule = rule.strip()
    parent_color = re.match(r'\w+\s\w+', rule).group()
    #child_matches = re.findall(r'(?P<count>\d+)\s(?P<color>\w+\s\w+)', rule)
    child_matches = re.findall(r'(\d+)\s(\w+\s\w+)', rule)

    for number, child_color in child_matches:
        graph.edge(child_color, parent_color, headlabel=number)
graph.view()
