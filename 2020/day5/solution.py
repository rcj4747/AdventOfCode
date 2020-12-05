from pprint import pprint
from typing import List


def read_file(filename: str) -> List[str]:
    passes = []
    with open(filename, 'r') as fp:
        passes.extend([line.strip() for line in fp])
    return passes


def bisect_range(codes: str, start: int = 0, end: int = 127) -> int:
    """A plane has X rows and Y columns, find the row/column based on bisection

    For each character bisect the rows or columns.

    'F' (front) or 'L' (left) gives us the lower half of the range.
    'B' (back) or 'R' (right) gives us the upper half of the range.

    This function is called with the remaining codes to process and the
    current range of rows/columns.
    """
    length = end - start + 1
    code = codes[0].upper()
    if code == 'F' or code == 'L':
        end = end - (length // 2)
    elif code == 'B' or code == 'R':
        start = start + (length // 2)
    codes = codes[1:]
    ret = start
    if codes:
        ret = bisect_range(codes, start=start, end=end)
    return ret


def main():
    passes = read_file('input.txt')
    highest_id = -1
    # pprint(passes)
    seating = [[0 for _ in range(8)] for _ in range(128)]
    for boarding_code in passes:
        row_codes = boarding_code[:-3]
        col_codes = boarding_code[-3:]
        # print(f'row_codes: {row_codes}\tcol_codes: {col_codes}')

        row = bisect_range(row_codes, start=0, end=127)
        col = bisect_range(col_codes, start=0, end=7)
        # print(f'row: {row} \t\tcol: {col}')

        if seating[row][col]:
            raise Exception(f'Seat {row}, {col} already filled')

        seating[row][col] = 1

        seat_id = row * 8 + col
        highest_id = seat_id if seat_id > highest_id else highest_id
    print(f'Highest seat ID found: {highest_id}')

    for row_num, row in enumerate(seating):
        if row.count(1) == 7:
            col_num = row.index(0)
            print(f'You are in row {row_num}, column {col_num}')
            print(f'Your seat ID is {row_num * 8 + col_num}')

if __name__ == '__main__':
    main()
