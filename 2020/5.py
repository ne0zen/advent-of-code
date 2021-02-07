#!/usr/bin/env python3

ROWS_ON_PLANE = 128
SEATS_IN_ROW = 8

plane = []
for row_num in range(ROWS_ON_PLANE):
    row = []
    for col_num in range(SEATS_IN_ROW):
        row.append((row_num, col_num, row_num*8 + col_num))
    plane.append(row)


def find_seat(boarding_pass):
    row_desc = ''.join(c for c in boarding_pass if c in 'FB')
    col_desc = ''.join(c for c in boarding_pass if c in 'LR')

    assert len(row_desc) == 7
    assert len(col_desc) == 3

    row_lower = 0
    row_upper = 127
    # find row
    for c in row_desc:
        if 'F' == c:
            row_lower = row_lower
            row_upper = row_lower + (row_upper + 1 - row_lower) // 2
        elif 'B' == c:
            row_lower = row_lower + (row_upper + 1 - row_lower) // 2
            row_upper = row_upper
        else:
            raise Exception(f"Unknown row descriptor: {c} in {boarding_pass}")
        #print(c, "row_lower:", row_lower, "row_upper:", row_upper)
    row = plane[row_lower:row_upper][0]

    col_lower = 0
    col_upper = 7
    for c in col_desc:
        if 'L' == c:
            col_upper = col_lower + (col_upper + 1 - col_lower) // 2
        elif 'R' == c:
            col_lower = col_lower + (col_upper + 1 - col_lower) // 2
        else:
            raise Exception(f"Unknown col descriptor: {c} in {boarding_pass}")
        #print(c, "col_lower:", col_lower, "col_upper:", col_upper)
    row_number, col_number, seat_number =row[col_lower]
    return row[col_lower]


if __name__ == "__main__":
    with open('input05.txt', 'rt') as f:
        seat_numbers = []
        for boarding_pass in f:
            boarding_pass = boarding_pass.strip()
            if not boarding_pass:
                continue
            _, _, seat_number = find_seat(boarding_pass)
            seat_numbers.append(seat_number)
        print("part1:", max(seat_numbers))
        f.seek(0)
        # part 2
        #seat_numbers = set(range(128*
        seat_numbers = set(range(ROWS_ON_PLANE * SEATS_IN_ROW))
        for boarding_pass in f:
            boarding_pass = boarding_pass.strip()
            if not boarding_pass:
                continue
            row_num, _, seat_number = find_seat(boarding_pass)
            seat_numbers.discard(seat_number)
        for seat in seat_numbers:
            if seat - 1 not in seat_numbers and seat + 1 not in seat_numbers:
                print("part2:", seat)



def test_find_seat():
    assert (44, 5, 357) == find_seat("FBFBBFFRLR")
    assert (70, 7, 567) == find_seat("BFFFBBFRRR")
    assert (14, 7, 119) == find_seat("FFFBBBFRRR")
    assert (102, 4, 820) == find_seat("BBFFBBFRLL")


