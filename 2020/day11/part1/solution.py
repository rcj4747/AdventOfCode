import copy
import sys
from pprint import pprint  # noqa:


FLOOR = '.'
SEAT_EMPTY = 'L'
SEAT_FILLED = '#'


def read_file(filename):
    with open(filename) as fp:
        return [list(x.strip()) for x in fp.readlines()]


def count_adjacent_seats(rows, row_num, col_num):
    row_prev = (row_num - 1) if (row_num - 1) >= 0 else row_num
    row_next = (row_num + 1) if (row_num + 1) < len(rows) else row_num

    col_prev = (col_num - 1) if (col_num - 1) >= 0 else col_num
    col_next = (col_num + 1) if (col_num + 1) < len(rows[0]) else col_num

    # Count all seats around the seat (and the seat itself)
    count = 0
    for row in rows[row_prev:row_next + 1]:
        count += row[col_prev:col_next + 1].count(SEAT_FILLED)

    # Exclude the seat in the count
    count -= rows[row_num][col_num].count(SEAT_FILLED)
    return count


def process_seating(rows):
    new_rows = copy.deepcopy(rows)
    unchanged = True
    for row_num, row in enumerate(rows):
        for col_num, space in enumerate(row):
            if space == FLOOR:
                continue
            adj_filled = count_adjacent_seats(rows, row_num, col_num)
            if space == SEAT_EMPTY and adj_filled == 0:
                unchanged = False
                new_rows[row_num][col_num] = SEAT_FILLED
            elif space == SEAT_FILLED and adj_filled >= 4:
                # Emty the seat
                unchanged = False
                new_rows[row_num][col_num] = SEAT_EMPTY
    return unchanged, new_rows


def count_filled_seats(rows):
    return sum([row.count('#') for row in rows])


def main():
    rows = read_file(sys.argv[1] if len(sys.argv) == 2 else 'input.txt')
    # pprint(rows)
    print(f'{len(rows) = }')
    print(f'{len(rows[0]) = }')
    count = 0
    while True:
        unchanged, rows = process_seating(rows)
        if unchanged:
            break
        count += 1
        print('.', end='', flush=True)
    print()
    print(f'After {count} iterations the seating is unchanged')
    print(f'{count_filled_seats(rows)} seats are occupied')


if __name__ == '__main__':
    main()
