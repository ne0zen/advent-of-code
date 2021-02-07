#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass(frozen=True)
class Field:
    name: str
    ranges: [range]


def parse_input(data):
    fields = []
    ranges = []
    your_ticket = None
    nearby_tickets = []
    line_iter = iter(data)

    def next_line():
        return next(line_iter).strip()

    # parse fields w/ ranges
    while line := next_line():
        assert ":" in line
        name, _, raw_ranges = line.partition(": ")
        assert " or " in raw_ranges
        parsed_ranges = []
        for raw_range in raw_ranges.split(" or "):
            lower, upper = map(int, raw_range.split("-"))
            upper = upper + 1
            parsed_ranges.append(range(lower, upper))

        fields.append(Field(name=name, ranges=tuple(parsed_ranges)))

    assert next_line() == "your ticket:"
    your_ticket = [int(item) for item in next_line().split(",")]
    assert "" == next(line_iter).strip()  # skip blank line

    assert next_line() == "nearby tickets:"
    for line in line_iter:
        ticket = [int(number) for number in line.strip().split(",")]
        nearby_tickets.append(ticket)

    return fields, your_ticket, nearby_tickets


def get_invalid_values(fields, nearby_tickets):
    invalid_values = set()

    for ticket in nearby_tickets:
        for value in ticket:
            valid_for = []
            for field in fields:
                for some_range in field.ranges:
                    if value in some_range:
                        valid_for.append(some_range)
            if 0 == len(valid_for):
                invalid_values.add(value)
    return invalid_values


def get_field_order(fields, nearby_tickets):
    invalid_values = get_invalid_values(fields, nearby_tickets)

    valid_tickets = [
        ticket for ticket in nearby_tickets if not invalid_values.intersection(ticket)
    ]

    # compute possibilities for each column
    possibilities_by_column_index = [set() for _ in range(len(fields))]
    for column_idx in range(len(fields)):
        for field in fields:
            if all(
                any(ticket[column_idx] in arange for arange in field.ranges)
                for ticket in valid_tickets
            ):
                possibilities_by_column_index[column_idx].add(field.name)
    # refine possibilities to field order
    field_order = [0] * len(fields)
    while True:
        next_field_names = set()
        for i, possibilities in enumerate(possibilities_by_column_index):
            num_possibilities = len(possibilities)
            if possibilities == None or num_possibilities == 0:
                continue
            elif num_possibilities == 1:
                field_name = possibilities.pop()
                next_field_names.add(field_name)
                field_order[i] = field_name
                possibilities = None
        # remove found field_names from possibilities of all columns
        for possibilities in possibilities_by_column_index:
            num_possibilities = len(possibilities)
            if possibilities == None or num_possibilities == 0:

                continue
            possibilities -= next_field_names
        if len(next_field_names) == 0:
            break

    return field_order


if __name__ == "__main__":
    import operator
    import functools

    with open("input16.txt", "rt") as f:
        fields, your_ticket, nearby_tickets = parse_input(f)
        field_names = [field.name for field in fields]
        invalid_values = get_invalid_values(fields, nearby_tickets)
        print("part1:", sum(invalid_values))

        # part 2
        field_order = get_field_order(fields, nearby_tickets)
        departure_field_names = [
            field_name
            for field_name in field_names
            if field_name.startswith("departure")
        ]
        print("departure_field_names:", departure_field_names)
        assert 6 == len(departure_field_names)

        departure_field_values = [
            your_ticket[field_order.index(field_name)]
            for field_name in departure_field_names
        ]
        assert 6 == len(departure_field_values)

        print("departure_field_values:", departure_field_values)
        total = functools.reduce(operator.mul, departure_field_values, 1)
        print("part2:", total)


def test_parse():
    data = """
    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12
    """.strip().split(
        "\n"
    )
    fields, your_ticket, nearby_tickets = parse_input(data)
    assert ["class", "row", "seat"] == [field.name for field in fields]
    assert [7, 1, 14] == your_ticket
    assert nearby_tickets == [
        [7, 3, 47],
        [40, 4, 50],
        [55, 2, 20],
        [38, 6, 12],
    ]


def test_part1():
    data = """
    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12
    """.strip().split(
        "\n"
    )
    fields, your_ticket, nearby_tickets = parse_input(data)
    assert {4, 55, 12} == get_invalid_values(fields, nearby_tickets)


def test_part2():
    data = """
    class: 0-1 or 4-19
    row: 0-5 or 8-19
    seat: 0-13 or 16-19

    your ticket:
    11,12,13

    nearby tickets:
    3,9,18
    15,1,5
    5,14,9
    """.strip().split(
        "\n"
    )
    fields, your_ticket, nearby_tickets = parse_input(data)
    field_order = get_field_order(fields, nearby_tickets)
    assert ["row", "class", "seat"] == field_order
    assert [11, 12, 13] == [
        your_ticket[field_order.index(field_name)] for field_name in field_order
    ]
