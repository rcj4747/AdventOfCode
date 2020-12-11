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
    # Count all seats around the seat
    count = 0
    # Seach along 8 vectors for the first seat you see
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0),
                  (1, 1), (-1, 1), (1, -1), (-1, -1))

    for row_incr, col_incr in directions:
        row_cur, col_cur = row_num, col_num
        while True:
            row_cur += row_incr
            if row_cur < 0 or row_cur == len(rows):
                break

            col_cur += col_incr
            if col_cur < 0 or col_cur == len(rows[0]):
                break

            if rows[row_cur][col_cur] in (SEAT_EMPTY, SEAT_FILLED):
                count += 1 if rows[row_cur][col_cur] == SEAT_FILLED else 0
                break

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
            elif space == SEAT_FILLED and adj_filled >= 5:
                # Emty the seat
                unchanged = False
                new_rows[row_num][col_num] = SEAT_EMPTY
    return unchanged, new_rows


def count_filled_seats(rows):
    return sum([row.count('#') for row in rows])


def main():
    rows = read_file(sys.argv[1] if len(sys.argv) == 2 else 'input.txt')
    # print('\n'.join([''.join(row) for row in rows]))

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
    # print('\n'.join([''.join(row) for row in rows]))


if __name__ == '__main__':
    main()
