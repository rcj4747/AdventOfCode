import math
import sys


def read_file(filename):
    with open(filename) as fp:
        # Modified input has answer to validate tests easily
        answer = int(fp.readline().strip())
        bus_ids = []
        for bus_index, bus_num in enumerate(fp.readline().strip().split(',')):
            if bus_num != 'x':
                bus_ids.append((int(bus_num), bus_index))
        return answer, bus_ids


def main():
    (answer, bus_ids) = read_file(
        # sys.argv[1]if len(sys.argv) == 2 else '2020/day13/part2/test.3417')
        sys.argv[1]if len(sys.argv) == 2 else 'input.txt')
    print(f'{bus_ids = }')

    # Start at the time of the first bus
    cur_start = 0

    # Iterate from the 2nd bus onward
    for index in range(1, len(bus_ids)):
        # Time since prior bus
        time_offset = bus_ids[index][1] - bus_ids[index - 1][1]

        bus_num = bus_ids[index][0]

        # Test the product of an increasing number of buses
        cur_product = math.prod([b[0] for b in bus_ids[:index]])

        # print(f'{index=}\t{bus_num=}\t{cur_product=:16}\t'
        #       f'{cur_start=:16}\t{time_offset=}')
        multiple = 1
        while True:
            # Find a multiple of the current bus product where the new
            # bus (with it's time offset) is aligned.  Start at the current
            # starting point.
            new_start = multiple * cur_product + cur_start + time_offset
            # print(f' {new_start=}')
            if not new_start % bus_num:
                print(f'{bus_num=}\t{cur_product=:16}\t'
                      f'{cur_start=:16}\t{time_offset=}\t{multiple=}')
                # print(f' {multiple=}')
                break
            multiple += 1
        # We can't have a match lower than this point, start the next search
        # from here.
        cur_start = new_start

    # We found the time of the last bus.  The solution is the time of the first
    # bus so we subtract the time offset (index) of the last bus
    solution = cur_start - bus_ids[-1][1]
    print(f'The busses arrive in order first at time {solution}')

    if solution == answer:
        print('Correct answer found')


if __name__ == '__main__':
    main()
